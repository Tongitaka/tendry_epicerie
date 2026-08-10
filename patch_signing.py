#!/usr/bin/env python3
"""
Ampiana signingConfigs (release) ao amin'ny android/app/build.gradle,
izay foronin'i Capacitor tamin'ny 'npx cap add android' (fichier tsy
voatahiry ao amin'ny git, ka mila ovaina isaky ny CI run).

Ampiasaina ireto env variable ireto (apetraka avy amin'ny GitHub Secrets):
  KEYSTORE_PATH      -> lalan-dàlan'ilay fichier .keystore/.jks navoaka
  KEYSTORE_PASSWORD
  KEY_ALIAS
  KEY_PASSWORD
"""
import re
import sys

GRADLE_PATH = "android/app/build.gradle"

SIGNING_BLOCK = """
    signingConfigs {
        release {
            storeFile file(System.getenv("KEYSTORE_PATH"))
            storePassword System.getenv("KEYSTORE_PASSWORD")
            keyAlias System.getenv("KEY_ALIAS")
            keyPassword System.getenv("KEY_PASSWORD")
        }
    }
"""

with open(GRADLE_PATH, "r", encoding="utf-8") as f:
    content = f.read()

if "signingConfigs" in content:
    print("signingConfigs efa ao, tsy manova na inona na inona.")
    sys.exit(0)

# 1) Ampidiro ny signingConfigs eo aorian'ny "android {" voalohany
content = content.replace("android {", "android {\n" + SIGNING_BLOCK, 1)

# 2) Ampio "signingConfig signingConfigs.release" ao anaty buildTypes { release { ... } }
pattern = re.compile(r"(buildTypes\s*\{\s*release\s*\{)")
if pattern.search(content):
    content = pattern.sub(r"\1\n            signingConfig signingConfigs.release", content, count=1)
else:
    print("ERROR: tsy hita ny bloc 'buildTypes { release { ... } }' ao amin'ny build.gradle")
    sys.exit(1)

with open(GRADLE_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Voaampy ny signingConfigs release ao amin'ny build.gradle")
