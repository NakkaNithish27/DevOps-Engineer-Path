# 🎬 Docker CI/CD Demonstration — Deploying to ECS: Deep Learning Material

**Video Title:** Docker CI/CD Demonstration (Lecture 180)
**Source:** Caption file and pipeline resource from DevOps CI/CD course
**Resource File:** [180. PAAC\_CICD\_ECS\_ECR.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.%20PAAC_CICD_ECS_ECR.txt?EntityRepresentationId=73f085e8-9820-4534-85a0-9ad70d7a2470)

This video is the culmination of the Docker CI/CD section. It walks through the **complete end-to-end pipeline** — from code fetch through quality checks, Docker image build, ECR publish, all the way to **deploying the container on Amazon ECS**. It covers the final deployment stage configuration, a new Jenkins plugin installation, a live pipeline execution, verification on ECS, and a critical discussion about better deployment strategies (task definition versioning vs. force-new-deployment). The instructor also positions ECS vs. Kubernetes in the broader DevOps landscape. [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt), [\[180. PAAC_...CD_ECS_ECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.%20PAAC_CICD_ECS_ECR.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1. The Complete CI/CD Pipeline — From Code to Running Container

This video presents the **fully assembled pipeline** that represents the culmination of everything built across previous lectures. It is not just a CI pipeline anymore — it is a full **CI/CD pipeline** that takes code from a developer's push all the way to a running container in production (or staging). [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt)

The pipeline stages, in order, are: [\[180. PAAC_...CD_ECS_ECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.%20PAAC_CICD_ECS_ECR.txt)

1.  **Fetch code** — Pull source code from GitHub (`docker` branch)
2.  **Build** — Compile with Maven, archive the WAR file
3.  **Unit Test** — Run unit tests with Maven
4.  **Checkstyle Analysis** — Static code style analysis
5.  **Sonar Code analysis** — Push all analysis results to SonarQube server
6.  **Quality Gate** — Wait for SonarQube's pass/fail verdict; abort if failed
7.  **Publish to Nexus** — Upload the WAR artifact to Nexus repository
8.  **Build App Image** — Build a Docker image containing the application
9.  **Upload App Image** — Push the Docker image to Amazon ECR
10. **Deploy to ECS** — Force the ECS service to pull and run the new image

Stages 1–6 are the **CI (Continuous Integration)** portion — they verify code quality. Stage 7 archives the artifact. Stages 8–9 are the **containerization** portion — they package the verified code into a Docker image. Stage 10 is the **CD (Continuous Deployment)** portion — it deploys the new container to a running service. This is the first time in this course that the pipeline extends all the way to actual deployment. [\[180. PAAC_...CD_ECS_ECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.%20PAAC_CICD_ECS_ECR.txt), [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt)

***

## 2. Amazon ECS — Elastic Container Service

Amazon ECS (Elastic Container Service) is AWS's **container orchestration service**. It manages the lifecycle of Docker containers — starting them, stopping them, scaling them, load-balancing them, and ensuring they stay healthy. When you deploy a container to ECS, you don't manually run `docker run` on a server. Instead, you tell ECS "run this image" and ECS handles everything: pulling the image from the registry, starting the container on available compute resources, routing traffic to it, and restarting it if it crashes. [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt)

In this pipeline, ECS is configured with two key identifiers: [\[180. PAAC_...CD_ECS_ECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.%20PAAC_CICD_ECS_ECR.txt), [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt)

*   **Cluster name: `vprofile`** — An ECS cluster is a logical grouping of compute resources (EC2 instances or Fargate capacity) where your containers run. Think of it as the "environment" or "pool of machines" dedicated to running your application's containers.

*   **Service name: `vproappservice`** — An ECS service is a long-running configuration that ensures a specified number of container instances (tasks) are always running. If a container dies, the service automatically launches a replacement. The service also handles integration with load balancers and manages deployments.

The instructor stores both values in the pipeline's global `environment` block, making them available to the deployment stage. [\[180. PAAC_...CD_ECS_ECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.%20PAAC_CICD_ECS_ECR.txt)

> 🔍 **Deep Dive (Optional)**
>
> ECS has a hierarchy: **Cluster → Service → Task → Container**. A **Task Definition** is a blueprint that describes which Docker image to use, how much CPU/memory to allocate, which ports to expose, and what environment variables to set. A **Task** is a running instance of that blueprint. A **Service** manages one or more tasks and ensures the desired count is maintained. The deployment approach in this video (`--force-new-deployment`) tells the service to stop existing tasks and start new ones using the *same* task definition — which means the service pulls the `latest` tagged image from ECR. A more robust approach (discussed later in the video) involves creating a *new* task definition revision with the updated image tag. [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt)

***

## 3. The `aws ecs update-service --force-new-deployment` Command

This is the core deployment mechanism used in the pipeline. The command: [\[180. PAAC_...CD_ECS_ECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.%20PAAC_CICD_ECS_ECR.txt), [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt)

```bash
aws ecs update-service --cluster ${cluster} --service ${service} --force-new-deployment
```

tells AWS ECS to **force a new deployment** of the specified service within the specified cluster. What "force a new deployment" means is: ECS will stop the currently running tasks (containers) and launch new ones using the current task definition. Since the pipeline has just pushed a new Docker image tagged as `latest` to ECR, the new tasks will pull this updated image. [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt)

The instructor describes what happens during deployment by checking the ECS console: the service **stops 1 running task**, **deregisters 1 target from the target group** (the load balancer stops sending traffic to the old container), **begins draining the connection** (allows existing in-flight requests to complete), and then the **new deployment completes** and reaches a **steady state** (the new container is running and receiving traffic). [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt)

The instructor explicitly acknowledges this is a **simple deployment approach**. He calls it "pretty simple" — we are "just forcing the container to fetch a new service, forcing the service, ECS service to fetch a new container." It works, but it has limitations that he discusses immediately afterward. [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt)

***

## 4. Better ECS Deployment Strategy — Task Definition Versioning

After demonstrating the force-new-deployment approach, the instructor consults **ChatGPT** for better ECS deployment practices. The AI responds that while the pipeline is "already quite solid," the deployment strategy can be improved. [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt)

The recommended **best practice** is: instead of forcing a new deployment with the same task definition, **register a new task definition** with the updated image tag, then update the service to use this new task definition revision. [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt)

The improved approach works like this: [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt)

1.  Take the existing `taskdef.json` file (the task definition template)
2.  **Search and replace** the image URI inside it with the new image tag (e.g., the current build number)
3.  Create a new JSON file with the updated image reference
4.  **Register** this new task definition with ECS using `aws ecs register-task-definition`
5.  **Update the service** using `aws ecs update-service` but specifying the **new task definition** instead of using `--force-new-deployment`

This is better because each deployment now has a **distinct, versioned task definition**. You can see exactly which image version each deployment used, roll back to a previous version by pointing the service to an older task definition revision, and maintain a clear audit trail of what was deployed and when. With `--force-new-deployment`, you lose this traceability because the task definition itself never changes — it always points to `latest`, and "latest" is a moving target. [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt)

The instructor leaves this as an **exercise** for the viewer: "Try to do this. See what problems or issues you get and try to fix it." [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt)

> ⚠️ **Expert Note (Optional)**
>
> The `--force-new-deployment` approach has another subtle issue: it relies on the `latest` tag. If the ECR image tagged `latest` hasn't actually changed (e.g., the push failed silently or cached), the "new deployment" will deploy the same old image. With task definition versioning, you use the explicit build number as the image tag (e.g., `:42`), so there is no ambiguity about which image is being deployed. This is why production pipelines almost always use explicit, immutable image tags rather than `latest`. [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt)

***

## 5. The `withAWS` Plugin — AWS Steps for Jenkins

The deployment stage uses a Jenkins pipeline step called `withAWS`, which comes from the **AWS Steps plugin**. This plugin must be installed separately — it is not part of Jenkins by default. [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt), [\[180. PAAC_...CD_ECS_ECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.%20PAAC_CICD_ECS_ECR.txt)

```groovy
withAWS(credentials: 'awscreds', region: 'us-east-1') {
    sh 'aws ecs update-service --cluster ${cluster} --service ${service} --force-new-deployment'
}
```

What `withAWS` does is: before executing the shell command inside its block, it **exports** the AWS credentials (access key and secret key stored in Jenkins under the credential ID `awscreds`) and the specified region (`us-east-1`) as environment variables. This means the `aws` CLI command inside the block automatically has the authentication context it needs to communicate with AWS APIs. Without this wrapper, the `aws ecs update-service` command would fail with an authentication error because it wouldn't know which AWS account to target or have permission to do so. [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt), [\[180. PAAC_...CD_ECS_ECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.%20PAAC_CICD_ECS_ECR.txt)

The instructor emphasizes two things to verify: [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt)

*   **`awscreds` must already be saved** in Jenkins credentials (from a previous setup step)
*   **The region must be correct** — his is `us-east-1`, but yours may differ

***

## 6. ECS vs. Kubernetes — Where Each Fits

The instructor provides important context about when to use ECS versus Kubernetes. He states: "I'm not saying ECS is not for production, but if you have many, many containers running where all the application runs on container infrastructure, then Kubernetes is the best option." [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt)

ECS is suitable for simpler container deployments, especially when you are already in the AWS ecosystem and want a managed service without the operational overhead of running a Kubernetes cluster. Kubernetes, on the other hand, is the industry standard for large-scale container orchestration — it provides more flexibility, is cloud-agnostic, and has a richer ecosystem of tools for managing complex microservice architectures. [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt)

The instructor explicitly frames this section's scope: "The focus of this section was to train you on CI/CD and not on containers and Kubernetes. So I kept deployment here simple by using ECS." Better container deployment patterns using Kubernetes will be covered in later lectures. [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt)

***

## 7. Global Environment Variables in Declarative Pipeline

The pipeline script in this video introduces **global environment variables** for the first time in this course's pipeline evolution. In previous lectures, we saw stage-level environment variables (like `scannerHome` inside the Sonar Code analysis stage). Now, the pipeline declares variables at the **pipeline level** — before the `stages` block — making them accessible to **all stages**. [\[180. PAAC_...CD_ECS_ECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.%20PAAC_CICD_ECS_ECR.txt)

```groovy
environment {
    registryCredential = 'ecr:us-east-1:awscreds'
    appRegistry = "980088651931.dkr.ecr.us-east-1.amazonaws.com/vprofileappimg"
    vprofileRegistry = "https://980088651931.dkr.ecr.us-east-1.amazonaws.com"
    cluster = "vprofile"
    service = "vproappservice"
}
```

 [\[180. PAAC_...CD_ECS_ECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.%20PAAC_CICD_ECS_ECR.txt)

Each variable serves a specific purpose:

*   **`registryCredential`** — A composite credential string in the format `ecr:<region>:<jenkins-credential-id>`. This is used by the Docker Pipeline plugin's `docker.withRegistry()` method to authenticate with ECR. The `ecr:` prefix tells the plugin to use ECR-specific authentication (which involves generating a temporary token via AWS IAM). `us-east-1` is the AWS region, and `awscreds` is the Jenkins credential ID storing the AWS access key and secret key.

*   **`appRegistry`** — The full ECR repository URI including the image name (`vprofileappimg`). This is used in the `docker.build()` command to tag the image with the correct registry path so it can be pushed to the right ECR repository.

*   **`vprofileRegistry`** — The ECR registry URL (with `https://` prefix). This is used by `docker.withRegistry()` to know *where* to push the image. Note it does not include the image name — it's just the registry endpoint.

*   **`cluster`** — The ECS cluster name (`vprofile`), used in the deployment command.

*   **`service`** — The ECS service name (`vproappservice`), used in the deployment command.

 [\[180. PAAC_...CD_ECS_ECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.%20PAAC_CICD_ECS_ECR.txt), [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt)

By placing these in the global `environment` block, any stage can reference them using `${variable_name}` syntax. This is cleaner than hardcoding values inside individual stages and makes the pipeline easier to maintain — if the registry URL or cluster name changes, you update it in one place. [\[180. PAAC_...CD_ECS_ECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.%20PAAC_CICD_ECS_ECR.txt)

***

## 8. Docker Image Build via Jenkins Pipeline DSL

The pipeline uses Jenkins' **Docker Pipeline plugin** to build images, rather than raw `docker build` shell commands. The stage: [\[180. PAAC_...CD_ECS_ECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.%20PAAC_CICD_ECS_ECR.txt)

```groovy
stage('Build App Image') {
    steps {
        script {
            dockerImage = docker.build( appRegistry + ":$BUILD_NUMBER", "./Docker-files/app/multistage/")
        }
    }
}
```

The `docker.build()` method is a Pipeline DSL (Domain Specific Language) function provided by the Docker Pipeline plugin. It takes two arguments: [\[180. PAAC_...CD_ECS_ECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.%20PAAC_CICD_ECS_ECR.txt)

1.  **Image name with tag**: `appRegistry + ":$BUILD_NUMBER"` — This resolves to something like `980088651931.dkr.ecr.us-east-1.amazonaws.com/vprofileappimg:42` (where 42 is the Jenkins build number). Tagging with the build number gives each image a **unique, traceable tag** tied to the specific Jenkins build that created it.

2.  **Dockerfile path**: `"./Docker-files/app/multistage/"` — This tells Docker where to find the Dockerfile and the build context. The Dockerfile is located inside the `Docker-files/app/multistage/` directory of the fetched source code repository (the `docker` branch).

The return value `dockerImage` is a **Docker image object** that the pipeline stores for use in the next stage (the upload/push stage). This is why it's wrapped in a `script { }` block — assigning a return value to a variable is Groovy scripting that requires the script context in a Declarative Pipeline. [\[180. PAAC_...CD_ECS_ECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.%20PAAC_CICD_ECS_ECR.txt)

> 🔍 **Deep Dive (Optional)**
>
> The Dockerfile path mentions "multistage" — this implies a **multi-stage Docker build**. In a multi-stage Dockerfile, you have multiple `FROM` instructions. The first stage might use a build image (e.g., with Maven and JDK) to compile the code, and the second stage uses a lightweight runtime image (e.g., Tomcat) and copies only the final artifact from the first stage. This produces a smaller, cleaner production image. The pipeline's Maven build stage has already compiled the WAR file, so the Dockerfile likely copies the pre-built WAR into the runtime image. The "multistage" directory name suggests the Dockerfile supports both approaches. [\[180. PAAC_...CD_ECS_ECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.%20PAAC_CICD_ECS_ECR.txt)

***

## 9. Docker Image Push via Jenkins Pipeline DSL

The upload stage pushes the built image to ECR: [\[180. PAAC_...CD_ECS_ECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.%20PAAC_CICD_ECS_ECR.txt)

```groovy
stage('Upload App Image') {
    steps {
        script {
            docker.withRegistry( vprofileRegistry, registryCredential ) {
                dockerImage.push("$BUILD_NUMBER")
                dockerImage.push('latest')
            }
        }
    }
}
```

`docker.withRegistry()` takes two arguments: the registry URL (`vprofileRegistry` = `https://980088651931.dkr.ecr.us-east-1.amazonaws.com`) and the credential ID (`registryCredential` = `ecr:us-east-1:awscreds`). This method authenticates with the registry before executing any commands inside its block. [\[180. PAAC_...CD_ECS_ECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.%20PAAC_CICD_ECS_ECR.txt)

Inside the block, the image is pushed **twice** with two different tags:

*   `dockerImage.push("$BUILD_NUMBER")` — Pushes with the explicit build number tag (e.g., `:42`). This creates an **immutable, traceable** reference to this specific build.
*   `dockerImage.push('latest')` — Pushes with the `latest` tag, overwriting whatever was previously tagged as `latest`. This provides a **convenience pointer** that always references the most recent build.

The dual-push strategy gives you both traceability (build number) and convenience (latest). The deployment stage uses `latest` via `--force-new-deployment`, but a more robust deployment would reference the explicit build number tag. [\[180. PAAC_...CD_ECS_ECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.%20PAAC_CICD_ECS_ECR.txt)

***

## 10. The Nexus Publish Stage — Artifact Archiving

Before the Docker stages, the pipeline includes a **Publish to Nexus** stage that was not present in earlier pipeline iterations: [\[180. PAAC_...CD_ECS_ECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.%20PAAC_CICD_ECS_ECR.txt)

```groovy
stage("Publish to Nexus") {
    steps {
        nexusArtifactUploader(
            nexusVersion: 'nexus3',
            protocol: 'http',
            nexusUrl: '172.31.21.185:8081',
            groupId: 'QA',
            version: "${env.BUILD_ID}-${BUILD_TIMESTAMP}",
            repository: 'vprofile-repo',
            credentialsId: 'nexuslogin',
            artifacts: [
                [ artifactId: 'vproapp',
                  classifier: '',
                  file: 'target/vprofile-v2.war',
                  type: 'war' ]
            ]
        )
    }
}
```

This stage uploads the WAR file to a **Nexus repository** as a versioned artifact. The version string `"${env.BUILD_ID}-${BUILD_TIMESTAMP}"` combines the Jenkins build number with a timestamp, ensuring every upload has a unique version. The `nexusUrl` uses a **private IP** (`172.31.21.185:8081`), meaning the Nexus server is on the same network as Jenkins. [\[180. PAAC_...CD_ECS_ECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.%20PAAC_CICD_ECS_ECR.txt)

This stage exists alongside the Docker stages — the WAR file is both stored in Nexus (as a traditional artifact for archival/rollback purposes) and embedded into the Docker image. These are complementary, not redundant: Nexus preserves the artifact for audit and manual deployment scenarios, while the Docker image is the actual deployment unit. [\[180. PAAC_...CD_ECS_ECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.%20PAAC_CICD_ECS_ECR.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are building and executing the **complete CI/CD pipeline** that takes the vprofile Java application from a GitHub push all the way to a **running container on Amazon ECS**. This is the full pipeline — code fetch, build, test, code analysis, quality gate, artifact archival, Docker image build, ECR push, and ECS deployment — all automated through a single Jenkins pipeline script. [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt), [\[180. PAAC_...CD_ECS_ECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.%20PAAC_CICD_ECS_ECR.txt)

**Why it matters:** In real-world systems, you need a fully automated path from code commit to production deployment. Every manual step is a potential point of failure, delay, and human error. This pipeline ensures that every code change is automatically verified for quality, packaged into a standardized container, and deployed — with zero human intervention after the initial push. [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt)

**What the final outcome looks like:** After the pipeline runs successfully, you will have a new Docker image in ECR and a freshly deployed container running on ECS, serving the updated application. The ECS service will have automatically drained the old container and replaced it with the new one. [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt)

***

## Step 1: Configuring the Cluster and Service Names in the Pipeline Code

The instructor starts with the pipeline script (from the resource file) and configures the two ECS-specific values in the global `environment` block. [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt)

He navigates to the ECS console to find the exact names:

**Cluster name:** `vprofile` — This is the ECS cluster that was set up in a previous prerequisite step. The instructor copies it and places it in the pipeline: [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt), [\[180. PAAC_...CD_ECS_ECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.%20PAAC_CICD_ECS_ECR.txt)

```groovy
cluster = "vprofile"
```

**Service name:** `vproappservice` — This is the ECS service running within the cluster. The instructor copies it and places it in the pipeline: [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt), [\[180. PAAC_...CD_ECS_ECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.%20PAAC_CICD_ECS_ECR.txt)

```groovy
service = "vproappservice"
```

Both values are placed inside the global `environment { }` block at the top of the pipeline, alongside the existing registry variables (`registryCredential`, `appRegistry`, `vprofileRegistry`). This makes them accessible to the deployment stage at the bottom of the pipeline. [\[180. PAAC_...CD_ECS_ECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.%20PAAC_CICD_ECS_ECR.txt)

**Connection to overall system:** These two values are the targeting coordinates for the deployment command. Without them, the `aws ecs update-service` command wouldn't know *which* cluster and *which* service to update. Getting them wrong would either fail the command (if the cluster/service doesn't exist) or deploy to the wrong service (if you have multiple services). [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt)

***

## Step 2: Understanding the Deploy to ECS Stage

The deployment stage in the pipeline code is: [\[180. PAAC_...CD_ECS_ECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.%20PAAC_CICD_ECS_ECR.txt)

```groovy
stage('Deploy to ecs') {
    steps {
        withAWS(credentials: 'awscreds', region: 'us-east-1') {
            sh 'aws ecs update-service --cluster ${cluster} --service ${service} --force-new-deployment'
        }
    }
}
```

Breaking down every part:

*   **`stage('Deploy to ecs')`** — Declares a new pipeline stage named "Deploy to ecs".

*   **`withAWS(credentials: 'awscreds', region: 'us-east-1')`** — This is from the **AWS Steps plugin**. It wraps the enclosed commands with AWS authentication context. `credentials: 'awscreds'` tells Jenkins to look up the stored credential with ID `awscreds` (an AWS access key + secret key pair saved in Jenkins credentials). `region: 'us-east-1'` sets the AWS region. These values are **exported as environment variables** so the `aws` CLI command inside can authenticate with AWS.

*   **`sh 'aws ecs update-service ...'`** — Executes a shell command using the AWS CLI.

*   **`--cluster ${cluster}`** — Specifies the ECS cluster name. `${cluster}` resolves to `vprofile` from the global environment variable.

*   **`--service ${service}`** — Specifies the ECS service name. `${service}` resolves to `vproappservice` from the global environment variable.

*   **`--force-new-deployment`** — Tells ECS to force a new deployment of the service, even if the task definition hasn't changed. This causes ECS to stop the current tasks and start new ones, which will pull the latest image from ECR.

 [\[180. PAAC_...CD_ECS_ECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.%20PAAC_CICD_ECS_ECR.txt), [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt)

The instructor emphasizes: **"Make sure the awscreds are already saved and make sure your region is correct."** If the credentials don't exist in Jenkins or the region is wrong, the deployment will fail. [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt)

***

## Step 3: Installing the AWS Steps Plugin

Before the pipeline can use `withAWS`, the **AWS Steps plugin** must be installed in Jenkins. The instructor walks through this: [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt)

1.  Go to **Jenkins dashboard**
2.  Click **Manage Jenkins**
3.  Click **Plugins**
4.  Go to **Available plugins**
5.  Search for **`aws steps`**
6.  Put a **check mark** next to the plugin
7.  Click **Install**

The instructor explains what this plugin provides: "This plugin gives us this `withAWS` option. So it's going to execute the shell command, but first export all these options." Without this plugin, the `withAWS` step would not exist in the pipeline DSL, and the pipeline would fail at that step with an unrecognized step error. [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt)

**How to verify success:** After installation, the plugin should appear in the "Installed plugins" tab. You may need to restart Jenkins depending on the plugin requirements.

**Common mistake:** Forgetting to install this plugin before running the pipeline. The error would appear at the "Deploy to ecs" stage as an unrecognized pipeline step.

***

## Step 4: Creating and Running the Jenkins Job

The instructor creates a new Jenkins pipeline job: [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt)

1.  Go to Jenkins main page
2.  Click **New Item**
3.  Job name: **`Vprofile-CICD-ECS`**
4.  Select **Pipeline**
5.  Click **OK**
6.  Scroll down to the Pipeline script section
7.  **Paste the complete pipeline code** (all stages from Fetch code through Deploy to ECS)
8.  Click **Save**
9.  Click **Build Now**
10. Go to **Stages** view to monitor progress

The instructor pauses the recording while the pipeline executes (it takes time to run through all 10 stages). [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt)

**Result:** "The entire pipeline got completed successfully." [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt)

***

## Step 5: Verifying the Deployment on ECS

After the pipeline succeeds, the instructor verifies the deployment in two ways: [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt)

### 5a. Checking Jenkins Logs

He clicks on the **Deploy to ecs** stage in the Stages view and examines the logs. The logs show the `aws ecs update-service` command being executed and returning **JSON output** describing the updated service configuration. This JSON is the AWS API response confirming the service update was accepted. [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt)

### 5b. Checking the ECS Console

He navigates to the ECS console: [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt)

1.  Go to the **cluster** (vprofile)
2.  Click on the **service** (vproappservice)
3.  Click on **Deployments** tab
4.  Scroll down to see the deployment events

The deployment events show the following sequence: [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt)

1.  **"Stopped 1 running task"** — ECS terminates the old container
2.  **"Deregistered 1 target in the target-group"** — The old container is removed from the load balancer's target group, so no new traffic is routed to it
3.  **"Began draining the connection"** — ECS waits for any in-flight requests to the old container to complete before fully stopping it (graceful shutdown)
4.  **"New deployment completed"** — The new container (with the updated image) is running
5.  **"Reached steady state"** — The service has stabilized with the desired number of healthy tasks running

This sequence is the standard ECS **rolling deployment** behavior. [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt)

***

## Step 6: Understanding the Limitations and Better Alternatives

After the successful deployment, the instructor discusses **why this approach is simple and what's better**. [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt)

He opens **ChatGPT** and pastes his entire pipeline, asking: "Can you suggest me a better ECS deployment option?" [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt)

ChatGPT responds that the pipeline is "already quite solid" but recommends a **task definition versioning** approach instead of `--force-new-deployment`. The improved strategy, in Groovy pipeline script form, works like this: [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt)

1.  Take a `taskdef.json` template file
2.  Use **search and replace** in the script to update the image URI with the new build's image tag
3.  Write the updated JSON to a new file
4.  **Register** the new task definition with AWS: `aws ecs register-task-definition --cli-input-json file://updated-taskdef.json`
5.  **Update the service** to use the new task definition revision: `aws ecs update-service --cluster <cluster> --service <service> --task-definition <new-task-def-arn>`

The key difference: instead of telling ECS "restart with whatever you have" (`--force-new-deployment`), you are telling ECS "here is a new version of the blueprint, use this one." Each deployment gets its own **versioned task definition**, providing full traceability and easy rollback. [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt)

The instructor leaves this as an **exercise**: "Try to do this. See what problems or issues you get and try to fix it." [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt)

***

## Step 7: Context — Where This Fits in the Larger Learning Path

The instructor provides important framing for how to think about this section going forward: [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt)

*   **ECS is production-capable**, but for large-scale container infrastructure (many containers, many microservices), **Kubernetes is the better option**. Later lectures will cover Kubernetes-based deployments.

*   **The focus of this section was CI/CD, not containers.** The deployment was kept intentionally simple using ECS so the emphasis remains on the pipeline automation — how to go from code push to deployment automatically.

*   **Recommended action:** "Play with this infrastructure, play with the CI/CD pipeline, make changes, do your experiments." The instructor encourages hands-on experimentation before moving on.

*   **Coming next:** Cleanup of the infrastructure, followed by lectures on **build triggers** and other important Jenkins/CI/CD concepts. [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt)

***

## 🔗 Complete Pipeline Architecture Map

    Developer pushes code to GitHub (docker branch)
        │
        ▼
    ┌─────────────────────────────────────────────────────────┐
    │  JENKINS PIPELINE (Vprofile-CICD-ECS)                   │
    │                                                         │
    │  ┌─────────────┐    ┌─────────┐    ┌──────────────┐    │
    │  │ Fetch Code  │───▶│  Build  │───▶│  Unit Test   │    │
    │  │ (git clone) │    │(mvn inst│    │ (mvn test)   │    │
    │  └─────────────┘    │  all)   │    └──────┬───────┘    │
    │                     └─────────┘           │            │
    │                                           ▼            │
    │  ┌──────────────┐    ┌──────────────┐  ┌──────────┐   │
    │  │  Quality     │◀───│ Sonar Code   │◀─│Checkstyle│   │
    │  │  Gate        │    │ Analysis     │  │ Analysis │   │
    │  │ (pass/fail)  │    │ (scanner+    │  │(mvn chk) │   │
    │  └──────┬───────┘    │  upload)     │  └──────────┘   │
    │         │            └──────────────┘                  │
    │         │ PASS                                         │
    │         ▼                                              │
    │  ┌──────────────┐    ┌──────────────┐  ┌───────────┐  │
    │  │ Publish to   │───▶│ Build App    │─▶│Upload App │  │
    │  │ Nexus        │    │ Image        │  │ Image     │  │
    │  │ (WAR→Nexus)  │    │(docker.build)│  │(→ ECR)    │  │
    │  └──────────────┘    └──────────────┘  └─────┬─────┘  │
    │                                              │        │
    │                                              ▼        │
    │                                       ┌───────────┐   │
    │                                       │Deploy to  │   │
    │                                       │ ECS       │   │
    │                                       │(aws ecs   │   │
    │                                       │ update-   │   │
    │                                       │ service)  │   │
    │                                       └───────────┘   │
    └─────────────────────────────────────────────────────────┘
        │
        ▼
    ECS pulls new image from ECR → stops old container → 
    drains connections → starts new container → steady state

 [\[180. PAAC_...CD_ECS_ECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.%20PAAC_CICD_ECS_ECR.txt), [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt)

***

## 📋 Complete Pipeline Script Reference

The full pipeline script from [180. PAAC\_CICD\_ECS\_ECR.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.%20PAAC_CICD_ECS_ECR.txt?EntityRepresentationId=73f085e8-9820-4534-85a0-9ad70d7a2470) is the definitive reference for this lecture. It contains all 10 stages, global environment variables, and both CI and CD configurations. Key points to double-check before running: [\[180. PAAC_...CD_ECS_ECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.%20PAAC_CICD_ECS_ECR.txt)

| Configuration          | Where to verify                | Value in this pipeline                         |
| ---------------------- | ------------------------------ | ---------------------------------------------- |
| Git branch             | GitHub repository              | `docker`                                       |
| Maven tool name        | Jenkins → Manage → Tools       | `MAVEN3.9`                                     |
| JDK tool name          | Jenkins → Manage → Tools       | `JDK17`                                        |
| SonarQube scanner tool | Jenkins → Manage → Tools       | `sonar8.0`                                     |
| SonarQube server name  | Jenkins → Manage → System      | `sonarserver`                                  |
| ECR registry URL       | AWS ECR console                | `980088651931.dkr.ecr.us-east-1.amazonaws.com` |
| ECR image repository   | AWS ECR console                | `vprofileappimg`                               |
| AWS credentials ID     | Jenkins → Manage → Credentials | `awscreds`                                     |
| Nexus credentials ID   | Jenkins → Manage → Credentials | `nexuslogin`                                   |
| Nexus server URL       | Nexus server private IP        | `172.31.21.185:8081`                           |
| ECS cluster name       | AWS ECS console                | `vprofile`                                     |
| ECS service name       | AWS ECS console                | `vproappservice`                               |
| AWS Steps plugin       | Jenkins → Manage → Plugins     | Must be installed                              |

 [\[180. PAAC_...CD_ECS_ECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.%20PAAC_CICD_ECS_ECR.txt), [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt)

Every value in the "Value in this pipeline" column is **environment-specific**. When you replicate this in your own setup, your account ID, region, IP addresses, and names will differ. The **structure and logic** of the pipeline, however, remains identical. [\[180.-Docke...onstration \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/180.-Docker-CICD-Demonstration.txt)
