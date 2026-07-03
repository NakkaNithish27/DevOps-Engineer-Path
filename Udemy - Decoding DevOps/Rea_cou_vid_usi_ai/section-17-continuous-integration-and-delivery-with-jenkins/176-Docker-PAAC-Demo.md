# 🎓 Docker CI Pipeline with Amazon ECR — PAAC Demo (Lecture 176)

**Video Title:** Docker PAAC (Pipeline as a Code) Demo — CI with Docker & ECR
**Resource File:** [176. PAAC\_CI\_DockerECR.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.%20PAAC_CI_DockerECR.txt?EntityRepresentationId=5d880592-dc01-484f-9245-150472980d96) (Jenkins Pipeline Code)
**Context:** This lecture is the culmination of the CI pipeline series. Up to this point, the pipeline could fetch code, build it, test it, analyze it with SonarQube, and enforce a quality gate. Now we are adding **Docker** to the pipeline — building a Docker image from the application artifact and pushing it to **Amazon ECR** (Elastic Container Registry). This transforms the pipeline output from a raw `.war` file into a deployable container image, which is the modern standard for application delivery. [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

***

***

## 🧠 SECTION 1: THEORY — Deep Learning Mode

***

### 1. The Shift from Artifact to Container Image — Why Docker in CI?

The instructor opens by saying we are going to execute the prerequisites and then execute the pipeline. This implies we are transitioning the CI pipeline's **output format**. Previously, the pipeline produced a `.war` file and uploaded it to Nexus. Now, the pipeline will produce a **Docker image** — a self-contained, portable package that includes the application, its runtime environment, and all dependencies. [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

Why does this matter? A `.war` file requires a pre-configured Tomcat server to run. That means someone (or some automation) must provision a server, install Java, install Tomcat, configure it, and then deploy the `.war`. A Docker image eliminates all of that — the image itself contains everything needed to run the application. You just run the container, and the application works. This is the fundamental reason Docker has become the standard delivery mechanism in modern DevOps.

***

### 2. Amazon ECR — What It Is and Why We Need It

The instructor explicitly defines ECR: **"Amazon ECR is a place where we can store Docker images, and the place where we store Docker images are called as registry. Container registry or Docker registry."** [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

**Amazon ECR (Elastic Container Registry)** is a fully managed Docker container registry provided by AWS. It serves the same purpose for Docker images that Nexus serves for Maven artifacts — it is a centralized, versioned storage location. When the CI pipeline builds a Docker image, that image needs to be stored somewhere that deployment systems can pull from. ECR is that storage location.

The term **"registry"** in the Docker world is equivalent to **"repository"** in the Maven world — it's where you push (upload) and pull (download) images. ECR is specifically an **AWS-native** registry, meaning it integrates tightly with other AWS services like ECS (Elastic Container Service) and EKS (Elastic Kubernetes Service) for deployment.

The instructor also foreshadows: **"In later lecture, we'll need it when we deploy our Docker image to AWS ECS."** This tells us ECR is not the final destination — it's the handoff point between CI and CD, just like Nexus was for the non-Docker pipeline. [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

***

### 3. AWS CLI — Why It's Installed Now for Later Use

The instructor installs AWS CLI on the Jenkins server and explicitly says: **"It is not required for this lecture, but in later lecture, we'll need it when we deploy our Docker image to AWS ECS."** [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

AWS CLI (Command Line Interface) is a tool that lets you interact with AWS services from the terminal. In this lecture, Jenkins interacts with ECR through the Docker pipeline plugin (which handles authentication and push internally), so the CLI isn't needed yet. However, when the pipeline later deploys to ECS, it will need to run AWS CLI commands to update ECS services or task definitions. The instructor is being efficient — installing it now while we're already SSH'd into the Jenkins server, rather than coming back later.

***

### 4. Docker Engine vs. Docker Desktop — An Important Distinction

When installing Docker on the Jenkins server, the instructor makes a deliberate point: **"You have to install Docker Engine. Not Docker Desktop."** He repeats this warning when navigating the Docker documentation: **"You'll also see here Docker Desktop. Do not click to that. We are going to install Docker Engine."** [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

**Docker Engine** is the server-side, headless runtime — it runs as a daemon (background service) on Linux servers and provides the `docker` command-line tool. It's what you install on servers, CI machines, and production hosts.

**Docker Desktop** is a GUI application designed for developers' local machines (macOS, Windows). It includes Docker Engine inside a lightweight VM, plus a graphical interface, Kubernetes integration, and other developer tools. It is **not appropriate** for a server environment — it's heavier, designed for interactive use, and unnecessary on a headless Linux server like Jenkins.

This is a common mistake for beginners who search "install Docker" and land on the Docker Desktop page instead of Docker Engine.

***

### 5. The Docker Group — Why Jenkins Can't Run Docker by Default

After installing Docker Engine, the instructor demonstrates a critical permission issue. He first runs `docker images` as the **root** user — it works fine. Then he switches to the **Jenkins** user and runs the same command — **"it says permission denied."** [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

This is because Docker runs as a daemon owned by `root`, and its socket (`/var/run/docker.sock`) is accessible only to the `root` user and members of the **`docker` group**. When Docker Engine is installed, it automatically creates a `docker` group, but no users are added to it by default (other than root).

Jenkins executes all pipeline commands as the `jenkins` user. The instructor confirms this by referencing a previous lecture: **"You've seen in the first job, we execute `whoami` command — it says Jenkins."** So if the `jenkins` user is not in the `docker` group, any `docker` command in a Jenkins pipeline will fail with "permission denied." [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

The solution is to add the `jenkins` user to the `docker` group, which the instructor does with the `usermod` command. After that, a **reboot** is required (or at minimum a Jenkins service restart) so that the Jenkins process picks up the new group membership.

> 🔍 **Deep Dive (Optional):**
> Adding a user to the `docker` group effectively gives that user **root-equivalent access** to the host machine, because Docker containers can mount the host filesystem and run as root inside the container. In production environments, this is a significant security consideration. Alternatives include running Docker commands via `sudo` in the pipeline (less clean), using rootless Docker, or running Jenkins itself as a Docker container with the Docker socket mounted (Docker-in-Docker or Docker-outside-of-Docker patterns).

***

### 6. IAM User, Policies, and Access Keys — How Jenkins Authenticates with AWS

To push Docker images to ECR, Jenkins needs to **authenticate** with AWS. This is done through an **IAM (Identity and Access Management) user** with programmatic access. [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

The instructor creates an IAM user named `Jenkins` and attaches **two policies**:

1.  **AmazonEC2ContainerRegistryFullAccess** — grants permission to push and pull images from ECR.
2.  **AmazonECSFullAccess** — grants permission to manage ECS clusters and services (needed for the deployment lecture that follows).

The instructor then creates an **access key** for this user. An access key consists of two parts:

*   **Access Key ID** — like a username for programmatic access.
*   **Secret Access Key** — like a password for programmatic access.

These two values together allow any system (in our case, Jenkins) to authenticate as this IAM user and perform actions within the permissions granted by the attached policies. The instructor downloads these as a **CSV file** and stores them for later use. [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

The instructor explicitly warns: **"It's extremely risky to show access key and secret key like this. But as soon as I'm done recording this lecture, I'm going to delete these keys."** This is the same security pattern seen with the Nexus credentials — lab-only exposure, never acceptable in production. [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

> ⚠️ **Expert Note (Optional):**
> In production, you would avoid long-lived access keys entirely. Instead, you'd assign an **IAM Role** directly to the Jenkins EC2 instance (an instance profile). The instance would automatically receive temporary credentials that rotate every few hours, with no keys to manage, store, or accidentally leak. Access keys are a simpler but less secure approach, appropriate for learning environments.

***

### 7. The Four Jenkins Plugins — What Each One Does

The instructor installs four plugins for Docker/ECR integration: [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

**7a. Amazon Web Services SDK: All**
This is a foundational plugin that provides the AWS SDK (Software Development Kit) libraries to Jenkins. Other AWS-related plugins depend on it. It also enables a new credential type in Jenkins — **AWS Credentials** — which allows you to store AWS access keys securely in Jenkins' credential store. The instructor specifically notes: **"This option you'll get after installing the AWS-SDK plugin."** [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

**7b. Amazon ECR**
This plugin provides Jenkins with the ability to authenticate with Amazon ECR. When a pipeline needs to push or pull images from ECR, this plugin handles the ECR-specific authentication flow (which involves exchanging IAM credentials for a Docker login token). Without it, you'd need to manually run `aws ecr get-login-password` commands in your pipeline. [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

**7c. Docker Pipeline**
This plugin provides pipeline-friendly steps for building, tagging, and pushing Docker images. It exposes the `docker.build()` and `docker.withRegistry()` methods used in the pipeline code. These are higher-level abstractions that make Docker operations clean and readable in a Jenkinsfile, instead of writing raw `sh 'docker build ...'` commands. [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

**7d. CloudBees Docker Build and Publish**
This plugin adds additional Docker build and publish capabilities to Jenkins. It complements the Docker Pipeline plugin by providing UI-based job configuration for Docker operations and additional pipeline steps for building and publishing Docker images. [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

The instructor also notes: **"Docker has so many other plugins also. Based on your use case, you're going to use those plugins. For our exercises, we are using these plugins. But it's not limited to that."** This is an important perspective — the plugin set is use-case-driven, not fixed. [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

***

### 8. The Pipeline Code Structure — Environment Variables and Their Roles

The pipeline code (from [176. PAAC\_CI\_DockerECR.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.%20PAAC_CI_DockerECR.txt?EntityRepresentationId=5d880592-dc01-484f-9245-150472980d96)) defines three environment variables that are central to the Docker/ECR integration: [\[176. PAAC_..._DockerECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.%20PAAC_CI_DockerECR.txt)

```groovy
environment {
    registryCredential = 'ecr:us-east-2:awscreds'
    appRegistry = "951401132355.dkr.ecr.us-east-2.amazonaws.com/vprofileappimg"
    vprofileRegistry = "https://951401132355.dkr.ecr.us-east-2.amazonaws.com"
}
```

**`registryCredential`** — This is a composite string in the format `ecr:<region>:<jenkins-credential-id>`. It tells the ECR plugin which AWS region to authenticate against and which Jenkins credential to use. The `ecr:` prefix tells the plugin this is an ECR-type authentication (not a standard Docker Hub login). The instructor emphasizes: **"This is the same name of the Jenkins credentials. If you've given a different name, make sure you put that over there."** [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

**`appRegistry`** — This is the **full image name** including the ECR registry URL. The format is `<aws-account-id>.dkr.ecr.<region>.amazonaws.com/<repository-name>`. This is used in the `docker.build()` step to tag the image with the correct registry path so Docker knows where to push it. The instructor shows how to get this value: go to ECR, copy the **URI** of the repository. [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

**`vprofileRegistry`** — This is the **registry URL** (without the repository/image name), prefixed with `https://`. It's used in the `docker.withRegistry()` step to tell Docker which registry to log into. The instructor specifically warns: **"After HTTPS, you have to copy the part, just make sure there is no slash vprofile image."** — meaning you must strip the image name and trailing slash, leaving only the base registry URL. [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

***

### 9. Docker Image Tagging Strategy — Build Number as Tag

The pipeline tags each Docker image with the Jenkins **build number** (`$BUILD_NUMBER`), and also tags it as `latest`: [\[176. PAAC_..._DockerECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.%20PAAC_CI_DockerECR.txt)

```groovy
dockerImage.push("$BUILD_NUMBER")
dockerImage.push('latest')
```

This means every pipeline execution produces an image tagged with its unique build number (1, 2, 3, ...) **and** overwrites the `latest` tag. This dual-tagging strategy allows two access patterns: you can pull a **specific version** by build number (for rollbacks or auditing), or you can always pull the **most recent** version using the `latest` tag.

The instructor verifies this in ECR: **"Try running the build few more times and you'll see different tags over here. 1, 2, 3, based on the build ID."** [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

***

### 10. The Cleanup Problem — Why Docker Images Must Be Removed After Push

After the image is successfully pushed to ECR, the instructor identifies a problem: **"The image is in the Jenkins as well. So we need to add a stage where we remove the image after this upload is completed."** [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

Every time `docker.build()` runs, it creates a Docker image on the Jenkins server's local disk. Over multiple builds, these images accumulate and consume disk space. Since the image is already safely stored in ECR, keeping it on Jenkins is wasteful and eventually dangerous — the server can run out of disk space, causing all subsequent builds to fail.

The solution is a cleanup stage that forcefully removes all local Docker images after the push completes. This is a standard practice in CI pipelines that build Docker images.

***

### 11. Command Substitution in the Cleanup Command

The cleanup command uses a Linux concept called **command substitution**: [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

```bash
docker rmi -f $(docker images -a -q)
```

The instructor explicitly calls this out: **"You've seen command substitution in Linux. So the command is `docker images -a -q`. It's going to list all the image IDs. So this command substitution is going to list all the image IDs and present it to this command, which is going to remove the Docker image forcefully."** [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

Command substitution (`$(...)`) executes the inner command first, captures its output, and inserts that output into the outer command. So `docker images -a -q` produces a list of image IDs, and those IDs become arguments to `docker rmi -f`, which deletes them all.

***

***

## ⚙️ SECTION 2: PRACTICAL — Guided Execution Mode

***

### What We Are Building

We are extending the existing CI pipeline to **build a Docker image** of the application and **push it to Amazon ECR**. The pipeline already fetches code, builds with Maven, runs tests, performs SonarQube analysis, and enforces a quality gate. We are adding two new stages: **Build App Image** and **Upload App Image**, plus a cleanup stage to remove local images.

**Why it matters:** This transforms the pipeline output from a server-dependent `.war` file into a portable, self-contained Docker image — the standard unit of deployment in modern cloud-native architectures.

**Final outcome:** A fully automated pipeline that, on every run, produces a versioned Docker image in ECR, ready to be deployed to ECS or any container orchestration platform. [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

***

### Step 1: SSH into the Jenkins Server

```bash
ssh -i <key-path> ubuntu@<jenkins-public-ip>
```

This is the standard SSH command used throughout the course to access the Jenkins EC2 instance. `<key-path>` is the path to your `.pem` private key file, `ubuntu` is the default username for Ubuntu AMIs on AWS, and `<jenkins-public-ip>` is the instance's public IPv4 address from the AWS EC2 console. [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

***

### Step 2: Update the Package Index

```bash
sudo apt update
```

`sudo` runs the command with root privileges. `apt` is the package manager for Ubuntu/Debian. `update` refreshes the local package index — it does not install anything, but it ensures the system knows about the latest available versions of all packages. This should always be run before installing new software to avoid installing outdated versions. [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

***

### Step 3: Install AWS CLI

```bash
sudo snap install aws-cli --classic
```

`snap` is an alternative package manager on Ubuntu that installs applications as self-contained "snap" packages. `aws-cli` is the AWS Command Line Interface package. `--classic` is a confinement flag — it gives the snap full access to the system (without sandboxing), which the AWS CLI needs because it must read configuration files and credentials from various system paths. [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

The instructor reminds us: **"It is not required for this lecture, but in later lecture, we'll need it when we deploy our Docker image to AWS ECS."** We're installing it now opportunistically. [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

***

### Step 4: Switch to Root User and Install Docker Engine

```bash
sudo -i
```

This switches to the root user. The instructor then navigates to the Docker documentation at `docs.docker.com` → **Manuals** → **Docker Engine** → **Install** → **Ubuntu**. [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

The installation involves two groups of commands from the official Docker documentation:

**First group — Set up the Docker repository:**
These commands add Docker's official GPG key and APT repository to the system, so Ubuntu knows where to download Docker packages from. The instructor says: **"These are the commands to set the repository."** You copy these directly from the Docker docs. [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

**Second group — Install Docker Engine and Docker CLI:**
This is the actual installation command. The instructor adds `-y` to the command: **"Let's put `-y` so it doesn't ask us any question."** The `-y` flag automatically answers "yes" to all confirmation prompts, allowing the installation to proceed without manual intervention. [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

**Verify Docker is running:**

```bash
systemctl status docker
```

`systemctl` is the Linux service manager. `status docker` checks whether the Docker daemon (background service) is running. You should see **"active (running)"** in the output. Press `q` to quit the status view. [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

***

### Step 5: Test Docker as Root vs. Jenkins User

The instructor demonstrates the permission issue:

```bash
docker images
```

As root, this works — it lists all Docker images (currently empty). [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

Then he switches to the Jenkins user:

```bash
su - jenkins
docker images
```

This fails with **"permission denied"**. The `jenkins` user does not have permission to interact with the Docker daemon because it's not in the `docker` group. [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

***

### Step 6: Add Jenkins User to the Docker Group

Exit back to the root user first (`exit`), then run: [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

```bash
usermod -a -G docker jenkins
```

Let's break down every part:

| Part        | Meaning                                                                           |
| ----------- | --------------------------------------------------------------------------------- |
| `usermod`   | The command to modify a user account                                              |
| `-a`        | **Append** — add the user to the group without removing them from other groups    |
| `-G docker` | Specifies the **supplementary group** to add the user to — in this case, `docker` |
| `jenkins`   | The **username** being modified                                                   |

The instructor initially misstates the order but corrects himself: **"This is going to add the Jenkins user in the Docker group."** [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

**Verify the group membership:**

```bash
id jenkins
```

This command displays all group memberships for the `jenkins` user. You should see `docker` listed among the groups. [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

> ⚠️ **Expert Note (Optional):**
> The `-a` (append) flag is critical. Without it, `usermod -G docker jenkins` would **replace** all existing supplementary groups with just `docker`, potentially removing the user from other important groups and breaking the system. Always use `-aG` together when adding a user to an additional group.

***

### Step 7: Reboot the Jenkins Server

```bash
reboot
```

The instructor explains why: **"We need to restart the Jenkins service so it loads all these things. Or the best way, what I do is we have a chance to reboot Jenkins. When we do reboot, all the services will get restarted. All the configurations will be loaded."** [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

A reboot is a clean way to ensure the Jenkins process picks up the new group membership. The `jenkins` process must be restarted after the group change — simply running `newgrp docker` in a terminal won't affect the Jenkins daemon. A full reboot guarantees everything is cleanly reloaded.

**What to do while waiting:** The instructor uses this waiting time productively — he proceeds to the AWS console to create the IAM user and ECR repository while Jenkins reboots. [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

***

### Step 8: Create an IAM User in AWS

Navigate to the **IAM** service in the AWS console. Go to **Users** → **Create User**. [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

| Setting         | Value                                  | Reasoning                                                 |
| --------------- | -------------------------------------- | --------------------------------------------------------- |
| **User name**   | `Jenkins`                              | Identifies this as the user Jenkins will authenticate as  |
| **Permissions** | Attach policies directly               | Simplest approach for a single-purpose service account    |
| **Policy 1**    | `AmazonEC2ContainerRegistryFullAccess` | Allows pushing/pulling images to/from ECR                 |
| **Policy 2**    | `AmazonECSFullAccess`                  | Allows managing ECS clusters (needed in the next lecture) |

The instructor searches for these policies by typing `container` and `ECS` respectively in the policy search bar. After reviewing the selections, click **Create user**. [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

***

### Step 9: Create Access Keys for the IAM User

After the user is created, click on the user name → **Security credentials** → scroll down to **Access keys** → **Create access key**. [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

Select the **CLI** use case (since Jenkins will use these keys programmatically). Check the acknowledgment checkbox ("I understand..."), click **Next**, then **Create access key**.

**Critical:** Click **Download .csv file** immediately. This CSV contains both the **Access Key ID** and the **Secret Access Key**. The secret key is shown **only once** — if you lose it, you must create a new key pair. Store this file securely. [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

***

### Step 10: Create the ECR Repository

Search for **ECR** in the AWS console. Click on **Elastic Container Registry**. Click **Create repository**. [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

| Setting             | Value            |
| ------------------- | ---------------- |
| **Repository name** | `vprofileappimg` |

That's all you need to configure. Click **Create**. [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

After creation, the ECR console shows the repository with its **URI** — this URI is what you will use in the pipeline code. It follows the format:

    <aws-account-id>.dkr.ecr.<region>.amazonaws.com/vprofileappimg

The instructor specifically points out this URI and its relationship to the pipeline code: **"If you check our pipeline, that is it like that. So you have to replace your code with this one."** [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

***

### Step 11: Install Jenkins Plugins

Go to the Jenkins UI → **Manage Jenkins** → **Plugins** → **Available plugins**. Search for and select these four plugins: [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

1.  **Amazon Web Services SDK: All** — search `AWS`
2.  **Amazon ECR** — search `ECR`
3.  **Docker Pipeline** — search `docker`
4.  **CloudBees Docker Build and Publish** — search `docker`

Click **Install**. Wait for all plugins to install. [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

***

### Step 12: Store AWS Credentials in Jenkins

Go to **Dashboard** → **Manage Jenkins** → **Credentials** → **System** → **Global credentials** → **Add Credentials**. [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

| Field                 | Value             | Explanation                                                            |
| --------------------- | ----------------- | ---------------------------------------------------------------------- |
| **Kind**              | `AWS Credentials` | This option appears only after installing the AWS SDK plugin           |
| **ID**                | `awscreds`        | Must match what's in the pipeline code's `registryCredential` variable |
| **Description**       | `awscreds`        | Human-readable label                                                   |
| **Access Key ID**     | *(from CSV file)* | The first value in the downloaded CSV                                  |
| **Secret Access Key** | *(from CSV file)* | The second value in the CSV                                            |

The instructor warns: **"Make sure these things are copied properly. Access key, secret key will be separated by comma, so make sure you do not copy the comma."** This is a common mistake — the CSV file separates values with commas, and accidentally including a comma in the key will cause authentication failures. [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

Click **Create**.

***

### Step 13: Update the Pipeline Code

Open the pipeline code from [176. PAAC\_CI\_DockerECR.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.%20PAAC_CI_DockerECR.txt?EntityRepresentationId=5d880592-dc01-484f-9245-150472980d96) and update three environment variables to match **your** AWS account and region: [\[176. PAAC_..._DockerECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.%20PAAC_CI_DockerECR.txt)

**`registryCredential`:**

```groovy
registryCredential = 'ecr:<your-region>:<your-jenkins-credential-id>'
```

The instructor changes `us-east-2` to `us-east-1` because that's where his ECR repository was created: **"US East 1 in the same place where we created the registry."** Your region must match where you created the ECR repository. [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

**`appRegistry`:**

```groovy
appRegistry = "<your-ecr-uri>/vprofileappimg"
```

Go to ECR, copy the repository URI, and paste it here. This is the full image path including the repository name. [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

**`vprofileRegistry`:**

```groovy
vprofileRegistry = "https://<your-ecr-base-url>"
```

This is the ECR URL **without** the repository/image name at the end. The instructor emphasizes: **"After HTTPS, you have to copy the part, just make sure there is no slash vprofile image."** [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

***

### Step 14: Understanding the Pipeline Stages

Let's walk through what each stage in the pipeline does, referencing the actual code: [\[176. PAAC_..._DockerECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.%20PAAC_CI_DockerECR.txt)

**Stage: Fetch code**

```groovy
git branch: 'docker', url: 'https://github.com/hkhcoder/vprofile-project.git'
```

Clones the `docker` branch (not `main` or `master`) of the vprofile project. This branch contains the Dockerfile and Docker-specific configurations.

**Stage: Build**

```groovy
sh 'mvn install -DskipTests'
```

Builds the Java application with Maven, skipping tests (tests are run in a separate stage). The `post { success { archiveArtifacts } }` block archives the `.war` file in Jenkins after a successful build.

**Stage: UNIT TEST**

```groovy
sh 'mvn test'
```

Runs the unit tests separately.

**Stage: Checkstyle Analysis**

```groovy
sh 'mvn checkstyle:checkstyle'
```

Runs static code style analysis.

**Stage: Sonar Code Analysis**
Runs the SonarQube scanner with all the project-specific parameters.

**Stage: Quality Gate**

```groovy
waitForQualityGate abortPipeline: true
```

Waits for SonarQube's quality gate result. If the code fails the quality gate, the entire pipeline aborts — no Docker image is built from bad code.

**Stage: Build App Image** *(NEW — Docker-specific)*

```groovy
dockerImage = docker.build(appRegistry + ":$BUILD_NUMBER", "./Docker-files/app/multistage/")
```

This is the first new Docker stage. Let's break it down:

*   `docker.build()` — builds a Docker image (provided by the Docker Pipeline plugin)
*   `appRegistry + ":$BUILD_NUMBER"` — tags the image as `<ecr-uri>/vprofileappimg:<build-number>`. For example, build #1 produces the tag `:1`
*   `"./Docker-files/app/multistage/"` — the **build context path** where the Dockerfile is located. The instructor confirms: **"In our repository in the docker branch, Docker-files, app, multistage, Dockerfile."** [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

**Stage: Upload App Image** *(NEW — Docker-specific)*

```groovy
docker.withRegistry(vprofileRegistry, registryCredential) {
    dockerImage.push("$BUILD_NUMBER")
    dockerImage.push('latest')
}
```

*   `docker.withRegistry()` — logs into the specified Docker registry using the given credentials
*   `dockerImage.push("$BUILD_NUMBER")` — pushes the image with the build number tag
*   `dockerImage.push('latest')` — pushes the same image with the `latest` tag

The instructor confirms the pipeline output: **"Docker login. It is doing a login to our registry, login succeeded, and there it tags the image. You see the tag? That is the build ID. Docker push, it's pushing and it's completed."** [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

***

### Step 15: Create and Execute the Pipeline Job in Jenkins

Go to the Jenkins dashboard → **New Item**: [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

| Setting  | Value                |
| -------- | -------------------- |
| **Name** | `docker-ci-pipeline` |
| **Type** | Pipeline             |

Click **OK**. Scroll down to the **Pipeline** section. Select **Pipeline script** (inline). Paste the entire pipeline code. Click **Save**. [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

Click **Build Now** to trigger the pipeline.

**Expected result:** All stages pass — Fetch, Build, Unit Test, Checkstyle, Sonar Analysis, Quality Gate, Build App Image, Upload App Image. The instructor confirms: **"The pipeline completed successfully."** [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

**Verify in ECR:** Go to the ECR console, click on the `vprofileappimg` repository. You should see the image with its tag (the build number). Run the build a few more times and you'll see tags `1`, `2`, `3`, etc. [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

***

### Step 16: Add the Cleanup Stage — Remove Local Docker Images

The instructor identifies the problem and adds a new stage to the pipeline: [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

```groovy
stage('Remove Container Images') {
    steps {
        sh 'docker rmi -f $(docker images -a -q)'
    }
}
```

Let's break down the cleanup command completely:

| Part            | Meaning                                                                                |
| --------------- | -------------------------------------------------------------------------------------- |
| `docker rmi`    | **Remove image** — deletes Docker images from the local system                         |
| `-f`            | **Force** — removes images even if they are being used by stopped containers           |
| `$(...)`        | **Command substitution** — executes the inner command and uses its output as arguments |
| `docker images` | Lists Docker images                                                                    |
| `-a`            | **All** — includes intermediate (dangling) images, not just top-level ones             |
| `-q`            | **Quiet** — outputs only image IDs (no table headers, names, or sizes)                 |

So `docker images -a -q` outputs a list of all image IDs, and `docker rmi -f` deletes each one of them. [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

The instructor explains the real-world reasoning: **"Like this, our disk space will be freed every time we build a Docker image."** Without this cleanup, images accumulate on the Jenkins server — each image can be hundreds of megabytes or more, and over dozens of builds, this fills up the disk. [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

**To update the pipeline:** Go to the job → **Configure** → delete the old script → paste the updated script with the new cleanup stage → **Save** → **Build Now**. [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

**Verify:** In the console output, at the end you should see Docker images being deleted. The instructor confirms: **"You see at the end, it is going to delete all the images."** [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

***

### Step 17: Post-Lecture Guidance

The instructor closes with important context: [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

**"That is the end of the continuous integration."** — This pipeline now represents a **complete CI process**: fetch → build → test → analyze → quality gate → containerize → push to registry → cleanup.

**"We can add notifications also"** — implying that in a production setup, you'd add Slack/email notifications for build success/failure.

**"We have one more thing now to deliver this Docker image... that will start the continuous delivery process."** — The next phase is **CD (Continuous Delivery)**, where the image stored in ECR is deployed to a running environment (AWS ECS).

**"If you're going to continue to the next lecture, keep the instance running. If you're going to take a break, make sure you shut down your Jenkins and SonarQube instance."** — A cost-saving reminder for AWS usage. [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt)

***

***

## 🧭 Complete Pipeline Flow — Visual Map

    ┌──────────────────────────────────────────────────────────────────────────┐
    │                    COMPLETE CI PIPELINE (Lecture 176)                     │
    │                                                                          │
    │  1. FETCH CODE        ──→  Git clone (docker branch)                     │
    │  2. BUILD             ──→  mvn install -DskipTests → .war artifact       │
    │  3. UNIT TEST         ──→  mvn test                                      │
    │  4. CHECKSTYLE        ──→  mvn checkstyle:checkstyle                     │
    │  5. SONAR ANALYSIS    ──→  SonarQube scanner                             │
    │  6. QUALITY GATE      ──→  Pass/Fail gate (abort if fail)                │
    │  7. BUILD IMAGE  ★    ──→  docker.build() → Docker image with build tag  │
    │  8. UPLOAD IMAGE ★    ──→  docker.push() → Image in Amazon ECR           │
    │  9. CLEANUP      ★    ──→  docker rmi -f → Free local disk space         │
    │                                                                          │
    │  ★ = New stages added in this lecture                                    │
    │                                                                          │
    │  NEXT: Continuous Delivery → Deploy from ECR to AWS ECS                  │
    └──────────────────────────────────────────────────────────────────────────┘

## 🧭 Prerequisites Checklist — Summary

| Prerequisite                 | Where               | What                                                   |
| ---------------------------- | ------------------- | ------------------------------------------------------ |
| AWS CLI installed            | Jenkins server      | `sudo snap install aws-cli --classic`                  |
| Docker Engine installed      | Jenkins server      | From Docker docs (Ubuntu)                              |
| Jenkins user in docker group | Jenkins server      | `usermod -aG docker jenkins` + reboot                  |
| IAM user with access key     | AWS IAM             | `Jenkins` user with ECR + ECS policies                 |
| ECR repository created       | AWS ECR             | `vprofileappimg`                                       |
| 4 plugins installed          | Jenkins UI          | AWS SDK, Amazon ECR, Docker Pipeline, CloudBees Docker |
| AWS credentials stored       | Jenkins credentials | `awscreds` (AWS Credentials type)                      |

 [\[176.-Docke...-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.-Docker-PAAC-Demo.txt), [\[176. PAAC_..._DockerECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/176.%20PAAC_CI_DockerECR.txt)

***

Would you like me to save this as a downloadable markdown file?
