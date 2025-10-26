import loguru
import os
from archiso import Archiso
from systemd import Systemd
from packages import Packages

class KDE(Archiso):
    def __init__(self, target_iso_dir: str, packages: Packages, systemd: Systemd):
        super().__init__(target_iso_dir)
        self.packages = packages
        self.systemd = systemd

    def install_base_kde(self):
        loguru.logger.info("Adding KDE packages")
        self.packages.add_packages([
            'aurorae', 'bluedevil',
            'breeze', 'breeze-plymouth',
            'discover', 'flatpak-kcm',
            'drkonqi',
            'kactivitymanagerd',
            'kde-cli-tools', 'kde-gtk-config',
            'kdecoration',
            'kdeplasma-addons',
            'kgamma', 'ark', '7zip', 'unarchiver', 'zip', 'unzip',
            'kglobalacceld', 'kscreen',
            'kinfocenter', 'kmenuedit',
            'knighttime', 'kpipewire',
            'krdp', 'kscreen', 'kscreenlocker',
            'ksshaskpass', 'ksystemstats', 'kwallet-pam',
            'kwayland', 'kwin', # No Xorg/X11 support, it's 2025, Wayland on Plasma 6 is fine.
            'kwrited', 'kate',
            'layer-shell-qt', 'filelight', 'gwenview',
            'libkscreen', 'libplasma',
            'milou', 'oxygen',
            'plasma-activities', 'plasma-activities-stats', 'plasma-browser-integration',
            'plasma-desktop', 'plasma-disks', 'plasma-firewall', 'plasma-integration',
            'plasma-nm', 'plasma-pa',
            'plasma-systemmonitor',
            'plasma-thunderbolt', 'plasma-vault',
            'plasma-workspace',
            'plasma5support', 'breeze5',
            'plymouth-kcm',
            'polkit-kde-agent',
            'powerdevil', 'print-manager',
            'qqc2-breeze-style', 'sddm-kcm',
            'spectacle', 'systemdgenie',
            'systemsettings', 'wacomtablet',
            'xdg-desktop-portal-kde',
            'sddm', 'konsole', 'gdl-look-and-feel',
            'archlinux-appstream-data', 'packagekit-qt6', 
            'dolphin', 'kio-admin',
            'kcron', 'kde-inotify-survey',
            'khelpcenter', 
            'kjournald',
            'partitionmanager'
        ])

    def setup_autologin(self):
        loguru.logger.info("Setting up SDDM autologin")

        autologin_dir = f'{self.target_iso_dir}/airootfs/etc/sddm.conf.d'
        os.system(f'mkdir -p {autologin_dir}')

        result = os.system(f'cp ./resources/etc/sddm.conf.d/autologin.conf {autologin_dir}/autologin.conf')
        if result != 0:
            raise Exception(f'Unable to copy autologin.conf. Code: {result}')
        
        loguru.logger.info("Done setting up autologin")
        
    def setup_sddm(self):
        self.systemd.activate_system_service('sddm', 'multi-user')
    
    def install_aio(self):
        self.install_base_kde()
        self.setup_sddm()
        self.setup_autologin()
