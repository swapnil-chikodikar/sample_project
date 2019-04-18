import time
import ssl
from pyvim.task import WaitForTask
import logging as log
from pyvim.connect import SmartConnect, Disconnect
from pyVmomi import vim


class VCenterconnection(object):
    """
    A class which contains the supported functions for VcenterOperations module.
    """

    def __init__(self, hostname, username, password):
        self.flag = 0
        self.conn = self.connect_to_vcenter(hostname, username, password, )

    def connect_to_vcenter(self, hostname=None, username=None, password=None, certFile=None):
        """
        It connects to host.

        Variables :
                    hostname: IP or name of the Vcenter.
                    username: username to access to Vcenter.
                    password: password for specified username.
                    certFile: Optional
        """

        if not certFile:
            try:
                _create_unverified_https_context = ssl._create_unverified_context
            except AttributeError:
                # Legacy Python that doesn't verify HTTPS certificates by default
                pass
            else:
                # Handle target environment that doesn't support HTTPS verification
                ssl._create_default_https_context = _create_unverified_https_context

        try:
            self.connect = SmartConnect(host=hostname,
                                        user=username, pwd=password, certFile=certFile)
            msg = "Successfull connection"
            print(msg)
            return self.connect, msg
        except vim.fault.InvalidLogin as error:
            msg = "Failed to connect to Vcenter %s using credentials \
                    username: %s and password: %s" % (hostname, username, password)
            log.error("Failed to connect to Vcenter {0} using credentials \
                          username: {1} and password: {2}".format(hostname, username, password))
            self.flag = 1
            return self.flag, msg
            # raise Exception(msg)
        except Exception as error:
            msg = "Unable to connect to Vcenter %s because of %s" % (hostname, error)
            log.error(msg)
            self.flag = 1
            # raise Exception(msg)
            return self.flag, msg
            # return msg
