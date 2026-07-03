# 🎓 Deep Learning Material: Build and Deploy Artifacts — Maven Build, S3 Transfer, and Tomcat Deployment Pipeline

**Source:** Video lecture on building and deploying artifacts (from [136. Build and Deploy Artifacts.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt?EntityRepresentationId=5682f445-d739-4956-aea3-beb9ce7cd822) caption file) [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

**Video Context:** This is a critical hands-on lecture that ties together many previously learned concepts — Maven builds, S3 storage, IAM users with access keys, IAM roles on EC2, AWS CLI, and Tomcat deployment — into a single **end-to-end artifact pipeline**. The instructor builds a Java artifact (`.war` file) from source code on a local computer, pushes it to an S3 bucket as an intermediary storage, then pulls it from S3 onto a Tomcat EC2 instance and deploys it. Two different authentication mechanisms are used: **IAM access keys** (for the local computer → S3) and **IAM roles** (for the EC2 instance → S3). This dual-auth pattern and the overall pipeline structure are the highest-value engineering takeaways.

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — The Artifact Pipeline: Why S3 Sits in the Middle

The core problem this lecture solves is: **how do you get an application from source code on a developer's computer to a running service on a production server?** The answer is a pipeline with three stages: **Build → Transfer → Deploy**. [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

The instructor outlines the architecture explicitly at the start: *"We are going to build the artifact from the source code on our computer and we are going to push it to S3 bucket. And on the Tomcat instance app01, we are going to fetch that artifact and deploy to the Tomcat service."* [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

S3 serves as the **intermediary artifact store** — a neutral, accessible, durable location where the built artifact is placed after build and before deployment. The local computer pushes the artifact to S3; the Tomcat server pulls it from S3. Neither the local computer nor the server needs to directly connect to each other. This decoupling is architecturally significant: the build system and the deployment target are **independent**, connected only through a shared storage location. [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

> 🔍 **Deep Dive**
>
> This three-stage pipeline (build → store → deploy) is the foundational pattern behind all CI/CD systems. In production, the "local computer" is replaced by a CI server (Jenkins, GitHub Actions), the "S3 bucket" is replaced by an artifact repository (Nexus, JFrog Artifactory, or S3 itself), and the "manual SSH deploy" is replaced by automated deployment tools (Ansible, CodeDeploy, Kubernetes). The lecture is building the manual version of what will later be automated. The instructor confirms this: *"Next lecture, we are going to set up a load balancer and access our application through the load balancer."* — showing this is one step in a larger project build.

***

## 1.2 — The Tool Chain: What Each Component Does

The instructor carefully lists what's needed on each side of the pipeline: [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

**On the local computer (build side):**

* **Maven** — the build tool that compiles Java source code into a deployable artifact (`.war` file)
* **JDK (Java Development Kit)** — Maven needs JDK to compile Java code; the required version is **Java 17** with **Maven 3.9.9**
* **AWS CLI** — to communicate with the S3 bucket (push the artifact)

**On the Tomcat server (deployment side):**

* **AWS CLI** — to communicate with the S3 bucket (pull the artifact)
* **Tomcat 10** — the application server that runs the Java web application

The instructor emphasizes version compatibility: *"If you see different version than this, then go back to prerequisites section."* Mismatched versions between Maven, JDK, and the project requirements are a common source of build failures.

***

## 1.3 — Two Authentication Mechanisms: IAM Keys vs. IAM Roles

This is the most architecturally important concept in the lecture. Two different parts of the pipeline need to authenticate with S3, and they use **different authentication mechanisms** for good reasons. [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

### IAM Access Keys (Local Computer → S3)

The local computer is **not an AWS resource** — it's your personal workstation, outside of AWS. It cannot be assigned an IAM role. The only way for it to authenticate with AWS services is through **IAM access keys** (Access Key ID + Secret Access Key), configured via `aws configure`. [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

The instructor creates a dedicated IAM user (`vprofile-s3-admin`) with **only S3 Full Access** permissions — not AdministratorAccess. This follows the **principle of least privilege**: the user can interact with S3 and nothing else. [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

### IAM Roles (EC2 Instance → S3)

The Tomcat server **is** an AWS resource (an EC2 instance). AWS resources can use **IAM roles** instead of access keys. A role is a set of permissions that you "attach" to an instance. When the instance has a role, any AWS CLI command run on that instance automatically authenticates using the role's permissions — no access keys needed on the instance. [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

The instructor creates an IAM role (`s3-admin`) with S3 Full Access, then applies it to the `app01` instance via **Actions → Security → Modify IAM Role**. After this, any `aws s3` command run on `app01` works without running `aws configure` — the instance automatically authenticates through the attached role. [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

The instructor explains: *"From our instance, we can run AWS CLI command to authenticate with the S3 service and only S3 service because it has just the permission for S3."* [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

> 🔍 **Deep Dive**
>
> Why use roles on EC2 instead of access keys? Access keys are **static credentials stored as text files** — if the instance is compromised, the keys can be stolen and used from anywhere. IAM roles use **temporary credentials** that are automatically rotated by AWS and are only accessible from the instance itself (via the instance metadata service). Roles are fundamentally more secure for AWS-to-AWS communication. The lecture implicitly demonstrates the rule: **use access keys only when you're outside AWS (your laptop); use roles when you're inside AWS (EC2 instances)**. [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

***

## 1.4 — The `application.properties` File: Backend Service Configuration in the Artifact

Before building the artifact, the instructor checks the `application.properties` file located at `src/main/resources/`. This file contains the **hostnames of backend services** that the application connects to: the database (`db01.vprofile.in`), Memcached (`mc01.vprofile.in`), and RabbitMQ (`rmq01.vprofile.in`). [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

These hostnames correspond to **Route 53 private DNS records** that map to the private IPs of the respective EC2 instances. The instructor verifies: *"In Route 53, we created the record right, db01.vprofile.in points to the private IP of db01 instance."* [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

This is architecturally important because the `application.properties` file gets **baked into the artifact** during the build. If the backend hostnames are wrong, the application will fail to connect to its dependencies at runtime — and you'd have to rebuild and redeploy the artifact to fix it. The instructor emphasizes saving the file after verification (`Ctrl+S`). [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

***

## 1.5 — The Maven Build: Source Code → Artifact

Maven reads the project's configuration files (primarily `pom.xml`), compiles the Java source code using JDK, runs any defined tests, packages everything into a **`.war` file** (Web Application Archive), and places it in the `target/` directory. The artifact for this project is `vprofile-V2.war`. [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

The instructor explains the relationship between the `.war` file and its contents: *"This is an archive of this folder. Once it's extracted on Tomcat server, it should have this folder, this content of the folder. You should have web-INF classes, in that you should have application.properties file."* This means the `.war` is a compressed package that Tomcat will automatically extract into a directory when deployed. [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

***

## 1.6 — Tomcat Deployment Mechanics: The ROOT Convention

On Tomcat, the web application directory is `/var/lib/tomcat10/webapps/`. Inside this directory, there's a `ROOT` folder — this is the **default application** that Tomcat serves when you access the server. To deploy your own application as the default, you must: **(1)** remove the existing `ROOT` folder, **(2)** copy your `.war` file and rename it to `ROOT.war`, **(3)** start Tomcat. When Tomcat starts, it automatically extracts `ROOT.war` into a `ROOT` directory and serves it. [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

The instructor performs exactly this sequence: stop Tomcat → remove old ROOT → copy artifact as ROOT.war → start Tomcat → Tomcat extracts it. The extraction takes a moment: *"Let's do LS to webapps. Okay, still not extracted. Let's check once again. There."* [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

***

## 1.7 — Access Key Security: Repeated Critical Warning

The instructor reiterates the access key security warning seen in previous lectures, with additional detail about real-world consequences: *"Some people by mistake put their access keys in the source code repository, public repository. And what happens in that case, your keys will be taken from the public repository and people will start doing bitcoin mining in your AWS account and many other things... hijack your account, demand ransom... there are bots on the internet that scan public repositories and find these kind of information and use it."* [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

Immediate mitigation if exposure happens: *"Make sure quickly you delete those keys or remove those keys or even disable the user."* [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building and Why

We are building a **complete artifact deployment pipeline**: build a Java `.war` file from source code on our local machine, upload it to an S3 bucket, download it onto a Tomcat EC2 instance, and deploy it as the running web application. The final outcome: the vprofile application running on the Tomcat instance, accessible via HTTP, connected to its backend services via DNS records. The next lecture will add a load balancer in front of this.

***

## Phase 1: AWS Setup (S3 Bucket + IAM Keys + IAM Role)

### Step 1: Create the S3 Bucket

1. AWS Console → **S3** → **Create Bucket** [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)
2. Type: **General purpose**
3. Name: `vprofile-las-artifacts` (you must use a different unique name — add numbers to ensure uniqueness)
4. All other settings: default → **Create Bucket** [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

**Take note of the bucket name** — you'll use it in CLI commands later.

***

### Step 2: Create IAM User with S3 Access Keys (for Local Computer)

**What we're doing:** Creating credentials for the local computer to push artifacts to S3.

1. AWS Console → **IAM** → **Users** → **Create User** [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

2. Name: `vprofile-s3-admin` → **Next**

3. **Attach policies directly** → search `S3` → select **AmazonS3FullAccess** → **Next** → **Create User** [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

   **Why only S3 access:** Least privilege — this user only needs to interact with S3, nothing else.

4. Click on the user → **Security credentials** → scroll to **Access keys** → **Create access key** [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

5. Use case: **CLI** → acknowledge → **Create access key**

6. **IMMEDIATELY** click **Download .csv file** [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

   **If you miss this download, the secret key is gone forever.** You'll have to generate new keys.

***

### Step 3: Create IAM Role with S3 Access (for EC2 Instance)

**What we're doing:** Creating a role that the Tomcat instance will use to pull artifacts from S3 — no access keys needed on the server.

1. IAM → **Roles** → **Create role** [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)
2. Trusted entity: **AWS service** → Use case: **EC2** → **Next**
3. Search `S3` → select **AmazonS3FullAccess** → **Next** [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)
4. Role name: `s3-admin` → **Create role** [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

### Step 4: Attach the IAM Role to the Tomcat Instance

1. EC2 → select **app01** instance → **Actions** → **Security** → **Modify IAM role** [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)
2. Dropdown → select **s3-admin** → **Update IAM role** [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

**What this enables:** Any `aws s3` command run on `app01` now authenticates automatically through the role. No `aws configure` needed on the instance.

**Modifying permissions later:** You can edit the role anytime to add or remove permissions. [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

***

## Phase 2: Local Computer Setup and Artifact Build

### Step 5: Verify Backend Configuration in Source Code

**What we're doing:** Ensuring the application will connect to the correct backend services after deployment.

1. In VS Code (or your editor), navigate to: `src/main/resources/application.properties` [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)
2. Verify the hostnames:
   * Database: `db01.vprofile.in` (must match Route 53 record pointing to db01's private IP)
   * Memcached: `mc01.vprofile.in` (must match Route 53 record)
   * RabbitMQ: `rmq01.vprofile.in` (must match Route 53 record)
3. **Save the file** (`Ctrl+S`) [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

**Common mistake:** Forgetting to save after editing. If the file isn't saved, the build uses the old values.

**Why this matters:** These values get baked into the artifact. Wrong hostnames = application can't reach backends at runtime.

***

### Step 6: Verify Tool Versions

**What we're doing:** Confirming Maven, JDK, and AWS CLI are installed with correct versions.

Open a terminal (Git Bash on Windows, Terminal on Mac) in the source code directory. In VS Code: `Ctrl+Shift+P` → search "terminal select default profile" → select **Git Bash** (Windows) or **Terminal** (Mac) → **View** → **Terminal**. [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

**Check Maven and JDK:**

```bash
mvn -version
```

* **Expected:** Maven 3.9.9, Java 17 [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)
* If versions differ, go back to the "Installing Software" lecture in the prerequisites section

**Check AWS CLI:**

```bash
aws
```

* **Expected:** Help output showing AWS CLI is installed [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)
* If not installed, refer to the installing software lecture

***

### Step 7: Configure AWS CLI with Access Keys

**What we're doing:** Storing the IAM access keys on the local computer so the CLI can authenticate with S3.

```bash
aws configure
```

Prompts: [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

| Prompt                | Value                        |
| --------------------- | ---------------------------- |
| AWS Access Key ID     | From the downloaded CSV      |
| AWS Secret Access Key | From the CSV (after comma)   |
| Default region        | `us-east-1` (or your region) |
| Default output format | `json`                       |

**Credentials stored at:** `~/.aws/credentials` (access key + secret key) and `~/.aws/config` (region + output format). If you make a mistake, edit these files directly with any text editor. [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

***

### Step 8: Build the Artifact with Maven

**What we're doing:** Compiling the Java source code into a deployable `.war` file.

**Ensure you're in the project root directory** (where `pom.xml` is located).

```bash
mvn install
```

* `mvn` — invokes Maven
* `install` — the Maven lifecycle phase that compiles, tests, packages, and installs the artifact [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

**What happens:** Maven reads `pom.xml`, downloads dependencies, compiles Java files using JDK 17, runs tests, and packages everything into a `.war` file.

**Expected output:** `BUILD SUCCESS` message. A `target/` folder appears containing `vprofile-V2.war`. [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

**What's inside the `.war`:** An archive containing the compiled application. When extracted by Tomcat, it produces a directory with `WEB-INF/classes/application.properties` (the backend config we verified earlier) and all compiled code. [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

**Common failure:** Wrong JDK or Maven version → build errors. Go back to prerequisites and install correct versions.

***

### Step 9: Push the Artifact to S3

**What we're doing:** Uploading the built artifact to the S3 bucket as the intermediary storage.

```bash
aws s3 cp target/vprofile-V2.war s3://vprofile-las-artifacts
```

* `aws s3` — targets the S3 service
* `cp` — copy action
* `target/vprofile-V2.war` — source: the locally built artifact
* `s3://vprofile-las-artifacts` — destination: the S3 bucket (use YOUR bucket name) [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

If you have a subfolder in the bucket, append it: `s3://bucket-name/subfolder/`

**Expected output:** Upload completed message. [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

**Verify the upload:**

```bash
aws s3 ls s3://vprofile-las-artifacts
```

* Should list `vprofile-V2.war` with its size and date [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

**Troubleshooting if it fails:**

* **Authentication error** → re-run `aws configure`, verify keys from CSV
* **Access denied** → check IAM user has `AmazonS3FullAccess` policy attached [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

***

## Phase 3: Deploy on Tomcat Instance

### Step 10: SSH into the Tomcat Instance

```bash
ssh -i downloads/<key-name>.pem ubuntu@<app01-public-ip>
```

* Get the public IP from EC2 Console for `app01`
* If **connection timed out**: edit the instance's security group → inbound rules → add SSH (port 22) from My IP [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

**Switch to root:**

```bash
sudo -i
```

***

### Step 11: Install AWS CLI on the Instance

**What we're doing:** Installing AWS CLI so the instance can pull from S3. Using `snap` package manager on Ubuntu.

```bash
snap install aws-cli --classic
```

* `snap` — Ubuntu's alternative package manager
* `--classic` — allows the snap package full system access (required for AWS CLI) [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

**Verify:**

```bash
aws
```

* Should show help output [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

**Note:** No `aws configure` needed on this instance — the IAM role attached in Step 4 handles authentication automatically.

***

### Step 12: Pull the Artifact from S3

```bash
aws s3 cp s3://vprofile-las-artifacts/vprofile-V2.war /tmp/
```

* Source: `s3://` + your bucket name + `/` + artifact name
* Destination: `/tmp/` (temporary local storage on the instance) [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

**Expected output:** Download completed, fast. [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

***

### Step 13: Deploy the Artifact to Tomcat

**What we're doing:** Replacing Tomcat's default application with our artifact.

**Stop Tomcat:**

```bash
systemctl stop tomcat10
```

If you see a warning about configuration changes:

```bash
systemctl daemon-reload
```

Then retry the stop command. [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

**Check the webapps directory:**

```bash
ls /var/lib/tomcat10/webapps/
```

* You should see a `ROOT` folder — this is the default Tomcat application [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

**Remove the default application:**

```bash
rm -rf /var/lib/tomcat10/webapps/ROOT
```

⚠️ **Double-check this path before running `rm -rf`.** The instructor emphasizes: *"Make sure you give the rm command, rm -rf. And this path, exactly this path, remove it."* [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

**Copy the artifact as ROOT.war:**

```bash
cp /tmp/vprofile-V2.war /var/lib/tomcat10/webapps/ROOT.war
```

* Renaming to `ROOT.war` makes Tomcat serve this application as the default (root path `/`) [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

**Start Tomcat:**

```bash
systemctl start tomcat10
```

**Verify extraction:**

```bash
ls /var/lib/tomcat10/webapps/
```

* Should now show both `ROOT.war` and a `ROOT/` directory (extracted by Tomcat) [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)
* The extraction takes a few seconds — re-run `ls` if `ROOT/` doesn't appear immediately

**Connection to system flow:** The application is now deployed and running. The next lecture adds a load balancer in front of this instance to make it accessible to users. [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🔷 The Complete Pipeline (End-to-End)

```
LOCAL COMPUTER                    S3 BUCKET                     EC2 (app01)
──────────────                    ─────────                     ───────────
Source code                       Artifact store                Tomcat server
  │                                  │                             │
  ├── application.properties         │                             │
  │   (backend hostnames)            │                             │
  │                                  │                             │
  ├── mvn install                    │                             │
  │   → target/vprofile-V2.war       │                             │
  │                                  │                             │
  ├── aws s3 cp ──────────────────►  vprofile-V2.war              │
  │   (auth: IAM access keys)       │                             │
  │                                  │                             │
  │                                  │  ◄──── aws s3 cp ──────────┤
  │                                  │        (auth: IAM role)     │
  │                                  │                             │
  │                                  │        → /tmp/              │
  │                                  │        → stop tomcat        │
  │                                  │        → rm ROOT            │
  │                                  │        → cp as ROOT.war     │
  │                                  │        → start tomcat       │
  │                                  │        → auto-extract       │
  │                                  │                             │
  │                                  │              APPLICATION LIVE
```

***

## 🔷 Dual Authentication Pattern

```
LOCAL COMPUTER → S3                  EC2 INSTANCE → S3
─────────────────────                ─────────────────────
Auth: IAM ACCESS KEYS                Auth: IAM ROLE
Why: laptop is OUTSIDE AWS           Why: instance is INSIDE AWS
How: aws configure → stores keys     How: attach role to instance
     in ~/.aws/credentials                no aws configure needed
Risk: keys are static text files     Benefit: temp credentials, auto-rotated
     → can be stolen/leaked          → cannot be extracted
Rule: LEAST PRIVILEGE                Rule: LEAST PRIVILEGE
     (S3FullAccess only)                  (S3FullAccess only)

PRINCIPLE: Keys for outside AWS. Roles for inside AWS.
```

***

## 🔷 Tool Requirements by Location

```
LOCAL COMPUTER              EC2 INSTANCE (app01)
─────────────────           ─────────────────────
Maven 3.9.9                 AWS CLI (snap install)
JDK 17                      Tomcat 10
AWS CLI                     IAM Role (s3-admin)
IAM Access Keys
```

***

## 🔷 Build → Transfer → Deploy Commands

```
# LOCAL: Build
mvn install                          → target/vprofile-V2.war

# LOCAL: Push to S3
aws s3 cp target/vprofile-V2.war s3://<bucket-name>

# LOCAL: Verify
aws s3 ls s3://<bucket-name>

# EC2: Pull from S3
aws s3 cp s3://<bucket-name>/vprofile-V2.war /tmp/

# EC2: Deploy to Tomcat
systemctl stop tomcat10
systemctl daemon-reload              (if warning about config changes)
rm -rf /var/lib/tomcat10/webapps/ROOT
cp /tmp/vprofile-V2.war /var/lib/tomcat10/webapps/ROOT.war
systemctl start tomcat10

# EC2: Verify
ls /var/lib/tomcat10/webapps/        → ROOT.war + ROOT/ (extracted)
```

***

## 🔷 IAM Setup Summary

```
IAM USER (for local computer):
  Name: vprofile-s3-admin
  Policy: AmazonS3FullAccess
  → Generate access keys → download CSV → aws configure

IAM ROLE (for EC2 instance):
  Name: s3-admin
  Policy: AmazonS3FullAccess
  Trusted entity: EC2
  → Attach to app01: Actions → Security → Modify IAM role
```

***

## 🔷 application.properties → Route 53 → Backend Instances

```
application.properties (baked into artifact at build time):
  db01.vprofile.in   ──Route 53──► private IP of db01 instance
  mc01.vprofile.in   ──Route 53──► private IP of mc01 instance
  rmq01.vprofile.in  ──Route 53──► private IP of rmq01 instance

WRONG HOSTNAMES = app builds fine but FAILS at runtime
Must verify BEFORE mvn install. Must SAVE file after editing.
```

***

## 🔷 Tomcat Deployment Mechanics

```
/var/lib/tomcat10/webapps/     ← Tomcat's application directory
  ├── ROOT/                     ← default app (must remove)
  └── ROOT.war                  ← your artifact (renamed to ROOT.war)

Tomcat start → detects ROOT.war → auto-extracts to ROOT/ → serves at /

Naming convention: ROOT.war = served at root path (/)
                   other.war = served at /other
```

***

## 🔷 Troubleshooting Chain

```
Build fails (mvn install)?
  → Check Maven version (3.9.9) and JDK version (17)
  → Check you're in the correct directory (where pom.xml is)

S3 push fails?
  → Authentication error → re-run aws configure, verify CSV keys
  → Access denied → check IAM user policy (S3FullAccess)

S3 pull fails (on EC2)?
  → Check IAM role attached to instance
  → Check role has S3FullAccess policy

SSH connection timed out?
  → Security group → add SSH (port 22) from My IP

App doesn't start after deploy?
  → Check application.properties hostnames match Route 53 records
  → Check ROOT.war is correctly placed in webapps/
  → Check Tomcat is running: systemctl status tomcat10
  → Wait a few seconds for extraction after start
```

***

## 🔷 Access Key Security (Compressed)

```
DANGER: Keys in public Git repo → bots scan → crypto mining → huge bills / ransom

RULES:
  1. Download CSV immediately (secret shown once)
  2. Never commit keys to any repository
  3. Delete keys after use (instructor deletes after recording)
  4. If exposed: immediately delete keys OR disable user

MITIGATION: Use IAM roles on AWS resources instead of keys whenever possible
```

***

## 🔷 Reusable Engineering Pattern: Build → Store → Deploy with Split Authentication

```
PATTERN: Artifact Pipeline with Intermediary Storage

BUILD SYSTEM ──push──► ARTIFACT STORE ──pull──► DEPLOYMENT TARGET
(laptop/CI)            (S3/Nexus/ECR)           (server/container)

Auth model:
  Build → Store:   credentials-based (keys, tokens)
  Store → Deploy:  identity-based (roles, service accounts)

Why intermediary store?
  → Decouples build from deploy (independence)
  → Artifact is versioned, auditable, reusable
  → Multiple targets can pull the same artifact
  → Build happens once, deploy happens many times

This pattern scales to:
  Jenkins → Nexus → Ansible → servers
  GitHub Actions → ECR → Kubernetes → pods
  Local → S3 → CodeDeploy → ASG instances
  
The specific tools change. The pattern is constant.
```

This is the single most transferable engineering pattern from this lecture — it appears in every CI/CD system you'll ever work with. [\[136. Build...Artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/136.%20Build%20and%20Deploy%20Artifacts.txt)
