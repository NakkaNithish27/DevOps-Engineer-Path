# AWS CodeBuild — Deep Learning Material

**Source:** [286-code-build.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt?EntityRepresentationId=70dc1c54-1101-42ea-a822-0763faceb0c9) (VTT Caption File), with supporting references from [286.buildspec.yml](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286.buildspec.yml?EntityRepresentationId=ba6a5ded-be82-4e43-a896-773f395b2a6c) and [286.GitMigration.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286.GitMigration.txt?EntityRepresentationId=2c99a371-5ff7-453f-bc53-66f7265a2ef9)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 What Is AWS CodeBuild?

AWS CodeBuild is a **fully managed continuous integration (CI) service** that compiles source code, runs tests, and produces deployable software packages (artifacts). The instructor frames it with a powerful anchoring comparison: **CodeBuild is the AWS cloud version of Jenkins**. If you understand Jenkins, you already understand the *purpose* of CodeBuild — it automates the build process. The fundamental difference lies not in *what* it does, but in *how it consumes compute resources*. [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

With Jenkins, you must provision and continuously run an **EC2 instance** (or a virtual machine, or a physical server). That instance runs 24/7 regardless of whether builds are happening or not — you pay for idle time. CodeBuild eliminates this entirely. It operates on a **pay-as-you-go model**: when you trigger a build, AWS provisions compute resources (RAM, CPU, memory) dynamically for the duration of that build. When the build finishes, the resources are released. You only pay for the actual build time consumed. There is no persistent server to manage, patch, or keep running. [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

The mapping between the two systems is direct: a **CodeBuild project** is conceptually equivalent to a **Jenkins job** (or Jenkins pipeline). You create a project, configure it with a source, build instructions, and output destination — then you run it. [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

> 🔍 **Deep Dive**
> The pay-as-you-go model has a deeper architectural implication: CodeBuild is **serverless CI**. There is no instance lifecycle to manage — no AMI updates, no disk space monitoring, no Jenkins plugin maintenance, no Java version conflicts on the server. The trade-off is that you lose the persistent console output that Jenkins provides. Once a build finishes, the compute is gone. This is why CloudWatch log integration (covered later) becomes essential — it's the only way to retain build output after execution. [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

***

## 1.2 The Build Spec File — The Core of CodeBuild

The **buildspec.yml** file is the central configuration mechanism of CodeBuild. It is a YAML-formatted file that contains **all the build instructions** — what to install, what commands to run before building, the actual build command, post-build actions, and what artifacts to produce. The instructor emphasizes this clearly: *"The main thing in CodeBuild is the build spec file."* [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

The buildspec file is to CodeBuild what a `Jenkinsfile` (or a job's build steps) is to Jenkins — it defines the entire build pipeline declaratively. The current version of the buildspec format is **0.2**. [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286.buildspec.yml)

### 1.2.1 Buildspec Structure — Phases

The buildspec file organizes build logic into **phases** — sequential stages that execute in a defined order. Each phase contains a `commands` section where you list shell commands as a YAML list (hyphen-prefixed entries). The phases available are: [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

1. **`install`** — Used to install tools, runtimes, and dependencies needed for the build. This phase has a special sub-key called `runtime-versions` where you can declaratively specify language runtimes (e.g., `java: corretto17`). CodeBuild knows how to interpret these declarations and installs the specified runtime automatically — you don't need to write manual installation commands for supported runtimes. [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286.buildspec.yml)

2. **`pre_build`** — Commands that must execute **before** the main build command. This is where you perform setup tasks: downloading specific tool versions (like Maven 3.9.8), modifying configuration files (like replacing database credentials in `application.properties` using `sed`), installing utilities (`apt-get install -y jq`), and any other preparation work. [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286.buildspec.yml)

3. **`build`** — The actual build command. In this lecture, it is simply `mvn install`, which compiles the Java source code, runs tests, and produces the artifact. [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286.buildspec.yml)

4. **`post_build`** — Commands that run **after** the build completes. In this lecture, `mvn package` is used here. The instructor explicitly notes this is **not strictly necessary** — `mvn install` already produces the artifact — but it is included to demonstrate that post-build steps exist and can contain additional commands. [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286.buildspec.yml)

The key insight is that these phases are simply **organized groups of shell commands**. There is no magic — it's "just commands," but divided into logical stages for clarity and control flow. [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

### 1.2.2 Environment Variables

The buildspec file supports an `env` section where you can define **environment variables** as key-value pairs. It also supports **parameter store** integration (AWS Systems Manager Parameter Store) for injecting secrets. In this lecture, the env section is commented out, but the instructor acknowledges its existence and notes that in the DevOps project course, these are covered in detail. [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286.buildspec.yml)

### 1.2.3 Artifacts Section

After all phases complete, the `artifacts` section defines **what output to capture** and where to send it. The configuration uses two keys: [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286.buildspec.yml)

* **`files`** — Specifies which files to include. The pattern `**/*` means "all files recursively."
* **`base-directory`** — Specifies the root directory from which to collect artifacts. In this case, `target/vprofile-v2` — the directory created by Maven after the build.

The entire content of the base directory is archived and sent to the configured destination (an S3 bucket in this case). The artifact is **not** the `.war` file alone — it is the entire extracted directory that would be deployed. If a destination like S3 is configured, CodeBuild archives the folder and copies it there. If deployment is configured, it deploys the folder content. [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

> 🔍 **Deep Dive**
> The artifacts section also supports **name overriding** — you can rename the output artifact to something different from the default directory name. The AWS documentation provides examples of targeting specific subdirectories, individual files, or all files within a path. The instructor recommends consulting the documentation as needed rather than memorizing all options. [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

***

## 1.3 Source Provider Connection — Bitbucket Authentication Mechanisms

CodeBuild needs to **fetch source code** from a repository. The source provider is selected during project creation. Supported providers include **Bitbucket, GitHub, and GitLab**. This lecture uses Bitbucket. [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

Connecting CodeBuild to Bitbucket requires authentication. The lecture walks through **four distinct mechanisms**, each with different security characteristics: [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

1. **Bitbucket App** — A connection managed entirely by AWS. This is what the lecture uses. You create a named connection (e.g., `bitbucketvproapp`), and if you are already logged into Bitbucket in the same browser, the connection is established automatically. If not, you are prompted to log in (e.g., via Google account). Once connected, your repositories and branches become selectable in CodeBuild. [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

2. **OAuth App** — Similar to the Bitbucket App, but with an extra feature: the OAuth token can be stored in **AWS Secrets Manager**. The instructor notes that Secrets Manager is not a free service. You can also choose to let CodeBuild manage the token directly without Secrets Manager. [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

3. **Personal Access Token (PAT)** — A **premium feature** of Bitbucket. The instructor describes this as the more recommended way but skips it because it requires a paid Bitbucket tier. [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

4. **App Password** — You provide your Bitbucket **username and password** directly. The instructor explicitly warns against this: *"Passwords are generally avoided for security reasons, they can be exposed easily."* This is the least secure option. To find the username, go to Bitbucket → gear icon → Personal Bitbucket Settings. The username can be viewed and changed there. App passwords can be generated from the same settings area. [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

> ⚠️ **Expert Note**
> The hierarchy of connection security (from most to least recommended) as implied by the lecture is: **PAT > Bitbucket App / OAuth App > App Password**. For production CI/CD pipelines, avoid app passwords entirely. PATs are ideal because they can be scoped with fine-grained permissions and rotated independently of the user account. [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

***

## 1.4 Build Environment Configuration

When creating a CodeBuild project, you configure the **build environment** — the compute container in which the build executes. Key decisions include: [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

* **Provisioning Model**: "On Demand" (pay-as-you-go) is the default. There is also a "Reserved Capacity" option, but the lecture uses on-demand. [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

* **Environment Image**: **AWS Managed Image** is the simplest choice — AWS provides pre-built Docker images with common tools pre-installed. Alternatively, you can specify a **custom Docker image** if you need specialized tools or configurations. [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

* **Compute Type**: EC2 or Lambda. Lambda is described as "much faster and cheaper," but EC2 is used in this lecture. [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

* **Operating System**: Ubuntu is selected. [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

* **Image Version**: **7.0** is selected. The instructor gives an important operational warning: as time passes, AWS will release newer image versions. However, he advises to **stick with 7.0** unless a new lecture is released confirming compatibility. Newer versions may introduce breaking changes. [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

* **Compute Resources**: The minimum is selected — **3 GB memory, 2 vCPUs**. [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

* **Service Role**: A **new service role** is created automatically. This IAM role grants CodeBuild the permissions it needs to access other AWS services (S3, CloudWatch, source repositories, etc.). [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

***

## 1.5 S3 Bucket — Artifact Storage Destination

Before creating the CodeBuild project, an **S3 bucket** must be created to store the build artifacts. The critical constraints are: [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

* The bucket must be in the **same region** as the CodeBuild project.
* The bucket name must be **globally unique** across all of AWS. The instructor suggests adding numbers to make it unique.
* No special configuration is needed — just create the bucket with a name and accept defaults.

The example name used is `awscicdvproartifact`. During CodeBuild project configuration, this bucket is selected under the artifacts section as the destination where the built artifact will be uploaded. [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

***

## 1.6 CloudWatch Logs — Build Output Persistence

Because CodeBuild is serverless and ephemeral, there is no persistent Jenkins-like console output that you can revisit anytime. The build compute exists only during the build. If you miss the output, it is gone — **unless** you configure CloudWatch Logs. [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

CloudWatch Logs captures the entire build output and stores it persistently. The configuration involves two identifiers:

* **Group Name** — A logical container for related log streams (e.g., `vprofileproject`).
* **Stream Name** — A specific log stream within the group (e.g., `vprobuild`).

Later, you can navigate to **CloudWatch → Log Groups → group name → stream name** to read the full build output. Beyond just reading, CloudWatch enables actions on logs — alerting, filtering, metric extraction, and more. [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

> ⚠️ **Expert Note**
> In production, CloudWatch Logs become your primary debugging tool for build failures. Without them, diagnosing a failed build becomes nearly impossible since the compute environment no longer exists. Always enable CloudWatch Logs for every CodeBuild project. [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

***

## 1.7 The `sed` Command — In-Build Configuration Injection

A significant portion of the pre\_build phase uses the **`sed`** (stream editor) command to perform **search-and-replace** operations on the `application.properties` file within the source code. This file lives at `src/main/resources/application.properties` and contains database connection settings (JDBC URL, username, password) that default to local development values (e.g., `db01:3306`, `admin`, `admin123`). [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286.buildspec.yml)

During the build, these values must be replaced with the **actual RDS instance details** — the production database endpoint, username, and password. The `sed -i` command modifies the file **in place** inside the build environment. The pattern is:

```bash
sed -i 's/OLD_VALUE/NEW_VALUE/' filepath
```

Three substitutions are made: [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286.buildspec.yml)

1. `jdbc.password=admin123` → `jdbc.password=<RDS_PASSWORD>`
2. `jdbc.username=admin` → `jdbc.username=<RDS_USERNAME>`
3. `db01:3306` → `<RDS_ENDPOINT>:3306`

This approach of injecting environment-specific configuration at build time (rather than hardcoding production values in the repository) is a common CI/CD pattern. The source code remains environment-agnostic; the build process adapts it to the target environment. [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

***

## 1.8 Buildspec File Placement — Two Approaches

The instructor mentions two ways to provide the buildspec file to CodeBuild: [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

1. **Inline Editor** — Paste the buildspec content directly into the CodeBuild console editor. This is what the lecture does. You switch to the "Editor" mode in the build commands section and paste the YAML content.

2. **In Source Code** — Place the `buildspec.yml` file in the root of your source code repository and specify its path. The instructor explicitly calls this *"the better way"* because it keeps the build definition version-controlled alongside the code.

The lecture also notes that the buildspec file is available from two sources: the **resource section** of the lecture, and within the **Bitbucket repository** itself under the `aws-ci` branch at `AWS files/buildspec.yml`. [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

***

## 1.9 Maven in the Build Context

Maven 3.9.8 is downloaded and installed manually in the `pre_build` phase rather than relying on whatever Maven version might be pre-installed in the AWS managed image. The installation sequence is: download the tarball via `wget` → extract it with `tar xzf` → create a symbolic link (`ln -s apache-maven-3.9.8 maven`) renaming the extracted directory to simply `maven`. When `mvn` is later invoked, it resolves to this specific Maven installation. [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286.buildspec.yml)

The `mvn install` command in the build phase compiles the source, runs tests, and produces the artifact. The `mvn package` in post\_build is redundant for this project (install already packages), but demonstrates that multiple commands can exist in any phase. [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

***

## 1.10 Git-to-Git Migration (Reference)

The supplementary file [286.GitMigration.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286.GitMigration.txt?EntityRepresentationId=2c99a371-5ff7-453f-bc53-66f7265a2ef9) provides a concise command sequence for migrating a Git repository (with full history) from one remote to another: [\[286.GitMigration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286.GitMigration.txt)

```
git clone <old-repo-url>
git branch -a
git checkout <branch-name>
git fetch --tags
git remote rm origin
git remote add origin <new-repo-url>
git push origin --all
git push --tags
```

This preserves all branches, tags, and commit history during the migration. The process is: clone the source → check out all branches → fetch all tags → remove the old remote → add the new remote → push everything (branches and tags) to the new destination. [\[286.GitMigration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286.GitMigration.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are creating an **AWS CodeBuild project** that fetches Java source code from a Bitbucket repository, builds it using Maven, injects RDS database credentials into the configuration at build time, and stores the resulting artifact in an S3 bucket. CloudWatch Logs are configured to persist the build output. This is the CI (Continuous Integration) stage of an AWS CI/CD pipeline. [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

By the end of this process: the CodeBuild project will be fully configured and ready to execute. The actual build execution and pipeline creation happen in the next lecture.

***

## Step 1: Create an S3 Bucket for Artifacts

Navigate to **AWS Console → S3 → Create bucket**.

| Field           | Value                                                                   |
| --------------- | ----------------------------------------------------------------------- |
| **Bucket name** | `awscicdvproartifact` (must be globally unique — add numbers if needed) |
| **Region**      | Same region as your CodeBuild project                                   |

Leave all other settings as defaults. Click **Create bucket**. [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

**Why first:** The S3 bucket must exist before the CodeBuild project is created, because you select this bucket as the artifact destination during project setup. If it doesn't exist yet, you won't be able to select it.

***

## Step 2: Open CodeBuild and Create a Project

Navigate to **AWS Console → search "CodeBuild" → open CodeBuild → Create project**.

| Field            | Value          |
| ---------------- | -------------- |
| **Project name** | `vproappbuild` |

This is equivalent to creating a Jenkins job — you are defining the build configuration. [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

***

## Step 3: Configure Source Provider (Bitbucket)

Under **Source provider**, select **Bitbucket**.

If no Bitbucket connection exists (indicated by a **red cross mark**), you need to create one: [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

1. Click **Manage account credentials** → opens a new tab.
2. You will see four authentication options. Select **Bitbucket app**.
3. Click **Create a new Bitbucket connection**.
4. Give it a name: `bitbucketvproapp`.
5. Click **Connect to Bitbucket**.
   * If you are already logged into Bitbucket in the same browser → connection happens automatically.
   * If not → a login window appears. Sign in with your Google account (or whatever you used for Bitbucket).
6. Select the new connection and click **Save**.
7. The tab closes (or return to the original tab manually).

Back on the CodeBuild source configuration: [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

| Field          | Value                                    |
| -------------- | ---------------------------------------- |
| **Repository** | Select your repository from the dropdown |
| **Branch**     | `aws-ci`                                 |

**Common mistake:** If you don't see your repository, the Bitbucket connection was not established successfully. Go back and verify the connection — look for the green checkmark replacing the red cross. [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

***

## Step 4: Configure Build Environment

Scroll down to the environment section: [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

| Field                  | Value                               |
| ---------------------- | ----------------------------------- |
| **Provisioning model** | On demand                           |
| **Environment image**  | AWS Managed Image                   |
| **Compute**            | EC2                                 |
| **Operating system**   | Ubuntu                              |
| **Runtime**            | Standard                            |
| **Image**              | 7.0                                 |
| **Service role**       | Create a new service role (default) |
| **Compute resources**  | 3 GB memory, 2 vCPUs (minimum)      |

**Operational warning on image version:** The instructor recorded in August 2024 with image 7.0. Newer images may be released over time. **Do not select a newer version** unless a new lecture confirms compatibility. Stick with 7.0 as long as it is available. [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

***

## Step 5: Configure Build Spec File

Under the build commands section, you have a choice: [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

* **"Use a buildspec file"** — references a file path in your source code (the better approach for production).
* **"Insert build commands" → switch to Editor** — paste the buildspec YAML inline.

For this lecture, select **"Insert build commands"** and click **"Switch to editor."**

### 5a: Obtain the Buildspec File

Get the file from either:

* The **resource section** of the lecture, or
* The **Bitbucket repository** → switch to branch `aws-ci` → navigate to `AWS files/buildspec.yml` → click "Open raw" → copy all content.

### 5b: Modify Database Credentials

Before pasting into CodeBuild, you must replace three values in the buildspec content with your actual RDS details. Open the copied content in a text editor (e.g., Sublime Text): [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286.buildspec.yml)

**Substitution 1 — Password:**

```yaml
- sed -i 's/jdbc.password=admin123/jdbc.password=<YOUR_RDS_PASSWORD>/' src/main/resources/application.properties
```

Replace `<YOUR_RDS_PASSWORD>` with the actual RDS master password you saved earlier (in sticky notes or a secure location). [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286.buildspec.yml)

**Substitution 2 — Username:**

```yaml
- sed -i 's/jdbc.username=admin/jdbc.username=<YOUR_RDS_USERNAME>/' src/main/resources/application.properties
```

If you kept the default username `admin`, this line requires no change. Only modify if you used a different username during RDS creation. [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286.buildspec.yml)

**Substitution 3 — Database Endpoint:**

```yaml
- sed -i 's/db01:3306/<YOUR_RDS_ENDPOINT>:3306/' src/main/resources/application.properties
```

Copy the endpoint from **RDS Console → your DB instance → Endpoint** field. Copy only the hostname (up to `.com`), not the port. The port `:3306` is already in the sed command. [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286.buildspec.yml), [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

**Where to find these values:**

* **Password**: Your saved sticky note / secure location from when you created the RDS instance.
* **Username**: RDS console or your notes.
* **Endpoint**: **AWS Console → RDS → Databases → select your instance → Connectivity & security → Endpoint**.

### 5c: Paste into CodeBuild

Select all the modified buildspec content, copy it, go to the CodeBuild editor pane, select everything in the editor, and paste. **Verify there are no YAML syntax errors** — the editor may show visual indicators. If errors exist, re-copy the original, re-apply changes, and re-paste. [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

### The Complete Buildspec File (for reference):

```yaml
version: 0.2

phases:
  install:
    runtime-versions:
      java: corretto17
  pre_build:
    commands:
      - apt-get update
      - apt-get install -y jq
      - wget https://archive.apache.org/dist/maven/maven-3/3.9.8/binaries/apache-maven-3.9.8-bin.tar.gz
      - tar xzf apache-maven-3.9.8-bin.tar.gz
      - ln -s apache-maven-3.9.8 maven
      - sed -i 's/jdbc.password=admin123/jdbc.password=<RDS_PASSWORD>/' src/main/resources/application.properties
      - sed -i 's/jdbc.username=admin/jdbc.username=<RDS_USERNAME>/' src/main/resources/application.properties
      - sed -i 's/db01:3306/<RDS_ENDPOINT>:3306/' src/main/resources/application.properties
  build:
    commands:
      - mvn install
  post_build:
    commands:
      - mvn package
artifacts:
  files:
    - '**/*'
  base-directory: 'target/vprofile-v2'
```

 [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286.buildspec.yml)

**Command-by-command breakdown of the pre\_build phase:**

| Command                                         | Purpose                                                               |
| ----------------------------------------------- | --------------------------------------------------------------------- |
| `apt-get update`                                | Updates the package index on the Ubuntu build container               |
| `apt-get install -y jq`                         | Installs `jq` (a JSON query utility); `-y` auto-confirms              |
| `wget https://...apache-maven-3.9.8-bin.tar.gz` | Downloads Maven 3.9.8 binary archive                                  |
| `tar xzf apache-maven-3.9.8-bin.tar.gz`         | Extracts the tarball (`x`=extract, `z`=gzip, `f`=file)                |
| `ln -s apache-maven-3.9.8 maven`                | Creates a symbolic link so `maven/` points to the extracted directory |
| `sed -i 's/OLD/NEW/' filepath`                  | In-place search-and-replace in `application.properties` (×3)          |

 [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286.buildspec.yml)

***

## Step 6: Configure Artifact Destination

Scroll down to the **Artifacts** section: [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

| Field                   | Value                                                |
| ----------------------- | ---------------------------------------------------- |
| **Type**                | Amazon S3                                            |
| **Bucket name**         | `awscicdvproartifact` (the bucket created in Step 1) |
| **Name/path**           | Leave empty (no folder name needed)                  |
| **Artifacts packaging** | Not required                                         |

This tells CodeBuild: after the build completes, take the contents of `target/vprofile-v2`, archive them, and upload to the specified S3 bucket. [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

***

## Step 7: Configure CloudWatch Logs

Scroll down to the **Logs** section. Ensure **CloudWatch logs** is enabled: [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

| Field           | Value             |
| --------------- | ----------------- |
| **Group name**  | `vprofileproject` |
| **Stream name** | `vprobuild`       |

**Why this matters:** Without CloudWatch, build logs are ephemeral — once the build compute is released, the output is gone forever. With this configuration, you can later navigate to **CloudWatch → Log Groups → `vprofileproject` → `vprobuild`** to read full build output, debug failures, and take further actions (alerts, metric filters, etc.). [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

***

## Step 8: Create the Build Project

Click **Create build project**. [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

**Do NOT run the build yet.** The instructor explicitly says to complete the project creation and stop — the build execution and pipeline creation happen in the next lecture.

**Verification:** After creation, the project should appear in the CodeBuild projects list with all configured settings visible (source: Bitbucket, environment: Ubuntu/7.0, artifacts: S3). [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

***

## Supporting Reference: Git-to-Git Migration

If you need to migrate your repository from one Git remote to another (preserving full history, all branches, and all tags), use this sequence from [286.GitMigration.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286.GitMigration.txt?EntityRepresentationId=2c99a371-5ff7-453f-bc53-66f7265a2ef9): [\[286.GitMigration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286.GitMigration.txt)

```bash
git clone <old-repo-url>        # Clone the source repository
git branch -a                    # List all branches (local + remote)
git checkout <branch-name>       # Check out each branch you want to migrate
git fetch --tags                 # Fetch all tags from the old remote
git remote rm origin             # Remove the old remote
git remote add origin <new-url>  # Add the new remote as origin
git push origin --all            # Push all branches to the new remote
git push --tags                  # Push all tags to the new remote
```

Repeat `git checkout <branch-name>` for **each branch** that exists on the old remote before removing the origin — otherwise those branches won't be in your local clone and won't be pushed. [\[286.GitMigration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286.GitMigration.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Core Identity

```
AWS CodeBuild = Serverless CI service = "Jenkins without the server"
  - Pay only for build time
  - No persistent EC2 instance
  - CodeBuild Project ≡ Jenkins Job
```

 [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

***

## System Architecture

```
Bitbucket Repo (aws-ci branch)
       │
       ▼ [Source fetch via Bitbucket App connection]
AWS CodeBuild Project (vproappbuild)
       │
       ├── Environment: Ubuntu 7.0, EC2, 3GB/2vCPU
       ├── Runtime: Java Corretto 17
       ├── Build tool: Maven 3.9.8 (manually installed)
       ├── Config injection: sed → application.properties → RDS details
       │
       ├── Build: mvn install
       │
       ▼ [Artifact upload]
S3 Bucket (awscicdvproartifact)
       │
       └── Content: target/vprofile-v2/**/*
       
CloudWatch Logs ← build output persistence
  └── Group: vprofileproject / Stream: vprobuild
```

 [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286.buildspec.yml)

***

## Buildspec Phase Flow

```
version: 0.2

PHASES (sequential):
  install ──► runtime-versions: java corretto17
      │
  pre_build ──► apt-get update
              ├── install jq
              ├── wget Maven 3.9.8 → tar extract → ln -s symlink
              └── sed ×3 → inject RDS (password, username, endpoint) into application.properties
      │
  build ──► mvn install (compile + test + artifact)
      │
  post_build ──► mvn package (redundant here — demonstrative)

ARTIFACTS:
  files: **/*
  base-directory: target/vprofile-v2
  destination: S3 bucket
```

 [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286.buildspec.yml), [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

***

## Bitbucket Connection Mechanisms (Security Hierarchy)

```
Most Secure ──────────────────────────── Least Secure
   PAT              Bitbucket App        App Password
 (premium)          / OAuth App        (username+password)
   ▲                    ▲                    ▲
   │                    │                    │
 Recommended       Used in lecture      "Avoid — easily exposed"
```

 [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

***

## Configuration Injection Pattern (sed)

```
Source code (application.properties):
  jdbc.password=admin123     ← dev default
  jdbc.username=admin        ← dev default
  db01:3306                  ← dev default

  ──sed -i 's/OLD/NEW/'──►

Build-time values:
  jdbc.password=<RDS_PWD>   ← production
  jdbc.username=<RDS_USER>  ← production (may be same)
  <RDS_ENDPOINT>:3306       ← production

Location in repo: src/main/resources/application.properties
```

 [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286.buildspec.yml), [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

***

## Key Operational Decisions

```
Image version: 7.0 (PINNED — do not use newer unless verified)
Compute: EC2 (Lambda = faster/cheaper alternative)
Environment: AWS Managed Image (custom Docker = alternative)
Provisioning: On-demand (Reserved = alternative)
Service role: Auto-created (new role)
Buildspec location: Inline editor (better = in source code repo)
```

 [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

***

## Ephemeral Compute → Log Persistence Problem

```
Jenkins: persistent instance → console output always available
CodeBuild: ephemeral compute → output vanishes after build

Solution: CloudWatch Logs
  ├── Group name → logical container
  └── Stream name → specific build stream
  
  Post-build access: CloudWatch → Log Groups → group → stream
```

 [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

***

## Maven Installation Chain

```
wget (download) → tar xzf (extract) → ln -s (symlink as "maven")
                                            │
                                     mvn command resolves here
```

 [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286.buildspec.yml)

***

## S3 Bucket Constraints

```
Region: MUST match CodeBuild project region
Name: MUST be globally unique (add numbers)
Create BEFORE CodeBuild project (dependency)
```

 [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

***

## Git Migration Flow (Separate Reference)

```
clone old → checkout all branches → fetch tags → rm old origin → add new origin → push --all → push --tags
                                                        │
                                          History + branches + tags preserved
```

 [\[286.GitMigration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286.GitMigration.txt)

***

## Reusable Engineering Patterns

**Serverless CI Pattern (Pay-per-Use Compute)**

```
No persistent server → compute provisioned per build → released after
  Benefit: zero idle cost, zero server maintenance
  Trade-off: no persistent state → must externalize logs/artifacts
  Recurrence: Lambda, Fargate, CodeBuild — same serverless principle
```

**Build-Time Config Injection Pattern**

```
Source code contains environment-agnostic defaults
  → CI pipeline injects target-environment values at build time
  → Artifact becomes environment-specific without polluting the repo
  Tool: sed / envsubst / template engines
  Principle: code is environment-agnostic; pipeline is environment-aware
```

**Phased Build Pipeline Pattern**

```
install → pre_build → build → post_build → artifacts
  Each phase = group of sequential commands
  Separation = clarity + failure isolation (know which phase failed)
  Recurrence: Jenkins stages, GitLab CI stages, GitHub Actions steps
```

**Externalized State Persistence Pattern**

```
Ephemeral compute → externalize everything that must survive:
  Logs → CloudWatch
  Artifacts → S3
  Secrets → Parameter Store / Secrets Manager
  Pattern: if the compute dies, where does this data live?
```

 [\[286-code-build \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/286-code-build.txt)

***

This completes the full reconstruction of the CodeBuild lecture. The three sections are designed as complementary layers — **Theory** for deep understanding, **Practical** for confident execution, and the **Compression Map** for rapid future recall. Let me know if you'd like any section expanded or adjusted! 🚀
