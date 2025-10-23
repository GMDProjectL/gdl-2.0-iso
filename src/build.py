import loguru
from archiso import Archiso
from users import Users
from systemd import Systemd
from packages import Packages

target_iso_dir = "archiso"
archiso = Archiso(target_iso_dir)
users = Users(target_iso_dir)
systemd = Systemd(target_iso_dir)
packages = Packages(target_iso_dir)

def main():
    loguru.logger.info("Builder is ready.")

    archiso.copy_releng_config()
    
    users.configure_user('root', '', '/root', '/usr/bin/zsh', 0, 0)
    users.configure_shadow('root', '', '/root', '/usr/bin/zsh', 0, 0)
    users.configure_group('root', 0, 'root')
    users.configure_gshadow('root', 'root')

    users.configure_user('liveuser', '', '/home/liveuser', '/usr/bin/zsh', 1000, 1000)
    users.configure_shadow('liveuser', '', '/home/liveuser', '/usr/bin/zsh', 1000, 1000)

    for group in ['adm', 'wheel', 'uucp', '']:
        users.configure_group('liveuser', 1000, group)
    
    users.configure_gshadow('liveuser', '')

    packages.load_existing_packages()
    packages.add_packages([
        'vulkan-intel', 'vulkan-nouveau', 'vulkan-mesa-layers', 'networkmanager',
        'linux-headers', 'dkms', 'mesa-utils', 'broadcom-wl-dkms'
    ])
    packages.remove_packages(['broadcom-wl', 'grml-zsh-config'])
    packages.dump_packages()


    systemd.activate_system_service('NetworkManager', 'multi-user')


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        loguru.logger.error(e)