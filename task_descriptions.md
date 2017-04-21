# Configuration File Handling with Puppet: a Software Experiment

The goal of this user study or software experiment is to outline differences
between Puppet strategy for manipulating
configuration files. Therefore, this study compares six different methods for
writing or modifying configuration files, from very general to very specific
methods.

This study consists of four tasks, whereas all tasks will be solved several
times, each with a different Puppet method. The four tasks can be classified in
3 main groups:
* writing a complete configuration from scratch
* partial configuration file manipulations
* maintenance tasks: adding features

To solve these tasks some Puppet knowledge is required. You should already have
received the guide "*A short Puppet Introduction*", if not it is available
online under
https://github.com/BernhardDenner/puppet-userstudy-controller/blob/master/puppet_introduction.md
This guide gives you enough Puppet know-how required to solve the tasks of this
user study. Additionally, this guide can be used as a reference during your
work.


### Experiment Procedure

The experiment controller (`expctr.py`, should be already running) will perform
all steps to set up the environment needed to solve the tasks. It will also guide
you through the experiment.

Before starting the experiment, read the following points carefully:

* Start the experiment with the command `new_experiment <group> <name>`. Please
  use your assigned group.
* Once the text editor appears, type the command `start` in the terminal window
  to begin with the first task. If you
  accidentally return to the experiment controller prompt
  (`Exp sh (group) name :>`) use `start` again to return to your last task.
* Your working environment consists of a **terminal window** and a **text editor**.
  We highly recommend placing the two windows next to each other.
* For each task a fresh container is started, which contains all required
  programs. So you can't do any harm on this machine.
* The terminal window can be used to test your code and to pass on to the next
  task. While you are working on a task, the following commands are available
  within the task's container:
  * `run_test` will run the Puppet agent and perform test cases on the resulting
    configuration files. Some test cases restore the original state of the
    manipulated configuration files. If you feel you really have messed up the
    configuration file in question, use `run_test` to get a clean starting point.
  * `run_puppet` just executes the Puppet agent
  * `exit`: this will end the current task's shell and therefore ends the
    current task. All test cases will run once again before the task container is
    closed.
  * `pause`: if you are interrupted (e.g. phone call), use this command to mark
    this time periode as "I'm not working now".
  * Your shell a normal `bash` shell. So you can use the usual commands to
    gather some information (e.g. `cat`, `less`, `vim`...)
* All tasks are started automatically. Read carefully the description below and
  online. Each task has to be solved with a specific method. The order of the
  used Puppet methods depends on your group. This shall help to increase the
  measurement quality.
* The relevant source folder for the current task will be added automatically 
  to the text editor. So you may close all source files or project folder  from
  an old task before continuing. If you accidentally close the editor window,
  wait a few seconds, it will restart automatically.
* All your actions will be recorded in a log file. All changes to the source
  files are traced automatically. This helps us to
  reconstruct your way to your solution.
* Most importantly the time you require to solve the task will be measured. This
  will be one of the key indicators during the experiment. So please do not make
  a break during a task. Try to schedule it between two tasks if required. If
  you really require a break or you are interrupted use the `pause` command to
  mark this period as "I'm not working now".
* The experiment controller will show your progress before each task
  (done/remaining). The shown estimated times are based on already conducted
  experiments (all participants without prior Puppet experience).
* You have finished a task, if all test cases for this task completed successfully.
  Read carefully. Some test cases check if the Puppet run fails. This means the 
  Puppet agent shows an error message although the test case was successful.
* If you have finished all tasks, use the command `finished` to export all your
  sources and logs.


## Task 1: Define a new Configuration File

Our development team has released the fresh new application called 'calculator'.
Our task is to write a Puppet module for this application to allow an automatic
deployment and configuration on our server farm. 'calculator' uses a
JSON style configuration file.

The Puppet module is almost complete. Your task is to define the missing
configuration part(s). Therefore, you  have to define the required Puppet code
to write the requested configuration settings to the specified file.

**calculator** expects these settings:
* object `general` of type object with the following properties
  * `instance` and with value of `$calculator::instance`
  * `worker_threads` and with value of `$calculator::worker_threads`
* object `logging` of type object with the following properties
  * `log_level` and with value of `$calculator::log_level`
  * `log_file` and with value of `$calculator::log_file`

This task has to be solved in 2 different variants (order depends on your group
setting):

- **Method A: resource type `file` + ERB template**

  Write the configuration part for the Puppet module 'calculator' using the 
  resource type 'file' together with and an ERB template:
   - modules/calculator/manifests/config.pp
   - modules/calculator/templates/config.json.erb

  If you are unfamiliar with the resource type `file` or how to write a ERB
  template, read Chapter "File Resource Type" and Chapter "ERB Templates" in
  the Puppet guide before you start the task.

  JSON syntax

  ```json
  {
    "object1": {
      "prop1": "value",
      "prop2": "value2"
    },
    "obj2": {
      "prop3": "value"
    }
  }
  ```


- **Method B: Libelektra**

  Write the configuration part for the Puppet module 'calculator' using the
  resource types 'kdbmount' and 'kdbkey' only:
   - modules/calculator/manifests/config.pp

  If you are unfamiliar with the concepts of Libelektra, read the Chapter 
  "Libelektra: Kdbmount and Kdbkey" in the Puppet guide before you start the task.


## Task 2.1: Hosts File Manipulations

Our DNS server has some issues, so we want to avoid outages due to
unresolvable hostnames. Therefore, we have to update/add some entries in
the hosts file.

Update/Add the following hosts, as specified in the `buildserver` class (via
class parameter/variables):
* update existing entries
  * hostname: `$master_hostname`, IP: `$master_ip`, alias: `master`
  * hostname: `$build1_hostname`, IP: `$build1_ip`, alias: `build1`
* add new entries
  * hostname: `$build2_hostname`, IP: `$build2_ip`, alias: `build2`
  * hostname: `$build3_hostname`, IP: `$build3_ip`, alias: `build3`

Also, make sure only **valid** IP addresses are written to the hosts file, as
someone could pass an invalid IP to our `buildserver` class.

**IMPORTANT**: for technical reasons we have to modify the file `/etc/hosts_bs`
instead of the real hosts file.

Syntax of a hosts file:
```sh
# comment
# <IP-address>     <hostname> [<host alias> ...]
192.168.1.1      gatekeeper gateway proxy
```

You can also take a look at the existing file: `cat /etc/hosts_bs`.

This task has to be solved in 3 different variants:

- **Method A: resource type `host`**

  For this task use the Puppet resource type 'host' only.

  If you are unfamiliar with the `host` resource type, read Chapter "host
  Resource Type" in the Puppet guide before you start your task.


- **Method C: resource type `augeas`**

  For this task use the Puppet resource type 'augeas' only.

  If you are unfamiliar with the concepts of Augeas, please read Chapter "augeas
  Resource Type" in the Puppet guide before you start your task.

  The Augeas hosts lens creates keys in the following format:
  ```
   /files/<file>/1/ipaddr = <IP address>     <--- first entry
   /files/<file>/1/canonical = <hostname>
   /files/<file>/1/alias = <host alias>
   /files/<file>/2/ipaddr = <IP address>     <--- second entry
   ...
  ```


- **Method D: Libelektra**

  For this task use the Puppet resource types 'kdbmount' and 'kdbkey' only.

  If you are unfamiliar with the concepts of Libelektra, read the Chapter 
  "Libelektra: Kdbmount and Kdbkey" in the Puppet guide before you start the task.

  The 'hosts' plugin uses the following keys to manage hosts entries:
  ```
   .../ipv4/<hostname> = <ipaddress>
   .../ipv4/<hostname>/<alias1> = <ipaddress>
   .../ipv4/<hostname>/<alias2> = <ipaddress>
   ...
  ```



## Task 2.2, Samba Configuration

Some of our team members use a Windows notebook for their daily work. To make
sharing files easier, we want to add a Samba server. However, we do not want
to replace the whole smb.conf file as Ubuntu has reasonable default settings.
Therefore, we just want to manipulate those settings, which we have to.

Modify the INI style config file /etc/samba/smb.conf in the following way:
* modify setting `workgroup` in section `global`: value of `$samba::workgroup`
* remove setting `syslog` in section `global`
* add setting `logging` in section `global` with fixed value `syslog@1 file`
* add a new section named by the value of `$samba::project_share_name` with
  the following settings:
  * `path` with value of `$samba::project_share_path`
  * `comment` with value of `$samba::project_share_comment`
  * `guest ok` with value `no`
* add a new section named by the value of `$samba::transfer_share_name` with
  the following settings:
  * `path` with value of `$samba::transfer_share_path`
  * `comment` with value of `$samba::transfer_share_comment`
  * `guest ok` with value `yes`

This task has to be solved in 3 different variants:

- **Method A, resource type `ini_setting`**

  For this task use the Puppet resource type `ini_setting` to modify the
  `smb.conf` file as described above.

  If you are unfamiliar with the `ini_setting` resource type, read the Chapter
  "ini_setting Resource Type" in the Puppet guide before you start your task.


- **Method C, resource type `augeas`**

  For this task use the Puppet resource type 'augeas' to modify the
  smb.conf file as described above.

  If you are unfamiliar with the concepts of Augeas, please read Chapter "augeas
  Resource Type" in the Puppet guide before you start your task.

  Augeas transformes smb.conf to the following tree:

  ```
   /files/etc/samba/smb.conf/target[1] = global
   /files/etc/samba/smb.conf/target[1]/workgroup = WORKGROUP
  ```

- **Method D, Libelektra**

  For this task use the Puppet resource types 'kdbmount' and 'kdbkey' to modify
  the smb.conf file as described above.

  If you are unfamiliar with the concepts of Libelektra, read the Chapter
  "Libelektra: Kdbmount and Kdbkey" in the Puppet guide before you start the task.


## Task 3, Rubyhttp Webserver Cache Config

A team member created a puppet module for the (fake) rubyhttp webserver, which
is doing a good job for a while now.
However, a newer version of 'rubyhttp' was released with a new 'cache' feature.
Therefore, we have to extend our 'rubyhttp' Puppet module, which allows us making
use of this new feature.

Extend the 'rubyhttp' Puppet module by two new parameters:
 - `$cache`: 
      Default value `file`, allowed values `file` or `memcached`.

      Setting in `/etc/rubyhttp/rubyhttp.json`: `general/cache`

 - `$memcached_connection`: 
      Default value undef (we do not have value restrictions for this parameter)

      Setting in `/etc/rubyhttp/rubyhttp.json`: `general/memcached_connection`

      This setting should be **ONLY INCLUDED** if `$cache == 'memcached'`,
      otherwise, this setting should not be in the config file.

The two new parameter are already used in `manifests/site.pp`.

This task has to be solved in 2 different variants:

- **Method A, `file` + ERB templates**

  Extend the following files using those methods found in there: `init.pp`,
  `config.pp` and `templates/config/general.erb`

  If you are unfamiliar with the resource type `file` or how to write an ERB
  template, read Chapter "File Resource Type" and Chapter "ERB Templates" in
  the Puppet guide before you start the task.

- **Method B, Libelektra**

  Extend the following files using those methods found in there: `init.pp` and
  `config.pp`.

  If you are unfamiliar with the concepts of Libelektra, read the Chapter
  "Libelektra: Kdbmount and Kdbkey" in the Puppet guide before you start the task.
