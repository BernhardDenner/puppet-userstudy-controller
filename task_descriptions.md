# Configuration File Handling with Puppet: a Software Experiment

The goal of this user study or software experiment is to outline differences
between Puppet strategy for manipulating
configuration files. Therefore, this study compares six different methods for
writing or modifying configuration files, from very general to very specific
methods.

This study consists of five tasks, whereas all tasks will be solved several
times, each with a different Puppet method. The five tasks can be classified in
3 main groups:
* writing a complete configuration from scratch
* partial configuration file manipulations
* maintenance tasks: bug fixing, adding features

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

Our development team has released the fresh new 'app' with two components:
'broker' and 'calculator'. Our task is to write two Puppet modules for these
two components. However, the Dev team didn't agree on a common config format,
so 'broker' uses a INI style format and 'calculator' a JSON config format.

The two modules are already written, you have to define the required Puppet code
to write the requested configuration settings to the specified files.

**broker** expects the following configuration settings:
* section `general` with settings
  * `instance_name` and with value of `$broker::instance_name`
  * `timeout` and with value of `$broker::timeout`
* section `notification` with settings
  * `method` and with value of `$broker::notification_method`
  * `email` and with value of `$broker::email`

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

  Write the configuration part for the two Puppet modules using the 
  resource type 'file' together with and an ERB template:
   - modules/broker/manifests/config.pp
   - modules/broker/templates/config.ini.erb
   - modules/calculator/manifests/config.pp
   - modules/calculator/templates/config.json.erb

  If you are unfamiliar with the resource type `file` or how to write a ERB
  template, read Chapter "File Resource Type" and Chapter "ERB Templates" in
  the Puppet guide before you start the task.

  INI syntax

  ```INI
  [section1]
  setting1 = value1

  [section2]
  setting2 = value2
  ```

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

  Write the configuration part for the two Puppet modules using the
  resource types 'kdbmount' and 'kdbkey' only:
   - modules/broker/manifests/config.pp
   - modules/calculator/manifests/config.pp

  If you are unfamiliar with the concepts of Libelektra, read the Chapter 
  "Libelektra: Kdbmount and Kdbkey" in the Puppet guide before you start the task.


## Task 2.1: Hosts File Manipulations

Our DNS server has some issues, so we want to avoid outages due to
unresolvable hostnames. Therefore we have to update/add some entries in
the hosts file.

Update/Add the following hosts, as specified in the `buildserver` class (via
class parameter/variables):
* update existing entries
  * hostname: `$master_hostname`, IP: `$master_ip`, alias: `master`
  * hostname: `$build1_hostname`, IP: `$build1_ip`, alias: `build1`
* add new entries
  * hostname: `$build2_hostname`, IP: `$build2_ip`, alias: `build2`
  * hostname: `$build3_hostname`, IP: `$build3_ip`, alias: `build3`

Also make sure only **valid** IP addresses are written to the hosts file, as
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

This task has to be solved in 4 different variants:

- **Method A: resource type `host`**

  For this task use the Puppet resource type 'host' only.

  If you are unfamiliar with the `host` resource type, read Chapter "host
  Resource Type" in the Puppet guide before you start your task.

  Hints:
   - The 'host' resource type uses '/etc/hosts' as default file, however we
     have to modify '/etc/hosts_bs'.


- **Method B: resource type `file_line`**

  For this task use the Puppet resource type 'file_line' only.

  If you are unfamiliar with the `file_line` resource type, read the Chapter
  "file_line Resource Type" in the Puppet guide before you start your task.

  Hints:
   - The function `validate_ip_address()` fails if the given argument
     is not an IP address.


- **Method C: resource type `augeas`**

  For this task use the Puppet resource type 'augeas' only.

  If you are unfamiliar with the concepts of Augeas please read Chapter "augeas
  Resource Type" in the Puppet guide before you start your task.

  Hints:
   - The Augeas hosts lens creates keys in the following format:
     ```
      /files/<file>/1/ipaddr = <IP address>     <--- first entry
      /files/<file>/1/canonical = <hostname>
      /files/<file>/1/alias = <host alias>
      /files/<file>/2/ipaddr = <IP address>     <--- second entry
      ...
     ```
   - You may use the path query `/files/<file>/*[canonical = '$hostname']/...`
     to match an existing entry
   - New hosts entries have to be created first. You can use the "dummy" path
     `/files/<file>/0/...` to add a new entry. Ensure you create the new
     entry with its child nodes in the following order: 'ipaddr', 'canonical',
     'alias'. Otherwise, the Augeas resource type might issue an error.
     Keep in mind: new entries will be added on each Puppet
     run. Therefore guard them by a appropriate "onlyif => match ..."
     parameter.
   - The function `validate_ip_address()` fails if the given argument
     is not an IP address.


- **Method D: Libelektra**

  For this task use the Puppet resource types 'kdbmount' and 'kdbkey' only.

  If you are unfamiliar with the concepts of Libelektra, read the Chapter 
  "Libelektra: Kdbmount and Kdbkey" in the Puppet guide before you start the task.

  Hints:
   - The Elektra 'hosts' plugin can read and write hosts files.
   - The 'hosts' plugin uses the following keys to manage hosts entries:
     ```
      .../ipv4/<hostname> = <ipaddress>
      .../ipv4/<hostname>/<alias1> = <ipaddress>
      .../ipv4/<hostname>/<alias2> = <ipaddress>
      ...
     ```
   - The 'network' plugin can be used to validate IP addresses.



## Task 2.2, Samba Configuration

Some of our team members use a Windows notebook for their daily work. To make
sharing files easier, we want to add a Samba server. However, we do not want
to replace the whole smb.conf file as Ubuntu has reasonable default settings.
Therefore we just want to manipulate those settings, which we have to.

The following modification have to be done:
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

  Hints:
   - You have to specify both, setting and section. The resource title (id)
     can be chosen arbitrarily.


- **Method C, resource type `augeas`**

  For this task use the Puppet resource type 'augeas' to modify the
  smb.conf file as described above.

  If you are unfamiliar with the concepts of Augeas please read Chapter "augeas
  Resource Type" in the Puppet guide before you start your task.

  Hints:
   - The samba config file is already included by Augeas, so you do not need
     a custom lens or custom file path. You can use
     `/files/etc/samba/smb.conf` directly.
   - The file is transformed to the following tree:
     ```
      /files/etc/samba/smb.conf/target[1] = global
      /files/etc/samba/smb.conf/target[1]/workgroup = WORKGROUP
     ```
   - You may use `.../target[. = 'global']/...` to modify settings below the
     'global' section
   - You have to create the share definition sections before manipulating
     settings below them. Make sure not to create them again if the section
     already exists. You may use the "dummy" index 0 for this e.g: 
     e.g. `set .../target[0] value`
     However, you can't create a new section and assign settings below them
     within the same augeas task. You have to use
     two different tasks for this. Use the relationship operator to ensure the
     section is created before settings are added:
     e.g. `Augeas["task1"] -> Augeas["task2"]`


- **Method D, Libelektra**

  For this task use the Puppet resource types 'kdbmount' and 'kdbkey' to modify
  the smb.conf file as described above.

  If you are unfamiliar with the concepts of Libelektra, read the Chapter
  "Libelektra: Kdbmount and Kdbkey" in the Puppet guide before you start the task.

  Hint:
   - Samba uses an INI configuration file format
   - You do not have to create section keys, Elektra will add them
     automatically.


## Task 3.1, Rubyhttp Webserver Config Bug

A team member created a puppet module for the (fake) rubyhttp webserver.
While he did a really greate job, he didn't test it very well before
pushing, so the 'rubyhttp' module creates an invalid configuration file.


This task has to be solved in 2 different variants:

- **Method A, `file` + ERB template**

  The config file `/etc/rubyhttp/rubyhttp.json` is generated by several ERB 
  templates. Maybe in one of them is the mistake?

  Use `run_test` to see what is going wrong and fix the problem.

  Hint:
   - JSON does not allow to place a ',' after the last element
   - The resource types `concat` and file `concat::fragment` are used to build the
     content of a file with different fragments.

  If you are unfamiliar with the resource type `file` or how to write a ERB
  template, read Chapter "File Resource Type" and Chapter "ERB Templates" in
  the Puppet guide before you start the task.


- **Method B, Libelektra**

  The config file `/etc/rubyhttp/rubyhttp.json` is generated with Elektra
  and its `kdbkey` resource types. The according definitions are all
  located in the source file `modules/rubyhttp/manifests/config.pp`

  Use `run_test` to see what is going wrong and fix the problem.

  Hint:
   - If you find an invalid configuration setting, you might ensure the invalid
     setting will be removed, as it might have been added already by an previous
     Puppet run.
   - 'rubyhttp -h' gives some help about expected settings.

  If you are unfamiliar with the concepts of Libelektra, read the Chapter
  "Libelektra: Kdbmount and Kdbkey" in the Puppet guide before you start the task.


## Task 3.2, Rubyhttp Webserver Cache Config

The 'rubyhttp' module is working for a while now. However, a newer version 
of 'rubyhttp' was released with a new 'cache' feature. Therefore we have to
extend our 'rubyhttp' Puppet module, which allows us to make use of this new
feature.

Extend the 'rubyhttp' Puppet module by two new parameter:
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
