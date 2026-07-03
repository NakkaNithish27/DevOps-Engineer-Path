# 🎓 Deep Learning Material: Basics of Terraform — Data Sources, Code Structure & Execution Workflow

**Source:** [222-basics-of-terraform.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt?EntityRepresentationId=2f575405-b001-414f-9779-0dc8a52bc7ba) (video caption) + [222.InstID.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222.InstID.txt?EntityRepresentationId=85c1b909-dae9-4052-b7f5-63b4f26174d0) (Terraform code file) — First hands-on Terraform lecture covering AMI ID discovery methods, the Terraform data source concept, code structure (data blocks, output blocks, arguments, filters), the Terraform execution workflow (`fmt → init → validate → plan → apply`), and how Terraform downloads provider plugins from the Terraform Registry. [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt), [\[222.InstID \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222.InstID.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 The Problem: Finding an AMI ID

To launch an EC2 instance on AWS — whether manually or through automation — you need an **AMI ID** (Amazon Machine Image ID). The AMI ID uniquely identifies the operating system image that the instance will boot from. But AMI IDs are not simple, memorable strings. They look like `ami-0abcdef1234567890`, and critically, **the same AMI name has a different AMI ID in every AWS region**. Ubuntu 24 HVM SSD in `us-east-1` (North Virginia) has one ID; the exact same Ubuntu 24 HVM SSD in `ap-south-1` (Mumbai) has a completely different ID. This means you cannot hardcode an AMI ID and expect it to work across regions. [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt)

The video presents four methods to find an AMI ID:

1. **AWS Console** — Click "Launch Instance," look at Quick Start, and the AMI ID is displayed next to each OS option. You can select different versions and see their IDs.
2. **Internet search** — Google "Ubuntu AMI ID" and find sites like Ubuntu's Amazon EC2 AMI Finder, which lists AMI IDs by region, version, architecture, and release date.
3. **AWS CLI** — Use the Command Line Interface to query AMI IDs programmatically.
4. **Terraform data sources** — Use Terraform itself to look up the AMI ID dynamically at execution time. [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt)

The video focuses on method 4 — using Terraform — not because it's the only way, but because it serves as the **first exercise to learn Terraform's code structure and execution model**. The AMI lookup is the vehicle; the real lesson is how Terraform code is written, structured, and executed. [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt)

***

## 1.2 Providers and Resources — Terraform's Foundation

Terraform manages infrastructure through **providers**. A provider is a plugin that gives Terraform the ability to interact with a specific platform. AWS is a provider. Google Cloud is a provider. Azure is a provider. When you write Terraform code that references AWS resources, Terraform knows it needs the AWS provider plugin to understand and execute those resources. [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt)

A **resource** in Terraform represents something you want to create, manage, or interact with on that provider's platform. Resources are **predefined** in Terraform — they are not invented by you. `aws_instance` is a resource for EC2 instances. `aws_ami` is a resource for AMI information. Each resource has a set of **arguments** (inputs you provide) and **attributes** (outputs you can read). The resource definitions, their arguments, and their attributes are all documented in the Terraform Registry documentation for each provider. [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt)

The instructor emphasizes: you do not need to memorize resource names or arguments. They are all in the documentation. What you need to understand is the **structure** — how resources, arguments, and values relate to each other. [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt)

***

## 1.3 Data Sources — Fetching Information from Outside Terraform

There are two fundamentally different things you can do with Terraform: **create/manage resources** (like launching an EC2 instance) and **read existing information** (like looking up an AMI ID that already exists in AWS). The video draws this distinction clearly.

When you want to fetch information that exists **outside of Terraform** — something you are not creating, just querying — you use a **data source**. The syntax starts with the keyword `data` instead of `resource`. In this exercise, we are not creating anything on AWS. We are just asking AWS: "What is the AMI ID for Ubuntu 22, HVM, in my current region?" The data source performs this lookup. [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt)

The general syntax of a data source block is:

```hcl
data "<RESOURCE_TYPE>" "<LOCAL_NAME>" {
  // arguments
}
```

* **`data`** — The keyword that tells Terraform this is a read-only lookup, not a create/modify operation.
* **`<RESOURCE_TYPE>`** — The predefined Terraform resource type, in double quotes. Here it is `"aws_ami"`.
* **`<LOCAL_NAME>`** — A name **you choose** to reference this data source elsewhere in your Terraform code. Here it is `"amiID"`. This name is arbitrary — you could call it anything.
* **`{ ... }`** — The **resource block**, enclosed in curly braces. Inside this block, you provide **arguments** that configure the data source. [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt), [\[222.InstID \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222.InstID.txt)

***

## 1.4 Arguments, Filters, and Value Types

Inside the resource block, you provide **arguments** — key-value pairs that tell the data source what to look for and how to behave. Each resource type has its own set of valid arguments, documented in the Terraform provider documentation.

For `aws_ami`, the arguments used in this exercise are:

**`most_recent = true`** — A boolean argument. Since there can be multiple AMIs matching the filters (different release dates, patch versions), this tells Terraform to return only the most recent one. The value `true` is a **boolean** — not quoted. [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt), [\[222.InstID \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222.InstID.txt)

**`filter { ... }`** — A nested block (not a simple key-value pair) that defines search criteria. You can have multiple `filter` blocks. Each filter has two sub-arguments:

* `name` — The name of the AMI attribute to filter on (a string in double quotes).
* `values` — A **list** of acceptable values (in square brackets, strings in double quotes).

The first filter uses `name = "name"` (filtering on the AMI's name attribute) with `values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]`. The `*` at the end is a **wildcard** — it matches any suffix, allowing for version numbers or date stamps that vary across releases. [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt), [\[222.InstID \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222.InstID.txt)

The second filter uses `name = "virtualization-type"` with `values = ["hvm"]` — ensuring we get a hardware-virtualized image. [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt), [\[222.InstID \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222.InstID.txt)

**`owners = ["099720109477"]`** — A list argument specifying who created the AMI. The number `099720109477` is **Canonical's AWS account ID** — the company that publishes official Ubuntu AMIs. This ensures you're getting an official, trusted image, not a random community AMI with the same name. [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt), [\[222.InstID \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222.InstID.txt)

The video highlights the different **value types** that arguments can take:

* **Boolean:** `true` / `false` (no quotes) — e.g., `most_recent = true`
* **String:** Text in double quotes — e.g., `name = "name"`
* **List:** Square brackets containing multiple values separated by commas — e.g., `values = ["hvm"]`. Lists can contain strings, booleans, or other types depending on the argument.

The instructor explicitly compares lists in Terraform to lists in Python — square bracket notation, comma-separated values. [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt)

***

## 1.5 Output Blocks — Printing Results

After the data source fetches information, you need a way to **see** the result. Terraform uses **output blocks** for this. The instructor compares it directly: "Output is just like `print` we have in Python, we have `echo` in Bash, like that in Terraform we have output." [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt)

The output block syntax:

```hcl
output "<OUTPUT_NAME>" {
  description = "..."
  value       = <expression>
}
```

* **`output`** — The keyword.
* **`<OUTPUT_NAME>`** — A name you choose for this output (e.g., `"instance_id"`).
* **`description`** — A human-readable string describing what this output represents. Optional but good practice.
* **`value`** — The actual data to print. This is an **expression** that references data from elsewhere in the Terraform code. [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt), [\[222.InstID \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222.InstID.txt)

The value expression `data.aws_ami.amiID.id` is a **reference chain** that navigates Terraform's internal data structure:

```
data          → it's a data source (not a resource)
  .aws_ami    → the resource type
  .amiID      → the local name we gave it
  .id         → the specific attribute we want (the AMI ID)
```

When Terraform executes the data source, it fetches a whole set of attributes about the AMI — ID, description, boot mode, architecture, and more. The `.id` at the end selects just the AMI ID from all that information. The video explicitly compares this to fetching values from a Python dictionary — you navigate through layers of keys to reach the specific value you need. [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt)

🔍 **Deep Dive**
The VS Code Terraform extension provides **autocomplete** for these reference chains. After typing `data.aws_ami.amiID.`, the extension shows all available attributes (id, description, boot\_mode, architecture, etc.). Without the extension, you would need to look up available attributes in the Terraform provider documentation. This is why the extension installation — while not mandatory — is practically valuable. [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt)

***

## 1.6 The Terraform Execution Workflow

Terraform is not a scripting language where you write code and it runs top-to-bottom immediately. It has a **multi-step execution workflow** with distinct phases, each serving a specific purpose. The video walks through every step and explains why each exists.

### `terraform fmt` — Format

This command checks and corrects the **formatting** (indentation, alignment, spacing) of all `.tf` files in the current directory. It does not check correctness — only style. If your indentation is inconsistent, `fmt` fixes it to Terraform's standard format. The video demonstrates this: after running `fmt`, some indentation shifts from where the instructor originally placed it to where Terraform's standard expects it. [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt)

### `terraform init` — Initialize

This is the **first command you must run** before doing anything else with Terraform. When you run `terraform init`, Terraform reads all `.tf` files in the current directory, identifies which **providers** are needed based on the resources you've used (e.g., it sees `aws_ami` and determines the AWS provider is needed), and **downloads the provider plugins** from the **Terraform Registry**. [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt)

The video shows the output: "Finding latest version of hashicorp/aws... Installing hashicorp/aws..." This download is what gives Terraform the ability to understand AWS-specific resources, their arguments, and how to communicate with the AWS API. Without `init`, Terraform has no provider plugins and cannot understand your code. [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt)

The video also demonstrates this dependency: running `terraform validate` before `terraform init` **fails** because Terraform hasn't downloaded the provider information yet and doesn't know what `aws_ami` is. `init` must come first. [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt)

### `terraform validate` — Validate

After initialization, `validate` checks whether your code is **syntactically correct** — are the arguments valid for the resource type? Are the values the right type? Are required arguments present? It does not connect to AWS or check real-world state. It only checks your code against the provider's schema (which was downloaded during `init`). The video runs it and gets: "Configuration is valid." [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt)

### `terraform plan` — Plan

This is the **impact assessment** step. `plan` connects to the real provider (AWS) and determines **what will happen** if you apply the code. It shows what will be created, modified, or destroyed. The instructor emphasizes this strongly: "You don't want to delete a few things unnecessarily. So you need to check what is going to happen when I apply it." [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt)

For this exercise (which only reads data and produces output, creating nothing), the plan shows: reading the data source, and the output value that will be produced. No resources will be added, changed, or destroyed. But the instructor notes: "Next lectures this will make more sense" — when you're creating actual infrastructure, `plan` becomes critical because it shows you if your code would accidentally destroy existing resources. [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt)

The video points out that the plan itself already shows the AMI ID in its output — you can see the result even before applying. [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt)

### `terraform apply` — Apply

This is the **execution** step. `apply` performs the actions described in the plan. It first re-displays the plan, then asks for confirmation: "Are you okay with this action?" You must type `yes` to proceed. The instructor warns: if the plan shows it will destroy or modify things, **read everything carefully** before confirming. Only say yes if you understand and accept the impact. [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt)

After confirmation, Terraform executes and shows: "Apply complete! Resources: 0 added, 0 changed, 0 destroyed." Plus the output block's value — the AMI ID. [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt)

⚠️ **Expert Note**
The `plan → apply` separation is a critical safety mechanism. In production Terraform workflows, the plan output is often saved to a file, reviewed by a team (sometimes through pull request reviews), and only then applied. This prevents unintended infrastructure destruction. The interactive `yes` confirmation is the simplest form of this safety gate, but CI/CD pipelines use more structured approval workflows. [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt)

***

## 1.7 The `.tf` File Convention

Terraform reads **all** `.tf` files in the current directory. The filename itself does not matter to Terraform — you could name the file anything as long as it ends in `.tf`. The video names the file `InstID.tf` (for "Instance ID"), but the instructor notes the name is the user's choice. What matters is the `.tf` extension and the directory you're in when you run Terraform commands. [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are writing our first Terraform code to dynamically look up an Ubuntu AMI ID from AWS using a data source, and printing it using an output block. This exercise is not about creating infrastructure — it is about learning Terraform's code structure and execution workflow. The final outcome: running `terraform apply` displays the correct AMI ID for Ubuntu 22 (Jammy) in your current AWS region. [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt)

***

## Step 1: Set Up the Working Environment

**1a. Create a project folder:**

Create a folder for your Terraform code. The video uses `F:\Terraform\exercise1`. The name is your choice — what matters is that you work inside this directory. [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt)

**1b. Open the folder in VS Code:**

File → Open Folder → select your folder. [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt)

**1c. Install the Terraform extension (optional but recommended):**

Click the Extensions icon in VS Code → search "Terraform" → install **HashiCorp Terraform**. This extension provides formatting help and **autocomplete** for resource attributes (e.g., after typing `data.aws_ami.amiID.`, it lists available attributes like `id`, `description`, `architecture`). Not mandatory, but practically valuable. [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt)

***

## Step 2: Create the Terraform File

Click the new file icon in VS Code's explorer panel (inside your exercise1 folder). Name it:

```
InstID.tf
```

The `.tf` extension is **required** — Terraform only reads files with this extension. The filename before `.tf` is your choice. [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt)

***

## Step 3: Write the Data Source Block

This block tells Terraform to look up an AMI ID from AWS.

```hcl
data "aws_ami" "amiID" {
  most_recent = true
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
  owners = ["099720109477"]
}
```

 [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt), [\[222.InstID \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222.InstID.txt)

Breaking down each element:

| Element                                       | Purpose                                                                  |
| --------------------------------------------- | ------------------------------------------------------------------------ |
| `data`                                        | Keyword: fetch existing information (read-only, no creation)             |
| `"aws_ami"`                                   | Resource type: predefined in Terraform's AWS provider for AMI lookups    |
| `"amiID"`                                     | Local name: your chosen reference label for this data source             |
| `most_recent = true`                          | Argument: if multiple AMIs match, return only the newest                 |
| `filter { name = "name" ... }`                | Filter: search by AMI name pattern; `*` wildcard allows any suffix       |
| `filter { name = "virtualization-type" ... }` | Filter: only HVM virtualization type                                     |
| `owners = ["099720109477"]`                   | Argument: Canonical's AWS account ID — ensures official Ubuntu AMIs only |

**Where the filter values come from:** The AMI name pattern (`ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*`) matches what you see in the AWS console or AMI finder websites. The owner ID (`099720109477`) is Canonical's public AWS account ID, found in AWS documentation or Ubuntu's AMI documentation. [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt)

***

## Step 4: Write the Output Block

After the data block (after its closing `}`), add:

```hcl
output "instance_id" {
  description = "AMI ID of Ubuntu instance"
  value       = data.aws_ami.amiID.id
}
```

 [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt), [\[222.InstID \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222.InstID.txt)

| Element                         | Purpose                                            |
| ------------------------------- | -------------------------------------------------- |
| `output`                        | Keyword: print/display a value after execution     |
| `"instance_id"`                 | Name for this output (your choice)                 |
| `description`                   | Human-readable label (optional, good practice)     |
| `value = data.aws_ami.amiID.id` | Reference chain navigating to the AMI ID attribute |

The reference chain `data.aws_ami.amiID.id` reads as: from the `data` source of type `aws_ami` named `amiID`, get the `.id` attribute. The data source fetches many attributes; `.id` selects just the AMI ID. [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt)

**Save the file** (`Ctrl + S`).

***

## Step 5: Open a Terminal and Navigate to Your Directory

In VS Code: Terminal → New Terminal. [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt)

The video uses **Git Bash**. If your default is PowerShell or Command Prompt, you can switch from the terminal dropdown, or use whichever terminal you prefer — all work.

Verify you're in the right directory:

```bash
ls
```

**Expected output:** You should see `InstID.tf` listed. If not, `cd` to the correct directory. [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt)

***

## Step 6: `terraform fmt` — Format the Code

```bash
terraform fmt
```

| Part        | Purpose                                                                                                 |
| ----------- | ------------------------------------------------------------------------------------------------------- |
| `terraform` | The Terraform CLI binary                                                                                |
| `fmt`       | Subcommand: format — standardizes indentation and alignment in all `.tf` files in the current directory |

**What happens:** Terraform reads all `.tf` files, adjusts whitespace and alignment to its standard style, and prints the names of any files it modified. If nothing needed changing, no output. [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt)

**Expected behavior:** The video shows indentation shifting to align with Terraform's standard. This is a cosmetic step — it does not validate logic.

***

## Step 7: `terraform init` — Initialize

```bash
terraform init
```

| Part        | Purpose                                                                                                                           |
| ----------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `terraform` | The CLI binary                                                                                                                    |
| `init`      | Subcommand: initialize — reads `.tf` files, identifies required providers, downloads provider plugins from the Terraform Registry |

 [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt)

**What happens internally:**

1. Terraform scans all `.tf` files in the current directory.
2. It detects that `aws_ami` belongs to the `hashicorp/aws` provider.
3. It downloads the AWS provider plugin from the Terraform Registry.
4. It creates a `.terraform/` directory to store the downloaded plugin.
5. It creates a `.terraform.lock.hcl` file to lock the provider version.

**Expected output:**

```
Finding latest version of hashicorp/aws...
Installing hashicorp/aws v5.x.x...
Terraform has been successfully initialized!
```

 [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt)

⚠️ **Critical ordering:** `init` must run before `validate`, `plan`, or `apply`. The video demonstrates this by showing that `terraform validate` fails if run before `init` — Terraform doesn't yet know what `aws_ami` is without the downloaded provider plugin. [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt)

**Common mistake:** Running `validate` or `plan` before `init`. Error message will indicate that the provider is not installed.

***

## Step 8: `terraform validate` — Validate Syntax

```bash
terraform validate
```

| Part        | Purpose                                                                                    |
| ----------- | ------------------------------------------------------------------------------------------ |
| `terraform` | The CLI binary                                                                             |
| `validate`  | Subcommand: checks all `.tf` files for syntactic correctness against the provider's schema |

**What it checks:** Are the resource types valid? Are the arguments correct for each resource type? Are the value types correct (boolean where boolean is expected, string where string is expected)? Are required arguments present?

**What it does NOT check:** It does not connect to AWS. It does not verify that the AMI actually exists. It only validates code structure.

**Expected output:** `Success! The configuration is valid.` [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt)

***

## Step 9: `terraform plan` — Preview Impact

```bash
terraform plan
```

| Part        | Purpose                                                                                                                     |
| ----------- | --------------------------------------------------------------------------------------------------------------------------- |
| `terraform` | The CLI binary                                                                                                              |
| `plan`      | Subcommand: connects to the provider (AWS), reads current state, and shows what changes would occur if you applied the code |

**What happens:**

1. Terraform connects to AWS using your configured credentials.
2. It executes the data source lookup (reads the AMI information).
3. It compares the desired state (your code) with the current state.
4. It displays what will be added, changed, or destroyed.

**Expected output for this exercise:**

```
data.aws_ami.amiID: Reading...
data.aws_ami.amiID: Read complete

Changes to Outputs:
  + instance_id = "ami-0abcdef1234567890"
```

No resources added, changed, or destroyed — because we're only reading data and printing output. The AMI ID appears in the plan itself. [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt)

**Connection to larger flow:** In future exercises where you create real infrastructure, `plan` becomes your safety net. It shows you exactly what Terraform will do before it does it — including whether it will **destroy** existing resources. Always read the plan carefully before applying.

***

## Step 10: `terraform apply` — Execute

```bash
terraform apply
```

| Part        | Purpose                                                         |
| ----------- | --------------------------------------------------------------- |
| `terraform` | The CLI binary                                                  |
| `apply`     | Subcommand: executes the planned changes; requires confirmation |

**What happens:**

1. Terraform re-runs the plan and displays it.
2. It prompts: `Do you want to perform these actions? Enter a value: `
3. You type **`yes`** and press Enter.
4. Terraform executes — in this case, reading the data source and printing the output.

**Expected output:**

```
Apply complete! Resources: 0 added, 0 changed, 0 destroyed.

Outputs:

instance_id = "ami-0abcdef1234567890"
```

 [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt)

The AMI ID printed is the result — the value fetched by the data source, navigated via `data.aws_ami.amiID.id`, and displayed by the output block.

⚠️ **Expert Note**
The instructor explicitly warns: when applying code that creates, modifies, or destroys real infrastructure, **read the plan output carefully** before typing `yes`. The `yes` confirmation is your last gate. In this exercise there's no risk (0 added, 0 changed, 0 destroyed), but in real Terraform workflows, a careless `yes` can delete production resources. [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt)

***

## Step 11: Review the Full Workflow (History)

The video runs `history` to show the complete command sequence:

```
1. terraform fmt          # format code
2. terraform validate     # ← FAILED (provider not initialized)
3. terraform init         # download provider plugins
4. terraform validate     # syntax check ← now succeeds
5. terraform plan         # preview impact
6. terraform apply        # execute (with confirmation)
```

 [\[222-basics...-terraform \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222-basics-of-terraform.txt)

The correct operational order is: **fmt → init → validate → plan → apply**. The video intentionally demonstrates the wrong order (validate before init) to show why init must come first.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Terraform Execution Workflow (Core Sequence)

```
terraform fmt       → fix formatting (cosmetic, no logic check)
    │
terraform init      → read .tf files → detect providers → download plugins from Registry
    │                   ⚠️ MUST run before validate/plan/apply
    │
terraform validate  → syntax check against provider schema (no AWS connection)
    │
terraform plan      → connect to AWS → read state → show impact (add/change/destroy)
    │                   ⚠️ SAFETY GATE: read before proceeding
    │
terraform apply     → re-show plan → prompt "yes" → execute
                        ⚠️ CONFIRMATION GATE: type "yes" only after reading plan
```

***

## Code Structure — Two Block Types

```
DATA SOURCE BLOCK (read-only lookup):
┌─────────────────────────────────────────────┐
│ data "<RESOURCE_TYPE>" "<LOCAL_NAME>" {      │
│   argument = value                          │
│   filter {                                  │
│     name   = "..."                          │
│     values = ["..."]                        │
│   }                                         │
│ }                                           │
└─────────────────────────────────────────────┘

OUTPUT BLOCK (print/display):
┌─────────────────────────────────────────────┐
│ output "<OUTPUT_NAME>" {                    │
│   description = "..."                       │
│   value       = data.<type>.<name>.<attr>   │
│ }                                           │
└─────────────────────────────────────────────┘
```

***

## Reference Chain Navigation

```
data.aws_ami.amiID.id
  │      │      │    │
  │      │      │    └── attribute (what you want: id, description, architecture...)
  │      │      └── local name (you chose this)
  │      └── resource type (predefined by Terraform)
  └── keyword (data source, not resource)

Analogy: Python dictionary navigation → dict["key1"]["key2"]
```

***

## Data Source: `aws_ami` — Arguments Used

```
data "aws_ami" "amiID" {
    │
    ├── most_recent = true                          (boolean: newest match only)
    │
    ├── filter { name="name", values=["...-*"] }    (AMI name with wildcard)
    │
    ├── filter { name="virtualization-type", values=["hvm"] }
    │
    └── owners = ["099720109477"]                   (Canonical = official Ubuntu)
}
```

***

## Argument Value Types

```
Boolean:  most_recent = true          (no quotes)
String:   name = "name"              (double quotes)
List:     values = ["hvm"]           (square brackets, comma-separated)
          owners = ["099720109477"]
```

***

## AMI ID — Critical Property

```
AMI ID is REGION-SPECIFIC
  Same AMI name → different ID per region
  Ubuntu 24 HVM SSD in us-east-1 ≠ same AMI in ap-south-1

→ Cannot hardcode AMI IDs for multi-region use
→ Data sources solve this: dynamic lookup at execution time
```

***

## `data` vs `resource` (Foundational Distinction)

```
data "aws_ami" "..."    → READ existing information (outside Terraform)
resource "aws_instance"  → CREATE/MANAGE infrastructure (by Terraform)

This lecture: data only (read AMI ID)
Next lecture: resource (launch EC2 instance)
```

***

## `terraform init` — What It Does Internally

```
Read .tf files
    │
    ▼
Detect providers needed (e.g., hashicorp/aws from aws_ami)
    │
    ▼
Download provider plugins from Terraform Registry
    │
    ▼
Store in .terraform/ directory
    │
    ▼
Create .terraform.lock.hcl (version lock)
    │
    ▼
"Terraform has been successfully initialized!"
```

***

## Why `validate` Fails Before `init`

```
validate needs provider schema to check syntax
    → provider schema comes from downloaded plugin
    → plugin downloaded during init
    → no init = no schema = validate fails

Correct: init → validate
Wrong:   validate → init
```

***

## File Convention

```
*.tf  → Terraform reads ALL .tf files in current directory
         filename doesn't matter (InstID.tf, main.tf, anything.tf)
         extension .tf is REQUIRED
         must be in the directory where you run terraform commands
```

***

## AMI Discovery Methods (Reference)

```
1. AWS Console     → Launch Instance → Quick Start → AMI ID shown
2. Internet        → Ubuntu AMI Finder (lists by region/version/arch)
3. AWS CLI         → command-line query
4. Terraform       → data "aws_ami" with filters (THIS lecture)
```

***

## The Complete Code (Reference)

```hcl
data "aws_ami" "amiID" {
  most_recent = true
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
  owners = ["099720109477"]
}

output "instance_id" {
  description = "AMI ID of Ubuntu instance"
  value       = data.aws_ami.amiID.id
}
```

 [\[222.InstID \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/222.InstID.txt)

***

## Key Engineering Patterns

| Pattern                                     | Manifestation                                                                                           |
| ------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| **Dynamic lookup over hardcoding**          | Data source fetches AMI ID at runtime — handles region differences, version changes automatically       |
| **Declarative intent**                      | You describe WHAT you want (Ubuntu, HVM, most recent) not HOW to find it — Terraform resolves it        |
| **Multi-phase execution with safety gates** | fmt → init → validate → plan → apply — each phase catches different classes of errors before execution  |
| **Plugin architecture**                     | Terraform core knows nothing about AWS; provider plugins downloaded at init give it AWS knowledge       |
| **Schema-driven validation**                | validate checks code against provider schema — catches errors without connecting to real infrastructure |
| **Impact preview before execution**         | plan shows add/change/destroy counts — prevents accidental destruction                                  |
| **Reference chain navigation**              | data.type.name.attribute — structured path to any piece of fetched information                          |

***

## Project Continuity

```
BEFORE: Terraform introduction, provider concepts
THIS:   First Terraform code — data source + output + execution workflow (fmt/init/validate/plan/apply)
NEXT:   Launch an EC2 instance using Terraform (resource block, not just data block)
```

***

This completes the full reconstruction. **Theory** builds understanding of data sources, providers, code structure, and the execution model. **Practical** walks through every command and every line of code with exact breakdowns. The **Compression Map** lets you mentally reload Terraform's entire structure — from block syntax to execution workflow — in under a minute. Let me know if you'd like Anki flashcards or any section expanded! 🚀
