# -*- coding: utf-8 -*-

"""Utilities."""

import os
import re
from stem import Signal
from stem.control import Controller
from urllib3.contrib.socks import SOCKSProxyManager
import certifi

import gevent.monkey
import socket

# Python 2.7 compatibility
# Works for Python 2 and 3
try:
    from importlib import reload
except ImportError:
    try:
        from imp import reload
    except:
        pass

# Python 2.7 compatibility
# Works for Python 2 and 3
try:
    basestring
except NameError:
    basestring = str


def normalize(value):
    """

    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.

    :param value: string.
        String.
    :return: string.
        Cleaned string.
    """
    value = re.sub('[^\w\s-]', '', value).strip()
    value = re.sub('[-\s]+', '-', value)
    return value


def set_save_folder(folder):
    """
    Sets the folder in which lyrics will be downloaded and saved.

    :param folder: string.
        Folder path.
    :return: string.
        Folder path.
    """
    if not folder:
        folder = os.path.join(os.path.expanduser("~"), 'Documents', 'LyricsMaster')
    else:
        folder = os.path.join(folder, 'LyricsMaster')
    return folder


class TorController:
    """
    Controller class for Tor client.

    Allows the Api to make requests over the Tor network.
    If 'controlport' is None, the library will use the default timing to renew the Tor circuit.
    If 'controlport' is passed as an argument, the library will create a new Tor circuit for each new album downloaded.
    See https://www.torproject.org/docs/tor-manual.html.en for more information on how Tor works.

    :param ip: string.
        The IP adress of the Tor proxy.
    :param socksport: integer.
        The SOCKSPORT port number for Tor.
    :param controlport: integer or string.
        The CONTROLPORT port number for Tor or the unix path to the CONTROLPATH.
    :param password: string.
        The password or control_auth_cookie to authenticate on the Tor CONTROLPORT.
    """

    def __init__(self, ip='127.0.0.1', socksport=9050, controlport=None, password=''):
        self.ip = ip
        self.socksport = socksport
        self.controlport = controlport
        self.password = password

    def __repr__(self):
        return '{0}.{1}({2}, {3}, {4}, {5})'.format(__name__, self.__class__.__name__, self.ip, self.socksport,
                                                    self.controlport, self.password)

    def get_tor_session(self):
        """
        Configures and create the session to use a Tor Socks proxy.

        :return: urllib3.SOCKSProxyManager object.
        """
        user_agent = {'user-agent':
                'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
        session = SOCKSProxyManager('socks5://{0}:{1}'.format(self.ip, self.socksport), cert_reqs='CERT_REQUIRED',
                                    ca_certs=certifi.where(), headers=user_agent)
        return session

    def renew_tor_circuit(self):
        """
        Renews the Tor circuit.
        Sends a NEWNYM message to the Tor network to create a new circuit.

        :return: bool.
            Whether a new tor ciruit was created.

        """

        def renew_circuit(password):
            """
            Sends a NEWNYM message to the Tor network to create a new circuit.

            :param password:
            :return: bool.
            """
            controller.authenticate(password=password)
            if controller.is_newnym_available():  # true if tor would currently accept a NEWNYM signal.
                controller.signal(Signal.NEWNYM)
                print('New Tor circuit created')
                result = True
            else:
                delay = controller.get_newnym_wait()
                print('Delay to create new Tor circuit: {0}s'.format(delay))
                result = False
            return result

        # Needs to reload the default socket to be able to send the is_newnym_avilable and get_newnym_wait signals
        reload(socket)
        if isinstance(self.controlport, int):
            with Controller.from_port(port=self.controlport) as controller:
                is_renewed = renew_circuit(self.password)
        elif isinstance(self.controlport, basestring):
            with Controller.from_socket_file(path=self.controlport) as controller:
                is_renewed = renew_circuit(self.password)
        else:
            is_renewed = False
        gevent.monkey.patch_socket()
        return is_renewed
