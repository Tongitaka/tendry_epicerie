#!/usr/bin/env python3
"""
Manoratra indray ny MainActivity.java, izay foronin'i Capacitor tamin'ny
'npx cap add android' (fichier tsy voatahiry ao amin'ny git, ka mila ovaina
isaky ny CI run - mitovy filojika amin'ny patch_signing.py), mba hangatahany
mivantana ny alalana Camera (sy Storage ho an'ny Android taloha) rehefa
manomboka ny application - ilaina amin'ny scanner QR/Code-barres
(html5-qrcode + getUserMedia) ao anaty app.
"""
import glob
import re
import sys

candidates = glob.glob("android/app/src/main/java/**/MainActivity.java", recursive=True)
if not candidates:
    print("ERROR: tsy hita ny MainActivity.java (efa nataonao ve 'npx cap add android'?)")
    sys.exit(1)

MAIN_ACTIVITY_PATH = candidates[0]

with open(MAIN_ACTIVITY_PATH, "r", encoding="utf-8") as f:
    original = f.read()

m = re.search(r"^package\s+([\w.]+);", original, re.MULTILINE)
if not m:
    print("ERROR: tsy hita ny package declaration ao amin'ny MainActivity.java")
    sys.exit(1)
package_name = m.group(1)

if "requestAppPermissions" in original:
    print("Efa voaova (patched) ny MainActivity.java, tsy manova.")
    sys.exit(0)

NEW_CONTENT = f"""package {package_name};

import android.Manifest;
import android.content.pm.PackageManager;
import android.os.Build;
import android.os.Bundle;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import com.getcapacitor.BridgeActivity;

import java.util.ArrayList;
import java.util.List;

public class MainActivity extends BridgeActivity {{

    private static final int PERMISSION_REQUEST_CODE = 1001;

    @Override
    public void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        requestAppPermissions();
    }}

    /** Mangataka ny alalana Camera (sy Storage ho an'ny Android <= 9) raha mbola tsy nomena. */
    private void requestAppPermissions() {{
        List<String> toRequest = new ArrayList<>();

        if (ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA)
                != PackageManager.PERMISSION_GRANTED) {{
            toRequest.add(Manifest.permission.CAMERA);
        }}

        if (Build.VERSION.SDK_INT <= Build.VERSION_CODES.P) {{
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE)
                    != PackageManager.PERMISSION_GRANTED) {{
                toRequest.add(Manifest.permission.WRITE_EXTERNAL_STORAGE);
            }}
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.READ_EXTERNAL_STORAGE)
                    != PackageManager.PERMISSION_GRANTED) {{
                toRequest.add(Manifest.permission.READ_EXTERNAL_STORAGE);
            }}
        }}

        if (!toRequest.isEmpty()) {{
            ActivityCompat.requestPermissions(
                this,
                toRequest.toArray(new String[0]),
                PERMISSION_REQUEST_CODE
            );
        }}
    }}
}}
"""

with open(MAIN_ACTIVITY_PATH, "w", encoding="utf-8") as f:
    f.write(NEW_CONTENT)

print(f"✅ Voaova ny MainActivity.java ({package_name}) mba hangataka alalana Camera/Storage.")
