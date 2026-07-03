# 🎓 Deep Learning Material: Using GitHub Copilot (AI) for AWS Cloud Automation with Python

**Source:** [219-copilot-ai-for-cloud-automation.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt?EntityRepresentationId=01e42c19-25e0-499e-83b3-5468dd170abc) — Video lecture demonstrating a complete workflow of using GitHub Copilot's inline chat, slash commands, and workspace generation to iteratively build a Python Boto3 script for AWS infrastructure automation (key pair, security group, EC2 instance, ALB), then converting it to modular structure, adding documentation, generating unit tests, and finally comparing step-by-step generation vs. whole-workspace generation — with critical analysis of AI-generated code quality and the "assistant, not replacement" philosophy. [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 GitHub Copilot vs. ChatGPT — Design Intent Difference

Both ChatGPT and GitHub Copilot are generative AI, but they are designed for different workflows. ChatGPT is a general-purpose conversational AI — you describe what you want, and it generates the entire response at once. GitHub Copilot is **designed for development** — it lives inside your code editor (VS Code in this video) and is built to work within the context of your actual code files. The key behavioral difference the video highlights is the **generation mode**: instead of producing an entire script in one shot, Copilot is most effectively used **step by step** — you write or generate a piece, verify it, then ask for the next piece. The AI sees your existing code as context and builds on top of it. [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

This distinction matters because it shapes how you interact with the tool. With ChatGPT, you describe the full system upfront and hope the output is correct. With Copilot, you build incrementally — each generation is smaller, more verifiable, and grounded in already-validated code. The video demonstrates both approaches and explicitly concludes that the step-by-step method is superior for reliability. [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

***

## 1.2 The Inline Chat Mechanism — `Ctrl+I` / `Cmd+I`

The primary interaction mode demonstrated in this video is **inline chat**. You select code (or position your cursor) in the editor, press `Ctrl+I` (Windows/Linux) or `Cmd+I` (Mac), and a small chat prompt appears inline — right inside your code file. You type a natural language instruction, and Copilot generates code that either replaces your selection or inserts new code at that position. [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

The critical design feature is that Copilot **sees all the existing code in the file** as context. This is what makes iterative building work: when you ask "create EC2 instance with this security group and key pair," Copilot reads the variables, resource IDs, and function names already present in the file and references them in the generated code. Each new generation is **context-aware** — it builds on what already exists. [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

After generation, you have three options: **accept** the generated code (it gets inserted into your file), **ask for changes** (refine the prompt), or **reject** it entirely. The video demonstrates accepting most generations, but also shows modifying prompts when the initial instruction wasn't specific enough. [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

***

## 1.3 The Step-by-Step Iterative Generation Pattern

This is the **central engineering methodology** of the entire video. The instructor builds a complete AWS infrastructure automation script by generating one resource at a time, in this sequence:

1. **Key pair** → accept, optionally test
2. **Security group** (with rules) → accept, optionally test
3. **EC2 instance** (with AMI, instance type, UserData, referencing the above key pair and SG) → accept, verify URLs, optionally test
4. **Application Load Balancer** (with instance registration and SG rule for port 80) → accept, optionally test

At each step, the instructor emphasizes: you **can** (and ideally should) run the script and test it after each addition. If you do test, you must **delete all created resources** before continuing, because the next generation will add more code that creates the same resources again — running the accumulated script would create duplicates or fail on already-existing resources. [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

The pattern is explicitly compared to **agile/iterative development**: "step by step, just like agile, iterative." You build incrementally, verify at each stage, and only proceed when the current piece is solid. [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

🔍 **Deep Dive**
The video reveals an important Boto3 architectural detail during the security group generation. Copilot generates two separate API calls: one to **create the security group** (which creates it with no rules), and a second to **add inbound rules** to that security group. These are two different Boto3 methods/modules on the EC2 resource. This is not a Copilot quirk — it reflects how the AWS API actually works. Security group creation and rule management are separate operations. [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

***

## 1.4 Prompt Engineering for Copilot — Specificity Matters

The video provides direct guidance on how to write effective prompts for Copilot: **"Try to make your sentence as short as possible and as much specific detail you can add over there."** Short but specific. Not verbose, not vague. [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

Examples of increasing specificity demonstrated:

* **Vague:** "create EC2 instance" — insufficient, Copilot wouldn't know which AMI, instance type, or configuration.
* **Specific (as demonstrated):** "create EC2 instance with this security group and key pair, Amazon Linux 2023, T2 Micro, UserData to set up website from tooplate.com" — Copilot has enough context to generate the AMI lookup, instance type, UserData script, and reference existing variables.
* For the load balancer: "Add ALB application load balancer and register this instance, security group rule to allow port 80 from anywhere" — includes the resource type, registration requirement, and security rule in one prompt. [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

***

## 1.5 The URL/Data Validation Warning

The video issues an explicit warning about AI-generated content that references external resources: **"Make sure you check this URL whether this exists or not. Sometimes it takes a fake URL or URL that does not exist."** When Copilot generated the UserData script that downloads a website template from a URL, the instructor stops and says to take that URL, paste it in a browser, and verify it actually downloads the expected package. [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

This is a specific instance of a broader principle: **AI tools can hallucinate references**. URLs, package names, API endpoints, AMI IDs — anything that is a specific external reference should be verified before trusting it. The generated code may be syntactically perfect but reference something that doesn't exist. [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

***

## 1.6 Modular Structure Conversion

After the complete linear script is working, the video demonstrates converting it into a **modular structure**. The instructor selects all the code, opens inline chat, and asks Copilot to "create a modular structure for this code." Copilot responds by refactoring the linear script into **functions** — one function per task: create security group, get latest Amazon Linux AMI, launch EC2 instance, create load balancer, etc. At the end, a `main()` function calls all these individual functions in sequence, passing arguments and storing return values in variables. [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

The engineering reasoning is stated directly: "If we are going to expand it later, you know, to use more things. And we do these things commonly — creating security group, creating load balancers. These are common things. So it's always better to have a modular structure, functions which you can import, and then you can call." Modular structure enables **reuse** — individual functions can be imported into other scripts without duplicating code. [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

***

## 1.7 Documentation Generation — `/doc` and Explicit Prompting

The video demonstrates two approaches to adding documentation:

**Approach 1: The `/doc` slash command.** Select the code, press `Ctrl+I`, and type `/doc`. Copilot reads the code and generates documentation — primarily docstrings for functions. In the video, the first attempt only generates a docstring for the `main` function, which is incomplete. [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

**Approach 2: Explicit natural language prompt.** Select the code again, press `Ctrl+I`, and type "make this more readable, add comments and docstrings." This produces more comprehensive output — docstrings for **every** function, not just `main`. The video shows that explicit, detailed prompts produce better documentation than the shortcut command. [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

The instructor explains the practical value of docstrings: "When you call the function, you can give the function name /docstring to call this, to see in other scripts what this function is about." Docstrings make functions self-describing, which is essential when functions are imported into other scripts as part of a modular structure. [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

***

## 1.8 Unit Test Generation — `/test`

The video demonstrates generating unit tests using the `/test` slash command. Select all the code, press `Ctrl+I`, type `/test`. Copilot prompts for configuration: which test framework (the instructor selects `unittest`, the standard Python test framework), which directory (root), and the naming convention (`name_test.py`). [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

Copilot generates the test code in a **separate file**. The instructor saves this as `two_plate_aws_test.py` — following the convention of appending `_test` to the original script name. The video does not walk through the test code in detail, but the key takeaway is that Copilot can generate test scaffolding automatically from existing code, and the developer mindset of "before I execute this code, we should have unit test cases" is explicitly encouraged. [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

***

## 1.9 Workspace Generation — `/new` and Its Limitations

The final demonstration is the most ambitious: generating an **entire workspace** from a single comprehensive prompt. The instructor opens the Copilot chat panel (not inline — a separate chat window), types `/new`, and provides a detailed description of the entire project in one message: "Python boto3 modular structure to create key pair, security group \[with rules], EC2 instance \[with all details], UserData script, load balancer, and all resource names should be after template name from tooplate.com." [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

Copilot proposes a **folder structure**: a `src/` directory containing separate Python files — `keypair.py`, `security_group.py`, `ec2.py`, `load_balancer.py`, `config.py`, and `main.py`. Each file contains functions for its respective resource. The instructor clicks "Create Workspace" and selects a parent folder. Copilot generates all the files with their contents. [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

**But the generated workspace has significant errors.** The video explicitly walks through several:

* **Case mismatch:** `config.py` defines `resource_name` (lowercase), but `main.py` imports `RESOURCE_NAME` (uppercase). Python is case-sensitive — this would crash.
* **Missing variable:** `main.py` imports `my_ip` from `config`, but `config.py` does not define any `my_ip` variable.
* **Missing imports:** `main.py` does not import functions from files like `security_group.py`, so calling `create_security_group()` would result in a `NameError`.
* **Unused import warnings:** The IDE flags `my_ip` as unused because it was imported but the variable doesn't exist in the source. [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

The instructor's conclusion is direct: **"At least now it is not recommended to generate the entire code and go through it, because you will be doing a lot of reverse engineering to fix these problems."** The workspace generation creates a far-from-perfect starting point that requires significant manual debugging — the opposite of the step-by-step approach where each piece is verified before proceeding. [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

⚠️ **Expert Note**
The instructor acknowledges that "as time passes, it grows. These AI tools will become more intelligent." The limitations described are current-state, not permanent. But the principle remains: the more code you generate at once without verification, the more reverse engineering you need to do when things break. Even as AI improves, the step-by-step-with-verification approach reduces risk and debugging effort. [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

***

## 1.10 The Core Philosophy — AI as Assistant, Not Replacement

The video's closing statement is the most important conceptual takeaway: **"You have to use these AI tools as your assistants, not as a replacement."** The instructor directly addresses the narrative that "DevOps and developers' work will be gone" and counters it: "It is just a tool that we can use to make our life better. And we can code faster, more efficient way. We definitely cannot give complete control." [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

The prerequisites for using Copilot effectively are explicitly stated: "You already had knowledge of AWS. You have knowledge of Python programming, basics of Python programming. You have seen Boto3, and now you're working with Copilot to get your scripts done." The AI accelerates someone who already understands the domain. Without AWS knowledge, you wouldn't know whether the generated code is correct. Without Python knowledge, you couldn't debug the errors. Without Boto3 understanding, you couldn't verify that the API calls make sense. The AI is a **force multiplier for existing knowledge**, not a substitute for it. [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are using GitHub Copilot inside VS Code to iteratively build a Python Boto3 script that automates AWS infrastructure creation: a key pair, a security group with rules, an EC2 instance with UserData, and an Application Load Balancer. We then refactor the script into modular functions, add documentation, generate unit tests, and finally attempt a full workspace generation to compare approaches. The final outcome: a modular, documented, testable Python automation script — built entirely through AI-assisted iterative development. [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

***

## Step 1: Create the Python File

In VS Code (with GitHub Copilot extension installed), create a new file:

**Filename:** `two_plate_aws.py`

This is your working script. All iterative generations will be added to this file. [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

***

## Step 2: Generate Key Pair Code

**2a. Open inline chat:**

Press `Ctrl+I` (Windows/Linux) or `Cmd+I` (Mac). A small prompt appears inline in your editor.

**2b. Enter the prompt:**

```
Use Python boto3 to create key pair
```

 [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

**2c. Review the generated code:**

Copilot generates Boto3 code to create an EC2 key pair. Review it for:

* Correct Boto3 client/resource usage
* Key pair name (you can ask Copilot to change it if needed — the video shows refining the prompt for the key pair name)

**2d. Accept or refine:**

If the key pair name or other details aren't right, type a follow-up in the inline chat: e.g., "change the key pair name to \[your-name]." Once satisfied, **accept** the generated code. [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

**Optional:** Run the script (`python two_plate_aws.py`) to test key pair creation. If you test, **delete the created key pair** before continuing, because the next iteration will add more code that creates resources from scratch.

***

## Step 3: Generate Security Group Code

**3a. Open inline chat** (`Ctrl+I` / `Cmd+I`).

**3b. Enter the prompt:**

```
create security group
```

Keep it short but specific. Add rule details if you know what you need. [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

**3c. Review the generated code:**

Copilot generates two operations:

1. **Create the security group** (no rules) — one Boto3 method
2. **Add inbound rules** to that security group — a separate Boto3 method

This two-step pattern reflects the actual AWS API structure (as discussed in Theory §1.3). [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

**3d. Accept.** Optionally test and clean up.

***

## Step 4: Generate EC2 Instance Code

**4a. Select all existing code** in the file (the key pair + security group code).

**4b. Open inline chat** (`Ctrl+I` / `Cmd+I`).

**4c. Enter a detailed prompt:**

```
create EC2 instance with this security group and key pair, Amazon Linux 2023, T2 Micro, UserData to set up website from tooplate.com
```

 [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

By selecting all existing code before prompting, Copilot sees the security group ID variable and key pair name — it will reference them in the EC2 creation code.

**4d. Review the generated code carefully:**

The generated code typically includes:

* An AMI lookup (getting the latest Amazon Linux 2023 AMI ID)
* A UserData variable containing a bash script
* The `run_instances` call with instance type, key pair, security group, and UserData

**⚠️ CRITICAL VERIFICATION:** Check the UserData URL. Copy the URL from the generated code, paste it in your browser, and verify it actually downloads the expected package. **Copilot can generate fake URLs that don't exist.** [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

**4e. Accept** if everything checks out. Optionally test and clean up.

***

## Step 5: Generate Load Balancer Code

**5a. Select all existing code.**

**5b. Open inline chat** (`Ctrl+I` / `Cmd+I`).

**5c. Enter the prompt:**

```
Add ALB application load balancer and register this instance, security group rule to allow port 80 from anywhere
```

 [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

**5d. Review:**

The generated code should include:

* ALB creation
* Target group creation and instance registration
* Security group rule allowing inbound port 80

**5e. Accept all changes.** The video shows Copilot may present changes in multiple batches — accept each batch. [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

**5f. Save the file:** `Ctrl+S`. [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

At this point, you have a complete linear script that creates all AWS resources in sequence.

***

## Step 6: Convert to Modular Structure

**6a. Select all code** in the file.

**6b. Open inline chat** (`Ctrl+I` / `Cmd+I`).

**6c. Enter the prompt:**

```
I need a modular structure for this code
```

 [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

**6d. Review the refactored code:**

Copilot converts the linear script into functions:

* One function per task (create security group, get AMI, launch instance, create ALB, etc.)
* A `main()` function at the end that calls all individual functions in order
* Variables for VPC ID, subnet IDs, etc. assigned in `main()`
* Function arguments and return values connecting the pieces

**6e. Accept all changes.** [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

**Connection to larger flow:** The script is now importable and reusable. Individual functions can be called from other scripts.

***

## Step 7: Add Documentation

### 7a. First attempt — `/doc` command

Select all code → `Ctrl+I` → type `/doc`

**Result:** Copilot generates a docstring for the `main()` function only. Incomplete. [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

### 7b. Second attempt — explicit prompt

Select all code → `Ctrl+I` → type:

```
make this more readable, add comments and docstrings
```

**Result:** Copilot generates docstrings for **every** function, plus inline comments. Much more comprehensive. [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

**Accept all docstrings.**

🔍 **Deep Dive**
The explicit prompt produces better results than the slash command because it gives Copilot more context about your intent. `/doc` is a shortcut that may apply minimal documentation. A natural language prompt like "add comments and docstrings" tells Copilot exactly what you want at every level of the code. [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

***

## Step 8: Generate Unit Tests

**8a.** Select all code → `Ctrl+I` → type `/test`

**8b.** Copilot prompts for configuration:

| Setting        | Choice                       |
| -------------- | ---------------------------- |
| Test framework | `unittest` (standard Python) |
| Directory      | Root directory               |
| File naming    | `name_test.py`               |

 [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

**8c.** Copilot generates test code in a **separate file** (shown in a new editor tab).

**8d.** Save the test file: `Ctrl+S` → name it `two_plate_aws_test.py` [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

You now have two files: the main script and its corresponding test file.

***

## Step 9: Generate a Full Workspace (Comparison Approach)

**9a.** Open the Copilot chat panel: click the dropdown → **"Open Chat."** [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

**9b.** Type `/new` to start a new workspace generation.

**9c.** Enter a comprehensive prompt with all project details:

```
Python boto3 modular structure to create key pair, security group [with rules],
EC2 instance [Amazon Linux 2023, T2 Micro, UserData from tooplate.com],
create load balancer, all resource names after template name from tooplate.com
```

 [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

**9d.** Copilot proposes a folder structure:

```
src/
├── keypair.py
├── security_group.py
├── ec2.py
├── load_balancer.py
├── config.py
└── main.py
```

**9e.** Click **"Create Workspace"** → select parent folder. Copilot generates all files. [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

**9f. Inspect the generated workspace — expect errors:**

The video identifies these specific problems:

| Error            | Location                 | Issue                                                                                                |
| ---------------- | ------------------------ | ---------------------------------------------------------------------------------------------------- |
| Case mismatch    | `config.py` vs `main.py` | `resource_name` (lowercase) defined, `RESOURCE_NAME` (uppercase) imported                            |
| Missing variable | `config.py`              | `main.py` imports `my_ip`, but `config.py` doesn't define it                                         |
| Missing imports  | `main.py`                | Functions from `security_group.py`, `ec2.py` etc. not imported (need `from security_group import *`) |
| Unused imports   | `main.py`                | IDE flags `my_ip` as unused (because it doesn't exist in source)                                     |

 [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

**Key lesson:** The full workspace generation is **far from perfect**. Fixing these errors requires **reverse engineering** — understanding what was intended, tracing import chains, and manually correcting mismatches. This is the opposite of the step-by-step approach where each piece is verified before adding the next.

⚠️ **Expert Note**
The workspace approach has value as a **scaffolding starting point** — it creates the folder structure and file separation quickly. But every file needs review, imports need fixing, and the configuration layer needs manual correction. Use it when you want a structural starting point, not when you need working code. For working code, use the step-by-step inline chat approach. [\[219-copilo...automation \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/219-copilot-ai-for-cloud-automation.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Two Approaches — Step-by-Step vs. Whole-Workspace

```
STEP-BY-STEP (Inline Chat)              WHOLE-WORKSPACE (/new)
─────────────────────────                ──────────────────────
Generate one resource at a time          Generate everything at once
Verify after each generation             Inspect/debug after all generated
Context-aware (sees existing code)       Context = single prompt only
Errors caught early, locally             Errors compound, require reverse engineering
Slower to start, faster to finish        Faster to start, slower to fix
✅ RECOMMENDED                           ⚠️ Scaffolding only, not production-ready
```

***

## Copilot Interaction Model

```
Inline Chat: Ctrl+I / Cmd+I
  │
  ├── Natural language prompt → code generation
  ├── Sees ALL existing code in file as context
  ├── Options: Accept / Refine / Reject
  │
  ├── Slash commands:
  │     /doc   → generate documentation (minimal)
  │     /test  → generate unit tests (separate file)
  │     /new   → generate entire workspace (chat panel, not inline)
  │
  └── Explicit prompts > slash commands for quality
```

***

## Iterative Build Sequence

```
1. Create file: two_plate_aws.py

2. Ctrl+I → "create key pair"              → accept → [test → delete resources]
3. Ctrl+I → "create security group"        → accept → [test → delete resources]
4. Select all → Ctrl+I → "create EC2..."   → ⚠️ verify URLs → accept → [test → delete]
5. Select all → Ctrl+I → "add ALB..."      → accept → save

6. Select all → Ctrl+I → "modular structure"    → functions created → accept
7. Select all → Ctrl+I → "add comments/docs"    → docstrings added → accept
8. Select all → Ctrl+I → /test                  → unit tests → save as _test.py

Result: Modular, documented, tested script — built iteratively with verification
```

***

## Prompt Quality Rule

```
BAD:   "create EC2 instance"                          (vague, insufficient context)
GOOD:  "create EC2 instance with this security group   (short + specific details)
        and key pair, Amazon Linux 2023, T2 Micro,
        UserData to set up website from tooplate.com"

Rule: SHORT as possible + SPECIFIC as possible
```

***

## Copilot Verification Checklist

```
After EVERY generation, check:
  ├── URLs/external references → paste in browser, verify they exist
  ├── Variable references → do they match existing code?
  ├── API calls → correct Boto3 methods?
  ├── Resource names → consistent across the script?
  └── Import statements → all needed modules imported?

⚠️ Copilot can hallucinate: URLs, package names, API endpoints, AMI IDs
```

***

## Boto3 Pattern Revealed by Copilot

```
Security Group creation = 2 API calls:
  1. ec2.create_security_group()         → creates SG (no rules)
  2. sg.authorize_security_group_ingress() → adds inbound rules

EC2 Instance creation:
  1. Get AMI ID (lookup latest Amazon Linux)
  2. Define UserData (bash script as string)
  3. ec2.run_instances(AMI, type, key, SG, UserData)

ALB creation:
  1. Create ALB
  2. Create target group
  3. Register instance to target group
  4. Add SG rule for port 80
```

***

## Modular Refactoring Flow

```
Linear script (all in one block)
    │
    │ Ctrl+I → "modular structure"
    ▼
Functions (one per task)
    ├── create_key_pair()
    ├── create_security_group()
    ├── get_latest_ami()
    ├── launch_ec2_instance()
    ├── create_load_balancer()
    └── main() → calls all above in sequence

WHY: Reuse (import functions into other scripts), readability, maintainability
```

***

## Documentation Hierarchy

```
/doc command          → minimal (main function docstring only)
Explicit prompt       → comprehensive (every function + comments)
  "add comments and docstrings"

Docstring value: callable from other scripts to describe function purpose
```

***

## Workspace Generation — Known Failure Modes

```
/new → generates folder structure + all files
    │
    Known errors:
    ├── Case mismatches (config defines lowercase, main imports UPPERCASE)
    ├── Missing variables (imports reference vars that don't exist in source)
    ├── Missing imports (functions from other files not imported in main.py)
    └── Phantom references (IDE flags unused imports for non-existent vars)

Fix requires: reverse engineering > forward building
Conclusion: Use for scaffolding only, not for working code
```

***

## Core Philosophy

```
AI (Copilot) = FORCE MULTIPLIER for existing knowledge

Prerequisites YOU must have:
  ├── AWS knowledge (to verify infra code is correct)
  ├── Python basics (to debug syntax/logic errors)
  └── Boto3 understanding (to verify API calls make sense)

AI without domain knowledge = unverifiable output
AI with domain knowledge = accelerated, efficient development

"Use AI tools as your assistants, not as a replacement"
"Go slowly. Step by step."
"We definitely cannot give complete control."
```

***

## Test & Cleanup Discipline

```
After testing any intermediate script:
  ├── Resources were created in AWS
  ├── MUST delete them before next iteration
  └── Why: Next run creates same resources again → duplicates / conflicts

Pattern: Generate → Test → Delete → Add more → Test → Delete → ...
```

***

## File Artifacts

```
Step-by-step output:
  two_plate_aws.py        → main script (modular, documented)
  two_plate_aws_test.py   → unit tests (generated via /test)

Workspace output:
  src/
  ├── config.py            → variables (resource names, IPs)
  ├── keypair.py           → key pair function
  ├── security_group.py    → SG function
  ├── ec2.py               → EC2 function
  ├── load_balancer.py     → ALB function
  └── main.py              → orchestrator (calls all functions)
```

***

## Key Engineering Patterns

| Pattern                                    | Manifestation                                                                           |
| ------------------------------------------ | --------------------------------------------------------------------------------------- |
| **Iterative generation with verification** | Build one piece → verify → build next; errors caught locally, not compounded            |
| **Context-aware generation**               | Copilot reads existing code; each generation references established variables/resources |
| **Modular refactoring**                    | Linear script → functions → importable, reusable components                             |
| **Documentation as code**                  | Docstrings generated alongside code, callable for self-description                      |
| **Test generation from implementation**    | Unit tests auto-generated from existing code structure                                  |
| **Scaffolding vs. working code**           | Workspace generation = structural starting point; step-by-step = working code           |
| **Human-in-the-loop verification**         | Every AI output must be reviewed; URLs verified; imports checked; logic validated       |
| **Tool amplification, not replacement**    | AI multiplies existing knowledge; without domain expertise, output is unverifiable      |

***

## Course Continuity

```
BEFORE: Learned Boto3 manually, understood AWS APIs, Python programming
THIS:   Used GitHub Copilot to accelerate Boto3 script development
        Learned iterative AI-assisted development workflow
        Compared step-by-step vs whole-workspace generation
AFTER:  End of AWS Cloud Automation with Python section
```

***

This completes the full reconstruction. **Theory** builds understanding of Copilot's interaction model, the iterative vs. whole-generation tradeoff, and the "assistant not replacement" philosophy. **Practical** gives you the exact workflow — every keystroke, prompt, and verification step. The **Compression Map** lets you rapidly recall the entire methodology, from prompt rules to known failure modes. Let me know if you'd like Anki flashcards or any section expanded! 🚀
