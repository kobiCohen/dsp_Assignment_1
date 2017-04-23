from subprocess import check_output, CalledProcessError, STDOUT
from logger.logger import Logger

log = Logger()


def install_programs():
    programs_list = ['python', 'poppler-utils']
    for program in programs_list:
        try:
            stdout_output = check_output(['sudo', 'apt', 'install', program], stderr=STDOUT)
        except CalledProcessError as ex:
            log.critical('deploy failed')
            log.critical(ex.message)
            exit(-1)


def install_python_package():
    pass


def deploy():
    install_programs()
    install_python_package()


