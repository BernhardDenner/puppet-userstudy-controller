#!/usr/bin/env python2.7

import os
import logging
import sys
import time

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), "experimentcontroller/")
    ))

import commandline
import manager
import basic_commands
from task import Task
from task import QuestionTask


VERSION = "v1.4"
LOG_FILENAME = "experiments_%s.log" % time.strftime("%Y%m%d_%H%M%S")




if __name__ == "__main__":
    logging.basicConfig(filename=LOG_FILENAME,
                    format='%(asctime)s:%(levelname)s:%(message)s',
                    level=logging.DEBUG,
                    )

    logging.info("starting experiment controller version %s", VERSION)
    print "Experiment controller version %s" % VERSION

    if 'DISPLAY' not in os.environ or len(os.environ['DISPLAY']) == 0:
        logging.error("no display variable set")
        print "Error: no DISPLAY variable set. A graphical interface is required"
        sys.exit(1)
    else:
        logging.debug("display: '%s'", os.environ['DISPLAY'])


    mgr = manager.Manager()
    if '--dev' in sys.argv:
        logging.info("dev mode enabled")
        mgr.devmode = True
        print "devmode enabled"
        print "logging to %s" % LOG_FILENAME

    mgr.register_command(basic_commands.QuitControler(mgr))
    mgr.register_command(basic_commands.NewExperiment(mgr))
    mgr.register_command(basic_commands.AbortExperiment(mgr))
    mgr.register_command(basic_commands.StartTask(mgr))
    mgr.register_command(basic_commands.FinishExperiment(mgr))
    mgr.register_command(basic_commands.Start(mgr))
    mgr.register_command(basic_commands.PullImages(mgr))

    mgr.add_task(Task(
        id = "task1a",
        name = "Task 1 method A",
        description = """
  Our development team has released the fresh new application called 'calculator'.
  Our task is to write a Puppet module for this application to allow an automatic
  deployment and configuration on our server farm. 'calculator' uses a
  JSON style configuration file.
  
  The Puppet module is almost complete. Your task is to define the missing
  configuration part(s). Therefore, you  have to define the required Puppet code
  to write the requested configuration settings to the specified file.
  
  Write the configuration part for the Puppet module 'calculator' using the 
  resource type 'file' together with an ERB template:
   - modules/calculator/manifests/config.pp
   - modules/calculator/templates/config.json.erb

  If you are unfamiliar with the resource type `file` or how to write a ERB
  template, read Chapter "File Resource Type" and Chapter "ERB Templates" in
  the Puppet guide before you start the task.
""",
        cnt_image = "puppet-experiment-task1:xenial",
        method = "T1_method_A",
        src_dir = "task1/T1_method_A",
        duration = 25
        )
    )
    mgr.add_task(Task(
        id = "task1b",
        name = "Task 1 method B",
        description = """
  Our development team has released the fresh new application called 'calculator'.
  Our task is to write a Puppet module for this application to allow an automatic
  deployment and configuration on our server farm. 'calculator' uses a
  JSON style configuration file.
  
  The Puppet module is almost complete. Your task is to define the missing
  configuration part(s). Therefore, you  have to define the required Puppet code
  to write the requested configuration settings to the specified file.
  
  Write the configuration part for the Puppet module 'calculator' using the 
  resource types 'kdbmount' and 'kdbkey' only:
   - modules/calculator/manifests/config.pp

  If you are unfamiliar with the concepts of Libelektra, read the Chapter 
  "Libelektra: Kdbmount and Kdbkey" in the Puppet guide before you start the task.
""",
        cnt_image = "puppet-experiment-task1:xenial",
        method = "T1_method_B",
        src_dir = "task1/T1_method_B",
        duration = 18
        )
    )




    mgr.add_task(Task(
        id = "task2.1a",
        name = "Task 2.1 method A",
        description = """
  Our DNS server has some issues, so we want to avoid outages due to
  unresolvable hostnames. Therefore, we have to update/add some entries in
  the hosts file.

  Update/Add the hosts, as specified in the 'buildserver' class.

  Also, make sure only valid IP addresses are written to the hosts file.

  IMPORTANT: for technical reasons we have to modify the file '/etc/hosts_bs'
  instead of the real hosts file.

  For this task use the Puppet resource type 'host' only.

  If you are unfamiliar with the `host` resource type, read Chapter "host
  Resource Type" in the Puppet guide before you start your task.
""",
        cnt_image = "puppet-experiment-task2.1:xenial",
        method = "T2.1_method_A",
        src_dir = "task2.1/T2.1_method_A",
        duration = 14
        )
    )
#    mgr.add_task(Task(
#        id = "task2.1b",
#        name = "Task 2.1 method B",
#        description = """
#  Our DNS server has some issues, so we want to avoid outages due to
#  unresolvable hostnames. Therefore, we have to update/add some entries in
#  the hosts file.
#
#  Update/Add the hosts, as specified in the 'buildserver' class.
#
#  Also, make sure only valid IP addresses are written to the hosts file.
#
#  IMPORTANT: for technical reasons we have to modify the file '/etc/hosts_bs'
#  instead of the real hosts file.
#
#  For this task use the Puppet resource type 'file_line' only.
#
#  If you are unfamiliar with the `file_line` resource type, read the Chapter
#  "file_line Resource Type" in the Puppet guide before you start your task.
#""",
#        cnt_image = "puppet-experiment-task2.1:xenial",
#        method = "T2.1_method_B",
#        src_dir = "task2.1/T2.1_method_B",
#        duration = 14
#        )
#    )
    mgr.add_task(Task(
        id = "task2.1c",
        name = "Task 2.1 method C",
        description = """
  Our DNS server has some issues, so we want to avoid outages due to
  unresolvable hostnames. Therefore, we have to update/add some entries in
  the hosts file.

  Update/Add the hosts, as specified in the 'buildserver' class.

  Also, make sure only valid IP addresses are written to the hosts file.

  IMPORTANT: for technical reasons we have to modify the file '/etc/hosts_bs'
  instead of the real hosts file.

  For this task use the Puppet resource type 'augeas' only.

  If you are unfamiliar with the concepts of Augeas, please read Chapter "augeas
  Resource Type" in the Puppet guide before you start your task.
""",
        cnt_image = "puppet-experiment-task2.1:xenial",
        method = "T2.1_method_C",
        src_dir = "task2.1/T2.1_method_C",
        duration = 40
        )
    )
    mgr.add_task(Task(
        id = "task2.1d",
        name = "Task 2.1 method D",
        description = """
  Our DNS server has some issues, so we want to avoid outages due to
  unresolvable hostnames. Therefore, we have to update/add some entries in
  the hosts file.

  Update/Add the hosts, as specified in the 'buildserver' class.

  Also, make sure only valid IP addresses are written to the hosts file.

  IMPORTANT: for technical reasons we have to modify the file '/etc/hosts_bs'
  instead of the real hosts file.

  For this task use the Puppet resource types 'kdbmount' and 'kdbkey' only.

  If you are unfamiliar with the concepts of Libelektra, read the Chapter
  "Libelektra: Kdbmount and Kdbkey" in the Puppet guide before you start the task.
""",
        cnt_image = "puppet-experiment-task2.1:xenial",
        method = "T2.1_method_D",
        src_dir = "task2.1/T2.1_method_D",
        duration = 30
        )
    )




    mgr.add_task(Task(
        id = "task2.2a",
        name = "Task 2.2 method A",
        description = """
  Some of our team members use a Windows notebook for their daily work. To make
  sharing files easier, we want to add a Samba server. However, we do not want
  to replace the whole smb.conf file as Ubuntu has reasonable default settings.
  Therefore, we just want to manipulate those settings, which we have to.

  For this task use the Puppet resource type 'ini_setting' to modify the
  smb.conf file as described in 'modules/samba/manifests/config.pp'.

  If you are unfamiliar with the `ini_setting` resource type, read the Chapter
  "ini_setting Resource Type" in the Puppet guide before you start your task.
""",
        cnt_image = "puppet-experiment-task2.2:xenial",
        method = "T2.2_method_A",
        src_dir = "task2.2/T2.2_method_A",
        duration = 12
        )
    )
#    mgr.add_task(Task(
#        id = "task2.2b",
#        name = "Task 2.2 method B",
#        description = """
#  Will be removed, this task isn't doable with the 'file_line' resource type
#""",
#        cnt_image = "puppet-experiment-task2.2:xenial",
#        method = "T2.2_method_B",
#        src_dir = "task2.2/T2.2_method_B"
#        )
#    )
    mgr.add_task(Task(
        id = "task2.2c",
        name = "Task 2.2 method C",
        description = """
  Some of our team members use a Windows notebook for their daily work. To make
  sharing files easier, we want to add a Samba server. However, we do not want
  to replace the whole smb.conf file as Ubuntu has reasonable default settings.
  Therefore, we just want to manipulate those settings, which we have to.

  For this task use the Puppet resource type 'augeas' to modify the
  smb.conf file as described in 'modules/samba/manifests/config.pp'.

  If you are unfamiliar with the concepts of Augeas, please read Chapter "augeas
  Resource Type" in the Puppet guide before you start your task.
""",
        cnt_image = "puppet-experiment-task2.2:xenial",
        method = "T2.2_method_C",
        src_dir = "task2.2/T2.2_method_C",
        duration = 30
        )
    )
    mgr.add_task(Task(
        id = "task2.2d",
        name = "Task 2.2 method D",
        description = """
  Some of our team members use a Windows notebook for their daily work. To make
  sharing files easier, we want to add a Samba server. However, we do not want
  to replace the whole smb.conf file as Ubuntu has reasonable default settings.
  Therefore, we just want to manipulate those settings, which we have to.

  For this task use the Puppet resource types 'kdbmount' and 'kdbkey' to modify
  the smb.conf file as described in 'modules/samba/manifests/config.pp'.

  If you are unfamiliar with the concepts of Libelektra, read the Chapter
  "Libelektra: Kdbmount and Kdbkey" in the Puppet guide before you start the task.
""",
        cnt_image = "puppet-experiment-task2.2:xenial",
        method = "T2.2_method_D",
        src_dir = "task2.2/T2.2_method_D",
        duration = 12
        )
    )

#    mgr.add_task(Task(
#        id = "task3.1a",
#        name = "Task 3.1 method A",
#        description = """
#  A team member created a puppet module for the (fake) rubyhttp webserver.
#  While he did a really greate job, he didn't test it very well before
#  pushing, so the 'rubyhttp' module creates an invalid configuration file.
#
#  The config file '/etc/rubyhttp/rubyhttp.json' is generated by several ERB 
#  templates. Maybe in one of them is the mistake?
#
#  Use 'run_puppet' to see what is going wrong and fix the problem.
#
#  If you are unfamiliar with the resource type `file` or how to write a ERB
#  template, read Chapter "File Resource Type" and Chapter "ERB Templates" in
#  the Puppet guide before you start the task.
#""",
#        cnt_image = "puppet-experiment-task3.1:xenial",
#        method = "T3.1_method_A",
#        src_dir = "task3.1/T3.1_method_A",
#        duration = 8
#        )
#    )
#    mgr.add_task(Task(
#        id = "task3.1b",
#        name = "Task 3.1 method B",
#        description = """
#  A team member created a puppet module for the (fake) rubyhttp webserver.
#  While he did a really greate job, he didn't test it very well before
#  pushing, so the 'rubyhttp' module creates an invalid configuration file.
#
#  The config file /etc/rubyhttp/rubyhttp.json is generated with Elektra
#  and its 'kdbkey' resource types. The according definitions are all
#  located in the source file 'modules/rubyhttp/manifests/config.pp'
#
#  Use 'run_puppet' to see what is going wrong and fix the problem.
#
#  If you are unfamiliar with the concepts of Libelektra, read the Chapter
#  "Libelektra: Kdbmount and Kdbkey" in the Puppet guide before you start the task.
#""",
#        cnt_image = "puppet-experiment-task3.1:xenial",
#        method = "T3.1_method_B",
#        src_dir = "task3.1/T3.1_method_B",
#        duration = 8
#        )
#    )

    mgr.add_task(Task(
        id = "task3.2a",
        name = "Task 3 method A",
        description = """
  A team member created a puppet module for the (fake) rubyhttp webserver, which
  is doing a good job for a while now.
  However, a newer version of 'rubyhttp' was released with a new 'cache' feature.
  Therefore, we have to extend our 'rubyhttp' Puppet module, which allows us making
  use of this new feature.

  Extend the 'rubyhttp' Puppet module by two new parameters:
   - '$cache': 
        Default value 'file', allowed values 'file' or 'memcached'
        Setting in '/etc/rubyhttp/rubyhttp.json': 'general/cache'

   - '$memcached_connection': 
        Default value undef (we do not have value restrictions for this parameter)
        Setting in '/etc/rubyhttp/rubyhttp.json': 'general/memcached_connection'
        (this should be ONLY INCLUDED if "$cache == 'memcached'" !!!

  The two new parameter are already used in 'manifests/site.pp'.

  If you are unfamiliar with the resource type `file` or how to write an ERB
  template, read Chapter "File Resource Type" and Chapter "ERB Templates" in
  the Puppet guide before you start the task.
""",
        cnt_image = "puppet-experiment-task3.2:xenial",
        method = "T3.2_method_A",
        src_dir = "task3.2/T3.2_method_A",
        duration = 12
        )
    )
    mgr.add_task(Task(
        id = "task3.2b",
        name = "Task 3 method B",
        description = """
  A team member created a puppet module for the (fake) rubyhttp webserver, which
  is doing a good job for a while now.
  However, a newer version of 'rubyhttp' was released with a new 'cache' feature.
  Therefore, we have to extend our 'rubyhttp' Puppet module, which allows us making
  use of this new feature.

  Extend the 'rubyhttp' Puppet module by two new parameters:
   - '$cache': 
        Default value 'file', allowed values 'file' or 'memcached'
        Setting in '/etc/rubyhttp/rubyhttp.json': 'general/cache'

   - '$memcached_connection': 
        Default value undef (we do not have value restrictions for this parameter)
        Setting in '/etc/rubyhttp/rubyhttp.json': 'general/memcached_connection'
        (this should be ONLY INCLUDED if "$cache == 'memcached'" !!!

  The two new parameter are already used in 'manifests/site.pp'.

  If you are unfamiliar with the concepts of Libelektra, read the Chapter
  "Libelektra: Kdbmount and Kdbkey" in the Puppet guide before you start the task.
""",
        cnt_image = "puppet-experiment-task3.2:xenial",
        method = "T3.2_method_B",
        src_dir = "task3.2/T3.2_method_B",
        duration = 12
        )
    )

    #
    # add question tasks
    #
    mgr.add_task(QuestionTask("q0", "task 0 questions", "task0"))
    mgr.add_task(QuestionTask("q1", "task 1 questions", "task1"))
    mgr.add_task(QuestionTask("q2.1", "task 2.1 questions", "task2.1"))
    mgr.add_task(QuestionTask("q2.2", "task 2.2 questions", "task2.2"))
#    mgr.add_task(QuestionTask("q3.1", "task 3.1 questions", "task3.1"))
    mgr.add_task(QuestionTask("q3.2", "task 3.2 questions", "task3.2"))


    #mgr.add_group("faulty", ['task2.2b'])

    mgr.add_group("g1", [
        'q0',
        'task1a', 'q1', 'task1b', 'q1',
        'task2.1a', 'q2.1', 'task2.1c', 'q2.1', 'task2.1d', 'q2.1',
        'task2.2a', 'q2.2', 'task2.2c', 'q2.2', 'task2.2d', 'q2.2',
#        'task3.1a', 'q3.1', 'task3.1b', 'q3.1',
        'task3.2a', 'q3.2', 'task3.2b', 'q3.2'
        ])

    mgr.add_group("g2", [
        'q0',
        'task1b', 'q1', 'task1a', 'q1',
        'task2.1d', 'q2.1', 'task2.1a', 'q2.1', 'task2.1c', 'q2.1',
        'task2.2d', 'q2.2', 'task2.2a', 'q2.2', 'task2.2c', 'q2.2',
#        'task3.1b', 'q3.1', 'task3.1a', 'q3.1',
        'task3.2b', 'q3.2', 'task3.2a', 'q3.2'
        ])
    mgr.add_group("g3", [
        'q0',
        'task1a', 'q1', 'task1b', 'q1',
        'task2.1c', 'q2.1', 'task2.1a', 'q2.1', 'task2.1d', 'q2.1',
        'task2.2c', 'q2.2', 'task2.2a', 'q2.2', 'task2.2d', 'q2.2',
#        'task3.1a', 'q3.1', 'task3.1b', 'q3.1',
        'task3.2a', 'q3.2', 'task3.2b', 'q3.2'
        ])
    mgr.add_group("g4", [
        'q0',
        'task1b', 'q1', 'task1a', 'q1',
        'task2.1d', 'q2.1', 'task2.1c', 'q2.1', 'task2.1a', 'q2.1',
        'task2.2d', 'q2.2', 'task2.2c', 'q2.2', 'task2.2a', 'q2.2',
#        'task3.1b', 'q3.1', 'task3.1a', 'q3.1',
        'task3.2b', 'q3.2', 'task3.2a', 'q3.2'
        ])


    mgr.start()
