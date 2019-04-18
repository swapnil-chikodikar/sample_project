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

    # def __init__(self, hostname, username, password):
    #
    #     self.conn = self.connect_to_vcenter(hostname, username, password)

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

            return msg
            # raise Exception(msg)
        except Exception as error:
            msg = "Unable to connect to Vcenter %s because of %s" % (hostname, error)
            log.error(msg)

            # raise Exception(msg)
            return msg
            # return msg

    def get_dc_object(self, vim_type, name):
        """
        Get the vsphere object associated with a given vim_type.

        variables:
            vimtype: It is type of the object that you want to return. example:vm or esxi host.
        """
        obj = None
        content = self.connect.RetrieveContent()
        container = content.viewManager.CreateContainerView(content.rootFolder, vim_type, True)
        for data in container.view:
            if data.name == name:
                obj = data
                break
        return obj

    def template_vm(self, esx_host, dc_name, ds_name, temp_name, new_vm):
        """
        template_vm(self, esx_host, dc_name, ds_name, temp_name):
        It creates a new vm from template.

        Variables:
            esx_host(str): Name of the cluster.
            dc_name(str): name of datacenter name.
            ds_name(str): name ofdatastore name.
            temp_name(str): name of template name.
            new_vm(str): name of new vm.

        Return:
            cloned object.

        WARNING:: template and datastore host must be same.
        """
        try:
            print 'VM creation in-progress'
            cluster = self.get_dc_object([vim.ComputeResource], esx_host)
            host = self.get_dc_object([vim.HostSystem], esx_host)
            if cluster == None:
                host_parent = host.parent
                resource_pool = host_parent.resourcePool
            else:
                resource_pool = cluster.resourcePool
            datacenter = self.get_dc_object([vim.Datacenter], dc_name)
            datastore = self.get_dc_object([vim.Datastore], ds_name)
            template_vm = self.get_dc_object([vim.VirtualMachine], temp_name)

            try:
                # Relocation spec
                relospec = vim.vm.RelocateSpec()
                relospec.datastore = datastore
                relospec.pool = resource_pool
                # relospec.host = target_host
                cloneSpec = vim.vm.CloneSpec(powerOn=False, template=False, location=relospec,
                                             customization=None, config=None)
                task = template_vm.Clone(name=new_vm, folder=datacenter.vmFolder, \
                                         spec=cloneSpec)
                states = [vim.TaskInfo.State.success, vim.TaskInfo.State.error]

                while task.info.state not in states:
                    time.sleep(1)
                status = task.info.state
                if status == "success":
                    print "VM created successfully."
                if status == "error":
                    print task.info.error.msg
                    print task.info.error
                    raise task.info.error
                return status

            except Exception as error:
                print error

        except Exception as error:
            print error.message
            raise error

    def scale_vm(self, esx_host, dc_name, ds_name, temp_name, new_vm):
        """
        used to Scale virtual machines using templates.

        - **parameters**, **types**, **return** and **return types**::

        """

        try:
            for i in range(31, 33):
                # obj = VCenterconnection()
                # self.template_vm('192.168.246.40', 'CRVS-Datacenter', 'CRVS-Datastore-Cluster',
                #                  'CRVS-RHEL6.5-Template', 'rhel6-test{}'.format(i))
                self.template_vm(esx_host, dc_name, ds_name, temp_name, new_vm)
                time.sleep(2)
                # self.remove_nic('ravi-automation-test{}'.format(i))
                time.sleep(1)
                # self.add_nic('ravi-automation-test{}'.format(i), 'VLAN222-crsrsla-prod')
            time.sleep(5)
            for j in range(31, 33):
                self.poweron_vm('rhel6-test{}'.format(j))
        except Exception as error:
            print error.message
            raise error

    def poweron_vm(self, name_of_vm):
        """
        poweron_vm(self,name_of_vm): It power on  the Virtual machine.

        Variables:
            name_of_vm(str): Name of the virtual machine.

        Return: power status of the vm.
        """
        vm = self.get_vm_by_name(name_of_vm)
        task = vm.PowerOn()
        WaitForTask(task, self)
        states = ['success', 'error']
        # states = [vim.TaskInfo.State.success, vim.TaskInfo.State.error]
        while task.info.state not in states:
            time.sleep(1)
        status = task.info.state
        if status == "success":
            print 'VM powered ON successfully'
        if status == "error":
            print "Error: could not power on VM successfully"
            print task.info.error.msg
            print task.info.error
            raise task.info.error
        return status

    def get_obj(self, content, vimtype, name=None):
        """
        Get the vsphere object associated with a given text name.

        variables:
            content: It is a Vcenter object.
            vimtype: It is type of the object that want to return. example:vm or esxi host.
            name: name of machine
        return:
            vimtype object.

        """
        if content.viewManager:
            machine_obj = None
            container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
            if name:
                for data in container.view:
                    if data.name == name:
                        machine_obj = data
                        break
                return machine_obj
            else:
                machine_obj = container.view
                return machine_obj

    def get_vm_by_name(self, name=None):
        """
        Find a virtual machine by it's name and return it.

        variables:
            name : Name of the virtual for which you want retrieve object.
        return:
            vm object.
        """

        vm_obj = self.get_obj(self.connect.RetrieveContent(), [vim.VirtualMachine], name)
        if vm_obj:
            return vm_obj
        else:
            print("VMUNAVAILABLE(NAME)")
            # raise VMUnavaiable(name)
