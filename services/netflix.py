# code to start Netflix from a deep-link;
# Legacy Netflix launcher for testing and fallback purposes.
# This function directly constructs the StartAndroidActivity 
# command for Netflix using the title_id and addon settings.
# It is kept separate from the generic launch_service function
# to allow for specific handling of Netflix's unique URL formatting and extras.
from default import ADDON
import xbmc 

def legacy_launch_netflix(title_id):
    target = f"https://www.netflix.com/watch/{title_id}"
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