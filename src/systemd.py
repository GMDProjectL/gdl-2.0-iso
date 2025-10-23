import loguru
import os
from archiso import Archiso
from pathlib import Path

class Systemd(Archiso):
    def __init__(self, target_iso_dir):
        super().__init__(target_iso_dir)
    
    def activate_system_service(self, name: str, target: str):
        loguru.logger.info(f'Activating `{name}` service...')
        result = os.system(f'ln -s /usr/lib/systemd/system/{name}.service archlive/airootfs/etc/systemd/system/{target}.target.wants/{name}.service')
        
        if result != 0:
            raise Exception(f'Failed to create symlink. Code: {result}')