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

# Service configuration structure defining launch parameters for each service.
# This allows unified handling of different services with varying parameter requirements.
# content_formatter (optional): service key for looking up format template in addon settings
SERVICE_CONFIGS = {
    "netflix": {
        "package": "com.netflix.ninja",
        "action": "android.intent.action.VIEW",
        "requires_content": True,
        "category": "android.intent.category.LEANBACK_LAUNCHER",
        "component": "com.netflix.ninja.MainActivity",
        "extras": '[{"key":"source","value":"30","type":"string"}]',
        "flags": "0x14000000",
        "content_formatter": "netflix",
    },
    "youtube": {
        "package": "com.google.android.youtube.tv",
        "action": "android.intent.action.VIEW",
        "requires_content": True,
        "category": "android.intent.category.LEANBACK_LAUNCHER",
        "content_formatter": "youtube",
    },
    "hbo_max": {
        "package": "com.wbd.stream",
        "action": "android.intent.action.VIEW",
        "requires_content": True,
        "category": "android.intent.category.LEANBACK_LAUNCHER",
        "content_formatter": "hbo_max",
    },
    "viki": {
        "package": "com.viki.android",
        "action": "android.intent.action.VIEW",
        "requires_content": True,
        "category": "",
        "content_formatter": "viki",
    },
    "disney_plus": {
        "package": "com.disney.disneyplus",
        "action": "android.intent.action.VIEW",
        "requires_content": True,
        "category": "android.intent.category.LEANBACK_LAUNCHER",
        "content_formatter": "disney_plus",
    },
    "prime_video": {
        "package": "com.amazon.amazonvideo.livingroom",
        "action": "android.intent.action.VIEW",
        "requires_content": True,
        "category": "android.intent.category.LEANBACK_LAUNCHER",
        "content_formatter": "prime_video",
    },
    "apple_tv": {
        "package": "com.apple.atve.androidtv.appletv",
        "action": "android.intent.action.VIEW",
        "requires_content": True,
        "category": "android.intent.category.LEANBACK_LAUNCHER",
        "content_formatter": "apple_tv",
    },
    "crunchyroll": {
        "package": "com.crunchyroll.crunchyroid",
        "action": "android.intent.action.VIEW",
        "requires_content": True,
        "category": "android.intent.category.LEANBACK_LAUNCHER",
        "content_formatter": "crunchyroll",
    },
    "default": {
        "action": "android.intent.action.VIEW",
        "requires_content": True,
    }
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

# Service package name variations - maps provider keys to lists of possible package names and wildcard patterns
# This allows discovering the same service under different package names or versions
PACKAGE_VARIATIONS = {
    "netflix": ["com.netflix.ninja", "netflix*"],
    "youtube": ["com.google.android.youtube.tv", "youtube*"],
    "hbo_max": ["com.wbd.stream", "com.hbo*", "com.maxgo*"],
    "viki": ["com.viki.android", "viki*"],
    "disney_plus": ["com.disney.disneyplus", "disney*"],
    "prime_video": ["com.amazon.amazonvideo.livingroom", "amazonvideo*"],
    "apple_tv": ["com.apple.atve.androidtv.appletv", "appletv*"],
    "plex": ["com.plexapp.android", "com.plex*"],
    "jellyfin": ["org.jellyfin.androidtv", "jellyfin*"],
    "emby": ["com.mb.androidtv", "com.mb*"],
    "crunchyroll": ["com.crunchyroll.crunchyroid", "crunchyroll*"],
    "paramount_plus": ["com.cbs.ca", "paramount*"],
    "peacock": ["com.peacocktv.peacockandroid", "peacocktv*"],
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

def find_package_for_service(service_key, installed_packages):
    """
    Find the actual installed package for a service by checking multiple possible names and wildcard patterns.
    
    Args:
        service_key: Service identifier (e.g., 'netflix', 'youtube')
        installed_packages: Set of installed package names from the system
    
    Returns:
        Tuple of (found_package, is_exact_match) or (None, False) if not found
    """
    if service_key not in PACKAGE_VARIATIONS:
        return None, False
    
    variations = PACKAGE_VARIATIONS[service_key]
    
    # First, try exact matches
    for variation in variations:
        if not '*' in variation and variation in installed_packages:
            return variation, True
    
    # Then, try wildcard patterns
    for variation in variations:
        if '*' in variation:
            pattern = variation.replace('*', '')
            for pkg in installed_packages:
                if pattern in pkg:
                    return pkg, False
    
    return None, False

def build_url(**kwargs):
    return sys.argv[0] + "?" + urllib.parse.urlencode(kwargs)

# Legacy Netflix launcher for testing and fallback purposes.
# This function directly constructs the StartAndroidActivity 
# command for Netflix using the title_id and addon settings.
# It is kept separate from the generic launch_service function
# to allow for specific handling of Netflix's unique URL formatting and extras.
def legacy_launch_netflix(title_id):
    # use_https = ADDON.getSettingBool("use_https")
    target = (
        f"https://www.netflix.com/watch/{title_id}"
        # if use_https else
        # f"https://www.netflix.com/title/{title_id}"
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

# Content formatters for services with special URL/parameter requirements
def format_content_url(service_key, title_id):
    """
    Format content URL using service-specific template from addon settings.
    
    Args:
        service_key: Service identifier (e.g., 'netflix', 'youtube', 'viki')
        title_id: The content/title identifier to format
    
    Returns:
        Formatted URL with title_id substituted into the template
    """
    format_setting_key = f"format_{service_key}"
    format_template = ADDON.getSetting(format_setting_key)
    
    if not format_template:
        # Fallback: return title_id as-is if no format template is configured
        return title_id
    
    # Replace {title_id} placeholder with the actual content ID
    formatted_url = format_template.format(title_id=title_id)
    
    # Debug: Display formatted URL in popup and wait for OK
    if ADDON.getSettingBool("debug_mode"):
        dialog = xbmcgui.Dialog()
        dialog.ok("Formatted URL (Debug)", formatted_url)
    
    return formatted_url


def format_content(content_id, formatter_type=None):
    """
    Format content according to service-specific requirements.
    
    Args:
        content_id: The content identifier to format
        formatter_type: Service key for looking up format template (e.g., 'netflix', 'youtube')
    
    Returns:
        Formatted content URL or content_id as-is if no formatter specified
    """
    if formatter_type:
        return format_content_url(formatter_type, content_id)
    # Default: return content_id as-is (used for generic services)
    return content_id


# Generic launcher for services using configuration-driven approach
def launch_service(package_id, content_id=None):
    """
    Launch a service with the specified package and optional content.
    Uses SERVICE_CONFIGS to determine launch parameters.
    Falls back to default configuration for unlisted services.
    """
    # Determine service config (try to find by package, otherwise use default)
    service_config = None
    for service_name, config in SERVICE_CONFIGS.items():
        if service_name != "default" and config.get("package") == package_id:
            service_config = config
            break
    
    if not service_config:
        service_config = SERVICE_CONFIGS["default"]

    # Handle case where no content is needed (launch app directly)
    if not content_id:
        xbmc.executebuiltin(
            "StartAndroidActivity("
            f"{package_id},"
            "android.intent.action.MAIN,,"
            "android.intent.category.LEANBACK_LAUNCHER)"
        )
        return

    # Format content according to service requirements
    formatted_content = content_id
    if service_config.get("content_formatter"):
        formatted_content = format_content(content_id, service_config["content_formatter"])

    # Build the StartAndroidActivity command with service-specific parameters
    action = service_config.get("action", "android.intent.action.VIEW")
    category = service_config.get("category", "android.intent.category.LEANBACK_LAUNCHER")
    
    # Build base command
    command_parts = [
        "StartAndroidActivity(",
        f"{package_id},",
        f"{action},,",
        f"{formatted_content},",
    ]
    
    # Add optional flags if specified
    if service_config.get("flags"):
        command_parts.append(f"{service_config['flags']},")
    else:
        command_parts.append(",,")
    
    # Add optional extras if specified
    if service_config.get("extras"):
        command_parts.append(f'"{service_config["extras"]}",')
    else:
        command_parts.append(",,")
    
    command_parts.append(",")
    command_parts.append(f"{category}")
    
    # Add optional component if specified
    if service_config.get("component"):
        command_parts.append(f",{service_config['component']}")
    
    command_parts.append(")")

    command = "".join(command_parts)
    xbmc.executebuiltin(command)

    # The add-on is only launching an external app here. Returning a dummy playable
    # item to Kodi causes the .strm flow to surface a "No playable item" error.
    # Exit cleanly instead of building a content listing.
    return


def configure_services():
    installed_packages = get_installed_packages()
    # Read package and enable settings defined in resources/settings.xml
    addon_path = ADDON.getAddonInfo("path")
    # icon_path = os.path.join(addon_path, "tick_and_cross.png")
    
    for service in sorted(SERVICES.keys()):
        slug = service.lower().replace('+', '_plus').replace(' ', '_')
        pkg_setting = f"package_{slug}"
        enable_setting = f"enable_{slug}"
        icon_image = f"icon_{slug}.png"

        # First, try to find the package by checking variations and wildcards
        found_pkg, is_exact = find_package_for_service(slug, installed_packages)
        
        # If not found, try the configured setting as fallback
        if not found_pkg:
            try:
                found_pkg = ADDON.getSetting(pkg_setting)
            except Exception:
                pass
        
        # If still not found, use the default
        if not found_pkg:
            found_pkg = DEFAULT_PACKAGES.get(slug)
        
        found = found_pkg in installed_packages # if found_pkg else False
        
        # Save the actual found package to settings (or the default if not found)
        try:
            ADDON.setSetting(pkg_setting, found_pkg or "")
        except Exception:
            pass

        # Update the enable flag so UI reflects detected services
        try:
            ADDON.setSettingBool(enable_setting, found)
        except Exception:
            pass

        # Create label with service name and package info
        status = "✓" if found else "✗"
        label = f"[{status}] {service}\n{found_pkg if found_pkg else 'Not found'}"
        
        item = xbmcgui.ListItem(label=label)
        item.setArt({"icon": os.path.join(addon_path, "resources", icon_image)})  # Set icon if available
        
        if found:
            url = build_url(action="launch", package=found_pkg)
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
        # Try to get from settings first (which may have been discovered/saved)
        saved_pkg = ADDON.getSetting(pkg_setting)
        if saved_pkg:
            return saved_pkg
    except Exception:
        pass
    
    # Fall back to default
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

    package = get_package_for_provider(provider_key)
    if not package:
        xbmcgui.Dialog().notification(
            'Stream Launcher',
            f'Unsupported provider: {provider}',
            xbmcgui.NOTIFICATION_WARNING,
            3000
        )
        return
    
    # Use unified launcher for all services.
    # The launcher exits cleanly after starting the external app so Kodi does not
    # report a missing playable item for the .strm link flow.
    launch_service(package, content_key)

    li = xbmcgui.ListItem()
    li.setProperty("IsPlayable", "true")
    xbmcplugin.setResolvedUrl(HANDLE, True, li)

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
