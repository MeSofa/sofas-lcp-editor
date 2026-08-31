# LCP Forge

A client-side `.lcp` (Lancer Content Package) generator for [COMP/CON](https://compcon.app).

Goal: match everything the official [`cc-lcp-editor`](https://github.com/massif-press/cc-lcp-editor)
does, plus per-field help text and (later) NPC support — and stay a single static file
so it can be embedded on a WordPress site via a Code Snippet shortcode.

## Running it

It's one self-contained file. Open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8777
```

then visit <http://localhost:8777/index.html>.

Vue 3 and JSZip load from unpkg CDN; everything else is inline. No build step.

## Status — Phase 1 (in progress)

Done:

- **Manifest** editor — name/author/description/version, image/website, v3 flag,
  dependencies, version history.
- **Manufacturers** — id, name, description, quote, light/dark colors, icon URL.
- **Frames** — full stat block (14 fields), mech types, mounts, traits (with actions),
  core system (active/passive, actions), variant handling.
- **Weapons** — mount/type, damage, range, tags, actions, on-attack/hit/crit/miss, SP, cost.
- **Systems** — type, SP, effect, tags, actions.
- **Custom tags** — id, name (with `{VAL}`), description, filter_ignore.
- **Export** — assembles a flat `.lcp` zip (`lcp_manifest.json` + one file per non-empty
  category) via JSZip; live validation blocks broken exports.
- **Import** — load an existing `.lcp`/`.zip` back into the editor.

Validated: export produces a flat zip with the correct file names; export → import
round-trips without data loss; generated JSON matches the lancer-data wiki schemas.

Not yet verified: import into a live COMP/CON instance (the real end-to-end check).

## Next

- Phase 2: remaining Pilot + Licensed data categories (backgrounds, talents, core bonuses,
  pilot gear, reserves, skill triggers, bonds, weapon mods, license collections).
- Phase 3: NPC classes / templates / features — the headline feature the official tool lacks.
- Phase 4: environments, SITREPs, statuses, tables, actions, custom stats, eidolons.
- Embed on the WordPress site via a Code Snippet shortcode.
- Confirm whether Foundry VTT import needs a separate export path.

## Schema reference

<https://github.com/massif-press/lancer-data/wiki> — the wiki is the source of truth.
Re-check it before extending; the schema does shift between COMP/CON releases.
