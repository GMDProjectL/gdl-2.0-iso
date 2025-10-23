#!/bin/sh

sudo apt-get update
sudo apt-get install -y podman

curl -s https://raw.githubusercontent.com/89luca89/distrobox/main/install | sh

ARCH_CONTAINER_NAME=gdl

distrobox create --root --image archlinux --name ${ARCH_CONTAINER_NAME} -Y

distrobox enter --root ${ARCH_CONTAINER_NAME} -- \
    sudo pacman -Syu \
        arch-install-scripts archiso python-loguru \
        --noconfirm
