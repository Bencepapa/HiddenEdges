# Hidden Edges · Takart élek

**Puzzles from the drafting table.** A logic game for e-ink readers, drawn like a technical drawing.

Every level is a small set of drawing sheets: views, a top plan, colour sheets, overlays, a revision log. You flip between the sheets and work out the rule of the level from what is drawn on them. The e-ink *ghosting* is part of the game: the sheet you leave stays faintly on the panel, and some puzzles can only be solved by reading that trace.

The game is a single HTML file with a canvas and plain JavaScript. It has no build step and no dependencies apart from one Google Font (Roboto Mono). The sound effects (page turns, overlay flips, pencil scribbles, ruler lines, the approval stamp) are generated in code with the Web Audio API.

## Play

Open `index.html` in a browser. It is made for a 6–8" e-ink tablet (developed on a BigMe B6 Color), but it runs on any phone or desktop browser.

- **Title screen:** pick a language, then a folder:
  - **EASY:** 15 levels.
  - **HARD:** 30 levels.
  - **RANDOM:** generated puzzles, locked until all HARD levels are solved or the password is entered.
- **Contents sheet (00):** every level with a tick box. Tap a row to jump to that level.
- **Header:**
  - **CLEAN:** wipes the ghost image with a black-white flash.
  - **‹ ›:** previous and next level.
  - **List / house icon:** back to the contents sheet or the title screen.
  - **Gear:** settings.
- **Footer:** sheet tabs. Swiping sideways also turns the sheets.

### Settings

| Setting | What it does |
|---|---|
| Line weight | Multiplies every line width. Some levels depend on it. |
| Rendering | Native, 16-level grey, Floyd–Steinberg or Bayer 8×8 dithering, to preview how a panel will show it. |
| E-ink emulation on mobile | Kaleido-style colour and paper tone on a normal screen. |
| Page turn | **Fast:** keeps the ghost image. **Normal:** a short flash on every page or level change. |
| Font size calibration | An offset on every label, or AUTO by screen size. |
| Sound | Paper-and-pen sound effects, synthesised in code with Web Audio (no audio files). |
| Reset progress | Clears EASY, HARD or everything. Resetting HARD locks RANDOM again. |

Progress and settings are kept in the browser's `localStorage`.

## Puzzle types

**HARD (30):** two views → top view, mosaic marks, mirror axis, overlays (rotate, flip, scale), dimension chains, drilled holes and sections, 45° construction of a missing view, grid-overlay prints, false traces, line-weight calibration, revision logs, cube nets, 45° shadows and painted shadows, furnishing by the sun's path.

**EASY (15):** key copying, skyline (visible-tower clues), view picker, tile shapes with triangles, furnishing by simple placement rules.

**RANDOM:** puzzles generated in the browser from a seed (shown as `#seed`; › makes a new one, the star marks a puzzle type as a favourite). Generators so far: view picker, height map, key copying, skyline (unique 4×4 Latin squares), shadow, painted shadow, revision log, dimension chains (blurred while a solver still finds exactly one drawing), tetromino and triangle tile shapes, drill holes (a solver checks that the two views fix every hole), construction (stepped profiles whose front and top views fix the side view), overlays (typed marks fit in exactly one way), cube nets (no other cube rotation gives the same picture) and furnishing. Furnishing has two variants: by the sun's path, where the rules are read from a hidden layout and then loosened while a solver keeps only a few solutions, and by placement rules, with apart, side-by-side and water rules.

## Languages

English, German, Italian and Hungarian. All UI text lives in one JSON table that is embedded in `index.html` (`<script id="i18n">`) and also exported as `i18n/takart-elek-lang.json`.

Each entry has:
- `hu`: the Hungarian source, which is also the lookup key;
- `ctx`: where the text appears, for translators;
- one field per language.

Placeholders such as `{n}` or `{total}` must be kept. An empty field falls back to Hungarian.

To add a language:
1. Fill its field in the table.
2. Add it to the `LANGS` list in `index.html`.
3. Draw its flag in `flag()`.

## Repository layout

```
index.html                 the game
i18n/                      exported language table
tools/i18n/                translation sources and build.py (writes the table into index.html and i18n/)
tools/generators/          Python solvers and generators used to design and verify levels
tools/test-pages/          line/hatch test sheet, display probe, font comparison page, sound test page
```

`tools/generators` holds the scripts that check that levels can be solved and, where it matters, have a unique solution:
- dimension chains;
- drill sections;
- cube nets;
- room layouts with sun, access, apart and water rules;
- skyline puzzles;
- tile shapes.

## Author

Bence Dobos · 2026
