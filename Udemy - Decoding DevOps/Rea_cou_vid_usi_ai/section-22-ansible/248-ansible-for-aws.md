# 🎓 Deep Learning Material: Ansible for AWS — Key Pair Creation & EC2 Instance Launch

**Source:** [248-ansible-for-aws.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt?EntityRepresentationId=ee4c252a-f83a-4d6d-b3aa-da24b78b8b29) (video caption) + [248.test-aws.yml](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248.test-aws.yml?EntityRepresentationId=29e5c2ee-1abb-4a15-a800-9b875f433642) (playbook file) — Video lecture covering Ansible integration with AWS, including IAM user creation for API access, exporting credentials, installing boto3, creating an EC2 key pair with the `ec2_key` module, capturing and saving the private key using `register` + `copy` + `when`, installing the `amazon.aws` collection, and launching an EC2 instance with `ec2_instance` using `exact_count` for idempotency. [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248.test-aws.yml)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 How Ansible Talks to AWS — The Fundamental Shift

In every previous Ansible exercise, the control machine connected to **remote target machines** via SSH and executed tasks on them. Managing AWS is fundamentally different. When you create a key pair or launch an EC2 instance, there is no target machine to SSH into — the resources don't exist yet. Instead, the playbook runs on **localhost** (the control machine itself) and makes **API calls** to the AWS account. The control machine becomes both the executor and the origin of requests. [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt)

This is why the playbook specifies `hosts: localhost` — every task runs locally. And `gather_facts: false` — because we don't need to collect information about the control machine's OS, network, or hardware. We're not configuring the control machine; we're using it as a launchpad to interact with AWS's API. [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248.test-aws.yml)

***

## 1.2 Authentication — How Ansible Knows Your AWS Account

When Ansible makes API calls to AWS, AWS needs to verify: who is making this request, and are they authorized? This is handled through **access keys** — specifically an **Access Key ID** and a **Secret Access Key**. These credentials are generated when you create an **IAM user** in AWS. [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt)

The credentials must be available to Ansible at runtime. The mechanism is **environment variables**: `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`. You set these using the `export` command. When Ansible (which is written in Python) runs, the underlying AWS SDK (boto3) reads these environment variables to authenticate every API call. [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt)

There is a practical problem with `export`: if you run `export` in a shell session and then exit, the variables are **destroyed**. Next time you log in, they're gone and you must export again. The solution the video recommends is to place the export commands in the **`.bashrc`** file. This file executes automatically every time you log in. After adding the lines, you either run `source ~/.bashrc` to reload immediately, or log out and back in. [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt)

⚠️ **Expert Note**
The IAM user in the video is given **AdministratorAccess** — full control over the entire AWS account. The instructor explicitly warns this is "very dangerous." In production, you should follow the principle of least privilege — grant only the specific permissions needed (e.g., EC2 access only). The access keys must never be committed to Git repositories or exposed in source code. [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt)

***

## 1.3 The boto3 Dependency — Python's AWS SDK

Ansible is written in Python. To interact with AWS, Python needs a library called **boto3** — the official AWS SDK for Python. Without boto3, Ansible cannot make any AWS API calls. The error you get is explicit: Ansible reports that it cannot find the boto/boto3 module. [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt)

boto3 is installed using **pip** (Python's package installer). But pip itself may not be installed on a fresh Ubuntu system. So the dependency chain is: install pip first (`sudo apt install python3-pip -y`), then install boto3 (`pip3.10 install boto3` — using the specific pip version that matches your Python installation). The video demonstrates using tab completion (`pip` + Tab + Tab) to find the correct pip binary name (e.g., `pip3.10`). [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt)

***

## 1.4 The `ec2_key` Module — Creating a Key Pair

The `ec2_key` module creates (or deletes) an EC2 key pair in AWS. When AWS creates a key pair, it generates both a public key and a private key. The **public key** is stored in your AWS account (visible in the EC2 console under Key Pairs). The **private key** is returned **only once** — at the moment of creation. If you don't capture it, it's gone forever. AWS does not store the private key and cannot give it to you again. [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt)

This "return only once" behavior is the central design challenge of this section. The module needs three things: the `name` of the key pair, the `region` where to create it, and a way to capture the output. The region can be specified directly in the task or via the `AWS_REGION` environment variable (similar to how credentials are exported). [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248.test-aws.yml)

***

## 1.5 `register` — Capturing Task Output into a Variable

Every Ansible task produces output — a JSON object containing details about what happened. By default, this output is discarded after the task completes. The `register` keyword captures this output into a **variable** that persists for the rest of the playbook run. [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt)

In this playbook: `register: keyout` saves the entire output of the `ec2_key` task into a variable called `keyout`. This variable is a nested dictionary. The private key content lives at `keyout.key.private_key`. The `changed` status (whether the task actually created something new or found the key already existing) lives at `keyout.changed`. [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248.test-aws.yml)

You can inspect the registered variable using the **`debug`** module: `debug: var: keyout` prints the entire variable structure. This is how the video reveals the JSON structure and discovers where the private key is stored within the output. [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt)

🔍 **Deep Dive**
The private key field (`keyout.key.private_key`) only exists in the registered output when the key is **newly created** (`changed: true`). If the key already exists in AWS and the task runs again, the output does **not** contain the private key — because AWS doesn't return it on subsequent queries. This is why the `when: keyout.changed` condition on the save task is essential — without it, the save task would fail trying to access a variable path that doesn't exist. [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt)

***

## 1.6 Conditional Save with `when: keyout.changed`

The `copy` module is used to save the private key to a local file. Its `content` parameter takes the variable `keyout.key.private_key`, and `dest` specifies the output file path (`./sample.pem`). But this task must only run when the key was **actually created** — not when it already existed. [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248.test-aws.yml)

The condition `when: keyout.changed` controls this. The `changed` field is a boolean — `true` if the key was newly created, `false` if it already existed. Since the value is already a boolean, you don't need `== true` — writing just `keyout.changed` is sufficient. If it's `true`, the task runs and saves the file. If it's `false`, the task is skipped. [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt)

This pattern — register output → conditionally act on `changed` status — is a core Ansible pattern for handling idempotent workflows where certain follow-up actions should only happen on first creation. [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt)

***

## 1.7 The `amazon.aws` Collection — Installing AWS Modules

The `ec2_key` module exists in Ansible's built-in modules, but the `ec2_instance` module (for launching instances) belongs to the **`amazon.aws` collection** — a separately installable package of AWS-specific modules. Before using it, you must install this collection on the control machine using: `ansible-galaxy collection install amazon.aws`. [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt)

The module's full qualified name in the playbook is `amazon.aws.ec2_instance`, which reflects the collection namespace. [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248.test-aws.yml)

***

## 1.8 The `ec2_instance` Module and `exact_count`

The `ec2_instance` module creates and manages EC2 instances. Key parameters include `name`, `key_name`, `instance_type`, `security_group`, `image_id`, `region`, and `tags`. [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248.test-aws.yml)

The most critical parameter for operational safety is **`exact_count`**. This integer tells Ansible: "Ensure exactly this many instances matching these filters are running." If you set `exact_count: 1` and run the playbook, it launches one instance. If you run the playbook again, it sees one matching instance already exists and does **nothing** — no duplicate is created. Without `exact_count`, every playbook run would launch a **new** instance, leading to uncontrolled duplication. The instructor explicitly warns about this. [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt)

The `image_id` (AMI ID) is **region-specific** — the same AMI has different IDs in different regions. You must ensure the AMI ID matches the region specified in the task. The video demonstrates finding the AMI ID from the EC2 console by clicking "Launch Instance" and noting the AMI ID for the default Amazon Linux image in the selected region (us-west-2). [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt)

Other parameters: `vpc_subnet_id` is commented out — omitting it causes the instance to launch in the default VPC and subnet. `security_group: default` uses the default security group. The `network: assign_public_ip` section is also commented out because instances in the default VPC already receive public IPs. [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248.test-aws.yml)

🔍 **Deep Dive**
The video mentions two additional optional parameters not fully implemented: `state: running` and `wait: true`. `wait: true` tells Ansible to block until the instance reaches the `running` state before returning. Without it, Ansible returns immediately after the API call, and the instance may still be in `pending` state. The playbook works either way, but `wait: true` provides certainty that the instance is fully operational before subsequent tasks run. [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt)

***

## 1.9 The Ansible-AWS Workflow Model

The video establishes a repeatable workflow for any AWS module: find the module in the documentation → check the example → copy the example into your playbook → modify parameters for your environment → run → troubleshoot errors (commonly: missing region, wrong AMI ID, missing subnet ID, missing boto3, missing collection). The instructor frames this as the core Ansible skill: "finding and using the right module, and when you fail, look at the error, troubleshoot it, and most importantly, use Ansible documentation." [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt)

The lecture closes by noting that while Ansible can manage AWS, **Terraform** is a "much more better cloud management tool" for this purpose. Ansible's strength is configuration management; Terraform's strength is infrastructure provisioning. Both can do both, but each has its sweet spot. [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are writing an Ansible playbook that runs on localhost, authenticates to AWS via exported credentials, creates an EC2 key pair, saves the private key to a local file, and launches an EC2 instance. The final outcome: a single playbook that provisions a complete EC2 instance with its key pair, idempotently (safe to run multiple times without creating duplicates). [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt)

***

## Step 1: Create an IAM User with Access Keys

Navigate to **AWS Console → IAM → Users → Add User**.

**1a. Create the user:**

| Setting     | Value                                              |
| ----------- | -------------------------------------------------- |
| User name   | `ansible-admin`                                    |
| Permissions | Attach policies directly → **AdministratorAccess** |

Click **Create user**. [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt)

**1b. Generate access keys:**

Click on the user → **Security credentials** → **Access keys** → **Create access key**. Select **CLI** use case. Acknowledge the warning. Click **Create access key**. **Download the CSV file** — this contains your Access Key ID and Secret Access Key. Click **Done**. [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt)

⚠️ **Expert Note**
AdministratorAccess gives full control of your AWS account. In production, create a policy with only the permissions needed (EC2, key pair management). Never expose these keys in Git or source code. [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt)

***

## Step 2: Export AWS Credentials on the Control Machine

SSH into your Ansible control machine.

**Option A (temporary — lost on logout):**

```bash
export AWS_ACCESS_KEY_ID=<your-access-key-id>
export AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
```

**Option B (persistent — recommended):**

Open `~/.bashrc`:

```bash
vim ~/.bashrc
```

Add at the end:

```bash
export AWS_ACCESS_KEY_ID=<your-access-key-id>
export AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
```

Save and reload:

```bash
source ~/.bashrc
```

 [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt)

**Why `.bashrc`:** The `export` command in a shell session is destroyed when you exit. Placing it in `.bashrc` means it auto-executes on every login. `source ~/.bashrc` reloads it without requiring logout/login. [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt)

***

## Step 3: Install Prerequisites — pip and boto3

**3a. Install pip:**

```bash
sudo apt install python3-pip -y
```

 [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt)

**3b. Install boto3:**

```bash
pip3.10 install boto3
```

Use tab completion (`pip` + Tab + Tab) to find the exact pip binary name matching your Python version. [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt)

**Why boto3:** Ansible uses Python to make AWS API calls. boto3 is the Python SDK for AWS. Without it, every AWS module fails with a "boto/boto3 not found" error. [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt)

***

## Step 4: Create the Project Directory and Playbook

```bash
mkdir aws
cd aws
vim test-aws.yml
```

 [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt)

***

## Step 5: Write the Key Pair Creation Task

```yaml
- hosts: localhost
  gather_facts: false
  tasks:
    - name: Create key pair
      ec2_key:
        name: sample
        region: us-west-2
      register: keyout
```

 [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248.test-aws.yml)

| Part                  | Meaning                                                      |
| --------------------- | ------------------------------------------------------------ |
| `hosts: localhost`    | Run on the control machine (API calls, not SSH to targets)   |
| `gather_facts: false` | Don't collect facts about the control machine — not needed   |
| `ec2_key:`            | Module for creating/deleting EC2 key pairs                   |
| `name: sample`        | Name of the key pair in AWS                                  |
| `region: us-west-2`   | AWS region where the key pair is created                     |
| `register: keyout`    | Capture the task's entire JSON output into variable `keyout` |

**First run without `register`:** The task succeeds but the private key is not captured. The key pair exists in AWS (public key stored), but the private key is lost. This is why `register` is essential. [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt)

**If you need to re-create:** Delete the key from the AWS console first. The private key is returned **only on first creation**. Running the task again when the key exists returns `changed: false` and no private key. [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt)

**Region error:** If you omit `region`, Ansible fails with "you need to specify the region." You can either add `region:` to each task or export `AWS_REGION` as an environment variable. [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt)

***

## Step 6: Add the Debug Task (Optional — For Inspection)

```yaml
    - name: Print key
      debug:
        var: keyout
```

This prints the full `keyout` variable to see its structure. After confirming the structure, you can comment this out (the video comments it with `#` to avoid printing the private key in future runs). [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248.test-aws.yml)

***

## Step 7: Add the Save Key Task with Condition

```yaml
    - name: Save key
      copy:
        content: "{{keyout.key.private_key}}"
        dest: ./sample.pem
      when: keyout.changed
```

 [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248.test-aws.yml)

| Part                                    | Meaning                                                                               |
| --------------------------------------- | ------------------------------------------------------------------------------------- |
| `copy:`                                 | Module for creating files with specified content                                      |
| `content: "{{keyout.key.private_key}}"` | The private key value extracted from the registered variable (Jinja2 template syntax) |
| `dest: ./sample.pem`                    | Save to a file named `sample.pem` in the current directory                            |
| `when: keyout.changed`                  | Only execute if the key was newly created (`changed: true`)                           |

**Why the condition:** If the key already exists, `keyout.key.private_key` doesn't exist in the output — the save task would fail with a "variable not found" error. `when: keyout.changed` prevents this by skipping the task entirely when the key wasn't newly created. [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt)

**Boolean shorthand:** `keyout.changed` is already `true` or `false` — no need to write `keyout.changed == true`. [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt)

***

## Step 8: Install the `amazon.aws` Collection

Before adding the EC2 instance task, install the AWS module collection:

```bash
ansible-galaxy collection install amazon.aws
```

 [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt)

This installs modules like `amazon.aws.ec2_instance` on the control machine. Without it, the `ec2_instance` module is not recognized.

***

## Step 9: Add the EC2 Instance Launch Task

```yaml
    - name: Start an instance
      amazon.aws.ec2_instance:
        name: "public-compute-instance"
        key_name: "sample"
        instance_type: t2.micro
        security_group: default
        image_id: ami-02d8bad0a1da4b6fd
        exact_count: 1
        region: us-west-2
        tags:
          Environment: Testing
```

 [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248.test-aws.yml)

| Parameter        | Value                       | Meaning                                                         |
| ---------------- | --------------------------- | --------------------------------------------------------------- |
| `name`           | `"public-compute-instance"` | Tag name for the instance                                       |
| `key_name`       | `"sample"`                  | The key pair created in the previous task                       |
| `instance_type`  | `t2.micro`                  | Small instance (free tier eligible)                             |
| `security_group` | `default`                   | Use the default security group                                  |
| `image_id`       | `ami-02d8bad0a1da4b6fd`     | AMI ID for Amazon Linux in us-west-2                            |
| `exact_count`    | `1`                         | Ensure exactly 1 matching instance exists — prevents duplicates |
| `region`         | `us-west-2`                 | Must match the region of the AMI ID                             |
| `tags`           | `Environment: Testing`      | Metadata tags on the instance                                   |

**Finding the AMI ID:** Go to AWS Console → EC2 → Launch Instance. Select the desired OS image. Copy the AMI ID shown. Ensure you're in the **same region** as specified in the playbook — AMI IDs differ between regions. [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt)

**`vpc_subnet_id` omitted:** The instance launches in the default VPC/subnet. [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt)

**`exact_count: 1` is critical:** Without it, every playbook run creates a **new** instance. With it, Ansible checks if a matching instance already exists and only creates one if needed. [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt)

***

## Step 10: Run the Complete Playbook

```bash
ansible-playbook test-aws.yml
```

 [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt)

**Expected output on first run:**

| Task              | Status                        |
| ----------------- | ----------------------------- |
| Create key pair   | `changed`                     |
| Save key          | `changed` (file created)      |
| Start an instance | `changed` (instance launched) |

**Expected output on second run:**

| Task              | Status                                                 |
| ----------------- | ------------------------------------------------------ |
| Create key pair   | `ok` (key already exists)                              |
| Save key          | `skipping` (keyout.changed is false)                   |
| Start an instance | `ok` (instance already exists, exact\_count satisfied) |

**Verify in AWS Console:** Check EC2 → Instances → the instance should appear in `running` state in us-west-2. Check EC2 → Key Pairs → `sample` should be listed. [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt)

**Verify locally:**

```bash
ls
cat sample.pem
```

The `sample.pem` file should contain the private key content. [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt)

***

## Step 11: Cleanup

After finishing, clean up to avoid costs:

1. **Terminate the EC2 instance:** AWS Console → EC2 → Instances → select instance → Instance State → Terminate.
2. **Delete the key pair:** AWS Console → EC2 → Key Pairs → select `sample` → Actions → Delete.
3. Optionally delete the local `sample.pem` file. [\[248-ansible-for-aws \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/248-ansible-for-aws.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Architecture — Ansible-to-AWS Flow

```
[ Control Machine (localhost) ]
    │
    │  Runs playbook locally (hosts: localhost)
    │  gather_facts: false (not configuring control machine)
    │
    ├── Environment Variables:
    │     AWS_ACCESS_KEY_ID
    │     AWS_SECRET_ACCESS_KEY
    │         │
    │         ▼
    │     boto3 (Python SDK) → AWS API calls
    │
    ├── Task 1: ec2_key       → Creates key pair in AWS
    │     register: keyout          (captures output)
    │
    ├── Task 2: copy          → Saves private key to ./sample.pem
    │     when: keyout.changed      (only on first creation)
    │
    └── Task 3: ec2_instance  → Launches EC2 instance
          exact_count: 1            (idempotent — no duplicates)
```

***

## Prerequisite Chain

```
1. IAM user (ansible-admin) + AdministratorAccess
2. Access keys → CSV download
3. Export to ~/.bashrc:
     export AWS_ACCESS_KEY_ID=<value>
     export AWS_SECRET_ACCESS_KEY=<value>
4. source ~/.bashrc
5. sudo apt install python3-pip -y
6. pip3.10 install boto3
7. ansible-galaxy collection install amazon.aws
```

***

## Key Pair Private Key — Return-Once Problem

```
ec2_key creates key pair:
  First run:   changed=true  → keyout.key.private_key EXISTS
  Second run:  changed=false → keyout.key.private_key DOES NOT EXIST

Solution:
  register: keyout              ← capture output
  copy: content → dest          ← save to file
  when: keyout.changed          ← only when newly created

⚠️ If you miss saving on first run → delete key from AWS → re-run
⚠️ Comment out debug task → don't print private key in logs
```

***

## `exact_count` — Idempotency Guard

```
WITHOUT exact_count:
  Run 1 → instance created
  Run 2 → ANOTHER instance created
  Run 3 → ANOTHER instance created
  = uncontrolled duplication

WITH exact_count: 1:
  Run 1 → instance created (count = 0 → 1)
  Run 2 → ok, no change (count already = 1)
  Run 3 → ok, no change (count already = 1)
  = safe, idempotent
```

***

## Region + AMI ID Constraint

```
AMI ID is REGION-SPECIFIC
  ami-02d8bad0a1da4b6fd → valid ONLY in us-west-2

Mismatch → "AMI not found" error

Always verify:
  1. Region in playbook task matches
  2. AMI ID found in EC2 console IN THAT REGION
```

***

## Error → Fix Sequence (Encountered in Video)

```
Error                                    │ Fix
─────────────────────────────────────────┼──────────────────────────────────
"boto/boto3 module not found"            │ pip install boto3 (install pip first)
"You need to specify the region"         │ Add region: to task or export AWS_REGION
Key created but private key not saved    │ Add register: + copy task with when: .changed
Module ec2_instance not found            │ ansible-galaxy collection install amazon.aws
Multiple instances on repeated runs      │ Add exact_count: 1
```

***

## Playbook Structure (Reference)

```yaml
- hosts: localhost
  gather_facts: false
  tasks:
    - name: Create key pair
      ec2_key:
        name: sample
        region: us-west-2
      register: keyout

    - name: Save key
      copy:
        content: "{{keyout.key.private_key}}"
        dest: ./sample.pem
      when: keyout.changed

    - name: Start an instance
      amazon.aws.ec2_instance:
        name: "public-compute-instance"
        key_name: "sample"
        instance_type: t2.micro
        security_group: default
        image_id: ami-02d8bad0a1da4b6fd
        exact_count: 1
        region: us-west-2
        tags:
          Environment: Testing
```

***

## Ansible for AWS vs Previous Ansible Usage

```
PREVIOUS (config mgmt):                    THIS (cloud provisioning):
  hosts: remote targets                      hosts: localhost
  transport: SSH to targets                  transport: API calls to AWS
  gather_facts: true (need OS info)          gather_facts: false (not configuring local)
  auth: SSH keys in inventory                auth: AWS access keys in env vars
  modules: yum, apt, service, copy           modules: ec2_key, ec2_instance
  dependency: none                           dependency: boto3 + amazon.aws collection
```

***

## `register` + `when` Pattern (Reusable)

```
Task A:
  module: creates/modifies something
  register: output_var

Task B:
  module: acts on output of Task A
  uses: output_var.some.nested.value
  when: output_var.changed        ← only if Task A actually did something

Pattern: capture → conditionally act → safe for repeated runs
```

***

## Region Specification — Two Methods

```
Method 1 (per-task):     region: us-west-2         ← in each task
Method 2 (env variable): export AWS_REGION=us-west-2  ← once, applies to all tasks
```

***

## Credential Security Rules

```
✗ Never put access keys in playbook source code
✗ Never commit keys to Git repositories
✗ Never give AdministratorAccess in production
✓ Use environment variables (bashrc or CI/CD secrets)
✓ Use least-privilege IAM policies
✓ Delete keys when no longer needed
```

***

## Ansible-AWS Workflow Model

```
1. Find module → Ansible docs (cloud modules → Amazon)
2. Go to Examples section → copy example
3. Paste into playbook → modify parameters
4. Run → read error → fix (region? AMI? boto3? collection?)
5. Verify in AWS console
6. Clean up (terminate instance, delete keys)

Instructor: "Terraform is a much more better cloud management tool"
            → Ansible CAN do it, but Terraform is purpose-built for it
```

***

## Cleanup Checklist

```
□ Terminate EC2 instance (AWS Console → EC2 → Instance State → Terminate)
□ Delete key pair (AWS Console → EC2 → Key Pairs → Delete)
□ Delete local sample.pem
□ (Optional) Delete IAM user / revoke access keys
```

***

## Key Engineering Patterns

| Pattern                             | Manifestation                                                                                         |
| ----------------------------------- | ----------------------------------------------------------------------------------------------------- |
| **Localhost-as-API-client**         | Control machine doesn't SSH anywhere — it makes API calls; `hosts: localhost` + `gather_facts: false` |
| **Register-then-conditionally-act** | Capture output → use `when: .changed` to gate follow-up tasks — safe for idempotent re-runs           |
| **Return-once secret handling**     | Private key returned only on creation → must capture immediately or it's lost forever                 |
| **Idempotency via exact\_count**    | Prevents resource duplication on repeated runs — count-based convergence                              |
| **Environment-variable auth**       | Credentials in env vars (not code) — portable, secure, standard across AWS tooling                    |
| **Dependency installation chain**   | pip → boto3 → amazon.aws collection — each layer must exist before the next works                     |
| **Copy-from-docs workflow**         | Find module → copy example → modify → run → troubleshoot — the standard Ansible development loop      |

***

## Course Context

```
THIS:     Ansible managing AWS (key pair + EC2 instance)
NEXT:     Terraform (purpose-built cloud provisioning tool)
TAKEAWAY: Ansible CAN provision cloud resources, but Terraform is the preferred tool for it
          Ansible's strength = configuration management on existing servers
```

***

This completes the full reconstruction. **Theory** explains *why* Ansible-to-AWS works differently from Ansible-to-servers and the key pair return-once problem. **Practical** walks through every prerequisite, every task, every error encountered and fixed. The **Compression Map** lets you rapidly reload the entire architecture, the error-fix chain, and the reusable `register` + `when` pattern. Let me know if you'd like Anki flashcards or any section expanded! 🚀
