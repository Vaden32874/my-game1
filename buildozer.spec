[app]
title = UI Jumper
package.name = uijumper
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# Ensure there are NO SPACES after the comma here
requirements = python3,pygame==2.1.0

orientation = portrait
fullscreen = 1

# Modern phones need this specific architecture
android.archs = arm64-v8a

# This helps the build process stay stable
p4a.branch = master
