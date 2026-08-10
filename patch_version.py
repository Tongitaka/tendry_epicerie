#!/usr/bin/env python3
"""
Mametraka versionCode sy versionName tapaka (mitombo hatrany, azo antoka) ao
amin'ny android/app/build.gradle, izay foronin'i Capacitor tamin'ny
'npx cap add android' (fichier tsy voatahiry ao amin'ny git, ka mila ovaina
isaky ny CI run).

ILAINA IO mba hahafahan'i Android mahalala fa "mise à jour" (fanavaozana) ny
APK vaovao, fa tsy version mitovy - raha tsy izany dia MANDA ny finday
hametraka ilay APK vaovao eo ambonin'ny efa misy (na tsy manova na inona
na inona), ka very daholo ny données efa tao.

Ampiasaina ny env variable VERSION_CODE sy VERSION_NAME (apetraky ny
workflow, ohatra amin'ny alalan'ny ${{ github.run_number }} mba hitombo
hatrany isaky ny build).
"""
import os
import re
import sys

GRADLE_PATH = "android/app/build.gradle"

version_code = os.environ.get("VERSION_CODE", "1")
version_name = os.environ.get("VERSION_NAME", "1.0.0")

with open(GRADLE_PATH, "r", encoding="utf-8") as f:
    content = f.read()

content, n1 = re.subn(r"versionCode\s+\d+", f"versionCode {version_code}", content)
content, n2 = re.subn(r'versionName\s+"[^"]*"', f'versionName "{version_name}"', content)

if n1 == 0 or n2 == 0:
    print(f"ERROR: tsy hita ny versionCode/versionName tao amin'ny {GRADLE_PATH} (n1={n1}, n2={n2})")
    sys.exit(1)

with open(GRADLE_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print(f"✅ Voapetraka: versionCode={version_code}, versionName={version_name}")
