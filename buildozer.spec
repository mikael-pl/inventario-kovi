[app]

# (str) Title of your application
title = Invent?rio Kovi

# (str) Package name
package.name = inventariokovi

# (str) Package domain (needed for android/ios packaging)
package.domain = com.kovi

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json,db,pdf

# (list) List of directory to exclude (let empty to not exclude anything)
#source.exclude_dirs = tests, bin
# (list) List of inclusions using pattern matching
source.include_patterns = assets/*,libs/*,libs/**/*

# (str) Application versioning (method 1)
version = 1.1.0

# (list) Application requirements
# Versao minima SEM dependencias que precisam CMake
requirements = python3,kivy==2.3.0,kivymd==1.2.0,requests

# (str) Custom source code for pyjnius (versão corrigida)
p4a.local_recipes = ./p4a-recipes

# (list) Recipes para incluir (necessário para libs que precisam compilação customizada)
# p4a.source_dir = 
# p4a.local_recipes = ./p4a-recipes

# (str) Supported orientation (landscape, portrait)
# landscape = horizontal (melhor para tablet)
orientation = landscape

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,CAMERA,WAKE_LOCK

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpymodules.so
android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a,armeabi-v7a

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
