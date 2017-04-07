# Configuration File Handling with Puppet: a Software Experiment

The goal of this user study or software experiment is to outline differences
between Puppet strategy for manipulating
configuration files. Therefore this study compares six different methods for
writing or modifying configuration files, from very general to very specific
methods.

This study consists of five tasks, whereas all tasks will be solved several
times, each with a different Puppet method. The five tasks can be classified in
3 main groups:
* writing a complete configuration file at once
* partial configuration file manipulations
* maintenance tasks: bug fixing, adding features


## Experiment Setup Requirements

The user study setup consist of a set of Docker container. Therefore first
ensure you have a recent Docker version installed and your account is able to
access the Docker daemon. Also the used text editor is running inside a Docker
container, which requires to access to your X-Display.

The experiment setup was tested on the following installations:
- Ubuntu 16.04 (development environment)
- Arch Linux (latest)
- Debian 8
- CentOS 7 (might require applying the `tools/atom-allow-x0-access.pp` selinux
  policy)
- above installations through ssh X11 forwarding (requires fast connection)


## How to Start

- Clone this repo
- start the `tools/expctr.py` tool
- run `pull_images`: this will pull all Docker images from Dockerhub
- read task instructions `task_descriptions.md`

Approximately study duration: 4.5h (without prior Puppet knowledge)

If you have finished the study, export the results with the command `finished`
and send me the resulting tarball.

Thank you very much ;)
