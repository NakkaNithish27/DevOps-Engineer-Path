# 📘 Docker CI/CD — Deploying to ECS (Pipeline Code Explained) — Deep Learning Material

*Reconstructed from video lecture: [178.-Docker-CICD-Code.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/178.-Docker-CICD-Code.txt?EntityRepresentationId=ac445751-a300-4711-8f5c-60dd69d45a10) with pipeline code reference: [178. PAAC\_CICD\_ECS\_ECR.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/178.%20PAAC_CICD_ECS_ECR.txt?EntityRepresentationId=ae784eab-1d55-4479-bdc6-f183c6212ce0)*

***

## 🧠 SECTION 1: THEORY (Deep Learning Mode)

### Context: Where This Lecture Fits

This lecture focuses on the **final stage** of the CI/CD pipeline — deploying the Docker container image to **AWS ECS (Elastic Container Service)**. In previous lectures, the pipeline already handles fetching code, building with Maven, running unit tests, performing Checkstyle and SonarQube analysis, enforcing a quality gate, publishing the artifact to Nexus, building a Docker image, and pushing that image to **AWS ECR (Elastic Container Registry)**. What remains is taking that image from ECR and actually **running it** as a container on ECS. This lecture explains the pipeline code that accomplishes that deployment. [\[178.-Docke...-CICD-Code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/178.-Docker-CICD-Code.txt)

***

### ECS Cluster: The Container Hosting Environment

An **ECS cluster** is the foundational infrastructure unit in AWS ECS. It is a logical grouping of resources where your containers run. Think of it as a "pool" of compute capacity that AWS manages on your behalf. When you deploy a container, you deploy it *into* a cluster. The cluster handles the underlying compute — whether that's EC2 instances or AWS Fargate serverless capacity — so you don't have to manually provision and manage individual servers for each container. [\[178.-Docke...-CICD-Code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/178.-Docker-CICD-Code.txt)

In this pipeline, a cluster named `vprofile` is used. This cluster will be created in the next lecture — this lecture only explains the code that *references* it. [\[178. PAAC_...CD_ECS_ECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/178.%20PAAC_CICD_ECS_ECR.txt)

***

### ECS Service: Complete Container Lifecycle Management

An **ECS service** is a construct that runs and maintains a specified number of container instances (tasks) within an ECS cluster. The lecture emphasizes that an ECS service gives you **complete management** of your container, bundling several critical capabilities into one: [\[178.-Docke...-CICD-Code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/178.-Docker-CICD-Code.txt)

*   **Load Balancer** — distributes incoming traffic across container instances
*   **Health Check Monitoring** — continuously checks whether your containers are healthy and automatically replaces unhealthy ones
*   **Logging** — captures container output for observability and debugging
*   **All in one** — these features are integrated, not separate tools you need to wire together [\[178.-Docke...-CICD-Code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/178.-Docker-CICD-Code.txt)

The service is the entity that actually *fetches* the Docker image from the ECR repository and *runs* it on the ECS cluster. In this pipeline, the service is named `vproappservice`. [\[178. PAAC_...CD_ECS_ECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/178.%20PAAC_CICD_ECS_ECR.txt)

The relationship is hierarchical: the **cluster** is the environment, and the **service** runs inside the cluster, managing one or more containers.

> 🔍 **Deep Dive (Optional)**
>
> An ECS service internally manages **tasks** — a task is one running instance of your container (defined by a task definition). The service ensures a desired number of tasks are always running. If a task crashes or fails a health check, the service automatically launches a replacement. When you trigger a new deployment (as this pipeline does), the service performs a **rolling update** — gradually replacing old tasks with new ones running the updated image, ensuring zero downtime.

***

### The Deployment Model: ECR → ECS

The flow the lecture describes is: the Docker image is already built and pushed to ECR (in previous pipeline stages). The deployment stage then tells the ECS service to look for the **latest image** available in the ECR repository and deploy it. This is the bridge between the CI part (build and push the image) and the CD part (deploy and run the image). [\[178.-Docke...-CICD-Code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/178.-Docker-CICD-Code.txt)

The mechanism is not a "pull and run" in the traditional Docker sense. Instead, the pipeline invokes an AWS CLI command that instructs the ECS service to perform a **new deployment**. The service itself then handles pulling the latest image from ECR and launching new container tasks based on it. [\[178.-Docke...-CICD-Code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/178.-Docker-CICD-Code.txt)

***

### Pipeline AWS Steps Plugin

To execute AWS commands within a Jenkins pipeline, you need the **Pipeline AWS Steps** plugin. This plugin provides pipeline DSL steps (like `withAWS`) that allow you to set AWS credentials and region context before executing AWS CLI commands. Without this plugin, your pipeline would have no native way to authenticate with AWS or set the correct region for API calls. [\[178.-Docke...-CICD-Code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/178.-Docker-CICD-Code.txt)

The plugin works by **exporting** the credentials and region information into the shell environment. When a shell command runs inside the `withAWS` block, it inherits these exported environment variables, allowing AWS CLI commands to authenticate automatically without hardcoding secrets in the pipeline code. [\[178.-Docke...-CICD-Code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/178.-Docker-CICD-Code.txt)

The lecture explicitly states that this plugin needs to be **installed in Jenkins** as a prerequisite. [\[178.-Docke...-CICD-Code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/178.-Docker-CICD-Code.txt)

***

### The `aws ecs update-service` Command

The core of the deployment is a single AWS CLI command:

```bash
aws ecs update-service --cluster ${cluster} --service ${service} --force-new-deployment
```

 [\[178. PAAC_...CD_ECS_ECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/178.%20PAAC_CICD_ECS_ECR.txt)

The lecture explains that this command performs the following: it checks for the **latest image available** in the ECR repository, fetches that container image, and executes the container on the ECS cluster under the specified service. [\[178.-Docke...-CICD-Code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/178.-Docker-CICD-Code.txt)

The `--force-new-deployment` flag is what triggers this behavior. Without it, if the service's task definition hasn't changed, ECS would not redeploy. The force flag tells ECS: "Even if nothing has technically changed in the configuration, start a new deployment cycle" — which causes the service to pull the latest image (tagged as `latest`) from ECR and replace the running containers. [\[178.-Docke...-CICD-Code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/178.-Docker-CICD-Code.txt)

> 🔍 **Deep Dive (Optional)**
>
> The reason `--force-new-deployment` works to pick up a new image is tied to how ECS resolves image tags. When the task definition references an image tag like `latest`, ECS resolves this tag to a specific image digest at deployment time. If the `latest` tag in ECR now points to a new image (because the pipeline just pushed one), forcing a new deployment causes ECS to re-resolve the tag, discover the new digest, and pull the updated image. Without the force flag, ECS would see that the task definition hasn't changed and skip the redeployment entirely — leaving the old image running.

***

### Environment Variables in the Pipeline

The lecture introduces two key variables defined at the top of the pipeline — `cluster` and `service` — that parameterize the deployment target: [\[178.-Docke...-CICD-Code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/178.-Docker-CICD-Code.txt)

```groovy
cluster = "vprofile"
service = "vproappservice"
```

 [\[178. PAAC_...CD_ECS_ECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/178.%20PAAC_CICD_ECS_ECR.txt)

These are defined in the `environment` block alongside other variables that were set up in previous lectures for ECR integration:

```groovy
environment {
    registryCredential = 'ecr:us-east-1:awscreds'
    appRegistry = "980088651931.dkr.ecr.us-east-1.amazonaws.com/vprofileappimg"
    vprofileRegistry = "https://980088651931.dkr.ecr.us-east-1.amazonaws.com"
    cluster = "vprofile"
    service = "vproappservice"
}
```

 [\[178. PAAC_...CD_ECS_ECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/178.%20PAAC_CICD_ECS_ECR.txt)

By defining `cluster` and `service` as environment variables rather than hardcoding them directly in the command, the pipeline becomes more maintainable. If the cluster or service name changes, you update it in one place (the `environment` block) rather than hunting through the pipeline code.

***

## ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

### What We Are Building

We are adding the **final deployment stage** to a Jenkins CI/CD pipeline. This stage takes the Docker image that was already built and pushed to AWS ECR (in previous stages) and **deploys it as a running container** on an AWS ECS cluster. After this stage executes, the application is live — running inside a managed container on ECS with load balancing, health checks, and logging handled automatically by the ECS service. [\[178.-Docke...-CICD-Code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/178.-Docker-CICD-Code.txt)

The lecture walks through the **code** that accomplishes this. The actual creation of the ECS cluster and service happens in the next lecture — this lecture is focused on understanding and writing the pipeline code. [\[178.-Docke...-CICD-Code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/178.-Docker-CICD-Code.txt)

***

### Step 1: Define the Cluster and Service Variables

At the top of the Jenkinsfile, inside the `environment` block, two new variables are added for the ECS deployment: [\[178.-Docke...-CICD-Code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/178.-Docker-CICD-Code.txt)

```groovy
environment {
    registryCredential = 'ecr:us-east-1:awscreds'
    appRegistry = "980088651931.dkr.ecr.us-east-1.amazonaws.com/vprofileappimg"
    vprofileRegistry = "https://980088651931.dkr.ecr.us-east-1.amazonaws.com"
    cluster = "vprofile"
    service = "vproappservice"
}
```

 [\[178. PAAC_...CD_ECS_ECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/178.%20PAAC_CICD_ECS_ECR.txt)

**`cluster = "vprofile"`** — This is the name of the ECS cluster that will be created in the next lecture. The ECS cluster is where your containers are hosted. The value `"vprofile"` is the name you will give the cluster during creation — it must match exactly. [\[178.-Docke...-CICD-Code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/178.-Docker-CICD-Code.txt)

**`service = "vproappservice"`** — This is the name of the ECS service that will be created inside the cluster. The service is responsible for fetching the Docker image from ECR and running it, providing load balancing, health checks, and logging. Again, this name must match the actual service name you create in ECS. [\[178.-Docke...-CICD-Code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/178.-Docker-CICD-Code.txt)

The other three variables (`registryCredential`, `appRegistry`, `vprofileRegistry`) were defined in previous lectures for building and pushing the Docker image to ECR. They remain unchanged.

**Connection to the overall system:** These variables parameterize the entire Docker workflow — from authentication with ECR, to identifying the image repository, to targeting the correct ECS cluster and service for deployment.

***

### Step 2: The Deploy to ECS Stage

After all the previous stages (fetch, build, test, analyze, quality gate, publish to Nexus, build Docker image, push to ECR), the final stage deploys the container: [\[178.-Docke...-CICD-Code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/178.-Docker-CICD-Code.txt)

```groovy
stage('Deploy to ecs') {
    steps {
        withAWS(credentials: 'awscreds', region: 'us-east-1') {
            sh 'aws ecs update-service --cluster ${cluster} --service ${service} --force-new-deployment'
        }
    }
}
```

 [\[178. PAAC_...CD_ECS_ECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/178.%20PAAC_CICD_ECS_ECR.txt)

Let's break down every component of this stage:

***

**`stage('Deploy to ecs')`** — Declares a new pipeline stage named "Deploy to ecs." This name appears in the Jenkins pipeline visualization (the stage view). It is the final functional stage before the pipeline completes. [\[178. PAAC_...CD_ECS_ECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/178.%20PAAC_CICD_ECS_ECR.txt)

***

**`withAWS(credentials: 'awscreds', region: 'us-east-1') { ... }`** — This is a step provided by the **Pipeline AWS Steps** plugin. It sets up the AWS execution context for any commands inside the block. [\[178.-Docke...-CICD-Code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/178.-Docker-CICD-Code.txt)

*   **`credentials: 'awscreds'`** — References a Jenkins credential with the ID `awscreds`. This credential was previously saved in Jenkins and contains the AWS access key and secret key needed to authenticate with AWS APIs. The `withAWS` step **exports** these credentials as environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`) so that any AWS CLI command running inside the block can authenticate automatically. [\[178.-Docke...-CICD-Code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/178.-Docker-CICD-Code.txt)

*   **`region: 'us-east-1'`** — Sets the AWS region for all commands in the block. This ensures the AWS CLI targets the correct region where your ECS cluster and ECR repository are located. This is also exported as an environment variable (`AWS_DEFAULT_REGION`). [\[178.-Docke...-CICD-Code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/178.-Docker-CICD-Code.txt)

The lecture explains this clearly: the plugin sets the region and credential, and "with that, you can execute your command." The shell command inside the block inherits this AWS context. [\[178.-Docke...-CICD-Code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/178.-Docker-CICD-Code.txt)

***

**`sh 'aws ecs update-service --cluster ${cluster} --service ${service} --force-new-deployment'`** — This is the actual deployment command, executed as a shell command on the Jenkins agent. Let's break down every part: [\[178. PAAC_...CD_ECS_ECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/178.%20PAAC_CICD_ECS_ECR.txt)

*   **`aws`** — Invokes the AWS Command Line Interface. This must be installed on the Jenkins agent for the command to work.

*   **`ecs`** — Specifies the ECS service group within the AWS CLI. All ECS-related commands fall under this group.

*   **`update-service`** — The specific ECS command. It updates an existing ECS service. In this context, "update" means triggering a new deployment cycle for the service.

*   **`--cluster ${cluster}`** — Specifies which ECS cluster the target service belongs to. `${cluster}` is resolved to the value `"vprofile"` from the environment variable defined earlier. [\[178.-Docke...-CICD-Code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/178.-Docker-CICD-Code.txt)

*   **`--service ${service}`** — Specifies which ECS service to update. `${service}` is resolved to `"vproappservice"` from the environment variable. [\[178.-Docke...-CICD-Code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/178.-Docker-CICD-Code.txt)

*   **`--force-new-deployment`** — This is the critical flag. It forces ECS to start a new deployment even if the service's task definition hasn't changed. What this does internally: ECS goes to the ECR repository, checks for the **latest image available**, pulls it, and starts new container tasks running that image, replacing the old ones. [\[178.-Docke...-CICD-Code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/178.-Docker-CICD-Code.txt)

**What happens internally when this command executes:**

1.  The AWS CLI sends an API request to the ECS service in the `us-east-1` region, authenticated with the `awscreds` credentials
2.  ECS receives the `update-service` request with `--force-new-deployment`
3.  ECS looks at the service's task definition to find the image reference (which points to the ECR repository with the `latest` tag)
4.  ECS resolves the `latest` tag in ECR to the newest image (the one the pipeline just pushed in the previous stage)
5.  ECS begins a rolling deployment — launching new tasks with the new image and gradually draining old tasks
6.  The service's load balancer routes traffic to the new healthy tasks
7.  Once all new tasks are healthy, old tasks are terminated [\[178.-Docke...-CICD-Code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/178.-Docker-CICD-Code.txt)

**Expected result:** The command returns a JSON response describing the updated service. The pipeline stage succeeds if the API call completes without error. The actual container replacement happens asynchronously — ECS continues the rolling deployment in the background after the command returns.

**How to verify success:**

*   In the Jenkins console output, you should see the JSON response from the `aws ecs update-service` command without any error messages
*   In the AWS ECS console, navigate to the cluster → service and check the "Deployments" tab to see the new deployment in progress
*   The service should eventually show the desired number of running tasks using the new image

**Common mistakes and failure scenarios:**

*   **AWS CLI not installed on Jenkins agent** — The `sh` command will fail with "aws: command not found"
*   **Incorrect credentials** — The `awscreds` credential in Jenkins must have IAM permissions to call `ecs:UpdateService`
*   **Cluster or service name mismatch** — If `cluster` or `service` variables don't match the actual names in ECS, the command fails with "service not found"
*   **Region mismatch** — If the region in `withAWS` doesn't match where the ECS cluster was created, the command will not find the cluster

> ⚠️ **Expert Note**
>
> The `--force-new-deployment` approach works well for simple deployments but has a subtlety: it depends on the `latest` tag in ECR being updated before this command runs. In this pipeline, the previous stage pushes the image with both the build number tag and the `latest` tag — so by the time this stage executes, `latest` points to the newest image. If, for any reason, the push stage failed silently or the `latest` tag wasn't updated, `--force-new-deployment` would redeploy the *same old image*, giving the illusion of a deployment without actually updating anything.

***

### Step 3: Plugin Prerequisite — Pipeline AWS Steps

The lecture explicitly states that the **Pipeline AWS Steps** plugin must be installed in Jenkins for the `withAWS` step to be available. This is a prerequisite that must be completed before running this pipeline. [\[178.-Docke...-CICD-Code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/178.-Docker-CICD-Code.txt)

To install it: navigate to **Manage Jenkins → Plugins → Available Plugins**, search for **Pipeline AWS Steps**, check the box, and install. The installation of this plugin is done alongside the creation of the ECS cluster and service in the next lecture. [\[178.-Docke...-CICD-Code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/178.-Docker-CICD-Code.txt)

Without this plugin, the pipeline will fail at the "Deploy to ecs" stage with an error indicating that `withAWS` is not a recognized pipeline step.

***

### Full Pipeline Code Reference

Here is the complete pipeline with all stages, including the new ECS deployment stage, as provided in the resource file: [\[178. PAAC_...CD_ECS_ECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/178.%20PAAC_CICD_ECS_ECR.txt)

```groovy
pipeline {
    agent any
    tools {
        maven "MAVEN3.9"
        jdk "JDK17"
    }
    environment {
        registryCredential = 'ecr:us-east-1:awscreds'
        appRegistry = "980088651931.dkr.ecr.us-east-1.amazonaws.com/vprofileappimg"
        vprofileRegistry = "https://980088651931.dkr.ecr.us-east-1.amazonaws.com"
        cluster = "vprofile"
        service = "vproappservice"
    }
    stages {
        stage('Fetch code') {
            steps {
                git branch: 'docker', url: 'https://github.com/hkhcoder/vprofile-project.git'
            }
        }
        stage('Build'){
            steps{
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
            steps{
                sh 'mvn test'
            }
        }
        stage('Checkstyle Analysis') {
            steps{
                sh 'mvn checkstyle:checkstyle'
            }
        }
        stage('Sonar Code analysis') {
            environment {
                scannerHome = tool 'sonar8.0';
            }
            steps{
                withSonarQubeEnv('sonarserver') {
                    sh '''${scannerHome}/bin/sonar-scanner \
                        -Dsonar.projectKey=vprofile \
                        -Dsonar.projectName=vprofile \
                        -Dsonar.projectVersion=1.0 \
                        -Dsonar.sources=src/ \
                        -Dsonar.java.binaries=target/classes \
                        -Dsonar.junit.reportsPath=target/surefire-reports \
                        -Dsonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml \
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
                        [artifactId: 'vproapp',
                         classifier: '',
                         file: 'target/vprofile-v2.war',
                         type: 'war']
                    ]
                )
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
            steps{
                script {
                    docker.withRegistry(vprofileRegistry, registryCredential) {
                        dockerImage.push("$BUILD_NUMBER")
                        dockerImage.push('latest')
                    }
                }
            }
        }
        stage('Deploy to ecs') {
            steps {
                withAWS(credentials: 'awscreds', region: 'us-east-1') {
                    sh 'aws ecs update-service --cluster ${cluster} --service ${service} --force-new-deployment'
                }
            }
        }
    }
}
```

***

### Connection to the Overall System

With this deployment stage added, the pipeline now represents a **complete end-to-end CI/CD workflow**: [\[178.-Docke...-CICD-Code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/178.-Docker-CICD-Code.txt), [\[178. PAAC_...CD_ECS_ECR \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/178.%20PAAC_CICD_ECS_ECR.txt)

1.  **Fetch Code** (GitHub, `docker` branch)
2.  **Build** (Maven, produce WAR artifact)
3.  **Unit Test** (Maven)
4.  **Checkstyle Analysis** (Maven)
5.  **SonarQube Code Analysis** (SonarQube Scanner)
6.  **Quality Gate** (SonarQube pass/fail verdict)
7.  **Publish to Nexus** (artifact repository)
8.  **Build Docker Image** (from the WAR artifact using a multistage Dockerfile)
9.  **Push Docker Image to ECR** (with build number tag + `latest` tag)
10. **Deploy to ECS** ← **this lecture** (force new deployment using the latest image)

The code is now fully explained. What remains before this pipeline can actually run is the **infrastructure setup** — creating the ECS cluster, creating the ECS service inside it, and installing the Pipeline AWS Steps plugin in Jenkins. All of that is covered in the next lecture. [\[178.-Docke...-CICD-Code \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/178.-Docker-CICD-Code.txt)
