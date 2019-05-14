#!/bin/bash


if [ "$EUID" -ne 0 ]; then
   echo "This script must be run as root" 
   exit 1
fi

os="$(lsb_release -is)"

echo "Detect OS: $os"
package="parallel R"



ubunto() {
for pack in $package; do
    if ! [ -x "$(command -v $pack)" ]; then
        sudo apt-get install $pack
    else
        echo "$pack is installed."
    fi
done
}

centos() {
for pack in $package; do
    if ! [ -x "$(command -v $pack)" ]; then
        yum install $package
    else
    	echo "$pack is installed."
    fi
done
}


case $os in
	"Ubuntu") ubunto;;
	"CentOS" | "Fedora" | "Redhat") centos;;
	"OpenSUSE"| "SUSE LINUX") echo "OpenSUSE";;
    *) echo "no clue - $os";;
esac
