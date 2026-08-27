# Introduction

WSL2 is a Linux compatibility layer available in Windows 11. It provides a full Linux kernel, allowing you to run Linux binary executables natively on your desktop.
This is good news for programmers, who often prefer to work in the Linux ecosystem when developing code. There are several reasons for this, including:
- code generally executes quicker on a Linux kernel than it does in Windows
- the default Linux command line interface (bash) is generally considered more approachable than the Windows equivalents (CMD/PowerShell)
- Linux package management tends to be a much cleaner way of handling software than Windows Installer
- Almost all servers and containers run Linux, so it helps to develop deployable code in the same ecosystem
For our team specifically, eHealth's Data Analytics Platform will soon provide us with access to an AWS environment with many Linux servers and applications. Being comfortable working in Linux will make operating in this environment much easier.
If any of that captures your interest, you are in the right place! This page will outline how to set up WSL2 as a development environment in NSW Health. It will also include instructions on how to install and configure some of the common tools needed for the work we do in our team. If there is a tool you use that is not on this list, once you establish a process please add instructions to this page.
This page would not exist without the late Harsha Bharadwaj (eHealth), who documented the core of these instructions. He was a wonderful colleague and incredibly generous with his extensive knowledge, and is much missed. Additional content has been added by Tim Hawkins. Thanks also to Ben Drury, who took this wiki page for a test drive and found all Tim's mistakes.
WSL is not officially supported by eHealth, so if you have any problems with configuration and setup - you are sort of on your own. But figuring stuff out for yourself is part of the fun of the Linux journey. :)
Installing WSL2
If you are running a compatible version of Windows, you can install WSL2 using the official Microsoft guide.
You will need a .wslconfig file in your %USERPROFILE% location on the Windows side, containing the following settings:
[wsl2]
networkingMode=mirrored
dnsTunneling=true
autoProxy=true
Installing a Linux Distribution
WSL2 allows the installation of a wide variety of Linux distros. The preferred distro for our team is Ubuntu LTS 24.04 (Noble Numbat). This should be the default distro installed.
Once installed, create your root user and password.
Learning the WSL Filesystem
At this point, it's recommended that you pause and get familiar with the file system on your new distro.
Even if you're familiar with Linux, it's important to understand the quirks of storage and performance on WSL. Again, Microsoft's official guide is great for this. For a broader primer on Linux, check out Fireship.io's Linux Directories Explained in 100 Seconds.
If you are still feeling lost, I can highly recommend the book Learning the UNIX Operating System, which is in our resources folder.
Interacting with WSL2 using the Command Line
The command line is scary! But it is much easier than it looks, and the default Linux shell (bash) is very friendly indeed. Once you start using the terminal, you'll realise how quick and easy it is - and you'll never want to go back to clicking around a GUI. :)
The official Microsoft guide provides a great crash course on basic commands to get you started. If you'd like to learn more, I can highly recommend the book Learning the bash Shell, available in our Resources folder.
SSL Verification for conda, pip etc.
When behind the NSWH proxy/firewall, you will likely encounter a range of SSL verification issues with a variety of tools like conda and pip. To fix these, you will need to update the certificate bundle in your distro to include the NSWH root certificate.
The easiest way to export this is to open 'Manage user certificates' (certmgr) in the Microsoft Management Console (mmc) on Windows. Under 'Trusted Root Certification Authority' > 'Certificates' find and export 'NSWHEALTH-RootCA'.
Copy the file to your user directory in your distro (for Ubuntu this will be /usr/local/share/ca-certificates/*.crt) - you may need to rename the file extension first.
Once copied, invoke sudo update-ca-certificates to add the root certificate to your bundle. Restart WSL and the relevant applications should be able to use the certificate.
Installing Visual Studio Code
VS Code is a customisable text editor developed by Microsoft, which can be used as a lightweight IDE.
Although WSL is compatible with native Linux code editors like vim and emacs, Microsoft has developed a number of extensions for VS Code to make it a very seamless development environment. Instructions for installing these are available in Microsoft's official guide.
Installing Docker
Docker is a service that allows the creation of containers. Containers are a way to package software with a lightweight virtualised operating system kernel - making them easier and simpler to deploy and run on different servers or machines.
Currently our team does not have the capacity to deploy containerised apps to servers, although this is expected to change with the rollout of the Data Analytics Platform. In the interim, Docker is still useful for spinning up well-isolated development environments ('devcontainers'). VS Code has excellent tools for creating devcontainers and you can read more about them here.
Docker Desktop for Windows is tightly integrated into WSL2. The official Microsoft guide provides great instructions for how to install and configure Docker to work with WSL. Docker Desktop itself provides a very polished and interactive 'getting started' tutorial which I can highly recommend - it's genuinely a lot of fun.
Once Docker Desktop is installed, you will need to configure the client to pass proxy information to containers. The official Docker guide provides good instructions on how to do this here.
Installing Git
Git is free and open source software for tracking and controlling changes to files. It is great for working collaboratively on projects with other team members, and works particularly well with text files (which makes it great for managing source code). If you are unfamiliar with Git, I highly recommend this introductory tutorial.
Git is most often used in conjunction with a web platform that allows remote hosting of Git repositories (e.g. GitHub). NSW Health runs a self-hosted instance of GitHub Enterprise under the name GitHealth. Our team's GitHealth Org is located here - you will need a current GitHealth license to access it. For more information on GitHealth, and for steps to obtain a GitHealth license, please refer to SARA.
Your WSL2 distro should come installed with Git, but if this needs to be installed or updated the steps in bash are as follows:
sudo add-apt-repository ppa:git-core/ppa -y
sudo apt update
sudo apt install git -y
git --version
To clone repos within WSL you will need to point your WSL git install at your config manager in windows:

git config --global credential.helper "/mnt/c/Program\ Files/Git/mingw64/bin/git-credential-manager.exe
Installing Oracle Instant Client
Accessing Oracle databases on WSL will require the installation of the Oracle Instant Client. Installers can be found here - download the ZIPs for the Basic and SQL*Plus packages.
Next (in bash), create a folder called /opt/oracle:
sudo mkdir -p /opt/oracle
then install the packages zip and libaio1:
sudo apt-get install zip libaio1
Once this is done you can unzip the Oracle client packages into your new folder (replace [location] with the file path of your download), and change to the Instant Client folder:
cd /opt/oracle
unzip /[location]/instantclient-basic-linux.x64-21.5.0.0.0dbru.zip
unzip /[location]/instantclient-sqlplus-linux.x64-21.5.0.0.0dbru.zip
cd instantclient_21_5
(note that the above code block assumes we are using Instant Client 21.5 - for newer versions update as appropriate)
Next, we need to create linked objects in WSL for the necessary libraries using the following commands:
ln -s libclntsh.so.12.1 libclntsh.so
ln -s libocci.so.12.1 libocci.so
Now we need to edit our .bashrc file in order to set an environment variable for Oracle Home. To edit the file using nano, type:
sudo nano ~/.bashrc
then add the following lines to the bottom of the file:
# set Oracle Home:
export ORACLE_HOME=/opt/oracle/instantclient_12_2
export LD_LIBRARY_PATH=ORACLE_HOME:LD_LIBRARY_PATH
export PATH=ORACLE_HOME:PATH

