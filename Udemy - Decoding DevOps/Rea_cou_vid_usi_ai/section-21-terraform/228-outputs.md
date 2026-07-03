# 🎓 Deep Learning Material: Terraform Outputs — Extracting, Displaying, and Persisting Infrastructure State Data

**Source:** Video lecture on Terraform outputs and local-exec provisioner (from [228-outputs.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/228-outputs.txt?EntityRepresentationId=8e26dc2b-8123-47ab-bff0-06a69a5da27b) caption file) [\[228-outputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/228-outputs.txt)

**Video Context:** This lecture teaches how to **extract information from Terraform's state** and make it usable — both by printing it to the terminal during `terraform apply` and by saving it to local files for external consumption. The instructor introduces the `output` block for displaying resource attributes (public IP, private IP) and the `local-exec` provisioner for writing those attributes to text files. This builds directly on prior knowledge of Terraform resources, the `remote-exec` provisioner (covered in the previous section), and the `terraform.tfstate` file. The lecture is short but architecturally significant — it connects Terraform's internal state management to the external operational world.

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — Terraform State: Where All Infrastructure Information Lives

When you run `terraform apply`, Terraform creates or modifies real infrastructure (EC2 instances, security groups, etc.) and receives a **large amount of information back** from AWS — instance IDs, public IPs, private IPs, ARNs, DNS names, and many other attributes. All of this information is stored in the **`terraform.tfstate` file** — Terraform's state file that acts as a local database of everything Terraform manages. [\[228-outputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/228-outputs.txt)

The instructor frames this: *"when we execute Terraform apply, it returns a lot of output and that is getting stored into Terraform TF state file and we can access information from that file itself directly."* [\[228-outputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/228-outputs.txt)

The state file is structured by **resource type** and **resource name**. You can navigate to any piece of information by following the path: `resource_type.resource_name.attribute_name`. For example, `aws_instance.server.public_ip` means: go to the `aws_instance` resource type, find the resource named `server`, and read its `public_ip` attribute. [\[228-outputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/228-outputs.txt)

The instructor breaks down the three-part path explicitly: *"aws\_instance is the resource type. Resource name is the server, so as we give any resource name, right? And attribute name inside that, public\_ip."* [\[228-outputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/228-outputs.txt)

***

## 1.2 — Output Blocks: Printing Resource Attributes to the Terminal

While the state file contains everything, it's a raw JSON file — not convenient for quick reference. Terraform's **`output` block** provides a clean mechanism to **extract specific attributes and display them** on the terminal after `terraform apply` completes. [\[228-outputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/228-outputs.txt)

An output block has three components:

* **Name** — a label you choose (e.g., `webPublicIP`)
* **Description** (optional) — explains what the output represents
* **Value** — the attribute path to extract (e.g., `aws_instance.web.public_ip`)

The instructor explains: *"output resources to print content, and we can print our attributes that are already saved."* The output block doesn't create or modify anything — it simply reads from the state and prints. [\[228-outputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/228-outputs.txt)

The value follows the same three-part path pattern: `resource_type.resource_name.attribute_name`. You can output any attribute that exists in the state — public IP, private IP, instance ID, AMI ID, etc. The instructor demonstrates outputting both `public_ip` and `private_ip` for the same instance, showing that you can have **multiple output blocks** in the same configuration. [\[228-outputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/228-outputs.txt)

After `terraform apply`, the outputs appear at the bottom of the terminal output, clearly labeled with the names you defined. [\[228-outputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/228-outputs.txt)

> 🔍 **Deep Dive**
>
> The output block also plays a role in **Terraform modules** — outputs defined in a child module are the mechanism by which that module exposes information to the parent module. In the context of this lecture, outputs are used simply for display, but in production Terraform architectures, they become the **interface** between modular infrastructure components. A networking module might output subnet IDs that a compute module consumes as inputs. [\[228-outputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/228-outputs.txt)

***

## 1.3 — `local-exec` Provisioner: Saving State Data to Local Files

Sometimes you don't just want to display information — you want to **save it to a file** for use by other tools, scripts, or team members. The `local-exec` provisioner executes a command **on the local machine** (the machine running Terraform), as opposed to `remote-exec` which executes on the remote resource (e.g., the EC2 instance). [\[228-outputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/228-outputs.txt)

The instructor contrasts: *"We have seen remote-exec in the previous section. Local-execute will execute command locally."* [\[228-outputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/228-outputs.txt)

Inside `local-exec`, you provide a `command` argument — any shell command that your local OS can execute. The instructor uses `echo` with output redirection to write IP addresses to a text file:

```hcl
provisioner "local-exec" {
  command = "echo ${aws_instance.web.private_ip} >> private_ips.txt"
}
```

The `echo` command prints the attribute value, and `>>` redirects the output to a file. This creates a local text file containing the private IP of the instance — accessible after `terraform apply` completes. [\[228-outputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/228-outputs.txt)

The instructor also mentions an alternative: you can use `self.private_ip` instead of the full resource path when the `local-exec` is defined **inside the same resource** it references. `self` refers to the current resource — a shorthand that avoids repeating the resource type and name. [\[228-outputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/228-outputs.txt)

**Important placement:** The `local-exec` provisioner must be placed **inside the `aws_instance` resource block**, after any `remote-exec` provisioners. [\[228-outputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/228-outputs.txt)

The instructor describes real-world use cases: *"there are chances that there will be tasks like that where you need to use that information for something else. So you can, runtime, you can get the information and then you can store it into a file. You can queue as per your own format, like list of IPs or AMI IDs, stuff like that."* [\[228-outputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/228-outputs.txt)

***

## 1.4 — Output vs. local-exec: Two Different Mechanisms for Two Different Purposes

Both `output` and `local-exec` extract information from the Terraform state, but they serve different purposes:

| Mechanism                | Where            | Purpose                                         | Persistence                                            |
| ------------------------ | ---------------- | ----------------------------------------------- | ------------------------------------------------------ |
| `output` block           | Terminal display | Human-readable display after apply              | Shown on screen; also queryable via `terraform output` |
| `local-exec` provisioner | Local filesystem | Machine-readable export for other tools/scripts | Written to a file that persists after apply            |

 [\[228-outputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/228-outputs.txt)

The `output` block is for **visibility** — seeing what Terraform created. The `local-exec` write-to-file is for **integration** — feeding Terraform's data into external systems, scripts, or documentation.

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building and Why

We are adding **output blocks** to a Terraform configuration to display the public and private IP of an EC2 instance after `terraform apply`, and using a **`local-exec` provisioner** to save the private IP to a local text file. The final outcome: after running `terraform apply`, you see the IPs printed on the terminal AND have them saved in `private_ips.txt` for external use.

***

## Step 1: Create the Exercise Directory

**What we're doing:** Setting up a new exercise by copying the previous one.

1. Copy the `exercise-four` directory and paste it [\[228-outputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/228-outputs.txt)
2. Rename the copy to `exercise-five`
3. Open `instance.tf` inside `exercise-five` [\[228-outputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/228-outputs.txt)

**Connection to system flow:** This preserves the existing EC2 instance configuration from the previous exercise. We're adding output and local-exec capabilities on top of it.

***

## Step 2: Add Output Blocks for Public and Private IP

**What we're doing:** Defining output blocks at the end of `instance.tf` to display IP addresses after apply.

The instructor notes that an output for `instance_id` already exists from a prior exercise. We add two more: [\[228-outputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/228-outputs.txt)

**Output for public IP:**

```hcl
output "webPublicIP" {
  description = "Public IP of the web instance"
  value       = aws_instance.web.public_ip
}
```

* `output` — the block type
* `"webPublicIP"` — the name/label for this output (appears in terminal)
* `value = aws_instance.web.public_ip` — the attribute path:
  * `aws_instance` — resource type (EC2 instance)
  * `web` — the resource name (as defined in the `resource "aws_instance" "web"` block)
  * `public_ip` — the specific attribute to extract [\[228-outputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/228-outputs.txt)

**Output for private IP:**

```hcl
output "webPrivateIP" {
  description = "Private IP of the web instance"
  value       = aws_instance.web.private_ip
}
```

Same structure, different attribute: `private_ip` instead of `public_ip`. [\[228-outputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/228-outputs.txt)

**How the instructor discovers available attributes:** When typing `aws_instance.web.` in the editor, the IDE shows a list of all available attributes. The instructor demonstrates: *"we can see the list all here. So I want to print the public IP."* [\[228-outputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/228-outputs.txt)

***

## Step 3: Add local-exec Provisioner to Save Private IP to File

**What we're doing:** Adding a `local-exec` provisioner inside the `aws_instance` resource to write the private IP to a text file on the local machine.

**Add this inside the `aws_instance "web"` resource block, after any existing `remote-exec` provisioner:** [\[228-outputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/228-outputs.txt)

```hcl
provisioner "local-exec" {
  command = "echo ${aws_instance.web.private_ip} >> private_ips.txt"
}
```

* `provisioner "local-exec"` — declares a local execution provisioner (runs on YOUR machine, not the EC2 instance)
* `command = "echo ..."` — the shell command to execute locally
* `${aws_instance.web.private_ip}` — Terraform interpolation syntax; replaced with the actual private IP at runtime
* `>> private_ips.txt` — shell redirection; appends the output to `private_ips.txt` (creates the file if it doesn't exist) [\[228-outputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/228-outputs.txt)

**Alternative syntax:** You can also use `self.private_ip` instead of `aws_instance.web.private_ip` when the provisioner is inside the same resource block. [\[228-outputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/228-outputs.txt)

**Placement rule:** This block must be inside the `aws_instance` resource definition, at the same level as other provisioners. [\[228-outputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/228-outputs.txt)

***

## Step 4: Execute the Terraform Workflow

**What we're doing:** Running the standard Terraform execution pipeline.

Open **Git Bash** (or terminal, or VS Code terminal) and navigate to `exercise-five`: [\[228-outputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/228-outputs.txt)

**Initialize:**

```bash
terraform init
```

* Downloads providers and initializes the backend [\[228-outputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/228-outputs.txt)

**Format:**

```bash
terraform fmt
```

* Auto-formats all `.tf` files to canonical style [\[228-outputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/228-outputs.txt)

**Validate:**

```bash
terraform validate
```

* Checks syntax and configuration correctness [\[228-outputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/228-outputs.txt)

**Plan:**

```bash
terraform plan
```

* Shows what Terraform will create/modify — review before applying [\[228-outputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/228-outputs.txt)

**Apply:**

```bash
terraform apply
```

**Expected result after apply completes:** [\[228-outputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/228-outputs.txt)

1. The EC2 instance is created (or already exists from prior state)

2. At the bottom of the terminal output, you see:
   ```
   Outputs:

   webPublicIP = "x.x.x.x"
   webPrivateIP = "10.x.x.x"
   ```
   The instructor confirms: *"you should see the outputs over here. These are the names that we have used in the resource, the output, basically."* [\[228-outputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/228-outputs.txt)

3. A file `private_ips.txt` is created in the exercise-five directory containing the private IP

**Verify the file:**

```bash
cat private_ips.txt
```

Or check it in VS Code. The instructor confirms: *"There, private\_ips.txt. Let's check it from the VS code. There."* [\[228-outputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/228-outputs.txt)

***

## Step 5: Cleanup

**What we're doing:** Destroying all infrastructure to avoid charges.

```bash
terraform destroy
```

Confirm with `yes` when prompted. [\[228-outputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/228-outputs.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🔷 Core Concept (One-Line Reconstruction)

> **Terraform `output` blocks print resource attributes to terminal; `local-exec` provisioner writes them to local files — both extract data from the same state using `resource_type.resource_name.attribute` paths.**

***

## 🔷 Attribute Path Pattern

```
resource_type . resource_name . attribute_name

Example:
  aws_instance  .  web  .  public_ip
  aws_instance  .  web  .  private_ip
  aws_instance  .  server  .  id

Inside same resource block:
  self.private_ip  (shorthand for current resource)
```

***

## 🔷 Output Block Structure

```hcl
output "label_name" {
  description = "optional description"
  value       = aws_instance.web.public_ip
}
```

```
AFTER terraform apply:

  Outputs:
  
  webPublicIP  = "54.x.x.x"
  webPrivateIP = "10.x.x.x"
```

***

## 🔷 local-exec Provisioner Structure

```hcl
resource "aws_instance" "web" {
  # ... instance config ...

  provisioner "remote-exec" {
    # runs on REMOTE instance (previous lecture)
  }

  provisioner "local-exec" {
    command = "echo ${aws_instance.web.private_ip} >> private_ips.txt"
  }
  # runs on LOCAL machine (this lecture)
}
```

***

## 🔷 Output vs. local-exec

```
OUTPUT BLOCK                         LOCAL-EXEC PROVISIONER
─────────────────                    ──────────────────────
Prints to terminal                   Writes to local file
Human-readable display               Machine-readable export
Defined outside resource block       Defined INSIDE resource block
For visibility                       For integration with other tools
Queryable: terraform output          Persists as file: private_ips.txt
```

***

## 🔷 remote-exec vs. local-exec

```
remote-exec → runs command on the REMOTE resource (EC2 instance)
              Use: install software, configure services on the server

local-exec  → runs command on the LOCAL machine (your laptop/CI runner)
              Use: save IPs to file, trigger local scripts, notify systems
```

***

## 🔷 Data Flow

```
terraform apply
  │
  ├── Creates/modifies AWS resources
  │
  ├── AWS returns attributes (IP, ID, ARN, DNS, etc.)
  │
  ├── Stored in: terraform.tfstate (JSON)
  │
  ├── output blocks → READ from state → PRINT to terminal
  │
  └── local-exec → READ from state → WRITE to local file
```

***

## 🔷 Terraform Execution Pipeline (Standard)

```bash
terraform init       # initialize providers/backend
terraform fmt        # format .tf files
terraform validate   # syntax check
terraform plan       # preview changes
terraform apply      # execute + show outputs
terraform destroy    # cleanup
```

***

## 🔷 Practical Use Cases for Outputs and local-exec

```
OUTPUTS:
  → Display public IP to SSH into instance
  → Display instance ID for reference
  → Display DNS name for load balancer endpoint
  → Pass data between Terraform modules

LOCAL-EXEC:
  → Save list of IPs to inventory file (for Ansible)
  → Save AMI IDs to reference file
  → Trigger local notification script
  → Generate configuration files for other tools
  → Append to running log of provisioned resources
```

***

## 🔷 File Created in This Lecture

```
exercise-five/
  ├── instance.tf        ← contains resource + outputs + local-exec
  ├── terraform.tfstate  ← auto-generated state (all attributes)
  └── private_ips.txt    ← created by local-exec (contains private IP)
```

***

## 🔷 Reusable Engineering Pattern: State Extraction and Export

```
PATTERN: Internal State → External Interface

SYSTEM CREATES RESOURCES
  │
  ▼
SYSTEM STORES STATE INTERNALLY (terraform.tfstate)
  │
  ├── DISPLAY interface → output blocks → terminal (human consumption)
  │
  └── EXPORT interface → local-exec → file (machine consumption)

This pattern appears in:
  - Terraform: outputs + local-exec (this lecture)
  - Kubernetes: kubectl get → display; kubectl get -o json > file → export
  - Docker: docker inspect → display; docker inspect > file → export
  - CI/CD: pipeline variables → display in logs; artifacts → export to files
  - AWS CLI: aws describe → display; --output json > file → export

Core principle:
  Every system that creates resources generates state.
  That state has value beyond the system itself.
  Provide both human-readable and machine-readable extraction paths.
```

This is the key engineering takeaway: Terraform's state is not just for Terraform's internal bookkeeping — it's a **data source** that can feed other tools, scripts, and processes in your infrastructure pipeline. [\[228-outputs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/228-outputs.txt)
