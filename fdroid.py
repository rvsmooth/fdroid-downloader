import requests
import json
import subprocess
import os

app_list = {
    "com.akylas.aard2": "fdroid",
    "com.akylas.documentscanner": "izzysoft",
    "com.artifex.mupdf.viewer.app": "fdroid",
    "com.bnyro.wallpaper": "fdroid",
    "com.looker.droidify": "fdroid",
    "com.philkes.notallyx": "fdroid",
    "com.termux": "fdroid",
    "com.xayah.databackup.foss": "fdroid",
    "dev.anilbeesetti.nextplayer": "fdroid",
    "helium314.keyboard": "fdroid",
    "net.cozic.joplin": "fdroid",
    "org.documentfoundation.libreoffice": "fdroid",
    "org.localsend.localsend_app": "fdroid",
    "proton.android.pass.fdroid": "fdroid",
    "ru.tech.imageresizershrinker": "fdroid",
    "ua.acclorite.book_story": "fdroid",
}

items_fdroid = []
items_izzysoft = []

for i in app_list:
    print(f"{i} is to be downloaded from {app_list[i]}")
    provider = app_list[i]

    if provider == "fdroid":
        items_fdroid.append(i)
    if provider == "izzysoft":
        items_izzysoft.append(i)


def wget_dl(url, out_path):
    """
    Download file from URL using wget.

    Attributes:
        url (str)      : URL to download.
        out_path (str) : Path where the downloaded file will be saved.
    """
    cmd = ["wget", "-qO", out_path, "--show-progress", "--wait=2", "--random-wait", url]
    subprocess.run(cmd)


def getapps(app_dict, api_url, dl_url):
    """
    Download apps from izzysoft or fdroid or similar api providing sites

    Args:
    app_dict (dict) : Applist
    api_url (str)   : Api url for izzysoft or f-droid
    dl_url (str)    : Common download url

    """
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
