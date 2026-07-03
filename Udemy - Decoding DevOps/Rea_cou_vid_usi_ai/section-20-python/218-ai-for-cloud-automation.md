# 🎓 Deep Learning Material: AI-Assisted Python Boto3 Scripts for Cloud Automation

**Source:** [218-ai-for-cloud-automation.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt?EntityRepresentationId=ae553abe-0b2f-4e3f-8d1e-adfc9fb782af) — Video lecture covering writing Python Boto3 scripts in VS Code for S3 file uploads, using generative AI (ChatGPT/GitHub Copilot) to generate complex multi-resource AWS infrastructure scripts, the iterative debug-delete-rerun cycle of AI-generated code, and the critical engineering lesson of building small verified scripts before integrating. [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 The Position of This Lecture in the Learning Arc

The instructor opens by establishing context: at this point in the course, the learner has already covered Python programming basics, Linux automation using Python Fabric, OS commands, and how to interact with AWS cloud services using Boto3 from the Python interactive shell (the previous lecture). This lecture transitions from **interactive shell exploration** to **writing actual scripts** in VS Code — and then makes a significant conceptual leap to using **generative AI** to produce entire infrastructure automation scripts. The progression is deliberate: learn the fundamentals yourself first, then leverage AI to scale your output. [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

***

## 1.2 The VS Code Environment Setup — Extensions as Development Accelerators

The video begins with setting up VS Code for Python + Boto3 development. Two extensions are installed: the **Python extension** (provides syntax highlighting, linting, IntelliSense, and debugging support for Python files) and the **AWS Boto3 extension** (provides autocompletion and type hints specific to Boto3 API calls). These are not decorative — they actively accelerate coding by suggesting method names, parameter types, and completing code structures. The video demonstrates this immediately: when writing the S3 upload script, VS Code's Copilot integration starts auto-completing entire lines based on context. [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

The working directory is the same folder containing the virtual environment created in the previous lecture. This is important because the virtual environment contains the installed Boto3 library. Scripts must be run with this environment activated, or Python won't find the `boto3` module. [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

***

## 1.3 The S3 Upload Script — Anatomy of a Boto3 Script

The first script (`s3_test.py`) performs a simple task: upload a local file to an S3 bucket. Despite its simplicity, it contains the **complete structural pattern** that every Boto3 script follows:

**Step 1: Import the library.** `import boto3` — makes the AWS SDK available in the script.

**Step 2: Create a client.** `s3 = boto3.client('s3')` — establishes a connection to the S3 service. The variable `s3` now holds an object with all S3-related methods. This is identical to what was done in the interactive shell in the previous lecture, but now it lives in a persistent script.

**Step 3: Define variables.** Bucket name, file name, object name — these are the parameters the operation needs. The video separates them as named variables rather than hardcoding them directly into the function call. This makes the script readable and modifiable.

**Step 4: Execute the operation inside a try/except block.** `s3.upload_file(file_name, bucket_name, object_name)` performs the actual upload. Wrapping it in `try/except` catches any errors (wrong filename, permissions issues, network problems) and prints them instead of crashing the script with a traceback. [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

The video then introduces a refinement: instead of hardcoding the filename, it replaces the variable with `input()` — taking the file path as **user input** at runtime. The object name is assigned the same value as the input filename. This transforms the script from a static tool to an interactive one. [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

🔍 **Deep Dive**
The `try/except` block is tested explicitly. The instructor first uploads a real file (`solar_system.txt`) — which succeeds. Then runs the script again with a non-existent filename — which triggers the `except` block and prints the error message. This is not just demonstrating the upload; it is **validating the error handling path**. The instructor notes "we also tested the try and except exception handling" — showing that testing both the success and failure paths is part of writing reliable scripts. [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

***

## 1.4 Script Execution Mechanics — Virtual Environment, Permissions, Interpreter

Before the script can run, several operational prerequisites must be satisfied:

**Activate the virtual environment:** `source DevOps/scripts/activate` (Windows/Git Bash). On macOS, the path is `DevOps/bin/activate` instead of `scripts`. The activated environment ensures the script can find `boto3` and any other installed packages. [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

**Execute permissions:** The instructor gives execute permission to the script (implied `chmod +x`). This is needed if you plan to run the script directly (`./s3_test.py`). [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

**Two ways to run:** Either `python3 s3_test.py` (calling the interpreter explicitly) or adding a **shebang line** `#!/usr/bin/env python` at the top of the script and running it directly. The video uses the explicit interpreter method. [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

**Terminal choice:** VS Code opens PowerShell by default on Windows. The instructor switches to **Git Bash** for a Unix-like terminal experience. [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

***

## 1.5 The Generative AI Paradigm Shift — From Manual Coding to Prompt Engineering

This is the most important conceptual section of the video. The instructor explicitly states: "Now you don't need to do everything by yourself... You can generate the entire script or even entire workspace to achieve complex tasks." But this statement comes with a critical prerequisite — **you must first understand the fundamentals**. The sequence matters: learn Python → learn Boto3 → learn AWS services → **then** use AI to generate code. Without that foundation, you cannot write correct prompts, verify outputs, or debug errors. [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

The instructor demonstrates this by asking ChatGPT to generate a complex multi-resource AWS setup script. The prompt asks for: key pair creation, security group with specific rules, EC2 instance with user data for a website, application load balancer with target group registration, and consistent resource naming. This is a task that would take significant manual coding effort, and the AI generates the entire script in one response. [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

However — and this is the core engineering lesson — **the generated script does not work on the first attempt**. It requires multiple rounds of debugging, error correction, cleanup, and re-execution. The AI gets the overall structure right but fails on operational details (naming conventions, special character restrictions, zone alignment). The human operator's knowledge of AWS is what enables diagnosing and fixing these issues. [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

⚠️ **Expert Note**
The instructor explicitly says: "Now coming to the most important point of this lecture... When you get error, you have to keep troubleshooting it, deleting it, and do this task repetitively until you get the final result. So the best way is always to write small small script, test it, and then you can integrate it together." This is the lecture's central engineering principle: **incremental development and verification beats monolithic generation**. AI can produce large scripts quickly, but validating them requires decomposition. [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

***

## 1.6 Prompt Engineering for Infrastructure Scripts

The prompt the instructor writes to ChatGPT is carefully structured and demonstrates what effective infrastructure prompting looks like. It is not a vague request — it specifies:

1. **Exact resources** to create (key pair, security group, EC2 instance, ALB)
2. **Specific configurations** (T2 micro, specific AMI, port 22 from my IP, port 80 from anywhere)
3. **Behavioral requirements** (user data script to set up a website from tooplate.com)
4. **Naming conventions** (name all resources based on the template name)
5. **Operational constraints** (all availability zones selected in the ELB)

The last constraint about availability zones comes from **prior operational experience**: the instructor previously encountered a bug where the load balancer only took the first two AZs, the instance landed in a third AZ, and registration failed because the instance was in a zone the load balancer didn't cover. This is knowledge that only comes from hands-on debugging, and it directly improves the prompt quality. [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

The instructor also compares ChatGPT and GitHub Copilot outputs, noting that Copilot gave better results for template naming (actually using the template name for all resources). The next lecture will use GitHub Copilot for the same task. [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

***

## 1.7 Anatomy of the AI-Generated Script — What ChatGPT Produced

The generated script imports four libraries: `boto3` (AWS SDK), `requests` (HTTP library for fetching public IP), `os` (file operations for saving the private key), and `time` (for wait/sleep operations). [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

**Dynamic IP Detection:** The script uses `requests.get()` to access an external URL that returns the caller's public IP address. It appends `/32` to convert it to CIDR notation for security group rules. This is a clever automation pattern — instead of hardcoding your IP, the script dynamically discovers it at runtime. [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

**Key Pair Creation and Local Storage:** When Boto3 creates a key pair, AWS generates the key and returns the private key material in the response. The script opens a local `.pem` file in write mode, writes the key material to it, and sets the file permissions to `400` (read-only by owner). This replicates what happens when you manually create and download a key pair from the AWS console. [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

**User Data:** The EC2 instance includes a user data script that installs and configures a web server using a template from tooplate.com. The template ChatGPT chose was "barista" (or "photo folio" in the Copilot version). User data runs automatically when the instance first boots. [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

**Resource Creation Sequence:** The script follows a dependency-aware order: key pair → security group → EC2 instance (needs both) → wait for instance to be running → load balancer security group → load balancer → target group → register instance → print endpoint. [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

***

## 1.8 The Iterative Debug Cycle — Real-World AI Code Failure Patterns

The video captures **three distinct execution failures**, each teaching a different lesson:

**Failure 1: Missing Python library.** `No module named requests`. The AI-generated script imports `requests`, but this library is not installed in the virtual environment. Fix: `pip install requests`. This is a **dependency gap** — the AI assumes libraries are available; the operator must ensure they are. [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

**Failure 2: AWS naming convention violation (load balancer).** The load balancer name contained underscores, but ALB names only allow alphanumeric characters and hyphens. The error message states this explicitly. The instructor feeds the error back to ChatGPT, which identifies the problem and suggests a fix. The instructor then manually modifies the variable in the script. [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

**Failure 3: AWS naming convention violation (target group).** Same category of error — underscores in the target group name. By this point, the instructor recognizes the pattern and fixes all remaining underscore-containing variable names without asking ChatGPT again. [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

Each failure requires **cleanup before retry**: the partially-created resources (EC2 instances, key pairs, security groups, load balancers, target groups) must be manually deleted from the AWS console before re-running the script. If you don't clean up, the next run will either fail on duplicate resource names or create unwanted duplicates. The cleanup order matters: load balancer first (because security groups can't be deleted while attached to active resources), then instances, then key pairs, then security groups. [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

🔍 **Deep Dive**
The security group deletion failure is instructive. The instructor tries to delete a security group and gets: "one network interface associated." This is because the EC2 instance was still terminating — its network interface still held a reference to the security group. The instructor waits for the instance to fully terminate, then retries the deletion successfully. This demonstrates the **resource dependency chain** in AWS: you cannot delete a resource that is still referenced by another active resource. Cleanup must follow the reverse of the creation order. [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

***

## 1.9 The Core Engineering Lesson — Small Scripts vs. Monolithic Generation

The instructor's final and most emphasized point: "The best way is always to write small small script, test it, and then you can integrate it together." Even when using AI to generate code, the recommended approach is:

1. Generate or write a script for **one resource** (e.g., just the key pair).
2. Test it. Verify the resource was created correctly in AWS.
3. Generate the next resource script.
4. Test it.
5. Once all individual scripts work, integrate them into a single script.

This is the **incremental build-and-verify** pattern. It avoids the problem demonstrated in the video: a monolithic script that creates five resources, fails on the third, leaves two orphaned resources, and requires full cleanup before retry. With small scripts, failures are isolated and cleanup is minimal. [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are writing and executing Python Boto3 scripts in VS Code to automate AWS operations — starting with a simple S3 file upload, then generating a complex multi-resource infrastructure script using ChatGPT. The final outcome: understanding the complete workflow of writing, executing, debugging, and cleaning up Boto3 automation scripts, and learning when and how to leverage generative AI for infrastructure code. [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

***

## Step 1: Prepare VS Code

**1a. Open the project folder:**

Go to **File → Open Folder** and select the folder containing your virtual environment from the previous lecture. The instructor's folder is named something like `Python_and_AWS_cloud`. [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

**1b. Install the Python extension:**

Go to **Extensions** (sidebar icon) → Search `Python` → Install the Microsoft Python extension. [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

**1c. Install the Boto3 extension:**

Search `Boto3` → Install the **AWS Boto3** extension. Click "Trust Publisher" if prompted. [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

These extensions provide autocomplete for Python syntax and Boto3 API methods, significantly speeding up development. [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

***

## Step 2: Write the S3 Upload Script

**2a. Create a new file:**

In the VS Code explorer, create a new file named `s3_test.py`. [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

**2b. Write the script:**

```python
import boto3

# Create S3 client
s3 = boto3.client('s3')

# Define variables
bucket_name = "your-bucket-name"
file_name = input("Enter the path of the file to upload: ")
object_name = file_name

# Upload file to S3
try:
    s3.upload_file(file_name, bucket_name, object_name)
    print(f"File {file_name} uploaded to bucket {bucket_name} as {object_name}")
except Exception as e:
    print(f"Error uploading file: {e}")
```

 [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

Line-by-line breakdown:

| Line                               | Purpose                                                                                            |
| ---------------------------------- | -------------------------------------------------------------------------------------------------- |
| `import boto3`                     | Makes the AWS SDK available                                                                        |
| `s3 = boto3.client('s3')`          | Creates an S3 client object with all S3 methods (same as done in the interactive shell previously) |
| `bucket_name = "your-bucket-name"` | **Replace** with your actual S3 bucket name                                                        |
| `file_name = input(...)`           | Takes the file path from user input at runtime instead of hardcoding                               |
| `object_name = file_name`          | The file will have the same name in S3 as the local file                                           |
| `s3.upload_file(...)`              | Boto3 method that uploads a local file to S3. Arguments: local path, bucket, object key            |
| `try/except`                       | Catches and prints any error (wrong path, permissions, network) instead of crashing                |

**Connection to larger flow:** This script validates that your Boto3 setup, AWS credentials, and virtual environment all work correctly before moving to more complex scripts.

***

## Step 3: Execute the Script

**3a. Open the terminal in VS Code:**

Go to **Terminal → New Terminal**. If it opens PowerShell, switch to **Git Bash** from the terminal dropdown. [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

**3b. Activate the virtual environment:**

```bash
source DevOps/scripts/activate
```

| Part                      | Purpose                                                                           |
| ------------------------- | --------------------------------------------------------------------------------- |
| `source`                  | Executes the activation script in the current shell session                       |
| `DevOps/scripts/activate` | Path to the activation script (Windows/Git Bash). On macOS: `DevOps/bin/activate` |

After activation, your prompt should show the environment name (e.g., `(DevOps)`). [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

**3c. (Optional) Give execute permission:**

```bash
chmod +x s3_test.py
```

Only needed if you plan to run the script directly (without `python3` prefix). [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

**3d. Run the script:**

```bash
python3 s3_test.py
```

 [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

**3e. Test the success path:**

When prompted, enter a real file name that exists in your current directory (e.g., `solar_system.txt`). Expected output: `File solar_system.txt uploaded to bucket ... as solar_system.txt`. [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

**3f. Test the failure path:**

Run again, enter a non-existent filename. Expected output: `Error uploading file: ...` with the exception details. This confirms your `try/except` block works. [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

***

## Step 4: Generate a Complex Infrastructure Script Using ChatGPT

**4a. Write the prompt:**

The instructor's prompt (adapted):

> Create a Python Boto3 script which achieves below mentioned tasks:
>
> 1. Create a key pair
> 2. Create a security group that allows port 22 from my IP and port 80 from anywhere
> 3. Create EC2 instance T2 micro with this key pair and security group, AMI: \[your AMI ID]. It should have the script in user data to set up website from tooplate.com
> 4. Create application load balancer, register this instance. Security group of ELB should allow port 80 from anywhere. Make sure all the zones are selected in ELB
> 5. Print the ELB endpoint
> 6. Give name to all AWS resources in the script as per the template name from tooplate.com

 [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

**Key details in the prompt:**

* The AMI ID is **region-specific** — use the correct one for your region (e.g., Amazon Linux 2023 AMI for us-east-1).
* "All zones selected in ELB" prevents the zone mismatch bug where the instance lands in a zone the load balancer doesn't cover.
* "Name as per template" gives consistent, identifiable resource names. [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

**4b. Review the generated code:**

The AI will produce a script that imports `boto3`, `requests`, `os`, and `time`. Key things to verify in the output:

* **Region:** Ensure it matches your target region. If not, add it to your prompt.
* **Dynamic IP:** Uses `requests.get()` to fetch your public IP + `/32` for CIDR notation.
* **Key pair:** Creates the key pair and writes the private key material to a local `.pem` file with `400` permissions.
* **Resource creation order:** Key pair → Security group → EC2 instance → Wait → LB security group → ALB → Target group → Register target → Print endpoint.
* **User data:** Should contain a bash script to install a web server and deploy a template. [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

***

## Step 5: Execute and Debug the AI-Generated Script

**5a. Create the script file:**

Create a new file (e.g., `folio_setup_aws.py`), paste the generated code, and save. [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

**5b. Install missing dependencies:**

The generated script likely imports `requests`, which isn't installed by default.

```bash
pip install requests
```

If you skip this, you'll get: `No module named requests`. [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

**5c. First execution attempt:**

```bash
python3 folio_setup_aws.py
```

 [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

**Expected failure — AWS naming violations:**

The script will likely fail with an error like: *"Load balancer name can only contain characters that are alphanumeric and hyphens."* This happens because the AI-generated resource names contain underscores or start with numbers. [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

**5d. Fix naming issues:**

Open the script and find all variable names used for AWS resource names (key pair name, security group name, load balancer name, target group name). Remove underscores and ensure names:

* Contain only alphanumeric characters and hyphens
* Do not start with a number
* Do not contain special characters [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

**5e. Clean up AWS resources before retrying:**

Before re-running, **delete all partially-created resources** in the AWS console. Cleanup order matters:

1. **Load balancer** (if created) — delete first
2. **Target group** (if created)
3. **EC2 instance** — terminate and wait for full termination
4. **Key pairs** — delete
5. **Security groups** — delete (may fail if instance hasn't fully terminated; wait and retry)

 [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

**Verification before retry:** In the EC2 dashboard, confirm: 0 running instances, 1 security group (default only), 0 key pairs. [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

⚠️ **Expert Note**
Security group deletion can fail with "one network interface associated" if the instance is still in the "shutting down" state. The network interface holds a reference to the security group until the instance is fully terminated. Wait for the instance state to show "terminated," then retry the security group deletion. This is the AWS resource dependency chain in action — deletion must follow the reverse of the creation order. [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

**5f. Re-execute after fixes:**

```bash
python3 folio_setup_aws.py
```

You may need to repeat the fix-cleanup-retry cycle multiple times (the video shows at least three iterations). Each time, read the error message, fix the specific issue, clean up, and retry. [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

**5g. Verify success:**

Once the script completes without errors, wait 5-10 minutes for the instance to boot and the user data script to finish. Then access the load balancer endpoint URL printed by the script in a browser. If the website loads, the entire automation worked. [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

***

## Step 6: Final Cleanup

After verification (or even without — the instructor says "you don't need to worry about whether the website works or not"), delete everything:

1. Load balancer
2. Target groups
3. EC2 instances
4. Key pairs
5. Security groups

Also delete any locally created `.pem` files that are no longer needed. [\[218-ai-for...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/218-ai-for-cloud-automation.txt)

**Connection to larger flow:** The next lecture repeats this process using GitHub Copilot instead of ChatGPT, with the approach of building and verifying one resource at a time rather than generating everything at once.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Boto3 Script Structural Pattern (Universal)

```
import boto3
client = boto3.client('<service>')    # connect to AWS service
client.<method>(parameters)           # execute operation

Every Boto3 script follows: Import → Client → Execute
```

***

## S3 Upload Script — Core Structure

```
import boto3
s3 = boto3.client('s3')
                                    ┌─ file_name (local path)
s3.upload_file(file_name,          ─┤─ bucket_name (S3 bucket)
               bucket_name,         └─ object_name (name in S3)
               object_name)

Wrapped in try/except → handles: wrong path, permissions, network errors
file_name from input() → interactive, not hardcoded
```

***

## Execution Prerequisites

```
VS Code folder = same folder as virtual environment
    │
    ├── Install extensions: Python + AWS Boto3
    ├── Activate venv: source DevOps/scripts/activate  (Mac: /bin/ instead of /scripts/)
    ├── Terminal: switch PowerShell → Git Bash
    └── Run: python3 script.py
```

***

## AI-Generated Infrastructure Script — Resource Creation Order

```
requests.get() → fetch public IP → /32 CIDR
    │
    ▼
Key Pair → save .pem locally (write mode, chmod 400)
    │
    ▼
Security Group (instance) → port 22 from my IP, port 80 from 0.0.0.0/0
    │
    ▼
EC2 Instance (t2.micro, AMI, key pair, SG, user data with website setup)
    │
    ▼
time.sleep / waiter → wait for instance running
    │
    ▼
Security Group (ELB) → port 80 from 0.0.0.0/0
    │
    ▼
Application Load Balancer → ALL availability zones
    │
    ▼
Target Group → register EC2 instance
    │
    ▼
Print ELB endpoint
```

***

## The Debug-Delete-Rerun Cycle

```
Execute script
    │
    ├── Error? ──→ Read error message
    │                 │
    │                 ├── Missing library? → pip install <lib>
    │                 ├── Naming violation? → fix variables (no underscores, no leading numbers)
    │                 └── Feed error to ChatGPT → get corrected code
    │                 │
    │                 ▼
    │              CLEANUP (reverse creation order):
    │                 Load Balancer → Target Group → EC2 (wait for terminated) → Key Pair → Security Group
    │                 │
    │                 ▼
    │              Verify dashboard: 0 instances, 0 key pairs, 1 SG (default only)
    │                 │
    │                 ▼
    │              Re-execute ──→ (loop back to top)
    │
    └── Success? → Wait 5-10 min → verify URL → cleanup
```

***

## AWS Naming Rules (Learned from Errors)

```
Load Balancer name:  alphanumeric + hyphens ONLY (no underscores, no leading numbers)
Target Group name:   alphanumeric + hyphens ONLY (no underscores)
Key Pair name:       more permissive, but keep clean
Security Group name: more permissive, but keep clean

Rule: remove ALL underscores from resource name variables before executing
```

***

## Resource Deletion Dependency Chain

```
Cannot delete SG while instance uses it
Cannot delete SG while network interface references it (instance still terminating)

Deletion order (reverse of creation):
  Load Balancer → Target Group → EC2 (wait for TERMINATED) → Key Pair → Security Group

Retry: if SG deletion fails → wait for instance to fully terminate → retry
```

***

## The Zone Alignment Bug

```
ALB created with only first 2 AZs in region
EC2 instance lands in 3rd AZ
    → Instance NOT registered in target group (zone mismatch)

Fix: prompt must specify "all availability zones selected in ELB"
```

***

## AI Code Generation — Prompt Engineering Checklist

```
Effective prompt includes:
  ✓ Exact resources to create (key pair, SG, EC2, ALB...)
  ✓ Specific configs (instance type, AMI, ports, sources)
  ✓ Behavioral requirements (user data, website setup)
  ✓ Naming conventions (consistent naming pattern)
  ✓ Operational constraints learned from experience (all AZs, no special chars)
  ✓ Region specification (if not default)

Prerequisite: YOU must understand AWS + Python + Boto3 to:
  → write correct prompts
  → verify generated code
  → debug failures
  → modify and re-prompt
```

***

## The Core Engineering Principle

```
MONOLITHIC GENERATION:
  Generate full script → execute → fail at step 3 → orphaned resources from steps 1-2
  → cleanup everything → fix → re-execute everything → repeat
  ⚠️ Slow, wasteful, error-prone

INCREMENTAL BUILD:
  Generate key pair script → test → ✓
  Generate SG script → test → ✓
  Generate EC2 script → test → ✓
  Integrate all → test → ✓
  ✅ Fast, isolated failures, minimal cleanup

"The best way is always to write small small script, test it,
 and then you can integrate it together."
```

***

## Dynamic IP Pattern (Reusable)

```python
import requests
my_ip = requests.get("https://checkip.amazonaws.com").text.strip() + "/32"
# → "203.0.113.45/32"  (your public IP in CIDR notation)
# Used in security group rules for "my IP" access
```

***

## Key Pair Creation + Local Save Pattern

```
boto3 create_key_pair() → response contains private key material
    │
    ├── open("keyname.pem", "w") → write key material to file
    └── os.chmod("keyname.pem", 0o400) → read-only by owner

Replicates: AWS Console "Create Key Pair" → download .pem file
```

***

## Tool Comparison (from video)

```
ChatGPT:  generates full scripts from detailed prompts
          → may not follow all instructions (e.g., template-based naming)
          → good for error diagnosis (paste error → get fix)

GitHub Copilot:  better at contextual naming, in-editor integration
                 → used in next lecture for incremental approach

Both require: human knowledge to verify, debug, and guide
```

***

## Project Continuity

```
BEFORE: Interactive Boto3 in Python shell (explored S3 commands)
THIS:   Boto3 scripts in VS Code + AI-generated infrastructure scripts + debug cycle
NEXT:   GitHub Copilot for incremental script building (one resource at a time, verified)
```

***

This completes the full reconstruction. **Theory** builds understanding of the AI-assisted development paradigm and why foundational knowledge is prerequisite. **Practical** gives you the exact execution flow from environment setup through the debug-delete-rerun cycle. The **Compression Map** lets you rapidly reload the script patterns, debugging workflow, and the critical "small scripts first" principle. Let me know if you'd like Anki flashcards or any section expanded! 🚀
