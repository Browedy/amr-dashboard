[app]
title = AMR Dashboard
package.name = amrdashboard
package.domain = org.nal

source.dir = .
source.include_exts = py

version = 1.0

requirements = python3==3.9.9,hostpython3==3.9.9,kivy==2.1.0,requests==2.28.1,certifi,charset-normalizer,idna,urllib3

p4a.bootstrap = sdl2
p4a.branch = develop
p4a.source_dir = 

orientation = landscape
fullscreen = 0

android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE
android.api = 29
android.minapi = 21
android.ndk = 25
android.accept_sdk_license = True
android.archs = armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
