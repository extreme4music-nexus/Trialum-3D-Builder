# Trialum 3D World Builder (TWCS)

## 🌿 S7 — NOVEMBER 19 2026 — 360 real GLB + four complete editable garden layouts

**AUTHORITATIVE CURRENT GUIDE.** Previously recorded milestones below are historical; any old note saying that a GLB gallery lives under "Избери 3D просторија…" is obsolete.

### Where to find everything

- **TOP → "Избери 3D просторија…"** contains REAL rooms: Agro Atrium, Warehouse, Cold Storage, Packing, Greenhouse, G01 water core; plus **four complete garden options V1/V2/V3/V4**. No standalone GLB packages here.
- **LEFT → "📦 Готови пакети / тест сцени"** contains all 53 previously visible GLB gallery packages (S7 F01 original 70 tiles, marble F01–F03, soil S01–S03, M01–M03, robotics S7-F/R01, irrigation I01–I06, lighting LED, G-00L fixtures). Select a package to open its fully editable QA scene.
- **LEFT → "Категорија"** filters model cards by asset family. **LEFT → "⬡ Поединечен 3D GLB модел"** is a second dropdown: **all 360 genuine GLBs are listed individually**, grouped by category; choosing one selects it for placement. Search still matches IDs such as `s7-f-r01-humanoid`.
- Removed all special top `S7-F 18`, `G-00L 28`, `IRR 58`, `LED 24`, `S7 F01` buttons and left S7-F/R01/ZIP quick buttons.

### New 22 real 3D plant binaries (total 360)

Based strictly on the Trialum original canonical flora:
`lumemoss` (land), `glowfern` (land), `mineralreed` (land), and `aquaglow` (G01 water).

- Land: **7 physical GLBs per species**: seedling, young, growing, mature, ready-for-transplant, weakened, dead (21).
- Water: **existing 6 Aquaglow GLBs preserved**, plus `aquaglow-ready-for-transplant.glb` (1 new).
- 22 new glTF2 GLBs, 6 preview animation clips each: `idle-sway`, `machine-pass`, `water-react`, `root-settle`, `growth-crossfade`, `droop`. These visual clips do not perform original engine growth.
- Source `tools/b1/build-s7-complete-garden.py`, generated SHA-256 manifest `assets/s7-flora-22-manifest.json`, all physical models in `assets/models/`.

### Four fully equipped edit-ready greenhouse variants

`projects/trialum-s7-complete-garden-v{1,2,3,4}.json`, **873 model instances each**. All have **exactly the same non-floor assets** and exact same physical placement: original greenhouse shell, true G01 water core, original G00L *left at entry* with two nursery RS racks plus four larger RM racks, hologram workstation, empty transport/maintenance machines and R01, four beds G02..G05, irrigation per bed, G01 and per-finger lighting, 4 aquatic and 20 terrestrial **preview** plants.

Only **773 floor tiles** change material palette and pattern:
V1 cream-white marble, V2 black marble contrast, V3 grey-green stone, V4 mixed mosaic. Every tile, rack, hose, lamp, robot and plant has an independent Builder scene object ID and can be moved/rotated/redecorated and saved as JSON.

**Not gameplay:** 25 holes on a S02 tile are only geometry. The canonical engine remains 4 land beds × 5 real slots + 4 aquatic slots. Preview plants are NOT active plantIds, racks do NOT contain invented inventory. All garden scenes have `officialScene:false`, `gameplayWrites:0` and `ownerVisualPass:false`. Pool cutout alignment, physical fit and FPS/visual fidelity require the owner's inspection before use in the game.

### Own Git branch for chosen design

After changing a V1–V4 garden, use top `Handoff · Градина V1…V4` selector (automatically matches opened starter variant), then **🌿 Handoff ↓** to download a self-contained JSON+manifest ZIP. Or **🌿 Гранка ↑** and explicitly confirm to create/update `design/s7-garden-v1` etc. in the **Builder repo only**. The local Python localhost server builds a data-only Git commit in an isolated temporary index, writes **only two handoff files** (`handoff/approved-scene.json`, `handoff/manifest.json`) on that branch, and pushes normally (never force, no checkout, no Game main changes). The chosen branch contains inherited Builder sources but its **branch diff** only contains the two handoff files. You may also use the ZIP manually if GitHub Desktop authentication is unavailable. On Node fallback there is no secure Git publishing, but ZIP still works.

Do not confuse clicking handoff with approving visuals or installing to Trialum. The game implementation stage uses a separate `feature/lw-d-s7-owner-garden-review` branch **only after your physical model and layout PASS** and independent original-engine QA.

**Getting the version:** GitHub Desktop `Trialum-3D-Builder` → `main` → Fetch origin / Pull origin → close the old localhost server → `START-BUILDER-WINDOWS.bat` → `http://127.0.0.1:8765/` → Ctrl+F5. The header should read `BUILDER · 360 GLB`. Preserve your personal JSON drafts; never erase `.git` or your own scenes.

**Handoff/next steps:** [S7 completed visual Builder handoff](docs/S7_COMPLETE_GARDEN_UI_PLANTS_HANDOFF_20261119.md). S7.8-G visuals are now built; next is **owner visual/pass** then **S7.8-H (original-engine action contracts, runtime placement, simulation integration and mobile QA)** and **S7.8-I (complete regression and owner acceptance)**. These next stages are NOT implemented by this editor work.

---

## Historical milestones and instructions (older counts/menus are archived)

## 🌱 Нови S02/S03 почвени GLB и интерактивна 5×5 матрица — 18.11.2026

Builder `main` содржи **135 вистински GLB модели**. Додадени се пет почвени модели: вистинска S02 плочка со **25 физички дупки**, S03 изглед на ископана почва, поединечна земјена влошка, означувач на избрана дупка и демонстрациски никулец.

**Отворање:** GitHub Desktop `Trialum-3D-Builder/main` → Fetch/Pull → затвори го стариот сервер → `START-BUILDER-WINDOWS.bat` → Edge `http://127.0.0.1:8765/`. Во `Избери 3D просторија…` постојат четири нови S02/S03 сцени. Кликни **„🌱 Матрица 5×5“** за преглед на 25 адресабилни точки; со клик додаваш/вадиш само **прегледна земјена влошка** и дупките остануваат отворени ако нема растение.

**Важно:** Матрицата е 3D распоред, НЕ 25 gameplay растителни слотови. Оригиналната игра и понатаму има 4 леи по 5 вистински растителни слотови. Демо никулецот не е вистински plantId. Ниту една промена не е направена во продукциската игра. Старата S7 документација го нарекува ископаниот тип S01, а одобрениот разговорен втор рендер го именуваше S03; именувањето треба да се усогласи пред интеграција.

[Комплетен GLB и 25-slot handoff](docs/S7_SOIL_5X5_ENGINE_BINDING_HANDOFF_20261118.md) · [Реални почвени GLB фајлови](assets/models/) · [Game draft PR #101](https://github.com/extreme4music-nexus/Trialum/pull/101).


## 🪨 F03 — 54 вистински сиво-зелени камени GLB (18.11.2026)

**Сите четири F03 3D рендери добија твој PASS.** Со ова издание се изработени и физички прикачени во GitHub **54 F03 GLB**: 27 мазни (F03-S) и 27 со многу суптилна нерамна текстура (F03-T). **Builder има вкупно 130 вистински GLB модели.**

Двете текстури се изведени од твоите одобрени оригинални сиво-зелени референтни слики (не од генерички замени). Сите форми се вистински затворени 3D тела; проверени се оригиналните мерења, нормали, GLB2 структура и SHA256. Сепак, студискиот рендер и реалното WebGL осветлување не гарантираат пикселска идентичност: **моделите сè уште ја чекаат твојата финална визуелна проверка**.

**Ново во изборникот „Избери 3D просторија…“:** **F03 · СИТЕ 54**, **F03-S · 27 МАЗНИ**, **F03-T · 27 СУПТИЛНО РАПАВИ**, **F03 · СПОРЕДБА**, **F03-S / F03-T · околу вистински G01**. Сите се посебно избирливи, се поместуваат како 3D предмети и не ги менуваат залихите или другите игровни податоци.

**За тестирање:** GitHub Desktop `Trialum-3D-Builder` `main` → Fetch/Pull → затвори го стариот localhost сервер → `START-BUILDER-WINDOWS.bat` → Edge `http://127.0.0.1:8765/`. Ако има локална `.git` lock грешка, користи `CONNECT-GITHUB-WINDOWS.bat` без бришење на проекти или Git метаподатоци.

**Авторитативен handoff:** [54 F03 физички GLB + SHA и CI проверки](docs/S7_F03_54_REAL_STONE_GLB_DELIVERY_20261118.md).


## 🖤 F02 — сите 29 вистински GLB модели од одобрениот црн мермер (18.11.2026)

Builder main сега има **76 физички GLB модели**: оригиналните 47 + **29 црни мермерни F02**. Шарата е изведена од одобрениот студиски рендер — темна црна основа со долги бели и ситни сиво-сребрени мермерни жилки, зачувана во заедничка текстура вградена во вистинските GLB фајлови. Сите 29 бинарни модели имаат идентични Git-хешови во Builder и изолирана Trialum развојна гранка. Не се замени со еднобојни црни блокови.

**Три нови сцени во „Избери 3D просторија…“:**
- **F02 · СИТЕ 29 црни мермерни GLB** — секое парче посебно: цела, две половини, четвртини, функционални рабови/агли, големи L-агли, повисоки рабови, модуларни кривини, мат и текстуриран финиш
- **F02 · закривен црн мермер околу G01** — поединечни црни плочки и рабови покрај вистински базен
- **F02 · сјаен / мат / влажна текстура** — споредба на полирана, мат и микротекстурирана GLB

Локално: затвори стар Builder сервер → GitHub Desktop Builder `main` → **Fetch origin → Pull origin** → `START-BUILDER-WINDOWS.bat` → Edge `http://127.0.0.1:8765/`.

**Важно:** 3D рендерите имаат уметничко осветлување што не може автоматски пикселски да се повтори во Editor; шарата од рендерот е основата на истата текстура, но **твојата финална визуелна проверка на самиот GLB сè уште е потребна**. Зачувувањето на сцени во Builder не ја менува активната игра или Play Store.

[Целосен F02 handoff, 29 модели и SHA манифест](docs/S7_F02_BLACK_MARBLE_RENDER_TO_GLB_HANDOFF_20261118.md).


## ✅ КОМПЛЕТИРАНИ ДВАТА ПОСЛЕДНИ БЕЛО-КРЕМ МЕРМЕРА: F01-H + F01-I (18.11.2026)

**Вкупно 47 вистински GLB во Builder, од нив 21 бело-крем F01-A…F01-I модел.** Веќе се запишани и H и I како физички `.glb` датотеки во GitHub Builder `main` и изолираната Trialum развојна гранка, со идентични бинарни хешови. Сите автоматски проверки се успешни.

- **F01-H:** `assets/models/f01-h-cream-marble-matte-service.glb` — 1×1m, 6cm дебелина, 4mm bevel, фин *honed* мат мермер (roughness 0.70), ист точен оригинален крем-беж F01-A дезен + посебен суптилен normal map.
- **F01-I:** `assets/models/f01-i-cream-marble-fine-textured-wet.glb` — 1×1m, 6cm дебелина, 4mm bevel, ист крем дезен, изразена фина текстура за влажна патека, пореалистична физичка 40×40 мрежа со микрорелјеф + normal map, roughness 0.86. **Ова е визуелна противлизгачка текстура; не се тврди сертифицирано физичко триење.**

**Во Builder:** од горното мени отвори `🤍 F01-H и F01-I · последни крем-мермерни плочки`. Ќе имаш 2 H + 2 I плочки и оригиналната F01-A во средина за споредба, со одделно поместување/ротирање.

**Важна граница:** претходните три F01-G модели добија твое одобрување (PASS). H и I ги чекаат твојот реален визуелен преглед во Builder; тестовите потврдуваат точен 3D фајл, но не е автоматски потврдена естетиката. Ниту една од овие две плочки не е вградена во продукциската игра.

[Точни SHA-256 хешови и целосна евиденција](docs/S7_F01_H_I_COMPLETE_CREAM_MARBLE_HANDOFF_20261118.md) · [Game draft PR #98](https://github.com/extreme4music-nexus/Trialum/pull/98).


## 🛠️ Windows GitHub lock грешки — поправено (18.11.2026)

Ако добиеш `index.lock: No such file or directory` или `ORIG_HEAD.lock: No such file or directory`, проблемот е во локалната `.git` папка/пристап до неа, **не мора да е лозинката на GitHub**. Новиот Builder прикажува точен код и насоки наместо општа порака за автентикација.

**Безбедно тестирање:** Прво зачувај ги дизајните и затвори го стариот Python сервер. Во GitHub Desktop провери `Repository → Show in Explorer` за твојот клон, па во истата папка стартувај `CONNECT-GITHUB-WINDOWS.bat`. Дијагностиката не брише `.git` или lock фајлови, не прави reset и не менува проекти. Ако мине, користи или GitHub Desktop или Builder GitHub ↓/↑, но не паралелно.

Ако `.git` навистина ја нема, не притискај повторно Push/Pull; зачувај копија од `projects/` и сопствените модели, па прво провери ја патеката на репото. **Не е потребно да го бришеш или повторно да го клонираш постојниот клон без проверка.** Прочитај [целосна дијагностика и безбедно обновување](docs/WINDOWS_GIT_LOCK_ERRORS_RECOVERY_20261118.md).


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


## НОВО — F01-F вистинска закривена мермерна плочка (owner render PASS)

Со новото издание Builder содржи **42 физички оригинални/изведени GLB**, од кои **16 се F01 мермер** (A-F). **F01-F** е вистински 32-сегментен glTF2 заоблен мермерен модул, дебел 6 cm со реален 4 mm bevel, вградена и непроменета оригинална F01-A минерална текстура; неговиот концепт-рендер е одобрен од сопственикот, а финалната визуелна проверка на моделот допрва следува.

За да го тестирате: затворете го стариот сервер, GitHub Desktop `main` → Fetch/Pull, стартувајте `START-BUILDER-WINDOWS.bat`, во горниот изборник **„Избери 3D просторија… → 🤍 F01-F · закривен мермер (за проверка)“**. Отвора `projects/trialum-f01-f-radial-wedge-review.json` со вистинскиот GLB и две неизменети одобрени F01-A споредбени плочки. Тестирајте агли/боја/bevel/жилки и зачувајте ги измените како обичен Builder проект.

Моделот е *byte-for-byte* идентичен во `Trialum` [Draft PR #96](https://github.com/extreme4music-nexus/Trialum/pull/96) и `Trialum-3D-Builder` main, со SHA-256 `0b76aaf4870dbb06ded35a961330f7337a172c68fdd0b0092d2e7db78443196c`, 89 948 bytes. [Builder CI](https://github.com/extreme4music-nexus/Trialum-3D-Builder/actions/runs/44186505770) и [Game GLB CI](https://github.com/extreme4music-nexus/Trialum/actions/runs/44186709070) PASS.

**Не е инсталиран во играта/главниот G01/Play Store.** Визуелно одобрување на вистинскиот GLB во Builder пред F01-G, според договорениот квалитетен редослед.


## Вистински Trialum GLB простории — 41 модели (17.11.2026)

Во горниот изборник **„🏛️ Избери 3D просторија…“** се отвораат вистински, уредливи проекти со GLB модели од Trialum:

| Проект | JSON | Што содржи |
|---|---|---|
| 🏛️ Агро лоби | `projects/trialum-agro-atrium.json` | Оригиналниот физички GLB атриум со трите врати |
| 📦 Главно стовариште | `projects/trialum-food-warehouse.json` | Оригиналниот GLB магацин + вистински рафтови, ладилници, транспортери и две прикачени соби |
| ❄️ Разладна комора | `projects/trialum-cold-storage.json` | Одделна физичка GLB соба со оригинални ладилници |
| 📦 Пакување | `projects/trialum-packing-room.json` | Одделна физичка GLB соба со оригинални рафтови и транспортна лента |
| 🌿 Стаклена градина | `projects/trialum-agro-greenhouse.json` | Вистинска S7 GLB обвивка; G01 модулите се присутни, намерно сокриени додека не се одобрат отворите во подот |
| 💧 G01 водно јадро | `projects/trialum-g01-water-core.json` | Сите G01 GLB модели без покривот на градината, за подобро уредување и преглед |

**S7 F01** го отвора претходниот постоечки работен мермерен проект (70 модули); не е избришан. B1 пилотот и шесте вистински Aquaglow растителни стадиуми се во каталогот, но не се фабрикувани во живата игра или во базените.

**Вкупно 41 физички .glb:** 15 оригинални F01 + 24 оригинални историски Trialum GLB + 2 нови **GLB конверзии на оригиналната S5 геометрија** за разладната и пакувањето. Изворните генератори и JSON-рецептите се зачувани во `tools/b1/` и `prototypes/lw-d/`. `assets/TRIALUM_LEGACY_GLB_MANIFEST.json` содржи SHA-256, големина, патека и број на мешови за секој од 26-те дополнителни модели. Бинарните фајлови се Git-tracked — се добиваат со обичен GitHub Desktop **Fetch/Pull** без ZIP.

**Граници:** Builder менува само дизајн/JSON, не залихи, ресурси, Play Store, оригинални Android APK или туѓи домови. Структурните S5/G01/S7 GLB модели во играта имаат сопствен статус; Builder прегледот и CI **не значат автоматски одобрен/инсталиран 3D дизајн во играта**. Визуелна потврда од сопственикот е задолжителна.


Приватен HTML5/Three.js билдер на простории за Trialum. Работи на локален компјутер и чува податоци за дизајн, НЕ ја менува основната игра, 3D engine, акаунти или залихи.

## Стартување на Windows — со GitHub Desktop

1. Во GitHub Desktop избери Clone repository → extreme4music-nexus/Trialum-3D-Builder.
2. Притисни Fetch origin / Pull origin за да ги преземеш и автоматски генерираните вистински GLB модели и локалните Three.js модули.
3. Отвори ја клонираната папка и двојно кликни **START-BUILDER-WINDOWS.bat**.
4. Edge/Chrome ќе се отвори на **http://127.0.0.1:8765/**. Ако се отвори прерано, притисни Refresh. Остави го терминалот отворен додека дизајнираш.

Потребен е Python 3 или Node.js 20+ за локалниот сервер; НЕ ти треба Android Studio, SDK, npm install, домен или облачен хост. По првото преземање на F01 моделите и vendor/ библиотеката, редакторот работи offline.

Ако новиот GitHub Actions bootstrap сè уште не завршил, Windows стартерот автоматски ќе се обиде да ги подготви потребните assets со Python 3. Може и рачно: py -3 scripts/setup.py.

## Прво редење

- Лево избери **F01-A** (цела), **F01-B1/B2** (половини), **F01-C1..C4** (четвртини) или **F01-D** (рабови). Ова е дел од **41 вистински glTF2 GLB модели** (вклучува F01-E агли; со owner review pending), а не нацртани квадрати.
- Кликни **Постави** и кликни на теренот. Избери друг модул, па продолжи да редиш.
- **Избор / Помести / Ротирај** користи ги 3D контролите или запиши точни координати и ротација во инспекторот десно.
- **Десно глувче:** ротирање камера; тркалце: зум; лево влечење: пан; лев клик: избор или лепење, зависно од алатката.
- Мрежа / Snap може 0,05, 0,1, 0,25, 0,5 или 1 метар.
- Површина → Ѕид за вертикални модули. Билдерот ги прикажува ѕидните водилки.
- Ctrl+Z / Ctrl+Y — Undo / Redo; Ctrl+D — копија; Delete — бриши; Ctrl+S — зачувај.
- **Активен вистински проект:** projects/trialum-s7-f01-production.json (70 оригинални F01 модули). Кликни **S7 F01** за да го отвориш дури и ако претходно си зачувал стар демо-проект во браузерот. Стариот projects/example-room.json останува само за архивски тестови.
- Со **Додај GLB** увезуваш свои локални .glb модели до 32MB (се чуваат привремено во IndexedDB за да преживеат освежување).

## Како го пушуваш дизајнот на GitHub

Во Edge или Chrome кликни **Зачувај** → избери го **коренот на клонираното Builder репо**. Билдерот создава проект во папката projects/, а ако си увезувал нови GLB модели, ги снима во assets/models/ и ја ажурира assets/catalog.json.

Отвори GitHub Desktop: ќе ги видиш промените → напиши порака за Commit → Commit to main → Push origin. Јас потоа можам да го преземам твојот JSON распоред од истото репо, да ги интегрирам врските со engine во главната Trialum 3D гранка и да подготвам Android QA.

JSON ↓ презема само распоред. ZIP ↓ го содржи JSON и твоите локално увезени GLB, за пренесување на друга машина. За најлесно GitHub зачувување користи **Зачувај**.

## Изворни GLB

Авторски Python генератори за F01-A/B/C/D/E се синхронизирани од оригиналниот Trialum S7 развој. А истата одобрена крем-бела PBR мермерна текстура. F01-A owner visual PASS; F01-B/C/D автоматски QA PASS и подлежат на визуелен преглед. F01-D рабовите се само прави; аглите се посебен планиран F01-E модул.

## Документи

- **docs/HANDOFF.md** — комплетен recovery handoff за продолжување на друга ChatGPT/Codex сесија.
- **docs/PROJECT_FORMAT.md** — форматот на JSON, позиции, GLB референци и правила за мрежата.
- **docs/SECURITY.md** — ограничувања, сигурносни граници, локално чување.

Ова е независен билдeр за дизајн; не е издание на Trialum Classic/3D или Google Play. Нема реклами, акаунти, серверски операции, игровни залихи, AI меморија или јавна синхронизација.

## Директно GitHub ↓ / GitHub ↑

Со **Python 3** серверот `START-BUILDER-WINDOWS.bat` можеш преку две копчиња да повлечеш и прикачиш *само Builder дизајни*. За работа на компјутерот е потребно Git, клонирано Builder репо (со origin кон `extreme4music-nexus/Trialum-3D-Builder`) и претходно поставена автентикација преку GitHub Desktop, Git Credential Manager или SSH. Билдерот не бара и не чува GitHub лозинки/токени.

**Редослед:** Зачувај → избери корен на клонираното репо → GitHub ↑ (локален commit + push). За нови фајлови користи GitHub ↓ (само ако немаш локални незачувани Git измени), потоа освежи Edge. Секој Push бара експлицитна потврда. Само `projects/`, `assets/models/` и `assets/catalog.json` смеат да се комитираат од копчето. `GitHub ↑` не прави merge во главната Trialum игра и не објавува Android build.

Ако работиш преку Node fallback, GitHub копчињата не се достапни; користи GitHub Desktop или инсталирај Python 3. GitHub Push може да откаже доколку локалниот Git нема автентикација; во тој случај постави Git Credential Manager преку GitHub Desktop. За конфликт, не се користи force push.

## Living Spaces извоз (идниот уредувач во играта)

Копчето **Дом JSON ↓** извезува ограничен data-only опис на дизајнот, со сопствени instance ID, позиции и сопственост. За секој постоечки GLB користи реални димензии од каталогот. Подните/структурните модули остануваат **неуредливи** за играчите; подоцнежниот мебел во слоевите props/decor може да биде уредлив, но не автоматски за AI. Не се увезува автоматски во постојните игри: во-игра одобрување, реални model IDs, backup и серверски дозволи се посебни следни чекори.
