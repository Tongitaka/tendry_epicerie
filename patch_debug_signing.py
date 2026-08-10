#!/usr/bin/env python3
"""
Mametraka signingConfigs "debugFixed" tapaka mafy (fixe) ao amin'ny
android/app/build.gradle, ho an'ny build DEBUG.

TENA ILAINA IO: raha tsy misy izao patch izao, dia clé (keystore) VAOVAO
random no foronin'i Android isaky ny CI run (satria mandeha amin'ny runner
"vierge" isaky ny fandehanana ny GitHub Actions ny CI), ka tsy mifanaraka
intsony ny sonia (signature) amin'ny APK taloha - koa MANDA ny finday
hametraka ilay APK debug vaovao eo ambonin'ny efa misy (tsy misy "mise à
jour" azo atao, tsy maintsy manala aloha ilay app taloha = very ny données).

Amin'ny alalan'ity script ity, dia clé debug MITOVY HATRANY no ampiasaina
isaky ny build (avy amin'ny Secret DEBUG_KEYSTORE_BASE64), ka azo atao
ny "mise à jour" mahazatra (installation eo ambonin'ny efa misy, tsy misy
fahaverezan'ny données) amin'ny APK "debug" ihany koa, tsy amin'ny APK
"release" voasonia ihany.

Ampiasaina ireto env variable ireto (avy amin'ny GitHub Secrets):
  DEBUG_KEYSTORE_PATH
  DEBUG_KEYSTORE_PASSWORD
  DEBUG_KEY_ALIAS
  DEBUG_KEY_PASSWORD

Raha tsy voapetraka ireo Secrets ireo (DEBUG_KEYSTORE_PATH tsy misy), dia
tsy manova na inona na inona ity script ity (hiverina amin'ny clé debug
random mahazatra an'i Android - tsara ho an'ny fitsapana haingana ihany,
fa tsy azo atao "mise à jour" amin'izay).
"""
import os
import re
import sys

GRADLE_PATH = "android/app/build.gradle"

if not os.environ.get("DEBUG_KEYSTORE_PATH"):
    print("ℹ️ DEBUG_KEYSTORE_PATH tsy voapetraka - tsy manova ny signing an'ny build debug (clé random mahazatra no hampiasaina).")
    sys.exit(0)

SIGNING_BLOCK = """
    signingConfigs {
        debugFixed {
            storeFile file(System.getenv("DEBUG_KEYSTORE_PATH"))
            storePassword System.getenv("DEBUG_KEYSTORE_PASSWORD")
            keyAlias System.getenv("DEBUG_KEY_ALIAS")
            keyPassword System.getenv("DEBUG_KEY_PASSWORD")
        }
    }
"""

with open(GRADLE_PATH, "r", encoding="utf-8") as f:
    content = f.read()

if "debugFixed" in content:
    print("signingConfigs.debugFixed efa ao, tsy manova.")
    sys.exit(0)

# 1) Ampidiro ny signingConfigs.debugFixed eo aorian'ny "android {" voalohany
content = content.replace("android {", "android {\n" + SIGNING_BLOCK, 1)

# 2) Ampio na ovay ny buildTypes.debug mba hampiasa io signingConfig io
if re.search(r"buildTypes\s*\{[^}]*?\bdebug\s*\{", content, re.DOTALL):
    content = re.sub(r"(buildTypes\s*\{[^}]*?\bdebug\s*\{)", r"\1\n            signingConfig signingConfigs.debugFixed", content, count=1, flags=re.DOTALL)
else:
    # Tsy misy bloc 'debug { ... }' mazava ao amin'ny buildTypes (mahazatra amin'i Capacitor),
    # koa ampiana izy io mivantana.
    content = re.sub(r"(buildTypes\s*\{)", r"\1\n        debug {\n            signingConfig signingConfigs.debugFixed\n        }", content, count=1)

with open(GRADLE_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Voapetraka ny signingConfigs.debugFixed ho an'ny build debug (tsy hiova intsony ny clé isaky ny CI run)")
