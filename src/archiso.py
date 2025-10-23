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