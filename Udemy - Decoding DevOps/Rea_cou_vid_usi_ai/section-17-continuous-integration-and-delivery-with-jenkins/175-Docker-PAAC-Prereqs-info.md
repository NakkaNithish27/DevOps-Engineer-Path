# 🎓 Docker Image Build & Push to Amazon ECR — CI Pipeline Integration

*Reconstructed from video lecture #175 and its accompanying pipeline resource*

***

## 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

### 1. The Shift: From Artifact Upload to Docker Image

In the previous pipeline stages, the CI flow was: fetch code → build → test → code analysis → quality gate → **upload artifact to a repository (like Nexus)**. The artifact was a `.war` file, and it was stored in an artifact repository for later deployment. Now, the approach changes fundamentally. Instead of uploading a `.war` file to Nexus, we are going to **build a Docker image** containing that artifact and **push it to Amazon ECR** (a Docker registry). The Docker image itself becomes the artifact. [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

This is a critical conceptual shift. In the traditional model, you ship a file (the `.war`) and then separately worry about the runtime environment (installing Tomcat, configuring it, deploying the `.war` into it). With Docker, you package **both** the application and its runtime environment into a single, self-contained image. Whoever pulls this image gets everything — Tomcat, the application, and the exact configuration — ready to run. This eliminates the "it works on my machine" problem entirely. [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

***

### 2. Jenkins and Docker — The Plugin Requirement

Jenkins does not have any built-in capability to build Docker images or push them to Docker registries. It is a general-purpose automation server — it knows how to run shell commands, manage pipelines, and orchestrate stages, but Docker-specific operations require a **plugin called Docker Pipeline**. [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

This plugin provides Groovy functions (like `docker.build()` and `docker.withRegistry()`) that you can use inside your Jenkinsfile. These functions internally translate into Docker CLI commands (`docker build`, `docker push`, `docker login`, etc.) and execute them on the Jenkins server. But here's the key distinction: the **plugin** provides the pipeline syntax and integration, while the actual Docker commands require the **Docker engine** to be installed on the Jenkins server itself. Without the engine, the plugin has nothing to execute against. [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

So two things are needed on Jenkins:

*   **Docker Pipeline plugin** — gives you the Groovy DSL functions in your Jenkinsfile
*   **Docker engine** — the actual runtime that executes `docker build`, `docker push`, etc. on the Jenkins server's operating system [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

> 🔍 **Deep Dive (Optional)**
>
> There are actually **three** plugins mentioned in this lecture that need to be installed: **Docker Pipeline**, **Amazon ECR**, and **AWS SDK**. Docker Pipeline provides the build/push functions. The Amazon ECR plugin enables Jenkins to authenticate with AWS ECR specifically. The AWS SDK plugin allows Jenkins to interact with AWS services and is needed to store and retrieve AWS credentials. All three work together — Docker Pipeline handles the Docker operations, ECR plugin handles ECR-specific authentication, and AWS SDK handles the underlying AWS credential management. [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

***

### 3. The `docker.build()` Function — Building a Docker Image

The first new pipeline stage is **Build App Image**. It uses the `docker.build()` function provided by the Docker Pipeline plugin. This function accepts **two arguments**: [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

1.  **Image name** (with tag) — the name to assign to the built image
2.  **Path to the Dockerfile** — where to find the build instructions

In the pipeline, it looks like this:

```groovy
dockerImage = docker.build(appRegistry + ":$BUILD_NUMBER", "./Docker-files/app/multistage/")
```

 [\[175. PAAC_..._DockerECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.%20PAAC_CI_DockerECR.txt)

The function is recognizable as a function by its **parentheses** — this is standard Groovy/Jenkins DSL syntax. When this executes, Jenkins internally runs the `docker build` CLI command on the Jenkins server, using the specified Dockerfile path and tagging the resulting image with the specified name. [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

The result is stored in a variable called `dockerImage`, which is then used in the next stage to push the image. This is wrapped inside a `script` block because `docker.build()` is a scripted pipeline function being used inside a declarative pipeline — the `script` block allows scripted syntax within declarative pipelines. [\[175. PAAC_..._DockerECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.%20PAAC_CI_DockerECR.txt)

***

### 4. The Dockerfile — What It Does (High Level)

The Dockerfile lives inside the source code repository, specifically at the path `Docker-files/app/multistage/`. To find it, you go to the GitHub repository URL, switch to the **docker** branch (this is important — not `main`, not `atom`, but `docker`), and navigate: `Docker-files → app → multistage → Dockerfile`. [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

This is a **two-stage (multistage) Dockerfile**: [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

*   **Stage 1:** Fetches the source code, switches to the `docker` branch, and runs `mvn install` to generate the `.war` artifact.
*   **Stage 2:** Takes a **Tomcat image** from Docker Hub, removes the default application from Tomcat, and copies the artifact built in Stage 1 into the Tomcat webapps directory.

The end result is a Docker image that contains a fully configured Tomcat server with the vprofile application deployed inside it — ready to run as a container. [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

> ⚠️ **Expert Note (Optional)**
>
> The instructor explicitly says: *"I don't want you to stress too much on the Dockerfile. We need to learn it in much detail in the Docker section."* The Dockerfile concepts will be covered thoroughly later. For now, the important thing is understanding that the Dockerfile contains the **instructions** for building the image, and the pipeline stage simply points to its location and triggers the build. [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

***

### 5. The `docker.withRegistry()` Function — Pushing to a Registry

The second new pipeline stage is **Upload App Image**. After building the image, we need to push it to a Docker registry where it can be stored and later pulled for deployment. The function used is `docker.withRegistry()`, which takes **two arguments**: [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

1.  **Registry URL** — the location of the Docker registry (in our case, Amazon ECR)
2.  **Registry credentials** — the credential ID stored in Jenkins that the plugin will use to authenticate

```groovy
docker.withRegistry(vprofileRegistry, registryCredential) {
    dockerImage.push("$BUILD_NUMBER")
    dockerImage.push('latest')
}
```

 [\[175. PAAC_..._DockerECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.%20PAAC_CI_DockerECR.txt)

What happens here is: the plugin **logs into** the Docker registry using the provided credentials (equivalent to `docker login`), and then inside the closure block, it **pushes** the image twice — once with the build number as the tag, and once with the `latest` tag. [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

***

### 6. Docker Tags — Versioning Images

When pushing the Docker image, two tags are applied: `$BUILD_NUMBER` and `latest`. Tags in Docker serve as **version identifiers** for images. The same image can have multiple tags pointing to it. [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

*   **`$BUILD_NUMBER`** — This is a Jenkins environment variable that auto-increments with each build (1, 2, 3, ...). Tagging with the build number gives you a unique, traceable version for every pipeline run. You can always go back to a specific build's image.
*   **`latest`** — This is Docker's **default tag**. When someone pulls an image without specifying a tag, Docker automatically uses `latest`. By pushing with this tag, you ensure that the most recent build is always accessible via the default pull command. [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

> 🔍 **Deep Dive (Optional)**
>
> The `latest` tag is not magic — it doesn't automatically point to the newest image. It's just a conventional name. You have to explicitly push to it (which is what the pipeline does). If you stop pushing to `latest`, it will remain pointing to whatever image was last pushed with that tag. This is a common source of confusion in Docker. [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

***

### 7. Pipeline Environment Variables — The Configuration Block

At the top of the pipeline, three variables are defined in the `environment` block. These are referenced throughout the Docker stages: [\[175. PAAC_..._DockerECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.%20PAAC_CI_DockerECR.txt), [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

```groovy
environment {
    registryCredential = 'ecr:us-east-2:awscreds'
    appRegistry = "951401132355.dkr.ecr.us-east-2.amazonaws.com/vprofileappimg"
    vprofileRegistry = "https://951401132355.dkr.ecr.us-east-2.amazonaws.com"
}
```

 [\[175. PAAC_..._DockerECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.%20PAAC_CI_DockerECR.txt)

**`registryCredential`** — This is the credential reference for the Docker plugin. Its format is specific: `ecr:<region>:<credential-name>`. The `ecr` prefix tells the plugin this is an ECR registry. `us-east-2` is the AWS region. `awscreds` is the **ID** of the credential stored in Jenkins (we will create this). The Docker plugin uses this format to know which authentication method to use and which AWS credential to retrieve. [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

**`appRegistry`** — This is the **full image name** including the ECR registry URL. The format is: `<AWS-account-ID>.dkr.ecr.<region>.amazonaws.com/<image-name>`. This is the naming convention AWS ECR uses. When you create an ECR repository, AWS gives you this URL. The part before the slash (`951401132355.dkr.ecr.us-east-2.amazonaws.com`) is the registry, and the part after (`vprofileappimg`) is the repository/image name. This variable is used in `docker.build()` to name the image correctly so it can be pushed to the right ECR repository. [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

**`vprofileRegistry`** — This is just the **registry URL** (with `https://` prefix), without the image name. This is used in `docker.withRegistry()` to specify where to log in. Notice: `appRegistry` and `vprofileRegistry` share the same base URL — the difference is that `appRegistry` includes the image name (used for building/naming) while `vprofileRegistry` is just the registry endpoint (used for authentication/login). [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

***

### 8. Amazon ECR — Elastic Container Registry

Amazon ECR is AWS's managed Docker registry service. It's where you store Docker images in the AWS ecosystem. Just like Docker Hub is a public Docker registry, ECR is a **private** registry hosted on AWS. You create a "repository" in ECR (which is essentially a named storage location for a specific image), and then you push/pull images to/from it. [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

When you create an ECR repository, AWS provides you with the registry URL in the format we discussed above. This URL is what you use in your pipeline to build, tag, and push images. [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

***

### 9. AWS IAM Credentials for Jenkins

For Jenkins to push images to ECR, it needs to authenticate with AWS. This is done through an **IAM user** with an **access key** and **secret key**. You create an IAM user in AWS specifically for this purpose, generate the access key pair, and then store those credentials in Jenkins' credential store (just like you store Sonar tokens or Nexus login credentials). [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

The Docker plugin (along with the AWS SDK plugin) retrieves these credentials at runtime and uses them to authenticate the `docker push` operation against ECR. The credential is referenced in the pipeline by its ID (`awscreds` in this case), which is embedded in the `registryCredential` variable format: `ecr:us-east-2:awscreds`. [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

***

### 10. Docker Engine on Jenkins + User Permissions

Since the Docker plugin executes actual Docker CLI commands on the Jenkins server, the **Docker engine** must be installed on the Jenkins machine itself. Without it, commands like `docker build` and `docker push` would simply fail with "command not found." [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

Additionally, there's a permissions consideration: Jenkins runs its processes as the **`jenkins` user** on the server. By default, the `jenkins` user does not have permission to run Docker commands — Docker commands require membership in the `docker` group. So you must **add the `jenkins` user to the `docker` group** and then **reboot** the Jenkins server for the group membership to take effect. Without this step, the pipeline would fail with a "permission denied" error when trying to execute Docker commands. [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

> 🔍 **Deep Dive (Optional)**
>
> The reboot is needed because group membership changes in Linux typically require a new login session to take effect. Since Jenkins runs as a system service, the simplest way to refresh the session is to reboot the server. Alternatively, you could restart just the Jenkins service, but a full reboot is the safest approach to ensure everything is clean. [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

***

### 11. AWS CLI Installation (Forward-Looking)

The video also mentions installing the **AWS CLI** on the Jenkins server. This is **not required for the current pipeline** (building and pushing Docker images). However, it will be needed in the **next phase — continuous delivery** — where the pipeline will need to interact with AWS services to deploy the containers. Installing it now saves time later. [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

***

## ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

### What We Are Building

We are extending the existing Jenkins CI pipeline for the **vprofile** project to include Docker image building and pushing to Amazon ECR. The pipeline already handles: code fetch → Maven build → unit test → Checkstyle → SonarQube analysis → quality gate. We are adding two new stages at the end: **Build App Image** (creates a Docker image containing our application) and **Upload App Image** (pushes that image to AWS ECR). The final outcome is a fully automated CI pipeline where every successful build produces a versioned Docker image stored in a cloud registry, ready for deployment. [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

This lecture focuses on **understanding the pipeline code and identifying all prerequisites**. The actual execution of these steps happens in the next lecture. [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

***

### Step 1: Understanding the Pipeline Structure

The pipeline is available in the lecture resource. Let's walk through every section. [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

**Agent and Tools:**

```groovy
pipeline {
    agent any
    tools {
        maven "MAVEN3.9"
        jdk "JDK17"
    }
```

 [\[175. PAAC_..._DockerECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.%20PAAC_CI_DockerECR.txt)

This is unchanged from previous lectures. `agent any` means the pipeline can run on any available Jenkins agent. The `tools` block ensures Maven 3.9 and JDK 17 are available for the build stages.

**Environment Block (NEW):**

```groovy
environment {
    registryCredential = 'ecr:us-east-2:awscreds'
    appRegistry = "951401132355.dkr.ecr.us-east-2.amazonaws.com/vprofileappimg"
    vprofileRegistry = "https://951401132355.dkr.ecr.us-east-2.amazonaws.com"
}
```

 [\[175. PAAC_..._DockerECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.%20PAAC_CI_DockerECR.txt)

This is new. These three variables hold all the AWS/ECR configuration:

*   **`registryCredential`** = `'ecr:us-east-2:awscreds'`
    *   `ecr` — tells the Docker plugin this is an ECR-type registry
    *   `us-east-2` — the AWS region where the ECR repository lives
    *   `awscreds` — the ID of the Jenkins credential that holds the AWS access key and secret key
    *   This specific format (`ecr:region:credentialId`) is required by the Docker plugin for ECR authentication [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

*   **`appRegistry`** = `"951401132355.dkr.ecr.us-east-2.amazonaws.com/vprofileappimg"`
    *   `951401132355` — the AWS account ID
    *   `.dkr.ecr.us-east-2.amazonaws.com` — the ECR registry domain for the `us-east-2` region
    *   `/vprofileappimg` — the ECR repository (image) name
    *   This full string is the **image name** used during `docker build`. When you create an ECR repository, this URL is provided by AWS. [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

*   **`vprofileRegistry`** = `"https://951401132355.dkr.ecr.us-east-2.amazonaws.com"`
    *   Same base URL as `appRegistry`, but with `https://` prefix and **without** the image name
    *   This is the **registry endpoint** used for `docker login` (via `docker.withRegistry()`) [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

***

### Step 2: Existing Stages (Quick Review)

```groovy
stage('Fetch code') {
    steps {
        git branch: 'docker', url: 'https://github.com/hkhcoder/vprofile-project.git'
    }
}
```

 [\[175. PAAC_..._DockerECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.%20PAAC_CI_DockerECR.txt)

Notice the branch is now **`docker`**, not `atom` (which was used in earlier lectures). This branch contains the `Docker-files` directory with the Dockerfile needed for the image build stage. [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

The remaining stages — Build, Unit Test, Checkstyle, Sonar Code Analysis, and Quality Gate — remain functionally the same as in previous lectures. They ensure the code is compiled, tested, analyzed, and quality-checked before we proceed to build a Docker image. [\[175. PAAC_..._DockerECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.%20PAAC_CI_DockerECR.txt)

***

### Step 3: Build App Image Stage (NEW)

```groovy
stage('Build App Image') {
    steps {
        script {
            dockerImage = docker.build(appRegistry + ":$BUILD_NUMBER", "./Docker-files/app/multistage/")
        }
    }
}
```

 [\[175. PAAC_..._DockerECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.%20PAAC_CI_DockerECR.txt)

**What we are doing:** Building a Docker image from the Dockerfile present in the source code.

**Why:** The Docker image is our deployable artifact — it contains both the application and its runtime environment (Tomcat), making it self-contained and portable.

**Command breakdown:**

*   `script { ... }` — allows scripted pipeline syntax inside a declarative pipeline. The `docker.build()` function requires scripted syntax.
*   `docker.build(...)` — the Docker Pipeline plugin's build function. It internally executes the `docker build` CLI command on the Jenkins server. [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)
*   **First argument:** `appRegistry + ":$BUILD_NUMBER"` — this constructs the full image name with tag. It evaluates to something like `951401132355.dkr.ecr.us-east-2.amazonaws.com/vprofileappimg:5` (where 5 is the current build number). This is the name and tag Docker assigns to the resulting image. [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)
*   **Second argument:** `"./Docker-files/app/multistage/"` — the path (relative to the workspace root) where the Dockerfile is located. Docker will look for a file named `Dockerfile` in this directory and execute its instructions. [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)
*   `dockerImage = ...` — the result of the build is stored in a variable called `dockerImage`. This variable is a Docker image object that can be used later (in the push stage) to interact with the built image. [\[175. PAAC_..._DockerECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.%20PAAC_CI_DockerECR.txt)

**What happens internally:** Jenkins, on its server, runs `docker build -t 951401132355.dkr.ecr.us-east-2.amazonaws.com/vprofileappimg:<build_number> ./Docker-files/app/multistage/`. Docker reads the multistage Dockerfile, executes both stages (build the artifact, then copy it into a Tomcat image), and produces a tagged image stored in the local Docker image cache on the Jenkins server. [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

**What the Dockerfile does (as explained in the video):**

*   Stage 1: Fetches source code, switches to docker branch, runs `mvn install` → generates the `.war` artifact
*   Stage 2: Takes a Tomcat base image from Docker Hub, removes the default application, copies the `.war` artifact from Stage 1 into Tomcat
*   Result: A Docker image with Tomcat + vprofile application, ready to run [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

***

### Step 4: Upload App Image Stage (NEW)

```groovy
stage('Upload App Image') {
    steps {
        script {
            docker.withRegistry(vprofileRegistry, registryCredential) {
                dockerImage.push("$BUILD_NUMBER")
                dockerImage.push('latest')
            }
        }
    }
}
```

 [\[175. PAAC_..._DockerECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.%20PAAC_CI_DockerECR.txt)

**What we are doing:** Pushing the built Docker image to Amazon ECR so it's stored in the cloud and available for deployment.

**Why:** A Docker image sitting only on the Jenkins server is useless for deployment. It needs to be in a centralized registry where deployment tools (ECS, Kubernetes, etc.) can pull it from.

**Command breakdown:**

*   `docker.withRegistry(vprofileRegistry, registryCredential)` — this function logs into the Docker registry specified by `vprofileRegistry` using the credentials referenced by `registryCredential`. Internally, it executes a `docker login` command. The ECR plugin and AWS SDK plugin handle the AWS-specific authentication flow (converting the access key/secret key into a Docker login token). [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)
*   `{ ... }` — the closure block. Everything inside this block executes in the context of an authenticated Docker session (i.e., already logged into ECR).
*   `dockerImage.push("$BUILD_NUMBER")` — pushes the image with the build number tag (e.g., `:5`). This gives a unique, traceable version. [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)
*   `dockerImage.push('latest')` — pushes the same image again with the `latest` tag. This ensures the most recent build is always available via the default tag. [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

**What happens internally:** Jenkins authenticates with ECR using AWS credentials → Docker pushes the image layers to the ECR repository → The image is now stored in ECR with two tags (build number and latest) → Anyone (or any service) with access to this ECR repository can pull and run this image.

***

### Step 5: Prerequisites Checklist (What Needs to Be Done Before Running)

The video carefully identifies all the prerequisites that must be completed before this pipeline can execute successfully. Here is the complete list as presented: [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

**On the Jenkins Server:**

1.  **Install Docker engine** — so Docker CLI commands (`docker build`, `docker push`) can actually execute. The Docker Pipeline plugin calls these commands, but they need the engine to run. [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

2.  **Add the `jenkins` user to the `docker` group** — Jenkins processes run as the `jenkins` Linux user. Without docker group membership, this user cannot execute Docker commands (permission denied). [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

3.  **Reboot the Jenkins server** — for the group membership change to take effect. [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

4.  **Install AWS CLI** — not needed for this pipeline, but will be needed in the next phase (continuous delivery). Install it now to save time later. [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

5.  **Install three Jenkins plugins:**
    *   **Amazon ECR** — enables ECR-specific authentication
    *   **Docker Pipeline** — provides `docker.build()`, `docker.withRegistry()`, and other Docker DSL functions
    *   **AWS SDK** — enables storing and retrieving AWS credentials in Jenkins [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

6.  **Store AWS credentials in Jenkins** — go to Jenkins credentials store and add the IAM user's access key and secret key. The credential ID must match what's referenced in the pipeline (`awscreds`). [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

**On AWS:**

7.  **Create an IAM user with access key and secret key** — this user's credentials will be stored in Jenkins and used by the Docker plugin to authenticate with ECR. [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

8.  **Create an ECR repository** — this is where the Docker images will be stored. When you create it, AWS provides the registry URL that you use in the pipeline's environment variables. [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

***

### Step 6: The Complete Pipeline (Full Reference)

Here is the complete pipeline with all stages, including the two new Docker stages, as provided in the resource file: [\[175. PAAC_..._DockerECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.%20PAAC_CI_DockerECR.txt)

```groovy
pipeline {
    agent any
    tools {
        maven "MAVEN3.9"
        jdk "JDK17"
    }
    environment {
        registryCredential = 'ecr:us-east-2:awscreds'
        appRegistry = "951401132355.dkr.ecr.us-east-2.amazonaws.com/vprofileappimg"
        vprofileRegistry = "https://951401132355.dkr.ecr.us-east-2.amazonaws.com"
    }
    stages {
        stage('Fetch code') {
            steps {
                git branch: 'docker', url: 'https://github.com/hkhcoder/vprofile-project.git'
            }
        }
        stage('Build') {
            steps {
                sh 'mvn install -DskipTests'
            }
            post {
                success {
                    echo 'Now Archiving it...'
                    archiveArtifacts artifacts: '**/target/*.war'
                }
            }
        }
        stage('UNIT TEST') {
            steps {
                sh 'mvn test'
            }
        }
        stage('Checkstyle Analysis') {
            steps {
                sh 'mvn checkstyle:checkstyle'
            }
        }
        stage("Sonar Code Analysis") {
            environment {
                scannerHome = tool 'sonar6.2'
            }
            steps {
                withSonarQubeEnv('sonarserver') {
                    sh '''${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=vprofile \
                        -Dsonar.projectName=vprofile \
                        -Dsonar.projectVersion=1.0 \
                        -Dsonar.sources=src/ \
                        -Dsonar.java.binaries=target/test-classes/com/visualpathit/account/controllerTest/ \
                        -Dsonar.junit.reportsPath=target/surefire-reports/ \
                        -Dsonar.jacoco.reportsPath=target/jacoco.exec \
                        -Dsonar.java.checkstyle.reportPaths=target/checkstyle-result.xml'''
                }
            }
        }
        stage("Quality Gate") {
            steps {
                timeout(time: 1, unit: 'HOURS') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
        stage('Build App Image') {
            steps {
                script {
                    dockerImage = docker.build(appRegistry + ":$BUILD_NUMBER", "./Docker-files/app/multistage/")
                }
            }
        }
        stage('Upload App Image') {
            steps {
                script {
                    docker.withRegistry(vprofileRegistry, registryCredential) {
                        dockerImage.push("$BUILD_NUMBER")
                        dockerImage.push('latest')
                    }
                }
            }
        }
    }
}
```

 [\[175. PAAC_..._DockerECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.%20PAAC_CI_DockerECR.txt)

***

### How It All Connects — The Complete CI Flow

    Jenkins Pipeline starts
        → Fetches code from GitHub (branch: docker)
        → Builds .war artifact with Maven
        → Runs Unit Tests
        → Runs Checkstyle Analysis
        → Sonar Scanner uploads results to SonarQube
        → Quality Gate: waits for SonarQube verdict
            → If FAIL → pipeline aborts
            → If PASS → continues
        → Builds Docker image (Tomcat + .war) using Dockerfile from source code
        → Pushes Docker image to Amazon ECR (tagged with build number + latest)
        → Pipeline complete: versioned Docker image stored in cloud registry

The key evolution is that the **artifact is no longer a raw file** — it's a **fully packaged, runnable Docker image**. This image can be pulled by any deployment system (ECS, EKS, plain Docker hosts) and run immediately without any additional setup. The pipeline has transformed from "build and store code" to "build and store a deployable unit." [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt), [\[175. PAAC_..._DockerECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.%20PAAC_CI_DockerECR.txt)

> ⚠️ **Expert Note (Optional)**
>
> The instructor emphasizes watching this video **twice** before proceeding — once to understand the pipeline code, and once to understand the prerequisite steps. He also recommends downloading the pipeline script from the resource section, reading the Docker Pipeline plugin documentation, and doing some independent research before executing the steps in the next lecture. This is sound advice — understanding the "why" before the "how" prevents blind copy-pasting and builds real engineering intuition. [\[175.-Docke...ereqs-info \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/175.-Docker-PAAC-Prereqs-info.txt)

***

Want me to save this as a downloadable Markdown file? 📄
