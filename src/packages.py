import loguru
import os
from typing import List
from archiso import Archiso
from pathlib import Path

class Packages(Archiso):
    def __init__(self, target_iso_dir):
        super().__init__(target_iso_dir)

        self.packages: List[str] = []
        self.packages_file = f'{self.target_iso_dir}/packages.x86_64'

    def load_existing_packages(self):
        loguru.logger.info(f'Loading existing packages...')

        with open(self.packages_file, 'r') as f:
            self.packages = f.readlines()
        
        loguru.logger.info(f'Loaded {len(self.packages)} packages: {', '.join(self.packages)}')
    
    def add_packages(self, packages: List[str]):
        for package in packages:
            self.packages.append(package)
    
    def remove_packages(self, packages: List[str]):
        for package in packages:
            self.packages.remove(package)
    
    def dump_packages(self):
        loguru.logger.info(f'Dumped {len(self.packages)} packages into {self.packages_file}...')

        with open(self.packages_file, 'w') as f:
            f.write('\n'.join(self.packages))