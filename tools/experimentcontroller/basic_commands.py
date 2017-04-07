#!/usr/bin/env python2.7

import os
import subprocess
import shlex
import time
import re
import tempfile
import logging
import time

from commandline import Command
from experiment import Experiment


EDITOR_CNT_IMAGE = "experiment-editor:xenial"

class ExecCommand(Command):
    def __init__(self, mgr):
        self.set_mgr(mgr)

    def exec_cmd(self, command, silent=False):
        logging.debug("running command: %s", command)
        if self.mgr.devmode:
            print "running command: %s" % command

        cmd = shlex.split(command)

        try:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
            logging.debug("command exited: returncode: %s, stdout: '%s', stderr: '%s'",
                    p.returncode, out, err)

            if p.returncode != 0:
                logging.error("error running command: %s", command)
                if not silent:
                    print "error running command:"
                    print err

            return (out, p.returncode)
        except (OSError, ValueError), err:
            logging.error("error running command: %s", err)
            if not silent:
                print "error running command:"
                print err

        return (None, -1)

class QuitControler(Command):
    def __init__(self, mgr):
        self.set_mgr(mgr)

    def get_keyword(self):
        return "quit"

    def run(self, args):
        if self.mgr.is_started():
            print "You have an experiment running, stop it first"
            return

        self.mgr.shutdown()


class NewExperiment(ExecCommand):

    def __init__(self, mgr):
        self.set_mgr(mgr)

    def get_keyword(self):
        return "new_experiment"

    def complete_cmd(self, args):
        if len(args) == 1:
            return self.mgr.get_group_names()
        return None


    def help_msg(self):
        return "%s: [group] [name]" % self.get_keyword()

    def run(self, args):
        if self.mgr.is_started():
            print "experiment already running"
            return

        if len(args) != 2:
            print "error: {} requires two parameter".format(self.get_keyword())
            print self.help_msg()
            return

        group = args[0]
        user_name = args[1]

        if not re.search("^[a-zA-Z0-9_]+$", user_name):
            logging.info("invalid username used: %s", user_name)
            print "error: name must not contain characters other than letters, numbers and _"
            return

        if not self.mgr.has_group(group):
            logging.info("wrong group name used: %s", group)
            print "error: group %s not defined" % group
            return

        ## raises exception if group is invalid
        tasks = self.mgr.get_tasks_for_group(group)
        experiment = Experiment(group, user_name, tasks)

        logging.info("starting new experiment for %s, group: %s", user_name, group)
        print "starting new experiment for user: {}, group: {}".format(user_name, group)
        # ensure we have access to the local display
        self.exec_cmd("xhost +local:", silent=True)

        print 
        print "starting new editor container..."

        # start container as root, we will switch witin the init script
        #docker_cmd = "docker run -d"
        docker_cmd = "docker create"
        docker_cmd += " --name exp_%s_%s" % (group, user_name)
        # volume mount for X11 socket, if local X-display is used
        docker_cmd += " -v /tmp/.X11-unix:/tmp/.X11-unix"

        # ssh forwarded connection require the xauth mechanism
        xauth_file = "%s/.Xauthority" % os.environ['HOME']
        if os.path.isfile(xauth_file):
            docker_cmd += " -v %s:/tmp/.xauth" % xauth_file

        docker_cmd += " -e DISPLAY=%s" % os.environ['DISPLAY']
        # if we use a X11 display over network (ssh)
        docker_cmd += " --net=\"host\""

        if self.mgr.devmode:
            docker_cmd += " -v %s:/home/user/src" % os.path.abspath(
                    os.path.join(os.path.dirname(__file__), "../../experiments")
                    )
        else:
            docker_cmd += " -v /home/user/src"

        docker_cmd += " " + EDITOR_CNT_IMAGE

        # run the docker_cmd command
        out, ret = self.exec_cmd(docker_cmd)
        cnt_id = out.strip()
        if ret == 0:
            logging.debug("got editor container id: %s", cnt_id)
            if self.mgr.devmode:
                print "id: %s" % cnt_id

            # on CentOS, the xauth file has selinux label attached, thus the 
            # container is not able to read it, therefore, try to copy it into
            # the container directly
            # Note: this work only for docker > 1.8
            if os.path.isfile(xauth_file):
                out, ret = self.exec_cmd("docker cp %s %s:/home/user/.Xauthority" % (xauth_file, cnt_id), silent=True)

            out, ret = self.exec_cmd("docker start %s" % cnt_id)
            if ret != 0:
                logging.error("error starting editor container")
                return False

            # everything worked as expected, set container id and experiment
            experiment.cnt_id = cnt_id
            logging.debug("about to start experiment")
            self.mgr.start_experiment(experiment)

            return True
        else:
            logging.error("could not start experiment editor container")
            print "could not start editor container"
            print "maybe you have to choose a different 'user name'"

        return False


class AbortExperiment(ExecCommand):
    def __init__(self, mgr):
        self.set_mgr(mgr)

    def get_keyword(self):
        return "abort_experiment"

    def run(self, args):
        if not self.mgr.is_started():
            print "no experiment running"
            return

        if not self.yes_no_question("Do you really want to quit the running experiment?"):
            return

        logging.debug("killing editor container")
        print "stopping editor container..."
        out, ret = self.exec_cmd("docker kill %s" % self.mgr.get_editor_container_id())
        #self.mgr.set_editor_container_id(None)
        self.mgr.stop_experiment()


class Start(Command):
    def __init__(self, mgr):
        self.set_mgr(mgr)

    def get_keyword(self):
        return "start"

    def run(self, args):
        if len(args) > 0:
            print "start does not take arguments"
            return

        if not self.mgr.is_started():
            print "no experiment environment started, use 'new_experiment' first"
            return

        exp = self.mgr.get_experiment()
        task = None
        if exp.get_current_task():
            logging.info("experiment already running, continuing with last task")
            print "experiment already started, continuing with current task..."
            task = exp.get_current_task()
        else:
            logging.info("starting with first task")
            task = exp.next_task()

        while task != None:
            logging.info("starting task: %s", task.id)
            task.start(self.mgr.get_editor_container_id())
            #print
            #if self.yes_no_question("Are you sure you have finished our task?"):
            #    task = exp.next_task()
            #else:
            #    logging.debug("restarting task")
            #    print "restarting last task"
            task = exp.next_task()

        print
        print
        print " Congratulations !!! you've done all your tasks ;)"
        print " Thank you for participating"
        print 
        print "if you want to redo a specific task use 'start_task' otherwise just type"
        print
        print " 'finished'"



class FinishExperiment(ExecCommand):
    def __init__(self, mgr):
        self.set_mgr(mgr)

    def get_keyword(self):
        return "finished"

    def run(self, args):
        if not self.mgr.is_started():
            print "no experiment running"
            return

        exp = self.mgr.get_experiment()

        if not self.yes_no_question("Are you sure you have done all your tasks?"):
            return

        print "saving logs..."
        cnt_logs = tempfile.NamedTemporaryFile()
        try:
            out, ret = self.exec_cmd("docker logs -t %s" % self.mgr.get_editor_container_id())
            cnt_logs.write(out)
            cnt_logs.flush()

            self.exec_cmd("docker cp {} {}:/var/log/experiment_container.log".format(cnt_logs.name, 
                self.mgr.get_editor_container_id()))
        finally:
            cnt_logs.close()

        src_tarball = "exp_{}_{}_{}.tar.gz".format(
                exp.group_name, exp.user_name,
                time.strftime("%Y%m%d_%H%M%S")
                )
        print "saving sources to {} ...".format(src_tarball)
        out, err = self.exec_cmd(
                "docker exec -ti {} /bin/build_src_tarball.sh '/root/{}'".format(
                    self.mgr.get_editor_container_id(), src_tarball)
                )

        out, err = self.exec_cmd(
                "docker cp {}:/root/{} {}".format(
                    self.mgr.get_editor_container_id(), src_tarball, src_tarball)
                )

        print "stopping editor container..."
        out, ret = self.exec_cmd("docker kill %s" % self.mgr.get_editor_container_id())

        print "saving editor container..."
        out, ret = self.exec_cmd("docker commit {} exp_{}_{}".format(
            self.mgr.get_editor_container_id(),
            exp.group_name,
            exp.user_name))
        print out
        self.mgr.stop_experiment()


class StartTask(Command):
    def __init__(self, mgr):
        self.set_mgr(mgr)

    def get_keyword(self):
        return "start_task"

    def complete_cmd(self, args):
        # only complete first argument
        if len(args) == 1 and self.mgr.is_started():
            return self.mgr.get_experiment().get_task_ids()
        return []

    def run(self, args):
        if not self.mgr.is_started():
            logging.error("no experiment running")
            print "no experiment running"
            return

        exp = self.mgr.get_experiment()
        task = None
        task_ids = exp.get_task_ids()
        if len(task_ids) == 0:
            logging.error("no task for group %s defined", exp.group_name)
            print "error no task for group %s defined" % exp.group_name
            return

        # without arguments task first task
        if not args:
            logging.debug("starting with first task")
            task_id = task_ids[0]
        else:
            if not args[0] in task_ids:
                logging.error("task %s not defined for group %s", args[0], exp.group_name)
                print "task '%s' not defined for group %s" % (args[0],
                        exp.group_name)
                return
            task_id = args[0]
            logging.debug("about to start task %s", task_id)

        exp.set_current_task_id(task_id)
        task = exp.get_current_task()

        task.start(self.mgr.get_editor_container_id())


class PullImages(ExecCommand):
    def __init__(self, mgr):
        self.set_mgr(mgr)

    def get_keyword(self):
        return "pull_images"

    def help_msg(self):
        return "%s: [image repo/prefix]\n" \
               "    default prefix: 'bernhard97'" % self.get_keyword()

    def run(self, args):
        prefix = "bernhard97"

        if len(args) > 1:
            print self.help_msg()
            return False
        elif len(args) == 1:
            prefix = args[0]

        images = []
        images.append(EDITOR_CNT_IMAGE)
        for task in self.mgr.get_tasks().values():
            if hasattr(task, 'cnt_image') and not task.cnt_image in images:
                images.append(task.cnt_image)

        logging.debug("pulling the following images with prefix %s: %s" % (prefix, images))

        tag_flags = ""
        out, ret = self.exec_cmd("docker help tag")
        if ret == 0:
            if "--force" in out:
                tag_flags = "--force"
        else:
            logging.error("error running docker help tag, using 'tag' without '--force' flag")

        success = True
        for image in images:
            repo_image = "{}/{}".format(prefix, image)
            docker_cmd = "docker pull {}".format(repo_image)

            print "pulling image %s ..." % repo_image
            logging.debug("running command: %s", docker_cmd)
            ret = os.system(docker_cmd)
            if ret != 0:
                success = False
                logging.error("failed pulling image %s", repo_image)
                print "error pulling image {}".format(repo_image)
            else:
                logging.debug("successfully pulled image %s", repo_image)
                # tag the image, so do not have to take care of the repo prefix
                self.exec_cmd("docker tag {} {} {}".format(tag_flags, repo_image, image))
            print

        if success != True:
            print "one or more images couldn't be pulled, please try again"




