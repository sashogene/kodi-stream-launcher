# kodi-stream-launcher
Add-on for Kodi that launches videos from a streaming library in the corresponding app on Android TV. 

See also the [roadmap](Kodi_Streamer_Roadmap.md).

## Purpose 

Kodi already includes streaming add-ons for online streaming providers, but those are cumbersome to set up and often stop working. At the same time, most devices running Kodi have additional apps that can display the content from the corresponding provider.

Instead of duplicating the streaming capability of the dedicated app, this add-on launches the content chosen from the Kodi library into the external app. The purpose is mainly library integration -- the content is hosted externally, but Kodi can scrape the corresponding metadata and cross-link the information to the locally stored content. At the same time, the Kodi library can be used as an index of favorite content that is hosted elsewhere, and collect under the same interface conceptually related content.

## Implementation

The add-on will use the standart .strm file format for library storage. 

´´´
plugin://plugin.video.streamlauncher/?action=play&provider=netflix&content_id=82682341
´´´ 

Kodi already recognizes this as playable media, and will scrape the metadata. Further, Kodi has a built-in mechanism to respond to links in strm files. In the example above, it will invoke the stream launcher, and will pass on the service provider and content ID as parameters. The add-on will then launch the external service app with a deep link to the content.


