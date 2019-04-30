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
            print('VM creation in-progress')
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
                task = template_vm.Clone(name=new_vm, folder=datacenter.vmFolder, spec=cloneSpec)
                states = [vim.TaskInfo.State.success, vim.TaskInfo.State.error]

                while task.info.state not in states:
                    time.sleep(1)
                status = task.info.state
                if status == "success":
                    print("VM created successfully.")
                if status == "error":
                    print(task.info.error.msg)
                    print(task.info.error)
                    raise task.info.error
                return status

            except Exception as error:
                print(error)

        except Exception as error:
            print(error.message)
            raise error

    def scale_vm(self, esx_host, dc_name, ds_name, temp_name, s_range, e_range, new_vm):
        """
        used to Scale virtual machines using templates.

        - **parameters**, **types**, **return** and **return types**::

        """
        try:
            # for i in range(31, 33):
            for i in range(s_range, e_range):
                # obj = VCenterconnection()
                # self.template_vm('192.168.246.40', 'CRVS-Datacenter', 'CRVS-Datastore-Cluster',
                #                  'CRVS-RHEL6.5-Template', 'rhel6-test{}'.format(i))
                new_name = new_vm + "%s" % i
                self.template_vm(esx_host, dc_name, ds_name, temp_name, new_name)
                time.sleep(2)
                # self.remove_nic('ravi-automation-test{}'.format(i))
                time.sleep(1)
                # self.add_nic('ravi-automation-test{}'.format(i), 'VLAN222-crsrsla-prod')
            time.sleep(5)
            for j in range(s_range, e_range):
                new_name = new_vm + "%s" % j
                self.poweron_vm(new_name)
        except Exception as error:
            print(error.message)
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
            print('VM powered ON successfully')
        if status == "error":
            print("Error: could not power on VM successfully")
            print(task.info.error.msg)
            print(task.info.error)
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

    def power_off(self, name_of_vm):
        """
        power_off(self,name_of_vm): It power off  the Virtual machine.

        Variables:
            name_of_vm(str): Name of the virtual machine.

        Return: power status of the vm.
        """
        try:
            if self:
                vm = self.get_vm_by_name(name_of_vm)
                # import pdb;pdb.set_trace()
                # power_off_task = WaitForTask(vm.PowerOff())
                if vm.summary.runtime.powerState.lower() == 'poweredoff':
                    return
                task = vm.PowerOff()
                states = [vim.TaskInfo.State.success, vim.TaskInfo.State.error]
                while task.info.state not in states:
                    time.sleep(1)
                status = task.info.state
                if status == "success":
                    log.info(task)
                    return status
                if status == "error":
                    log.error(task.info.error.msg)
                    return status
            else:
                raise Vcenterconnectionerror()
        except Exception as error:
            print(error.message)
            raise error

    def destroy_vm(self, name_of_vm):
        """
        used to delete an virtual machine

        - **parameters**, **types**, **return** and **return types**::

        :param vm_name: name of vm that has to be created
        :param vm_name: string
        :return: return status of deletion
        """
        self.power_off(name_of_vm)
        # import pdb;pdb.name_of_vm()
        vm = self.get_dc_object([vim.VirtualMachine], name_of_vm)
        task = vm.Destroy_Task()
        WaitForTask(task)
        states = [vim.TaskInfo.State.success, vim.TaskInfo.State.error]
        while task.info.state not in states:
            time.sleep(1)
        status = task.info.state
        if status == "success":
            return status
        if status == "error":
            log.error(task.info.error.msg)
            log.info(task.info.error)
            return status

    def Multi_vm_delete(self, vm_name, s_range, e_range):
        """
        used to delete an virtual machine

        - **parameters**, **types**, **return** and **return types**::

        :param vm_name: name of vm that has to be created
        :param vm_name: string
        :return: return status of deletion
        """
        try:
            for i in range(s_range, e_range):
                new_name = vm_name + "%s" % i
                self.destroy_vm(new_name)
        except Exception as error:
            print(error.message)
            raise error

    def add_network(self, name_of_vm, port_group):
        """
    Adds new NIC to Virtual machine.

    -**parameters**, **types**, **return** and **return types**

    :param new_vm_name: Name of the VM to add the NIC.
    :type new_vm_name: string
    :param port_group: Port Group to assign the NIC to.
    :type port_group: string
    :param vds: Flag if the given virtual portgroup is of VDS or VSS.
    :type vds: string- yes/no

    :return: success or error
    :rtype: string

    """
        adapter_type = 'e1000'
        vds = "yes"
        try:
            # import sys,pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
            vmachine = self.vcenter.get_dc_object([vim.VirtualMachine], name_of_vm)

            if vds == 'yes':
                network = self.vcenter.get_dc_object([vim.dvs.DistributedVirtualPortgroup], port_group)
            else:
                network = self.get_network(port_group)

            new_nic = vim.vm.ConfigSpec()
            nic_changes = []
            nic_spec = vim.vm.device.VirtualDeviceSpec()
            nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
            if adapter_type == 'e1000':
                nic_spec.device = vim.vm.device.VirtualE1000()
            elif adapter_type == 'vmxnet2':
                nic_spec.device = vim.vm.device.VirtualVmxnet2()
            else:
                nic_spec.device = vim.vm.device.VirtualVmxnet3()
            nic_spec.device.deviceInfo = vim.Description()
            if vds == 'yes':
                vir_port = vim.vm.device.VirtualEthernetCard.DistributedVirtualPortBackingInfo()
                nic_spec.device.backing = vir_port
                dvs_port_connection = vim.dvs.PortConnection()
                dvs_port_connection.portgroupKey = network.key
                dvs_port_connection.switchUuid = network.config.distributedVirtualSwitch.uuid
                nic_spec.device.backing.port = dvs_port_connection
            else:
                nic_spec.device.backing = vim.vm.device.VirtualEthernetCard.NetworkBackingInfo()
                nic_spec.device.backing.useAutoDetect = False
                nic_spec.device.backing.network = network
                nic_spec.device.backing.deviceName = port_group
            nic_spec.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
            nic_spec.device.connectable.startConnected = True
            nic_spec.device.connectable.connected = True
            nic_spec.device.connectable.allowGuestControl = True
            nic_spec.device.connectable.status = 'untried'
            nic_spec.device.wakeOnLanEnabled = True
            nic_spec.device.addressType = 'assigned'
            nic_changes.append(nic_spec)
            new_nic.deviceChange = nic_changes
            add_nic = vmachine.ReconfigVM_Task(spec=new_nic)
            log.info('Adding Network adapter to the VM...')
            while add_nic.info.state not in ['success', 'error']:
                time.sleep(1)
            status = add_nic.info.state
            if status == 'success':
                log.info('Nic added successfully: {}'.format(name_of_vm))
            if status == 'error':
                log.info('Could not add Network adapter {}'.format(name_of_vm))
            return status

        except Exception as error:
            log.info("Caught exception: {} \n {}".format(error, error.message))

    def remove_network(self, name_of_vm):
        """
    Removes all the NICs from the VM.

    -**parameters**, **types**, **return** and **return types**

    :param new_vm_name: Name of the VM to remove NICs.
    :type new_vm_name: string

    :return: success or error
    :rtype: string

    """
        try:
            # vmachine = self.get_vm_by_name(name_of_vm)
            vmachine = self.get_dc_object([vim.VirtualMachine], name_of_vm)
            network = None
            devices = vmachine.config.hardware.device
            networks = []
            for device in devices:
                if isinstance(device, vim.vm.device.VirtualEthernetCard):
                    networks.append(device)
            status = 'error'
            if not networks:
                log.info("INFO: No network adapters connected to the VM to remove")
                status = 'success'
            else:
                for network in networks:
                    name = network.deviceInfo.label
                    nic_spec = vim.vm.device.VirtualDeviceSpec()
                    nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.remove
                    nic_spec.device = network
                    remove_nic = vim.vm.ConfigSpec()
                    remove_nic.deviceChange = [nic_spec]
                    task = WaitForTask(vmachine.ReconfigVM_Task(spec=remove_nic))

                    if task == 'success':
                        log.info("removed '{}' network adapter : {}".format(name, name_of_vm))
                    else:
                        log.info("Could not '{}' Remove Network adapter: {}".format(name, name_of_vm))
                    status = 'success'
            return status
        except Exception as error:
            log.info("Error in 'remove_nic' keyword... {} \n {}".format(error, error.message))

    def add_nic(self, name_of_vm, port_group):
        """
        add_nic(self,name_of_vm,port_group,adapter_type='e1000'):It adds new NIC to Virual machine.

        Variables:
            name_of_vm(str): Name of the virtual machine.
            port_group(str): Name of the port group.
            adapter_type(str): Type of the adaper(default is E1000 and other \
            available are vmxnet2 and vmxnet3).
        Return:
            None
        """
        # self.vcenter = obj
        adapter_type = 'E1000'
        try:
            vm = self.get_vm_by_name(name_of_vm)
            network = self.get_network(port_group)
            new_nic = vim.vm.ConfigSpec()
            nic_changes = []
            nic_spec = vim.vm.device.VirtualDeviceSpec()
            nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
            # import pdb;pdb.set_trace()
            if adapter_type == 'E1000':
                nic_spec.device = vim.vm.device.VirtualE1000()
            elif adapter_type == 'vmxnet2':
                nic_spec.device = vim.vm.device.VirtualVmxnet2()
            else:
                nic_spec.device = vim.vm.device.VirtualVmxnet3()
            nic_spec.device.deviceInfo = vim.Description()
            nic_spec.device.backing = vim.vm.device.VirtualEthernetCard.NetworkBackingInfo()
            nic_spec.device.backing.useAutoDetect = False
            nic_spec.device.backing.network = network
            nic_spec.device.backing.deviceName = port_group
            nic_spec.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
            nic_spec.device.connectable.startConnected = True
            nic_spec.device.connectable.allowGuestControl = True
            nic_spec.device.connectable.connected = False
            nic_spec.device.connectable.status = 'untried'
            nic_spec.device.wakeOnLanEnabled = True
            nic_spec.device.addressType = 'assigned'
            nic_changes.append(nic_spec)
            new_nic.deviceChange = nic_changes
            add_nic = vm.ReconfigVM_Task(spec=new_nic)
            print('Adding Network adapter to the VM...')
            while add_nic.info.state not in ['success', 'error']:
                import time
                time.sleep(1)
            status = add_nic.info.state
            if status == 'success':
                print('Nic added successfully')
            if status == 'error':
                print('Could not add Network adapter')
            return status

        except Exception as error:
            print("Caught exception: {} \n {}".format(error, error.message))

    def remove_nic(self, name_of_vm):
        """
        remove_nic(self,name_of_vm,device_name): It removes the NIC.

        Variables:
            name_of_vm(str): Name of the virtual machine.
           device_number(str): Name of the device(Ex "Network adapter 2"=2).

        Return:
            None

        Note: Power off VM before doing This operation.

        """
        # self.vcenter = obj

        try:
            vm = self.get_vm_by_name(name_of_vm)
            network = None
            devices = vm.config.hardware.device
            networks = []
            for device in devices:
                if isinstance(device, vim.vm.device.VirtualEthernetCard):
                    networks.append(device)
            status = 'error'
            if not networks:
                print("INFO: No network adapters connected to the VM to remove")
                status = 'success'
            else:
                for network in networks:
                    name = network.deviceInfo.label
                    nic_spec = vim.vm.device.VirtualDeviceSpec()
                    nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.remove
                    nic_spec.device = network
                    remove_nic = vim.vm.ConfigSpec()
                    remove_nic.deviceChange = [nic_spec]
                    task = WaitForTask(vm.ReconfigVM_Task(spec=remove_nic))

                    if task == 'success':
                        print("removed '{}' network adapter".format(name))
                    else:
                        print("Could not '{}' Remove Network adapter".format(name))
                    status = 'success'

            return status
        except Exception as error:
            print("Error in 'remove_nic' keyword... {} \n {}".format(error, error.message))

    def Multi_static_ips(self, vm_name, s_range, e_range):
        """
        used to assign Static IPs to Multiple virtual machines

        - **parameters**, **types**, **return** and **return types**::

        :param vm_name: name of vm that has to be created
        :param vm_name: string
        :return: return status of deletion
        """
        try:
            for i in range(s_range, e_range):
                new_name = vm_name + "%s" % i
                self.assign_ip(new_name, '192.168.122.{}'.format(i))
        except Exception as error:
            print(error.message)
            raise error

    def assign_ip(self, name_of_vm, ip):
        """
        template_vm(self, esx_host, dc_name, ds_name, temp_name):
        It creates a new vm from template.

        Variables:
            name_of_vm(str): Name of the VM.
            ip(str): Static IP for the VM created

        Return:
            IP assignment status.

        """
        # self.vcenter = obj
        if self.vm_os_type(name_of_vm) == "Windows":
            print("WWWWWWWWWWWWWWW")
        elif self.vm_os_type(name_of_vm) == "Centos" or self.vm_os_type(name_of_vm) == "Red Hat":
            print("LLLLLLLLLLLLLL")
        # import pdb;pdb.set_trace()
        try:
            self.power_off(name_of_vm)
            vm = self.get_vm_by_name(name_of_vm)
            adaptermap = vim.vm.customization.AdapterMapping()
            adaptermap.adapter = vim.vm.customization.IPSettings()
            adaptermap.adapter.ip = vim.vm.customization.FixedIp()
            # isDHDCP = False

            # if not isDHDCP:
            adaptermap.adapter.ip.ipAddress = ip
            adaptermap.adapter.subnetMask = '255.255.255.0'
            adaptermap.adapter.gateway = '192.168.122.1'

            globalip = vim.vm.customization.GlobalIPSettings(dnsServerList=['10.130.205.71', '10.130.205.78'])

            # import pdb;pdb.set_trace()
            if self.vm_os_type(name_of_vm) == "Centos" or self.vm_os_type(name_of_vm) == "Red Hat":
                ident = vim.vm.customization.LinuxPrep(hostName=vim.vm.customization.FixedName(name=name_of_vm))
            elif self.vm_os_type(name_of_vm) == "Windows":
                ident = vim.vm.customization.Sysprep()
                ident.guiUnattended = vim.vm.customization.GuiUnattended()
                ident.guiUnattended.autoLogon = False  # the machine does not auto-logon
                ident.guiUnattended.password = vim.vm.customization.Password()
                ident.guiUnattended.password.value = "Sungard01"
                ident.guiUnattended.password.plainText = True  # the password is not encrypted
                ident.userData = vim.vm.customization.UserData()
                ident.userData.fullName = "Ravi"
                ident.userData.orgName = "Company"
                ident.userData.computerName = vim.vm.customization.FixedName()
                ident.userData.computerName.name = name_of_vm
                ident.identification = vim.vm.customization.Identification()

            # ident.domain = '{}.crvs.com'.format(name_of_vm)
            customspec = vim.vm.customization.Specification(nicSettingMap=[adaptermap], globalIPSettings=globalip,
                                                            identity=ident)
            try:
                # import pdb;pdb.set_trace()
                task = vm.Customize(spec=customspec)
                WaitForTask(task, self)
                states = ['success', 'error']
                ##                states = [vim.TaskInfo.State.success, vim.TaskInfo.State.error]
                while task.info.state not in states:
                    time.sleep(1)
                status = task.info.state
                if status == "success":
                    print('IP assignmet is successful')
                    time.sleep(1)
                    self.poweron_vm(name_of_vm)
                if status == "error":
                    print(task.info.error.msg)
                    print(task.info.error)
                    raise task.info.error
                return status
            except Exception as error:
                print(error)

        except Exception as error:
            print(error.message)
            raise error

    def get_network(self, port_group_name=None):
        """
        get_network(self,port_group_name = None): It returns the port group object if port_group \
                                    name is spicified otherwise returns all port groups avialable.

        Variables:
            port_group(str): Name of the port_group(optional).

        Return:
            network(obj/list): Port group name specified it returns speific object otherwise
                             returns all the vaialble port groups list.

        """
        network = self.get_obj(self.connect.RetrieveContent(), [vim.Network], port_group_name)
        if network:
            return network
        else:
            raise Exception("port group '{}'  is not available".format(port_group_name))

    def vm_os_type(self, name_of_vm):
        """
        function used to get ostype of vm by using the vm_name

        - **parameters** **types** **return** **rtype**

        :param name_of_vm: name of the VM
        :type name_of_vm: string
        :return: ostype of the name_of_vm
        :rtype: str
        """
        # import pdb;pdb.set_trace()
        vm_obj = self.get_dc_object([vim.VirtualMachine], name_of_vm)
        os_type = vm_obj.config.guestFullName
        if "CentOS" in os_type:
            ostype = "Centos"
            return ostype
        elif "Windows" in os_type:
            ostype = "Windows"
            return ostype
        elif "Red Hat" in os_type:
            ostype = "Red Hat"
            return ostype

    def disconnect(self):
        """
        It disconnect connection object if there is any.
        """

        if self.connect:
            Disconnect(self.connect)
