# 🎓 Deep Learning Material: AWS CLI (Command Line Interface) — Installation, Authentication, and Programmatic AWS Access

**Source:** Video lecture on AWS CLI and Amazon Q (from [116-aws-cli.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt?EntityRepresentationId=7839d891-f284-443e-8945-400d0b6c80ef) caption file), supplemented by [116.Installing+AWS+CLI.pdf](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116.Installing+AWS+CLI.pdf?EntityRepresentationId=cd9e4268-4609-42fb-8d70-099c5e4e2c38) and [116.AWS+Command+Line+Interface+Part+1.pdf](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116.AWS+Command+Line+Interface+Part+1.pdf?EntityRepresentationId=ba19a1b2-629a-4ee0-8628-8a1c568d8fd4) [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt), [\[116.Instal...ng+AWS+CLI \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116.Installing+AWS+CLI.pdf), [\[116.AWS+Co...ace+Part+1 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116.AWS+Command+Line+Interface+Part+1.pdf)

**Video Context:** This is a dense, hands-on lecture that bridges the gap between the AWS Management Console (graphical/browser-based) and programmatic/command-line access to AWS. The instructor installs AWS CLI, creates an IAM user with access keys, configures authentication, runs real AWS commands (describe instances, create key pair, create security group, launch instance), uses Amazon Q as a command-discovery tool, and closes with a critical engineering principle: **learn manually first, then automate**. The accompanying PDF provides an extended command reference covering EC2, EBS, S3, ELB, RDS, VPC, Auto Scaling, and CloudWatch — serving as a CLI cheat sheet beyond the video scope.

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — AWS CLI: What It Is and Why It Exists

Everything you do on AWS through the browser — through the **AWS Management Console** — can also be done from the **command line** by issuing commands. That is what the AWS CLI (Command Line Interface) is: a tool installed on your local computer (Windows, macOS, or Linux) that lets you interact with AWS services by typing commands instead of clicking through a web interface. [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

The instructor frames this against what the learner has already done: *"So far we launched instance. We created key pair... All those things can be also done from the command line interface. By issuing commands."* The key insight is that the CLI and the Console are **two interfaces to the same underlying AWS API**. They do the same thing — the Console wraps it in a graphical UI, the CLI wraps it in text commands. [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

Why does this matter? Because graphical interfaces require a human sitting in front of a browser. You cannot automate a browser click. But you **can** automate a command. The CLI is the bridge between **manual AWS operations** and **automated/programmatic AWS operations** — which is exactly what DevOps pipelines, CI/CD systems, and infrastructure-as-code tools require. The instructor explicitly states this: *"When we do DevOps, CI, CD pipelines, when we do programmatic access, there are situations where we need the command lines."* [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

> 🔍 **Deep Dive**
>
> The AWS CLI is built on top of the **AWS SDK** (specifically the Python SDK, boto3). When you run an AWS CLI command, it internally constructs an API request, signs it with your credentials, sends it to the AWS service endpoint over HTTPS, and returns the JSON response. This is the same API that the Console calls, that the SDKs call, and that any programmatic tool calls. Understanding that **everything in AWS is ultimately an API call** is a foundational architectural insight — the CLI is just one of many clients for that API.

***

## 1.2 — Authentication: Console vs. CLI — Two Different Credential Mechanisms

When you use the AWS Console (browser), you authenticate with a **username and password**. But the CLI cannot use username/password — it authenticates using **access keys**. Access keys come in two parts: an **Access Key ID** and a **Secret Access Key**. The instructor draws the analogy: *"it works like you know username and password that we have seen but not actually username password."* [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

Access keys are associated with **IAM users**. IAM (Identity and Access Management) is AWS's identity and permission system. To use the CLI, you must: **(1)** create an IAM user, **(2)** attach permissions/policies to that user, and **(3)** generate access keys for that user. The access keys are then configured on your local machine so the CLI can authenticate every command it sends to AWS. [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

***

## 1.3 — IAM Users, Policies, and the Permission Model

When you create an IAM user, it starts with **no permissions and no credentials** — the instructor emphasizes: *"So far there are no access we are giving to this user. Just creating the user. There's no credential. There's no nothing attached to this user."* Permissions must be explicitly attached. [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

AWS uses **policies** to define permissions. IAM has many **ready-made (managed) policies**. For example, `AmazonEC2FullAccess` gives complete access to the EC2 service but nothing else. You can search for service-specific policies and attach them to fine-tune what the user can do. For the lecture, the instructor attaches **AdministratorAccess** — which gives **complete access to the entire AWS account**. [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

The instructor immediately follows this with a critical security warning: *"Be very very careful with this one. You cannot lose credentials for this user. You cannot expose it to anybody, anywhere. Because if that happens, then that other party is going to get complete access on your AWS account."* [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

> ⚠️ **Expert Note**
>
> `AdministratorAccess` is used here for learning convenience. In production, this violates the **principle of least privilege** — you should create policies that grant only the specific permissions needed for the specific task. An IAM user for CI/CD pipelines should have access only to the services the pipeline interacts with (e.g., EC2, S3, ECR), not to billing, IAM user management, or account settings.

***

## 1.4 — Access Key Security: The Most Critical Operational Warning

The instructor delivers the strongest security warning in the entire lecture about access keys: *"These are text and there are many instances where people post it on GitHub. Public repositories, public places where there are bots that can scan these keys, get the keys, and will start doing crypto mining. In your AWS account. You'll have many instances and you will have huge bills within a few hours."* [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

Three rules the instructor states: **(1)** Do not lose them. **(2)** Do not put them into public places. **(3)** Do not show them to anybody. [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

There is also a critical one-time-visibility behavior: the Secret Access Key is shown **only once** at the time of creation. After that, it's gone from the console forever. You must download the CSV file at creation time — if you lose it, you must create new keys. [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

Additionally, the instructor shows that you can **manage access key lifecycle**: deactivate keys, delete keys, and create multiple access keys for a single user. You can select which to activate and which to deactivate. [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

***

## 1.5 — AWS CLI Configuration: How Credentials Are Stored Locally

When you run `aws configure`, it asks for four pieces of information: Access Key ID, Secret Access Key, Default Region, and Output Format. This information is stored in **two files** in your home directory under a `.aws` folder: [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

* **`~/.aws/credentials`** — stores the Access Key ID and Secret Access Key
* **`~/.aws/config`** — stores the default region and output format

The instructor notes: *"if you make a mistake you can manually also go to editor text editor like VI and open it and make the changes. Or you can just run the AWS configure command once again and give your entries."* Common errors are copy-paste mistakes with the keys. [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

> 🔍 **Deep Dive**
>
> This local file storage follows the same **layered configuration pattern** seen in bash startup files (from earlier lectures). The `~/.aws/` directory is per-user — each OS user on the machine can have their own AWS credentials. The default region set here applies to all commands unless overridden with `--region` flag on individual commands. The instructor sets `us-east-1` (North Virginia) as the default region and notes *"we can change it whenever we want."* [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

***

## 1.6 — The AWS CLI Command Structure

Every AWS CLI command follows a consistent pattern: `aws <service> <action> [--parameters]`. For example: [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

* `aws sts get-caller-identity` — service: STS, action: get-caller-identity
* `aws ec2 describe-instances` — service: EC2, action: describe-instances
* `aws ec2 create-key-pair --key-name MyKey` — service: EC2, action: create-key-pair, parameter: key-name

The output is in **JSON format** by default (as configured during `aws configure`). For long outputs, the CLI opens them in the **`more` editor** — you press Enter to scroll and `Q` to quit. [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

The instructor explicitly states that memorizing commands is **not the goal**: *"there are many AWS services and there are many, many settings... it's impossible to remember these commands. You should not even remember the commands. That will be a stupid idea."* Instead, you should use: **(1)** AWS CLI documentation, **(2)** Amazon Q (AWS's AI assistant), or **(3)** ChatGPT to discover and construct commands. [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

***

## 1.7 — Amazon Q: AWS's AI Assistant for Command Discovery

Amazon Q Developer is AWS's built-in AI assistant. The instructor uses it as a **chat tool** (like ChatGPT) to ask questions and get AWS CLI commands. It's accessible via an icon in the AWS Console. [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

The instructor's assessment: *"Amazon Q is slower than other AI tools like ChatGPT for chatting, but it is the most precise one that I have seen so far."* For simple tasks, ChatGPT works fine. But for complex AWS-specific tasks (scripting, programmatic resource creation), Amazon Q has an advantage in precision. [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

Amazon Q also functions as a **code assistant** (like GitHub Copilot) in VS Code — the instructor mentions this will be used later for scripting and automation code. [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

***

## 1.8 — The Foundational Engineering Principle: Manual First, Then Automate

This is the most important conceptual teaching in the entire lecture. The instructor makes it into a universal rule:

*"You must have observed that I'm executing the commands about a task that we already did. And that's how it should be. You should know what you're doing. You should have already done it through graphically, or you should know it somehow. So mastering AWS CLI or even programmatic access of AWS will not come directly. First, you should know that... you should have done that either graphically or you should have worked on it. Then only these commands will make sense."* [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

He reinforces: *"And that's my thumb rule that I teach to everyone in DevOps. Know how to do things manually first before you start automating it... If you do not know security group and if I show you this command... you won't be able to make any sense out of it. If it fails you, you will not know why it failed."* [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

This directly echoes the ChatGPT lecture's principle (from earlier in the course): **tools amplify existing knowledge, they don't replace it**. Whether the tool is ChatGPT, Amazon Q, or the AWS CLI itself — you must understand what you're doing conceptually before you can effectively use any tool to do it faster.

***

## 1.9 — Don't Run Commands Blindly

The instructor's closing advice on CLI usage: *"Just don't run it blindly. Take a look see what command is saying and test it before you use it into your scripting."* This applies whether the command came from documentation, Amazon Q, or ChatGPT. Every command should be understood before execution, and tested in isolation before being embedded in automation scripts. [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building and Why

We are setting up **AWS CLI access** from a local computer, creating an IAM user with programmatic access keys, configuring authentication, and then using the CLI to perform real AWS operations: describing instances, creating a key pair, creating a security group with rules, and launching an EC2 instance. The final operational outcome: you can interact with any AWS service from your terminal, which is the prerequisite for all future automation, scripting, and CI/CD work.

***

## Step 1: Install AWS CLI

**What we're doing:** Installing the AWS CLI tool on your local machine.

**Windows** (PowerShell as admin): [\[116.Instal...ng+AWS+CLI \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116.Installing+AWS+CLI.pdf)

```
choco install awscli -y
```

* `choco` — Chocolatey package manager for Windows
* `install awscli` — installs the AWS CLI package
* `-y` — auto-confirms the installation without prompting

**macOS** (Terminal): [\[116.Instal...ng+AWS+CLI \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116.Installing+AWS+CLI.pdf)

```
brew install awscli
```

* `brew` — Homebrew package manager for macOS

**Linux** (Terminal): [\[116.Instal...ng+AWS+CLI \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116.Installing+AWS+CLI.pdf)

```
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

* `curl` — downloads the installer zip
* `unzip` — extracts it
* `sudo ./aws/install` — runs the installation script with root privileges

**Connection to system flow:** The CLI binary is now available on your machine. But it cannot do anything yet — it has no credentials to authenticate with AWS. [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

***

## Step 2: Create an IAM User for CLI Access

**What we're doing:** Creating a dedicated IAM user whose access keys the CLI will use to authenticate.

1. Go to **AWS Console** → search for **IAM** service → open it [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)
2. Go to **Users** → click **Create User**
3. Give the user a name (instructor uses: `cliadmin`) → click **Next**
4. On the permissions page, click **Attach policies directly**
5. Search for and select **AdministratorAccess** → click **Next** → **Create User** [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

**Why a dedicated user:** You don't use your main AWS account credentials for CLI access. You create a separate IAM user with specific permissions, so you can control, rotate, and revoke access independently.

**Why AdministratorAccess:** For learning purposes, this gives full access to all services. The instructor warns this is dangerous in production — use least-privilege policies instead. [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

***

## Step 3: Generate Access Keys for the IAM User

**What we're doing:** Creating the credential pair (Access Key ID + Secret Access Key) that the CLI will use.

1. Click on the newly created user → go to **Security credentials** tab [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)
2. Scroll to **Access keys** → click **Create access key**
3. Select use case: **Command Line Interface (CLI)** [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)
4. Check **"I understand the risk"** → click **Next** → **Create access key**
5. **IMMEDIATELY** click **Download .csv file** — the Secret Access Key is shown **only this one time** [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

**Expected result:** A CSV file in your Downloads folder containing both the Access Key ID and Secret Access Key, comma-separated.

**Critical warning:** Do NOT share, commit to Git, or expose these keys. Bots scan public repositories for AWS keys and will launch crypto-mining instances in your account within hours. [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

**How to verify:** Back in the IAM console, you can see the Access Key ID listed, but the Secret Access Key is **no longer visible** — it's only in your downloaded CSV. [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

**Key lifecycle management:** You can deactivate, delete, or create additional access keys from the same page. One user can have multiple access keys. [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

***

## Step 4: Configure AWS CLI with the Access Keys

**What we're doing:** Linking the locally installed CLI to your AWS account by providing the credentials.

**Open the CSV file in Notepad** to see your Access Key and Secret Key.

**Open Git Bash (Windows) or Terminal (macOS/Linux)** and run: [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

```bash
aws configure
```

The command prompts for four values:

| Prompt                | What to enter                  | Example                           |
| --------------------- | ------------------------------ | --------------------------------- |
| AWS Access Key ID     | Copy from CSV                  | `AKIAIOSFODNN7EXAMPLE`            |
| AWS Secret Access Key | Copy from CSV (after comma)    | `wJalrXUtnFEMI/K7MDENG/bPxRfi...` |
| Default region name   | Your preferred AWS region code | `us-east-1`                       |
| Default output format | Response format                | `json`                            |

* **Region code:** Check your AWS Console for the correct code. The instructor uses **us-east-1** (North Virginia). The region determines which AWS data center your commands target by default. [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)
* **Output format:** JSON is the default and most common for programmatic parsing.

**What happens internally:** Two files are created: [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

```bash
ls ~/.aws/
```

* `~/.aws/credentials` — contains access key and secret key
* `~/.aws/config` — contains region and output format

**Common mistake:** Copy-paste errors with the keys (extra spaces, missing characters, copying the wrong column from the CSV). If any subsequent command fails with an authentication error, re-run `aws configure` and re-enter the values carefully. [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

***

## Step 5: Verify Authentication — `aws sts get-caller-identity`

**What we're doing:** Running a verification command to confirm the CLI can successfully authenticate with AWS.

```bash
aws sts get-caller-identity
```

* `aws` — the CLI binary
* `sts` — AWS Security Token Service (the identity/authentication service)
* `get-caller-identity` — returns information about the IAM identity making the call [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

**Expected output (JSON):**

```json
{
    "UserId": "AIDAEXAMPLEID",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/cliadmin"
}
```

**How to verify success:** If you see Account ID, User ID, and ARN — authentication works. If you get an error (e.g., `InvalidClientTokenId`, `SignatureDoesNotMatch`), re-run `aws configure` and re-enter credentials. [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

**Connection to system flow:** This is the "health check" for CLI authentication. Always run this first before attempting any other commands.

***

## Step 6: Describe EC2 Instances — First Real AWS Command

**What we're doing:** Querying AWS to list all EC2 instances in the configured default region.

```bash
aws ec2 describe-instances
```

* `ec2` — targets the EC2 service
* `describe-instances` — lists all instances in the current region (us-east-1) [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

**Expected output:** JSON response opened in the `more` pager. Contains detailed information: architecture type, device name, volume ID, public IP, instance type (t2.micro), etc. Press **Enter** to scroll, **Q** to quit. [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

***

## Step 7: Using Amazon Q to Discover Commands

**What we're doing:** Using AWS's AI assistant to find CLI commands for specific tasks instead of memorizing them.

**Access Amazon Q:** Click the Amazon Q icon in the AWS Console → start chatting. [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

### 7a: Create a Key Pair

**Prompt to Amazon Q:** *"How to create key pair using AWS cli"* [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

**Command returned and executed:**

```bash
aws ec2 create-key-pair --key-name MyKeyPair --query 'KeyMaterial' --output text > MyKeyPair.pem
```

* `create-key-pair` — creates a new key pair in AWS
* `--key-name MyKeyPair` — names the key pair
* `--query 'KeyMaterial'` — extracts only the private key material from the JSON response
* `--output text` — outputs as plain text (not JSON)
* `> MyKeyPair.pem` — redirects the private key content into a local `.pem` file [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt), [\[116.AWS+Co...ace+Part+1 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116.AWS+Command+Line+Interface+Part+1.pdf)

**What happens:** The **public key** is stored in AWS (visible in EC2 → Key Pairs). The **private key** is saved locally in `MyKeyPair.pem`. [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

**Verification:**

```bash
cat MyKeyPair.pem     # Shows private key content locally
```

Check EC2 Console → Key Pairs → the public key appears there. [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

### 7b: Create a Security Group with Rules

**Prompt to Amazon Q:** *"Create security group with name my SG with rule 22 from my IP and 80 from anywhere"* [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

**Step 1 — Get your public IP:**

```bash
MY_IP=$(curl https://checkip.amazonaws.com)
echo $MY_IP
```

* `curl https://checkip.amazonaws.com` — accesses an AWS-provided URL that returns your public IP
* The result is stored in variable `$MY_IP` [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

**Step 2 — Create the security group:**

```bash
aws ec2 create-security-group --group-name my-sg --description "My security group"
```

* Returns a **Group ID** (e.g., `sg-0390becf3cae63339`) — you need this for subsequent commands [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

**Step 3 — Add rule: port 22 from your IP:**

```bash
aws ec2 authorize-security-group-ingress --group-name my-sg --protocol tcp --port 22 --cidr $MY_IP/32
```

* `authorize-security-group-ingress` — adds an inbound rule
* `--protocol tcp` — TCP protocol
* `--port 22` — SSH port
* `--cidr $MY_IP/32` — allows only your specific IP (`/32` = single host) [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

**Step 4 — Add rule: port 80 from anywhere:**

```bash
aws ec2 authorize-security-group-ingress --group-name my-sg --protocol tcp --port 80 --cidr 0.0.0.0/0
```

* `--cidr 0.0.0.0/0` — allows all IP addresses (public HTTP access) [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

**Key operational insight:** The security group is created **first** (empty), then rules are added **separately**. This is a two-step process — creation and configuration are decoupled. [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

### 7c: Launch an EC2 Instance

**Prompt to Amazon Q:** *"Launch EC2 instance with below details: name web02, key pair MyKeyPair, security group name, Amazon Linux AMI, instance type..."* with a specific AMI ID. [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

**Finding the AMI ID:** The instructor gets the AMI ID from the AWS Console (Launch Instance page) for Amazon Linux in the current region. Amazon Q can also find AMI IDs based on region, but the instructor prefers being specific. [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

**Command returned and executed:**

```bash
aws ec2 run-instances --image-id <ami-id> --count 1 --instance-type t2.micro --key-name MyKeyPair --security-groups my-sg
```

* `run-instances` — launches one or more EC2 instances
* `--image-id` — the AMI (Amazon Machine Image) to use
* `--count 1` — launch exactly 1 instance
* `--instance-type t2.micro` — the instance size
* `--key-name MyKeyPair` — the key pair for SSH access
* `--security-groups my-sg` — the security group to attach [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt), [\[116.AWS+Co...ace+Part+1 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116.AWS+Command+Line+Interface+Part+1.pdf)

**Expected output:** Large JSON response with instance details (instance ID, state: "pending", private IP, etc.). Press **Q** to exit the pager. [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

**Verification in Console:** Go to EC2 → Instances → `web02` appears. Check Security tab → security group attached. Check key pair name. [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

***

## Step 8: Cleanup — Terminate Resources and Deactivate Keys

**What we're doing:** Removing all created resources and securing the access keys to avoid unnecessary charges and security exposure.

**Terminate the instance** (instructor encourages finding the command yourself via CLI): [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

```bash
aws ec2 terminate-instances --instance-ids <instance-id>
```

<cite>turn6search7</cite>

**Deactivate or delete access keys:** Go to IAM → Users → select the user → Security credentials → Access keys → Deactivate or Delete. [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

**Or delete the IAM user entirely:** IAM → Users → select → Delete user → Confirm. [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

**Why cleanup matters:** Running instances incur charges. Active access keys are a security liability. The instructor says: *"make sure you deactivate the access keys that you have created."* [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

> ⚠️ **Expert Note**
>
> In production, key rotation is a standard security practice — periodically generate new keys, update configurations, deactivate old keys, then delete them after a grace period. Never leave unused keys active. AWS also supports **temporary credentials** via IAM Roles and STS (Security Token Service), which are preferred over long-lived access keys for production workloads.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🔷 Core Concept (One-Line Reconstruction)

> **AWS CLI = text-command interface to the same AWS API that the Console uses, authenticated via access keys instead of username/password, enabling automation and programmatic access.**

***

## 🔷 The Complete Setup Flow

```
INSTALL CLI
  │  Windows: choco install awscli -y (PowerShell admin)
  │  macOS:   brew install awscli
  │  Linux:   curl zip → unzip → sudo ./aws/install
  │
  ▼
CREATE IAM USER
  │  IAM → Users → Create User → name it
  │  Attach policy: AdministratorAccess (or least-privilege)
  │  NO console access, NO credentials yet
  │
  ▼
GENERATE ACCESS KEYS
  │  User → Security credentials → Create access key
  │  Use case: CLI
  │  ⚠️ Secret key shown ONCE → Download CSV immediately
  │
  ▼
CONFIGURE CLI
  │  aws configure
  │  → Access Key ID (from CSV)
  │  → Secret Access Key (from CSV)
  │  → Default region (e.g., us-east-1)
  │  → Output format (json)
  │  Stored in: ~/.aws/credentials + ~/.aws/config
  │
  ▼
VERIFY
  │  aws sts get-caller-identity
  │  → Returns: UserId, Account, Arn
  │  → Error? Re-run aws configure (likely copy-paste mistake)
  │
  ▼
USE CLI
  │  aws <service> <action> [--parameters]
  │
  ▼
CLEANUP
     Terminate instances + Deactivate/Delete access keys + Delete IAM user
```

***

## 🔷 Authentication Model: Console vs. CLI

```
CONSOLE (Browser)                    CLI (Terminal)
─────────────────────                ─────────────────────
Auth: username + password            Auth: Access Key ID + Secret Access Key
Human interactive                    Scriptable, automatable
Cannot be automated                  Foundation for CI/CD & IaC
```

***

## 🔷 AWS CLI Command Pattern

```
aws  <service>  <action>  [--parameter value]

Examples:
  aws sts get-caller-identity
  aws ec2 describe-instances
  aws ec2 create-key-pair --key-name MyKey
  aws ec2 run-instances --image-id ami-xxx --count 1 --instance-type t2.micro
```

***

## 🔷 Access Key Security Rules

```
⚠️ CRITICAL:
  1. Download CSV immediately (secret shown ONCE only)
  2. NEVER commit to Git / public repos
  3. NEVER share with anyone
  4. Deactivate when not in use
  5. Delete when no longer needed

RISK: Bots scan GitHub → steal keys → crypto mine → huge bills in hours
```

***

## 🔷 Credential Storage (Local Files)

```
~/.aws/
  ├── credentials    → Access Key ID + Secret Access Key
  └── config         → Default region + Output format

Fix mistakes: vi ~/.aws/credentials  OR  re-run aws configure
```

***

## 🔷 Command Discovery (Don't Memorize!)

```
Need a CLI command?
  ├── AWS CLI Documentation (docs.aws.amazon.com/cli)
  ├── Amazon Q (AWS Console → Q icon → chat)
  │     Slower than ChatGPT, but more precise for AWS
  └── ChatGPT (good for simple tasks)

RULE: Understand the command before running it.
      Test before embedding in scripts.
```

***

## 🔷 Operational Flow Demonstrated in Video

```
1. aws sts get-caller-identity          → verify auth
2. aws ec2 describe-instances           → list existing instances
3. aws ec2 create-key-pair              → create SSH key pair
     → public key in AWS, private key saved locally (.pem)
4. curl https://checkip.amazonaws.com   → get my public IP
5. aws ec2 create-security-group        → create SG (empty)
6. aws ec2 authorize-security-group-ingress (×2) → add rules
     → port 22 from my IP, port 80 from anywhere
7. aws ec2 run-instances                → launch instance
     → with key pair, SG, AMI ID, instance type
8. Verify in Console                    → confirm all resources
9. aws ec2 terminate-instances          → cleanup
10. IAM → delete user / deactivate keys → secure cleanup
```

***

## 🔷 Security Group Creation Pattern (Two-Step)

```
STEP 1: Create group (empty, no rules)
  aws ec2 create-security-group --group-name X --description "..."
  → returns: group-id

STEP 2: Add rules (one command per rule)
  aws ec2 authorize-security-group-ingress --group-name X --protocol tcp --port 22 --cidr <IP>/32
  aws ec2 authorize-security-group-ingress --group-name X --protocol tcp --port 80 --cidr 0.0.0.0/0
```

***

## 🔷 Extended CLI Command Reference (From PDF — Beyond Video)

The PDF ([116.AWS+Command+Line+Interface+Part+1.pdf](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116.AWS+Command+Line+Interface+Part+1.pdf?EntityRepresentationId=ba19a1b2-629a-4ee0-8628-8a1c568d8fd4)) provides commands for services not demonstrated in the video but available for reference: [\[116.AWS+Co...ace+Part+1 \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116.AWS+Command+Line+Interface+Part+1.pdf)

```
EC2:    create/delete key-pair, security-group, run/terminate instances,
        create-tags, create/delete launch-template
EBS:    create-volume (gp2, encrypted), create-snapshot (with tags),
        delete-volume, allocate-address (Elastic IP)
ELB:    create-load-balancer (application/network), register instances,
        delete load balancer
Auto Scaling: create/delete auto-scaling-group (min/max size, subnets)
RDS:    create/delete db-instance (engine, class, storage, credentials)
S3:     ls, mb (make bucket), cp, mv, sync, rm, rb (remove bucket)
VPC:    create-vpc, create-subnet, create-internet-gateway,
        attach-internet-gateway, create-route-table, create-route,
        associate-route-table, full cleanup sequence
CloudWatch: put-metric-alarm, delete/disable/enable alarm
```

***

## 🔷 The Foundational Engineering Principle

```
MANUAL FIRST → THEN AUTOMATE

"Know how to do things manually first before you start automating it."

Console (graphical) → understand what you're doing
  │
  ▼
CLI (command line) → same operations, scriptable
  │
  ▼
Scripts / CI-CD / IaC → full automation

If you skip step 1:
  → Commands make no sense
  → Failures are undiagnosable  
  → AI-generated commands are unjudgeable
```

This is the same pattern from the ChatGPT lecture: **tools amplify knowledge, they don't replace it**. Whether the tool is the AWS Console, AWS CLI, Amazon Q, or ChatGPT — your foundational understanding is the prerequisite. [\[116-aws-cli \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/116-aws-cli.txt)

***

## 🔷 Reusable Engineering Pattern: Dual-Interface Access to Shared API

```
PATTERN: Multiple interfaces, one underlying API

         ┌─── Console (GUI) ──── human interactive
         │
AWS API ──┼─── CLI (commands) ─── scriptable, automatable
         │
         ├─── SDK (code) ──────── programmatic (Python/Java/etc.)
         │
         └─── IaC (Terraform/CloudFormation) ── declarative infra

ALL call the SAME API. ALL need authentication.
Console = username/password.  Everything else = access keys / roles.

This pattern appears everywhere:
  - Kubernetes: kubectl (CLI) vs Dashboard (GUI) vs API
  - Docker: docker CLI vs Docker Desktop vs Docker API
  - Git: git CLI vs GitHub UI vs Git API
```
