#!/usr/bin/env python

import os
import sys
import subprocess
import logging

import commandline


class Manager(object):

    def __init__(self):
        self.editor_cnt_id = None
        self.devmode = False
        self.cmdline = commandline.CommandLine()

        self.task_list = []
        self.groups = {}
        self.tasks = {}

        self.current_group = None
        self.current_task = None
        self.current_task_list = None

        self.current_experiment = None

    #def set_editor_container_id(self, _id):
    #    self.editor_cnt_id = _id

    def get_editor_container_id(self):
        if self.current_experiment != None:
            return self.current_experiment.cnt_id
        return None

    def is_started(self):
        # if we have set an experiment and a cnt_id
        return self.get_editor_container_id() != None

    def set_devmode(self, mode):
        self.devmode = mode

    def shutdown(self):
        logging.info("shutdown manager")
        self.cmdline.shutdown()

    def start(self):
        logging.info("start manager")
        self.cmdline.start()

    def register_command(self, command):
        logging.debug("register command %s", command.get_keyword())
        self.cmdline.register(command)

    def add_task(self, task):
        logging.debug("add task %s", task.id)
        if task.id in self.tasks:
            raise NameError("task %s already defined" % task.id)

        self.tasks[task.id] = task
        self.task_list.append(task)
        task.set_manager(self)

    def get_task(self, id):
        try:
            return self.tasks[id]
        except KeyError:
            return None

    def get_tasks(self):
        return self.tasks

    def add_group(self, name, task_ids):
        logging.debug("add group %s", name)
        if name in self.groups:
            raise NameError("group name %s already defined" % name)

        for i in task_ids:
            if not i in self.tasks:
                raise NameError("task %s does not exist" % i)

        self.groups[name] = task_ids

    def has_group(self, name):
        return name in self.groups

    def get_group_names(self):
        return self.groups.keys()

    def get_tasks_for_group(self, group_name):
        ret = []
        for i in self.groups[group_name]:
            ret.append(self.get_task(i))
        return ret

    def start_experiment(self, experiment):
        logging.info("start experiment: group: %s, user: %s",
                experiment.group_name, experiment.user_name)
        self.current_experiment = experiment
        self.cmdline.set_prompt("(%s) %s" % (experiment.group_name, experiment.user_name))

    def get_experiment(self):
        return self.current_experiment

    def stop_experiment(self):
        logging.info("stop experiment")
        self.current_experiment = None
        self.cmdline.set_prompt("")

