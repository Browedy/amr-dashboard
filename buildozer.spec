[app]
title = AMR Dashboard
package.name = amrdashboard
package.domain = org.nal

source.dir = .
source.include_exts = py

version = 1.0

requirements = python3,kivy==2.2.1,requests,certifi,urllib3,charset-normalizer,idna
android.skip_update = False
p4a.bootstrap = sdl2
orientation = landscape
fullscreen = 0

android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
