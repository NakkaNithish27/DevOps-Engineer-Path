# 🐍 Python Fabric — Remote Server Automation with Python

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

## 1.1 The Core Problem: Managing Hundreds of Servers Remotely

Imagine you are responsible for hundreds of servers. You need to execute commands on all of them — install packages, check disk space, deploy applications. Doing this manually by SSH-ing into each machine is impractical. You need a way to sit on one machine (your laptop, or a dedicated "script box") and push commands to remote servers programmatically. Fabric is the Python library that solves exactly this problem. It lets you write Python functions that execute shell commands — both locally and on remote machines — and call those functions directly from the command line. [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

The critical mental model here is: **Fabric turns Python functions into CLI-executable remote operations.** You write a function in Python, and you invoke it from the bash shell using the `fab` command, passing hostnames, usernames, and arguments. This bridges the gap between Python's scripting power and the operational need to manage infrastructure via SSH. [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

## 1.2 pip — The Python Package Ecosystem Gateway

Before you can use Fabric (or any external Python library), you need **pip** — Python's package installer. pip is to Python what `apt` is to Ubuntu or `yum` is to CentOS. It connects to the Python Package Index (PyPI) and downloads/installs libraries into your Python environment. [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

The subtlety the video highlights is that **the correct version of pip depends on both your Python version and your operating system**. As Python and OS versions evolve, the installation command for pip itself changes. To handle this variability, there is a bootstrap script at `bootstrap.pypa.io/get-pip.py`. When you download and run this script with `python3`, it auto-detects your environment and installs the correct pip version for you. This is an important operational pattern: **use a self-detecting bootstrap script rather than hardcoding version-specific installation commands.** [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

🔍 **Deep Dive:** The script at `bootstrap.pypa.io/get-pip.py` doesn't install pip directly upon download. It downloads a Python script file. You then execute that script (`python3 get-pip.py`), and the script itself handles the detection and installation logic. This two-step pattern (download installer → run installer) is common in infrastructure tooling. [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

## 1.3 Fabric — Architecture and Core Design

Fabric (specifically version <2.0, which is the "classic" Fabric API used in this video) provides a set of methods imported from `fabric.api`. The fundamental architectural concept is: [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215.fabfile.py)

**You create a file named `fabfile.py` in a working directory.** This is not just any Python file — it is a convention-based entry point. When you run the `fab` command from that directory, Fabric automatically discovers `fabfile.py` and exposes every function defined in it as a CLI command. This is a **convention-over-configuration** pattern: no registration, no config file pointing to your script. Just name it `fabfile.py` and Fabric finds it. [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

The import statement `from fabric.api import *` loads all available Fabric methods into your script's namespace. The key methods are: [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215.fabfile.py)

**`local(command)`** — Executes a shell command on the **local machine** (the machine where you're running the `fab` command, i.e., your script box). It literally passes the string you give it to the local bash shell for execution and returns the output. If the command you pass is not a valid bash command, it will fail. [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

**`run(command)`** — Executes a shell command on the **remote machine** as a normal (non-root) user. It SSHs into the target machine, runs the command under the user you specified (via `-u` flag or `env.user`), and returns the output. You cannot use `run()` for commands that require root/sudo privileges — `yum install`, for example, would fail with a permission error under `run()`. [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

**`sudo(command)`** — Executes a shell command on the **remote machine** with elevated (root) privileges. Internally, it prepends `sudo` to whatever command you provide. This is why the remote user must be in the sudoers file with `NOPASSWD` — so that the sudo elevation doesn't block waiting for an interactive password prompt during automated execution. [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

**`put(local_source, remote_destination, use_sudo=True/False)`** — Transfers a file from the local machine to the remote machine using SCP under the hood. The `use_sudo` parameter is critical: if the remote destination directory is owned by root (like `/var/www/html/`), the devops user cannot write to it without sudo. Setting `use_sudo=True` makes the transfer happen with root privileges on the remote side. [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

**`lcd(path)`** — "Local cd." Used as a context manager (`with lcd(path):`), it changes the working directory on the **local machine** for the duration of the `with` block. Any `local()` calls inside the block execute relative to that directory. [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

**`cd(path)`** — "Remote cd." Used as a context manager (`with cd(path):`), it SSHs into the remote machine and changes the working directory there. Any `run()` or `sudo()` calls inside the block execute relative to that remote directory. [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

The distinction between `lcd` and `cd` is one of the most important concepts in Fabric. Both look similar, but one operates locally and the other operates remotely. Confusing them is a common mistake. [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

🔍 **Deep Dive:** The `env.user` variable (set as `env.user = 'devops'` in the fabfile) is a global configuration that tells Fabric which user to use when connecting to remote machines. This can be overridden at the command line with `-u`. The architecture here is: **global defaults in the fabfile, CLI overrides at execution time.** [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215.fabfile.py)

## 1.4 The `fab` CLI — Bridging Python Functions to Shell Commands

The `fab` command is the Fabric CLI tool. Its core behavior: [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

1. It looks for `fabfile.py` in the current working directory.
2. It discovers all functions defined in that file.
3. It exposes them as CLI "commands" that you can invoke by name.

`fab -l` lists all available commands (functions). `fab <function_name>` executes that function. Arguments are passed using the colon syntax: `fab greeting:msg=Morning`. Multiple arguments are comma-separated. The `-H` flag specifies the target host, and `-u` specifies the remote username. [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

This is a powerful pattern: **you never need to write argument parsing code.** Fabric handles the mapping from CLI arguments to Python function parameters automatically. [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

⚠️ **Expert Note:** The `-p` flag exists to pass a password on the command line, but this is insecure because the password gets stored in shell history. The video explicitly recommends SSH key-based authentication instead — exchange keys once, and then `fab` uses the private key automatically for all subsequent connections. This is standard operational security practice. [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

## 1.5 SSH Key-Based Authentication — The Security Foundation

Fabric relies on SSH to connect to remote machines. There are two authentication methods: password-based and key-based. The video strongly emphasizes **key-based authentication** as the correct approach for automation. [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

The flow is: you generate an SSH keypair on the script box (`ssh-keygen`), then copy the public key to each remote machine (`ssh-copy-id devops@web01`). After this, the script box can SSH into the remote machine without a password — it presents the private key, the remote machine checks it against the stored public key, and grants access. [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

Fabric automatically uses the default private key (`~/.ssh/id_rsa`) when connecting. You don't need to specify the key path in the `fab` command. This is why `fab -H web01 -u devops remote_exec` works without any `-p` or `-i` flag — the key exchange was done beforehand. [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

🔍 **Deep Dive:** For SSH password login to work during the initial key exchange, `PasswordAuthentication` must be set to `yes` in `/etc/ssh/sshd_config` on the remote machine, and the SSH service must be restarted afterward. Once keys are exchanged, you could disable password authentication entirely for better security. The SSH service name is `sshd` on CentOS/RPM-based systems. [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

## 1.6 Remote Machine Preparation — User, Sudo, and SSH Config

Before Fabric can operate on remote machines, three prerequisites must be satisfied on each target: [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

1. **A dedicated user must exist** (e.g., `devops`). This user is the identity under which Fabric will SSH in and execute commands.
2. **That user must have passwordless sudo privileges.** This is configured via `visudo` by adding a line like `devops ALL=(ALL) NOPASSWD: ALL`. Without `NOPASSWD`, the `sudo()` method in Fabric would hang waiting for a password prompt in a non-interactive SSH session.
3. **Password-based SSH login must be enabled** (at least temporarily, for the initial key exchange). This is done by ensuring `PasswordAuthentication yes` in `/etc/ssh/sshd_config` and restarting `sshd`.

This is a **one-time setup per machine.** Once the user exists, has sudo rights, and SSH keys are exchanged, Fabric can operate on that machine indefinitely without further manual intervention. [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

## 1.7 Host-to-IP Mapping — Operational Manageability

Instead of using raw IP addresses in `fab -H 192.168.x.x`, the video adds hostname-to-IP mappings in `/etc/hosts` on the script box (e.g., `192.168.56.37 web01`). This way, you can use `fab -H web01` — which is more readable, more manageable, and less error-prone than remembering IP addresses across hundreds of servers. [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

⚠️ **Expert Note:** In production environments, this hostname resolution would typically be handled by DNS rather than `/etc/hosts`. But for local Vagrant-based development environments, `/etc/hosts` is a quick and effective solution. [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

## 1.8 The Broader pip Ecosystem — Jenkins, AWS, and Beyond

The video briefly demonstrates that Fabric is just one of many Python libraries available through pip for DevOps work: [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

**python-jenkins** — A library that lets you manage Jenkins programmatically from Python. You can create, copy, delete, and update jobs, retrieve build information, and more. The pattern is: install the library (`pip install python-jenkins`), import it, create a connection object by passing the Jenkins URL + credentials, and then call methods on that object. [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

**boto3** — Amazon's official Python SDK for AWS. It allows you to manage AWS resources (S3 buckets, EC2 instances, CloudWatch alarms, etc.) programmatically. The pattern is identical: install (`pip install boto3`), configure credentials (`aws configure`), import, create a resource/client object, and call methods. [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

The unifying engineering pattern across all of these is: **install → import → authenticate → get object → call methods.** This is the standard Python library interaction model. [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

⚠️ **Expert Note (Critical Security Warning):** The video strongly warns against storing AWS access keys and secret keys in Python source code. If the code is pushed to a repository like GitHub, the keys can be accidentally exposed. The correct approach is to store credentials externally — via `aws configure` (which stores them in `~/.aws/credentials`) or via environment variables — and keep them completely separate from the codebase. [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

## 1.9 The R\&D Reality of Automation

The video closes with an important meta-insight: **most of your time in automation goes into R\&D — understanding functions, methods, reading documentation, and testing — not into writing the final script.** The actual script-writing is a small fraction of the total effort. This is a reusable engineering truth that applies broadly across all automation work. [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

## What We Are Building

We are setting up a complete remote automation workflow using Python Fabric. Starting from a bare script box (an Ubuntu/CentOS VM managed via Vagrant), we will: install pip and Fabric, write Fabric functions that execute commands locally and remotely, prepare remote VMs for Fabric access, and culminate in a fully automated website deployment function that installs a web server, downloads a website template, and deploys it — all from a single command. The final outcome: run one `fab` command and a website goes live on remote servers. [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215.fabfile.py)

***

### Step 1: Install pip Using the Bootstrap Script

We need pip to install Fabric. Rather than using OS-specific package managers (which may give us the wrong pip version), we use the universal bootstrap script.

**Download the script:**

```bash
wget bootstrap.pypa.io/get-pip.py
```

* `wget` — command-line file downloader
* `bootstrap.pypa.io/get-pip.py` — the URL hosting the pip bootstrap script

This downloads a Python file called `get-pip.py` to your current directory. **It does not install pip yet.** It only downloads the installer script. [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

**Run the script to install pip:**

```bash
python3 get-pip.py
```

* `python3` — invokes the Python 3 interpreter
* `get-pip.py` — the downloaded script, which detects your OS and Python version and installs the correct pip

**Verification:** After execution, you should see installation messages confirming pip was installed. You can verify with `pip --version`. [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

***

### Step 2: Install Fabric via pip

```bash
pip install 'fabric<2.0'
```

* `pip install` — tells pip to download and install a package
* `'fabric<2.0'` — installs Fabric version less than 2.0 (the "classic" Fabric with the `fabric.api` interface). The quotes prevent the shell from misinterpreting `<` as a redirection operator

**What happens internally:** pip connects to PyPI, downloads the Fabric package and its dependencies, and installs them into your Python environment. After this, `from fabric.api import *` becomes available in Python scripts. [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

**Verification:** The command should end with `Successfully installed fabric-...`. [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

***

### Step 3: Create the Working Directory and fabfile.py

```bash
cd /opt/pyscripts
mkdir fabric
cd fabric
vim fabfile.py
```

The file **must** be named `fabfile.py`. This is how Fabric discovers your functions. Any other name and `fab -l` will find nothing. [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

***

### Step 4: Write and Test a Basic Python Function via Fabric

In `fabfile.py`, write: [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215.fabfile.py)

```python
from fabric.api import *

def greeting(msg):
    print("Good {}".format(msg))
```

Save and exit (`:wq` in vim).

**List available commands:**

```bash
fab -l
```

* `fab` — the Fabric CLI tool
* `-l` — list all functions found in `fabfile.py` in the current directory

Output shows: `Available commands: greeting` [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

**Execute the function:**

```bash
fab greeting:msg=Morning
```

* `greeting` — the function name (Fabric calls it a "command")
* `:msg=Morning` — passes the value `Morning` to the `msg` parameter
* Multiple arguments would be comma-separated: `fab func:arg1=val1,arg2=val2`

**Expected output:** `Good Morning` followed by `Done.` — confirming the function executed successfully. [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

This step demonstrates the core Fabric mechanism: **Python functions become CLI commands without any argument-parsing boilerplate.** [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

***

### Step 5: Write a Local Command Execution Function

Add to `fabfile.py`: [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215.fabfile.py)

```python
def system_info():
    print("Disk Space")
    local("df -h")
    print("RAM size")
    local("free -m")
    print("System uptime.")
    local("uptime")
```

* `local("df -h")` — executes `df -h` on the **local** script box shell and prints the output
* `local("free -m")` — shows RAM information in megabytes
* `local("uptime")` — shows system uptime

**Execute:**

```bash
fab system_info
```

**Expected output:** Each `print()` message appears as a label, followed by `[localhost] local: <command>` (indicating local execution), followed by the actual command output. The `[localhost]` tag confirms this ran on the local machine, not a remote one. [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

⚠️ **Expert Note:** Whatever string you pass to `local()` must be a valid bash command. Fabric passes it directly to the shell. If the command is invalid, Fabric will return an error and the task will abort. [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

***

### Step 6: Prepare Remote Machines (web01 and web02)

This is a one-time setup on each target VM.

#### 6a. Create the devops user

```bash
vagrant ssh web01
sudo -i
useradd devops
passwd devops
# Enter password: admin123
```

* `useradd devops` — creates a new user named `devops`
* `passwd devops` — sets the password for that user [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

#### 6b. Grant passwordless sudo

```bash
visudo
```

Find the line `root ALL=(ALL) ALL`, copy it, and add:

```
devops ALL=(ALL) NOPASSWD: ALL
```

* `NOPASSWD` is critical — without it, `sudo()` in Fabric would hang waiting for a password prompt in the non-interactive SSH session [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

#### 6c. Enable SSH password authentication

```bash
vim /etc/ssh/sshd_config
```

Find `PasswordAuthentication`, remove the `#` (uncomment), ensure it reads:

```
PasswordAuthentication yes
```

Restart SSH:

```bash
systemctl restart sshd
```

* The service name is `sshd` on CentOS/RPM-based systems [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

#### 6d. Repeat for web02

Perform the exact same steps (6a–6c) on web02, using the same username (`devops`) and same password (`admin123`). Consistency matters because Fabric will use the same credentials for both machines. [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

***

### Step 7: Set Up Host-to-IP Mapping on the Script Box

Back on the script box:

```bash
vim /etc/hosts
```

Add:

```
192.168.56.37  web01
192.168.56.38  web02
```

(Get the actual IPs from your Vagrantfile.)

**Verify:**

```bash
ping web01 -c 4
```

* `-c 4` — send 4 ping packets
* You should see replies and the resolved IP address [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

***

### Step 8: Exchange SSH Keys for Passwordless Login

On the script box (as root):

```bash
ssh-keygen
```

Accept all defaults (press Enter through all prompts). This generates a keypair at `~/.ssh/id_rsa` (private) and `~/.ssh/id_rsa.pub` (public). [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

**Copy public key to remote machines:**

```bash
ssh-copy-id devops@web01
# Enter password: admin123
ssh-copy-id devops@web02
# Enter password: admin123
```

**Verify passwordless login:**

```bash
ssh devops@web01
# Should log in without password prompt
exit
```

You don't need to specify `-i ~/.ssh/id_rsa` because SSH uses the default key automatically. [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

This step connects to Step 6c — password login was enabled precisely so that `ssh-copy-id` could work. After keys are exchanged, Fabric will use key-based auth for all future connections. [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

***

### Step 9: Write and Execute Remote Command Functions

Add to `fabfile.py`: [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215.fabfile.py)

```python
env.user = 'devops'

def remote_exec():
    print("Get System Info")
    run("hostname")
    run("uptime")
    run("df -h")
    run("free -m")
    sudo("yum install mariadb-server -y")
    sudo("systemctl start mariadb")
    sudo("systemctl enable mariadb")
```

* `env.user = 'devops'` — sets the default SSH user globally (can be overridden with `-u`)
* `run("hostname")` — executes `hostname` on the remote machine as the devops user
* `sudo("yum install mariadb-server -y")` — executes `yum install` with root privileges on the remote machine

**Execute on web01:**

```bash
fab -H web01 -u devops remote_exec
```

* `-H web01` — target host
* `-u devops` — SSH username (overrides `env.user` if different)

**Expected output:** Each command output is prefixed with `[web01]`, confirming execution happened on the remote machine, not locally. The final `Done.` confirms success. [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

**Execute on web02:**

```bash
fab -H web02 -u devops remote_exec
```

Just change the hostname — same function, different target. This demonstrates the power of Fabric: **one function, any number of hosts.** [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

***

### Step 10: Write and Execute the Full Web Deployment Function

This is the culminating function. Add to `fabfile.py`: [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215.fabfile.py)

```python
def web_setup(WEBURL, DIRNAME):
    print("###...###")
    local("apt install zip unzip -y")
    print("Installing dependencies")
    sudo("yum install httpd wget unzip -y")
    print("Start & enable service.")
    sudo("systemctl start httpd")
    sudo("systemctl enable httpd")
    print("Downloading and pushing website to webservers.")
    local(("wget -O website.zip %s") % WEBURL)
    local("unzip -o website.zip")
    with lcd(DIRNAME):
        local("zip -r tooplate.zip * ")
        put("tooplate.zip", "/var/www/html/", use_sudo=True)
    with cd("/var/www/html/"):
        sudo("unzip -o tooplate.zip")
    sudo("systemctl restart httpd")
    print("Website setup is done.")
```

**Command breakdown:** [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

* `local("apt install zip unzip -y")` — installs zip/unzip on the local script box (needed to repackage the website files)
* `sudo("yum install httpd wget unzip -y")` — installs Apache (httpd), wget, and unzip on the **remote** machine
* `sudo("systemctl start httpd")` / `sudo("systemctl enable httpd")` — starts the web server and enables it to survive reboots
* `local("wget -O website.zip %s" % WEBURL)` — downloads the website template ZIP from the URL passed as argument, saving it as `website.zip` on the local machine
* `local("unzip -o website.zip")` — extracts the downloaded ZIP locally. `-o` overwrites without prompting
* `with lcd(DIRNAME):` — changes local directory into the extracted folder
  * `local("zip -r tooplate.zip *")` — repackages all content (HTML, CSS, images) into `tooplate.zip`
  * `put("tooplate.zip", "/var/www/html/", use_sudo=True)` — SCP-transfers the zip to the remote machine's web root with sudo
* `with cd("/var/www/html/"):` — changes directory on the **remote** machine
  * `sudo("unzip -o tooplate.zip")` — extracts the website files into the web root on the remote machine
* `sudo("systemctl restart httpd")` — restarts Apache to serve the new content

**Why the repackaging?** The downloaded ZIP contains a folder inside it. We `cd` into that folder, zip only the *contents* (not the folder itself), and push that flat zip to `/var/www/html/`. This ensures the HTML/CSS/images land directly in the web root, not inside a subfolder. [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

**Getting the arguments:**

1. Go to tooplate.com, pick a template
2. Press F12 (browser DevTools) → Network tab → click Download → cancel the download → copy the ZIP URL from the network request → this is your `WEBURL`
3. Download and extract the ZIP to see the folder name inside → this is your `DIRNAME` [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

**Execute:**

```bash
fab -H web01 -u devops web_setup:WEBURL=https://www.tooplate.com/zip-templates/2136_kool_form_pack.zip,DIRNAME=2136_kool_form_pack
```

Run the same command with `-H web02` to deploy on the second server. [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

**Verification:** Open a browser and navigate to the IP address of web01 or web02. The website template should be live. [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

🔍 **Deep Dive:** Notice the operational flow crosses the local/remote boundary multiple times: install locally → install remotely → download locally → repackage locally → transfer to remote → extract remotely → restart remotely. The `local()`/`run()`/`sudo()` and `lcd()`/`cd()` pairs are how Fabric cleanly handles this boundary crossing within a single function. [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

⚠️ **Expert Note:** The script assumes the local script box is Ubuntu/Debian (`apt install`) and the remote machines are CentOS/RPM-based (`yum install`). In a mixed environment, you'd need conditional logic or separate functions per OS family. [\[215-python-fabric \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/215-python-fabric.txt)

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

## System Architecture

```
SCRIPT BOX (local)
  ├── pip → installs Fabric
  ├── fabfile.py → defines all automation functions
  ├── fab CLI → discovers fabfile.py → exposes functions as commands
  └── SSH keys (~/.ssh/id_rsa) → authenticate to remote machines
        │
        ├──── [SSH] ──→ web01 (CentOS, devops user, sudoers+NOPASSWD)
        └──── [SSH] ──→ web02 (CentOS, devops user, sudoers+NOPASSWD)
```

## Core Method Map

| Method    | Executes On    | Privilege     | Purpose                  |
| --------- | -------------- | ------------- | ------------------------ |
| `local()` | Script box     | Current user  | Local shell commands     |
| `run()`   | Remote         | Normal user   | Remote non-root commands |
| `sudo()`  | Remote         | Root          | Remote root commands     |
| `put()`   | Local → Remote | Optional sudo | SCP file transfer        |
| `lcd()`   | Script box     | —             | Local directory context  |
| `cd()`    | Remote         | —             | Remote directory context |

## Key Relationships

```
fab CLI ──reads──→ fabfile.py ──contains──→ Python functions
fab -H ──specifies──→ target host
fab -u ──specifies──→ SSH user (or env.user default)
fab func:arg=val ──maps──→ function(arg=val)
```

## Remote Machine Setup Chain

```
useradd devops
  → passwd devops
    → visudo: devops NOPASSWD
      → sshd_config: PasswordAuthentication yes
        → systemctl restart sshd
          → [from script box] ssh-copy-id devops@host
            → key-based login enabled
              → Fabric can connect
```

## Web Deployment Flow (Local ↔ Remote Boundary)

```
LOCAL:  apt install zip unzip
REMOTE: sudo yum install httpd wget unzip
REMOTE: sudo systemctl start/enable httpd
LOCAL:  wget → download ZIP
LOCAL:  unzip → extract
LOCAL:  lcd(DIRNAME) → cd into extracted folder
LOCAL:  zip -r tooplate.zip * → repackage contents flat
LOCAL→REMOTE: put(tooplate.zip → /var/www/html/) [use_sudo]
REMOTE: cd(/var/www/html/) → unzip tooplate.zip
REMOTE: sudo systemctl restart httpd
✅ Website live at remote IP
```

## pip Ecosystem Pattern (Reusable)

```
pip install <library>
  → import <library>
    → authenticate (creds/keys/tokens)
      → get object/resource/client
        → call methods on object
```

Applies to: Fabric, python-jenkins, boto3, and any Python library.

## Security Boundaries

```
✅ Credentials in ~/.aws/credentials or env vars (external)
❌ Credentials in Python source code (exposed in repos)

✅ SSH key-based auth (no password in shell history)
❌ fab -p password (stored in bash history)
```

## Reusable Engineering Patterns

| Pattern                            | Instance in This Video                            |
| ---------------------------------- | ------------------------------------------------- |
| Convention over configuration      | `fabfile.py` auto-discovered by `fab`             |
| Bootstrap/self-detecting installer | `get-pip.py` detects OS + Python version          |
| Controller/worker                  | Script box (controller) → web01/web02 (workers)   |
| Local/remote boundary management   | `local()`/`lcd()` vs `run()`/`sudo()`/`cd()`      |
| One-time setup, repeated execution | User+sudo+SSH setup once → fab commands unlimited |
| Credential separation              | Keys/creds external to code                       |
| R\&D-heavy, execution-light        | Most time in understanding; script is small       |

## Rapid Recall Triggers

* **"How does Fabric work?"** → fabfile.py + fab CLI + SSH + local/run/sudo
* **"How to deploy a website with Fabric?"** → web\_setup: install → download → repackage → put → extract → restart
* **"lcd vs cd?"** → lcd = local directory context, cd = remote directory context
* **"Why NOPASSWD?"** → Non-interactive SSH session can't type sudo password
* **"Why repackage the ZIP?"** → Downloaded ZIP has a folder wrapper; web root needs flat content
* **"Why not put password in code?"** → Repository exposure risk; use external credential stores
