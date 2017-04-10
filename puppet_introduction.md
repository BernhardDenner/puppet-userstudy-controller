# A short Puppet Introduction

#### Table of Contents

1. [Introduction](#introduction)
1. [Resources - core of Puppet](#resources)
1. [Classes](#classes)
1. [Variables](#variables)
1. [Conditional Statements](#conditional-statements)
1. [Function](#functions)
1. [ERB Templates](#erb-templates)
   * [Tags](#tags)
   * [Accessing Variables in templates](#accessing-variables-in-templates)
   * [Template Examples](#template-examples)
1. [Working Example: Puppet in Action](#working-example-puppet-in-action)
1. [Useful Resource Types for Experiment
   Tasks](#useful-resource-types-for-experiment-tasks)
   * [`file` Resource Type and ERB
     Templates](#-file-resource-type-and-erb-templates)
   * [Libelektra: Kdbmount and Kdbkey](#libelektra-kdbmount-and-kdbkey)
     * [`kdbmount` Resource Type](#-kdbmount-resource-type)
     * [`kdbkey` Resource Type](#-kdbkey-resource-type)
   * [`file_line` Resource Type](#-file_line-resource-type)
   * [`ini_setting` Resource Type](#-ini_setting-resource-type)
   * [`augeas` Resource Type](#-augeas-resource-type)
   * [`host` Resource Type](#-host-resource-type)
1. [References](#references)

## Introduction

Puppet, is used to manage configuration of
Unix-like systems in a declarative manner. The user describes system resources
and their states, using Puppet's domain specific language. This declarative
description of a desired system state is then compared to the actual system
state. If the desired state differs from the actual state, Puppet will perform
actions to bring the managed system into the desired state.

The desired system state is defined as a set of resource declarations within one
ore more *Puppet manifests* (source files). Such Puppet manifests can then be
*applied* to a system.

## Resources

Resources are the fundamental unit of Puppet. Resource declarations tells
Puppet how the desired system state should look like. A resource can be a user,
file, cronjob, package..., roughly any identifiable property of a computer
system.

Within Puppet, each resource declaration consists of the following elements:
* **resource type**: basically which resource we want to manage. Is it a `file`,
  `user` or `package`.
* **title**: each resource within one resource type must have a **unique**
  title. So for files this will be the *absolute path name*, for packages
  it will be the *package name* and so on.

  Again, each defined resource type-title pair has to be globally unique. For
  example, there must not be two `file` definitions for the same absolute path
  name. Otherwise Puppet won't know, which one to use.
* **attributes**: each resource definition can have one or more attribute value
  pairs,
  which describe the concrete state of the resource. For example the attribute
  `owner` describes the owner of a file.

  Since different types of resources have different aspects to manage (e.g. a
  package does not have an owner), each resource type has different attributes
  it can handle. A complete list of built-in resource types with their
  attributes can be found at [Resource Type
  Reference](https://docs.puppet.com/puppet/latest/type.html).


Example resource declarations:

```puppet
# ensure the file /etc/resolv.conf exists with owner = 'root', group = 'root'
# and file permissions 0644
file { '/etc/resolv.conf':
  ensure => file,
  owner  => 'root',
  group  => 'root',
  mode   => '0644'
}

# Within one scope (see below) we can define resource defaults for a particular type:
# file modules/webserver/manifests/init.pp
class webserver {
  # default attributes for all file resource definitions within this class (scope)
  File {  # Note the capital 'F'
    owner => 'www',
    group => 'www',
  }

  file { '/var/www':
    ensure => directory
    # owner and group are added implicetly
  }

  file { '/etc/www/config.ini':
    ensure => file
  }

  # several resource definitions at once
  file {
    '/etc/www/domain1.conf': ensure => file ;  # Note the ';' here
    '/etc/www/domain2.conf':
      ensure => file,
      mode   => '0644';

    '/etc/www/secret-domain.conf':
      ensure => file,
      owner  => 'root',  # default is overrided here
      mode   => '0640';
  }
}
```


## Classes

Classes are named blocks of Puppet code and exist for grouping resource
definitions. They can't be compared to 'classes' from a object oriented point of
view. Puppet classes can't be instantiated, instead they are just *used* or
*included*.

Classes can have an arbitrary number of parameter.

```puppet
class webserver($sitedir, $ensure = 'present') {
  # resource declarations
  ...
}
```

## Variables

Beside its declarative resource definition, Puppet also has some aspects of
procedural programming languages to allow some flexibility.

Variables are **immutable**, so each of them can have a single assignment only.
Variables are always prefixed with a `$`. Within a double-quoted string, they
can also be referenced by `${variable}`.

```puppet
$configfile = '/etc/myapp/myapp.conf'
$content = 'This is just some text'

file { $configfile:
  ensure => file,
  # include variable in string (use double-quotes)
  content => "${content} from some one"
}

$content = "other text"  # this does not work
```

Variables are defined within a **scope** and are only available within the scope
in which they are defined.

Within a child scope, variables from the parent scope can be accessed using
their *qualified names*, i.e. adding its scope names delimited by `::` (e.g.
`$webserver::sitedir`).

```puppet
# modules/webserver/manifests/init.pp
class webserver($sitedir) {
  $defaults = 'some default value'
  ...
}

# modules/webserver/manifests/config.pp
class webserver::config {
  # access to $sitedir of class webserver
  $x = $webserver::sitedir
  $y = $webserver::defaults
  ...
}
```

## Conditional Statements

Conditional statements let Puppet code behave differently in different
situations.

* **if-statement**

  ```puppet
  if $variable == "some value" or $variable == "other value" {
    # $variable has concrete value
  }
  elsif $variable =~ /^rege[Xx] \d+/ and $variable !~ /^dan[gG]erous/ {
    # $variable matches first regular expression but not second one
  }
  elsif $variable != undef {
    # variable has a value (undef means 'no value')
  }
  else {
    # else case
  }
  ```
* **case-statement**: simpler form of if-elsif-else chains

  ```puppet
  case $variable {
    'some fixed value':  { # $variable == 'some fixed value' }
    'this', 'that':      { # $variable is 'this' or 'that' }
    /^(hello)|(world)$/: { # $variable matches regex ('hello' or 'world')}
    default:             { # default case if nothing matches }
  }
  ```
* **selectors**: allow conditioned variable assignments

  ```puppet
  $variable = $sitedir ? {
    'some fixed value' => 'fixed value',
    /^rege[Xx] \d+/    => 'regex match',
    default            => 'nothing matched',
  }
  ```


## Functions

Puppet allows to call pre-defined function (junks of Ruby code), which **returns
values**, **modify the catalog** or simply **fail**.

There are several built-in function and more are available through Puppet
modules, especially by the `puppetlabs-stdlib` module.

```puppet
# content of file is defined by parsing and evaluating the specified ERB template
file { '/etc/ntp.conf':
  ensure  => file,
  content => template('ntp/ntp.conf.erb')  # template() built-in function
}

# include the 'webserver' class
include webserver  # include build-in function

# stdlib function basename(): get basename of a path
if basename($path) == 'file.txt' {
  # build-in function: aborts compilation with given message
  fail("file.txt must not be touched")
}

# stdlib fuction: aborts compilation if $client is not a valid IP address
validate_ip_address($client)
```


## ERB Templates

Templates are boilerplates for large string values, typically used as
content of files. ERB templates are normal text files with embedded Ruby code.
This Ruby code is evaluated during the function call `template()` and the result
of this evaluation, together with normal text parts, are returned by the
`template()` function.

Typical use case:

file: `modules/apache2/templates/site.conf.erb`

```apache
<VirtualHost *:80>
  DocumentRoot <%= @docroot %>
</VirtualHost>
```

file: `modules/apache2/manifests/config.pp`

```puppet
class apache2::config {
  $docroot = '/var/www/html'
  file { '/etc/apache2/sites-available/default.conf':
    ensure  => file,
    content => template('apache2/site.conf.erb')  # takes the path to the template
  }
}
```

Results in `/etc/apache2/sites-available/default.conf`

```
<VirtualHost *:80>
  DocumentRoot /var/www/html
</VirtualHost>
```

Important to note is the parameter of the function `template()`. This function
expects the path to the template in the following form:
`<module-name>/<path-under-templates-dir>`. Examples:

```sh
.../modules/ssh/templates/sshd.conf.erb         # template file
template('ssh/sshd.conf.erb')                   # path without 'templates' dir

.../modules/ntp/templates/server/ntp.conf.erb   # template file
template('ntp/server/ntp.conf.erb')
```
### Tags

Everything enclosed in `<% %>` is interpreted as Ruby code and will be
evaluated. The following forms can be used:

* `<% CODE %>`: simple evaluation
* `<%= EXPRESSION %>`: evaluation, whereas result of expression will be added to result
  of template
* `<%- CODE -%>`: simple evaluation, whereas leading and trailing white space
  (including followed newline) will not be part of the template result. Closing
  bracket can be combined with other forms.

### Accessing Variables in Templates

Variables in the **current scope** are available in the ERB template as Ruby
instance variables. i.e. `$` replaced by `@`: `$variable` => `@variable`.

**Out-of-scope** variables are accessible through the `scope` Hash object:
`$apache::docroot` => `scope['apache::docroot']`

```ruby
# template is called within scope apache::config
<%= @docroot %>                    # access to $apache::config::docroot
<%= scope['apache::defaults'] %>   # access to $apache::defaults
```

### Template Examples

```ruby
# simple evaluation
<% if @docroot == 'some value' %>
goes into the template if condition is true
<% end %>

# evaluation and result of expression is added to the result
Hello <%= "world" %>. Docroot = <%= @docroot -%>

# evaluation, leading and trailing whitespce (also newline) will not be part of result
  <%- if @docroot == '/var/www/html' -%>
  <%# default docroot (comment line) -%>
  Access <%= scope['apache::default_access'] %>
  <%- end -%>

# more complex example with condition and loop iteration
<%- if @aliases.is_a? Hash -%>
  <Aliases>
  <%- @aliases.each do |key, value| -%>
    <%= key %> = "<%= value %>"
  <%- end -%>
  </Aliases>
<%- end -%>
```


## Working Example: Puppet in Action

The following code listing is fully working example. It ensures the configfile
`/etc/exampleapp.ini` exists with a defined content. This listing shows four
different files:
```puppet
# file: /etc/puppet/modules/exampleapp/manifests/init.pp
class exampleapp($queue, $logfile) {
  # ensure this class is used with values for both parameter
  if $queue == undef or $logfile == undef {
    fail("you have to specify values for both parameter")
  }
  include exampleapp::config
}

# file: /etc/puppet/modules/exampleapp/manifests/config.pp
class exampleapp::config {
  $configfile = '/etc/exampleapp.ini'

  # add variables used in template to this scope: this reduces coupling
  $queue = $exampleapp::queue
  $logfile = $exampleapp::logfile
  file { $configfile:
    ensure  => file,
    content => template('exampleapp/config.ini.erb')
  }
}

# file: /etc/puppet/modules/exampleapp/templates/config.ini.erb
[section 1]
queue = <%= @queue %>
[section 2]
logfile = <%= @logfile %>

# file: /etc/puppet/manifests/site.pp
node "mycomputer" {
  # apply the exampleapp class to the default host "mycomputer"
  class { "exampleapp":
    queue    => 'hello',
    logfile => '/var/log/exampleapp.log'
  }
}
```

So now if we run puppet we'll get:
```
root $> puppet apply /etc/puppet/manifests/site.pp
Info: Loading facts
Notice: Compiled catalog for t2_1_method_a.netbb in environment production in
0.22 seconds
Info: Applying configuration version '1490950501'
Notice: /Stage[main]/Exampleapp::Config/File[/etc/exampleapp.ini]/ensure:
defined content as '{md5}d3d2fb08e40c226c9027b1f02667eac4'
Notice: Finished catalog run in 0.03 seconds
root $> cat /etc/exampleapp.ini
[section 1]
queue = hello
[section 2]
logfile = /var/log/exampleapp.log
```

## Useful Resource Types for Experiment Tasks

The resource types described in this chapter are required to solve the
experiment tasks.

### `file` Resource Type and ERB Templates

The `file` resource type was already used in the above examples, so you should
be familiar with if already. An ERB template introduction and examples can be
found in chapter [ERB Templates](#erb-templates).

Most important attributes:

 * `path`: absolute path to the file, if not given the resource title is used
 * `ensure`: whether is should exist and if so which kind of file it should be.
   * `file`: file should exist
   * `directory`: make sure it is a directory
   * `present`: file or directory exists, if missing a regular file is created
   * `absent`: make sure file of directory does NOT exist
 * `content`: content of the file
 * `owner`: owner of the file, user name or uid
 * `group`: group of the file, user name or gid
 * `mode`: file system permissions, such as '0644'

The full documentation can be found at [Resource Type
Reference#File](https://docs.puppet.com/puppet/3.8/type.html#file).

### Libelektra: Kdbmount and Kdbkey

Resource types to handle configuration files using *libelektra*.

Elektra is a general purpose, key value based configuration framework. It
operates on a global, hierarchically organized shared key space (kdb => key
database).
Configuration files of different formats can be **mounted** into this key space.
Mounting allows to integrate different configuration files into the Elektra key
space. This means, all settings of a configuration file can be queried and
also manipulated by Elektra.
This makes it possible to manipulate settings in the *mounted* configuration
file on a key value basis. (See
[puppet-libelektra](https://github.com/ElektraInitiative/puppet-libelektra/blob/master/README.md)
documentation for more information on Elektra and mounting).

Example of the Elektra key space:
```sh
# This examples assumes /etc/samba/smb.conf is mounted under system/sw/samba
# and /etc/ntp.conf is mounted under system/sw/ntp
...
system/sw/samba                  # <= /etc/samba/smb.conf is mounted here
system/sw/samba/global           # <= INI section within smb.conf
system/sw/samba/global/workgroup # <= configuration setting under section 'global'
...
system/sw/ntp                # <= mountpoint for /etc/ntp.conf
system/sw/ntp/server         # <= setting 'server' in ntp.conf
system/sw/ntp/driftfile      # <= setting 'driftfile' in ntp.conf
...
```

Each mount point (here `system/sw/samba` and `system/sw/ntp`) is defined by the
following elements:
* *mount point*: path within the Elektra key space
* *file*: configuration file used for mounting
* *list of plugins*: Elektra plugin used to read/write the configuration file.
  Additionally, plugins for validation or manipulations can be added.

Configuration files are NOT added automatically (mounted) into the Elektra key
space. This has to be done once per configuration file. Therefore we can use the
resource type `kdbmount`. Once a configuration file is mounted, we can
manipulate its setting with the `kdbkey` resource.

The full documentation can be found under [Github
puppet-libelektra](https://github.com/ElektraInitiative/puppet-libelektra/blob/master/README.md)

#### `kdbmount` Resource Type

`kdbmount` ensures a specific configuration file is mounted at the given Elektra
mount point.

Important attributes:
* `name`: mount point to use, if not given the resource title is used
* `ensure`: mount point should be `present` or `absent` (default: `present`)
* `file`: path to configuration file to mount
* `plugins`: list of Elektra plugins used for mounting

```puppet
# mount the file /etc/samba/smb.conf at system/sw/samba
kdbmount { 'system/sw/samba':
  ensure  => 'present',
  file    => '/etc/samba/smb.conf',
  plugins => 'ini'
}

# mount the JSON file /etc/myapp/config.json at system/sw/myapp
# also add the validation plugins 'type', 'enum', 'range' and 'network' which
# will perform value validation
kdbmount { 'system/sw/myapp':
  file    => '/etc/myapp/config.json',
  plugins => ['json', 'type', 'enum', 'range', 'network']
}
```

#### `kdbkey` Resource Type

Once a configuration file is mounted, its settings can be manipulated with the
`kdbkey` resource type.

Important attributes:
* `name`: Elektra key path, if omitted, the resource title is used
* `ensure`: if key should be `present` or `absent` (default: `present`)
* `value`: desired value of key
* `prefix`: Elektra key name prefix. If given, this prefix will be prepended to
  `name` attribute (or title if name is missing)
* `check`: add key validation checks. Given validations will be
  performed before each write operation. This can be used to ensure only valid
  values are written to the configuration file.
* `comments`: key comments, if the storage plugin and configuration file format
  supports comments, this will go into the configuration file

```puppet
# from above example, ensure configuration setting 'workgroup' under section
# 'global' exists and has value 'MY_WORKGROUP'
kdbkey { 'system/sw/samba/global/workgroup':
  ensure => 'present',
  value  => 'MY_WORKGROUP'
}

# ensure desired configuration setting is missing
kdbkey { 'system/sw/samba/global/debug level':
  ensure => 'absent'
}

$myapp_mountpoint = 'system/sw/myapp'
kdbkey {
  # ensure 'instances' has given value, is of type 'short' and is within 1 and 10
  # requires 'system/sw/myapp' is mounted with plugins 'type' and 'range'
  'instances':
    prefix => $myapp_mountpoint, # key name is "system/sw/myapp/instances"
    value  => $instances,
    check  => {
      'type'  => 'short',
      'range' => '1-10'
    } ;

  # specify value for 'client' and ensure it has a valid IP address
  # requires 'system/sw/myapp' is mounted with 'network' plugin
  'client':
    prefix => $myapp_mountpoint,
    value  => $client_ip,
    check  => 'ipaddr' ;
}
```

### `file_line` Resource Type

This resource type (available in *puppetlabs-stdlib*) can be used to ensure a
specific **line** within a file exists or is missing. It can also be used to
replace particular lines with a given one.

Important attributes of `file_line`:
* `ensure`: whether the line should be `present` or `absent` (default:
  `present`)
* `path`: path to the file which should be manipulated
* `line`: line string, that should be added to the file defined by `path`
* `match`: regular expression, if a matching line was found, this matching line
  will be replaced by the value of `line`. If not, the `line` will be added to
  the file.
* `match_for_absence`: if set to true and `ensure => absent` the line matching
  `match` will be deleted.


```puppet
# ensure the specified line exists in the given file
file_line { "hosts samba server":  # use an arbitrary unique resource title here
  path => '/etc/hosts',
  line => "$samba_ip   $samba_hostname samba"
}

# ensure given line exists replacing a matching line if existing
file_line { "hosts VPN server":
  path  => '/etc/hosts',
  line  => "$vpn_ip   $vpn_hostname vpn",
  match => " vpn$"
}

# ensure $dead_ntp_server is not in the ntp.conf
file_line { "remove dead ntp server":
  ensure => 'absent',
  path   => '/etc/ntp.conf',
  line   => "server $dead_ntp_server"
}
```

The full documentation can be found under [Puppetforge
Puppetlabs-stdlib#file_line](https://forge.puppet.com/puppetlabs/stdlib#file_line).

### `ini_setting` Resource Type

This resource type allows to manipulate INI based configuration files on a per
setting bases. Instead of modifying the whole configuration file it allows to
manipulate concrete INI settings only.

Important attributes of `ini_setting`:
* `ensure`: whether the setting should be `present` or `absent`
* `path`: path to configuration file to manipulate
* `section`: if given, specifies the *section* in which the setting can be found
* `setting`: setting to manipulate
* `value`: value of the setting

```puppet
# specify specific value for setting 'baz' under section 'bar'
ini_setting { "sample setting":
  ensure  => present,
  path    => '/tmp/foo.ini',
  section => 'bar',
  setting => 'baz',
  value   => 'quux',
}

# ensure setting 'other_setting' under section 'bar' is not present in '/tmp/foo.ini'
ini_setting { 'removed setting':
  ensure  => 'absent',
  path    => '/tmp/foo.ini',
  section => 'bar',
  setting => 'other_setting'
}
```

The full documentation can be found under [Puppetforge
puppetlabs-inifile](https://forge.puppet.com/puppetlabs/inifile).

### `augeas` Resource Type

*Augeas* is library to manipulate configuration files on a per setting bases. It
parses existing configuration files and transforms them to in internal XML-like
representation. The user is able to query and manipulate this internal XML
representation, whereas changes are written back to the actual configuration
file. Puppet has a built-in resource type `augeas` which allows interacting with
this library. In contrast to Elektra, configuration files do not have to be
*mounted* instead very common config files are added an parsed automatically.

The `augeas` resource type is designed to operate on Augeas *tasks*, i.e. a user
defines a set of Augeas commands to modify the XML representation and therefore
modify the underlying configuration file.

Important attributes:
* `changes`: one or more Augeas commands
* `context`: if given all Augeas path names will be prepended by this parameter
* `incl`: load a specific configuration file, which is not part of the default
  Augeas config file set.
* `lens`: Name of the Augeas *lens* to be used for loading custom config files
* `onlyif`: only apply given commands (`changes`) if this Augeas query evaluates
  to true

Important commands for attribute `changes`:
* `set <PATH> <VALUE>`: set value
* `remove <PATH>`: delete specified path

Important commands for attribute `onlyif`:
* `get <PATH> <COMPARATOR> <VALUE>`: whereas `<COMPARATOR>` is one of `>, >=,
  !=, ==, <=, <`
* `match <PATH> size <COMPARATOR> <INT>`: match for number or elements

An Augeas `<PATH>` starts with `/files` followed by the absolute path name of
the desired configuration file. The XML representation is accessible by this
path, whereas hierarchies will be extended by another path levels:

```sh
/files/etc/samba/smb.conf/target[1]/workgroup
# target[1] referse to the first section in smb.conf, here 'global'
# target[1]/workgroup  referse to setting workgroup in section 'global'
```

Augeas supports a XPath like query within its path specifications to allow more
flexible matches:
```sh
/files/etc/samba/smb.conf/*[. = 'global']/workgroup
# select the 'target' node with value 'global'
# this matches always setting 'workgroup' under section 'global' even if it is not the first section
```

Examples:

```puppet
# enable X11 forwarding for the SSH-server, only if it isn't enabled already
augeas { 'enable sshd X11 forwarding':
  context => '/files/etc/ssh/sshd_config',
  changes => [
    "set X11Forwarding yes",
    "set X11DisplayOffset 10"
  ],
  onlyif  => "get X11Forwarding != yes"
}

# add a new Host specific SSH client config for all users
augeas { "add $host client config":
  context => '/files/etc/ssh/ssh_config',
  onlyif  => "match *[. = '${host}'] size == 0",
  changes => "set Host[0] '${host}'",
}

# now we add host specific settings
augeas { "add settings to $host client config":
  context => '/files/etc/ssh/ssh_config',
  changes => [
    "set *[. = '${host}']/X11Forwarding yes"     # enable X11Forwaring on the client
  ],
  onlyif  => "get *[. = '${host}']/X11Forwarding != yes", # do it only if we have to

  # now ensure, this Augeas task is executed AFTER the "add $host client config" task
  require => Augeas["add $host client config"]
}
```

The full documentation can be found under [Resource Type
Reference#Augeas](https://docs.puppet.com/puppet/3.8/type.html#augeas).
Additional explanations and usage examples are available under [Resource tips
and examples:
Augeas](https://docs.puppet.com/puppet/latest/resources_augeas.html).

### `host` Resource Type

`host` is a built-in resource type to manipulate entries of '/etc/hosts' files.

Important attributes:
* `name`: hostname, if not given resource title is used
* `ensure`: whether the host entry should be `present` or `absent` (default:
  `present`)
* `ip`: IP address used for this host entry. If you supply an invalid IP address
  the `host` resource type fails.
* `host_aliases`: any host aliases for this host. Multiple values must be
  specified as an array.
* `target`: full path to hosts file. (default: '/etc/hosts')

```puppet
# ensure entry exists
host { 'storagemoster1':
  ensure       => present,
  ip           => '192.168.3.12',
  host_aliases => ['samba', 'nfs']
}

# ensure entry in alternative hosts file is missing
host { 'oldserver':
  ensure => absent,
  target => '/etc/hosts_other'
}
```

The full documentation is available under [Resource Type
Reference#host](https://docs.puppet.com/puppet/3.8/type.html#host).


## References

* Puppet 3.8 Reference Manual: https://docs.puppet.com/puppet/3.8/
* Resource Type Reference: https://docs.puppet.com/puppet/3.8/type.html
* Puppetforge puppetlabs-stdlib Reference: https://forge.puppet.com/puppetlabs/stdlib
* Embedded Ruby (ERB) Template Syntax:
  https://docs.puppet.com/puppet/3.8/lang_template_erb.html
* Github puppet-libelektra Reference:
  https://github.com/ElektraInitiative/puppet-libelektra/blob/master/README.md
* Puppetforge puppetlabs-inifile Reference: https://forge.puppet.com/puppetlabs/inifile
* Resource tips and examples: Augeas:
  https://docs.puppet.com/puppet/latest/resources_augeas.html
