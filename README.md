# Tendry Epicerie – App Android (Capacitor)

## 📁 Ny firafitry ny dossier (efa vonona)

```
tendry-app/
├── .github/
│   └── workflows/
│       └── build-apk.yml     ← manamboatra APK automatique amin'i GitHub (jereo etsy ambany)
├── package.json
├── capacitor.config.json
├── .gitignore
├── README.md
└── www/                      ← ny app web-nao (tsy azo kasihina ny anaram-baovao)
    ├── index.html
    ├── style.css
    ├── chart.js
    ├── html5-qrcode.min.js
    ├── sw.js
    └── manifest.json
```

Ny dossier `android/` dia **tsy ao anatin'ity** satria mila `npx cap add android` aloha
(mila internet + Node.js, tsy azo atao ato amin'ny chat ity). Rehefa vitanao ilay
dingana etsy ambany dia hipoitra ho azy io dossier android/ io.

## 🛠️ Fitaovana ilaina eo amin'ny solosainao

- **Node.js** (v18 na v20+) – https://nodejs.org
- **Android Studio** (misy Android SDK + JDK 17) – https://developer.android.com/studio

## 🚀 Dingana (ataovy any amin'ny solosaina, tsy eto amin'ny chat)

### 1. Alao GitHub ilay dossier
```bash
cd tendry-app
git init
git add .
git commit -m "Tendry Epicerie - version Android"
git branch -M main
git remote add origin https://github.com/<anaranao>/tendry-epicerie.git
git push -u origin main
```

### 2. Ampidiro ny Capacitor sy ny plateforme Android
```bash
npm install
npx cap add android
npx cap sync android
```
→ Amin'io dingana io no hiforonan'ny dossier `android/` (projet Android Studio feno).

### 3. Sokafy amin'i Android Studio
```bash
npx cap open android
```
Miandry ny Gradle sync voalohany (mety maharitra 2-5 min raha vao voalohany).

### 4. Alao ny sary (icônes) sy ny "splash screen"
- Apidiro ny logo-nao ao amin'ny `www/icons/icon-192.png` sy `www/icons/icon-512.png`
  (jereo ny manifest.json — efa voatondro any izy ireo).
- Amin'i Android Studio: kitiho *Res Manager* → *Image Asset* → *Launcher Icons* mba
  hamoronana automatique ny icônes rehetra ho an'ny app (mipdf launcher).
- Azonao atao ihany koa ny mamokatra azy rehetra indray mandeha amin'ny package
  `@capacitor/assets` (`npx @capacitor/assets generate`).

### 5. Alao ny fahazoan-dàlana Caméra (ilaina amin'ny scan QR/Code-barres)
Ampio ao amin'ny `android/app/src/main/AndroidManifest.xml` (ambony kely, alohan'ny
`<application>`):
```xml
<uses-permission android:name="android.permission.CAMERA" />
<uses-feature android:name="android.hardware.camera" android:required="false" />
```

### 6. Manamboatra APK (débogage haingana, hitsapana eo amin'ny téléphone)
Amin'i Android Studio: **Build → Build Bundle(s)/APK(s) → Build APK(s)**
→ ho hita any amin'ny `android/app/build/outputs/apk/debug/app-debug.apk`

### 7. Manamboatra APK/AAB "signé" (ho apetraka amin'ny Play Store na hozarainao)
1. **Build → Generate Signed Bundle / APK**
2. Mamorona *keystore* vaovao (tehirizo tsara io fichier io + ny mots de passe azy,
   ilaina indray isaky ny fanavaozana ny app any aoriana)
3. Fidio **APK** (raha hozarainao mivantana) na **AAB** (raha ho any amin'ny Play Store)

## 🤖 Famoronana APK amin'ny GitHub Actions (tsy mila Android Studio)

Efa ao anatin'ity dossier ity ny `.github/workflows/build-apk.yml`. Rehefa
`git push`-nao any amin'i GitHub io repo io (jereo ny dingana 1 etsy ambony), dia:

1. GitHub mihitsy no hamorona ny dossier `android/` (`npx cap add android`),
   hametraka ny fahazoan-dàlana caméra, ary hanamboatra ny APK — automatique, tsy
   mila ataonao na inona na inona.
2. Miandry kely (~3-6 min), avy eo:
   - Midira ao amin'ny repo-nao any amin'i GitHub → tab **Actions**
   - Kitiho ilay "run" farany (misy ✅ maitso raha vita tsara)
   - Any ambany dia hisy **Artifacts** → `tendry-epicerie-debug-apk` → alaivo (download)
   - Fongarana ho `app-debug.apk` io — ampidiro amin'ny téléphone Android dia i-install
     (mila alefa ny "Installer avy amin'ny loharano tsy fantatra" any amin'ny paramètre)
3. Raha misy fanavaozana ataonao ao amin'ny `www/` (index.html, sns.) dia `git push`
   fotsiny indray — hi-build ho azy indray ny APK vaovao.

### ⚠️ Io APK io dia "debug" ihany (fitsapana)
Tsy mety apetraka amin'ny Play Store izy io, fa azo apetraka mivantana amin'ny
téléphone. Vakio ny fizarana **📦 Fanamboarana ho an'ny Play Store** etsy ambany
raha te-hametraka an'ity app ity any amin'ny Play Store.

## 📦 Fanamboarana APK/AAB "signé" ho an'ny Play Store (amin'i GitHub Actions)

Efa vonona ao amin'ny workflow ny job faharoa (`build-release`) izay manamboatra
automatique ny **AAB signé** (ilaina amin'ny Play Store) sy ny **APK signé**
(azo apetraka mivantana). Mila ataonao IREO DINGANA ETO AMBANY IREO indray mandeha
ihany (any amin'ny solosaina, satria mila `keytool`):

### 1. Mamorona ny "keystore" (fanalahidy hanasoniavana ny app)
```bash
keytool -genkey -v -keystore tendry-release.keystore -alias tendry -keyalg RSA -keysize 2048 -validity 10000
```
- Hangatahina anao ny mots de passe (keystore + key) sy ny anaranao/orinasa
- **TEHIRIZO TSARA** io fichier `tendry-release.keystore` io + ny mots de passe
  rehetra (tehirizo any amin'ny toerana azo antoka, tsy any amin'ny GitHub!),
  satria **ilaina foana** izy io isaky ny hanavaozanao ny app any aoriana — raha
  very io dia tsy azo atao intsony ny manavao ilay app efa napetraka amin'ny
  Play Store, fa mila mamorona app vaovao indray.

### 2. Ovay ho Base64 ilay keystore
```bash
base64 -i tendry-release.keystore -o keystore-base64.txt
```
(amin'i Windows PowerShell: `[Convert]::ToBase64String([IO.File]::ReadAllBytes("tendry-release.keystore")) | Out-File keystore-base64.txt`)

### 3. Ampidiro ao amin'i GitHub ireto Secrets ireto
Any amin'ny repo → **Settings → Secrets and variables → Actions → New repository secret**,
ampidiro efatra ireto (ny anarany dia tsy maintsy mitovy PIPY amin'ireto):

| Anaran'ny Secret     | Ilay atao ao anatiny                                   |
|----------------------|---------------------------------------------------------|
| `KEYSTORE_BASE64`    | ny votoatin'ilay `keystore-base64.txt` (dia paste)      |
| `KEYSTORE_PASSWORD`  | ny mot de passe navalinao tamin'ny `-storepass`         |
| `KEY_ALIAS`          | `tendry` (na izay alias nomenao)                        |
| `KEY_PASSWORD`       | ny mot de passe an'ilay key (matetika mitovy amin'ny KEYSTORE_PASSWORD) |

### 4. `git push` indray (na "Re-run" ilay Action)
Amin'io fotoana io dia hilay ho azy ny job faharoa `build-release`, ary hisy
Artifacts roa fanampiny ao amin'ny **Actions → (run farany) → Artifacts**:
- `tendry-epicerie-release-aab` → **`app-release.aab`** — ity no alefa any amin'ny
  [Google Play Console](https://play.google.com/console) (Production/Test)
- `tendry-epicerie-release-apk` → `app-release.apk` — raha ilainao apetraka
  mivantana amin'ny téléphone

### 5. Fandefasana any amin'ny Play Console (ataon-tenanao, tsy azo atao amin'ny Action)
1. Mamorona kaonty *Google Play Console* (misy saram-pidirana engan-tokana ~25$)
2. Mamorona app vaovao → mameno ny mombamomba (sary, sarin'efijery, description...)
3. **Production** (na Internal/Closed testing aloha) → **Create new release** →
   apidiro ilay `app-release.aab` → hafarana

## 🔁 Isaky ny manova ny index.html/CSS/JS
```bash
npx cap sync android
```
avy eo Build indray ao Android Studio (na `git push` fotsiny raha GitHub Actions).

## ⚠️ Marihina
- `localStorage` dia mitovy tsara amin'ny WebView Android (Capacitor), ka voatahiry
  daholo ny angona (stock, varotra, recette...) ao anaty téléphone.
- Raha te-hametraka logo/anarana hafa ho an'ny app dia ovay ny `appName` sy `appId`
  ao amin'ny `capacitor.config.json` **alohan'ny** `npx cap add android`.
