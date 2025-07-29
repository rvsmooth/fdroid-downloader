import requests
import json
import subprocess
import os

app_list = {
    "com.artifex.mupdf.viewer.app": "fdroid",
    "org.localsend.localsend_app": "fdroid",
    "proton.android.pass.fdroid": "fdroid",
    "helium314.keyboard": "fdroid",
    "org.mozilla.fennec_fdroid": "fdroid",
    "com.looker.droidify": "fdroid",
    "ua.acclorite.book_story": "fdroid",
    "com.bnyro.wallpaper": "fdroid",
    "net.cozic.joplin": "fdroid",
    "org.proninyaroslav.libretorrent": "fdroid",
    "org.documentfoundation.libreoffice": "fdroid",
    "com.termux": "fdroid",
    "dev.anilbeesetti.nextplayer": "fdroid",
    "ru.tech.imageresizershrinker": "fdroid",
    "com.xayah.databackup.foss": "fdroid",
    "com.akylas.documentscanner": "izzysoft",
}

items_fdroid = []
items_izzysoft = []

for i in app_list:
    print(f"{i} is installed from {app_list[i]}")
    provider = app_list[i]

    if provider == "fdroid":
        items_fdroid.append(i)
    if provider == "izzysoft":
        items_izzysoft.append(i)


def wget_dl(url, out_path):
    cmd = ["wget", url, "-O", out_path]
    subprocess.run(cmd)


def getapps(app_dict, api_url, dl_url):
    for item in app_dict:
        response = requests.get(f"{api_url}/{item}")
        response_json = json.loads(response.text)
        version = response_json["suggestedVersionCode"]
        apk = f"{item}_{version}.apk"
        wget_dl(f"{dl_url}/{apk}", out_path=f"downloads/{apk}")


if os.path.exists("downloads"):
    print("downloads dir exists")
else:
    os.makedirs("downloads")

getapps(
    items_izzysoft,
    api_url="https://apt.izzysoft.de/fdroid/api/v1/packages",
    dl_url="https://apt.izzysoft.de/fdroid/repo",
)

getapps(
    items_fdroid,
    api_url="https://f-droid.org/api/v1/packages",
    dl_url="https://f-droid.org/repo",
)
