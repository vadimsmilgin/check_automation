#!/usr/bin/python

from __future__ import annotations
from abc import ABC, abstractmethod
import os
import sys
import subprocess
import utils

retrieve_unpackaged = 'ant retrieveUnpackaged'
retrieve_sobjects = 'ant retrieveSObjects'
retrieve_workflows = 'ant retrieveWorkflows'


class Context:
    def __init__(self, strategy: Strategy) -> None:
        self._strategy = strategy

    @property
    def strategy(self) -> Strategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        self._strategy = strategy

    def get_s_objects_path(self):
        return self._strategy.get_s_objects_path()

    def get_automation_files_path(self):
        return self._strategy.get_automation_files_path()

    def get_flows_path(self):
        return self._strategy.get_flows_path()

    def get_workflows_path(self):
        return self._strategy.get_workflows_path()

    def get_retrieve_sobjects_path(self):
        return self._strategy.get_retrieve_sobjects_path()

    def execute(self):
        os.chdir(self._strategy.get_sample_path())
        output = subprocess.run(retrieve_unpackaged, shell=True)
        if output.returncode == 0:
            os.chdir(utils.rootFolder)
            package_creator = subprocess.run([sys.executable, 's_object_package_creator.py'], check=True)
            if package_creator.returncode == 0:
                os.chdir(self._strategy.get_sample_path())
                output2 = subprocess.run(retrieve_sobjects, shell=True)
                if output2.returncode == 0:
                    os.chdir(utils.rootFolder)
                    wf_package_creator = subprocess.run([sys.executable, 'workflow_package_creator.py'], check=True)
                    if wf_package_creator.returncode == 0:
                        os.chdir(self._strategy.get_sample_path())
                        output3 = subprocess.run(retrieve_workflows, shell=True)
                        if output3.returncode == 0:
                            os.chdir(utils.rootFolder)
                            subprocess.run([sys.executable, 'validator.py'], check=True)


class Strategy(ABC):
    @abstractmethod
    def get_sample_path(self):
        pass

    @abstractmethod
    def get_automation_files_path(self):
        pass

    @abstractmethod
    def get_flows_path(self):
        pass

    @abstractmethod
    def get_workflows_path(self):
        pass

    @abstractmethod
    def get_retrieve_sobjects_path(self):
        pass

    @abstractmethod
    def get_s_objects_path(self):
        pass


class Windows(Strategy):
    sample_path = '.\\sample'

    automation_files_path = '.\\sample\\retrieveUnpackaged'
    flows_path = '.\\sample\\retrieveUnpackaged\\flows'
    workflows_path = '.\\sample\\retrieveUnpackaged\\workflows'
    retrieve_sobjects_path = '.\\sample\\retrieveSObjects'
    s_objects_path = '.\\sample\\retrieveSObjects\\objects'

    def get_sample_path(self):
        return Windows.sample_path

    def get_automation_files_path(self):
        return Windows.automation_files_path

    def get_flows_path(self):
        return Windows.flows_path

    def get_workflows_path(self):
        return Windows.workflows_path

    def get_retrieve_sobjects_path(self):
        return Windows.retrieve_sobjects_path

    def get_s_objects_path(self):
        return Windows.s_objects_path


class MacOS(Strategy):
    sample_path = './sample'

    automation_files_path = './sample/retrieveUnpackaged'
    flows_path = './sample/retrieveUnpackaged/flows'
    workflows_path = './sample/retrieveUnpackaged/workflows'
    s_objects_path = './sample/retrieveSObjects/objects'
    retrieve_sobjects_path = './sample/retrieveSObjects'

    def get_sample_path(self):
        return MacOS.sample_path

    def get_automation_files_path(self):
        return MacOS.automation_files_path

    def get_flows_path(self):
        return MacOS.flows_path

    def get_workflows_path(self):
        return MacOS.workflows_path

    def get_retrieve_sobjects_path(self):
        return MacOS.retrieve_sobjects_path

    def get_s_objects_path(self):
        return MacOS.s_objects_path
