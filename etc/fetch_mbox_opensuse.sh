#! /bin/bash
###############################################
# A wrapper shell script to fetch the compressed mailboxes of suse mailing lists
# each download happens with one second delay and happens quietly
# finally all the mboxes are saved in "opensuse_mbox" directory
#
# To run
# $bash fetch_mbox_opensuse.sh
#
# Author: Achyudh Ram
# Date: 28-August-2016
##############################################
mkdir -p opensuse_mbox
declare -a links=("blinux" "opensuse-m17n" "blinux-de" "opensuse-maintenance" "general" "opensuse-marketing" "limal-commit" "opensuse-medical" "limal-devel" "opensuse-mingw" "obs-commits" "opensuse-mobile" "obs-errors" "opensuse-mobile-de" "obs-tests" "opensuse-multimedia" "opensuse" " opensuse-multimedia-de" "opensuse-ambassadors" "opensuse-networking" "opensuse-ambassadors-australia" "opensuse-nl" "opensuse-ambassadors-chinese" "opensuse-optimize" "opensuse-ambassadors-netherlands" "opensuse-packaging" "opensuse-ambassadors-north-america" "opensuse-pl" "opensuse-amd64" "opensuse-ppc" "opensuse-announce" "opensuse-programming" "opensuse-arm" "opensuse-programming-de" "opensuse-artwork" "opensuse-project" "opensuse-autoinstall" "opensuse-proofreading" "opensuse-bar" "opensuse-pt" "opensuse-board" "opensuse-ru" "opensuse-boosters" "opensuse-ruby" "opensuse-bugs" "opensuse-security" "opensuse-buildservice" "opensuse-security-announce" "opensuse-cloud" "opensuse-softwaremgmt" "opensuse-commit" "opensuse-squeegee" "opensuse-conference" "opensuse-summit" "opensuse-contrib" "opensuse-test" "opensuse-cz" "opensuse-testing" "opensuse-da" "opensuse-translation" "opensuse-de" "opensuse-translation-de" "opensuse-doc" "opensuse-translation-el" "opensuse-edu" "opensuse-translation-es" "opensuse-edu-de" "opensuse-translation-hu" "opensuse-el" "opensuse-translation-ru" "opensuse-es" "opensuse-translation-sk" "opensuse-factory" "opensuse-updates" "opensuse-factory-base" "opensuse-ux" "opensuse-factory-graphics" "opensuse-virtual" "opensuse-factory-mozilla" "opensuse-web" "opensuse-features" "opensuse-web-de" "opensuse-foundation" "opensuse-wiki" "opensuse-fr" "opensuse-wiki-de" "opensuse-gnome" "opensuse-women" "opensuse-goblin" "opensuse-xfce" "opensuse-ham" "opensuse-xorg" "opensuse-ham-de" "opensuse-zh" "opensuse-hu" "packet-writing" "opensuse-ia64" "packet-writing-announce" "opensuse-invis" "proxy-suite" "opensuse-isdn-de" "radeonhd" "opensuse-it" "vhostmd" "opensuse-ja" "yast-announce" "opensuse-java" "yast-commit" "opensuse-kde" "yast-devel" "opensuse-kde3" "zypp-commit" "opensuse-kernel" "zypp-devel" "opensuse-lxde")

for i in "${links[@]}"
do
	wget -c -w 1 -r -l 1 -A .mbox.gz http://lists.opensuse.org/$i/
done
find ./lists.opensuse.org -type f -name '*.mbox.gz' -exec mv -i {} ./opensuse_mbox  \;
cd ./opensuse_mbox
gunzip *
