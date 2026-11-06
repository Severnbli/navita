# Navita

Unofficial build of [Kavita](https://github.com/Kareadita/Kavita) (latest stable release) with fixes and a complete Russian translation. Not affiliated with the Kavita project. For everything else see the official [Kavita](https://github.com/Kareadita/Kavita) and [docs](https://wiki.kavitareader.com).

```sh
docker pull severnbli/navita
```

It is the official `jvmilazz0/kavita` image of the same version with the web UI rebuilt from the changed source and the server translations replaced, so it runs and is configured exactly like Kavita.

## Changes

- Book reader, scroll layout: footnote and other anchor links now scroll to the target, and back links return to the reference instead of the start of the chapter.
- Complete Russian translation of the web UI and the server (error messages and emails). Strings that Kavita has not translated yet are filled in, translations made upstream are kept.

## How it is built

A [workflow](.github/workflows/build.yml) runs daily and on every push. It takes the latest Kavita release, checks that the official image is the same version, and then:

1. applies the patches from [`patches/`](patches) with `git am`;
2. merges [`translations/`](translations) into the source with [`scripts/merge-translations.py`](scripts/merge-translations.py): a string is used when Kavita has no translation for it or still has the English text, keys removed upstream are dropped, and keys that are still untranslated are reported as warnings;
3. publishes the complete changed source as a [release](https://github.com/Severnbli/navita/releases) and pushes the image to Docker Hub as `latest`, `<version>` and `<version>-navita.<commit>`.

`translations/<lang>/ui.json` maps to `UI/Web/src/assets/langs/<lang>.json` and `translations/<lang>/server.json` to `Kavita.Server/I18N/<lang>.json`, with the same key structure as Kavita's `en.json`.

## License

GPL-3.0, like Kavita. The modifications are listed in [NOTICE.md](NOTICE.md), which is also shipped in the image as `/kavita/NAVITA-NOTICE.md`. Source of every image: [releases](https://github.com/Severnbli/navita/releases).
