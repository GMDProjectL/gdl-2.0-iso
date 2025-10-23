import loguru
from archiso import Archiso
from pathlib import Path

class Users(Archiso):
    def __init__(self, target_iso_dir):
        super().__init__(target_iso_dir)

        self.passwd_file = Path(self.target_iso_dir).joinpath('airootfs/etc/passwd')
        self.shadow_file = Path(self.target_iso_dir).joinpath('airootfs/etc/shadow')
        self.group_file = Path(self.target_iso_dir).joinpath('airootfs/etc/group')
        self.gshadow_file = Path(self.target_iso_dir).joinpath('airootfs/etc/gshadow')

    def configure_user(self, username: str, password: str, home: str, shell: str, uid: int, gid: int):
        loguru.logger.info(f'Configuring user {username}')

        with open(self.passwd_file, 'a') as f:
            f.write(f'{username}:x:{gid}:{uid}:{password}:{home}:{shell}' + '\n')

    def configure_shadow(self, username: str, password: str, home: str, shell: str, uid: int, gid: int):
        loguru.logger.info(f'Configuring shadow for {username}')

        with open(self.shadow_file, 'a') as f:
            f.write(f'{username}:x:{gid}:{uid}:{password}:{home}:{shell}' + '\n')

    def configure_group(self, username: str, gid: int, group: str):
        loguru.logger.info(f'Configuring group for {username}')

        with open(self.group_file, 'a') as f:
            f.write(f'{group}:x:{gid}:{username}' + '\n')

    def configure_gshadow(self, username: str, group: str):
        loguru.logger.info(f'Configuring gshadow for {username}')

        with open(self.shadow_file, 'a') as f:
            f.write(f'{group}:!*::{username}' + '\n')