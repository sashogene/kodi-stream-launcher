#!/bin/bash
# Configurable list of files to include in the zip
ADDON_FILES_TO_ZIP=(
    "addon.xml"
    "resources/settings.xml"
    "resources/icon_viki.png"
    "resources/icon_netflix.png"
    "resources/icon_youtube.png"
    "resources/icon_hbo_max.png"
    "Kodi_launcher.png"
    "default.py"
)
rm release/kodi-stream-launcher.zip
zip release/kodi-stream-launcher.zip "${ADDON_FILES_TO_ZIP[@]}" 
cp release/kodi-stream-launcher.zip /nfs/Public/Kodi_development/
