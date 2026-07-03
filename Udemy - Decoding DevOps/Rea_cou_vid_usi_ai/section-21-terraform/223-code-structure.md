# 🎓 Deep Learning Material: Terraform Code Structure, State, and Resource Definition

**Source:** [223-code-structure.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt?EntityRepresentationId=1ea6fa56-6a72-423b-882c-170b5a688006) — Video lecture covering Terraform code organization across multiple `.tf` files, the Terraform state file (`terraform.tfstate`), the `.terraform` directory created by `terraform init`, provider configuration, key pair resource creation with `ssh-keygen`, and security group resource definition with ingress/egress rules — all building toward launching an EC2 instance. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 The Real Objective — Code Structure Over Resource Creation

The instructor opens with a critical framing: the goal of this lecture is **not** to launch an EC2 instance. Launching an instance is merely the example. The actual objective is to understand **Terraform code structure** — how to organize files, how the state works, and how to write resource definitions properly. This distinction matters because it shifts the learner's focus from "what buttons to press" to "how Terraform thinks." Every resource created in this lecture (key pair, security group, instance) is a vehicle for understanding code organization principles. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

***

## 1.2 The `.terraform` Directory and `terraform init`

In the previous exercise, after writing a simple Terraform file and running `terraform init`, a `.terraform` directory was created. This directory is **automatically generated and maintained** — you do not edit it manually. Inside it, you find the **provider executable** (a binary file — for Windows, an `.exe`). This is the plugin binary that Terraform downloads for whichever provider you declared (AWS, in this case). When you run `terraform init`, Terraform reads your code, identifies which providers you need, downloads the correct provider plugin binaries, and places them inside `.terraform`. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

There is also a **lock file** (`.terraform.lock.hcl`). This file is also maintained automatically by `terraform init`. It records the exact provider version being used, ensuring that subsequent runs use the same version. The lock file contains metadata like the provider name and its version. You don't edit this file — Terraform manages it. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

***

## 1.3 The Terraform State File (`terraform.tfstate`)

This is one of the most important concepts in Terraform. When you execute `terraform apply`, Terraform does what your code instructs — creates resources, fetches data, configures infrastructure. After completing these actions, Terraform records **everything it did and everything it knows** about the resulting infrastructure into a file called `terraform.tfstate`. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

The state file is essentially the **output record** of `terraform apply`. It contains the complete details of every resource Terraform manages — IDs, attributes, metadata, relationships. In the previous exercise, the code fetched an AMI ID. The state file recorded this: the resource type (`aws_ami`), the name (`ami_id`), the provider, and critically, the actual AMI ID value that was fetched. When the code said `output` with `.id`, it was pulling that value from what was stored in the state file. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

The state file is how Terraform knows what currently exists. On the next `terraform apply`, Terraform compares the desired state (your code) against the current state (the state file) to determine what needs to change. Without the state file, Terraform would have no memory of what it previously created and would try to create everything from scratch, leading to duplicates or errors. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

In this exercise, the state file is stored **locally** — it's just a file sitting in your project directory. The instructor explicitly foreshadows that in upcoming lectures, the state will be stored **remotely** in an S3 bucket. This is the production approach, because a local state file cannot be shared across team members and can be accidentally deleted or corrupted. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

🔍 **Deep Dive**
The state file is created at **runtime** during `terraform apply`. It is not a static configuration file — it is a dynamic record that changes every time Terraform modifies infrastructure. You can open it and read it (it's JSON), but you should not manually edit it. Every attribute of every resource is accessible from this file, which is why Terraform outputs and cross-resource references work — they pull data from the state. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

***

## 1.4 Multi-File Code Organization — Why and How

This is the central teaching of the lecture. Terraform does **not** require you to put all your code in one file. You can split your resource definitions across as many `.tf` files as you want within the same directory, and Terraform will automatically read **all** `.tf` files in that directory and treat them as a single configuration. There is no import statement, no include directive — just place multiple `.tf` files in the same folder, and Terraform merges them. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

The reason to split is **readability and maintainability**. If you have a provider block, a key pair, a security group with multiple rules, and an instance definition all in one file, that file becomes long and hard to navigate. By separating resources into logical files — `provider.tf`, `keypair.tf`, `security_group.tf`, `instance.tf`, `instance_id.tf` — each file has a clear, single responsibility. You can find and edit any resource quickly. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

The instructor also gives the opposite warning: don't create **too many** files either. If your resources are small, you can group related ones into a single file. The principle is pragmatic balance — enough separation for clarity, not so much that the project becomes a maze of tiny files. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

The file names themselves are **arbitrary** — Terraform doesn't care whether you call a file `provider.tf` or `xyz.tf`. The `.tf` extension is what matters. The names are purely for human readability. By convention, people name files after the resources they contain. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

***

## 1.5 The Provider Block

The `provider` block tells Terraform **which cloud platform** (or service) you are working with and provides configuration for connecting to it. In this case, the provider is `aws`, and the configuration includes the **region** (`us-east-1`). [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

The provider name must be exact — `"aws"` is the name Terraform uses to identify the AWS provider plugin. Inside the provider block, you can specify additional configuration: access keys, secret keys, profiles (for multiple AWS accounts), and IAM role assumptions. However, the instructor explicitly and strongly warns: **never put access keys in your source code**. This is described as "definitely very, very bad idea." The instructor mentions it only to show that the option exists in the documentation, not to encourage its use. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

The provider documentation lives at `registry.terraform.io/browse/providers`. Clicking on the AWS provider and then "Documentation" reveals the full list of resources you can create (instances, CloudWatch, VPCs, etc.) and all configuration options for the provider block itself. The documentation shows example usage, version constraints (using the `~>` approximate version operator, e.g., `~> 5.0`), and all AWS configuration references. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

The provider block is placed in its own file (`provider.tf`) because it is **separate information** from any specific resource. It defines the connection context, not the infrastructure itself. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

***

## 1.6 The Key Pair Resource

To launch an EC2 instance, you need a **key pair** — this is the SSH authentication mechanism. The key pair consists of a public key (stored in AWS) and a private key (kept locally by you). When you SSH into the instance, your private key authenticates against the public key stored in AWS. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

In Terraform, the resource type for this is `aws_key_pair`. The resource definition has two critical fields: `key_name` (the name that will appear in the AWS EC2 console) and `public_key` (the actual content of the public key file). The resource also has a **resource name** — this is the internal Terraform identifier used to reference this resource from other parts of your code. In the video, both the resource name and the key name are set to `dove-key`. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

The public key content is generated locally using `ssh-keygen` before writing the Terraform code. You run the command, it creates two files (e.g., `dove-key` for private, `dove-key.pub` for public), and you copy the contents of the `.pub` file into the `public_key` field of the Terraform resource. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

The resource definition is found in the Terraform documentation: search for `key_pair` in the AWS provider docs, find the resource page, and copy the example usage as a starting template. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

***

## 1.7 The Security Group Resource — Structure, Rules, and Referencing

A security group is a **VPC resource** that acts as a virtual firewall controlling inbound and outbound traffic. In the AWS console, you create security groups with inbound and outbound rules. In Terraform, the same concept is expressed as code, but with specific terminology differences. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

The security group itself is created with `aws_security_group`. The definition includes: a resource name (internal Terraform identifier), a `name` (the name visible in the AWS console), a `description`, and optionally a `vpc_id`. If you **omit** `vpc_id`, the security group is created in the **default VPC** — the video deliberately removes this field to keep things simple. Tags can be added for organizational labeling. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

### Ingress and Egress Rules

Security group **rules** are separate resources from the security group itself. They use the resource types `aws_vpc_security_group_ingress_rule` (inbound) and `aws_vpc_security_group_egress_rule` (outbound). The terminology mapping is: **ingress = inbound**, **egress = outbound**. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

Each rule is its own resource block with its own resource name. A rule references the security group it belongs to via the `security_group_id` field. This field uses Terraform's **cross-resource referencing** syntax: `aws_security_group.dove-sg.id`. This expression means: "Go to the resource of type `aws_security_group` with the name `dove-sg`, and get its `id` attribute." This ID doesn't exist yet when you write the code — it will be generated at runtime and stored in the state file. Terraform resolves these references automatically during `apply` by building a dependency graph. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

### From Port / To Port

When creating security group rules in the AWS console, you specify a single port number. In Terraform, you specify `from_port` and `to_port`. For a single port (like 22 for SSH or 80 for HTTP), you set **both to the same value**: `from_port = 22, to_port = 22`. This is not "from inbound to outbound" — it defines a **port range**. When both values are the same, the range is a single port. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

### CIDR Blocks and IP Addressing

The `cidr_ipv4` field defines which IP addresses are allowed. `0.0.0.0/0` means **any IPv4 address** (anywhere on the internet). A specific IP with `/32` (e.g., `203.0.113.42/32`) means **exactly that one IP** — `/32` is the most restrictive CIDR notation, specifying a single host. The instructor notes that CIDR ranges and networking will be covered in detail in a later VPC section. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

### IP Protocol `-1`

For egress (outbound) rules, the video uses `ip_protocol = "-1"`. This special value means **all protocols and all ports**. The outbound rule with `-1` and `0.0.0.0/0` means: the instance can send traffic to any destination on any port using any protocol. This is the standard default outbound configuration. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

### IPv4 vs IPv6 Egress

The video creates separate egress rules for IPv4 and IPv6. The IPv4 rule uses `cidr_ipv4 = "0.0.0.0/0"` and the IPv6 rule uses `cidr_ipv6 = "::/0"`. These are separate fields — you cannot put an IPv6 address in the `cidr_ipv4` field. If you want to allow outbound traffic to both IPv4 and IPv6 destinations, you need two rules. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

⚠️ **Expert Note**
The instructor emphasizes: "we have to make sure we give the outbound rule of the security group. Otherwise, our instance won't be able to reach the internet." This is a common mistake — people focus on inbound rules and forget that without an explicit egress rule, the instance may not be able to initiate outbound connections (e.g., downloading packages, reaching APIs). [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

***

## 1.8 Using Terraform Documentation as a Workflow

The video demonstrates a consistent workflow for writing resource definitions: go to `registry.terraform.io` → find the provider → click Documentation → search for the resource type → find the example usage → copy it → modify it for your needs. This is not a shortcut — it is the **intended workflow**. Terraform has hundreds of resource types, and no one memorizes their exact syntax. The documentation provides templates that you adapt. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

***

## 1.9 Data Types in Terraform HCL — Strings vs Integers

The video makes a brief but important note about syntax: string values must be in **double quotes** (`"us-east-1"`, `"0.0.0.0/0"`), while integer values do **not** use quotes (`22`, `80`). Port numbers are integers. CIDR blocks, resource names, and descriptions are strings. Mixing these up causes syntax errors. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are creating a structured Terraform project with multiple `.tf` files — each responsible for a distinct resource — that will ultimately launch an EC2 instance with a custom key pair and security group. In this lecture, we complete the provider, key pair, and security group files. The instance file is left for the next lecture. The final structure demonstrates how to organize Terraform code for readability and maintainability. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

***

## Step 1: Examine the Previous Exercise's Artifacts

Before starting the new exercise, examine what `terraform init` and `terraform apply` created in exercise one.

**1a. The `.terraform` folder:**

Expand the `.terraform` directory inside exercise one. You will find the provider executable (binary file). This was downloaded by `terraform init` — it is the AWS provider plugin. You don't need to open or edit this file. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

**1b. The lock file (`.terraform.lock.hcl`):**

Click on the lock file. It shows provider metadata — name, version. This file is maintained automatically by `terraform init`. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

**1c. The state file (`terraform.tfstate`):**

Open this file. It contains the JSON record of everything Terraform created or fetched. Scroll through it — you'll see the resource type (`aws_ami`), the resource name (`ami_id`), the provider, and the actual AMI ID value that was output. The `.id` reference in your output block pulled from this state data. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

**Connection to larger flow:** Understanding these artifacts explains how Terraform tracks state and resolves references — foundational knowledge for everything that follows.

***

## Step 2: Create the Project Structure for Exercise Two

**2a. Create a new folder:**

In VS Code, create a new folder at the **same level** as exercise one (not inside it). Name it `exercise two` (or any name). The video shows the instructor accidentally creating it inside exercise one, then dragging it out. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

**2b. Create the `.tf` files:**

Inside exercise two, create the following files:

| File                | Purpose                                       |
| ------------------- | --------------------------------------------- |
| `instance_id.tf`    | AMI ID data source (copied from exercise one) |
| `provider.tf`       | AWS provider configuration                    |
| `keypair.tf`        | Key pair resource                             |
| `security_group.tf` | Security group + rules                        |
| `instance.tf`       | EC2 instance (next lecture)                   |

Make sure every file has the `.tf` extension. File names are arbitrary — they're for human readability only. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

**2c. Copy the AMI ID code:**

Copy the entire contents of `instance_id.tf` from exercise one into the new `instance_id.tf` in exercise two. Save it. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

**Connection to larger flow:** Each file will contain one logical resource, creating a clean, maintainable project structure.

***

## Step 3: Write the Provider Configuration

Open `provider.tf` and write:

```hcl
provider "aws" {
  region = "us-east-1"
}
```

 [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

| Part                   | Meaning                                                                                           |
| ---------------------- | ------------------------------------------------------------------------------------------------- |
| `provider`             | Block type — declares a provider configuration                                                    |
| `"aws"`                | Provider name — must match exactly (this is the identifier Terraform uses to find the AWS plugin) |
| `region = "us-east-1"` | AWS region where all resources will be created                                                    |

**Where to find documentation:** Navigate to `registry.terraform.io/browse/providers` → click AWS → click Documentation. The provider block documentation shows all available configuration options (region, access keys, profiles, roles). [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

⚠️ **Expert Note**
The documentation shows `access_key` and `secret_key` options. **Never use these.** The instructor repeats this warning twice. Credentials in source code are a severe security risk — they get committed to Git, shared, and exposed. Use environment variables, AWS CLI profiles, or IAM roles instead. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

***

## Step 4: Generate an SSH Key Pair

Before writing the key pair resource, generate the actual keys.

**4a. Open a terminal in VS Code:**

Terminal → New Terminal. Make sure you are inside the exercise two directory:

```bash
cd exercise-two    # or whatever your folder name is
ls                 # verify you see your .tf files
```

 [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

**4b. Generate the key pair:**

```bash
ssh-keygen
```

| Prompt                                | Action                                                                                |
| ------------------------------------- | ------------------------------------------------------------------------------------- |
| "Enter file in which to save the key" | Type `dove-key` (just the name, so it creates the key files in the current directory) |
| "Enter passphrase"                    | Press Enter (no passphrase)                                                           |
| "Enter same passphrase again"         | Press Enter                                                                           |

 [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

**What this creates:**

| File           | Purpose                                                          |
| -------------- | ---------------------------------------------------------------- |
| `dove-key`     | Private key (keep this — you'll use it to SSH into the instance) |
| `dove-key.pub` | Public key (content goes into Terraform code → stored in AWS)    |

**4c. View and copy the public key:**

```bash
cat dove-key.pub
```

Select the entire output. In a Bash terminal, selecting text and right-clicking copies it. You need this content for the next step. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

***

## Step 5: Write the Key Pair Resource

**5a. Find the resource template:**

In the Terraform AWS documentation, search for `key_pair`. Click on the `aws_key_pair` resource. Copy the example usage. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

**5b. Write the resource in `keypair.tf`:**

```hcl
resource "aws_key_pair" "dove-key" {
  key_name   = "dove-key"
  public_key = "<paste your public key content here>"
}
```

 [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

| Part             | Meaning                                                                                      |
| ---------------- | -------------------------------------------------------------------------------------------- |
| `resource`       | Block type — declares an infrastructure resource                                             |
| `"aws_key_pair"` | Resource type — the kind of AWS resource to create                                           |
| `"dove-key"`     | Resource name — Terraform's internal identifier for this resource (used in cross-references) |
| `key_name`       | The name that appears in the AWS EC2 console under Key Pairs                                 |
| `public_key`     | The actual content of the `.pub` file — paste the full string from `cat dove-key.pub`        |

Paste the public key content inside double quotes. Save with `Ctrl+S`. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

**Connection to larger flow:** The instance resource (next lecture) will reference this key pair so that SSH access is configured on launch.

***

## Step 6: Write the Security Group Resource

Open `security_group.tf`. This file will contain the security group itself plus all its rules.

**6a. Find the resource template:**

In Terraform AWS documentation, search for `security_group`. Click on `aws_security_group`. Copy the example usage. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

**6b. Write the security group definition:**

```hcl
resource "aws_security_group" "dove-sg" {
  name        = "dove-sg"
  description = "dove-sg"

  tags = {
    Name = "dove-sg"
  }
}
```

 [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

`vpc_id` is deliberately **omitted** — this causes the security group to be created in the default VPC. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

***

## Step 7: Write the Ingress (Inbound) Rules

**7a. Find your public IP:**

Open a browser and search "what is my IPv4". Note your IP address. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

**7b. SSH rule (port 22 from your IP):**

```hcl
resource "aws_vpc_security_group_ingress_rule" "SSH_from_my_IP" {
  security_group_id = aws_security_group.dove-sg.id
  cidr_ipv4         = "<your-ip>/32"
  from_port         = 22
  to_port           = 22
  ip_protocol       = "tcp"
}
```

 [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

| Part                                                | Meaning                                                                                         |
| --------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| `"aws_vpc_security_group_ingress_rule"`             | Resource type for inbound rules                                                                 |
| `"SSH_from_my_IP"`                                  | Resource name (your choice — descriptive)                                                       |
| `security_group_id = aws_security_group.dove-sg.id` | Cross-reference: get the ID of the `dove-sg` security group (resolved at apply time from state) |
| `cidr_ipv4 = "<your-ip>/32"`                        | Allow only this exact IP (`/32` = single host)                                                  |
| `from_port = 22` / `to_port = 22`                   | Port range — both the same for a single port                                                    |
| `ip_protocol = "tcp"`                               | SSH uses TCP                                                                                    |

**7c. HTTP rule (port 80 from anywhere):**

```hcl
resource "aws_vpc_security_group_ingress_rule" "allow_HTTP" {
  security_group_id = aws_security_group.dove-sg.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 80
  to_port           = 80
  ip_protocol       = "tcp"
}
```

 [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

`0.0.0.0/0` = any IPv4 address (anywhere on the internet). [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

***

## Step 8: Write the Egress (Outbound) Rules

**8a. IPv4 outbound (all traffic):**

```hcl
resource "aws_vpc_security_group_egress_rule" "allow_all_outbound_IPv4" {
  security_group_id = aws_security_group.dove-sg.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1"
}
```

 [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

| Part                      | Meaning                                          |
| ------------------------- | ------------------------------------------------ |
| `ip_protocol = "-1"`      | All protocols, all ports — unrestricted outbound |
| `cidr_ipv4 = "0.0.0.0/0"` | To any IPv4 destination                          |

**8b. IPv6 outbound (all traffic):**

```hcl
resource "aws_vpc_security_group_egress_rule" "allow_all_outbound_IPv6" {
  security_group_id = aws_security_group.dove-sg.id
  cidr_ipv6         = "::/0"
  ip_protocol       = "-1"
}
```

 [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

Note: `cidr_ipv6` is a **different field** from `cidr_ipv4`. They cannot be mixed. Separate rules are needed for IPv4 and IPv6 outbound. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

⚠️ **Expert Note**
Without egress rules, the instance cannot reach the internet — it won't be able to download packages, contact APIs, or perform any outbound communication. Always define outbound rules. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

***

## Step 9: Validate the Syntax

Before proceeding, review the entire `security_group.tf` file for common mistakes:

* Every `security_group_id` reference uses the correct resource name (`dove-sg`).
* All string values are in **double quotes** (CIDR blocks, protocols, descriptions).
* Port numbers are **integers** (no quotes around `22`, `80`).
* No missing closing braces. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

Save all files with `Ctrl+S`. [\[223-code-structure \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/223-code-structure.txt)

**Connection to larger flow:** The security group and key pair are now defined. The instance resource (next lecture) will reference both — the key pair for SSH access and the security group for network rules. Terraform will resolve all cross-references at apply time using the dependency graph and state file.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Project File Structure

```
exercise-two/
├── provider.tf         → provider "aws" { region }
├── instance_id.tf      → data source: AMI ID (copied from ex1)
├── keypair.tf          → resource: aws_key_pair
├── security_group.tf   → resource: aws_security_group + 4 rules
├── instance.tf         → resource: aws_instance (NEXT LECTURE)
├── dove-key            → private key (local, never uploaded)
└── dove-key.pub        → public key (content pasted into keypair.tf)
```

Terraform reads **ALL `.tf` files** in the directory as one configuration. File names are for humans, not Terraform.

***

## Terraform Artifact Map (from `init` and `apply`)

```
terraform init  →  .terraform/          (provider binary + plugins)
                   .terraform.lock.hcl  (provider version lock)

terraform apply →  terraform.tfstate    (JSON record of ALL created resources)
                                         - resource types, names, IDs, attributes
                                         - cross-references resolved from here
                                         - currently LOCAL, will move to S3 (future)
```

***

## State File Mental Model

```
Your Code (.tf files)         = DESIRED state (what you WANT)
State File (terraform.tfstate) = CURRENT state (what EXISTS)

terraform apply = diff(desired, current) → create/update/destroy to match
```

***

## Provider Block

```hcl
provider "aws" {
  region = "us-east-1"
}
```

```
Available options (from docs):  region, access_key, secret_key, profile, assume_role
                                ⚠️ NEVER put access_key/secret_key in code
Docs: registry.terraform.io → AWS → Documentation
```

***

## Resource Definition Pattern

```
resource "<TYPE>" "<NAME>" {
  <attribute> = <value>
}

TYPE = aws_key_pair, aws_security_group, aws_instance, etc.
NAME = internal Terraform ID (used in cross-references)
```

***

## Cross-Resource Referencing

```
aws_security_group.dove-sg.id
     │                │      │
     resource type    name   attribute (from state file, resolved at apply time)
```

Pattern: `<resource_type>.<resource_name>.<attribute>`

***

## Key Pair Flow

```
ssh-keygen → dove-key (private, keep local)
           → dove-key.pub (public, paste content into keypair.tf)

resource "aws_key_pair" "dove-key" {
  key_name   = "dove-key"        ← name in AWS console
  public_key = "<content>"       ← from cat dove-key.pub
}
```

***

## Security Group Architecture

```
resource: aws_security_group "dove-sg"
  ├── name, description, tags
  └── vpc_id OMITTED → default VPC

INGRESS RULES (inbound):
  ├── SSH_from_my_IP:   port 22,  tcp,  <my-ip>/32     (single host)
  └── allow_HTTP:       port 80,  tcp,  0.0.0.0/0      (anywhere)

EGRESS RULES (outbound):
  ├── allow_all_outbound_IPv4:  all ports (-1),  0.0.0.0/0
  └── allow_all_outbound_IPv6:  all ports (-1),  ::/0

ALL rules reference:  security_group_id = aws_security_group.dove-sg.id
```

***

## Port / Protocol / CIDR Quick Reference

```
from_port = 22, to_port = 22    → single port (NOT from/to direction)
ip_protocol = "tcp"              → TCP protocol
ip_protocol = "-1"               → ALL protocols, ALL ports

cidr_ipv4 = "0.0.0.0/0"         → any IPv4 (internet-wide)
cidr_ipv4 = "x.x.x.x/32"       → exactly one IP
cidr_ipv6 = "::/0"              → any IPv6

⚠️ cidr_ipv4 and cidr_ipv6 are SEPARATE fields → need separate rules
```

***

## Terraform Documentation Workflow

```
registry.terraform.io → Provider (AWS) → Documentation
  → search resource name (e.g., "key_pair", "security_group")
  → copy Example Usage
  → modify for your needs

This is the INTENDED workflow — not a shortcut.
```

***

## HCL Syntax Rules

```
Strings:   double quotes   →  "us-east-1", "tcp", "0.0.0.0/0"
Integers:  no quotes       →  22, 80
Extension: .tf             →  mandatory for Terraform to read the file
```

***

## Code Organization Principles

```
SPLIT when:   resources are logically distinct (provider ≠ key pair ≠ security group)
GROUP when:   resources are small or tightly related
AVOID:        one giant file (hard to maintain)
AVOID:        too many tiny files (hard to navigate)

File names:   arbitrary (human convention only)
Terraform:    reads ALL .tf files in directory as single config
```

***

## Dependency Chain (This Lecture → Next)

```
provider.tf       → establishes AWS connection + region
keypair.tf        → creates key pair for SSH access
security_group.tf → creates firewall rules for the instance
                          ↓
instance.tf (NEXT LECTURE) → references key pair + security group
                          ↓
terraform init → terraform apply → EC2 instance running
```

***

## Key Engineering Patterns

| Pattern                              | Manifestation                                                                                               |
| ------------------------------------ | ----------------------------------------------------------------------------------------------------------- |
| **Single-responsibility files**      | Each `.tf` file holds one logical resource — separation of concerns in IaC                                  |
| **State as truth**                   | `tfstate` is the authoritative record of infrastructure; code is intent, state is reality                   |
| **Cross-resource referencing**       | `type.name.attribute` — resources reference each other without hardcoding values                            |
| **Template-from-docs**               | Copy example from official docs → modify; never write from scratch                                          |
| **Deferred resolution**              | References like `.id` don't exist at write time; Terraform resolves them at apply time via dependency graph |
| **Local → Remote state progression** | Start local for learning; move to S3 for production (shared, durable, lockable)                             |
| **Credential separation**            | Provider supports credentials in code but you MUST use external auth (env vars, profiles, roles)            |

***

This completes the full reconstruction. **Theory** explains *why* Terraform structures code, state, and resources the way it does. **Practical** gives you every file, every resource block, and every command to reproduce the setup. The **Compression Map** lets you reload the entire project structure, referencing syntax, and security group architecture in under two minutes. Let me know if you'd like Anki flashcards or any section expanded! 🚀
