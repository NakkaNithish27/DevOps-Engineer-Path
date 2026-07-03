# 🎓 Deep Learning Material: Terraform for VPC Setup — Manual Resources vs Module Approach

**Source:** [275-terraform-for-vpc-setup.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/275-terraform-for-vpc-setup.txt?EntityRepresentationId=ba61968f-99a6-4840-b46c-7b78655d20ec) (video caption) + [275.vpc.tf.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/275.vpc.tf.txt?EntityRepresentationId=bed074f4-2943-4558-99ef-2c6d86f0d386) (module code) — Video lecture comparing two approaches to creating an AWS VPC with Terraform: the manual resource-by-resource method (writing individual resource blocks for VPC, subnets, internet gateway, route tables, and associations) versus the module-based method using `terraform-aws-modules/vpc/aws`, demonstrating the massive simplification modules provide. [\[275-terraf...-vpc-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/275-terraform-for-vpc-setup.txt), [\[275.vpc.tf \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/275.vpc.tf.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 Two Approaches to Creating a VPC with Terraform

There are two fundamentally different ways to create a VPC using Terraform. The **first method** is the resource-by-resource approach: you go to the Terraform AWS provider documentation, find each individual resource type (`aws_vpc`, `aws_subnet`, `aws_internet_gateway`, `aws_route_table`, `aws_route_table_association`), and write a separate resource block for each. This gives you full control but produces a large amount of code. The **second method** uses a **Terraform module** — a pre-written, community-maintained package that encapsulates all those individual resources into a single, compact configuration block. [\[275-terraf...-vpc-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/275-terraform-for-vpc-setup.txt)

The instructor's recommendation is clear: **do not write VPC code from scratch using individual resources**. The manual code is shown only so you understand what happens underneath. The module approach is what you should use in practice. The instructor explicitly says: "I don't recommend you write this code" and "I really don't want you to write it. Just understand that." [\[275-terraf...-vpc-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/275-terraform-for-vpc-setup.txt)

***

## 1.2 The Manual Method — Resource-by-Resource

When building a VPC manually in Terraform, you follow the exact same flow as creating a VPC through the AWS console, but expressed as code. The resource creation sequence mirrors the architectural dependency chain you learned in the VPC lectures:

**Step 1 — Create the VPC:** Resource type `aws_vpc`. You specify the `cidr_block` (e.g., `10.0.0.0/16`), and enable DNS support (`enable_dns_support = true`) and DNS hostnames (`enable_dns_hostnames = true`) so that instances launched in this VPC receive DNS names. [\[275-terraf...-vpc-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/275-terraform-for-vpc-setup.txt)

**Step 2 — Create the subnets:** Resource type `aws_subnet`. You create multiple subnet resources — in the video, three public and three private subnets. Each subnet specifies: the `vpc_id` (referencing the VPC resource created in Step 1 via `aws_vpc.<name>.id`), a `cidr_block` that falls within the VPC's CIDR range (e.g., `10.0.1.0/24`, `10.0.2.0/24`), an `availability_zone` (using variables for `us-east-2a`, `us-east-2b`, `us-east-2c`), and for public subnets, `map_public_ip_on_launch = true` — which automatically assigns a public IP to instances launched in that subnet. [\[275-terraf...-vpc-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/275-terraform-for-vpc-setup.txt)

**Step 3 — Create the internet gateway:** Resource type `aws_internet_gateway`. You specify the `vpc_id` and tags. This is simple — just create the gateway and attach it to the VPC. [\[275-terraf...-vpc-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/275-terraform-for-vpc-setup.txt)

**Step 4 — Create the route table for public subnets:** Resource type `aws_route_table`. Inside it, you define a `route` block with `cidr_block = "0.0.0.0/0"` (all traffic) pointing to `gateway_id = aws_internet_gateway.<name>.id`. This is the rule that makes subnets public — routing all non-local traffic to the internet gateway. [\[275-terraf...-vpc-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/275-terraform-for-vpc-setup.txt)

**Step 5 — Associate the route table with public subnets:** Resource type `aws_route_table_association`. This connects each public subnet to the public route table. You need **one association per subnet** — three public subnets means three association resources. Each specifies a `subnet_id` and a `route_table_id`. [\[275-terraf...-vpc-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/275-terraform-for-vpc-setup.txt)

The instructor deliberately **skips the NAT gateway** in the manual code to save costs. NAT gateways are not free — they incur hourly charges and data processing fees. The instructor notes: "We did not create a NAT gateway route table and bind the table to it simply to save on costs." The steps for NAT gateway would follow the same pattern: create the NAT gateway, create a route table pointing `0.0.0.0/0` to the NAT gateway, and associate that route table with the private subnets. [\[275-terraf...-vpc-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/275-terraform-for-vpc-setup.txt)

The total resource count for this manual setup is **21 resources** (as shown by `terraform plan`): the VPC, six subnets, the internet gateway, route tables, route table associations, plus the instance, key pair, and security group. [\[275-terraf...-vpc-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/275-terraform-for-vpc-setup.txt)

🔍 **Deep Dive**
The manual code also includes an instance resource (`aws_instance`) that references the VPC's subnet. The instance's `subnet_id` is set to `aws_subnet.dev-pub-1.id` — a cross-resource reference that pulls the subnet's ID at runtime from the Terraform state. By placing the instance in a specific subnet, it automatically becomes part of that VPC. The security group is also referenced, and the rest of the instance configuration follows the same patterns from previous Terraform lectures. [\[275-terraf...-vpc-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/275-terraform-for-vpc-setup.txt)

***

## 1.3 Why the Manual Method Is Problematic

The manual approach works — the code is functional and can be applied. But it has significant drawbacks:

* **Volume:** Creating a VPC with six subnets, an internet gateway, route tables, associations, and a NAT gateway produces dozens of resource blocks. The code becomes long and difficult to maintain.
* **Complexity:** Every resource must correctly reference other resources. A single typo in a cross-reference (wrong resource name, wrong attribute) breaks the entire setup.
* **Repetition:** The three public subnet blocks are nearly identical — only the CIDR, availability zone, and name differ. Same for private subnets, route table associations, etc. This is exactly the kind of repetition that modules and loops eliminate.
* **Error-prone:** When writing this much infrastructure code manually, mistakes are likely — missing associations, wrong VPC IDs, incorrect CIDR ranges. [\[275-terraf...-vpc-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/275-terraform-for-vpc-setup.txt)

The instructor rushes through the manual code intentionally: "That's why I rushed to show you all this source code, because I really don't want you to write it." The purpose is conceptual understanding, not operational practice. [\[275-terraf...-vpc-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/275-terraform-for-vpc-setup.txt)

***

## 1.4 The Module Method — `terraform-aws-modules/vpc/aws`

A **Terraform module** is a pre-written, reusable package of Terraform code. Instead of writing individual resource blocks, you declare a `module` block that references the module's source, and you provide inputs (variables). The module internally contains all the resource definitions, cross-references, associations, and logic — you just configure the high-level parameters. [\[275-terraf...-vpc-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/275-terraform-for-vpc-setup.txt)

The VPC module used is `terraform-aws-modules/vpc/aws`, which is available on the **Terraform Registry** (registry.terraform.io). You find it by going to the registry, clicking on Modules, filtering by AWS, and clicking on VPC. The registry page shows examples, documentation, and a link to the full source code on GitHub. [\[275-terraf...-vpc-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/275-terraform-for-vpc-setup.txt)

The module code is remarkably compact:

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  name    = "dove-vpc"
  cidr    = "10.0.0.0/16"

  azs             = ["us-east-1a", "us-east-1b", "us-east-1c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_nat_gateway = true
  enable_vpn_gateway = true

  tags = {
    Terraform   = "true"
    Environment = "dev"
  }
}
```

 [\[275.vpc.tf \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/275.vpc.tf.txt)

This single block replaces the entire manual VPC setup. It creates the VPC, all six subnets (three public, three private), the internet gateway, route tables, route table associations, and — with `enable_nat_gateway = true` — the NAT gateway, its route table, and its associations. The `terraform plan` output shows **32 resources** being created from this compact code. [\[275-terraf...-vpc-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/275-terraform-for-vpc-setup.txt)

The key inputs:

* **`source`** — Where the module code lives. `terraform-aws-modules/vpc/aws` is a shorthand for the Terraform Registry path.
* **`name`** — The name for the VPC.
* **`cidr`** — The VPC's CIDR block.
* **`azs`** — A list of availability zones. You can hardcode them or use data sources/functions to dynamically fetch them.
* **`private_subnets`** / **`public_subnets`** — Lists of CIDR blocks for each subnet type. The CIDRs must fall within the VPC's CIDR range.
* **`enable_nat_gateway`** — Boolean. Set to `true` to create a NAT gateway for private subnets.
* **`enable_vpn_gateway`** — Boolean. Set to `true` to create a VPN gateway.
* **`tags`** — Tags applied to all created resources. [\[275.vpc.tf \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/275.vpc.tf.txt)

⚠️ **Expert Note**
The NAT gateway has a cost. The instructor warns: "Remember that there is a NAT gateway, so there will be a fee when creating a NAT gateway." If you're just testing, either set `enable_nat_gateway = false` or make sure to destroy the infrastructure immediately after testing with `terraform destroy`. [\[275-terraf...-vpc-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/275-terraform-for-vpc-setup.txt)

***

## 1.5 `module` vs `resource` — The Key Distinction

In previous Terraform lectures, you used `resource` blocks to create individual AWS resources. The `module` block is different — it is **not** a single resource. It is a **wrapper** that internally contains many resource blocks. When you declare a module, Terraform downloads the module's source code (during `terraform init`), reads all its internal resource definitions, and creates everything the module specifies. [\[275-terraf...-vpc-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/275-terraform-for-vpc-setup.txt)

The relationship: `resource` = one AWS object. `module` = many AWS objects packaged together with configurable inputs. This is why the manual method creates 21 resources from many resource blocks, while the module creates 32 resources from one module block. The module actually creates **more** resources (because it includes the NAT gateway and additional infrastructure the manual code skipped), yet requires far less code. [\[275-terraf...-vpc-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/275-terraform-for-vpc-setup.txt)

***

## 1.6 Studying Module Source Code as a Learning Strategy

The instructor recommends going to the module's GitHub repository and reading the source code. The full code for the VPC module is available on GitHub (linked from the Terraform Registry page). Inside, you can see how the module authors handle availability zones (using data sources and functions like `slice()` to automatically get AZ names), how they use loops (local iteration with `for_each`), and how they structure complex multi-resource configurations. [\[275-terraf...-vpc-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/275-terraform-for-vpc-setup.txt)

The instructor says: "This is also another good way to learn Terraform. I read the available resource and then clicked on it." Reading production-quality module code exposes you to advanced Terraform patterns — data sources, locals, loops, conditional resource creation — that you might not encounter in basic tutorials. [\[275-terraf...-vpc-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/275-terraform-for-vpc-setup.txt)

***

## 1.7 Where This Module Reappears

The instructor foreshadows: this VPC module will be used again in the **Kubernetes section** when creating a Kubernetes cluster on AWS. A Kubernetes cluster requires a VPC with specific subnet configurations, and the module makes that setup trivial. Additional Terraform features will also be introduced in that context. [\[275-terraf...-vpc-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/275-terraform-for-vpc-setup.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are creating an AWS VPC using Terraform in two ways: first examining the manual resource-by-resource code (to understand what happens underneath), then building the same VPC using the `terraform-aws-modules/vpc/aws` module (the recommended approach). The final outcome: a complete VPC with public subnets, private subnets, internet gateway, route tables, and optionally a NAT gateway — all from a single compact Terraform file. [\[275-terraf...-vpc-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/275-terraform-for-vpc-setup.txt)

***

## Part A: The Manual Method (Understand, Don't Reproduce)

### Step 1: Download and Examine the Manual Code

Download the lecture resources. You should find a VPC folder containing `vpc.tf` (the manual VPC code) and supporting files (`variables.tf`, `instance.tf`, etc.). Open `vpc.tf` and read through it. [\[275-terraf...-vpc-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/275-terraform-for-vpc-setup.txt)

The code follows the VPC creation flow:

```
aws_vpc → aws_subnet (×6) → aws_internet_gateway → aws_route_table → aws_route_table_association (×3)
```

**Key things to observe in the code:**

* The VPC resource has `enable_dns_support = true` and `enable_dns_hostnames = true`.
* Public subnets have `map_public_ip_on_launch = true`.
* Availability zones are defined as variables (in `variables.tf`): `us-east-2a`, `us-east-2b`, `us-east-2c`, with region `us-east-2`.
* Subnet CIDRs (e.g., `10.0.1.0/24`) are subsets of the VPC CIDR (`10.0.0.0/16`).
* The route table's route block has `cidr_block = "0.0.0.0/0"` → `gateway_id = aws_internet_gateway.<name>.id`.
* Three `aws_route_table_association` resources link each public subnet to the route table.
* NAT gateway is deliberately omitted to save costs. [\[275-terraf...-vpc-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/275-terraform-for-vpc-setup.txt)

### Step 2: Test the Manual Code (Optional)

Navigate to the VPC folder in your terminal:

```bash
cd vpc
```

**2a. Initialize:**

```bash
terraform init
```

Downloads the AWS provider plugin. [\[275-terraf...-vpc-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/275-terraform-for-vpc-setup.txt)

**2b. Validate:**

```bash
terraform validate
```

Checks syntax correctness. Expected: "Success! The configuration is valid." [\[275-terraf...-vpc-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/275-terraform-for-vpc-setup.txt)

**2c. Plan:**

```bash
terraform plan
```

Shows what Terraform will create. Expected: **21 resources to add**. Review the list — you should see the VPC, subnets, internet gateway, route table, route table associations, instance, key pair, and security group. [\[275-terraf...-vpc-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/275-terraform-for-vpc-setup.txt)

**2d. Apply (optional — only if you want to test):**

```bash
terraform apply
```

Type `yes` to confirm. Creates all 21 resources in AWS. [\[275-terraf...-vpc-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/275-terraform-for-vpc-setup.txt)

**2e. Destroy (mandatory if you applied):**

```bash
terraform destroy
```

Type `yes` to confirm. Removes all created resources. **Always destroy after testing to avoid charges.** [\[275-terraf...-vpc-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/275-terraform-for-vpc-setup.txt)

***

## Part B: The Module Method (Recommended Approach)

### Step 3: Create the Module Project

Create a new folder separate from the manual code:

```bash
mkdir vpc-module
cd vpc-module
```

 [\[275-terraf...-vpc-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/275-terraform-for-vpc-setup.txt)

### Step 4: Create the VPC Module File

Create a file called `vpc.tf`:

```bash
vim vpc.tf
```

Paste the module code (modify as needed):

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  name    = "dove-vpc"
  cidr    = "10.0.0.0/16"

  azs             = ["us-east-1a", "us-east-1b", "us-east-1c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_nat_gateway = true
  enable_vpn_gateway = true

  tags = {
    Terraform   = "true"
    Environment = "dev"
  }
}
```

 [\[275.vpc.tf \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/275.vpc.tf.txt)

**Customization points:**

| Parameter            | What to Set                   | Notes                      |
| -------------------- | ----------------------------- | -------------------------- |
| `name`               | Your VPC name                 | e.g., `"dove-vpc"`         |
| `cidr`               | VPC CIDR range                | e.g., `"10.0.0.0/16"`      |
| `azs`                | Your region's AZs             | Must match your AWS region |
| `private_subnets`    | CIDR list for private subnets | Must be within VPC CIDR    |
| `public_subnets`     | CIDR list for public subnets  | Must be within VPC CIDR    |
| `enable_nat_gateway` | `true` or `false`             | ⚠️ `true` incurs charges   |
| `enable_vpn_gateway` | `true` or `false`             | Enable if VPN needed       |

Save and exit. [\[275-terraf...-vpc-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/275-terraform-for-vpc-setup.txt), [\[275.vpc.tf \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/275.vpc.tf.txt)

### Step 5: Initialize the Module

```bash
terraform init
```

 [\[275-terraf...-vpc-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/275-terraform-for-vpc-setup.txt)

| What Happens                         | Why It Matters                                             |
| ------------------------------------ | ---------------------------------------------------------- |
| Downloads the AWS provider plugin    | Needed for AWS API calls                                   |
| Downloads the VPC module source code | Fetches the pre-written module from the Terraform Registry |
| Creates `.terraform/` directory      | Stores downloaded providers and modules                    |

**Expected output:** "Terraform has been successfully initialized."

### Step 6: Plan the Infrastructure

```bash
terraform plan
```

**Expected output:** **32 resources to add** — significantly more than the manual 21 because the module includes the NAT gateway, its elastic IP, its route table, and its associations. [\[275-terraf...-vpc-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/275-terraform-for-vpc-setup.txt)

Review the plan output. You should see: VPC, public subnets, private subnets, internet gateway, NAT gateway (if enabled), route tables (public and private), route table associations, elastic IPs, and more.

### Step 7: Apply (Optional — Cost Warning)

```bash
terraform apply
```

Type `yes` to confirm. [\[275-terraf...-vpc-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/275-terraform-for-vpc-setup.txt)

⚠️ **Cost warning:** If `enable_nat_gateway = true`, the NAT gateway incurs hourly charges. Only apply if you intend to use the VPC immediately. If just testing, you can skip apply or destroy immediately after verifying creation. [\[275-terraf...-vpc-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/275-terraform-for-vpc-setup.txt)

### Step 8: Destroy (Mandatory If Applied)

```bash
terraform destroy
```

Type `yes` to confirm. [\[275-terraf...-vpc-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/275-terraform-for-vpc-setup.txt)

**Always destroy after testing.** The instructor emphasizes this at both the beginning and end of the module demonstration: "If you create something, make sure you destroy it also."

***

## Step 9: Explore the Module Source Code (Learning)

Navigate to the Terraform Registry: `registry.terraform.io` → Modules → search for AWS VPC. Click on the `terraform-aws-modules/vpc/aws` module. [\[275-terraf...-vpc-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/275-terraform-for-vpc-setup.txt)

**9a.** Read the **Usage** section — it shows the module block example.

**9b.** Click the **GitHub** link to view the full source code. Open `main.tf` to see:

* How availability zones are fetched dynamically using data sources
* How `slice()` function is used to select AZs
* How loops iterate over subnet lists
* How conditional resource creation works (NAT gateway only if enabled)

**9c.** Look at the **Complete example** in the examples dropdown on the registry page. It shows a production-ready configuration with all options. [\[275-terraf...-vpc-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/275-terraform-for-vpc-setup.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Core Comparison: Manual vs Module

```
MANUAL (resource-by-resource):
  aws_vpc + aws_subnet ×6 + aws_internet_gateway + aws_route_table
  + aws_route_table_association ×3 + (NAT GW skipped for cost)
  = ~21 resources, dozens of lines, error-prone
  Purpose: understand what's underneath

MODULE (terraform-aws-modules/vpc/aws):
  1 module block, ~15 lines of config
  = 32 resources (includes NAT GW + all associations)
  Purpose: USE THIS in practice
```

***

## Module Code (Complete Reference)

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  name    = "dove-vpc"
  cidr    = "10.0.0.0/16"
  azs             = ["us-east-1a", "us-east-1b", "us-east-1c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
  enable_nat_gateway = true
  enable_vpn_gateway = true
  tags = { Terraform = "true", Environment = "dev" }
}
```

***

## VPC Creation Flow (Manual = What Module Does Internally)

```
1. aws_vpc              → CIDR, DNS support/hostnames
2. aws_subnet ×N        → public (map_public_ip=true) + private
3. aws_internet_gateway  → attach to VPC
4. aws_route_table (pub) → 0.0.0.0/0 → IGW
5. aws_route_table_association ×N → link public subnets to pub RT
6. aws_nat_gateway       → in public subnet, with elastic IP
7. aws_route_table (priv) → 0.0.0.0/0 → NAT GW
8. aws_route_table_association ×N → link private subnets to priv RT
```

***

## `module` vs `resource`

```
resource = 1 AWS object
module   = many AWS objects, pre-packaged with configurable inputs

module "vpc" {
  source = "..."     ← where to get the code (Registry/GitHub)
  name   = "..."     ← input variables
  ...
}

terraform init → downloads module source code + provider
```

***

## Subnet CIDR Design

```
VPC:              10.0.0.0/16     (~65,536 IPs)
Private subnets:  10.0.1.0/24     (256 IPs)
                  10.0.2.0/24
                  10.0.3.0/24
Public subnets:   10.0.101.0/24   (256 IPs)
                  10.0.102.0/24
                  10.0.103.0/24

All subnet CIDRs MUST fall within VPC CIDR range
```

***

## Operational Sequence

```
mkdir vpc-module && cd vpc-module
vim vpc.tf                    ← paste module block
terraform init                ← downloads module + provider
terraform plan                ← shows 32 resources to add
terraform apply               ← creates everything (⚠️ NAT GW costs)
terraform destroy             ← ALWAYS destroy after testing
```

***

## Cross-Reference Pattern (Manual Code)

```
Instance → Subnet:
  subnet_id = aws_subnet.dev-pub-1.id

Route Table → IGW:
  gateway_id = aws_internet_gateway.<name>.id

Route Table Association → Subnet + Route Table:
  subnet_id    = aws_subnet.<name>.id
  route_table_id = aws_route_table.<name>.id

All .id values resolved at runtime from Terraform state
```

***

## Manual VPC Resource: Key Attributes

```
aws_vpc:
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true      ← DNS resolution within VPC
  enable_dns_hostnames = true      ← instances get DNS names

aws_subnet (public):
  map_public_ip_on_launch = true   ← auto-assign public IP

aws_route_table:
  route { cidr_block = "0.0.0.0/0", gateway_id = igw.id }
```

***

## Module Discovery Workflow

```
registry.terraform.io → Modules → AWS → VPC
  → Usage examples (module block)
  → Inputs/Outputs documentation
  → GitHub link → full source code (main.tf)
  → Examples dropdown → complete configurations
```

***

## Cost Awareness

```
enable_nat_gateway = true  → ⚠️ NAT GW has hourly charges + data fees
enable_nat_gateway = false → no NAT GW, private subnets can't reach internet

ALWAYS terraform destroy after testing to stop charges
```

***

## Key Engineering Patterns

| Pattern                           | Manifestation                                                                       |
| --------------------------------- | ----------------------------------------------------------------------------------- |
| **Module abstraction**            | 32 resources from 15 lines — complexity hidden behind inputs                        |
| **Understand-then-abstract**      | Manual code shown first for understanding, module used for practice                 |
| **Community modules as standard** | `terraform-aws-modules/vpc/aws` is the industry-standard VPC module                 |
| **Source code as learning**       | Module's GitHub repo teaches advanced Terraform (loops, data sources, conditionals) |
| **Cost-conscious infrastructure** | NAT gateway deliberately skipped in manual code; warning given for module approach  |
| **Destroy-after-test**            | Cloud resources cost money — always clean up after experimentation                  |
| **Module reuse across projects**  | Same VPC module reappears in Kubernetes cluster setup — write once, use everywhere  |

***

## Project Continuity

```
BEFORE: Default VPC examination (lecture 266), Terraform code structure (lecture 223)
THIS:   VPC creation — manual resources vs module (module = recommended)
NEXT:   More Terraform features + Kubernetes cluster setup using this VPC module
```

***

This completes the full reconstruction. **Theory** explains both approaches and why modules win. **Practical** gives you the exact file contents, commands, and cost warnings for both methods. The **Compression Map** gives you the module code, the manual flow, and the operational sequence for instant recall. Let me know if you'd like Anki flashcards or any section expanded! 🚀
