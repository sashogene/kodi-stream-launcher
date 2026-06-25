#!/bin/bash
# Configurable list of files to include in the zip
ADDON_FILES_TO_ZIP=(
    "kodi-stream-launcher/addon.xml"
    "kodi-stream-launcher/default.py"
    "kodi-stream-launcher/Kodi_launcher.png"
    "kodi-stream-launcher/resources/settings.xml"
    "kodi-stream-launcher/resources/icon_viki.png"
    "kodi-stream-launcher/resources/icon_netflix.png"
    "kodi-stream-launcher/resources/icon_youtube.png"
    "kodi-stream-launcher/resources/icon_hbo_max.png"
)
cd ..
rm kodi-stream-launcher/release/kodi-stream-launcher.zip
zip kodi-stream-launcher/release/kodi-stream-launcher.zip "${ADDON_FILES_TO_ZIP[@]}" 
cp kodi-stream-launcher/release/kodi-stream-launcher.zip /nfs/Public/Kodi_development/
