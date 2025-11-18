[app]
title = AMR Dashboard
package.name = amrdashboard
package.domain = org.nal

source.dir = .
source.include_exts = py

version = 1.1

requirements = python3,kivy,requests

orientation = landscape

android.permissions = INTERNET,ACCESS_NETWORK_STATE

android.api = 31
android.minapi = 21
android.archs = armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
