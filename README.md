# kodi-stream-launcher
Add-on for Kodi that launches videos from a streaming library in the corresponding app on Android TV. 

## Purpose 

Kodi already includes streaming add-ons for online content providers, but those are cumbersome to set up and often stop working. At the same time, most devices running Kodi have additional apps that can display the content from the corresponding provider.

Instead of duplicating the streaming capability of the dedicated app, this add-on launches the content chosen from the Kodi library into the external app. The purpose is mainly library integration -- the content is hosted externally, but Kodi can scrape the corresponding metadata and cross-link the information to the locally stored content. At the same time, the Kodi library can be used as an index of favorite content that is hosted elsewhere, and collect under the same interface conceptually related content.

## Implementation

The add-on will use the standart .strm file format for library storage. 

```
plugin://plugin.video.streamlauncher/?action=play&provider=netflix&content_id=82682341
```

Kodi already recognizes this as playable media, and will scrape the metadata. Further, Kodi has a built-in mechanism to respond to links in strm files. In the example above, it will invoke the stream launcher, and will pass on the service provider and content ID as parameters. The add-on will then launch the external service app with a deep link to the content.

See also the [roadmap](Kodi_Streamer_Roadmap.md).

## Configuration

When launched from the add-on menu (without parameters), the plugin will perform configuration. That will include scanning the host device for installed relevant streaming apps, and storing the package name.

In addition, settings may include behavior preferences and options to cater to existing and future changes to deep-linking behavior.

A possible implementation may allow for choosing whether to call the external app, or use a built-in renderer for Kodi, when one is available. That way strm links will become more versatile by keeping their original Kodi purpose while adding the ability to serve as external links.

## Library integration

At the concept stage, library entries will be created manually following Kodi naming guidelines and the strm file structure shown above. Future development may include tools for adding content using context menus in Kodi. This is however not a priority, since content addition to Kodi is usually managed on the storage level, and Kodi interface mostly takes care of metadata sccraping.

