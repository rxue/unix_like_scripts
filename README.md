# How to run

**Prerequisite**: install `git` as the first step and then clone this project somewhere
1. `cd` to this project directory, `linux-scripting`
2. `chmod +x ubuntu/install.sh`
3. `sudo ./ubuntu/install.sh`

## How to install a single software
example: `sudo bash -c 'source ubuntu/install_functions.sh && install_docker'`


# Bash
[Bash Beginners Guide](http://www.tldp.org/LDP/Bash-Beginners-Guide/Bash-Beginners-Guide.pdf)

## Coding Convention
* Sha-bang aka. Shebang

The sha-bang (`#!`) at the head of a script tells your system that this file is a set of commands to be fed to the command interpreter indicated. 

This is a **Linux-based Bash** script project, i.e. **non-POSIX**. So sha-bang `#!/bin/bash` is used.

<sub>Reference: [Advanced Bash-Scripting Guide](http://tldp.org/LDP/abs/html/) > [Chapter 2. Starting Off With a Sha-Bang](http://tldp.org/LDP/abs/html/sha-bang.html)</sub>

* Variables

When referencing a variable, surround its name with curly braces to clarify to the parser and to human readers where the variable name stops and other text begins; for example, `${etcdir}` instead of just `$etcdir`

There's no standard convention for the naming of shell variables, but all-caps names typically suggest environment variables or variables read from global configuration files. More often than not, local variable are all-lowercase with components separated by underscores.

<sub>Reference: UNIX AND LINUX SYSTEM ADMINISTRATION HANDBOOK (4th edition) > Chapter 2 Scripting and the Shell > Shell basics > Variables and quoting (P/33)</sub>

* Functions

Declaring a function is just a matter of writing `function my_func { my_code }`. Calling a function is just like calling another program, just write its name. 

<sub>Reference: [BASH Programming - Introduction HOW-TO](http://tldp.org/HOWTO/Bash-Prog-Intro-HOWTO.html) > [8. Functions](http://tldp.org/HOWTO/Bash-Prog-Intro-HOWTO-8.html)</sub>

* Coding Strategy

Try to replace old style auxiliary language like `sed`, `awk` with **python** in case the syntax is too complicated to be readable. 

## Code Description

### configure_debian_functions.sh
#### How to use functions in configure_debian_functions.sh 
All the functions are about installing extra software, usually to `/opt`. In order to install software to `/opt`, 
1. go to the directory of this script, shift to `sudo` mode with `su` command
2. give the password of `sudo`, click enter to shift to `sudo` mode
3. `source configure_debian_function.sh`
4. call any of the functions in configure_debian_functions.sh, e.g. `install_maven`
  
`bash configure_my_debian.sh`

#### TODO
* Add a crontab to shutdown PC at a specified time every day
* Command instead of logout for Xsession refresh still unsolved, `source /etc/X11/Xsession` encountered errors
* In case of installing on Virtual Box, add the Guest Addition installation script
* Install the **lvm2 (Logical Volume Manager)** and make use of it to manage the disk instead of *partitions* (As administrators get comfortable with logical volume management, partitions are disappearing, too.). Try to make use of **snapshots** to make a backup mechanism with an external storage device
* Make an lost+found mechanism like the recycle bin in Windows
* 20170206: based on the Java class file format (refer to https://en.wikipedia.org/wiki/Java_class_file and http://stackoverflow.com/questions/698129/how-can-i-find-the-target-java-version-for-a-compiled-class), create a script to get the Java class version information

<sub>Reference: UNIX AND LINUX SYSTEM ADMINISTRATION HANDBOOK (4th edition) > Chapter 8 Storage > 8.4 Peeling the Onion: The Software Side of Storage (P/222)</sub>

### mounted_disk_monitor.sh
Technical keywords:
* `getopts`
* rsyslog > command `logger` with option `-t`
* process substitution

#### TODO
* WARNING SHOULD BE SENT ONCE A DAY, whereas currently it is sent only ONCE 

## Learning
### FAQ
----
* How to check the distribution version of your current Linux 
Answer: Distribution version is stored in `/etc/os-release` 
* How to get running script directory: ``$(cd `dirname $0` && pwd)``
* How to list the system's disks and identify the new drive: `sudo fdisk -l`
* How search text from a File with `less` from bottom up: `?keyword`

## Other Software Installation
https://github.com/nodesource/distributions#debmanual
