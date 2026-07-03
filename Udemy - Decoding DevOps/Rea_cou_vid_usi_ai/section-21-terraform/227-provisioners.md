# 🧠 Terraform Provisioners — Remote Execution & File Deployment on Infrastructure

**Source:** *227. Provisioners* — Terraform / Infrastructure as Code Series (Video Caption Reconstruction + Shell Script)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 The Problem: Infrastructure Is Created, But It's Empty

Terraform excels at creating infrastructure — EC2 instances, security groups, VPCs, key pairs. But when an EC2 instance launches, it's just a bare operating system. There's no web server installed, no application deployed, no configuration applied. The instance exists, but it doesn't *do* anything yet.

In many workflows, you need something to happen **right after** the instance is created: install packages, deploy an application, run a setup script. Terraform provides a mechanism for this called **provisioners** — blocks within a resource definition that execute actions (file transfers, remote commands) as part of the resource creation process. This lecture teaches how to use provisioners to push a shell script to a newly created EC2 instance and execute it, resulting in a fully configured web server with a deployed website.

***

## 1.2 Provisioners: What They Are and Their Fundamental Limitation

A provisioner in Terraform is a block you add **inside a resource definition** (like `aws_instance`) that performs actions beyond creating the resource itself. Terraform supports several provisioner types; this lecture covers two: **`file`** (copies files to the remote machine) and **`remote-exec`** (executes commands on the remote machine).

The most important conceptual point — emphasized right at the start of the Terraform documentation and by the instructor — is that **"Provisioners are a last resort."** This isn't a casual warning; it reflects a fundamental architectural limitation.

Terraform's core power is **state management**. It creates a resource, records its state, and can detect drift, plan changes, and destroy resources because it tracks their state. But provisioners operate **outside Terraform's state management boundary**. Terraform can execute a script for you, and it can detect whether the script execution itself passed or failed at the process level. But **what the script does** — whether Apache was actually installed correctly, whether the website files were copied to the right place, whether the service is actually running — Terraform cannot know. The *output* and *resulting state* of provisioned actions are invisible to Terraform.

This means: if you run `terraform apply`, the provisioner installs Apache and deploys a website. Later, someone SSHes into the instance and deletes the website files. Terraform has no way to detect this. `terraform plan` will show no changes, because from Terraform's perspective, the `aws_instance` resource hasn't changed — the provisioner's effects aren't tracked.

> 🔍 **Deep Dive:** This limitation is a consequence of Terraform's declarative model. Terraform declares *what* infrastructure should exist and tracks its state via provider APIs (e.g., AWS API for EC2 instances). But the internal state of a running OS — installed packages, file contents, running services — is not something the AWS API exposes. Terraform would need an agent inside the instance to track that, which is fundamentally a configuration management tool's job (Ansible, Chef, Puppet), not an infrastructure provisioning tool's job.

***

## 1.3 The Preferred Alternative: Pre-Built Images (AMIs + Packer)

The instructor presents the **recommended approach** before even showing provisioners: build a **pre-configured AMI** that already contains everything the instance needs. Instead of creating a bare instance and then running scripts on it, you create an image (AMI) in advance with all packages installed, all files deployed, all services configured. Then Terraform simply launches an instance from that AMI — no post-creation provisioning needed.

The tool for creating such images is **Packer**, which integrates well with Terraform. The workflow the instructor references: you write a Packer configuration that specifies a base image, a script to run (installing Apache, deploying the website), and the output AMI. Packer builds the image, you get an AMI ID, and you use that AMI ID in your Terraform code. The instance launches fully ready.

Why is this preferred? Because the AMI's contents are **baked in** — they're part of the image, not a post-launch action. Every instance launched from that AMI is identical and predictable. There's no risk of a provisioning script failing mid-execution and leaving the instance in a half-configured state. The documentation even links to a tutorial: "Provision infrastructure with Packer."

Despite this recommendation, the instructor proceeds with provisioners because *"when it comes to real time, there will be many times when you need to execute something on the instances when you're creating it."* Provisioners are a practical reality in many workflows.

***

## 1.4 The Two-Step Provisioning Model: Push Then Execute

The provisioner workflow for this lecture follows a clear two-step model:

**Step 1: File Provisioner** — Push the shell script (`web.sh`) from the local machine to the remote instance. This copies a file from a local source path to a destination path on the instance.

**Step 2: Remote-Exec Provisioner** — Execute commands on the remote instance via SSH. This runs the script that was just pushed, which installs Apache, downloads a website template, and deploys it.

Both provisioners live **inside** the `aws_instance` resource block — they are arguments/blocks within the resource, not separate resources. This is a critical structural point: provisioners are not standalone; they're attached to the lifecycle of the resource they belong to. They execute as part of creating that specific instance.

***

## 1.5 File Provisioner — Mechanics

The `file` provisioner copies a file from the machine running Terraform to the newly created instance. It has two key arguments:

* **`source`** — The local path of the file to copy (e.g., `web.sh`).
* **`destination`** — The remote path where the file should be placed (e.g., `/tmp/web.sh`).

The file provisioner relies on the **connection block** (covered next) to know how to reach the instance. It uses the SSH connection to transfer the file — essentially performing an SCP (secure copy) operation under the hood.

The destination `/tmp/web.sh` is chosen deliberately — the `/tmp` directory is world-writable, so the SSH user doesn't need elevated permissions to write there. The script will later be executed with `sudo` to get the privileges needed for package installation and service management.

***

## 1.6 Connection Block — How Terraform SSHes into the Instance

For both `file` and `remote-exec` provisioners to work, Terraform needs to establish an SSH connection to the instance. The **`connection` block** inside the resource provides all the SSH details:

**`type = "ssh"`** — Specifies the connection protocol. SSH is the standard for Linux instances.

**`user`** — The SSH username. For Ubuntu AMIs, this is `ubuntu` (the default user created by the AMI). The instructor stores this in a variable (`var.webuser`) rather than hardcoding it, following the Terraform variable pattern from earlier lectures.

**`private_key`** — The content of the private key used for SSH authentication. This is not the file *path* — it's the actual key *content*. To convert a file path to file content, Terraform provides the **`file()` function**. Writing `file("path/to/key.pem")` tells Terraform: "read this file and return its contents as a string." That string (the private key content) is then used for SSH authentication.

**`host = self.public_ip`** — The IP address to SSH into. `self.public_ip` is a **self-reference** — it refers to the public IP of the instance being created by this very resource block. At the time the provisioner runs, the instance already exists (it was just created), so its public IP is available. The `self` keyword lets the resource refer to its own attributes.

> 🔍 **Deep Dive:** The `self` reference is unique to provisioner contexts within Terraform. In normal resource arguments, you reference other resources by name (e.g., `aws_instance.my_server.public_ip`). But inside a provisioner block that belongs to a resource, `self` refers to that same resource — because the provisioner runs as part of the resource's own creation lifecycle, the resource needs a way to reference its own just-created attributes.

***

## 1.7 Security Group Requirement: Port 22 Must Be Open

For the SSH connection to work, the instance's **security group must allow inbound traffic on port 22** (SSH). The instructor explicitly warns about this: *"Make sure in the security group, 22 is allowed from anywhere, or update your public IP over there."*

Two options are presented:

1. Allow port 22 from **`0.0.0.0/0`** (anywhere) — simpler but less secure. Anyone on the internet can attempt SSH connections.
2. Allow port 22 from **your specific public IP** with a `/32` CIDR mask — more secure. Only your machine can SSH in. To find your IP: Google "what is my IPv4."

If port 22 isn't open, the provisioner will hang waiting for the SSH connection and eventually time out, failing the entire `terraform apply`.

***

## 1.8 Remote-Exec Provisioner — Command Execution

The `remote-exec` provisioner executes commands on the remote instance after the SSH connection is established. It uses an **`inline`** argument — a list of commands (Python list syntax: square brackets, comma-separated, each command in double quotes):

```hcl
inline = [
  "chmod +x /tmp/web.sh",
  "sudo /tmp/web.sh"
]
```

**Command 1: `chmod +x /tmp/web.sh`** — Grants execute permission to the script. Files copied via the `file` provisioner don't automatically have execute permission. Without this, attempting to run the script would fail with "Permission denied."

**Command 2: `sudo /tmp/web.sh`** — Executes the script with root privileges. `sudo` is required because the script runs `apt install` and `systemctl` commands that need root access. The path `/tmp/web.sh` is where the file provisioner placed the script.

The `-y` flag on `apt install` inside the script is critical — the instructor specifically warns: *"Make sure you have `-y` where you have the apt install command because the script should execute. This should not stop, otherwise the execution will fail."* Without `-y`, `apt` would prompt for confirmation interactively, but there's no human at the terminal during automated provisioning. The command would hang indefinitely waiting for input, and eventually the provisioner would fail.

***

## 1.9 The Shell Script: web.sh — What Gets Executed

The script that gets pushed and executed is a standard web server deployment script (referenced from the companion file `web.sh`):

```bash
#!/bin/bash
apt update
apt install wget unzip apache2 -y
systemctl start apache2
systemctl enable apache2
wget https://www.tooplate.com/zip-templates/2117_infinite_loop.zip
unzip -o 2117_infinite_loop.zip
cp -r 2117_infinite_loop/* /var/www/html/
systemctl restart apache2
```

This script: updates package lists, installs Apache2 (plus wget and unzip as utilities), starts and enables Apache, downloads a website template from tooplate.com, extracts it, copies the files to Apache's document root (`/var/www/html/`), and restarts Apache to serve the new content. The instructor notes this is familiar from earlier Bash scripting lectures — nothing new in the script itself.

***

## 1.10 The Terraform Workflow Commands and Their Role

The lecture follows the standard Terraform workflow, which the instructor runs through quickly because the project is copied from a previous exercise:

**`terraform init`** — Initializes the working directory, downloads providers. Completes quickly here because provider files already exist from the copied Exercise3.

**`terraform fmt`** — Formats all `.tf` files to canonical style. A quality check.

**`terraform validate`** — Validates the syntax and internal consistency of the configuration. Catches errors like mismatched variable names before any infrastructure is touched.

**`terraform plan`** — Shows what Terraform will create/change/destroy. For a new setup (previous infrastructure was destroyed), this shows a completely new set of resources.

**`terraform apply`** — Executes the plan. Creates the instance, then runs the provisioners (file push, then remote-exec). The instructor notes you can see the `remote-exec` output during apply — the script's stdout appears in the terminal.

**`terraform destroy`** — Tears down all managed infrastructure when done.

> ⚠️ **Expert Note:** The instructor reiterates the state limitation after the successful deployment: *"The Terraform cannot maintain the state of your website. For that, you need to use a separate tool or you need to be sure that you're deploying it from an AMI where everything works fine."* This is the final conceptual anchor: provisioners get the job done, but they create an untracked state. For production reliability, prefer pre-built images or configuration management tools.

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building and Why

We are using **Terraform provisioners** to create an EC2 instance that automatically becomes a fully functional web server with a deployed website — all in a single `terraform apply`. A shell script is pushed to the instance and executed remotely, installing Apache2 and deploying a website template. No manual SSH required after creation.

**Final outcome:** An EC2 instance running Apache2, serving a website template from tooplate.com, accessible via the instance's public IP in a browser — all provisioned automatically through Terraform.

***

## Step 1: Create the Exercise4 Directory by Copying Exercise3

The project structure builds on the previous exercise. Copy the **Exercise3** directory and rename the copy to **Exercise4**.

```
Copy Exercise3 → Paste → Rename to Exercise4
```

**Why copy:** Exercise4 needs the same provider configuration, variables, and base resource definitions. Copying saves time and ensures consistency. `terraform init` will complete quickly because the provider plugins already exist.

**Connection to flow:** This gives us the base Terraform files (`instance.tf`, `vars.tf`, provider config, key files) to build upon.

***

## Step 2: Create the Shell Script — `web.sh`

Inside the Exercise4 folder, right-click → **New File** → name it `web.sh`.

Enter the following content (also available from lecture resources):

```bash
#!/bin/bash
apt update
apt install wget unzip apache2 -y
systemctl start apache2
systemctl enable apache2
wget https://www.tooplate.com/zip-templates/2117_infinite_loop.zip
unzip -o 2117_infinite_loop.zip
cp -r 2117_infinite_loop/* /var/www/html/
systemctl restart apache2
```

**Line-by-line breakdown:**

* `#!/bin/bash` — Shebang line: tells the OS to use Bash to interpret this script.
* `apt update` — Refreshes the package index so `apt install` knows the latest available packages.
* `apt install wget unzip apache2 -y` — Installs three packages. **`-y`** is critical — it auto-confirms the installation prompt. Without it, the script hangs waiting for user input during automated execution, and the provisioner fails.
* `systemctl start apache2` — Starts the Apache web server immediately.
* `systemctl enable apache2` — Enables Apache to start automatically on boot.
* `wget https://...2117_infinite_loop.zip` — Downloads the website template archive.
* `unzip -o 2117_infinite_loop.zip` — Extracts the archive. `-o` overwrites existing files without prompting.
* `cp -r 2117_infinite_loop/* /var/www/html/` — Copies extracted website files to Apache's document root. `-r` for recursive copy.
* `systemctl restart apache2` — Restarts Apache to ensure it serves the new content.

**Save the file.**

***

## Step 3: Add the Webuser Variable — `vars.tf`

Open the `vars.tf` file **in the Exercise4 folder** (make sure you're editing the right folder's file).

Add a new variable:

```hcl
variable "webuser" {
  default = "ubuntu"
}
```

**Why `ubuntu`:** The EC2 instance uses an Ubuntu AMI, and the default SSH username for Ubuntu AMIs is `ubuntu`. This variable will be referenced in the connection block for SSH access.

**Save the file.**

***

## Step 4: Add Provisioner Blocks to `instance.tf`

Open `instance.tf` in the Exercise4 folder. Inside the `aws_instance` resource block, **after the tags block**, add the following three blocks:

### 4a: Connection Block

```hcl
connection {
  type        = "ssh"
  user        = var.webuser
  private_key = file("path/to/your-key.pem")
  host        = self.public_ip
}
```

**Breakdown:**

* `type = "ssh"` — Connection protocol. SSH for Linux instances.
* `user = var.webuser` — References the variable defined in Step 3 (`ubuntu`).
* `private_key = file("path/to/your-key.pem")` — The `file()` function reads the private key file and returns its **content** as a string. The private key file should already exist in your source code from previous exercises. Replace the path with your actual key file path.
* `host = self.public_ip` — `self` references the instance being created by this resource block. `.public_ip` gets its public IP address after creation.

### 4b: File Provisioner

```hcl
provisioner "file" {
  source      = "web.sh"
  destination = "/tmp/web.sh"
}
```

**Breakdown:**

* `provisioner "file"` — Declares a file provisioner block. Not a separate resource — it's **inside** the `aws_instance` block.
* `source = "web.sh"` — Local file to copy (the script created in Step 2).
* `destination = "/tmp/web.sh"` — Remote path on the instance. `/tmp` is used because it's world-writable — no elevated permissions needed to write there.

### 4c: Remote-Exec Provisioner

```hcl
provisioner "remote-exec" {
  inline = [
    "chmod +x /tmp/web.sh",
    "sudo /tmp/web.sh"
  ]
}
```

**Breakdown:**

* `provisioner "remote-exec"` — Declares a remote execution provisioner.
* `inline = [...]` — A list of commands to execute in order (Python list syntax: square brackets, comma-separated, double-quoted strings).
* `"chmod +x /tmp/web.sh"` — Grants execute permission to the script file. Without this, execution would fail with "Permission denied."
* `"sudo /tmp/web.sh"` — Runs the script with root privileges. `sudo` is needed because `apt install` and `systemctl` require root.

**Save `instance.tf`.**

***

## Step 5: Verify Security Group — Port 22 Open

Before applying, confirm that your security group allows **inbound SSH (port 22)**. Check the security group resource in your Terraform config.

Two options:

| Approach              | CIDR                  | Security Level                                        |
| --------------------- | --------------------- | ----------------------------------------------------- |
| Open to all           | `0.0.0.0/0`           | Less secure, simpler                                  |
| Restricted to your IP | `<your-public-ip>/32` | More secure; Google "what is my IPv4" to find your IP |

If port 22 is not open, the provisioner's SSH connection will **time out** and `terraform apply` will fail.

Also verify **port 80 (HTTP)** is open — needed to access the website after deployment.

***

## Step 6: Run the Terraform Workflow

Open **Git Bash** (or terminal, or VS Code terminal). Navigate to Exercise4:

```bash
cd Exercise4
```

### 6a: Initialize

```bash
terraform init
```

**Expected:** Quick completion (providers already present from copied Exercise3).

### 6b: Format

```bash
terraform fmt
```

**Expected:** Lists any files that were reformatted, or no output if already formatted.

### 6c: Validate

```bash
terraform validate
```

**Expected:** `Success! The configuration is valid.`

**If validation fails:** Check for mismatched variable names (e.g., defining `webuser` in `vars.tf` but referencing `var.web_user` in `instance.tf`).

### 6d: Plan

```bash
terraform plan
```

**Expected:** Shows the full plan for creating all resources (this is a completely new setup — the instructor destroyed everything from the previous lecture).

### 6e: Apply

```bash
terraform apply
```

Confirm with `yes` when prompted.

**What to observe during apply:** You will see the `remote-exec` provisioner output in your terminal — the stdout from the script execution (apt output, download progress, etc.). This is live output from the remote instance being provisioned.

**Expected final output:** `Apply complete!` with resources created.

**If apply hangs on the provisioner:**

* SSH timeout → port 22 not open in security group, or wrong key file
* Script hangs → missing `-y` flag on `apt install`
* Connection refused → instance not yet in running state (rare, Terraform usually waits)

***

## Step 7: Verify the Deployment

### 7a: Check in AWS Console

Go to **EC2 → Instances** in the correct region (North Virginia for this project). Verify:

* Instance is in **Running** state.
* Check the **security group inbound rules**: port 80 (HTTP) and port 22 (SSH) should be open.

### 7b: Access the Website

Copy the instance's **public IP** from the EC2 console. Paste it into a browser:

```
http://<instance-public-ip>
```

**Expected:** The tooplate "Infinite Loop" website template loads in the browser.

**If the website doesn't load:**

* Wait 2–3 minutes — the instance state may still be initializing.
* Verify port 80 is open in the security group.
* Verify the script executed successfully (check the `terraform apply` output for errors).

***

## Step 8: Clean Up — Destroy Infrastructure

When finished:

```bash
terraform destroy
```

Confirm with `yes`. This removes all resources created by Terraform.

> ⚠️ **Expert Note:** Remember the core limitation: after `terraform apply`, Terraform does not track the website state. If someone deletes website files on the instance, `terraform plan` shows no changes. For production: use pre-built AMIs (Packer) or configuration management tools (Ansible) for state-aware deployments. Provisioners are for quick, pragmatic, "get it running" scenarios.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Provisioner Architecture Within Terraform

```
aws_instance resource block
  ├── (normal args: ami, instance_type, key, tags, sg...)
  │
  ├── connection {                    ← HOW to reach the instance
  │     type        = "ssh"
  │     user        = var.webuser     ("ubuntu")
  │     private_key = file("key.pem") ← file() reads content
  │     host        = self.public_ip  ← self-reference to this instance
  │   }
  │
  ├── provisioner "file" {            ← STEP 1: push script
  │     source      = "web.sh"
  │     destination = "/tmp/web.sh"
  │   }
  │
  └── provisioner "remote-exec" {     ← STEP 2: execute script
        inline = [
          "chmod +x /tmp/web.sh",     ← make executable
          "sudo /tmp/web.sh"          ← run with root
        ]
      }

KEY: provisioners are INSIDE the resource block, NOT separate resources
```

***

## Execution Flow

```
terraform apply
  │
  ├── 1. Create EC2 instance (aws_instance)
  │       → instance gets public IP
  │
  ├── 2. Establish SSH connection
  │       → type: ssh
  │       → user: ubuntu (var.webuser)
  │       → key: file() reads private key content
  │       → host: self.public_ip
  │       → REQUIRES: port 22 open in security group
  │
  ├── 3. File provisioner: SCP web.sh → /tmp/web.sh
  │
  ├── 4. Remote-exec provisioner:
  │       → chmod +x /tmp/web.sh
  │       → sudo /tmp/web.sh
  │           ├── apt update
  │           ├── apt install wget unzip apache2 -y
  │           ├── systemctl start/enable apache2
  │           ├── wget template zip
  │           ├── unzip → cp to /var/www/html/
  │           └── systemctl restart apache2
  │
  └── 5. Apply complete → website accessible on public IP:80
```

***

## The Core Limitation (Most Important Concept)

```
Terraform CAN:
  ✅ Create infrastructure (EC2, SG, etc.)
  ✅ Execute provisioner scripts
  ✅ Detect script pass/fail at process level

Terraform CANNOT:
  ❌ Track what the script DID (installed packages, deployed files)
  ❌ Detect drift in provisioned state (someone deletes website files)
  ❌ Re-provision on drift (terraform plan shows no changes)

CONSEQUENCE:
  Provisioner effects are OUTSIDE Terraform's state boundary
  "Provisioners are a last resort"
```

***

## Preferred Alternative: Pre-Built Images

```
RECOMMENDED PATH:
  Packer → builds AMI with all software pre-installed
  Terraform → launches instance from that AMI
  RESULT: no post-creation provisioning needed; state is baked into image

PROVISIONER PATH (this lecture):
  Terraform → creates bare instance → pushes script → executes script
  RESULT: works but state is untracked after creation
```

***

## Prerequisite Checklist

```
Security Group:
  ✅ Port 22 (SSH) — open to your IP or 0.0.0.0/0
  ✅ Port 80 (HTTP) — open to 0.0.0.0/0 (for website access)

Script:
  ✅ -y flag on apt install (prevents interactive hang)
  ✅ Saved in Exercise4 directory as web.sh

Variables:
  ✅ webuser = "ubuntu" in vars.tf (Exercise4 folder)

Key file:
  ✅ Private key file accessible from Terraform working directory
```

***

## Key Terraform Constructs Introduced

```
file()              → function: reads file content, returns string
                       USE: private_key = file("key.pem")

self.public_ip      → self-reference to the resource's own attribute
                       USE: host = self.public_ip (inside provisioner)

provisioner "file"  → copies local file to remote instance
                       args: source, destination

provisioner "remote-exec" → executes commands on remote instance
                       args: inline = ["cmd1", "cmd2"]

connection { }      → SSH details for provisioners
                       args: type, user, private_key, host
```

***

## Terraform Workflow (This Lecture)

```
cd Exercise4
terraform init        → quick (copied from Exercise3)
terraform fmt         → format check
terraform validate    → syntax/variable validation
terraform plan        → review what will be created
terraform apply       → create + provision (observe remote-exec output)
→ verify: browser → http://<public-ip> → website loads
terraform destroy     → clean up
```

***

## Failure Signature Index

```
SSH timeout during provisioner         → port 22 not open in SG, or wrong key
Script hangs during remote-exec        → missing -y on apt install
Permission denied running script       → missing chmod +x before execution
Website not loading in browser         → port 80 not open, or instance still initializing
terraform validate fails               → variable name mismatch between vars.tf and instance.tf
"file not found" on file provisioner   → web.sh not in Exercise4 directory, or wrong source path
```

***

## Reusable Engineering Pattern: Managed Creation + Unmanaged Configuration

```
PATTERN:
  Tool A creates the resource        (Terraform → EC2 instance)
  Tool A pushes config to resource   (provisioner → file + remote-exec)
  Tool A CANNOT track config state   (state boundary ends at resource creation)

IMPLICATION:
  Resource lifecycle = managed
  Configuration lifecycle = unmanaged (by this tool)

SOLUTIONS:
  1. Bake config into image (Packer → AMI) → eliminates post-creation config
  2. Use config management tool (Ansible/Chef) → manages config state separately
  3. Accept the limitation (provisioners) → for quick/dev/learning scenarios

WHERE ELSE:
  • Docker: Dockerfile bakes config into image (preferred) vs. exec into container (escape hatch)
  • Kubernetes: init containers run setup → but K8s doesn't track what they did
  • Cloud-init: user data scripts → cloud provider doesn't track their output
```

***

## One-Line Mental Reload Trigger

> *"Provisioners are a last resort — file pushes script, remote-exec runs it via SSH (connection: self.public\_ip, file() for key, port 22 open), but Terraform can't track what the script does — prefer pre-built AMIs with Packer."*

This single sentence reconstructs the full provisioner architecture, both provisioner types, the connection mechanism, the security prerequisite, the execution model, the fundamental state limitation, and the recommended alternative. [\[227-provisioners \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/227-provisioners.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/227.web.sh)
