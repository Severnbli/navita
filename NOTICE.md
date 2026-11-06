# Navita – unofficial modified build of Kavita

This image is a modified version of Kavita (https://github.com/Kareadita/Kavita),
built from Kavita release __TAG__. It is not made, endorsed or supported by the
Kavita project (Kareadita). Report problems with this image to
https://github.com/__REPO__/issues, not to the Kavita project.

## License

Kavita is free software licensed under the GNU General Public License version 3.
This modified version is distributed under the same license, without any warranty.
The full license text is in /kavita/LICENSE.txt and
https://github.com/__REPO__/blob/navita/LICENSE.

## Modifications

Modified by Severnbli. Modification date of each change is given below and in the
modified source files.

- 2026-11-05 – UI/Web/src/app/book-reader/_components/book-reader/book-reader.component.ts:
  in the book reader's default (scroll) layout, links to anchors (footnotes and
  their back links) scrolled to a wrong position because the offset was computed
  against the window instead of the scrolling reader container.
- 2026-11-06 – UI/Web/src/assets/langs/ru.json and Kavita.Server/I18N/ru.json:
  the Russian translation of the web UI and the server was completed. Strings
  missing from the upstream translation or still in English were added from
  translations/ru/ by scripts/merge-translations.py.

Only the web UI (/kavita/wwwroot) and the server translations (/kavita/I18N)
are replaced. Everything else in this image is taken unchanged from the
official image __BASE_IMAGE__.

## Corresponding source

- Complete source of this build (Kavita __TAG__ with the modifications applied,
  plus the build scripts): release __RELEASE__ at
  https://github.com/__REPO__/releases/tag/__RELEASE__
- Patches, translations and build scripts: https://github.com/__REPO__/tree/__NAVITA_SHA__
- Unmodified upstream source: https://github.com/Kareadita/Kavita/tree/__TAG__
