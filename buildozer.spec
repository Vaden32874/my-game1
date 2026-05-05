[app]

# (str) Title of your application
title = UI Jumper

# (str) Package name
package.name = uijumper

# (str) Package domain (needed for android packaging)
package.domain = org.test

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let's keep it simple)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning
version = 0.1

# (list) Application requirements
# THIS IS THE CRITICAL PART: WE REMOVED KIVY AND ADDED PYGAME
requirements = python3,pygame

# (str) Supported orientations (landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (list) Permissions
android.permissions = INTERNET

# (list) The Android archs to build for. arm64-v8a is for modern phones.
android.archs = arm64-v8a

# (bool) Use the old toolchain (leave at 0)
p4a.branch = master
