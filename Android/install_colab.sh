#!/bin/bash

log="install.log"

echo -e "########## Installation des prérequis pour le build android #############\n
         \t ------------- Mise  à jour apt-get ----------------"
sudo apt update && sudo apt upgrade -y

echo -e "\t ------------- Installation Buildozer et cython ----------------\n"
pip install Buildozer 2 >> $log
pip install cython 2 >> $log

echo -e "\t ------------- Installation des librairies essentielles ----------------\n"

sudo apt-get install -y \
    python3-pip \
    build-essential \
    git \
    python3 \
    python3-dev \
    ffmpeg \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    zlib1g-dev \
    libgstreamer1.0 \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good 2 >> $log

sudo apt-get install build-essential libsqlite3-dev sqlite3 bzip2 libbz2-dev zlib1g-dev libssl-dev openssl libgdbm-dev libgdbm-compat-dev liblzma-dev libreadline-dev libncursesw5-dev libffi-dev uuid-dev libffi7 libtool 2 >> $log

echo -e "\t ------------- Installation du jdk nécessaire ----------------\n"

sudo apt-get install openjdk-17-jre-headless -qq > /dev/null
import os
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-17-openjdk-amd64"
update-alternatives --set java /usr/lib/jvm/java-17-openjdk-amd64/bin/java
java -version
