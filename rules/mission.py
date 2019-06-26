#!/bin/python
#encoding:utf-8

import json
import ConfigParser

from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
from ansible.inventory.host import Host


Options = namedtuple('Options',
                     ['connection', 'module_path', 'forks', 'timeout', 'remote_user', 'private_key_file',
                                         'ask_pass', 'ssh_common_args', 'ssh_extra_args',
                                         'sftp_extra_args',
                                         'scp_extra_args', 'become', 'become_method', 'become_user', 'ask_value_pass',
                                         'verbosity',
                                         'check', 'listhosts', 'listtasks', 'listtags', 'syntax', 'diff'])


#private_key_file
class ResultCallback(CallbackBase):
    def __init__(self, taskid, writeBackUrl, host):
        super(ResultCallback, self).__init__()
        self.taskid = taskid
        self.writeBackUrl = writeBackUrl
        self.host = host

    def v2_runner_on_ok(self, result, **kwargs):
        """Print a json representation of the result

        This method could store the result in an instance attribute for retrieval later
        """
        # logger.info("ansible执行成功：")
        # logger.info(result._result)
        print result._result
        pass

    def v2_runner_on_failed(self, result, **kwargs):

        # logger.error("ansible执行失败")
        # logger.error(result._result)
        print result._result
        pass


class BasisAnsibleobject(object):
    def __init__(self, ):
        self.loader = DataLoader()
        self.options = Options(connection='smart', module_path='/path/to/mymodules', forks=100, timeout=10,
                               remote_user='ubuntu', private_key_file='/root/.ssh/id_rsa', ask_pass=False, ssh_common_args=None,
                               ssh_extra_args=None,
                               sftp_extra_args=None, scp_extra_args=None, become=None, become_method=None,
                               become_user=None, ask_value_pass=False, verbosity=None, check=False, listhosts=False,
                               listtasks=False, listtags=False, syntax=False, diff=False)

        self.passwords = dict(sshpass=None, becomepass=None)

        self.inventory = InventoryManager(loader=self.loader, sources='/etc/ansible/hosts')
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)

    def createplay(self, filename, hosts, taskid, username, password, sshLoginType, systemType, command):  # action
        try:
            with open('/etc/ansible/{0}'.format(hosts), 'w') as f:
                f.writelines(hosts)
        except Exception as e:
            # logger.error("【错误】 ansible配置文件写入失败 -- mission.py line68")
            pass

        self.inventory = InventoryManager(loader=self.loader, sources='/etc/ansible/{0}'.format(hosts))
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)

        if sshLoginType == 'ssh_key' and systemType == 'linux':
            command = "iptables-save"  #重启防火墙命令
            remote_command = command
            self.variable_manager.set_host_variable(Host(hosts, '22'), 'ansible_ssh_user', username)
            self.variable_manager.set_host_variable(Host(hosts, '22'), 'ansible_ssh_pass', password)

            play_source = dict(
                name="Ansible Play",
                hosts='all',
                gather_facts='no',
                tasks=[
                    dict(action=dict(module="command", args=remote_command)),

                    dict(action=dict(module="command", args=command)),

                ]
            )

        self.play = Play.load(play_source, variable_manager=self.variable_manager, loader=self.loader)

        return self.play,self.variable_manager,self.inventory


class Taskmanager(BasisAnsibleobject):
    def __init__(self, taskid, variable_manager, inventory, writeBackUrl,hosts,username,password,sshLoginType,systemType):
        super(Taskmanager, self).__init__()
        self.hosts = hosts
        self.results_callback = ResultCallback(taskid,writeBackUrl,hosts)
        self.tqm = None
        self.variable_manager = variable_manager
        if sshLoginType == 'ssh_key' and systemType == 'linux':
            self.variable_manager.set_host_variable(Host(hosts, '22'), 'ansible_ssh_user', username)
            self.variable_manager.set_host_variable(Host(hosts, '22'), 'ansible_ssh_pass', password)

        self.inventory = inventory

    def CreateTask(self, ):
        self.tqm = TaskQueueManager(
            inventory=self.inventory,
            variable_manager=self.variable_manager,
            loader=self.loader,
            options=self.options,
            passwords=self.passwords,
            stdout_callback=self.results_callback,
        )
        return self.tqm

    def start(self, tqm, play):
        try:
            result = tqm.run(play)
        except Exception as e:
            print(str(e))
        finally:
            if self.tqm is not None:
                self.tqm.cleanup()


def ansible_do_something(fileName, systemIP, taskid, command, writeBackUrl, userName, passWord, sshLoginType,
                         systemType):
    try:
        play_manager = BasisAnsibleobject()
        play, variable_manager, inventory = play_manager.createplay(filename=fileName, hosts=systemIP,
                                                                    taskid=taskid, username=userName, password=passWord,
                                                                    sshLoginType=sshLoginType, systemType=systemType,
                                                                    command=command)
        task = Taskmanager(taskid, variable_manager, inventory,
                           writeBackUrl, systemIP, userName,
                           passWord, sshLoginType, systemType)

        tqm = task.CreateTask()
        task.start(tqm=tqm, play=play)
    except Exception as e:
        return False
    return True


class Mission(object):

    def __init__(self):
        pass

    @staticmethod
    def create_firewall_rule(host, username, password, command):
        ansible_do_something("public.xml", systemIP=host, taskid="",
                             command=command,
                             writeBackUrl="",
                             userName=username,
                             passWord=password,
                             sshLoginType="ssh_key",
                             systemType="linux")
        pass

