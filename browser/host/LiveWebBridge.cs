// JA21 9.8.7 live-web composition bridge. This is selected only when the Microsoft WebView2 SDK
// adapter has been provisioned. The browser shell, VEC1 lifecycle, policy and evidence
// remain JA21/VEC1; Edge WebView2 is used only as the modern document/media engine.
using System;
using System.IO;
using System.Windows;
using Microsoft.Web.WebView2.Core;
using Microsoft.Web.WebView2.Wpf;

namespace VBJA21
{
    internal static class LiveWebFactory
    {
        public static bool IsAvailable(string root)
        {
            string sdk = PortablePaths.WebView2SdkRoot(root);
            if(!Directory.Exists(sdk) || String.Equals(Environment.GetEnvironmentVariable("JA21_NATIVE_ONLY"), "1", StringComparison.Ordinal)) return false;
            try { CoreWebView2Environment.GetAvailableBrowserVersionString(); return true; } catch { return false; }
        }

        public static string AdapterStatus(string root)
        {
            if (!IsAvailable(root)) return "native-only";
            try { return "WebView2 " + CoreWebView2Environment.GetAvailableBrowserVersionString(); }
            catch { return "WebView2 runtime unavailable"; }
        }

        public static ILiveWebSurface Create(string root, int tabId, bool isPrivate)
        {
            return new WebView2LiveWebSurface(root, tabId, isPrivate);
        }

        public static ILiveWebSurface CreateDossier(string root)
        {
            return new WebView2LiveWebSurface(root, 0, false, true);
        }
    }

    internal sealed class WebView2LiveWebSurface : ILiveWebSurface
    {
        private readonly WebView2 _view;
        private readonly string _root;
        private readonly string _dataDir;
        private readonly bool _private;
        private readonly bool _dossier;
        private bool _ready;
        private bool _disposed;

        public event Action<string, string> NavigationCommitted;
        public event Action<string> StatusChanged;
        public event Action<bool> FullScreenChanged;

        public WebView2LiveWebSurface(string root, int tabId, bool isPrivate)
            : this(root, tabId, isPrivate, false) { }

        public WebView2LiveWebSurface(string root, int tabId, bool isPrivate, bool dossier)
        {
            if (dossier) TrailDossierStartup.Boot("webview-surface-begin");
            _root = root;
            _private = isPrivate;
            _dossier = dossier;
            string state = Environment.GetEnvironmentVariable("JA21_WEB_DATA_ROOT");
            if(String.IsNullOrWhiteSpace(state)) state = PortablePaths.LiveWebState(root);
            Directory.CreateDirectory(state);
            _dataDir = isPrivate
                ? System.IO.Path.Combine(state, "private", "tab-" + tabId.ToString() + "-" + Guid.NewGuid().ToString("N"))
                : System.IO.Path.Combine(state, dossier ? "trail-dossier" : "profile");
            Directory.CreateDirectory(_dataDir);

            // The clean dossier window has no optical browser overlays. A native HWND
            // WebView2 avoids the composition/GPU surface which failed in this runtime.
            _view = new WebView2();
            _view.HorizontalAlignment = HorizontalAlignment.Stretch;
            _view.VerticalAlignment = VerticalAlignment.Stretch;
            CoreWebView2CreationProperties creation = new CoreWebView2CreationProperties { UserDataFolder = _dataDir };
            // Dossier presentation is text, photographs and local SVG maps. Software
            // rendering preserves those features without requiring a working GPU process.
            if (_dossier) creation.AdditionalBrowserArguments = "--disable-gpu";
            string fixedRuntime = PortablePaths.FixedWebView2Root(root);
            if(!String.IsNullOrWhiteSpace(fixedRuntime)) { var bp = creation.GetType().GetProperty("BrowserExecutableFolder"); if(bp != null && bp.CanWrite) bp.SetValue(creation, fixedRuntime, null); }
            _view.CreationProperties = creation;
            PortableFabric.Record("live.web", "surface-create", isPrivate ? "private WebView2 composition surface" : "persistent portable WebView2 composition surface");
            _view.CoreWebView2InitializationCompleted += OnInitialized;
            _view.NavigationStarting += delegate(object sender, CoreWebView2NavigationStartingEventArgs e)
            {
                // WPF NavigationStarting is main-frame only. Local dossier/map iframes
                // and image subresources remain governed by the local app's CSP.
                if (_dossier && !TrailDossierPolicy.IsFixedRoot(e.Uri)) {
                    e.Cancel = true;
                    if (e.IsUserInitiated && !e.IsRedirected) OpenDossierSource(e.Uri);
                    else EmitStatus("Trail Dossier blocked navigation away from the fixed local address.");
                    return;
                }
                Uri target;
                if(Uri.TryCreate(e.Uri,UriKind.Absolute,out target) && (target.Scheme=="http" || target.Scheme=="https"))
                {
                    try { if (!_dossier) JaAddressPolicy.Check(target); }
                    catch(Exception policyEx) { e.Cancel=true; EmitStatus("Live web navigation blocked · "+policyEx.Message); return; }
                }
                else if(Uri.TryCreate(e.Uri,UriKind.Absolute,out target) && target.Scheme!="about")
                { e.Cancel=true; EmitStatus("Live web blocked a non-web navigation scheme."); return; }
                EmitStatus("Loading live web · " + SafeHost(e.Uri));
            };
            _view.NavigationCompleted += delegate(object sender, CoreWebView2NavigationCompletedEventArgs e)
            {
                if (e.IsSuccess) EmitNavigation();
                RecordDiagnostic("navigation-completed", "success=" + e.IsSuccess.ToString() + "; error=" + e.WebErrorStatus.ToString());
                EmitStatus(e.IsSuccess ? "Live web settled" : (_dossier ? "Trail Dossier could not load the local service. Run Start-Hike.cmd, then press F5 to retry." : "Live web navigation failed · " + e.WebErrorStatus.ToString()));
            };
            if (dossier) TrailDossierStartup.Boot("webview-surface-complete");
        }

        private void OnInitialized(object sender, CoreWebView2InitializationCompletedEventArgs e)
        {
            if (_dossier) TrailDossierStartup.Boot(e.IsSuccess ? "webview-initialized" : "webview-initialization-failed");
            if (!e.IsSuccess || _view.CoreWebView2 == null)
            {
                string detail = e.InitializationException == null ? "unknown" : e.InitializationException.GetType().Name + ": " + e.InitializationException.Message;
                RecordDiagnostic("initialization-failed", detail);
                EmitStatus((_dossier ? "Trail Dossier could not initialize its renderer" : "Live web engine could not initialize") + " · " + detail);
                return;
            }
            _ready = true;
            RecordDiagnostic("initialized", EngineLabel + "; host=standard-wpf; software-rendering=" + _dossier.ToString());
            CoreWebView2Settings s = _view.CoreWebView2.Settings;
            s.IsStatusBarEnabled = false;
            s.IsBuiltInErrorPageEnabled = !_dossier;
            s.AreDevToolsEnabled = !_dossier && String.Equals(Environment.GetEnvironmentVariable("JA21_ENABLE_DEVTOOLS"), "1", StringComparison.Ordinal);
            s.IsPasswordAutosaveEnabled = false;
            s.IsGeneralAutofillEnabled = false;
            s.AreDefaultScriptDialogsEnabled = true;
            s.AreDefaultContextMenusEnabled = !_dossier;
            s.IsZoomControlEnabled = true;
            s.AreBrowserAcceleratorKeysEnabled = !_dossier;
            if (_dossier) {
                s.AreHostObjectsAllowed = false;
                s.IsWebMessageEnabled = false;
                s.IsSwipeNavigationEnabled = false;
                _view.CoreWebView2.SourceChanged += delegate {
                    // pushState/replaceState can change a URL without NavigationStarting.
                    // The app keeps day selection in memory, so even hash/query changes
                    // are restored to the exact fixed root.
                    if (!TrailDossierPolicy.IsFixedRoot(Source) && Source != "about:blank")
                        _view.Source = new Uri(TrailDossierPolicy.RootUrl);
                };
            }

            // Some video/player shells apply `cursor:none` while media is active. In a browser-owned
            // virtual desktop that can make the system pointer appear to fall behind the video surface.
            // Install a narrow guard that only overrides elements which explicitly compute to cursor:none;
            // ordinary link/text/resize cursor semantics remain site-controlled.
            string cursorGuard =
                "(function(){" +
                "function ja21CursorGuard(ev){var n=ev&&ev.target?ev.target:null;var hops=0;" +
                "while(n&&n.nodeType===1&&hops++<16){try{if(getComputedStyle(n).cursor==='none')n.style.setProperty('cursor','auto','important');}catch(e){}n=n.parentElement;}}" +
                "document.addEventListener('pointerover',ja21CursorGuard,true);" +
                "document.addEventListener('pointermove',ja21CursorGuard,true);" +
                "document.addEventListener('mousemove',ja21CursorGuard,true);" +
                "})();";
            try { _view.CoreWebView2.AddScriptToExecuteOnDocumentCreatedAsync(cursorGuard); } catch { }
            _view.CoreWebView2.NewWindowRequested += delegate(object o, CoreWebView2NewWindowRequestedEventArgs n)
            {
                if (_dossier) {
                    n.Handled = true;
                    if (n.IsUserInitiated) OpenDossierSource(n.Uri);
                    else EmitStatus("Trail Dossier blocked an automatic popup.");
                    return;
                }
                // Keep web navigation in the omni surface rather than spawning external browser chrome.
                n.Handled = true;
                Uri popup; if(!String.IsNullOrWhiteSpace(n.Uri) && Uri.TryCreate(n.Uri,UriKind.Absolute,out popup) && (popup.Scheme=="http" || popup.Scheme=="https")) Navigate(n.Uri);
                else EmitStatus("Live web blocked a non-web popup target.");
            };
            _view.CoreWebView2.ContainsFullScreenElementChanged += delegate(object o, object args)
            {
                Action<bool> h=FullScreenChanged; if(h!=null)h(_view.CoreWebView2.ContainsFullScreenElement);
            };
            _view.CoreWebView2.PermissionRequested += delegate(object o, CoreWebView2PermissionRequestedEventArgs p)
            {
                // Camera, microphone, geolocation, notifications and clipboard escalation are denied
                // unless explicitly opted in for this launch. Ordinary video playback is unaffected.
                if (!_dossier && String.Equals(Environment.GetEnvironmentVariable("JA21_ALLOW_WEB_PERMISSIONS"), "1", StringComparison.Ordinal)) return;
                p.State = CoreWebView2PermissionState.Deny;
            };
            _view.CoreWebView2.ProcessFailed += delegate(object o, CoreWebView2ProcessFailedEventArgs p)
            {
                string kind = p.ProcessFailedKind.ToString();
                string detail = "kind=" + kind + "; reason=" + EventProperty(p, "Reason") + "; exit=" + EventProperty(p, "ExitCode") + "; process=" + EventProperty(p, "ProcessDescription");
                RecordDiagnostic("process-failed", detail);
                bool fatal = kind == "BrowserProcessExited" || kind == "RenderProcessExited" || kind == "RenderProcessUnresponsive";
                if (_dossier && fatal)
                    EmitStatus("Trail Dossier could not continue · " + detail + ". Press F5, or close and reopen the dossier. Committed hike history remains in the local service.");
                else
                    EmitStatus("Live web process recovery · " + detail);
            };
            _view.CoreWebView2.DownloadStarting += delegate(object o, CoreWebView2DownloadStartingEventArgs d)
            {
                try
                {
                    string path = PortablePaths.UniqueDownloadPath(_root, d.ResultFilePath);
                    d.ResultFilePath = path;
                    PortableFabric.Record("downloads", "download-route", System.IO.Path.GetFileName(path));
                    EmitStatus("Download routed to portable workspace · " + System.IO.Path.GetFileName(path));
                }
                catch(Exception ex) { d.Cancel = true; EmitStatus("Portable download path unavailable · " + ex.Message); }
            };
            EmitStatus("Live web engine ready · " + EngineLabel);
            // Dossier readiness means a successful document navigation, rather
            // than merely starting the renderer with its requested Source set.
            if (!_dossier) EmitNavigation();
        }

        private void EmitNavigation()
        {
            Action<string, string> h = NavigationCommitted;
            if (h == null) return;
            string src = Source;
            string title = DocumentTitle;
            h(src, title);
        }
        private void EmitStatus(string text) { Action<string> h = StatusChanged; if (h != null) h(text); }
        private static string EventProperty(object value, string name)
        {
            try { var property = value.GetType().GetProperty(name); return property == null ? "unavailable" : Convert.ToString(property.GetValue(value, null)); }
            catch { return "unavailable"; }
        }
        private void RecordDiagnostic(string category, string detail)
        {
            if (!_dossier) return;
            try {
                string state = "source=" + Source + "; ready=" + _ready.ToString() + "; profile=" + _dataDir;
                string line = DateTime.UtcNow.ToString("o") + " " + category + " " + detail + "; " + state;
                File.AppendAllText(System.IO.Path.Combine(_dataDir, "trail-dossier-diagnostics.log"), line.Replace("\r", " ").Replace("\n", " ") + Environment.NewLine);
                PortableFabric.Record("live.web", category, detail);
            } catch { }
        }
        private void OpenDossierSource(string raw)
        {
            if (!TrailDossierPolicy.CanOpenSource(raw)) { EmitStatus("Trail Dossier blocked a non-web source link."); return; }
            try { TrailDossierPolicy.OpenSource(raw); }
            catch { EmitStatus("Trail Dossier could not open the source in your default browser."); }
        }
        private static string SafeHost(string raw) { Uri u; return Uri.TryCreate(raw, UriKind.Absolute, out u) ? u.Host : "site"; }

        public FrameworkElement View { get { return _view; } }
        public bool Ready { get { return _ready; } }
        public string EngineLabel
        {
            get
            {
                try { return "Microsoft Edge WebView2 " + CoreWebView2Environment.GetAvailableBrowserVersionString(); }
                catch { return "Microsoft Edge WebView2"; }
            }
        }
        public string Source { get { return _view.Source == null ? "" : _view.Source.AbsoluteUri; } }
        public string DocumentTitle { get { try { return _view.CoreWebView2 == null ? "" : _view.CoreWebView2.DocumentTitle; } catch { return ""; } } }
        public bool CanGoBack { get { try { return _view.CoreWebView2 != null && _view.CoreWebView2.CanGoBack; } catch { return false; } } }
        public bool CanGoForward { get { try { return _view.CoreWebView2 != null && _view.CoreWebView2.CanGoForward; } catch { return false; } } }

        public void Navigate(string url)
        {
            if (_disposed) return;
            if (_dossier && !TrailDossierPolicy.IsFixedRoot(url)) throw new InvalidOperationException("Trail Dossier remains at its fixed local address.");
            Uri u;
            if (!Uri.TryCreate(url, UriKind.Absolute, out u)) throw new Exception("Live web address is not absolute.");
            if(u.Scheme!="http" && u.Scheme!="https") throw new Exception("Live web opens only HTTP or HTTPS addresses.");
            if (!_dossier) JaAddressPolicy.Check(u);
            PortableFabric.Record("live.web", "navigate", u.Host);
            _view.Source = u;
        }
        public void GoBack() { if (CanGoBack) _view.GoBack(); }
        public void GoForward() { if (CanGoForward) _view.GoForward(); }
        public void Reload() { try { if (_view.CoreWebView2 != null) _view.Reload(); } catch { } }
        public void Stop() { try { if (_view.CoreWebView2 != null) _view.CoreWebView2.Stop(); } catch { } }
        public void ClearBrowsingData() { try { if (_view.CoreWebView2 != null) _view.CoreWebView2.Profile.ClearBrowsingDataAsync(); } catch { } }

        public void Dispose()
        {
            if (_disposed) return;
            _disposed = true;
            try { _view.Dispose(); } catch { }
            if (_private)
            {
                try { Directory.Delete(_dataDir, true); } catch { }
            }
        }
    }
}
