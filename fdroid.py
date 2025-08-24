import requests
import json
import subprocess
import os
import glob

with open("app_list.json", "r") as applist:
    app_list = json.load(applist)

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
        if os.path.exists(apk):
            print(apk, "is downloaded already")
        else:
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

question = input(
    "Would you want to install the apks to the currently connected adb device? (yes/no): "
)

apks = glob.glob("./downloads/*.apk")
adb_install = ["adb", "install"]
if question.lower() == "yes":
    for apk in apks:
        adb_install = adb_install[:2]
        adb_install.append(apk)
        subprocess.run(adb_install)

elif question.lower() == "no":
    print("Skipping Installation")
else:
    print("Invalid choices")
