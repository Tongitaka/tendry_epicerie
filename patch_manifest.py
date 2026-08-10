#!/usr/bin/env python3
"""
Manampy ny fahazoan-dàlana Camera + Storage ao amin'ny AndroidManifest.xml,
izay foronin'i Capacitor tamin'ny 'npx cap add android' (fichier tsy voatahiry
ao amin'ny git, ka mila ovaina isaky ny CI run - mitovy filojika amin'ny
patch_signing.py).

Ilaina ny alalana Camera mba hahafahan'ny scanner QR/Code-barres (html5-qrcode +
getUserMedia) miasa ao anaty WebView an'ny application.
"""
import glob
import sys

candidates = glob.glob("android/app/src/main/AndroidManifest.xml")
if not candidates:
    print("ERROR: tsy hita ny AndroidManifest.xml (efa nataonao ve 'npx cap add android'?)")
    sys.exit(1)

MANIFEST_PATH = candidates[0]

PERMISSIONS_BLOCK = (
    '    <uses-permission android:name="android.permission.CAMERA" />\n'
    '    <uses-feature android:name="android.hardware.camera" android:required="false" />\n'
    '    <uses-feature android:name="android.hardware.camera.autofocus" android:required="false" />\n'
    '    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" android:maxSdkVersion="28" />\n'
    '    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" android:maxSdkVersion="32" />\n'
)

with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
    content = f.read()

if "android.permission.CAMERA" in content:
    print("Efa misy ny alalana Camera ao amin'ny AndroidManifest.xml, tsy manova.")
else:
    idx = content.find("<application")
    if idx == -1:
        print("ERROR: tsy hita ny tag <application> ao amin'ny AndroidManifest.xml")
        sys.exit(1)
    content = content[:idx] + PERMISSIONS_BLOCK + content[idx:]
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ Voaampy ny alalana Camera/Storage ao amin'ny AndroidManifest.xml")
