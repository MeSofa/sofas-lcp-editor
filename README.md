# Sofa's LCP Editor

A client-side `.lcp` (Lancer Content Package) generator for [COMP/CON](https://compcon.app).
(Repo/dir name still `lcp-forge` for history's sake.)

Goal: match everything the official [`cc-lcp-editor`](https://github.com/massif-press/cc-lcp-editor)
does, plus per-field help text and NPC support — and stay a single static file
so it can be embedded on a WordPress site via a Code Snippet shortcode.

## Running it

It's one self-contained file. Open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8777
```

then visit <http://localhost:8777/index.html>.

Vue 3 and JSZip load from unpkg CDN; everything else is inline. No build step.

## Status

Covers licensed data, pilot data, and NPC data. Done:

- **Manifest** — name/author/description/version, image/website, v3 flag, dependencies, version history.
- **Manufacturers** — id, name, description, quote, light/dark colors, icon URL.
- **Frames** — 14-field stat block, mech types, add/remove mount list (repeats allowed),
  variant handling, `y_pos` + `specialty`; traits and core system each with the full
  mechanical builder set below.
- **Weapons** — mount/type, damage (+ save/AoE/AP), range, tags, on-attack/hit/crit/miss,
  SP, cost, all seven flags (skirmish/barrage/no_attack/no_mods/no_core_bonus/no_bonus/no_synergy).
- **Systems** — type, SP, effect, no_bonus/no_synergy flags.
- **CORE Bonuses** — id, name, source, effect, description, mounted_effect + mechanical builders.
- **Talents** — three ranks, each with `exclusive` + the mechanical builders.
- **Skill Triggers** — id, name, description, detail, family.
- **Backgrounds** — id, name, description, example skill ids.
- **Reserves** — type, label, consumable + mechanical builders.
- **Pilot Gear** — Weapon / Armor / Gear; weapons get damage + range; all get tags + builders.
- **NPC Classes** — role, info (flavor/tactics/terse), 13 tiered stats (single or per-tier)
  + tiered size, base/optional feature id lists, optional-selection limits.
- **NPC Templates** — description, forceTag, prohibited templates, feature id lists, caveat,
  selection limits; `"template": true` written automatically.
- **NPC Features** — trait / system / reaction / tech / weapon; per-type fields (reaction
  trigger; tech/weapon attack_bonus + accuracy; weapon: weapon_type, per-tier damage,
  range, attacks, on-attack/hit/crit/miss); tags + actions/bonuses/synergies/deployables.
- **Weapon Mods** — system fields + allowed weapon types/sizes, added tags/damage/range,
  on-attack/hit/crit/miss, plus the mod's own mechanical builders.
- **Bonds** — major/minor ideals, questions (+ suggested answers), powers (frequency,
  prerequisite, veteran/master).
- **Environments** · **SITREPs** (pc/enemy victory, stalemate, deployment, objective,
  extraction) · **Statuses & Conditions** · **Rollable Tables** (die + min/max/result rows)
  · **Custom Stats** (experimental) · **Name Lists** (`lists.json`).
- **Shared mechanical builders** on weapons / systems / frame traits / core system:
  **Actions** (+ cost/pilot/mech/bonus_damage), **Bonuses**, **Synergies**, **Counters**,
  **Deployables** (drones/turrets/mines: stats + nested damage/range/actions/bonuses).
- **Tag picker** — pick core Lancer tags by name from a grouped catalogue (verbatim rules
  text from `lib/tags.json`, `{VAL}` substituted live); the `tg_` id is written for you.
  A ⚙ badge marks tags the Foundry Lancer system actually automates. "Custom / from a
  dependency" escape hatch for arbitrary ids.
- **Bonus picker** — grouped by what each bonus modifies, with the exact "what COMP/CON
  changes" text, value-type hint, PC/NPC scope, and the special-value-string reference
  inline. This is the data Foundry reads for automation.
- **Custom tags** — id, name (with `{VAL}`), description, filter_ignore, with an upfront
  note that custom ids are display-only (no app automates an unknown tag id).
- Every input field has an ⓘ tooltip.
- **Export** — flat `.lcp` zip (`lcp_manifest.json` + one file per non-empty category) via
  JSZip; live validation (required fields, unique ids, source/license cross-refs, known bonus ids).
- **Import** — load an existing `.lcp`/`.zip` back in; unknown fields (e.g. weapon `profiles`,
  `ammo`) round-trip untouched.

Validated in-browser: flat zip with correct names; export → import round-trips byte-stable;
generated JSON matches the lancer-data wiki schemas.

A generated sample pack lives at
[`examples/lcp-forge-test-pack_1.0.0.lcp`](examples/) — install it in COMP/CON to
confirm the toolchain end-to-end (still the one outstanding manual check).

### Not yet in the UI (all round-trip untouched on import)

- Weapon **profiles** (multi-mode weapons) and **ammo** lists.
- **Integrated / special equipment** ID selectors (used by frames, core bonuses, talents, …).
- **Active Effects** objects — the richer status/resist/effect blocks.
- **Base Actions** (`actions.json`) and **Eidolons** (`eidolon_layers.json`) — niche;
  eidolons need the Wallflower LCP and nest NPC features + shards.
- **License collections** (`license_*.json` bundles).
- **NPC collection-style** files (`npcc_*` / `npct_*`) — export is library-style
  (`npc_classes.json` + `npc_features.json`), which COMP/CON also accepts.
- `deprecated` flag; manufacturer inline SVG icons.
- Layout is a `height: 100vh` app-shell — fine standalone, needs tuning for the WP embed.

### UI

- Home tab holds the manifest + a contents overview.
- Each category is a compact list of rows; **clicking a row opens a modal editor**
  (Done / ✕ / Esc / click-outside to close).
- The left nav **toggles from the ☰ button** for a full-width editing area; nav groups
  also collapse individually.
- Button-driven inputs: frame mounts, mech-type presets, weapon types, and the
  bonus/synergy "restrict" filters.
- **Settings panel** on the Home tab: 6 dark themes (COMP/CON, HORUS, Harrison Armory,
  IPS-Northstar, Smith-Shimano, Union), a background-chatter toggle, and an animations toggle.
  Saved to `localStorage` — never touches the exported pack.
- **Comms chatter** — a faint scrolling feed behind the Home screen (COMP/CON style); the lines
  live in the `CHATTER` map near the top of the `<script>` (keyed by theme id), currently
  placeholder text.
- Still to do: item search within long lists; the WordPress embed.

### Editing the comms ticker

In `index.html`, find `const CHATTER = {`. Each key is a theme id; each value is an array
of one-liners that loop across the bottom bar. Edit / add freely — they're just strings.

## Next

- Embed on the WordPress site via a Code Snippet shortcode.
- Confirm whether Foundry VTT import needs a separate export path.
- Aesthetics pass to match the site's Bloom theme.

## Schema reference

<https://github.com/massif-press/lancer-data/wiki> — the wiki is the source of truth.
Re-check it before extending; the schema does shift between COMP/CON releases.
