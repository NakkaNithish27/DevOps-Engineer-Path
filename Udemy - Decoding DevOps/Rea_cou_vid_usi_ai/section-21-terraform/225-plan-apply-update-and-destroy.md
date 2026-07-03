# 🏗️ Terraform — Plan, Apply, Update & Destroy — Deep Learning Material

**Source:** *Plan, Apply, Update and Destroy* (Terraform Video Lecture Caption File) [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

## 1.1 The Terraform Execution Lifecycle — Four Phases

Terraform operates through a clear lifecycle when managing infrastructure: **init → fmt/validate → plan → apply**. And when you're done: **destroy**. Each phase has a distinct responsibility, and understanding what each phase *can and cannot catch* is the central lesson of this lecture. The instructor doesn't just walk through them — he deliberately breaks things at different phases to show where each phase's detection capabilities end and blind spots begin. [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

***

## 1.2 terraform init — Downloading Provider Libraries

`terraform init` is the first command you run in any Terraform project directory. It reads the provider configuration (e.g., `provider "aws"`) and downloads the **provider libraries** (also called provider plugins) from the Terraform Registry. These libraries are the code that knows how to communicate with AWS APIs (or any other provider). Without init, Terraform has no ability to interact with any cloud platform. [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

Init is idempotent — running it multiple times doesn't cause harm. It checks if the required libraries are already present and only downloads what's missing or needs updating.

***

## 1.3 terraform fmt — Code Formatting

`terraform fmt` automatically reformats your `.tf` files to follow Terraform's canonical style (consistent indentation, alignment, spacing). It modifies files in place and **reports which files it changed**. In this lecture, it corrects both `instance.tf` and `provider.tf`. [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

This is a non-functional step — it changes how the code looks, not what it does. But it matters for readability, team consistency, and code review.

***

## 1.4 terraform validate — Syntax and Configuration Checking

`terraform validate` checks your `.tf` files for **syntactic correctness and basic configuration validity**. It verifies that the HCL syntax is well-formed, that required arguments are present, and that value types match what's expected. [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

The instructor hits a real validation error: `"Inappropriate value for attribute ipv4. String required."` — a CIDR value was given in list format (with square brackets `[]`) instead of as a plain string. The fix is removing the square brackets. After the fix, `terraform validate` returns `"Success! The configuration is valid."` [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

**Critical limitation:** Validate checks **syntax and type correctness**, not **logical correctness**. The instructor later demonstrates that a reference to a non-existent resource name (`test-sg`) passes validation perfectly — `terraform validate` reports success because the syntax is valid HCL. The error is only caught during `terraform plan`, which actually evaluates resource references. This is an important distinction: validate is a syntax linter, not a logic checker. [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

***

## 1.5 terraform plan — The Dry Run That's Not Always Right

`terraform plan` is the most conceptually important command in Terraform's workflow. It performs a **three-way comparison**: your `.tf` code files, the **state file** (Terraform's record of what it previously created), and the **actual target infrastructure** (what currently exists in AWS). Based on this comparison, it produces a detailed report of what will happen if you apply: what will be **added**, what will be **changed**, and what will be **destroyed**. [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

The output shows a summary line: `Plan: 7 to add, 0 to change, 0 to destroy.` Each resource is listed with symbols indicating the operation: `+` for add, `~` for change, `-` for destroy. The instructor stresses a critical reading order: **always look at destroy first**. The number of resources being destroyed is the most dangerous information. Additions are safe (new things being created). Changes might be safe. But destructions can cause outages, data loss, and irreversible damage. [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

**The most important lesson in this entire lecture: plan is not always right.** The instructor states this explicitly and then proves it with a live failure. The plan said the infrastructure change was valid, but when `terraform apply` actually tried to execute it, AWS rejected the request because an availability zone from region `us-east-2` was referenced in a provider configured for `us-east-1`. The plan couldn't catch this because the zone name `us-east-2a` is syntactically valid — it exists in AWS, just not in the provider's configured region. Plan validated the syntax; only the actual API call during apply revealed the cross-region mismatch. [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

🔍 **Deep Dive:**
Why can't plan catch everything? Plan performs a **simulated execution** — it asks the provider "what would happen if I created this resource with these parameters?" But some validations can only happen during actual API calls. AWS might accept a plan-time check for a zone name's format but only validate the zone-region relationship during the actual `RunInstances` API call. This is why the instructor says: "Do not completely trust in the plan. Make sure you validate all the source code, you check it."

***

## 1.6 terraform apply — Real Execution With Real Consequences

`terraform apply` executes the plan against the real infrastructure. It first shows you the plan (same output as `terraform plan`), then asks for confirmation (`yes`). After confirmation, it creates, modifies, or destroys resources by making actual API calls to AWS. [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

After a successful apply, Terraform creates or updates the **terraform.tfstate** file — a JSON file that records every resource Terraform created, along with all its attributes (AMI ID, security group IDs, instance IDs, etc.). This state file is Terraform's memory of what it has built. The instructor recommends reading through the state file to familiarize yourself with the structure — this knowledge becomes essential later when you need to reference resource attributes or output values. [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

After apply, if you run `terraform plan` again with no code changes, the output should be `"No changes"` — because the code, the state file, and the actual infrastructure are all in sync. This is the **converged state**: everything matches. [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

***

## 1.7 Mutable vs. Immutable Changes — The Destroy-and-Recreate Behavior

This is the most operationally critical concept in the lecture. When you change a Terraform resource attribute, Terraform determines whether the change is **mutable** (can be applied in place) or **immutable** (requires destroying the resource and recreating it). [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

**Mutable changes (in-place update):** Changing a security group rule (e.g., changing the CIDR from `my_ip` to `0.0.0.0/0`) is mutable. Terraform updates the existing security group without destroying anything. Plan shows: `1 to change`. The resource continues to exist; only the rule changes. Tags and names are typically mutable too. [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

**Immutable changes (destroy + recreate):** Changing the **key pair** attached to an EC2 instance or changing the **AMI ID** are immutable. You cannot change an EC2 instance's key pair or AMI after launch — the instance must be terminated and a new one created with the new values. When plan detects an immutable change, it shows the resource as `must be replaced` with both a minus sign (destroy) and a plus sign (create). [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

The instructor demonstrates this with the key pair change: plan shows `1 to destroy` for the instance and `2 to add` (new key pair + new instance). The instance gets destroyed and recreated. This is the scenario where the instructor's warning becomes urgent: **always look at the destroy count first.** If you didn't expect any resources to be destroyed and plan shows `1 to destroy`, stop and investigate before applying.

The instructor explicitly warns: **"Terraform is great, but at the same time it's also very terrifying. If you're not careful with the execution, you may end up destroying things."** [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

⚠️ **Expert Note:**
Immutability rules vary by resource and by attribute. For EC2 instances, AMI and key pair are immutable. For security groups, rules are mutable. For VPCs, CIDR blocks are immutable. There's no universal rule — you learn which attributes are immutable through experience and documentation. The plan output always tells you whether a resource `must be replaced`, which is your signal that destruction will occur.

***

## 1.8 The Plan-Apply Divergence — When Plan Succeeds But Apply Fails

The instructor creates the most impactful demonstration in the lecture: changing the availability zone from `us-east-1a` to `us-east-2a` while keeping the provider region as `us-east-1`. [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

**What plan shows:** Destroy the existing instance (zone change is immutable), create a new instance in `us-east-2a`, add the new key pair. Plan says this is valid.

**What actually happens during apply:** Terraform destroys the existing instance successfully. Then it tries to create the new instance in `us-east-2a` — but AWS rejects it because `us-east-2a` belongs to region `us-east-2`, not `us-east-1` (the provider's configured region). **The apply fails after the destruction has already completed.** [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

The result: **the old instance is destroyed and the new instance was never created.** The infrastructure is now in a broken state — no running instance. The instructor's point: "If this happens real time, you will be sweating now. The instance is destroyed and you don't have any other instance."

This scenario proves three things:

1. **Plan is not a guarantee** — it checks what it can, but some validations only happen at execution time.
2. **Destroy happens before create** — when a resource must be replaced, Terraform destroys first, then creates. If creation fails, you're left with nothing.
3. **Human validation is irreplaceable** — you must check names, zones, regions, and all configuration values yourself. Don't rely solely on plan or AI-generated code. [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

The fix is straightforward: correct the zone back to `us-east-1a` (matching the provider's region), save, plan, and apply. The instance gets recreated successfully.

***

## 1.9 Manual Infrastructure Changes — The Drift Problem

The instructor stops the running EC2 instance manually from the AWS Console (power off), then runs `terraform plan`. The result: **"No changes. Your infrastructure matches the configuration."** But the instance is stopped — clearly the infrastructure doesn't match what we want. [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

**Why Terraform doesn't detect this:** The Terraform code never specified what **state** the instance should be in (running vs. stopped). The code only declared that the instance should *exist* with certain attributes (AMI, key pair, security group, zone). Terraform checks those attributes and finds them unchanged — the instance still exists, still has the right AMI, still has the right key pair. The fact that it's powered off is invisible to Terraform because that attribute wasn't declared. [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

**The fix:** Use the separate resource `aws_ec2_instance_state` to explicitly declare the desired state of the instance. This resource takes an `instance_id` (referencing the instance resource) and a `state` argument (e.g., `"running"` or `"stopped"`). Once this resource is added to the code, `terraform plan` detects the drift: the desired state is `running` but the actual state is `stopped`, so it plans to start the instance. [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

This reveals a fundamental Terraform principle: **Terraform only manages what you declare.** If you don't declare the instance state, Terraform doesn't manage it. If you don't declare a tag, Terraform doesn't care if someone manually adds or removes tags. The scope of Terraform's management is exactly the scope of your declarations.

The corollary: **if you manage infrastructure through code, always manage it through code.** Manual changes create drift — discrepancies between the code/state and reality — which leads to unpredictable behavior on the next apply. [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

***

## 1.10 terraform destroy — Complete Teardown

`terraform destroy` deletes **every resource** managed by the Terraform code in the current directory. It performs the same three-way comparison (code, state, infrastructure) but plans to destroy everything. It shows you what will be destroyed and asks for confirmation. [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

After destruction, the state file is updated to reflect that no resources exist. This is the cleanup command — used at the end of exercises, experiments, or when decommissioning infrastructure.

***

## 1.11 The Documentation-First Approach

The instructor closes with important advice: "Don't try to memorize or by-heart anything. I have shown you everything from the documentation, you can get it from the docs easily." The resource names, argument names, and available values all come from the Terraform AWS Provider documentation. You don't memorize `aws_ec2_instance_state` — you look it up when you need it. The skill is knowing what to look for, not remembering every resource name. [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

He also addresses AI-generated code: you can use ChatGPT to generate Terraform code, but **you must verify everything**. The plan-apply divergence scenario proved that even syntactically valid, logically plausible code can fail catastrophically. AI tools generate code; humans validate it.

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

## What We Are Building

We are executing a Terraform project (Exercise2) that creates AWS infrastructure: an EC2 instance, a key pair, a security group with rules, and associated resources. We then modify the code to observe how Terraform handles different types of changes (mutable, immutable, invalid), deliberately break things to learn failure modes, and finally destroy everything. The goal is not just to build infrastructure but to deeply understand Terraform's behavior during updates and failures. [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

***

## Step 1: Initialize the Project

Open Git Bash (or Terminal on macOS). Navigate to the Exercise2 folder:

```bash
cd <path-to-Exercise2>
ls
```

Confirm you see the `.tf` files.

```bash
terraform init
```

* `terraform` — the CLI tool
* `init` — initializes the working directory, downloads provider plugins from the Terraform Registry

**Expected output:** Download messages for the AWS provider, followed by "Terraform has been successfully initialized." [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

***

## Step 2: Format and Validate

```bash
terraform fmt
```

**Expected output:** Lists files it reformatted (e.g., `instance.tf`, `provider.tf`). If no files are listed, they were already correctly formatted. [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

```bash
terraform validate
```

**First run — expected error:** `"Inappropriate value for attribute ipv4. String required."` — a CIDR value is wrapped in square brackets (list format) when it should be a plain string.

**Fix:** Open the file in VS Code. Remove the `[]` square brackets from the CIDR values. Save (`Ctrl+S`). [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

```bash
terraform validate
```

**Expected output:** `"Success! The configuration is valid."` [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

***

## Step 3: Run the Plan

```bash
terraform plan
```

Terraform compares your `.tf` files against the state file and actual infrastructure (both empty on first run).

**Expected output:** A detailed listing of every resource to be created, with all attributes shown. Summary line: `Plan: 7 to add, 0 to change, 0 to destroy.` [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

**How to read the plan:**

1. **Look at destroy count first** — this is the most dangerous number. On first run, it should be 0.
2. **Look at change count** — what existing resources will be modified.
3. **Look at add count** — new resources being created.
4. **Read the `+` lines** to understand exactly what's being created and with what values.

***

## Step 4: Apply the Plan

```bash
terraform apply
```

Terraform shows the plan again and asks for confirmation.

Type `yes` and press Enter. [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

**What happens internally:** Terraform makes API calls to AWS to create each resource (key pair, security group, security group rules, EC2 instance, etc.). This takes time, especially for the EC2 instance.

**Expected output:** `"Apply complete! Resources: 7 added, 0 changed, 0 destroyed."` [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

**Verify the state file:** In VS Code, check `Exercise2/` — a `terraform.tfstate` file now exists. Open it and browse the JSON content. It contains every resource's attributes (AMI ID, instance ID, security group ID, etc.). The instructor recommends reading through it to familiarize yourself with the structure. [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

**Verify in AWS Console:**

* **EC2 → Instances:** One running instance in `us-east-1`.
* **EC2 → Key Pairs:** The key pair created by Terraform.
* **EC2 → Security Groups:** The security group with two inbound rules (SSH port 22 from your IP, HTTP port 80 from anywhere). Outbound rules: one for IPv4, one for IPv6, both to any destination. [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

***

## Step 5: Confirm Convergence

```bash
terraform plan
```

**Expected output:** `"No changes. Your infrastructure matches the configuration."` — code, state, and infrastructure are all in sync. Even running `terraform apply` now would do nothing. [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

***

## Step 6: Make a Mutable Change (Security Group Rule)

Open `security_group.tf` in VS Code. Change the SSH rule's CIDR from your IP to `0.0.0.0/0` (allow from anywhere). Save.

```bash
terraform plan
```

**Expected output:** `Plan: 0 to add, 1 to change, 0 to destroy.` The security group rule will be updated in place. [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

```bash
terraform apply
```

Type `yes`. The change applies quickly — just an API call to update the security group rule. No resources are destroyed or recreated. [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

**Verify in AWS Console:** The security group's SSH rule should now show `0.0.0.0/0` instead of your specific IP.

***

## Step 7: Attempt an Immutable Change (Key Pair)

Generate a new SSH key:

```bash
ssh-keygen
```

When prompted for the filename, enter `testkey`. This creates `testkey` (private) and `testkey.pub` (public) in the current directory. [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

**Modify two files:**

1. **Key pair resource file:** Add a new key pair resource (or modify the existing one). Change the name to `testkey`. Replace the public key content with the content of `testkey.pub`.
2. **Instance resource file:** Change the `key_name` argument from `dove-key` to `test-key`.

Save both files. [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

```bash
terraform plan
```

**Expected output:** `Plan: 2 to add, 0 to change, 1 to destroy.` The instance shows `must be replaced` with `-/+` symbols. The key pair is being added, the old instance is being destroyed, a new instance is being created. [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

**⚠️ This is the critical moment:** The plan shows `1 to destroy`. The instructor's rule: **always check what's being destroyed and ask yourself if that's what you intended.** If you didn't expect destruction, stop and investigate.

**In this case, revert the change** (the instructor chooses not to apply):

Change `key_name` back to `dove-key` in the instance file. Save.

```bash
terraform plan
```

**Expected output:** `0 to destroy`, `1 to add` (the new key pair resource we added, which is safe). [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

***

## Step 8: Reference a Non-Existent Resource

In the instance file, change the security group reference from `dove-sg` to `test-sg` (a resource that doesn't exist in any `.tf` file). Save.

```bash
terraform validate
```

**Expected output:** `"Success!"` — validate doesn't catch this because the HCL syntax is valid. [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

```bash
terraform plan
```

**Expected output:** Error — `"A managed resource 'aws_security_group' 'test-sg' has not been declared in the root module."` Plan catches the reference error because it actually evaluates resource dependencies. [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

**Fix:** Change `test-sg` back to `dove-sg`. Save.

**Lesson:** Validate checks syntax. Plan checks logic and references. They catch different categories of errors.

***

## Step 9: The Cross-Region Failure (Plan Succeeds, Apply Fails)

Change the availability zone in the instance configuration from `us-east-1a` to `us-east-2a`. Save.

```bash
terraform plan
```

**Expected output:** Plan shows `1 to destroy` (old instance), `2 to add` (new instance + key pair). Plan **does not report any errors** — `us-east-2a` is a valid zone name. [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

```bash
terraform apply
```

Type `yes`.

**What happens:**

1. Terraform **destroys the existing instance** — this succeeds.
2. Terraform creates the key pair — this succeeds.
3. Terraform tries to create the new instance in `us-east-2a` — **this FAILS** with `"Invalid availability zone."` [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

**Result:** The old instance is gone. The new instance was never created. Infrastructure is broken.

**Root cause:** `us-east-2a` exists in AWS but belongs to region `us-east-2`. The provider is configured for `us-east-1`. You can't create a `us-east-1` resource in a `us-east-2` zone. Plan couldn't detect this — only the actual AWS API call during apply revealed the mismatch. [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

**Verify:** Go to AWS Console → switch to `us-east-2` region → EC2 → you'll see `us-east-2a` exists there. But your provider targets `us-east-1`.

**Fix:**

Change the zone back to `us-east-1a`. Save.

```bash
terraform plan
terraform apply
```

Type `yes`. The instance is recreated in the correct zone. [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

***

## Step 10: Manual Change and State Drift

Go to the **AWS Console → EC2 → Instances**. Select the running instance. Click **Instance state → Stop instance**. Wait for it to reach "Stopped" state. [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

Return to the terminal:

```bash
terraform plan
```

**Expected output:** `"No changes."` — Terraform doesn't detect that the instance is stopped because the code never declared the desired instance state. [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

**Fix — Add instance state resource to the code:**

Add to your `.tf` file:

```hcl
resource "aws_ec2_instance_state" "web_state" {
  instance_id = aws_instance.web.id
  state       = "running"
}
```

* `aws_ec2_instance_state` — a resource type specifically for managing EC2 instance power state
* `instance_id` — references the instance resource's ID
* `state` — the desired state (`"running"` or `"stopped"`)

Save the file. [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

```bash
terraform plan
```

**Expected output:** Terraform now detects the drift — it plans to change the instance state from stopped to running. [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

```bash
terraform apply
```

Type `yes`. Terraform starts the instance. [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

**Lesson:** Terraform only manages what you declare. If you don't declare instance state, manual power-off is invisible to Terraform.

***

## Step 11: Destroy Everything

```bash
terraform destroy
```

Terraform plans the destruction of all managed resources and asks for confirmation.

Type `yes`.

**Expected output:** All resources destroyed. The state file is updated to reflect an empty infrastructure. [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)

**Verify in AWS Console:** No instances, no key pairs (Terraform-managed ones), no security groups (Terraform-managed ones) should remain.

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

## Terraform Execution Lifecycle

```
init → fmt → validate → plan → apply
                                  ↓
                               [tfstate created/updated]
                                  ↓
                          infrastructure matches code

Teardown: destroy → deletes ALL managed resources
```

## Three-Way Comparison (plan & apply)

```
.tf CODE FILES ←→ terraform.tfstate ←→ ACTUAL AWS INFRASTRUCTURE
       ↑                  ↑                      ↑
   what you want    what Terraform         what actually
                    last created            exists now

plan = compare all three → report differences
apply = execute the differences
```

## Plan Output — Reading Order (CRITICAL)

```
Plan: X to add, Y to change, Z to destroy

READ ORDER:
  1. DESTROY (Z) ← most dangerous — check FIRST
  2. CHANGE (Y)  ← review what's changing
  3. ADD (X)     ← safest — new resources

Symbols:
  +    = create
  ~    = update in place
  -    = destroy
  -/+  = destroy then recreate (must be replaced)
```

## Mutable vs. Immutable Changes

```
MUTABLE (in-place update, no destruction):
  Security group rules (CIDR, port)
  Tags
  Instance name

IMMUTABLE (destroy + recreate):
  EC2 key pair
  EC2 AMI ID
  Availability zone

Plan shows: "must be replaced" → DESTRUCTION WILL OCCUR
```

## Error Detection by Phase

```
terraform validate:
  ✓ catches: syntax errors, type mismatches (string vs list)
  ✗ misses: non-existent resource references, cross-region zone errors

terraform plan:
  ✓ catches: non-existent resource references, dependency errors
  ✗ misses: cross-region zone mismatch, API-level validation failures

terraform apply:
  ✓ catches: everything (real API calls)
  ✗ problem: destruction happens BEFORE creation
              → if creation fails, old resource already gone

LESSON: each phase catches MORE but plan is NOT a guarantee
```

## The Catastrophic Failure Scenario

```
Code change: zone us-east-1a → us-east-2a (provider = us-east-1)

validate → ✓ success (syntax valid)
plan     → ✓ success (zone name exists, plan can't check region match)
apply    → Step 1: DESTROY old instance ✓ (succeeds)
           Step 2: CREATE new instance ✗ (FAILS — invalid zone for region)

RESULT: old instance GONE, new instance NEVER CREATED
        infrastructure = broken, no running instance

FIX: correct zone → plan → apply → instance recreated

LESSON: "Do not completely trust in the plan"
```

## State Drift — Manual Change Detection

```
Manual action: stop instance via AWS Console
terraform plan: "No changes" ← DOES NOT DETECT

WHY: code never declared instance state
     Terraform only manages what you DECLARE

FIX: add resource:
  aws_ec2_instance_state {
    instance_id = aws_instance.web.id
    state       = "running"
  }

NOW: terraform plan detects stopped → plans to start
RULE: manage through code, ALWAYS manage through code
```

## terraform.tfstate

```
Created/updated after every apply
JSON format
Contains: every resource's attributes
  (AMI ID, instance ID, SG ID, key pair, etc.)

Purpose: Terraform's MEMORY of what it built
Used in: plan comparisons, resource references, output values

Recommendation: read through it to learn the attribute structure
```

## terraform destroy

```
Deletes EVERY resource in current directory's .tf files
Compares: code + state + infrastructure
Plans destruction → asks confirmation → executes

Use for: cleanup, teardown, decommissioning
```

## Validation Error Quick Reference

```
"String required" (validate)
  → remove [] brackets from CIDR values

"has not been declared in root module" (plan)
  → resource reference name doesn't match any resource block

"Invalid availability zone" (apply)
  → zone doesn't belong to the provider's configured region

"No changes" but instance is stopped (plan)
  → instance state not declared → add aws_ec2_instance_state
```

## Reusable Engineering Patterns

**1. Validation Layers Have Increasing Fidelity**

```
validate: syntax check (fast, shallow)
plan:     logic check (medium, deeper)
apply:    reality check (slow, complete)

Each layer catches more → but costs more (time, risk)
Pattern applies to: CI/CD pipelines, code reviews, staging environments
Lesson: never skip intermediate layers, but never trust them completely
```

**2. Destroy-Before-Create = Risk Window**

```
Immutable change → old resource destroyed FIRST
                 → new resource created SECOND
If step 2 fails → infrastructure broken (gap between destroy and create)

Mitigation: review plan carefully, validate all values manually
Same risk in: blue-green deployments, database migrations, DNS cutover
```

**3. Declarative Scope = Management Scope**

```
What you declare = what Terraform manages
What you omit = invisible to Terraform

Undeclared attributes can drift without detection
Manual changes to declared attributes → detected on next plan
Manual changes to undeclared attributes → invisible forever

RULE: if you want Terraform to manage it, you MUST declare it
```

**4. Tools Generate, Humans Validate**

```
AI can generate Terraform code
Plan can simulate execution
But neither guarantees correctness

"You can generate all the code through AI...
 but you have to check everything"

Human validation: names, zones, regions, resource references
Machine validation: syntax, types, dependency graphs
Gap between them: where failures live
```

***

*This completes the full reconstruction. Theory explains Terraform's comparison model, mutability rules, and the plan-apply trust boundary. Practical walks through every command, every failure, and every fix. The Compression Map enables instant recall of the validation hierarchy, the catastrophic failure pattern, and the core principle that Terraform only manages what you declare.* [\[225-plan-a...nd-destroy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/225-plan-apply-update-and-destroy.txt)
