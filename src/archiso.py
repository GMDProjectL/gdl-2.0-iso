import loguru
import os

class Archiso:
    def __init__(self, target_iso_dir: str):
        self.target_iso_dir = target_iso_dir

    def copy_releng_config(self):
        loguru.logger.info(f'Copying Arch Releng config to `{self.target_iso_dir}`...')
        result = os.system(f'cp -r /usr/share/archiso/configs/releng/ {self.target_iso_dir}')
        
        if result != 0:
            raise Exception(f'Failed to copy Arch Releng config. Code: {result}')
    

    def copy_os_release(self):
        loguru.logger.info(f'Copying os-release...')
        result = os.system(f'cp ./resources/etc/os-release {self.target_iso_dir}/airootfs/etc/os-release')
        
        if result != 0:
            raise Exception(f'Failed to copy os-release. Code: {result}')
    

    def copy_pacman_conf(self):
        loguru.logger.info(f'Copying pacman.conf...')

        if os.system(f'rm {self.target_iso_dir}/pacman.conf') != 0:
            raise Exception(f'Unable to remove old pacman.conf. Code: {result}')

        os.system(f'cp ./resources/archiso/pacman.conf {self.target_iso_dir}/airootfs/etc/pacman.conf') # Maybe this works????
        result = os.system(f'cp ./resources/archiso/pacman.conf {self.target_iso_dir}/pacman.conf')
        
        if result != 0:
            raise Exception(f'Failed to pacman.conf. Code: {result}')
    

    def copy_profile_def(self):
        loguru.logger.info(f'Copying profiledef.sh...')
        result = os.system(f'cp ./resources/archiso/profiledef.sh {self.target_iso_dir}/profiledef.sh')
        
        if result != 0:
            raise Exception(f'Failed to copy profiledef.sh. Code: {result}')
    

    def copy_grub_config(self):
        loguru.logger.info(f'Copying GRUB config...')
        result = os.system(f'cp ./resources/grub/grub.cfg {self.target_iso_dir}/grub/grub.cfg')
        
        if result != 0:
            raise Exception(f'Failed to copy GRUB config. Code: {result}')
    

    def copy_systemd_boot_config(self):
        loguru.logger.info(f'Copying systemd-boot config...')
        deletion_result = os.system(f'rm -rf {self.target_iso_dir}/efiboot/loader/*')
        
        if deletion_result != 0:
            raise Exception(f'Failed to delete existing systemd-boot config. Code: {result}')


        result = os.system(f'cp -r ./resources/systemd-boot/* {self.target_iso_dir}/efiboot/loader/')
        
        if result != 0:
            raise Exception(f'Failed to copy systemd-boot config. Code: {result}')
    

    def build_iso(self):
        loguru.logger.info(f'Building ISO...')
        result = os.system(f'sudo mkarchiso -v -w builddir {self.target_iso_dir}')
        
        if result != 0:
            raise Exception(f'Failed to build ISO. Code: {result}')