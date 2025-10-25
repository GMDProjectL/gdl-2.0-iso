import loguru
import os
from archiso import Archiso
from pathlib import Path

class Users(Archiso):
    def __init__(self, target_iso_dir):
        super().__init__(target_iso_dir)

        self.passwd_file = Path(self.target_iso_dir).joinpath('airootfs/etc/passwd')
        self.shadow_file = Path(self.target_iso_dir).joinpath('airootfs/etc/shadow')
        self.group_file = Path(self.target_iso_dir).joinpath('airootfs/etc/group')
        self.gshadow_file = Path(self.target_iso_dir).joinpath('airootfs/etc/gshadow')

    def copy_sudoers(self):
        loguru.logger.info('Copying sudoers...')

        os.system(f'mkdir {self.target_iso_dir}/airootfs/etc/sudoers.d')
        result = os.system(f'cp ./resources/etc/sudoers.d/* {self.target_iso_dir}/airootfs/etc/sudoers.d/')

        if result != 0:
            raise Exception('Can\'t copy sudoers.')

    def configure_user(self, username: str, password: str, home: str, shell: str, uid: int, gid: int):
        loguru.logger.info(f'Configuring user {username}')

        with open(self.passwd_file, 'a') as f:
            f.write(f'{username}:x:{gid}:{uid}:{password}:{home}:{shell}' + '\n')

    def configure_shadow(self, username: str, password: str, home: str, shell: str, uid: int, gid: int):
        loguru.logger.info(f'Configuring shadow for {username}')

        with open(self.shadow_file, 'a') as f:
            f.write(f'{username}::14871::::::' + '\n')

    def configure_group(self, username: str, gid: int, group: str):
        loguru.logger.info(f'Configuring group for {username}')

        with open(self.group_file, 'a') as f:
            f.write(f'{group}:x:{gid}:{username}' + '\n')

    def configure_gshadow(self, username: str, group: str):
        loguru.logger.info(f'Configuring gshadow for {username}')

        with open(self.shadow_file, 'a') as f:
            f.write(f'{group}:!*::{username}' + '\n')
