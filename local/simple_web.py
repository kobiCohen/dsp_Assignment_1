from subprocess import call
from webbrowser import open_new


def run_server(server_home_dic, port):
    """
    run the server 
    :param server_home_dic:  string-> the directory for the web 
    :param port: int -> the port number you want to run
    :return: None
    """
    call('cd {}; python -m SimpleHTTPServer {}'.format(server_home_dic, port), shell=True)


def open_browser(port):
    """
    open your browser with the website
    :param port: int -> the port number of your website
    :return: None
    """
    open_new('http://127.0.0.1:{}/'.format(port))


def build_and_run_server(server_home_dic, port):
    """
    create and run your browser
    :param server_home_dic:  string-> the directory for the web 
    :param port: int -> the port number you want to run
    :return: None
    """
    open_browser(port)
    run_server(server_home_dic, port)
