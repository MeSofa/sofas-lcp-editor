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

- **Manifest** — name/author/description/version, image/website, v3 flag, dependencies, version history.
- **Manufacturers** — id, name, description, quote, light/dark colors, icon URL.
- **Frames** — 14-field stat block, mech types, add/remove mount list (repeats allowed),
  variant handling, `y_pos` + `specialty`; traits and core system each with the full
  mechanical builder set below.
- **Weapons** — mount/type, damage (+ save/AoE/AP), range, tags, on-attack/hit/crit/miss,
  SP, cost, all seven flags (skirmish/barrage/no_attack/no_mods/no_core_bonus/no_bonus/no_synergy).
- **Systems** — type, SP, effect, no_bonus/no_synergy flags.
- **Shared mechanical builders** on weapons / systems / frame traits / core system:
  **Actions** (+ cost/pilot/mech/bonus_damage), **Bonuses** (full bonus-id list, value +
  special strings, damage/range/weapon-type/size filters, overwrite/replace — this is what
  Foundry reads for automation), **Synergies** (locations + detail + filters),
  **Counters**, **Deployables** (drones/turrets/mines: stats + nested damage/range/actions/bonuses).
- **Custom tags** — id, name (with `{VAL}`), description, filter_ignore.
- **Export** — flat `.lcp` zip (`lcp_manifest.json` + one file per non-empty category) via
  JSZip; live validation (required fields, unique ids, source/license cross-refs, known bonus ids).
- **Import** — load an existing `.lcp`/`.zip` back in; unknown fields (e.g. weapon `profiles`,
  `ammo`) round-trip untouched.

Validated in-browser: flat zip with correct names; export → import round-trips byte-stable;
generated JSON matches the lancer-data wiki schemas.

Not yet verified: import into a live COMP/CON instance (the real end-to-end check).

### Known gaps vs. the official editor (deferred)

- Weapon **profiles** (multi-mode weapons) and **ammo** lists — round-trip but no UI yet.
- **Integrated / special equipment** ID selectors.
- **Active Effects** objects (the richer status/resist/effect blocks).
- **Weapon Mods** (`weapon-mods.json`) — Phase 2, with the rest of licensed data.
- `deprecated` flag; manufacturer inline SVG icons.
- Layout is `height: 100vh` app-shell — fine standalone, needs tuning for the WP embed.

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
