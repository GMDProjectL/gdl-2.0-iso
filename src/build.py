import loguru
from archiso import Archiso
from users import Users

target_iso_dir = "archiso"
archiso = Archiso(target_iso_dir)
users = Users(target_iso_dir)

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


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        loguru.logger.error(e)