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

params = dict(urllib.parse.parse_qsl(sys.argv[2].lstrip("?")))

def get_installed_packages():
    try:
        output = subprocess.check_output(["pm", "list", "packages"]).decode("utf-8", errors="ignore")
        return {line.replace("package:", "").strip() for line in output.splitlines()}
    except Exception:
        return set()

def build_url(**kwargs):
    return sys.argv[0] + "?" + urllib.parse.urlencode(kwargs)

def launch_title(title_id):
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
    for service, package in SERVICES.items():
        if package in installed_packages:
            ADDON.setSettingBool(f"enable_{service.lower()}", True)
        else:
            ADDON.setSettingBool(f"enable_{service.lower()}", False)   
       
def show_root():
    for show in NETFLIX_SHOWS:
        url = build_url(action="play", title_id=show["id"])
        item = xbmcgui.ListItem(label=show["title"])
        xbmcplugin.addDirectoryItem(HANDLE, url, item, False)

    xbmcplugin.endOfDirectory(HANDLE)

params = dict(urllib.parse.parse_qsl(sys.argv[2][1:]))

if params.len() == 0:
    configure_services()
elif params.get("action") == "play":
    #xbmcgui.Dialog().notification('title_id: ', params["title_id"], xbmcgui.NOTIFICATION_INFO, 3000)
    launch_title(params["title_id"])
else:
    show_root()
