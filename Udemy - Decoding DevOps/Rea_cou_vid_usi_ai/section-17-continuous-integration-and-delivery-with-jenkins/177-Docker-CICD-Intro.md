# Docker CI/CD Introduction — Extending Continuous Integration to Continuous Delivery with Amazon ECS

> **Source**: [177.-Docker-CICD-Intro.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/177.-Docker-CICD-Intro.txt?EntityRepresentationId=371d52fe-a7ce-4352-971a-a76d45535dcc) (caption transcript) + Architectural diagram (177. JenkinsCICDECS.png) [\[177.-Docke...CICD-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/177.-Docker-CICD-Intro.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1. The Starting Point — Recap of the Existing CI Pipeline

Before introducing anything new, the instructor grounds the discussion in **what already exists**. The continuous integration (CI) pipeline built across previous lectures follows this flow: [\[177.-Docke...CICD-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/177.-Docker-CICD-Intro.txt)

**Developer commits code → GitHub → Jenkins fetches code → Run tests → Code analysis → Upload results to SonarQube → Check Quality Gate → Publish Docker image to Amazon ECR**

The architectural diagram shown in the video (and uploaded as the reference image) illustrates this CI pipeline visually. It shows:

*   A **Developer** committing code via Git to a **GitHub** repository (the Git repository at the top).
*   **Jenkins** orchestrating the pipeline, with stages flowing left to right: **Fetch Code** (using Git plugin) → **Build** (using Maven) → **Unit Test** (using Maven) → **Code Analysis** (using SonarQube, with a Quality Gate check) → **Upload Artifact** (to Nexus OSS / artifact storage).
*   External services: **SonarQube** receives analysis results and enforces the Quality Gate; **NexusOSS (Sonatype)** stores the versioned artifact.

This is the CI portion — everything up to and including publishing the artifact (in this case, a Docker image to Amazon ECR). The pipeline ensures that every code change is automatically built, tested, analyzed for quality, and if it passes all checks, the resulting Docker image is published to a registry. [\[177.-Docke...CICD-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/177.-Docker-CICD-Intro.txt)

The key point the instructor is making: **this CI pipeline is already complete.** What's missing is the **delivery** — actually deploying and hosting that Docker image so it runs as a live application. This is where the lecture pivots.

***

## 2. Extending CI to CD — The Conceptual Shift

The instructor frames this lecture around a single, clear idea: **we are going to extend our continuous integration pipeline to continuous delivery.** [\[177.-Docke...CICD-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/177.-Docker-CICD-Intro.txt)

**Continuous Integration (CI)** ends at publishing the artifact — the Docker image is built, tested, scanned, and pushed to Amazon ECR (Elastic Container Registry). At this point, the image exists in a registry but is not running anywhere.

**Continuous Delivery (CD)** picks up where CI ends. It takes that published Docker image and **deploys it to a hosting platform** where it actually runs as a live, accessible application. The instructor describes this as adding "the next stage, the next command" — Amazon ECS will **fetch the latest Docker image** from ECR and **host it**. [\[177.-Docke...CICD-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/177.-Docker-CICD-Intro.txt)

The extended pipeline flow becomes:

**Developer commits → GitHub → Jenkins (fetch, build, test, analyze, quality gate) → Publish Docker image to ECR → Deploy to Amazon ECS**

This is the complete CI/CD pipeline — from code commit to running application. The instructor is intentional about showing this as a natural, incremental extension: you don't rebuild the pipeline; you add one more stage at the end. [\[177.-Docke...CICD-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/177.-Docker-CICD-Intro.txt)

***

## 3. Docker Hosting Platforms — Where Do Containers Actually Run?

This is the central theoretical discussion of the video. The instructor has established that Docker images have been created (containerized/dockerized the application). The question now is: **where do you host these containers?** [\[177.-Docke...CICD-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/177.-Docker-CICD-Intro.txt)

The instructor presents three categories of Docker hosting, each with different use cases and trade-offs:

***

### 3.1 Direct Docker Engine — The Simplest (and Most Limited) Approach

The most basic way to run a container is to have a **Docker Engine** installed on a machine and run `docker run` with your image name. The Docker Engine pulls the image and starts a container. [\[177.-Docke...CICD-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/177.-Docker-CICD-Intro.txt)

The instructor is very clear about when this is appropriate: **testing and local development only**. He explicitly says: *"You do not want to run containers directly on Docker engine"* for production, and gives specific reasons: [\[177.-Docke...CICD-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/177.-Docker-CICD-Intro.txt)

1.  **Infrastructure management burden** — You need to set up and manage the Docker Engine yourself, and also manage the underlying platform where it runs (an EC2 instance, a virtual machine, or a physical server). You're responsible for OS patching, networking, storage, monitoring — everything.

2.  **No production-grade features** — A standalone Docker Engine does not provide **high availability** (if the engine crashes, your container is gone), **self-healing** (if a container dies, nothing automatically restarts it), or the many other features that production workloads require (load balancing, rolling updates, service discovery, secrets management, etc.). [\[177.-Docke...CICD-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/177.-Docker-CICD-Intro.txt)

The instructor's framing is deliberate: `docker run` on a Docker Engine is a **development tool**, not a **production deployment strategy**.

***

### 3.2 Kubernetes — The Production Standard (Covered Later)

For production workloads, the instructor identifies **Kubernetes** as the primary solution. Kubernetes is a container orchestration platform that provides all the features Docker Engine lacks — high availability, self-healing, scaling, rolling deployments, and much more. [\[177.-Docke...CICD-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/177.-Docker-CICD-Intro.txt)

The instructor explicitly says Kubernetes will be covered **in depth in a later section** of the course. He lists multiple Kubernetes solutions to show the breadth of the ecosystem: [\[177.-Docke...CICD-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/177.-Docker-CICD-Intro.txt)

*   **Standalone Kubernetes** — Self-managed, you install and maintain the Kubernetes cluster yourself.
*   **Amazon EKS (Elastic Kubernetes Service)** — AWS's managed Kubernetes offering.
*   **AKS (Azure Kubernetes Service)** — Microsoft Azure's managed Kubernetes.
*   **GKE (Google Kubernetes Engine)** — Google Cloud's managed Kubernetes.
*   **OpenShift** — Red Hat's enterprise Kubernetes platform.

The instructor notes: *"There are many Kubernetes solutions out there and we are going to talk about all those things in later lectures."* The purpose of mentioning them here is to establish that Kubernetes is the eventual destination, but for the current stage of the course, a simpler platform will be used. [\[177.-Docke...CICD-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/177.-Docker-CICD-Intro.txt)

> 🔍 **Deep Dive (Optional)**
>
> The reason the instructor defers Kubernetes is pedagogical — Kubernetes has a significant learning curve (cluster setup, manifests, pods, services, ingress, namespaces, RBAC, etc.). By using Amazon ECS first, students can experience container deployment in a CI/CD pipeline without the complexity overhead of Kubernetes. Once the CI/CD concepts are solid, the Kubernetes section can focus on orchestration-specific topics without conflating them with pipeline mechanics.

***

### 3.3 Amazon ECS (Elastic Container Service) — The Practical Choice for Now

The instructor selects **Amazon ECS** as the hosting platform for this phase of the course. ECS is described as a **container hosting platform** — it takes Docker images and runs them as containers in a managed, scalable, secure environment. [\[177.-Docke...CICD-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/177.-Docker-CICD-Intro.txt)

The instructor references the AWS documentation, which describes ECS as a service to *"run highly secure, reliable, scalable containers."* He positions ECS as *"the most quick and easy way to run containers reliably or securely"* with the ability to scale. [\[177.-Docke...CICD-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/177.-Docker-CICD-Intro.txt)

A key aspect the instructor highlights from the documentation: ECS allows you to *"launch thousands of containers across the cloud using preferred CD and automation tools."* This directly connects to what the pipeline is doing — Jenkins (the automation tool) will instruct ECS to deploy the Docker image as part of the CD pipeline. [\[177.-Docke...CICD-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/177.-Docker-CICD-Intro.txt)

The flow is: Jenkins publishes the Docker image to **Amazon ECR** (the registry) → Jenkins triggers deployment → **Amazon ECS** fetches the latest image from ECR and hosts the container. [\[177.-Docke...CICD-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/177.-Docker-CICD-Intro.txt)

> 🔍 **Deep Dive (Optional)**
>
> Amazon ECS operates with two launch types, though the instructor doesn't go into this detail in this introductory lecture:
>
> *   **EC2 launch type** — Containers run on EC2 instances that you manage (you choose instance types, handle capacity).
> *   **Fargate launch type** — Fully serverless; AWS manages the underlying infrastructure entirely. You just specify CPU/memory requirements and ECS handles everything else.
>
> ECS uses the concept of **Task Definitions** (blueprints for your container — image, CPU, memory, ports, environment variables) and **Services** (which ensure a desired number of tasks are running and handle load balancing). These concepts will likely be covered in the next lecture when the instructor discusses prerequisites.

***

## 4. The Relationship Between ECR and ECS

Though the instructor doesn't dedicate a formal explanation to this, the relationship is implied clearly throughout the lecture and is fundamental to understanding the architecture: [\[177.-Docke...CICD-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/177.-Docker-CICD-Intro.txt)

*   **Amazon ECR (Elastic Container Registry)** is where Docker images are **stored** after being built and pushed by the CI pipeline. It is a Docker image registry — analogous to Docker Hub, but private and managed by AWS.
*   **Amazon ECS (Elastic Container Service)** is where Docker containers are **run**. It pulls images from a registry (in this case, ECR) and runs them as live containers.

The CI pipeline pushes to ECR. The CD pipeline tells ECS to pull from ECR and deploy. ECR is the storage; ECS is the runtime. [\[177.-Docke...CICD-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/177.-Docker-CICD-Intro.txt)

***

## 5. What's Coming Next — Pipeline Code and Prerequisites

The instructor closes by previewing the next lecture. He says the pipeline code to deploy to ECS is **"pretty simple, just one more stage we are going to add"** — reinforcing the incremental nature of extending CI to CD. [\[177.-Docke...CICD-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/177.-Docker-CICD-Intro.txt)

He also mentions **prerequisites** — things that need to be set up in AWS (ECS cluster, task definitions, services, IAM roles, etc.) before the pipeline stage can work. These will be covered in the next lecture. [\[177.-Docke...CICD-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/177.-Docker-CICD-Intro.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

This lecture is **entirely conceptual and introductory** — there are no commands, no hands-on steps, and no pipeline code written. The instructor is setting the stage for the next lecture where the actual implementation happens. [\[177.-Docke...CICD-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/177.-Docker-CICD-Intro.txt)

What is being planned:

*   **Goal**: Extend the existing CI pipeline (which ends at publishing a Docker image to Amazon ECR) to a full **CI/CD pipeline** that also deploys the Docker container to **Amazon ECS**.
*   **Why it matters**: A Docker image sitting in a registry is not useful until it's running. Real-world systems need automated deployment — every successful CI build should result in the application being live (or at least staged for release). This eliminates manual deployment, reduces human error, and enables rapid iteration.
*   **What the final outcome looks like**: After the pipeline runs, the application is not only built, tested, and analyzed — it is also **live and running** on Amazon ECS, accessible as a deployed service. [\[177.-Docke...CICD-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/177.-Docker-CICD-Intro.txt)

***

## The Architectural Flow (Mapped to the Diagram)

The uploaded architectural diagram shows the CI portion of the pipeline in detail. Here is how each component maps to the pipeline stages: [\[177.-Docke...CICD-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/177.-Docker-CICD-Intro.txt)

### Existing CI Pipeline (Shown in the Diagram):

1.  **Developer** commits code using Git → pushed to **GitHub** (the Git repository shown at the top of the diagram).

2.  **Jenkins** detects the change and begins the pipeline. The blue box in the diagram represents the Jenkins pipeline, containing all stages:

    *   **Fetch Code** (Git plugin) — Jenkins clones the repository from GitHub. The Git logo is shown inside this stage box.
    *   **Build** (Maven) — Jenkins compiles and packages the application. The Maven logo appears in this stage.
    *   **Unit Test** (Maven) — Jenkins runs unit tests. Maven logo again, since `mvn test` is a Maven command.
    *   **Code Analysis** (SonarQube) — Jenkins runs code analysis and sends results to **SonarQube** (shown as an external service above the pipeline, connected by an arrow). The **Quality Gate** (labeled "GATE" in the diagram) checks whether the code meets quality thresholds.
    *   **Upload Artifact** — The final CI stage uploads the artifact. In the diagram, this connects to **NexusOSS (Sonatype)** shown in the top right.

### The CD Extension (Described Verbally, Not in This Diagram):

3.  After the CI stages complete, a new stage **publishes the Docker image to Amazon ECR**.

4.  A further new stage **deploys the container to Amazon ECS**, which fetches the latest image from ECR and hosts it. [\[177.-Docke...CICD-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/177.-Docker-CICD-Intro.txt)

***

## Decisions Made in This Lecture

Even though no commands are executed, the instructor makes several architectural decisions that shape the next lecture's hands-on work: [\[177.-Docke...CICD-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/177.-Docker-CICD-Intro.txt)

### Decision 1: Use ECS, Not Direct Docker Engine

**Reasoning**: Docker Engine alone lacks high availability, self-healing, and requires managing the underlying infrastructure. Not suitable for production or production-like deployment pipelines. [\[177.-Docke...CICD-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/177.-Docker-CICD-Intro.txt)

### Decision 2: Use ECS, Not Kubernetes (For Now)

**Reasoning**: Kubernetes is the production standard but has significant complexity. ECS provides a quick, reliable, scalable way to host containers without the Kubernetes learning curve. Kubernetes will be covered in depth later. [\[177.-Docke...CICD-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/177.-Docker-CICD-Intro.txt)

### Decision 3: The Pipeline Extension is "Just One More Stage"

**Reasoning**: The CI pipeline is already complete. Deploying to ECS is a natural, incremental addition — one more stage in the Jenkinsfile. This reinforces the power of Pipeline as Code: extending functionality is adding code, not rebuilding infrastructure. [\[177.-Docke...CICD-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/177.-Docker-CICD-Intro.txt)

***

## What Needs to Be Done Before the Next Lecture (Prerequisites Mentioned)

The instructor says there are **prerequisites** that need to be fulfilled before deploying Docker images to ECS. While he doesn't list them in this lecture (they'll be covered in the next one), based on the context established so far, these will involve: [\[177.-Docke...CICD-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/177.-Docker-CICD-Intro.txt)

*   Setting up an **ECS cluster** in AWS
*   Creating a **task definition** (the blueprint for the container — which image, how much CPU/memory, which ports)
*   Creating an **ECS service** (to manage running instances of the task)
*   Ensuring **IAM roles and permissions** allow Jenkins to interact with ECS
*   Ensuring **network/security group** configuration allows ECS to pull from ECR and expose the application

The instructor explicitly says: *"In the next lecture, we will see the pipeline code in order to do this, which is pretty simple, just one more stage we are going to add, and then the prerequisites that we need to fulfill."* [\[177.-Docke...CICD-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/177.-Docker-CICD-Intro.txt)

***

## Summary of Key Concepts and Their Relationships

| Concept                        | Role in the Pipeline                   | Status                                 |
| ------------------------------ | -------------------------------------- | -------------------------------------- |
| **GitHub**                     | Source code repository; trigger point  | Already set up                         |
| **Jenkins**                    | Pipeline orchestrator; runs all stages | Already set up                         |
| **Maven**                      | Build and test tool                    | Already configured                     |
| **SonarQube**                  | Code quality analysis + Quality Gate   | Already integrated                     |
| **Nexus OSS**                  | Artifact storage (WAR files)           | Already integrated                     |
| **Amazon ECR**                 | Docker image registry (storage)        | Already integrated (previous lectures) |
| **Amazon ECS**                 | Docker container hosting (runtime)     | **New — to be set up next**            |
| **Docker Engine (standalone)** | Local/testing container runtime        | Explicitly ruled out for production    |
| **Kubernetes**                 | Production container orchestration     | Deferred to later section              |

 [\[177.-Docke...CICD-Intro \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/177.-Docker-CICD-Intro.txt)

***

This completes the full reconstruction of the video content. This lecture is a conceptual bridge — it establishes **why** we need a container hosting platform, **what options exist**, and **which one we'll use** (Amazon ECS), setting up the hands-on implementation in the next lecture. Would you like me to save this as a downloadable markdown file?
