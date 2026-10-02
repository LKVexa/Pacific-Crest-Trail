$ErrorActionPreference = 'Stop'

function Get-JA21TextSha256([string]$Text) {
    $hasher = [Security.Cryptography.SHA256]::Create()
    try { return ([BitConverter]::ToString($hasher.ComputeHash([Text.Encoding]::UTF8.GetBytes($Text)))).Replace('-', '').ToLowerInvariant() }
    finally { $hasher.Dispose() }
}

function Get-JA21FileSha256([string]$Path) {
    # The portable host redirects APPDATA; avoid relying on a lazily imported
    # Get-FileHash script module in the Windows PowerShell process.
    $stream = [IO.File]::OpenRead($Path)
    $hasher = [Security.Cryptography.SHA256]::Create()
    try { return ([BitConverter]::ToString($hasher.ComputeHash($stream))).Replace('-', '').ToLowerInvariant() }
    finally { $stream.Dispose(); $hasher.Dispose() }
}

function Get-JA21PresenterFingerprint([string]$Code, [string[]]$References) {
    $closure = @($References) + @([object].Assembly.Location, [System.Linq.Enumerable].Assembly.Location, [System.CodeDom.Compiler.CompilerParameters].Assembly.Location, [System.Management.Automation.PSObject].Assembly.Location)
    $records = @()
    foreach ($path in ($closure | Where-Object { $_ } | Sort-Object -Unique)) {
        $full = [IO.Path]::GetFullPath($path)
        if (-not (Test-Path -LiteralPath $full -PathType Leaf)) { throw "Presenter reference is missing: $full" }
        $identity = [Reflection.AssemblyName]::GetAssemblyName($full).FullName
        $records += [ordered]@{ name = [IO.Path]::GetFileName($full); identity = $identity; bytes = (Get-Item -LiteralPath $full).Length; sha256 = Get-JA21FileSha256 $full }
    }
    # Absolute package paths are intentionally absent: identical portable assemblies
    # have identical fingerprints after the independent application is copied.
    $records = @($records | Sort-Object { $_.identity }, { $_.name }, { $_.sha256 })
    $specification = [ordered]@{
        schema = 'JA21/PRESENTER-CACHE/1'
        source_sha256 = Get-JA21TextSha256 $Code
        source_bytes = [Text.Encoding]::UTF8.GetByteCount($Code)
        references = $records
        runtime = [ordered]@{ clr = [Runtime.InteropServices.RuntimeEnvironment]::GetSystemVersion(); environment_version = [Environment]::Version.ToString(); powershell = $PSVersionTable.PSVersion.ToString(); edition = [string]$PSVersionTable.PSEdition; pointer_bytes = [IntPtr]::Size }
        compiler = 'PowerShell Add-Type CSharp library default options'
    }
    $canonical = $specification | ConvertTo-Json -Depth 12 -Compress
    return [pscustomobject]@{ Signature = Get-JA21TextSha256 $canonical; Specification = $specification; Canonical = $canonical }
}

function Import-JA21Presenter([string]$Code, [string[]]$References, [string]$CacheRoot) {
    $fingerprint = Get-JA21PresenterFingerprint $Code $References
    $cache = [IO.Path]::GetFullPath($CacheRoot)
    $directory = Join-Path $cache $fingerprint.Signature
    $assemblyPath = Join-Path $directory 'presenter.dll'
    $manifestPath = Join-Path $directory 'presenter.json'
    New-Item -ItemType Directory -Force -Path $directory | Out-Null
    $mutex = [Threading.Mutex]::new($false, ('Local\JA21PresenterCache_' + $fingerprint.Signature))
    $acquired = $false
    try {
        try { $acquired = $mutex.WaitOne([TimeSpan]::FromSeconds(90)) }
        catch [Threading.AbandonedMutexException] { $acquired = $true }
        if (-not $acquired) { throw 'Another launch is compiling this browser presenter. Retry after it finishes.' }
        $hit = $false
        if ((Test-Path -LiteralPath $assemblyPath -PathType Leaf) -and (Test-Path -LiteralPath $manifestPath -PathType Leaf)) {
            $manifest = Get-Content -LiteralPath $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
            if ($manifest.schema -ne 'JA21/PRESENTER-CACHE/1' -or $manifest.signature -cne $fingerprint.Signature -or $manifest.specification_json -cne $fingerprint.Canonical) { throw 'Presenter cache metadata differs from the current source and reference fingerprint. Refusing to load it.' }
            $actualHash = Get-JA21FileSha256 $assemblyPath
            if ($manifest.dll_sha256 -cne $actualHash -or $manifest.dll_bytes -ne (Get-Item -LiteralPath $assemblyPath).Length) { throw 'Presenter cache binary checksum differs. Refusing to load it.' }
            Write-JA21BootStage 'presenter-cache-hit' $fingerprint.Signature.Substring(0,12)
            $hit = $true
        } else {
            # An incomplete pair is never considered a cache hit. New bytes are
            # compiled to a unique file; publication installs DLL before its seal.
            Write-JA21BootStage 'presenter-cache-miss' $fingerprint.Signature.Substring(0,12)
            $temporary = Join-Path $directory ('build-' + [guid]::NewGuid().ToString('N') + '.dll')
            $temporaryManifest = Join-Path $directory ('build-' + [guid]::NewGuid().ToString('N') + '.json')
            try {
                Write-JA21BootStage 'presenter-compile-begin'
                Add-Type -TypeDefinition $Code -Language CSharp -ReferencedAssemblies $References -OutputAssembly $temporary -OutputType Library -ErrorAction Stop
                $manifest = [ordered]@{ schema = 'JA21/PRESENTER-CACHE/1'; signature = $fingerprint.Signature; specification_json = $fingerprint.Canonical; dll_sha256 = Get-JA21FileSha256 $temporary; dll_bytes = (Get-Item -LiteralPath $temporary).Length; compiled_utc = [DateTime]::UtcNow.ToString('o') }
                [IO.File]::WriteAllText($temporaryManifest, ($manifest | ConvertTo-Json -Depth 5), [Text.UTF8Encoding]::new($false))
                if (Test-Path -LiteralPath $assemblyPath) { [IO.File]::Replace($temporary, $assemblyPath, [System.Management.Automation.Language.NullString]::Value) } else { [IO.File]::Move($temporary, $assemblyPath) }
                if (Test-Path -LiteralPath $manifestPath) { [IO.File]::Replace($temporaryManifest, $manifestPath, [System.Management.Automation.Language.NullString]::Value) } else { [IO.File]::Move($temporaryManifest, $manifestPath) }
                Write-JA21BootStage 'presenter-compile-complete'
            } finally {
                if (Test-Path -LiteralPath $temporary) { Remove-Item -LiteralPath $temporary }
                if (Test-Path -LiteralPath $temporaryManifest) { Remove-Item -LiteralPath $temporaryManifest }
            }
        }
        $assembly = [Reflection.Assembly]::LoadFrom($assemblyPath)
        $program = $assembly.GetType('VBJA21.Program', $false)
        if ($null -eq $program) { throw 'Cached browser presenter is missing its expected entry point.' }
        $entry = $program.GetMethod('Run', [Reflection.BindingFlags]'Public,Static', $null, [Type[]]@([string]), $null)
        if ($null -eq $entry -or $entry.ReturnType -ne [void]) { throw 'Cached browser presenter entry point has an unexpected signature.' }
        Write-JA21BootStage 'presenter-loaded' ($(if ($hit) { 'verified cache' } else { 'verified new build' }))
        return [pscustomobject]@{ CacheHit = $hit; Signature = $fingerprint.Signature; Path = $assemblyPath; Assembly = $assembly }
    } finally {
        if ($acquired) { $mutex.ReleaseMutex() }
        $mutex.Dispose()
    }
}
