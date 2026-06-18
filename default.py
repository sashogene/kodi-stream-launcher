import os
import sys
import urllib.parse
import subprocess

import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

ADDON = xbmcaddon.Addon()
HANDLE = int(sys.argv[1])

NETFLIX_SHOWS = [
    {"title": "Stranger Things", "id": "80057281", "thumb": ""},
    {"title": "Wednesday", "id": "81231974", "thumb": ""},
    {"title": "The Witcher", "id": "80189685", "thumb": ""}
]

SERVICES = {
    "Netflix": "com.netflix.ninja",
    "YouTube": "com.google.android.youtube.tv",
    "HBO Max": "com.wbd.stream",
    "Viki": "com.viki.android",
    "Disney+":"com.disney.disneyplus",
    "Prime Video":"com.amazon.amazonvideo.livingroom",
    "Apple TV":"com.apple.atve.androidtv.appletv",
    "Plex":"com.plexapp.android",
    "Jellyfin":"org.jellyfin.androidtv",
    "Emby":"com.mb.androidtv",
    "Crunchyroll":"com.crunchyroll.crunchyroid",
    "Paramount+":"com.cbs.ca",
    "Peacock":"com.peacocktv.peacockandroid"
}

DEFAULT_PACKAGES = {
    "netflix": "com.netflix.ninja",
    "youtube": "com.google.android.youtube.tv",
    "hbo_max": "com.wbd.stream",
    "viki": "com.viki.android",
    "disney_plus": "com.disney.disneyplus",
    "prime_video": "com.amazon.amazonvideo.livingroom",
    "apple_tv": "com.apple.atve.androidtv.appletv",
    "plex": "com.plexapp.android",
    "jellyfin": "org.jellyfin.androidtv",
    "emby": "com.mb.androidtv",
    "crunchyroll": "com.crunchyroll.crunchyroid",
    "paramount_plus": "com.cbs.ca",
    "peacock": "com.peacocktv.peacockandroid"
}

PROVIDER_ALIASES = {
    "max": "hbo_max",
    "hbo max": "hbo_max",
    "hbo_max": "hbo_max",
    "disney+": "disney_plus",
    "disney plus": "disney_plus",
    "primevideo": "prime_video",
    "prime video": "prime_video",
    "apple tv": "apple_tv",
    "paramount+": "paramount_plus",
    "paramount plus": "paramount_plus",
    "youtube tv": "youtube",
    "yt": "youtube"
}

# Parse query parameters from the plugin URL passed by Kodi when the plugin is invoked.
# The parameters are expected to be in the format of a query string (e.g., "?action=play&provider=netflix&content_id=12345").
# The code uses urllib.parse.parse_qsl to parse the query string into a list of key-value pairs, which is
# then converted into a dictionary for easier access to the parameters in the plugin's logic.
params = dict(urllib.parse.parse_qsl(sys.argv[2].lstrip("?")))

# Determine OS and Kodi version for compatibility checks
IS_ANDROID = sys.platform.startswith("linux") and "ANDROID_ARGUMENT" in os.environ
KODI_VERSION = int(xbmc.getInfoLabel("System.BuildVersion").split(".")[0])

# This function retrieves the list of installed packages on the Android TV device by executing the "pm list packages" command and parsing its output. It returns a set of package
def get_installed_packages():
    if not IS_ANDROID:
        return set()
    try:
        output = subprocess.check_output(["pm", "list", "packages"]).decode("utf-8", errors="ignore")
        return {line.replace("package:", "").strip() for line in output.splitlines()}
    except Exception:
        return set()

def build_url(**kwargs):
    return sys.argv[0] + "?" + urllib.parse.urlencode(kwargs)

# Generic launcher for service and title IDs, using Android intents to open the respective app directly to the content.
def launch_service(service_id, title_id=None):
    if service_id == "com.netflix.ninja" and title_id:
        launch_netflix(title_id)
        return

    if not title_id:
        xbmc.executebuiltin(
            "StartAndroidActivity("
            f"{service_id},"
            "android.intent.action.MAIN,,"
            "android.intent.category.LEANBACK_LAUNCHER)"
        )
        return

    if service_id == "com.google.android.youtube.tv":
        xbmc.executebuiltin(
            "StartAndroidActivity("
            f"{service_id},"
            "android.intent.action.VIEW,,"
            f"{title_id},"
            "android.intent.category.LEANBACK_LAUNCHER)"
        )
        return

    xbmc.executebuiltin(
        "StartAndroidActivity("
        f"{service_id},"
        "android.intent.action.VIEW,,"
        f"{title_id},"
        "android.intent.category.LEANBACK_LAUNCHER)"
    )


def launch_netflix(title_id):
    use_https = ADDON.getSettingBool("use_https")
    target = (
        f"https://www.netflix.com/watch/{title_id}"
        if use_https else
        f"https://www.netflix.com/title/{title_id}"
    )
    extras_json = '[{"key":"source","value":"30","type":"string"}]'
    xbmc.executebuiltin(
        "StartAndroidActivity("
        "com.netflix.ninja,"
        "android.intent.action.VIEW,,"
        f"{target},"        
        "0x14000000,"
        f'"{extras_json}",'
        ","
        "android.intent.category.LEANBACK_LAUNCHER,"
        "com.netflix.ninja.MainActivity)"
    )

def configure_services():
    installed_packages = get_installed_packages()
    # Read package and enable settings defined in resources/settings.xml
    for service in sorted(SERVICES.keys()):
        default_pkg = SERVICES[service]
        slug = service.lower().replace('+', '_').replace(' ', '_')
        pkg_setting = f"package_{slug}"
        enable_setting = f"enable_{slug}"

        # Read configured package (fallback to default)
        try:
            pkg = ADDON.getSetting(pkg_setting) or default_pkg
        except Exception:
            pkg = default_pkg

        found = pkg in installed_packages

        # Update the enable flag so UI reflects detected services
        try:
            ADDON.setSettingBool(enable_setting, found)
        except Exception:
            pass

        item = xbmcgui.ListItem(label=("v " if found else "x ") + service)
        if found:
            url = build_url(action="launch", package=pkg)
            xbmcplugin.addDirectoryItem(HANDLE, url, item, False)
        else:
            xbmcplugin.addDirectoryItem(HANDLE, "", item, False)

    xbmcplugin.endOfDirectory(HANDLE)

def get_provider_key(provider):
    if not provider:
        return None

    key = provider.strip().lower().replace(' ', '_')
    return PROVIDER_ALIASES.get(key, key)


def get_package_for_provider(provider_key):
    if not provider_key:
        return None

    pkg_setting = f"package_{provider_key}"
    try:
        return ADDON.getSetting(pkg_setting) or DEFAULT_PACKAGES.get(provider_key)
    except Exception:
        return DEFAULT_PACKAGES.get(provider_key)


def handle_play_action(provider, content_id):
    provider_key = get_provider_key(provider)
    content_key = content_id

    if not provider_key or not content_key:
        xbmcgui.Dialog().notification(
            'Stream Launcher',
            'Missing provider or content_id',
            xbmcgui.NOTIFICATION_WARNING,
            3000
        )
        return

    if provider_key == 'netflix':
        launch_netflix(content_key)
        return

    package = get_package_for_provider(provider_key)
    if not package:
        xbmcgui.Dialog().notification(
            'Stream Launcher',
            f'Unsupported provider: {provider}',
            xbmcgui.NOTIFICATION_WARNING,
            3000
        )
        return

    launch_service(package, content_key)


def show_root():
    for show in NETFLIX_SHOWS:
        url = build_url(action="play", title_id=show["id"])
        item = xbmcgui.ListItem(label=show["title"])
        xbmcplugin.addDirectoryItem(HANDLE, url, item, False)

    xbmcplugin.endOfDirectory(HANDLE)

#params = dict(urllib.parse.parse_qsl(sys.argv[2][1:]))

if params == {}:
    configure_services()
elif params.get("action") == "play":
    handle_play_action(
        params.get("provider"),
        params.get("content_id")
    )
else:
    show_root()
