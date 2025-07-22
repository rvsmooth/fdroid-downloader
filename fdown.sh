#!/bin/bash
api_url="https://f-droid.org/api/v1/packages"
dl_url="https://f-droid.org/repo"
outdir="fdroid_dl"

__download_assets() {
  wget -qP $outdir/ --show-progress -nc --wait=2 --random-wait $1
}

error_out() {
  echo "Failed to download $1" | tee -a failed.log
  echo "Check failed.log for details"
  touch failed.log
}
packages="
com.artifex.mupdf.viewer.app
org.localsend.localsend_app
proton.android.pass.fdroid
helium314.keyboard
org.mozilla.fennec_fdroid
com.looker.droidify
ua.acclorite.book_story
com.bnyro.wallpaper
net.cozic.joplin
org.proninyaroslav.libretorrent
org.documentfoundation.libreoffice
com.termux
dev.anilbeesetti.nextplayer
ru.tech.imageresizershrinker
"
urls=()
for package in $packages; do
  set -x
  version=$(curl "$api_url/$package" | jq ".suggestedVersionCode")
  final_url=$(echo "${dl_url}/${package}_${version}.apk")
  urls+=("$final_url")
done

[ ! -d "$outdir" ] && mkdir $outdir

for item in ${urls[@]}; do
  __download_assets $item || { error_out $item; }
done

for a in "${outdir}/*.apk"; do
  echo "Installing $a"
  adb install $a
done
