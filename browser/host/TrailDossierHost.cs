using System;
using System.Diagnostics;
using System.IO;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Media;

namespace VBJA21
{
    internal static class TrailDossierStartup
    {
        private static string _lastStage;
        private static readonly Stopwatch Clock = Stopwatch.StartNew();

        public static void Boot(string stage)
        {
            try {
                if (!String.Equals(Environment.GetEnvironmentVariable("JA21_DOSSIER_MODE"), "1", StringComparison.Ordinal)) return;
                string portable = Environment.GetEnvironmentVariable("JA21_PORTABLE_ROOT");
                if (String.IsNullOrEmpty(portable)) return;
                File.AppendAllText(System.IO.Path.Combine(portable, "logs", "boot-latest.log"),
                    DateTime.UtcNow.ToString("o") + "\t" + stage + "\tmanaged_elapsed_ms=" + Clock.ElapsedMilliseconds.ToString() + Environment.NewLine,
                    new UTF8Encoding(false));
            } catch { }
        }

        public static void Mark(string stage, string detail)
        {
            if (stage == "window-visible" && (_lastStage == "dossier-ready" || _lastStage == "failed")) return;
            _lastStage = stage;
            Boot(stage);
            try
            {
                string path = Environment.GetEnvironmentVariable("JA21_DOSSIER_STARTUP_STATUS");
                string launch = Environment.GetEnvironmentVariable("JA21_DOSSIER_LAUNCH_ID");
                string portable = Environment.GetEnvironmentVariable("JA21_PORTABLE_ROOT");
                Guid id;
                if (String.IsNullOrEmpty(path) || String.IsNullOrEmpty(portable) || !Guid.TryParse(launch, out id)) return;
                string logs = System.IO.Path.GetFullPath(System.IO.Path.Combine(portable, "logs")) + System.IO.Path.DirectorySeparatorChar;
                string target = System.IO.Path.GetFullPath(path);
                if (!target.StartsWith(logs, StringComparison.OrdinalIgnoreCase) ||
                    System.IO.Path.GetFileName(target) != "launch-" + id.ToString() + ".json") return;
                var record = new System.Collections.Generic.Dictionary<string, object> {
                    {"version", 1}, {"launch_id", id.ToString()},
                    {"process_id", Process.GetCurrentProcess().Id},
                    {"at_utc", DateTime.UtcNow.ToString("o")},
                    {"stage", stage}, {"detail", detail ?? String.Empty}
                };
                string temporary = target + "." + Guid.NewGuid().ToString("N") + ".tmp";
                try
                {
                    using (FileStream stream = new FileStream(temporary, FileMode.CreateNew, FileAccess.Write, FileShare.None))
                    using (StreamWriter writer = new StreamWriter(stream, new UTF8Encoding(false)))
                        writer.Write(new System.Web.Script.Serialization.JavaScriptSerializer().Serialize(record));
                    if (File.Exists(target)) File.Replace(temporary, target, null);
                    else File.Move(temporary, target);
                }
                finally { if (File.Exists(temporary)) File.Delete(temporary); }
            }
            catch { /* Startup diagnostics must never prevent the house browser opening. */ }
        }
    }

    // This host owns presentation only. The local service owns hike data and completion.
    public static class TrailDossierPolicy
    {
        public const string RootUrl = "http://127.0.0.1:8765/";

        public static bool IsFixedRoot(string raw)
        {
            // An exact spelling prevents alternate authorities, paths, queries and fragments.
            return String.Equals(raw, RootUrl, StringComparison.Ordinal);
        }

        public static bool CanOpenSource(string raw)
        {
            Uri u;
            if (!Uri.TryCreate(raw, UriKind.Absolute, out u)) return false;
            if (u.Scheme != Uri.UriSchemeHttp && u.Scheme != Uri.UriSchemeHttps) return false;
            if (!String.IsNullOrEmpty(u.UserInfo) || String.IsNullOrEmpty(u.Host)) return false;
            return true;
        }

        public static void OpenSource(string raw)
        {
            if (!CanOpenSource(raw)) throw new InvalidOperationException("Only HTTP or HTTPS source links can open outside Trail Dossier.");
            Uri u = new Uri(raw, UriKind.Absolute);
            // A URL is a structured process target, never a command or shell expression.
            Process.Start(new ProcessStartInfo(u.AbsoluteUri) { UseShellExecute = true });
        }
    }

    internal sealed class TrailDossierWindow : Window
    {
        private readonly ILiveWebSurface _surface;
        private readonly Border _message;
        private readonly TextBlock _messageText;

        public TrailDossierWindow(string root)
        {
            TrailDossierStartup.Boot("window-constructor-begin");
            Title = "Trail Dossier";
            Width = 1360;
            Height = 920;
            MinWidth = 720;
            MinHeight = 520;
            WindowStartupLocation = WindowStartupLocation.CenterScreen;
            WindowStyle = WindowStyle.SingleBorderWindow;
            Background = new SolidColorBrush(Color.FromRgb(7, 27, 33));
            System.Windows.Automation.AutomationProperties.SetName(this, "Trail Dossier");

            // This is a different window class, so address bars, tab rails, drawers,
            // command palettes and general-browser shortcut handlers never exist here.
            Grid content = new Grid();
            _surface = LiveWebFactory.CreateDossier(root);
            content.Children.Add(_surface.View);
            _messageText = new TextBlock {
                Text = "Opening your daily trail dossier...",
                Foreground = Brushes.White,
                FontSize = 18,
                TextWrapping = TextWrapping.Wrap,
                MaxWidth = 620
            };
            _message = new Border {
                Background = Background,
                Padding = new Thickness(30),
                HorizontalAlignment = HorizontalAlignment.Center,
                VerticalAlignment = VerticalAlignment.Center,
                Child = _messageText,
                IsHitTestVisible = false
            };
            content.Children.Add(_message);
            Content = content;

            _surface.NavigationCommitted += delegate(string address, string documentTitle) {
                if (TrailDossierPolicy.IsFixedRoot(address)) {
                    _surface.View.Visibility = Visibility.Visible;
                    _message.Visibility = Visibility.Collapsed;
                    TrailDossierStartup.Mark("dossier-ready", "The fixed local dossier document has loaded.");
                }
                Title = "Trail Dossier";
            };
            _surface.StatusChanged += delegate(string status) {
                if (status.StartsWith("Trail Dossier could not", StringComparison.Ordinal)) {
                    // Native WebView2 owns HWND airspace: hide its failed surface so the
                    // WPF error panel remains readable instead of being obscured by it.
                    _surface.View.Visibility = Visibility.Collapsed;
                    _messageText.Text = status;
                    _message.Visibility = Visibility.Visible;
                    TrailDossierStartup.Mark("failed", status);
                }
            };
            PreviewKeyDown += delegate(object sender, KeyEventArgs e) {
                Key key = e.Key == Key.System ? e.SystemKey : e.Key;
                ModifierKeys mods = Keyboard.Modifiers;
                bool control = (mods & ModifierKeys.Control) != 0;
                bool alt = (mods & ModifierKeys.Alt) != 0;
                if ((control && (key == Key.L || key == Key.K || key == Key.T || key == Key.N || key == Key.W || key == Key.B || key == Key.Tab)) ||
                    (alt && (key == Key.Left || key == Key.Right || key == Key.Home)) ||
                    key == Key.F6 || key == Key.F10 || key == Key.F11 || key == Key.F12 ||
                    key == Key.BrowserBack || key == Key.BrowserForward || key == Key.BrowserHome) e.Handled = true;
                if (key == Key.F5 || (control && key == Key.R)) {
                    _surface.View.Visibility = Visibility.Visible;
                    _message.Visibility = Visibility.Collapsed;
                    _surface.Reload();
                    e.Handled = true;
                }
                // Alt+F4 and the standard Windows title-bar close control remain available.
            };
            ContentRendered += delegate { TrailDossierStartup.Mark("window-visible", "The house browser window is visible."); };
            Loaded += delegate { _surface.Navigate(TrailDossierPolicy.RootUrl); };
            Closed += delegate { _surface.Dispose(); };
            TrailDossierStartup.Boot("window-constructor-complete");
        }
    }

    internal static class TrailDossierHost
    {
        public static bool Enabled { get { return String.Equals(Environment.GetEnvironmentVariable("JA21_DOSSIER_MODE"), "1", StringComparison.Ordinal); } }

        public static void Run(string root)
        {
            TrailDossierStartup.Boot("portable-layout-begin");
            PortablePaths.EnsureLayout(root);
            TrailDossierStartup.Boot("portable-fabric-begin");
            PortableFabric.Configure(root);
            TrailDossierStartup.Boot("runtime-seal-begin");
            RuntimeSeal.Verify(root);
            TrailDossierStartup.Boot("renderer-availability-begin");
            if (!LiveWebFactory.IsAvailable(root))
                throw new InvalidOperationException("Trail Dossier requires the installed WebView2 live renderer. Start the local hike service, then retry with the supported runtime.");
            TrailDossierStartup.Boot("renderer-availability-complete");
            PortableFabric.Record("live.web", "trail-dossier", "fixed local dossier presentation");
            System.Windows.Application app = new System.Windows.Application();
            app.ShutdownMode = ShutdownMode.OnMainWindowClose;
            TrailDossierStartup.Boot("window-create-begin");
            app.Run(new TrailDossierWindow(root));
        }
    }
}
