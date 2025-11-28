import loguru
from archiso import Archiso
from users import Users
from systemd import Systemd
from packages import Packages
from temp_sh import TempSh
from kde import KDE

target_iso_dir = "archiso"
archiso = Archiso(target_iso_dir)
users = Users(target_iso_dir)
systemd = Systemd(target_iso_dir)
packages = Packages(target_iso_dir)
temp_sh = TempSh()
kde = KDE(target_iso_dir, packages, systemd)

def main():
    loguru.logger.info("Builder is ready.")

    archiso.copy_releng_config()
    archiso.copy_pacman_conf()
    
    users.configure_user('root', '', '/root', '/usr/bin/fish', 0, 0)
    users.configure_shadow('root', '', '/root', '/usr/bin/fish', 0, 0)
    users.configure_group('root', 0, 'root')
    users.configure_gshadow('root', 'root')

    users.configure_user('liveuser', '', '/home/liveuser', '/usr/bin/fish', 1000, 1000)
    users.configure_shadow('liveuser', '', '/home/liveuser', '/usr/bin/fish', 1000, 1000)

    for group in ['adm', 'wheel', 'uucp', '']:
        users.configure_group('liveuser', 1000, group)
    
    users.configure_gshadow('liveuser', '')

    users.copy_sudoers()

    packages.load_existing_packages()
    packages.add_packages([
        'vulkan-intel', 'vulkan-nouveau', 'vulkan-mesa-layers', 'networkmanager',
        'linux-zen', 'linux-zen-headers', 'dkms', 'mesa-utils', 'broadcom-wl-dkms', 'fish', 
        'chromium', # sorry, but for real, firefox LAGS my VM, Mozilla should really consider doing smth with it
        'cups', 'grub-customizer', 'yay-bin', 'rsync', 'python-flask', 'python-requests', 'pyside6',
        'qqc2-desktop-style', 'qqc2-breeze-style', 'base-devel', 'git'
    ])
    packages.remove_packages(['broadcom-wl', 'grml-zsh-config', 'lftp', 'linux', 'linux-headers'])

    kde.install_aio()
    
    packages.dump_packages()

    systemd.activate_system_service('NetworkManager', 'multi-user')

    archiso.copy_profile_def()
    archiso.copy_grub_config()
    archiso.copy_systemd_boot_config()
    archiso.copy_os_release()

    archiso.build_iso()
    temp_sh.upload()


if __name__ == '__main__':
    main()