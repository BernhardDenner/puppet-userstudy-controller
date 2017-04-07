#!/usr/bin/env python

import sys
import subprocess
import shlex
import os
import re
import commandline
import logging

class Task(object):

    def __init__(self,
            id,
            name,
            description,
            cnt_image, 
            src_dir,
            method = None,
            modules = None,
            manifest = None,
            duration = None):
        self.id = id
        self.name = name
        self.description = description
        self.cnt_image = cnt_image
        self.method = method
        if modules == None:
            self.modules = "%s/modules" % method
        else:
            self.modules = modules
        if manifest == None:
            self.manifest = "%s/manifests/site.pp" % method
        else:
            self.manifest = manifest
        self.src_dir = "/home/user/src/%s" % src_dir

        self.mgr = None
        self.duration = duration

    def set_manager(self, manager):
        self.mgr = manager

    def print_progress(self):
        exp = self.mgr.get_experiment()
        cur_task_index = exp.get_current_task_index()
        total_tasks = exp.get_number_of_tasks()

        # index starts with 0
        cur_task_index += 1

        sys.stdout.write("\nprogress: [")
        for i in range(0, cur_task_index):
            sys.stdout.write("=")
        for i in range(cur_task_index, total_tasks):
            sys.stdout.write(" ")
        sys.stdout.write("] ")
        print "task {}/{} (including questionnaires) (expected: {} min)".format(
            cur_task_index, total_tasks,
            exp.get_expected_remaining_time()
            )
        sys.stdout.flush()


    def start(self, editor_cnt_id):
        logging.info("starting task %s", self.id)
        if editor_cnt_id == None:
            logging.error("no cnt_id set")
            print "error: no editor container running, experiment started?"
            return False

        print \
"""----------------------------------------------------------------------
{name} test container

{description}

-----------------------------------------------------------------------""".format(
        name=self.name, description=self.description, method=self.method)

        self.print_progress()

        if self.duration != None:
            print """
  Expected time for solving: {} min. Might be a good time for a break now.
  """.format(self.duration)

        c = commandline.Command()
        while not c.yes_no_question("if you are ready press 'y' to start"):
            pass

        print \
"""
starting {name}

adding project folder '{method}' to the editor

use one of the following commands to test your code:

  run_puppet    ... execute puppet
  run_test [-a] ... run puppet and all test cases
                    (without -a stop on first failing test)

if you have done the task run

  exit

-------------------------------------------------------------------------""".format(name=self.name, method=self.method)

        # open the src_dir in editor
        #
        editor_cmd = "docker exec -ti %s /bin/atom_open_file %s" % (
                editor_cnt_id, self.src_dir)

        logging.debug("running docker cmd: %s", editor_cmd)

        p = subprocess.Popen(shlex.split(editor_cmd),
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        logging.debug("got returncode: %s, stdout: '%s', stderr: '%s'",
                p.returncode, out, err)
        if p.returncode != 0:
            print "error while executing editor command:"
            print out
            print err
            return False


        cnt_hostname = re.sub(r'[^\w\d]', '_', self.method)

        docker_cmd =  "docker run -ti --volumes-from %s" % editor_cnt_id
        docker_cmd += " -e MANIFEST=%s -e MODULES=%s" % (self.manifest, self.modules)
        docker_cmd += " -h %s" % cnt_hostname
        docker_cmd += " %s" % self.cnt_image
        docker_cmd += " /bin/container_init.sh"

        logging.debug("running docker command: %s", docker_cmd)

        if self.mgr.devmode:
            print "running command: %s" % docker_cmd

        os.system(docker_cmd)

        print
        c = commandline.Command()
        if not c.yes_no_question("Are you sure you want to terminate this container and proceed with the next task?"):
            logging.debug("restart task")
            print "restarting current task"
            self.start(editor_cnt_id)

        logging.info("task %s finished", self.id)




class QuestionTask(Task):
    def __init__(self, id, name, task_dir, question_file='questions.txt'):
        self.id = id
        self.name = name
        self.task_dir = task_dir
        self.question_file = question_file
        self.duration = 5

    def start(self, editor_cnt_id):
        logging.info("starting QuestionTask %s", self.id)
        if editor_cnt_id == None:
            logging.error("no cnt_id set")
            print "error: not editor container running, experiment started?"
            return False

        self.print_progress()

        print """
  please answer the questionnaire appearing in the editor window
  """

        # open the questionnaire
        #
        editor_cmd = "docker exec -ti {cnt_id} /bin/atom_open_file /home/user/src/{taskdir}/{file}".format(
                cnt_id=editor_cnt_id,
                taskdir=self.task_dir,
                file=self.question_file)
        logging.debug("running docker cmd: %s", editor_cmd)

        p = subprocess.Popen(shlex.split(editor_cmd),
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        logging.debug("got returncode: %s, stdout: '%s', stderr: '%s'",
                p.returncode, out, err)
        if p.returncode != 0:
            print "error while executing editor command:"
            print out
            print err
            return False

        c = commandline.Command()
        while not c.yes_no_question("if you have answered all questions press 'y' to proceed (don't forget to save (CTRL-s))"):
            pass

        logging.info("QuestionTask %s finished", self.id)




