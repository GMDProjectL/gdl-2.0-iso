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
            'plasma', 'sddm', 'konsole', 'gdl-look-and-feel'
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
