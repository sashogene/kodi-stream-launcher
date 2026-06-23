#!/bin/bash
# Configurable list of files to include in the zip
ADDON_FILES_TO_ZIP=(
    "kodi-stream-launcher/addon.xml"
    "kodi-stream-launcher/resources/settings.xml"
    "kodi-stream-launcher/Kodi_launcher.png"
    "kodi-stream-launcher/default.py"
)
#cd release
rm release/kodi-stream-launcher.zip
zip release/kodi-stream-launcher.zip "${ADDON_FILES_TO_ZIP[@]}" 
cp release/kodi-stream-launcher.zip /nfs/Public/Kodi_development/
