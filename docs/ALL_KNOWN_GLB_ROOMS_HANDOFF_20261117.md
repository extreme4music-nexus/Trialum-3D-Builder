# ALL KNOWN TRIALUM GLB ASSETS → BUILDER (2026-11-17)

## НОВО F01-G — закривен крем-мермерен раб, според одобрениот 3D рендер (18.11.2026)

**45 вистински GLB модели во Builder.** Од нив **3 нови F01-G** се изработени од вистинска 3D геометрија со иста замрзната крем-мермерна текстура F01-A, реално заоблена линија, дебелина 13,5 cm, ширина 19 cm, 8 mm bevel и подискретен сјај (roughness 0.225).

- `f01-g-cream-marble-pool-trim-3m-showcase.glb` — долго **НЕПРЕКИНАТО 3,26 m** заоблено парче, како левиот студиски рендер; изложбен модел.
- `f01-g-cream-marble-pool-trim-1m.glb` — **едно посебно преместливо ~1,09 m парче**, вистински мал закривен раб со 6 mm спој.
- `f01-g-cream-marble-pool-trim-half.glb` — **половина ~0,54 m парче**, за премини/доработка.

**Два тестни проекта во менито „Избери 3D просторија…“:**

1. **✨ F01-G · Долга мермерна лајсна 3D** → `projects/trialum-f01-g-curved-trim-showcase.json`. Трите модели стојат посебно за ротирање и споредување со левиот дел од рендерот.
2. **🤍 F01-G · 7 закривени рабови ОКОЛУ G01** → `projects/trialum-f01-g-pool-curb-g01-preview.json`. Во оригиналниот вистински базен G01 се поставени **седум вистински F01-F мали подни плочки плус седум посебни F01-G завршни рабови**, со ограда, мост и анимирана вода — десниот концепт од рендерот.

**Физички модели во двата репозиториума (исти Git blob и SHA256):** [Game feature branch](https://github.com/extreme4music-nexus/Trialum/tree/feature/lw-d-s7-f01-g-pool-marble-trim-20261118/assets/models) и [Builder main](https://github.com/extreme4music-nexus/Trialum-3D-Builder/tree/main/assets/models). Generator `tools/b1/build-s7-f01-g-pool-trim.py`. [Game source QA SUCCESS](https://github.com/extreme4music-nexus/Trialum/actions/runs/44214935599) и [Builder 45 GLB CI SUCCESS](https://github.com/extreme4music-nexus/Trialum-3D-Builder/actions/runs/44215016691).

**Што не е ветено:** ChatGPT генерираниот рендер не е вистинска CAD мерна документација; не може да се гарантира пиксел-по-пиксел идентичност меѓу студиско осветлување и Edge WebGL. Испораката користи ист дизајн, ист оригинален крем/беж мермер и вистински модуларни физички димензии. **Owner visual GLB PASS сè уште е отворен.** Продукциската игра, Google Play и водните/магацински gameplay слотови не се менувани. За вистинско применување во играта ќе следува посебна ревизија на премините и коридорите покрај мостот.

**Windows:** GitHub Desktop → Builder `main` → Fetch/Pull → затвори стар терминал → `START-BUILDER-WINDOWS.bat` → Edge `http://127.0.0.1:8765/`.


## F01-F — ИСПРАВКА ПО ТВОЈАТА ЗАБЕЛЕШКА: ПЛОЧКИТЕ МОРА ДА БИДАТ ОКОЛУ БАЗЕНОТ
**Претходниот самостоен голем F01-F е ОДБИЕН и заменет; неговите стари 89 948 bytes / r9.15–10.15 m / SHA 0b76… НЕ СЕ ВЕЌЕ ВАЖЕЧКИ.**

Новиот `assets/models/f01-marble-cream-radial-wedge.glb` е **ЕДНА МАЛА САМОСТОЈНА 3D ПЛОЧКА** покрај постојната кружна патека на реалниот G01: r=7.2–8.2 m, 1m радијална ширина и 7.5° модуларен сегмент (околу 1m должина), 24 вистински закривени поделби, 6cm дебелина, 4mm bevel, 6mm фуга, непроменета F01-A PBR текстура. Се повторува во 48 чекори, но **не се поставени 48 во играта**.

Во менито **Избери 3D просторија… → F01-F · закривен мермер** се отвора `projects/trialum-f01-f-radial-wedge-review.json` со **7 посебно избирливи плочки** наредени како закривен крем-мермерен сегмент во самиот G01: заедно со вистинската оригинална ограда, кружна патека, главен базен, три помошни базени, мост и анимирана вода. Сегментите се прикажани како **дизајнерски површински слој** малку над постојната патека, а не се инсталирани во вистинската игра — нема промени на 4-те водни слота или на нивната логика.

Нов GLB SHA256: `982c6d5193bd4b4ea09d59aa099c957a998c24dfa883ac5435f819b756f31e8d` · 83 200 bytes · Git blob `7b759d7206e813761cbd2d70fc2b11b86a4ff25f` идентичен во двете GitHub репоа. Испорака проверена со [Game GLB CI](https://github.com/extreme4music-nexus/Trialum/actions/runs/44191561176) и [Builder CI](https://github.com/extreme4music-nexus/Trialum-3D-Builder/actions/runs/44191681735).

**ВАЖНО:** Коригираниот изглед и поставување во Builder чекаат визуелна проверка од сопственикот. Ова го поправа геометрискиот и сценскиот пропуст, но не тврди дека screenshot е пиксел-по-пиксел идентичен со концептниот рендер.

**Status:** all 42 physical glTF2 binaries are Git-tracked in Builder `main`; owner visual QA pending.
**Game source:** `extreme4music-nexus/Trialum` commit `b801808a5b219284d52c52a8ae8e643700c84478` on the isolated LW-D scene stack; game source / gameplay unchanged by this Builder import.

## Verified model inventory
- **F01 original real marble**: 16 GLB (1 whole, 2 halves, 4 quarters, 4 edge strips, 4 corners, 1 F01-F radial wedge); F01-A owner original visual PASS, other parts pending.
- **Agro Atrium S1**: 1 GLB (`atrium.glb`).
- **Food Warehouse S4**: 7 original GLB (`warehouse-shell.glb`, `smart-storage-rack.glb`, `cold-locker.glb`, `cargo-crates.glb`, `conveyor-sorter.glb`, `holo-inventory-kiosk.glb`, `mini-transporter.glb`).
- **Two original S5 physical annex room layouts converted to new real GLB prefabs**: 2 (`food-cold-annex-shell.glb`, `food-packing-annex-shell.glb`), derived from dimensions and part positions in `warehouse-rooms.mjs`. These are **new GLB conversions**, not misrepresented as prior shipped binaries.
- **S7 Greenhouse original empty shell**: 3 (`greenhouse-shell.glb`, independently inspectable `greenhouse-floor-shell.glb`, `greenhouse-glass-roof-shell.glb`). The latter two are alternatives to parts of the full shell, not extra stacked construction.
- **G01 original candidate water-core**: 6 (main basin, satellites, railings and walkway, bridge, pumps, animated water with original morph-target clip).
- **Aquaglow original stage variants**: 6 (sprout, young, growing, mature, weakened, dead). These are a **library of variations**, not created aquarium plants; original engine only authorizes up to four real live aquatic specimens.
- **B1 original graybox pilot**: 1 (`pilot-room.glb`), historical technical test only, not a finished room.

**Math:** 15 + 1 + 7 + 2 + 3 + 6 + 6 + 1 = **42**. 40 are original real glTF2 sources authored in game (including the new F01-F owner-render-approved wedge); the two S5 annex GLBs are newly extracted from original runtime geometry.

## Source and binary provenance
- Canonical GLB generators mirrored under `tools/b1/` together with exact `scene.json` and `visual-recipe.json` snapshots in `prototypes/lw-d/scenes/`. Only *data* and generators are mirrored; no playable game code, server state or Android assets.
- `scripts/build_all_assets.py` regenerates 26 additional binary models, validates GLB2 headers and mesh structures, verifies byte-exact copies, and creates `assets/TRIALUM_LEGACY_GLB_MANIFEST.json` with SHA256 and sizes.
- `scripts/setup.py` independently regenerates frozen 15 F01 models and pinned Browser Three.js (0.180.0).
- The original two Node generators use pinned build-only Three.js 0.187.0 from `tools/b1/package.json`, matching game source rather than silently altering the geometry generator.
- GitHub Actions `.github/workflows/bootstrap.yml` validates **all 42** and commits binaries to `assets/models/` on Builder `main`. GitHub Desktop Fetch → Pull gets the real files, not temporary Actions artifact ZIPs.
- A separate test ensures the previous inline importmap CSP resolution fix still works with the larger library.

## Ready-to-open editable projects
| UI label | Project JSON | Actual GLBs |
|---|---|---|
| Агро лоби | `projects/trialum-agro-atrium.json` | 1 original atrium scene with source semantic doors |
| Главно стовариште | `projects/trialum-food-warehouse.json` | warehouse shell, real equipment, 2 attached structural annex prefabs |
| Разладна комора | `projects/trialum-cold-storage.json` | original-layout cold annex structural GLB and two real lockers |
| Пакување | `projects/trialum-packing-room.json` | original-layout packing annex GLB, racks and conveyor |
| Стаклена градина | `projects/trialum-agro-greenhouse.json` | original greenhouse shell; G01 candidate parts present but hidden pending physical floor cutouts |
| G01 водно јадро | `projects/trialum-g01-water-core.json` | six real G01 water candidate GLBs; preview only |
| S7 F01 | `projects/trialum-s7-f01-production.json` | preserved 70-part editable original marble tile staging project |

All are Builder data-only layouts. No game stock, per-pet reserves, money, history, account state or authoritative save writes. They do not fabricate greenhouse plants or unlock canonical growth slots.

## Owner QA / next handoff
1. On Windows **exit old localhost terminal**, GitHub Desktop Builder main **Fetch/Pull**, double-click `START-BUILDER-WINDOWS.bat`, Edge `http://127.0.0.1:8765/` → hard refresh.
2. Use **Избери 3D просторија…** to view all six rooms, and **S7 F01** for marble staging. Use the left-category filter to find all 41 real GLBs.
3. Inspect original scene geometry, interior clipping, annex door geometry, camera orbit, GLB animation, selection and inspector. **No CI pass substitutes this owner visual PASS.**
4. Save edits into cloned Builder `projects/` and use GitHub ↑ (commit/push) or GitHub Desktop. Never merge edited design into Trialum main without separate engine integration and owner consent.
5. Ongoing GLB production rule: source generators + matching exact output in both active game development branch and Builder main; filename, hash, pivot, size, visual review status in manifest. Continue one asset family at a time.

**Known limits:** catalogue dimensions for non-F01 modules are UI approximations, not authoritative physical collider bounds. Existing game GLBs use world-space geometry and some roofs obscure interiors; user may hide the structural shell during redesign. Existing standalone G01 core components are *review candidates* with a separate cutout/geometry owner gate; do not label full in-game greenhouse water integration finished based on this project.

## F01-F OWNER RENDER PASS → REAL GLB BUILT

The F01-F 1m radial dry perimeter wedge is a real 89,948-byte model with 32 curved subdivisions/392 triangles and original F01-A embedded PBR image. Its exact SHA256 is `0b76aaf4870dbb06ded35a961330f7337a172c68fdd0b0092d2e7db78443196c`; matching Git blob SHA `2735c84d70220bcf69b391debf3d01f57d85f07f` across both repositories. Open `projects/trialum-f01-f-radial-wedge-review.json` from the new room preset, compare with original A. Game CI and Builder CI are green; owner's physical model PASS still required. Neither source CI nor the earlier concept render certifies a pixel-perfect match under all lighting conditions.
