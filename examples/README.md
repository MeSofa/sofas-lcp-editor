# Examples

## `sample-pack_1.0.0.lcp`

A minimal pack exported straight from the editor — one of each core item type.
Use it to confirm the toolchain works before building real content.

Contents (all fictional, safe to install and uninstall):

| File | Item |
|---|---|
| `manufacturers.json` | **FORGE DYNAMICS** (`FRG`) |
| `frames.json` | **Anvil** (`frg_frame_anvil`) — LL2 Defender, Main+Heavy mounts, one trait with an `armor` bonus, a CORE system ("Immovable Object" / "Anchor") |
| `weapons.json` | **Sledge** (`frg_weapon_sledge`) — LL0 Main Melee, 2d6 Kinetic, Threat 1, Knockback 1 |
| `systems.json` | **Bulwark Field** (`frg_system_bulwark`) — LL1 Shield, 2 SP, Limited 2, a Protocol action |

### To test in COMP/CON

1. <https://compcon.app> → **Content** (jigsaw icon) → **Manage / Import Content**
2. Install `sample-pack_1.0.0.lcp`
3. Check the compendium for FORGE DYNAMICS, then build a pilot with the Anvil
   license and confirm the Sledge, Bulwark Field, trait bonus and CORE system
   all appear.
4. Uninstall it from the same screen when done.
