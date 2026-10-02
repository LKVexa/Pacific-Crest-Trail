using System;

namespace VBJA21
{
    internal static class LiveWebFactory
    {
        public static bool IsAvailable(string root) { return false; }
        public static string AdapterStatus(string root) { return "live-web adapter not provisioned"; }
        public static ILiveWebSurface Create(string root, int tabId, bool isPrivate) { throw new Exception("Live web adapter is not provisioned."); }
        public static ILiveWebSurface CreateDossier(string root) { throw new Exception("Trail Dossier requires the WebView2 live renderer."); }
    }
}
