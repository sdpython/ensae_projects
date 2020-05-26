
.. _l-cheatsheet-jenkins:

Cheat Sheet on Jenkins
======================

.. contents::
    :local:

Installation
++++++++++++

Install Jenkins:

::

    wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -
    sudo sh -c 'echo deb https://pkg.jenkins.io/debian-stable binary/ > \
        /etc/apt/sources.list.d/jenkins.list'
    sudo apt-get update
    sudo apt-get install jenkins

Remove Jenkins:

::

    apt-get remove --purge jenkins

Change Jenkins user:

::

    nano /etc/init.d/jenkins
    chown -R dupre:dupre /var/lib/jenkins
    chown -R dupre:dupre /var/cache/jenkins
    chown -R dupre:dupre /var/log/jenkins

    chown -R jenkins:jenkins /var/lib/jenkins
    chown -R jenkins:jenkins /var/cache/jenkins
    chown -R jenkins:jenkins /var/log/jenkins

    /etc/init.d/jenkins restart

Start, Restart
++++++++++++++

::

    /etc/init.d/jenkins start
