# 🎬 CI for Docker — Introduction: Deep Learning Material

**Video Title:** CI for Docker — Intro (Lecture 174)
**Source:** Caption file from DevOps CI/CD pipeline course
**Context:** This is an introductory lecture that sets the stage for building a Docker-based Continuous Integration pipeline. It establishes the conceptual shift from artifact-based CI to image-based CI, maps out the entire pipeline flow, and introduces the registry publishing model before diving into code in subsequent lectures. [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1. The Evolution from Artifact Publishing to Docker Image Publishing

In the previous CI pipeline covered in this course, the end product was a **WAR file** — a traditional Java web application archive. The pipeline would build the code, test it, analyze it, and then publish that WAR file as the final artifact. That approach works, but it has a fundamental limitation: a WAR file is just your application code packaged up. It still needs a properly configured application server (like Tomcat), the right Java runtime, the correct OS-level dependencies, and specific environment settings to actually run. The WAR file alone does not guarantee that the application will behave the same way across different environments. [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

In **this** CI pipeline, the end product changes. Instead of publishing a WAR file, we are publishing a **Docker image**. A Docker image bundles everything — the application artifact (the WAR file), the runtime environment, the OS libraries, the configurations — into a single, self-contained, portable unit. When you publish a Docker image, anyone who pulls it can run it and get exactly the same behavior, regardless of the underlying host machine. This is the core shift: from "here's the code artifact, figure out how to run it" to "here's a fully packaged, ready-to-run image." [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

The instructor explicitly states: "Our previous continuous integration pipeline publishes artifacts, the WAR file. In this continuous integration pipeline, we will be publishing Docker images." This is not just a technical change — it represents a fundamental shift in how software is delivered in modern DevOps. [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

The instructor references the **"Introduction to Containers" section** of the course for the foundational knowledge of how Docker images are built and published. The key message is: we will be doing the **same thing** (building and publishing images), but doing it **through pipeline as code from Jenkins** — meaning it will be fully automated, repeatable, and triggered by code changes. [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

> 🔍 **Deep Dive (Optional)**
>
> The shift from WAR-file CI to Docker-image CI reflects a broader industry trend. In traditional CI, the pipeline produces a deployable artifact and the deployment environment is managed separately (often manually or through configuration management tools like Ansible/Chef). In container-based CI, the pipeline produces a deployable *environment* — the image itself *is* the deployment unit. This eliminates the "works on my machine" problem because the image encapsulates everything needed to run. This is why modern CI/CD pipelines almost universally target container images rather than raw artifacts. [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

***

## 2. The Complete Docker CI Pipeline Flow

The instructor lays out the **entire pipeline flow** from trigger to final output. This is the architectural blueprint for everything that will be built in subsequent lectures. Each stage serves a specific purpose, and the order is deliberate: [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

**Trigger → Code Fetch → Unit Tests → Checkstyle Analysis → SonarQube Analysis → Quality Gate → Docker Build → Docker Publish**

Here is how it works, stage by stage:

**1. Developer makes a code change and pushes to GitHub.** This is the trigger event. In a real CI system, Jenkins is configured (typically via webhooks or polling) to detect changes on a specific branch. The moment new code lands on GitHub, the pipeline activates. [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

**2. Jenkins detects the change and fetches the code.** Jenkins pulls the latest version of the source code from the GitHub repository into its workspace. This is the starting point for all subsequent stages — everything operates on this fetched code. [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

**3. Unit tests are executed.** Jenkins runs the project's unit tests (via `mvn test` for Java/Maven projects, as covered in earlier lectures). This is the first quality checkpoint — if the code doesn't pass its own tests, there is no point proceeding further. [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

**4. Checkstyle code analysis.** The code is scanned for style and convention violations using Checkstyle (via `mvn checkstyle:checkstyle`). This generates an XML report of all violations. [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

**5. SonarQube code analysis.** The SonarQube Scanner scans the source code and collects results from all previous analysis stages (unit test reports, coverage reports, Checkstyle results). All of this is **uploaded to the SonarQube server** for centralized quality visualization. [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

**6. Quality Gate check.** After uploading results, the pipeline **waits** for SonarQube's Quality Gate verdict. The Quality Gate is a set of threshold conditions (e.g., "no critical bugs," "coverage above 80%"). If the code meets all thresholds, the gate passes. If not, it fails and the pipeline stops here. This is a critical gate — it prevents poor-quality code from being packaged into a Docker image. [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

**7. Docker image build.** If and only if the Quality Gate passes, the pipeline proceeds to build a Docker image. This Docker image **contains the artifact** (the WAR file produced during the build). The "build process here" that the instructor refers to is specifically the **Docker build process** — running `docker build` to create an image from a Dockerfile that incorporates the application artifact. [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

**8. Docker image publish to a registry.** The built Docker image is pushed to a **container registry** — a centralized storage service for Docker images. From there, any deployment system (Kubernetes, ECS, Docker Swarm, etc.) can pull the image and run it. [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

The important insight is that stages 1 through 6 are essentially the **same pipeline** we built in previous lectures (the WAR-file CI pipeline). The new addition is stages 7 and 8 — the Docker build and publish steps. The Docker CI pipeline is an **extension** of the existing CI pipeline, not a replacement. [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

***

## 3. Container Registries — Where Docker Images Live

A **container registry** is a storage and distribution service for Docker images. It serves the same purpose for Docker images that a Maven repository (like Nexus) serves for JAR/WAR files, or that an app store serves for mobile applications — it is the central place where built images are stored and from which they are distributed to deployment targets. [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

The instructor lists several registry options: [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

| Registry                                    | Provider        | Notes                                                            |
| ------------------------------------------- | --------------- | ---------------------------------------------------------------- |
| **Amazon ECR** (Elastic Container Registry) | AWS             | Used in this course because the infrastructure is already on AWS |
| **GCR** (Google Container Registry)         | Google Cloud    | Google's equivalent                                              |
| **Azure Container Registry**                | Microsoft Azure | Azure's equivalent                                               |
| **Docker Hub**                              | Docker Inc.     | The public default registry; also offers private repos           |
| **Nexus**                                   | Sonatype        | Self-hosted; can serve as both Maven repo and Docker registry    |

The instructor chooses **Amazon ECR** for this course because the existing infrastructure is already running on AWS. This is a practical decision, not a technical requirement — the pipeline logic for building and tagging Docker images remains **identical** regardless of which registry you use. [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

The **only thing that changes** between registries is the **login process**. Each registry has its own authentication mechanism:

*   ECR uses AWS IAM credentials and a special `aws ecr get-login-password` command
*   Docker Hub uses `docker login` with a username and password/token
*   GCR uses a JSON key file or `gcloud auth configure-docker`
*   Nexus uses `docker login` pointed at your Nexus server URL

Once you are authenticated (logged in), the `docker push` command works the same way for all registries. The instructor emphasizes this point clearly: "Doesn't matter where you publish your image. The only process that we change over here is the login process to your registry service. Otherwise, all of this remains similar." [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

> ⚠️ **Expert Note (Optional)**
>
> In production environments, the choice of registry is influenced by factors beyond just which cloud you're on. ECR integrates natively with ECS and EKS (AWS container orchestration services), so if your deployment target is AWS, ECR gives you seamless IAM-based authentication and lifecycle policies for image cleanup. If you're multi-cloud or want vendor independence, a self-hosted solution like Nexus or Harbor gives you full control. Docker Hub is convenient for open-source projects but has rate limits on pulls for free accounts. The registry choice also affects your CI pipeline's network latency — pushing images to a registry in the same cloud region as your Jenkins server is significantly faster than pushing cross-cloud. [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

***

## 4. Pipeline as Code — Automating the Entire Docker CI Workflow from Jenkins

The instructor states: "We will be doing similar thing, but we will be doing it through pipeline as code from a Jenkins." This phrase — **pipeline as code** — is not incidental. It captures a core DevOps principle that underpins this entire lecture series. [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

Pipeline as code means your entire CI/CD workflow — every stage, every command, every condition, every integration — is defined in a **script file** (a `Jenkinsfile` or pipeline script) that lives alongside your source code, can be version-controlled, reviewed, audited, and reproduced. It is not a series of manual clicks in a UI. It is not a set of tribal knowledge steps that only one person on the team knows. It is **code** — deterministic, repeatable, and transparent. [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

In the context of this video, the instructor is saying: yes, you already know how to build Docker images manually (from the "Introduction to Containers" section). You know how to run `docker build`, `docker tag`, and `docker push` from the command line. But doing it manually defeats the purpose of CI. The entire point is that **every time a developer pushes code**, the pipeline automatically fetches, tests, analyzes, gates, builds, and publishes — with zero human intervention. Jenkins orchestrates all of this through the pipeline script. [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

This is the bridge between the earlier Docker knowledge (manual image building) and what comes next (automated image building triggered by code changes via Jenkins pipeline). [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

***

## 5. The Quality Gate as a Gatekeeper Before Docker Build

One subtle but critical point in the pipeline flow is the **position** of the Quality Gate check. The instructor says: "Wait for the quality gate. If everything is good, **then** we are going to build a Docker image." [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

This ordering is deliberate and important. The Quality Gate sits between the code analysis stages and the Docker build stage, acting as a **hard stop**. If the code quality does not meet the defined thresholds on SonarQube (too many bugs, too many vulnerabilities, insufficient test coverage, etc.), the pipeline halts and the Docker image is **never built**. [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

Why does this matter? Because a Docker image is a **distributable, deployable artifact**. Once it exists in a registry, someone (or some automated system) can pull it and run it. If you allow a Docker image to be built from code that fails quality checks, you now have a potentially broken or insecure image sitting in your registry, ready to be deployed. The Quality Gate prevents this by ensuring that only code that meets your organization's quality standards makes it into an image. [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

> 🔍 **Deep Dive (Optional)**
>
> The Quality Gate mechanism works asynchronously. After the SonarQube Scanner uploads results, SonarQube processes them server-side and evaluates them against the Quality Gate conditions. The Jenkins pipeline uses a `waitForQualityGate()` step (from the SonarQube plugin) that polls the SonarQube server until a verdict is returned. If the verdict is "OK," the pipeline proceeds. If "ERROR," the pipeline fails. This was introduced in the previous lecture and is now integrated into the larger Docker CI pipeline. The instructor covered Quality Gate configuration in detail in an earlier lecture — here it appears as a stage in the complete pipeline architecture. [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

***

## 6. The Docker Build Process — Image Contains the Artifact

The instructor specifically clarifies what the "build process" means in this pipeline: "The build process is the Docker build process where we get the Docker image." He further adds: "That Docker image will contain the artifact." [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

This is an important clarification because there are **two different builds** happening in this pipeline, and conflating them is a common source of confusion:

1.  **Maven Build** (`mvn install`) — This compiles the Java source code and produces the WAR file artifact. This happens early in the pipeline (the Build stage).

2.  **Docker Build** (`docker build`) — This takes the WAR file produced by Maven and packages it into a Docker image along with the runtime environment (e.g., a Tomcat base image, Java runtime, OS libraries). This happens late in the pipeline, after all quality checks pass.

The Docker image is not just the application code — it is the application code **plus** everything needed to run it. The WAR file goes *into* the Docker image during the Docker build step, typically via a `COPY` instruction in the Dockerfile. [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

***

## 7. What the Next Lectures Will Cover — Prerequisites and Pipeline Code

The instructor closes by previewing what comes next: "Let's take a look at the pipeline code, how this can be done, and then we will talk about the prerequisite that we need to do in order to run this pipeline on Jenkins." [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

This tells us two things about the upcoming lectures:

1.  **Pipeline code walkthrough** — The actual Jenkinsfile/pipeline script with Docker build and ECR push stages will be shown and explained.
2.  **Prerequisites setup** — Before the pipeline can work, certain infrastructure and configuration must be in place. This likely includes: setting up an ECR repository on AWS, configuring AWS credentials in Jenkins, installing Docker on the Jenkins server (or agent), installing necessary Jenkins plugins (e.g., Docker Pipeline plugin, AWS credentials plugin), and creating the Dockerfile for the vprofile project.

This lecture is purely an **architectural overview** — no commands are executed, no code is written. It establishes the mental model so that when the actual implementation begins, you already understand where each piece fits. [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are building a **Docker-based Continuous Integration pipeline** in Jenkins that automates the entire journey from a developer's code push to a production-ready Docker image stored in a container registry. [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

**Why it matters:** In modern DevOps, applications are deployed as containers — not as raw WAR/JAR files dropped onto servers. A Docker CI pipeline ensures that every code change automatically goes through quality checks and, if it passes, gets packaged into a standardized, portable Docker image that can be deployed to any container orchestration platform (Kubernetes, ECS, Docker Swarm, etc.). This eliminates manual build steps, ensures consistency, and enforces quality gates before anything becomes deployable. [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

**What the final outcome looks like:** When complete, every push to GitHub will trigger a Jenkins pipeline that:

1.  Fetches the code
2.  Runs unit tests
3.  Runs Checkstyle code analysis
4.  Runs SonarQube analysis and uploads results
5.  Waits for the Quality Gate verdict
6.  Builds a Docker image containing the application artifact
7.  Pushes that Docker image to **Amazon ECR**

The result is a verified, quality-checked Docker image sitting in ECR, ready for deployment. [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

***

## Step 1: Understanding the Starting Point — The Previous CI Pipeline

Before building the Docker CI pipeline, you need to understand what already exists. In the previous lectures, we built a CI pipeline that does the following: fetches code from GitHub, builds the project with Maven (`mvn install -DskipTests`), runs unit tests (`mvn test`), runs Checkstyle analysis (`mvn checkstyle:checkstyle`), scans with SonarQube Scanner (uploading all results to the SonarQube server), and checks the Quality Gate. The final output of that pipeline was the **WAR file** — a Java web application archive stored as a Jenkins build artifact. [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

The Docker CI pipeline **retains all of these stages**. Everything from fetch through Quality Gate remains unchanged. What changes is what happens **after** the Quality Gate passes — instead of stopping at the WAR file, we now take that WAR file, package it into a Docker image, and push the image to a registry. [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

This is a critical design insight: **the Docker CI pipeline is an extension, not a rewrite.** You are adding stages to an existing, proven pipeline. This means all the configuration from previous lectures (Maven tool, JDK tool, SonarQube server, SonarQube scanner, Quality Gate) must already be in place and working before you attempt the Docker stages. [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

***

## Step 2: Understanding the New Stages — Docker Build and Publish

The two new stages that extend the pipeline are: [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

### Docker Build Stage

This stage runs the `docker build` command. A **Dockerfile** (which must exist in the project repository) contains instructions that:

*   Start from a base image (e.g., a Tomcat image that already has Java and Tomcat installed)
*   Copy the WAR file (produced by the Maven build stage) into the appropriate directory inside the image
*   Configure any necessary settings

The output of this stage is a **Docker image** — a self-contained, runnable package that includes the application and its entire runtime environment. The instructor emphasizes that "that Docker image will contain the artifact" — meaning the WAR file is embedded inside the image. [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

### Docker Publish Stage

This stage pushes the built Docker image to a **container registry**. In this course, the registry is **Amazon ECR** (Elastic Container Registry). The process involves:

1.  **Authenticating** (logging in) to the registry
2.  **Tagging** the image with the registry URL
3.  **Pushing** the image using `docker push`

The instructor makes a key point here: the **only thing that changes** between different registries (ECR, GCR, Azure, Docker Hub, Nexus) is the **login process**. The build and push commands remain essentially the same. This means the skills you learn here transfer directly to any other registry. [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

***

## Step 3: Choosing the Container Registry — Amazon ECR

The instructor selects **Amazon ECR** as the target registry for one practical reason: "we're using AWS already." The existing Jenkins server, SonarQube server, and other infrastructure are already running on AWS, so using ECR keeps everything within the same ecosystem. [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

The alternatives listed are: [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

*   **Google Container Registry (GCR)** — if your infrastructure is on Google Cloud
*   **Azure Container Registry** — if your infrastructure is on Azure
*   **Docker Hub** — the default public registry, also supports private repositories
*   **Nexus** — a self-hosted option that can function as both a Maven repository and a Docker registry

The choice of registry does **not** affect the pipeline structure. It only affects the authentication step. Once authenticated, `docker push` works identically regardless of destination. [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

> ⚠️ **Expert Note (Optional)**
>
> When setting up ECR in practice, you will need to: create an ECR repository (via AWS Console or CLI), configure IAM permissions so Jenkins can authenticate and push images, and install the AWS CLI on the Jenkins server (or agent) so the `aws ecr get-login-password` command is available. These prerequisites are what the instructor refers to when he says "we will talk about the prerequisite that we need to do in order to run this pipeline on Jenkins." These setup steps will be covered in the next lectures. [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

***

## Step 4: Preparing for the Next Lectures

This lecture is an **architecture and planning** lecture — no commands are executed, no pipelines are created. Its purpose is to give you the complete mental model of what the Docker CI pipeline looks like end-to-end before you start building it. [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

Before proceeding to the next lectures, verify that you have the following from previous lectures already working:

*   ✅ Jenkins server running and accessible
*   ✅ Maven and JDK tools configured in Jenkins
*   ✅ SonarQube server running and accessible
*   ✅ SonarQube Scanner tool installed in Jenkins
*   ✅ SonarQube server configured in Jenkins (Manage Jenkins → System)
*   ✅ Quality Gate configured on SonarQube
*   ✅ A working CI pipeline that successfully fetches, builds, tests, analyzes, and passes the Quality Gate
*   ✅ Familiarity with Docker concepts (from the "Introduction to Containers" section the instructor references)

The next lectures will cover: the **actual pipeline code** (the Jenkinsfile with Docker build and ECR push stages) and the **prerequisites** (ECR setup, AWS credentials in Jenkins, Docker installation on Jenkins server, etc.). [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)

***

## 🔗 How This Lecture Connects to the Overall Learning Path

    Previous Lectures                    This Lecture (174)              Next Lectures
    ─────────────────                    ──────────────────              ─────────────
                                                                        
    WAR-file CI Pipeline          →      Architecture Overview    →     Pipeline Code +
    (fetch → build → test →              (what changes, what             Prerequisites Setup
     checkstyle → sonar →                 stays, which registry,         (ECR, credentials,
     quality gate → publish WAR)          full pipeline flow)            Dockerfile, Jenkinsfile)
                                                                        
    Introduction to Containers    →      "We will do the same    →     Automated Docker build
    (manual docker build,                 thing, but through             and push via Jenkins
     docker push, Dockerfile)             pipeline as code"              pipeline script

The key takeaway from this lecture is: **you already know all the individual pieces** — CI pipelines, Docker image building, container registries. This lecture shows you how they **connect together** into a single automated flow. The next lectures will show you the exact code and configuration to make it work. [\[174.-CI-fo...er---Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/174.-CI-for-Docker---Intro.txt)
