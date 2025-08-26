# Fdroid Downloader

A simple python script to download packages from fdroid or izzysoft for convenience

## Usage
- Make sure you got adb, wget installed and your device connected and allowed for ADB from your pc.
- Put in your app lists in [app_list.json](https://raw.githubusercontent.com/rvsmooth/fdroid-downloader/refs/heads/main/app_list.json) and put the file in the same directory as of the script. And execute the executable.

### Step 1

First add your packages to app_list.json.
for an example,
for `https://f-droid.org/en/packages/org.fdroid.fdroid/` the package name will be `org.fdroid.fdroid`. And the remote will be `fdroid`.

### Step 2

Then execute the program

```
python3 fdown.py
```
