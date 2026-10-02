> Source edition: release imagery/runtime assets are excluded. Read [SOURCE_DELIVERY.md](SOURCE_DELIVERY.md) before running.

# Trail Dossier

A Windows treadmill-training companion presented in the JA21 house browser at
`http://127.0.0.1:8765/`. Each dossier covers about ten virtual trail miles.
Workouts and virtual progress are recorded separately; opening the application
does not complete a leg or record exercise.

## Features

- 266 northbound daily dossiers covering the pinned 2,655.84-mile route.
- Topographic and Satellite map views with the same route and checkpoints.
- Ten distinct local photographs per leg, labeled ground or aerial, with
  geographic assignment, source credit, and licensing information.
- Daily preparation, workout records, interactive decisions, and a journal.
- Persistent local progress, explicit completion, exports, and verified backups.
- A clean house-browser window with a fixed local address. The dossier's search
  field remains available.
- A source-aware presenter cache that avoids recompiling unchanged browser code
  on every launch, with visible startup progress and diagnostic timestamps.

## Requirements

- Windows with the installed .NET Framework 4.x WPF components and Windows
  PowerShell used by the house browser.
- Python 3.9 or newer with its standard `sqlite3` module. The service does not
  require Python packages for ordinary use. Content rebuild tools may have
  additional dependencies described in their help.
- Microsoft Edge WebView2 Runtime. The house browser uses WebView2 as its document
  renderer; its shell and navigation policy remain the JA21 house browser.
- A writable project folder. Keep the entire supplied content edition together.

## Start the application

1. Extract or clone the complete project into a writable folder.
2. Double-click **Start-Hike.cmd**.
3. Keep the startup console open while it prepares the house browser. It reports
   progress and confirms when the dossier window is visible.

Use a normal launch first. Administrator access is not required for the local
service, saved history, or browser cache. If Windows explicitly reports an
access-denied error for a protected installation folder, use a writable folder.
If your administrator requires an elevated launch for that location, you may
right-click **Start-Hike.cmd** and select **Run as administrator**. Elevation
does not replace a missing runtime or authorize changes to managed script policy.

The first launch after a browser-source or runtime change builds a new presenter.
Later launches verify and reuse that build. The local cache lives in
`browser/workspace/cache/presenter/`; it is not part of a public source release.

Useful commands from the project folder:

```powershell
.\Start-Hike.cmd -Status
.\Start-Hike.cmd -NoBrowser
.\Start-Hike.cmd -NoPause
```

`-NoBrowser` starts or reuses the local service without opening a window.
`-NoPause` is for scripted use; an ordinary failed double-click keeps its error
message visible. Relaunching reuses a verified service and resumes saved progress.

To stop the owned local service:

```powershell
.\scripts\Stop-Hike.ps1
```

## Startup diagnostics

Read `data/launcher.jsonl` for service and presentation stages, and
`browser/workspace/logs/boot-latest.log` for browser phase timings. Each launch
also has a status file under `browser/workspace/logs/`. A visible window and a
loaded dossier are reported separately. Browser-source and reference changes
invalidate the compiled cache; an altered cache is refused.

Keep the original house-browser distribution separate. This project contains
an independent adapted copy and does not modify the original D: installation.

## Saved data and privacy

Hike history and exercise notes live in `data/hike.sqlite`. Backups, exports,
`config/local.json`, the browser workspace, caches, and launch logs are local
state and must not be committed or uploaded to GitHub. Stop the service before
moving the project or synchronizing an active database to another computer.

The exact itinerary is pinned by checksum. Do not edit it in place for an
existing campaign. The longer operational guide, source notes, backup commands,
and control review are available in [README.html](README.html).

## Source scope

Daily boundaries are virtual checkpoints, rather than verified campsites or
real-world stopping recommendations. Ground photographs are assigned using
archived source geotags; aerial photographs contain route points within their
geographic bounds. Imagery is historical geographic context. Contour intervals
and label units depend on the source; the maps do not calculate treadmill incline.

The 3,720-control register preserves the detailed original requirements and
their current assessments. Registration and implementation status do not
establish full institutional verification or acceptance.

## License and notices

Custom application code and documentation are licensed under **Apache License
2.0**. See [LICENSE](LICENSE), [NOTICE](NOTICE), and [LICENSES.txt](LICENSES.txt).
Route data, ground photographs, map imagery, the adapted house browser, and
third-party components retain their separately documented terms and credits.
The Apache license does not replace those third-party licenses.
