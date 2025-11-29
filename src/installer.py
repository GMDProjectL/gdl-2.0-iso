import loguru
import os
from archiso import Archiso
from systemd import Systemd
from packages import Packages

class Installer(Archiso):
    def __init__(self, target_iso_dir: str, packages: Packages, systemd: Systemd):
        super().__init__(target_iso_dir)
        self.packages = packages
        self.systemd = systemd
        self.opt = f'{self.target_iso_dir}/airootfs/opt'
        self.installer_dir_location = f'{self.opt}/installer'
    
    def clone_installer(self):
        loguru.logger.info("Cloning the installer...")
        return os.system(f'git clone https://github.com/GMDProjectL/gdl-2.0-installer {self.installer_dir_location}') == 0
    
    def create_gui_autostart(self):
        autostart_dir = f'{self.target_iso_dir}/airootfs/etc/skel/.config/autostart'
        desktop_file = f'{autostart_dir}/installer-gui.desktop'

        if not os.path.exists(autostart_dir):
            os.makedirs(autostart_dir)

        with open(desktop_file, 'w') as f:
            f.write(
                '[Desktop Entry]' + '\n' +
                'Exec=/opt/installer/main.py' + '\n' +
                'Path=/opt/installer' + '\n' +
                'Icon=' + '\n' +
                'Name=GDL Installer' + '\n' +
                'Terminal=False' + '\n' +
                'Type=Application' + '\n'
            )
    
    def create_server_systemd_service(self):
        services_dir = f'{self.target_iso_dir}/airootfs/usr/lib/systemd/system'
        service_file = f'{services_dir}/installer-server.service'

        if not os.path.exists(services_dir):
            os.makedirs(services_dir)
        
        with open(service_file, 'w') as f:
            f.write(
                '[Service]' + '\n' +
                'Type=notify' + '\n' +
                'Restart=no' + '\n' +
                'TimeoutSec=30sec' + '\n' +
                'IgnoreSIGPIPE=no' + '\n' +
                'KillMode=none' + '\n' +
                'GuessMainPID=no' + '\n' +
                'RemainAfterExit=no' + '\n' +
                'WorkingDirectory=/opt/installer/server' + '\n' +
                'ExecStart=/opt/installer/server/run.sh' + '\n' +

                '[Install]' + '\n' +
                'WantedBy=multi-user.target' + '\n'
            )
    
    def activate_server_systemd_service(self):
        self.systemd.activate_system_service('installer-server', 'multi-user')