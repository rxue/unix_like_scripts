# Bash
[Bash Beginners Guide](http://www.tldp.org/LDP/Bash-Beginners-Guide/Bash-Beginners-Guide.pdf)

## Coding Convention
* Sha-bang aka. Shebang

The sha-bang (`#!`) at the head of a script tells your system that this file is a set of commands to be fed to the command interpreter indicated. 

This is a **Linux-based Bash** script project, i.e. **non-POSIX**. So sha-bang `#!/bin/bash`

<sub>Reference: [Advanced Bash-Scripting Guide](http://tldp.org/LDP/abs/html/) > [Chapter 2. Starting Off With a Sha-Bang](http://tldp.org/LDP/abs/html/sha-bang.html)</sub>

* Variables

When referencing a variable, surround its name with curly braces to clarify to the parser and to human readers where the variable name stops and other text begins; for example, `${etcdir}` instead of just `$etcdir`

There's no standard convention for the naming of shell variables, but all-caps names typically suggest environment variables or variables read from global configuration files. More often than not, local variable are all-lowercase with components separated by unserscores.

<sub>Reference: UNIX AND LINUX SYSTEM ADMINISTRATION HANDBOOK (4th edition) > Chapter 2 Scripting and the Shell > Shell basics > Variables and quoting (P/33)</sub>

* Functions

Declaring a function is just a matter of writing `function my_func { my_code }`. Calling a function is just like calling another program, just write its name. 

<sub>Reference: [BASH Programming - Introduction HOW-TO](http://tldp.org/HOWTO/Bash-Prog-Intro-HOWTO.html) > [8. Functions](http://tldp.org/HOWTO/Bash-Prog-Intro-HOWTO-8.html)</sub>

## Code Description

### configure_my_debian.sh
`bash configure_my_debian.sh`


#### TODO
* Add a crontab to shutdown PC at a specified time every day
* Command instead of logout for Xsession refresh still unsolved, `source /etc/X11/Xsession` encountered errors
* In case of installing on Virtual Box, add the Guest Addition installation script

FAQ:
----
* How to check the distribution version of your current Linux: `lsb_release -a` 
* How to get running script directory: ``$(cd `dirname $0` && pwd)``
 
