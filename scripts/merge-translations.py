#!/usr/bin/env python3
"""Merge the translations in translations/ into a Kavita source tree.

Usage: merge-translations.py <kavita-source-dir>

translations/<lang>/ui.json     -> UI/Web/src/assets/langs/<lang>.json
translations/<lang>/server.json -> Kavita.Server/I18N/<lang>.json

A string from translations/ is used when upstream has no translation for that
key or still has the English text. Translations made upstream always win, keys
that no longer exist in en.json are dropped. The result follows the key order
of en.json. Keys that stay untranslated are reported as GitHub warnings.
"""

import json
import sys
from pathlib import Path

TARGETS = {
    "ui.json": Path("UI/Web/src/assets/langs"),
    "server.json": Path("Kavita.Server/I18N"),
}


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def merge(en, upstream, ours, path, stats):
    """Return upstream merged with ours.

    Upstream keys keep their order. A new key is placed after the key that
    precedes it in en.json, so the diff against upstream stays small.
    """
    values = {}
    for key, en_value in en.items():
        name = f"{path}.{key}" if path else key
        up = upstream.get(key)
        mine = ours.get(key)
        if isinstance(en_value, dict):
            values[key] = merge(en_value, up if isinstance(up, dict) else {},
                                mine if isinstance(mine, dict) else {}, name, stats)
        elif isinstance(mine, str) and (up is None or up == en_value):
            values[key] = mine
            stats["applied"] += 1
        elif up is not None:
            values[key] = up
            if mine is not None:
                stats["upstream"] += 1
        else:
            stats["missing"].append(name)
    for key in ours:
        if key not in en:
            stats["stale"].append(f"{path}.{key}" if path else key)

    order = [key for key in upstream if key in values]
    previous = None
    for key in en:
        if key not in values:
            continue
        if key not in order:
            order.insert(order.index(previous) + 1 if previous else 0, key)
        previous = key
    return {key: values[key] for key in order}


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    src = Path(sys.argv[1])
    root = Path(__file__).resolve().parent.parent / "translations"

    for lang_dir in sorted(p for p in root.iterdir() if p.is_dir()):
        lang = lang_dir.name
        for file_name, target_dir in TARGETS.items():
            ours_path = lang_dir / file_name
            if not ours_path.exists():
                continue
            target = src / target_dir / f"{lang}.json"
            en = load(src / target_dir / "en.json")
            upstream = load(target) if target.exists() else {}
            stats = {"applied": 0, "upstream": 0, "missing": [], "stale": []}
            merged = merge(en, upstream, load(ours_path), "", stats)
            with open(target, "w", encoding="utf-8") as f:
                json.dump(merged, f, ensure_ascii=False, indent=4)
                f.write("\n")

            print(f"{target}: {stats['applied']} strings added, "
                  f"{stats['upstream']} already translated upstream, "
                  f"{len(stats['stale'])} stale, {len(stats['missing'])} untranslated")
            if stats["stale"]:
                print(f"  stale (not in en.json): {', '.join(stats['stale'])}")
            if stats["missing"]:
                print(f"::warning file={target}::{len(stats['missing'])} keys have no {lang} "
                      f"translation: {', '.join(stats['missing'])}")


if __name__ == "__main__":
    main()
