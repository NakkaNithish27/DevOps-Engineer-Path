# 🎓 Deep Learning Material: AWS Systems Manager (SSM) & CloudShell — Centralized Infrastructure Control from the Browser

*Reconstructed from video lecture captions (117. SSM & CloudShell Intro.txt)*

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 AWS Systems Manager: What It Is and What Problem It Solves

AWS Systems Manager (SSM) is a **centralized operations management service** that lets you manage your EC2 instances (and other nodes) **at scale** without needing to SSH into each one individually. The instructor frames it clearly: *"You can manage many nodes at scale when it comes to operations or system administration."* [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

The core problem it solves is operational scale. Consider the scenario the instructor describes: *"Imagine you are managing hundreds of EC2 instances, and you need to execute one command on your hundreds of instances, like restarting a service or running a patch."*  Without SSM, you'd need to SSH into each instance one by one, run the command, exit, move to the next — an impossibly tedious and error-prone process at scale. SSM eliminates this by providing a **centralized control plane** from which you can reach any managed instance (or group of instances) through the AWS console, without ever opening an SSH client. [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

SSM provides two key capabilities demonstrated in this lecture: [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

1. **Session Manager** — Get a shell session to an individual EC2 instance directly from the AWS console, without SSH keys, without SSH tools, and without configuring security group inbound rules for SSH.
2. **Run Command** — Execute commands on one or many instances simultaneously from the console, with output captured and displayed centrally.

Beyond these, the instructor briefly mentions additional SSM capabilities: **compliance management, change management, parameter store** (for storing variables/secrets), **operations center, incident management**, and integration with CloudWatch. He describes SSM as *"an amazing tool for system administrator or operations to manage the entire operation of your fleet of servers."* [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

🔍 **Deep Dive:**
The architecture of SSM communication is the reverse of traditional SSH. In traditional SSH, **you connect to the instance** — your machine initiates an inbound connection to port 22 on the EC2 instance, which requires the security group to allow inbound SSH traffic and requires you to have the private key. With SSM, **the EC2 instance connects outbound to the SSM service**. The instructor states this explicitly: *"When we want to connect EC2 instance from SSM, in that case actually EC2 instance connects to the SSM service."*  This is a fundamental architectural inversion — the instance reaches out to AWS, not the other way around. This means you don't need to open inbound SSH ports in the security group, and you don't need SSH keys for this access path. [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

***

## 1.2 IAM Roles: Service-to-Service Permission Mechanism

For SSM to work, the EC2 instance needs **permission** to connect to the SSM service. This introduces a critical IAM concept: **roles**. [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

The instructor distinguishes roles from user permissions with a clear question: *"We have already seen if we can create user and assign permission to the user. But what if one service wants to connect to another service? So EC2 wants to connect to SSM. In that case we use roles."* [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

This is a fundamental AWS authorization concept:

* **IAM Users** = permissions for **humans** (or external systems) accessing AWS
* **IAM Roles** = permissions for **AWS services** accessing other AWS services

An IAM Role is a set of permissions that you **attach to a service** (in this case, an EC2 instance) so that the service can act on your behalf. When you attach a role with SSM permissions to an EC2 instance, the instance can communicate with the SSM service using temporary credentials automatically managed by AWS. You don't configure any credentials on the instance — the role handles it. [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

The specific permission needed is the **AmazonSSMManagedInstanceCore** policy. This is a managed (pre-built by AWS) policy that grants the minimum permissions an EC2 instance needs to be managed by Systems Manager — registering as a managed node, receiving commands, sending status updates, and establishing sessions. [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

⚠️ **Expert Note:**
The IAM Role architecture solves a significant security problem. Without roles, you'd need to embed AWS access keys (long-lived credentials) directly on the EC2 instance, which is a security anti-pattern — keys can be leaked, stolen, or forgotten. Roles use **temporary, automatically rotated credentials** that the EC2 instance retrieves from the instance metadata service. No static secrets are ever stored on the instance. This is why IAM Roles are the recommended way for service-to-service communication in AWS.

***

## 1.3 Session Manager: Shell Access Without SSH

Session Manager is the SSM feature that gives you an **interactive shell session** to an EC2 instance directly through the AWS console's web browser. [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

The instructor emphasizes what you **don't need** when using Session Manager instead of traditional SSH: [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

* **No SSH keys** — You don't need to create, download, or manage key pairs
* **No SSH tools** — No git bash, no terminal SSH client, no PuTTY
* **No security group changes** — You don't need to open port 22 inbound

The instructor makes this point emphatically: *"So this way you don't need to manually connect or do SSH. You don't need keys. You don't need to work on the security groups."* [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

The workflow is: attach the IAM role → go to Session Manager → select instance → start session → get a shell. Once inside, you can execute any command just as you would in a normal SSH session (the instructor demonstrates `sudo -i` to switch to root and checking the OS). [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

The instructor also provides a recommended operational pattern: *"You can have an IAM role ready as soon as you launch the instance. You make sure you attach that IAM role and then you can connect it like this."*  This means the IAM role should be part of your standard instance launch process, not an afterthought. [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

🔍 **Deep Dive:**
There's a timing consideration: after attaching the IAM role, the instance may not appear immediately in Session Manager's instance list. The instructor notes: *"It might take some time for the instance to show up over here. So if it doesn't show your instance, cancel it. Wait for some time. Also check if your IAM role is correctly attached and then you can try again."*   This delay happens because the SSM agent on the instance needs to register with the SSM service after the role is attached. The agent periodically checks for credentials and registers — this isn't instantaneous. [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

***

## 1.4 Run Command: Executing at Scale

Run Command is the SSM feature that lets you execute commands on **one or many instances simultaneously** without opening individual shell sessions. [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

The mechanism works through **command documents**. A command document defines what type of operation to run. The instructor shows a list of available documents and notes that most won't make sense yet — some relate to Ansible playbooks, CloudWatch, Docker, and other services that will be covered later. For running shell commands, the document is **AWS-RunShellScript**. [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

Once you select the document, you specify: [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

1. **The commands** to execute — you type them directly, or you can paste an entire shell script
2. **The working directory** (optional) — where the commands should run
3. **The target instances** — selected by one of three methods:
   * **Manual selection** — pick specific instances from a list
   * **Tags** — target all instances with a specific tag (e.g., project = DevOps). The instructor explains: *"Let's say you want to execute something on project DevOps. You need to make sure that all the instances are tagged like that properly with this tag, and then you can give the tag and its value and it will execute it on the instances that has this tag. It could be one or many."* [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)
   * **Resource groups** — target a pre-defined group of instances

After execution, the output is displayed centrally. There's an **output section** for standard output and an **error section** for errors. You can also store output in **S3 buckets** or **CloudWatch Logs** for persistence and analysis (these options are available but will be understood better after learning those services). [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

The status of each execution is tracked — the instructor sees "in progress" then "success" after refreshing. [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

⚠️ **Expert Note:**
Tag-based targeting is where Run Command becomes truly powerful at scale. In a well-tagged infrastructure, you can execute a patch across all production web servers by targeting `Environment=Production, Role=WebServer` — without knowing the specific instance IDs. This requires **tagging discipline** as a prerequisite. If instances aren't tagged consistently, tag-based targeting becomes unreliable. Tagging is not just organizational — it's an operational control mechanism.

***

## 1.5 Other SSM Capabilities (Mentioned, Not Demonstrated)

The instructor briefly identifies additional SSM features that exist beyond Session Manager and Run Command: [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

* **Compliance** — Track and enforce compliance across managed instances
* **Change Management** — Manage operational changes (described as "very essential for system administrators")
* **Parameter Store** — Store variables, configuration data, and secrets (the instructor says "we're going to use this service" in a later project)
* **Operations Center** — Centralized view of operational issues
* **Incident Management** — Handle and track incidents

These are mentioned to establish that SSM is not just a shell access tool — it's a **comprehensive operations platform**. [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

***

## 1.6 AWS CloudShell: Browser-Based AWS CLI

CloudShell is a **browser-based command-line environment** that comes pre-installed with the AWS CLI and is automatically authenticated with your current console login credentials. [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

The instructor contrasts it with the traditional AWS CLI setup: *"We have seen in AWS CLI, if you want to execute AWS commands, first we need to install AWS CLI, and then we need to set up the access key. And then we can execute the command. With CloudShell, you can do it all from here."* [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

With CloudShell:

* **No installation needed** — AWS CLI is pre-installed
* **No access key setup** — You're authenticated with your console user's permissions
* **Immediate use** — Open it and start typing AWS commands

The instructor demonstrates running `aws ec2 describe-instances` (lists EC2 instance details in JSON) and `aws s3 ls` (lists S3 buckets) directly from CloudShell without any configuration. [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

CloudShell can be opened in the same tab or in a **separate tab** for a dedicated CLI workspace. [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

***

## 1.7 The Browser-Based Management Ecosystem

The instructor closes with an important architectural observation about the tools available within a single AWS console login: [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

*"In one AWS cloud login you get here CloudShell, Systems Manager, Amazon Q Developer as an AI assistant. So you can manage everything from the browser."*

**Amazon Q Developer Chat** is briefly introduced as an AI assistant available in the console. If you need a command you don't know, you can ask it, get the command, and execute it directly in CloudShell. [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

The instructor's guidance on when to use which tool: *"Which to use when totally depends on your requirement. I have used all of them for different different requirement and use cases. The point is, as a DevOps, you should know about these tools so you can use them whenever it's required."* [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are launching an EC2 instance and connecting to it through **AWS Systems Manager Session Manager** (without SSH), then running commands on it via **Run Command**, and finally exploring **CloudShell** for browser-based AWS CLI access. The final outcome: managing an instance entirely from the browser — no SSH, no keys, no local tools. [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

***

## Phase 1: Launch the EC2 Instance

### Step 1: Navigate to EC2 and Launch an Instance

Go to the EC2 service in the AWS console → click **Launch Instance**. [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

**Configuration choices:**

| Setting            | Value                                 | Reasoning                                                               |
| ------------------ | ------------------------------------- | ----------------------------------------------------------------------- |
| **Name**           | `server one`                          | Simple identifier                                                       |
| **AMI**            | Ubuntu Server 24 (Free Tier eligible) | The instructor selects Ubuntu                                           |
| **Instance Type**  | t2.micro or t3.micro                  | Whichever is Free Tier eligible in your region                          |
| **Key Pair**       | Select existing or create new         | **Doesn't matter** — we won't use it for login; we're using SSM instead |
| **Security Group** | Select existing                       | The instructor selects an existing one                                  |

Click **Launch Instance**. [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

**Key point about the key pair:** The instructor explicitly says: *"Keep your login. You can select the existing key or create a new key. It doesn't matter because we are not going to use key to login. We are going to do it through SSM."*  The key pair is still selected (AWS may require it), but it won't be used for access. [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

**Connection to flow:** The instance is now running, but it cannot yet communicate with SSM. It needs an IAM role with the right permissions.

***

## Phase 2: Create and Attach the IAM Role

### Step 2: Navigate to IAM and Create a Role

Go to the **IAM** service → click **Roles** → click **Create Role**. [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

**Configuration:**

1. **Trusted entity type:** Select **AWS service**
2. **Use case:** Select **EC2** — this means the role is designed to be assumed by EC2 instances
3. Click **Next**

### Step 3: Attach the Permission Policy

On the permissions page, search for the policy: [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

```
SSM managed instance
```

**What to look for:** The policy named **AmazonSSMManagedInstanceCore** — the instructor says: *"Also, you can find it the one that ends with core."* [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

Select this policy and click **Next**.

### Step 4: Name and Create the Role

* **Role name:** `SSM-managed-instance-core` (or any descriptive name)
* **Description:** Same or similar — the instructor uses the same text [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

Scroll down and click **Create Role**.

**Verification:** You should see a success message confirming the role was created.

### Step 5: Attach the Role to the EC2 Instance

Navigate back to **EC2** → select your instance → click **Actions** → **Security** → **Modify IAM role**. [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

From the dropdown, select the role you just created. Click **Update IAM role**. [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

**Verification:** The IAM role should now appear in the instance's details.

**Common mistake:** Forgetting to attach the role after creating it. The role must be explicitly attached to the instance — creating it alone does nothing.

**Connection to flow:** The instance now has permission to communicate with SSM. The SSM agent on the instance will use this role's credentials to register itself as a managed node.

***

## Phase 3: Access the Instance via Session Manager

### Step 6: Open Session Manager

Navigate to **AWS Systems Manager** service (search for it in the console) → in the left sidebar, click **Session Manager** → click **Start session**. [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

**Important timing note:** The instance may not appear in the list immediately. The instructor warns: *"It might take some time for the instance to show up over here. So if it doesn't show your instance, cancel it. Wait for some time. Also check if your IAM role is correctly attached and then you can try again."* [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

**Troubleshooting if instance doesn't appear:**

1. Verify the IAM role is correctly attached (check in EC2 instance details)
2. Wait 2-5 minutes for the SSM agent to register
3. Ensure the instance is in a **running** state
4. Try canceling and clicking "Start session" again

### Step 7: Start the Session

1. Optionally enter a **reason** (e.g., "shell access") — this is for auditing purposes [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)
2. **Select your instance** from the list
3. Click **Next** → **Next** → **Start Session** [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

**What happens:** A new tab opens with a terminal/shell session connected to your instance. [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

### Step 8: Use the Shell

You now have a working shell. Test it: [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

```bash
sudo -i
```

This switches to the root user. You can now check the OS, run any commands, perform any administration tasks — exactly as if you had SSH'd in. [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

**What you did NOT need:**

* No SSH key
* No SSH client (git bash, terminal, PuTTY)
* No security group rule for port 22

**When done:** Close the session (close the tab or type `exit`). [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

***

## Phase 4: Execute Commands via Run Command

### Step 9: Navigate to Run Command

Go back to **AWS Systems Manager** → in the left sidebar, click **Run Command** → click **Run command**. [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

### Step 10: Select the Command Document

You'll see a list of command documents. Search for: [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

```
run shell script
```

Select **AWS-RunShellScript** from the results. [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

**What this document does:** It tells SSM that you want to run raw shell commands on the target instance(s).

### Step 11: Enter Your Commands

Scroll down to the **Command parameters** section. In the commands field, type the commands you want to execute: [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

```bash
ls -l /var/log
tree -m
apt update output
sudo apt update
```

(The instructor enters a list of sample commands to demonstrate the feature.) [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

**You can also:** Paste an entire shell script into this field.

**Optional:** Specify a **working directory** where the commands should execute.

### Step 12: Select Target Instances

Scroll down to the **Target selection** section. Three options: [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

1. **Specify instance tags** — Enter a tag key/value pair (e.g., `Project = DevOps`). All instances with this tag will be targeted. Requires instances to be properly tagged.
2. **Choose a resource group** — Select a pre-defined group of instances
3. **Choose instances manually** — Select specific instances from a list

The instructor selects the instance manually since there's only one. [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

**Additional options (mentioned, explored later):**

* Store output in an **S3 bucket**
* Store output in **CloudWatch Logs**

### Step 13: Run and Check Output

Click **Run**. [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

**What you'll see:**

* Status changes from **In progress** to **Success** (refresh if needed)
* The instance ID is shown with its status

Click on the instance ID → **View output**: [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

* **Output section** — Shows standard output (stdout) from the commands
* **Error section** — Shows any errors (stderr) from the commands

**Verification:** The output should match what you'd expect from running those commands directly on the instance. [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

***

## Phase 5: Explore CloudShell

### Step 14: Open CloudShell

In the AWS console, click the **CloudShell** icon (usually in the top navigation bar or bottom of the screen). [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

A terminal opens directly in your browser. No setup required. [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

### Step 15: Run AWS CLI Commands

Test with: [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

```bash
aws ec2 describe-instances
```

**Breakdown:**

* `aws` — The AWS CLI tool (pre-installed in CloudShell)
* `ec2` — The service to interact with
* `describe-instances` — The API action (lists all EC2 instances)

**Expected output:** JSON-formatted data about your EC2 instances. [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

```bash
aws s3 ls
```

**Breakdown:**

* `aws s3 ls` — Lists all S3 buckets in your account

**Expected output:** List of your S3 buckets (if any exist). [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

**What you did NOT need:**

* No AWS CLI installation
* No access key configuration
* No `aws configure` setup

CloudShell inherits the permissions of your console login user. [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

**Optional:** Open CloudShell in a **separate tab** for a dedicated CLI workspace. [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

**Additional tool:** If you need a command you don't know, open **Amazon Q Developer Chat** in the console, ask your question, get the command, and execute it in CloudShell. [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

***

## Phase 6: Cleanup

### Step 16: Terminate the EC2 Instance

The instructor explicitly says: *"Once you are done, then delete your EC2 instance."* [\[117. SSM &...hell Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/117.%20SSM%20%26%20CloudShell%20Intro.txt)

Go to EC2 → select your instance → Instance State → **Terminate instance**.

**Why:** The instance costs money (even on free tier, you have limited hours). Always clean up after labs.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## SSM Core Identity

```
AWS Systems Manager = Centralized operations control plane for EC2 fleet
Problem: Managing hundreds of instances manually (SSH one-by-one) is impossible
Solution: Central console → shell access + command execution at scale
```

***

## SSM Architecture (Connection Direction)

```
Traditional SSH:
  [Your machine] ──inbound──→ [EC2 port 22]
  Requires: SSH key + security group rule + SSH client

SSM Session Manager:
  [EC2 instance] ──outbound──→ [SSM Service] ←── [AWS Console/You]
  Requires: IAM Role on EC2 (AmazonSSMManagedInstanceCore)
  Does NOT require: SSH keys, SSH tools, security group port 22

Key insight: CONNECTION IS REVERSED — instance connects out, not you connecting in
```

***

## IAM Role Mechanism

```
Human → AWS service:  IAM User (credentials)
Service → Service:    IAM Role (temporary credentials, auto-managed)

EC2 → SSM requires:
  1. Create IAM Role (trusted entity = EC2)
  2. Attach policy: AmazonSSMManagedInstanceCore
  3. Attach role to EC2 instance (Actions → Security → Modify IAM role)

Role = permission wrapper for a service, not a person
```

***

## Two Core SSM Features

```
SESSION MANAGER                      RUN COMMAND
─────────────────────────────────    ──────────────────────────────────
Interactive shell to ONE instance    Execute commands on ONE or MANY
Browser-based terminal               No shell session needed
Like SSH but without keys/ports      Results displayed centrally
Manual exploration & admin           Automation & scale operations

Session Manager → single-instance interactive
Run Command → multi-instance batch execution
```

***

## Run Command Targeting

```
HOW TO SELECT TARGETS:
  ├── Manual: Pick specific instance IDs from list
  ├── Tags:   Key=Value (e.g., Project=DevOps) → all matching instances
  └── Resource Group: Pre-defined group of instances

Tag-based targeting = the scale mechanism
  Prerequisite: Instances must be tagged consistently
  
Command Document: AWS-RunShellScript (for shell commands)
Output: stdout → Output section | stderr → Error section
Optional: Store in S3 bucket or CloudWatch Logs
```

***

## CloudShell Identity

```
CloudShell = Browser-based AWS CLI terminal

Traditional AWS CLI:
  Install CLI → aws configure → set access key/secret → run commands

CloudShell:
  Open in console → run commands immediately
  ├── AWS CLI pre-installed
  ├── Authenticated with your console login permissions
  └── No setup, no keys, no configuration

Can open in same tab or separate tab
```

***

## Browser-Based Management Ecosystem

```
Single AWS Console Login gives you:
  ├── Session Manager  → Shell access to instances (no SSH)
  ├── Run Command      → Batch execution across fleet
  ├── CloudShell       → AWS CLI without setup
  └── Amazon Q Dev     → AI assistant for commands you don't know

All from browser. No local tools needed.
"Which to use when depends on your requirement"
```

***

## Operational Flow (Complete)

```
── LAUNCH ──
EC2 → Launch Instance (Ubuntu, t2/t3.micro, any key pair, any SG)

── PERMISSIONS ──
IAM → Roles → Create Role
  → AWS Service → EC2
  → Policy: AmazonSSMManagedInstanceCore
  → Name & Create
EC2 → Select instance → Actions → Security → Modify IAM Role → Attach

── SESSION ACCESS ──
SSM → Session Manager → Start Session
  → Wait for instance to appear (may take minutes)
  → Select instance → Next → Next → Start Session
  → Shell opens in new tab → sudo -i → work

── BATCH EXECUTION ──
SSM → Run Command → Run command
  → Search: "run shell script" → Select AWS-RunShellScript
  → Enter commands in command field
  → Select targets (manual / tag / resource group)
  → Run → Check status → View output

── CLOUDSHELL ──
Click CloudShell icon → terminal opens
  → aws ec2 describe-instances
  → aws s3 ls
  → No setup needed

── CLEANUP ──
EC2 → Terminate instance (always)
```

***

## Troubleshooting: Instance Not Appearing in Session Manager

```
Instance not in Session Manager list?
  ├── Check: IAM Role correctly attached? (EC2 → instance details)
  ├── Wait: SSM agent needs time to register (2-5 min)
  ├── Check: Instance is running?
  └── Retry: Cancel → Start Session again
```

***

## Other SSM Features (Mentioned, Future Use)

```
Compliance        → Track/enforce compliance across fleet
Change Management → Manage operational changes
Parameter Store   → Store variables, configs, secrets (used in later project)
Operations Center → Centralized operational view
Incident Manager  → Track/handle incidents
```

***

## Reusable Engineering Patterns

| Pattern                        | Manifestation                                                                              |
| ------------------------------ | ------------------------------------------------------------------------------------------ |
| **Connection inversion**       | Instance connects out to SSM, not you connecting in → eliminates inbound port requirements |
| **Role-based service auth**    | IAM Role = service-to-service trust without embedded credentials                           |
| **Centralized control plane**  | SSM console = single point for shell, commands, compliance, params                         |
| **Tag-based targeting**        | Tags transform from labels into operational selectors for fleet-wide actions               |
| **Zero-setup tooling**         | CloudShell = pre-configured CLI; Session Manager = pre-configured shell                    |
| **Separation of access paths** | SSH (direct, key-based) vs. SSM (indirect, role-based) — different paths, same outcome     |

***

## Core Mental Model

```
SSM = "SSH and batch execution, but through AWS, not through network ports"

Permission chain:
  IAM Role (with SSMManagedInstanceCore policy)
    → attached to EC2 instance
      → instance registers with SSM service
        → appears in Session Manager & Run Command targets

CloudShell = "AWS CLI, but zero-setup, in your browser"

Together: SSM + CloudShell + Q Developer = manage everything from browser
  No SSH client, no AWS CLI install, no access keys, no port 22
```

***

This material captures every concept, service interaction, configuration step, troubleshooting detail, and operational pattern from the lecture — structured for deep understanding (Theory), confident execution (Practical), and rapid future recall (Compression Map). 🚀
