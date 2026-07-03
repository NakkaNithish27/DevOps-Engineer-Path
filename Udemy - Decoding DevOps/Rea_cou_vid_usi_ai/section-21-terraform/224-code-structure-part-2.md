# Terraform Code Structure Part 2 — Writing the EC2 Instance Resource

**Source:** Video caption file — *"Code Structure Part 2"* (from a Terraform / Infrastructure as Code course) [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — Context: What Has Already Been Built

Before this lecture begins, three Terraform files already exist from Part 1. Understanding their state is essential because the instance resource we are about to write **depends on all three**. [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

**`provider.tf`** — Declares AWS as the provider and specifies the region (US East 1). This tells Terraform which cloud platform to interact with and where geographically to create resources.

**`keypair.tf`** — Defines an AWS key pair resource named `dove-key`. The public key content was generated using the `ssh-keygen` command and copied into the `public_key` argument. This key pair will be associated with EC2 instances for SSH access.

**`securitygroup.tf`** (or equivalent) — Defines a security group named `dove-sg` with four rules: two **ingress** (inbound) rules — port 22 (SSH) allowed from the user's IP only, port 80 (HTTP) allowed from anywhere — and two **egress** (outbound) rules — all traffic allowed for both IPv4 and IPv6. [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

Now, in this lecture, the fourth file — **`instance.tf`** — is created to define the EC2 instance that will use the key pair and security group already defined. The instance resource ties everything together.

***

## 1.2 — The Terraform Resource Block: `aws_instance`

In Terraform, infrastructure components are defined as **resources**. Each resource has a type (what kind of infrastructure) and a name (your local identifier for it). The EC2 instance resource type is `aws_instance`. [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

```hcl
resource "aws_instance" "web" {
  ami           = ...
  instance_type = ...
  ...
}
```

`"aws_instance"` is the **resource type** — it tells Terraform this is an EC2 instance. `"web"` is the **local resource name** — your label for this specific instance within the Terraform configuration. The combination `aws_instance.web` is how you reference this resource elsewhere in your code. [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

***

## 1.3 — Arguments vs. Attribute References: A Critical Distinction

The video explicitly teaches one of the most important conceptual distinctions in Terraform: the difference between **argument references** and **attribute references**. [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

**Argument references** are the **inputs** — the values you provide in your code to tell Terraform how to create the resource. When you write `ami = "ami-12345"` or `instance_type = "t3.micro"`, those are arguments. You are giving Terraform information it needs to create the resource. In the documentation, these are listed under "Argument Reference." [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

**Attribute references** are the **outputs** — values that only exist **after** the resource is created. Things like the instance's ID, its public IP address, its private DNS name. You don't provide these; AWS generates them when the resource is created, and Terraform stores them in the state file. In the documentation, these are listed under "Attribute Reference."

The video warns: "Make sure you check the argument references when you're writing the code." When you're looking at the documentation for `aws_instance` and you see fields listed, you must check whether each field is an argument (something you provide) or an attribute (something Terraform gives you after creation). Confusing the two leads to code that doesn't work. [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

🔍 **Deep Dive:**
The state file is where attribute references are stored. When Terraform creates an `aws_instance`, AWS returns information about the created instance (its ID, public IP, etc.). Terraform records all of this in the state file. Other resources can then reference these attributes. For example, if a DNS record needs the instance's public IP, it can reference `aws_instance.web.public_ip` — but that value only exists after the instance is created. Terraform's dependency graph handles the ordering automatically. [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

***

## 1.4 — Mandatory vs. Optional Arguments

Not all arguments are required. The documentation marks each argument as either **required** or **optional**. [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

**Mandatory arguments** must be provided or Terraform will refuse to create the resource. For `aws_instance`, the `ami` (which machine image to use) is essential — without it, Terraform doesn't know what operating system to install.

**Optional arguments** have sensible defaults or represent features you may not need. The video explicitly notes that `key_name` is optional: "It says optional. So it's not mandatory. So if you don't mention, you don't have the key." Similarly, `vpc_security_group_ids` is optional — "if you don't mention this, it's going to use the default security group." [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

The video's observation: "Most of the argument references will be optional, some will be mandatory." This sets the right expectation — when reading Terraform docs, you'll see many arguments, but only a few are required. Focus on the required ones first, then add optional ones based on your specific needs. [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

***

## 1.5 — Cross-Resource References: How Resources Connect

This is the most architecturally important concept in this lecture. Terraform resources don't exist in isolation — they reference each other, creating a **dependency graph**. [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

**AMI reference:** The `ami` argument doesn't use a hardcoded AMI ID string. Instead, it references a data source from another file: `aws_ami.amiID.id`. This means: "Get the value of the `id` attribute from the `aws_ami` data source named `amiID`." The AMI data source was defined in an earlier file (`instance_id.tf` or equivalent) that looks up the correct AMI dynamically. [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

**Key pair reference:** The `key_name` argument can be given as a direct string (`"dove-key"`) or as a resource reference (`aws_key_pair.dove-key.key_name`). Both work — the string approach is simpler, the reference approach is more robust because if the key pair name changes, the reference updates automatically. [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

**Security group reference:** The `vpc_security_group_ids` argument references the security group resource: `aws_security_group.dove-sg.id`. This fetches the security group's ID from the security group resource. [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

The video makes an explicit and important warning about references: **"Don't put this into the double quotes because it's not a string. The value of this will be a string, but this basically is the variable."** When you write `aws_security_group.dove-sg.id`, Terraform treats it as a reference — it resolves it to the actual ID value at execution time. If you wrap it in quotes (`"aws_security_group.dove-sg.id"`), Terraform treats it as a literal string, not a reference, and your code breaks. [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

🔍 **Deep Dive:**
Cross-resource references create **implicit dependencies**. When Terraform sees that `aws_instance.web` references `aws_security_group.dove-sg.id`, it understands that the security group must be created **before** the instance. You don't need to explicitly declare this ordering — Terraform infers it from the references and builds a dependency graph. This is a core design principle of Terraform: the dependency graph is derived from the code structure itself. [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

***

## 1.6 — The `list` Type Hint in Documentation

When the documentation says an argument accepts a **"list of"** values, Terraform expects the value in **square brackets** `[]`. [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

The video highlights this for `vpc_security_group_ids`: "It says list of security group IDs. Whenever it says list here, to give it in the square bracket, the value should be in the square bracket." [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

```hcl
vpc_security_group_ids = [aws_security_group.dove-sg.id]
```

Even if you're providing only one security group, it must be in square brackets because the argument expects a list. This directly connects to the Python data types covered earlier in the course — a list in Terraform HCL uses the same `[]` syntax as a Python list. [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

***

## 1.7 — Availability Zone: Region vs. Zone Relationship

The `availability_zone` argument specifies which specific zone within the region to launch the instance in. The video sets it to `"us-east-1a"`. [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

The relationship: the **region** is set in `provider.tf` as `us-east-1`. Availability zones are subdivisions of a region — `us-east-1a`, `us-east-1b`, `us-east-1c`, etc. The zone you specify must exist within the provider's region. The video warns: "This should exist. I cannot give here anything." If you specify a zone that doesn't exist or isn't in the configured region, Terraform will fail. [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

***

## 1.8 — Tags: Metadata for Resource Identification

Tags are key-value pairs attached to AWS resources for identification, organization, and cost tracking. The video adds two tags to the instance: [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

```hcl
tags = {
  Name    = "Dove-Instance"
  Project = "Dove-web"
}
```

`Name` is a special tag in AWS — it's what appears as the instance name in the EC2 console. `Project` is a custom tag for organizational grouping. The video notes: "We can give as many as we want" — there's no limit on the number of tags (up to AWS's per-resource tag limit). [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

***

## 1.9 — The Documentation Workflow: How to Find Arguments

The video demonstrates a practical workflow for writing Terraform resources using documentation: [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

1. Search the Terraform AWS provider documentation (e.g., search "EC2 space instance").
2. Find the resource page (`aws_instance`).
3. Look at the basic example to understand the minimum structure.
4. Scroll to the **Argument Reference** section to find all available arguments.
5. Use the browser's `Ctrl+F` (find) to search for specific arguments by name (e.g., searching `key_pair` to find `key_name`).
6. Check whether each argument is mandatory or optional.
7. Check the expected type (string, list, map, etc.).
8. Add arguments to your code one by one based on your needs.

The video states: "We'll get the minimum information and then we'll find the arguments and then we'll mention it one by one." This is the practical reality of writing Terraform — you start with the minimal required structure and incrementally add arguments from the documentation. [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are writing the `instance.tf` file — the Terraform resource definition for an EC2 instance that uses the key pair, security group, and AMI data source already defined in previous files. The final outcome: a complete Terraform configuration that, when executed, will create an EC2 instance in `us-east-1a` with SSH access via the `dove-key` key pair, protected by the `dove-sg` security group, tagged for identification. Execution itself happens in the next lecture. [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

***

## File Context (Already Exists)

```
provider.tf       → AWS provider, region us-east-1
keypair.tf        → aws_key_pair "dove-key", public key from ssh-keygen
securitygroup.tf  → aws_security_group "dove-sg", 4 rules (22/myIP, 80/anywhere, egress all)
instance_id.tf    → aws_ami data source "amiID" (AMI lookup)
```

We are now creating: **`instance.tf`** [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

***

### Step 1: Find the Resource Documentation

**What we are doing:** Locating the Terraform documentation for the `aws_instance` resource to understand its arguments.

**Execution:**

1. Go to the Terraform AWS provider documentation.
2. Search for **"EC2 space instance"**.
3. Under Elastic Compute Cloud resources, find **`aws_instance`**. [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)
4. The first example shows how to find the AMI ID and the basic resource structure.

**Connection to flow:** The documentation is your reference for every argument you'll add in the following steps.

***

### Step 2: Write the Resource Block with AMI and Instance Type

**What we are doing:** Creating the `aws_instance` resource with the minimum required arguments.

```hcl
resource "aws_instance" "web" {
  ami           = aws_ami.amiID.id
  instance_type = "t3.micro"
}
```

**Breakdown:**

* `resource "aws_instance" "web"` — declares an EC2 instance resource with local name `web`.
* `ami = aws_ami.amiID.id` — references the AMI data source defined in another file. `aws_ami` is the data source type, `amiID` is its local name, `.id` is the attribute that returns the actual AMI ID string. This is a **cross-resource reference**, not a hardcoded string — no quotes around it. [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)
* `instance_type = "t3.micro"` — a direct string value specifying the instance size.

**IDE behavior:** When you type `aws_ami.amiID.` and press dot, the IDE should show autocomplete with available attributes like `id`. This helps you discover the correct attribute name. [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

***

### Step 3: Add the Key Pair

**What we are doing:** Associating the `dove-key` key pair with the instance for SSH access.

**How to find the argument:** In the documentation page, use `Ctrl+F` and search for `key_pair`. You'll find `key_name` under argument references. It says: "Optional. Key name of the key pair to use for the instance." [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

```hcl
  key_name = aws_key_pair.dove-key.key_name
```

**Breakdown:**

* `key_name` — the argument name (found in documentation).
* `aws_key_pair.dove-key.key_name` — a cross-resource reference to the key pair resource defined in `keypair.tf`. It fetches the `key_name` attribute from the `dove-key` key pair resource. [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

**Alternative (simpler but less robust):**

```hcl
  key_name = "dove-key"
```

This directly provides the key name as a string. Both work. The reference approach is preferred because it creates an explicit dependency and updates automatically if the key pair name changes. [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

**Common mistake:** Using `key_pair` as the argument name (it's `key_name`, not `key_pair` — the documentation is the source of truth).

***

### Step 4: Add the Security Group

**What we are doing:** Attaching the `dove-sg` security group to the instance.

**How to find the argument:** In the documentation, search for `security_group`. You'll find `vpc_security_group_ids`. It says: "Optional. List of security group IDs." [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

```hcl
  vpc_security_group_ids = [aws_security_group.dove-sg.id]
```

**Breakdown:**

* `vpc_security_group_ids` — the argument name.
* `[...]` — **square brackets are mandatory** because the documentation says "list of." Even for a single security group, it must be in a list.
* `aws_security_group.dove-sg.id` — cross-resource reference to the security group's ID. `aws_security_group` is the resource type, `dove-sg` is the local name, `.id` is the attribute that returns the AWS-generated security group ID. [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

**Critical warning from the video:** "Don't put this into the double quotes because it's not a string. The value of this will be a string, but this basically is the variable."

* ✅ Correct: `[aws_security_group.dove-sg.id]` — Terraform resolves the reference to the actual ID.
* ❌ Wrong: `["aws_security_group.dove-sg.id"]` — Terraform treats this as a literal string, not a reference. [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

**Common mistake:** Forgetting the square brackets. Without `[]`, Terraform raises a type error because it expects a list, not a single value.

**Common mistake:** Wrapping the reference in quotes, turning it into a dead string.

***

### Step 5: Add the Availability Zone

**What we are doing:** Specifying which availability zone within the region to launch the instance.

```hcl
  availability_zone = "us-east-1a"
```

**Breakdown:**

* `availability_zone` — the argument name.
* `"us-east-1a"` — a string value. This is a direct value, not a reference, so it goes in quotes.
* The zone must exist within the provider's region (`us-east-1` in `provider.tf`). `us-east-1a` is a valid zone within `us-east-1`. [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

**How to verify the zone is valid:** The zone must be a real AWS availability zone within your configured region. You cannot invent zone names.

**Common mistake:** Specifying a zone that doesn't match the provider's region (e.g., `us-west-2a` when the provider is `us-east-1`).

***

### Step 6: Add Tags

**What we are doing:** Adding metadata tags to the instance for identification and organization.

```hcl
  tags = {
    Name    = "Dove-Instance"
    Project = "Dove-web"
  }
```

**Breakdown:**

* `tags` — the argument. It accepts a **map** (key-value pairs in curly braces — same as a Python dictionary).
* `Name = "Dove-Instance"` — the `Name` tag is special in AWS; it appears as the instance name in the EC2 console.
* `Project = "Dove-web"` — a custom tag for project identification. [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

**You can add as many tags as needed** — the video notes "we can give as many as we want."

***

### Complete `instance.tf` File

```hcl
resource "aws_instance" "web" {
  ami                    = aws_ami.amiID.id
  instance_type          = "t3.micro"
  key_name               = aws_key_pair.dove-key.key_name
  vpc_security_group_ids = [aws_security_group.dove-sg.id]
  availability_zone      = "us-east-1a"

  tags = {
    Name    = "Dove-Instance"
    Project = "Dove-web"
  }
}
```

 [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

**What happens next:** The video states that execution (`terraform plan`, `terraform apply`) and experimentation (making changes and observing effects) will happen in the next lecture. This lecture is purely about writing the code correctly.

**How to verify (before execution):** Review each argument — confirm AMI reference points to a valid data source, key name matches the key pair resource, security group reference matches the security group resource, availability zone is within the provider's region, tags are correct.

⚠️ **Expert Note:**
The video mentions one more thing to add — "the state of the instance" — which will be covered in the next lecture. This likely refers to controlling whether the instance should be `running` or `stopped` after creation, or using lifecycle rules. The current code is complete for instance creation but may be extended with state management in the following session. [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## System Identity

```
TOPIC:    Terraform EC2 Instance Resource (Code Structure Part 2)
PURPOSE:  Write instance.tf that references key pair, security group, and AMI
CONTEXT:  Fourth file in a multi-file Terraform project
STATUS:   Code written, execution in NEXT lecture
```

 [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

***

## File Architecture (Complete Project)

```
provider.tf        → AWS provider, region us-east-1
keypair.tf         → aws_key_pair "dove-key" (public key from ssh-keygen)
securitygroup.tf   → aws_security_group "dove-sg" (22/myIP, 80/any, egress all)
instance_id.tf     → aws_ami data source "amiID" (dynamic AMI lookup)
instance.tf        → aws_instance "web" ← THIS LECTURE

DEPENDENCY FLOW:
  provider.tf ──────────────────────────────┐
  keypair.tf ── dove-key.key_name ──────────┤
  securitygroup.tf ── dove-sg.id ───────────┼──→ instance.tf (aws_instance "web")
  instance_id.tf ── amiID.id ──────────────┘
```

 [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

***

## Resource Block Structure

```
resource "aws_instance" "web" {
  ami                    = aws_ami.amiID.id              ← REFERENCE (no quotes)
  instance_type          = "t3.micro"                    ← STRING (quotes)
  key_name               = aws_key_pair.dove-key.key_name← REFERENCE (no quotes)
  vpc_security_group_ids = [aws_security_group.dove-sg.id]← LIST [ ] + REFERENCE
  availability_zone      = "us-east-1a"                  ← STRING (quotes)
  tags = {                                               ← MAP { }
    Name    = "Dove-Instance"
    Project = "Dove-web"
  }
}
```

 [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

***

## Arguments vs. Attributes (Critical Distinction)

```
ARGUMENT REFERENCES (inputs — YOU provide):
  ├── ami, instance_type, key_name, vpc_security_group_ids, availability_zone, tags
  ├── Found in docs under "Argument Reference"
  ├── Mandatory or Optional (check docs)
  └── Written in your .tf code

ATTRIBUTE REFERENCES (outputs — AWS generates AFTER creation):
  ├── id, public_ip, private_dns, etc.
  ├── Found in docs under "Attribute Reference"
  ├── Stored in Terraform state file
  └── Referenced BY other resources (e.g., aws_instance.web.public_ip)

⚠️ Don't confuse inputs with outputs when reading docs
```

 [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

***

## Cross-Resource Reference Syntax

```
PATTERN: resource_type.resource_name.attribute

EXAMPLES:
  aws_ami.amiID.id                    → AMI ID from data source
  aws_key_pair.dove-key.key_name      → key name from key pair resource
  aws_security_group.dove-sg.id       → SG ID from security group resource

RULES:
  ✅ No quotes around references:  ami = aws_ami.amiID.id
  ❌ Quotes make it a dead string: ami = "aws_ami.amiID.id"

  "The value of this will be a string, but this basically is the variable"
```

 [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

***

## Type Hints from Documentation

```
DOC SAYS          TERRAFORM SYNTAX        PYTHON EQUIVALENT
─────────         ────────────────        ─────────────────
"string"          = "value"               str
"list of ..."     = [value1, value2]      list [ ]
"map"             = { key = "value" }     dict { }

RULE: "list of" → MUST use square brackets, even for single item
      [aws_security_group.dove-sg.id]  ← one item, still in [ ]
```

 [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

***

## Documentation Workflow

```
1. Search Terraform AWS provider docs for resource type
2. Find resource page (e.g., aws_instance)
3. Check basic example → understand minimum structure
4. Go to Argument Reference section
5. Ctrl+F to find specific arguments by name
6. Check: mandatory or optional?
7. Check: expected type (string, list, map)?
8. Add arguments to code one by one
```

 [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

***

## Mandatory vs. Optional Pattern

```
MANDATORY:
  ami            → which OS image (no default possible)
  instance_type  → which size (no sensible default)

OPTIONAL (with consequences if omitted):
  key_name       → omit = no SSH access
  vpc_security_group_ids → omit = uses DEFAULT security group
  availability_zone → omit = AWS picks one in the region
  tags           → omit = no metadata labels

"Most of the argument references will be optional, some will be mandatory"
```

 [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

***

## Availability Zone ↔ Region Constraint

```
provider.tf: region = "us-east-1"

VALID zones:   us-east-1a, us-east-1b, us-east-1c, ...
INVALID zones: us-west-2a (wrong region), us-east-1z (doesn't exist)

RULE: Zone must exist AND be within the provider's region
```

 [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

***

## Implicit Dependency Graph (From References)

```
aws_ami.amiID ─────────────────┐
                                │
aws_key_pair.dove-key ─────────┼──→ aws_instance.web
                                │
aws_security_group.dove-sg ────┘

Terraform INFERS creation order from references:
  1. Create key pair + security group + resolve AMI (parallel, no deps on each other)
  2. Create instance (depends on all three)

NO explicit ordering needed — references CREATE the dependency graph
```

 [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

***

## Reusable Engineering Patterns

| Pattern                              | Manifestation                                                                               |
| ------------------------------------ | ------------------------------------------------------------------------------------------- |
| **Reference Over Hardcode**          | `aws_key_pair.dove-key.key_name` instead of `"dove-key"` — auto-updates, creates dependency |
| **Implicit Dependency Graph**        | Cross-resource references → Terraform infers creation order automatically                   |
| **Input/Output Separation**          | Argument references (you provide) vs. Attribute references (system generates)               |
| **Documentation-Driven Development** | Find arguments in docs → add one by one → verify type and optionality                       |
| **Type-Aware Values**                | Strings in quotes, references without quotes, lists in `[]`, maps in `{}`                   |
| **Incremental Construction**         | Start with minimum required → add optional arguments based on needs                         |
| **Multi-File Organization**          | Each concern (provider, keypair, SG, instance) in its own `.tf` file                        |

 [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

***

## One-Line System Reconstruction

> **The `instance.tf` file defines `aws_instance "web"` with cross-resource references to `aws_ami.amiID.id` (AMI), `aws_key_pair.dove-key.key_name` (SSH), and `[aws_security_group.dove-sg.id]` (firewall, in list brackets), plus string values for availability zone (`us-east-1a`) and tags — where references must never be quoted (they're variables not strings), list-type arguments require `[]`, and Terraform automatically infers the creation dependency graph from these references.** [\[224-code-s...ure-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/224-code-structure-part-2.txt)

***

This completes the full reconstruction of the Terraform Code Structure Part 2 lecture. It builds directly on Part 1 (where provider, key pair, and security group were defined) and leads into the next lecture where `terraform plan` and `terraform apply` will execute this configuration and the instructor will experiment with changes. Let me know if you'd like any section expanded or adjusted! 🚀
