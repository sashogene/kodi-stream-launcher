# Next steps in priority order

## 1. Iron out errors during start-up
## 2. Ad icons and artwork
## 3. Create a demo page
## 4. Make package
## 5. See the rest of the roadmap


## 1. Formalize the `.strm` format (Highest ROI)

Right now we've proven that Kodi can act as a launcher for external streaming services.

I'd define a service-agnostic `.strm` format before adding more providers.

For example:

```text
plugin://plugin.video.streamlauncher/?action=play&provider=netflix&content_id=82682341
```

```text
plugin://plugin.video.streamlauncher/?action=play&provider=youtube&content_id=dQw4w9WgXcQ
```

```text
plugin://plugin.video.streamlauncher/?action=play&provider=viki&content_id=1271001v
```

```text
plugin://plugin.video.streamlauncher/?action=play&provider=max&content_id=abcdef
```

Then your add-on becomes a generic router:

```python
service = parsed.service
content_id = parsed.id

launchers[service](content_id)
```

This will make adding new services trivial.

---

* Done!

## 2. Create a launcher abstraction layer

Instead of:

```python
launch_netflix(id)
launch_viki(id)
launch_youtube(id)
```

create:

```python
class ServiceLauncher:
    package
    activity
    category
    extras
    url_template
```

Example:

```python
SERVICES = {
    "netflix": {
        "package": "com.netflix.ninja",
        "activity": "com.netflix.ninja.MainActivity",
        "url": "https://www.netflix.com/watch/{id}",
        "extras": '[{"key":"source","value":"30","type":"string"}]'
    }
}
```

Then support for a new service is mostly configuration.

---

* Done!

## 3. YouTube should probably come next

YouTube TV is usually much friendlier to deep linking than Netflix.

Package is commonly:

```text
com.google.android.youtube.tv
```

or

```text
com.google.android.youtube.tvunplugged
```

depending on device.

If you can get YouTube working, you'll have a second validation that the framework is generic.

---

* Done!

## 4. HBO Max / Max

The package currently tends to be:

```text
com.wbd.stream
```

but changes more often than Netflix.

You'll likely need package discovery logic.

---

## 5. Viki

Viki is interesting because it may accept web URLs more readily than native deep links.

That could simplify the launcher considerably.

---

## 6. GitHub repository

I'd suggest organizing it immediately as:

```text
kodi-stream-launcher/
├── addon.py
├── resources/
├── services/
│   ├── netflix.py
│   ├── youtube.py
│   ├── max.py
│   └── viki.py
├── strm_parser.py
├── README.md
└── docs/
```

This will make community contributions much easier.

For GitHub, use URL citations for navigation:

* [GitHub Docs](https://docs.github.com)
* [Kodi Add-on Development Guide](https://kodi.wiki/view/Add-on_development)

---

## 7. Full Kodi Library Integration

This is where things get really interesting.

A mature solution would:

### Scan

```text
Netflix
 └─ Breaking Bad
     └─ S01E01.strm
```

### Create Kodi library entries

Kodi already treats `.strm` files as playable media.

The challenge is enriching them with metadata.

Typical approach:

```text
.strm
.nfo
poster.jpg
fanart.jpg
```

For example:

```text
Breaking Bad/
 ├─ tvshow.nfo
 ├─ poster.jpg
 ├─ fanart.jpg
 ├─ Season 01/
 │   ├─ Breaking Bad S01E01.strm
 │   ├─ Breaking Bad S01E01.nfo
```

Then Kodi's normal scraper infrastructure handles the rest.

---

## 8. Repository Inclusion

The easiest path is usually:

1. GitHub project.
2. Standalone repository ZIP.
3. Custom Kodi repository add-on.
4. Community adoption.
5. Consider submission to Kodi Foundation repositories later.

I would not worry about official inclusion until you've demonstrated:

* Netflix support
* YouTube support
* One additional streaming provider
* Stable `.strm` integration

---

## A feature I'd add early

Auto-detect installed apps.

Kodi can launch:

```python
StartAndroidActivity(package)
```

to test packages.

Or query Android package information.

Then the UI could show:

```text
Detected Services

✓ Netflix
✓ YouTube
✓ Max
✗ Viki
```

and automatically enable the appropriate launchers.

That would make the add-on much more portable across Android TV devices.

From what you've described, I think you've already crossed the hardest technical hurdle: proving that Kodi 21.2 can generate the exact Android TV intent Netflix requires. Everything else is largely architecture, metadata, and packaging.

