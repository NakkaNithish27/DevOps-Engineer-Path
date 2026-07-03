# Nexus Artifact Upload in Jenkins Pipeline — Publishing Artifacts to Nexus Repository

> **Source**: [172.-Nexus-PAAC-Demo.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt?EntityRepresentationId=17ffd80c-fd96-46e2-9a01-603f8f7917f6) (caption transcript) + [172. PAAC\_CI\_Sonar\_Nexus.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.%20PAAC_CI_Sonar_Nexus.txt?EntityRepresentationId=fcf42388-d79f-41b7-9383-a8c36c96d111) (pipeline code resource) [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt), [\[172. PAAC_...onar_Nexus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.%20PAAC_CI_Sonar_Nexus.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1. The Problem — Why Upload Artifacts to Nexus?

In the previous lectures, the pipeline was already fetching code, building it, running unit tests, performing Checkstyle analysis, running SonarQube code analysis, and enforcing a Quality Gate. After all those stages succeed, a `.war` artifact sits inside Jenkins' workspace — specifically at `target/vprofile-v2.war`. But that artifact is trapped inside Jenkins. It exists only in the workspace of that particular build on that particular Jenkins server. [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

This is a problem for several reasons. First, Jenkins workspaces are temporary — they get cleaned up, overwritten by the next build, or lost if the server goes down. Second, other systems (deployment pipelines, QA environments, staging servers) need to pull that artifact, and they cannot reach into Jenkins' workspace to get it. Third, there is no versioning — you have no record of which build produced which artifact or when.

The solution is an **artifact repository** — a centralized, versioned storage system purpose-built for storing build outputs. **Nexus Repository** (by Sonatype) is one such system, and it was already set up in earlier lectures with a repository named `vprofile-repo`. The task in this video is to add a pipeline stage that **takes the artifact from Jenkins and uploads it to Nexus**, with a unique version for every build. [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

***

## 2. The Nexus Artifact Uploader Plugin

Jenkins communicates with Nexus through a plugin called the **Nexus Artifact Uploader** plugin. This plugin was already installed in a previous lecture. Its purpose is straightforward: it takes a file (JAR, WAR, or any artifact) from the Jenkins workspace and uploads it to a specified Nexus repository using Nexus's REST API. [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

In a Jenkinsfile, this plugin is invoked using the step name **`nexusArtifactUploader()`**, and you pass a set of named parameters to it — Nexus version, protocol, URL, repository name, credentials, and artifact details. The instructor's approach to finding the correct syntax is practical and worth noting: he looks at the **plugin documentation** (which shows a Jenkins pipeline example with the plugin name and options), checks **GitHub examples**, and also uses **AI tools** to see example usage. He then copies an example and modifies it to fit the project. [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

This is the standard workflow for integrating any Jenkins plugin into a pipeline: find the documentation or an example, copy the structure, and customize the parameters for your project.

***

## 3. Artifact Versioning — BUILD\_ID and BUILD\_TIMESTAMP

One of the most important concepts in this video is **dynamic artifact versioning**. Every time the pipeline runs, the uploaded artifact must have a **unique version** so that Nexus stores each build's artifact separately rather than overwriting the previous one. [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

The instructor achieves this by combining two Jenkins environment variables:

*   **`BUILD_ID`** — A built-in Jenkins variable that gives the build number (1, 2, 3, ...). It is incremental — each new build gets the next integer. This alone provides uniqueness, but doesn't tell you *when* the build happened.

*   **`BUILD_TIMESTAMP`** — A variable provided by the **Build Timestamp** plugin (installed in a previous lecture). It gives the exact date and time when the build started, formatted according to a pattern you configure in Jenkins. [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

By combining them as `${env.BUILD_ID}-${BUILD_TIMESTAMP}`, each artifact gets a version like `2.26-05-05_21-11` — the build number followed by the timestamp. This is both unique and human-readable. You can immediately tell which build produced it and when. [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

The **timestamp format** is configured in Jenkins under **Manage Jenkins → System** (formerly "Configure System"). You scroll to the Build Timestamp section and set the pattern. The instructor changes the default format to: **`yy-MM-dd_HH-mm`** — a two-digit year, month, day, then underscore, followed by hour and minute in 24-hour format. He explicitly removes seconds from the default format because minute-level precision is sufficient. [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

> 🔍 **Deep Dive (Optional)**
>
> The syntax for referencing environment variables in a Jenkinsfile uses the pattern `${env.VARIABLE_NAME}` or just `${VARIABLE_NAME}`. However, there's an important subtlety: the version string must be wrapped in **double quotes** (`"..."`), not single quotes (`'...'`). In Groovy (and therefore in Jenkinsfile), single-quoted strings are **literal** — they don't interpolate variables. Double-quoted strings **do** interpolate, so `"${env.BUILD_ID}"` resolves to the actual build number, while `'${env.BUILD_ID}'` would remain as the literal text `${env.BUILD_ID}`. This is a common source of bugs in Jenkinsfiles.

> ⚠️ **Expert Note (Optional)**
>
> In production, you might use more sophisticated versioning — semantic versioning from a `pom.xml`, Git commit hashes, or release tags. The `BUILD_ID + TIMESTAMP` approach is simple and effective for learning and for projects where the pipeline is the sole source of truth for versioning. For enterprise-grade artifact management, versioning strategy often ties into release management processes and may involve Maven release plugins or dedicated versioning tools.

***

## 4. The Nexus Artifact Uploader Parameters — Understanding Each One

The `nexusArtifactUploader()` step takes several parameters, and each one maps to a specific aspect of the upload process. Understanding them is essential: [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt), [\[172. PAAC_...onar_Nexus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.%20PAAC_CI_Sonar_Nexus.txt)

**`nexusVersion: 'nexus3'`** — Specifies which major version of Nexus you're running. Nexus 2 and Nexus 3 have different APIs. The value `'nexus3'` tells the plugin to use the Nexus 3 API. Since the course installed Nexus 3, this is correct. [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

**`protocol: 'http'`** — The communication protocol. Nexus can run over HTTP or HTTPS. In this setup, Nexus is running on a plain HTTP port (no SSL configured), so `'http'` is correct. [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

**`nexusUrl`** — The address of the Nexus server. The instructor uses the **private IP address** of the Nexus EC2 instance followed by port `8081` (Nexus's default port). A critical instruction: **do not include `http://` in this value** — the protocol is already specified in the `protocol` parameter. Including it here would result in a malformed URL like `http://http://...`. The instructor explicitly warns: *"Don't give HTTP or anything else. The protocol is already mentioned here."* [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

**`groupId: 'QA'`** — In Maven repository conventions, artifacts are organized by group ID, artifact ID, and version (the GAV coordinates). The group ID is typically a reverse domain name (like `com.example.project`), but for this project the instructor simply uses `'QA'` as a label to indicate this is from the QA pipeline. [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

**`version`** — The dynamic version string discussed above: `"${env.BUILD_ID}-${BUILD_TIMESTAMP}"`. [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

**`repository: 'vprofile-repo'`** — The name of the Nexus repository where artifacts will be stored. This must match exactly the repository name created in Nexus. The instructor confirms: *"Repository name is vprofile-repo. That is the one that we created in Nexus."* [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

**`credentialsId: 'nexuslogin'`** — The ID of a Jenkins credential (created in a previous lecture) that stores the Nexus username and password. Jenkins uses this credential to authenticate with Nexus when uploading. The instructor says: *"We created the Nexus credential, and its name is just Nexus login. So it's going to use that username and password that we mentioned in this credential."* [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

**`artifacts: [...]`** — An array of artifact definitions. Each artifact in the array is a map with these keys:

*   **`artifactId: 'vproapp'`** — The name of the artifact. The instructor chooses `'vproapp'` as a short name for the VProfile application. This becomes part of the artifact's identifier in Nexus. [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)
*   **`classifier: ''`** — An optional Maven classifier (used to distinguish variants like `sources`, `javadoc`, etc.). Left empty here because there's only one variant.
*   **`file: 'target/vprofile-v2.war'`** — The **path to the actual file** in the Jenkins workspace. This is the WAR file produced by `mvn install`. The instructor verifies this path by navigating to the Jenkins workspace: *"Go to workspaces. In workspaces, you should have a folder called Target. In that we have a vprofile-v2.war."* [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)
*   **`type: 'war'`** — The packaging type / file extension of the artifact.

***

## 5. Security Group Configuration — Network Access Between Jenkins and Nexus

Before the pipeline can upload to Nexus, Jenkins must be able to reach Nexus on **port 8081** over the network. Since both are running on AWS EC2 instances, this is controlled by **Security Groups** (AWS's virtual firewall). [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

The instructor checks the Nexus instance's security group and finds that port 8081 is currently open to "anywhere" (`0.0.0.0/0`). He tightens this by:

1.  Changing the existing rule to allow 8081 from **his own IP** (so he can access the Nexus web UI).
2.  Adding a **new inbound rule** allowing port 8081 from the **Jenkins security group** — this means any EC2 instance that belongs to Jenkins' security group can reach Nexus on 8081. [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

This is a standard AWS networking practice: instead of opening ports to the world, you restrict access to specific security groups, creating a trust relationship between services.

> ⚠️ **Expert Note (Optional)**
>
> In production environments, you would also typically run Nexus behind HTTPS (with a proper SSL certificate), restrict access further using VPC peering or private subnets, and potentially use IAM roles or service accounts instead of username/password credentials. The HTTP + password approach used here is appropriate for a learning environment.

***

## 6. The Concept of a Complete CI Pipeline — And What's Still Missing

After adding the Nexus upload stage, the instructor pauses to reflect on whether this is now a **complete continuous integration pipeline**. The stages are: Fetch Code → Build → Unit Test → Checkstyle Analysis → Sonar Code Analysis → Quality Gate → Publish to Nexus. [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

The instructor's answer is nuanced: *"So this is a complete continuous integration pipeline, or is it? Well, you see everything, but you don't see the start, you don't see the end, right?"* [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

Two things are missing:

1.  **Build Triggers** (the "start") — Currently, the pipeline runs only when you click "Build Now" manually. A real CI pipeline should trigger automatically — on a Git push, on a schedule, or on a webhook. This will be covered in a later lecture. [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

2.  **Notifications** (the "end") — When a pipeline fails, the team (DevOps engineers, developers) should be notified immediately — by email, Slack, or other channels — with information about **what failed and where**. Without notifications, failures go unnoticed. The instructor says notifications will be covered in the next lecture. [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

This is an important conceptual lesson: a CI pipeline is not just about the build and analysis stages in the middle. The **trigger mechanism** and the **feedback mechanism (notifications)** are equally critical components of a complete CI system.

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are adding a **"Publish to Nexus"** stage to an existing Jenkins CI pipeline. This stage takes the WAR artifact produced by the build stage and uploads it to a **Nexus repository** with a **unique, dynamic version** for every build. [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

**Why it matters**: In real-world systems, build artifacts must be stored in a centralized, versioned repository so that downstream processes (deployment pipelines, QA teams, release managers) can retrieve specific versions reliably. Nexus serves as this centralized artifact store.

**The final outcome**: Every time the pipeline runs, a new versioned artifact (e.g., `vproapp-2.26-05-05_21-11.war`) appears in the `vprofile-repo` repository in Nexus, downloadable and traceable. [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

The existing pipeline already has these stages: Fetch Code → Build → Unit Test → Checkstyle Analysis → Sonar Code Analysis → Quality Gate. We are adding one more stage at the end. [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

***

## Step 1: Verify the Artifact Exists in Jenkins Workspace

Before writing any pipeline code, the instructor first confirms **what artifact exists and where**. This is a critical habit — you need to know the exact file path to tell the plugin what to upload. [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

Navigate to the **Jenkins dashboard** → click on the existing code analysis job → click on any recent **Build ID** → click on **Workspace**. Inside the workspace, look for a folder called **`target/`**. Inside that folder, you should see **`vprofile-v2.war`**. [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

This confirms two things:

*   The artifact exists at the path `target/vprofile-v2.war` (relative to the workspace root).
*   The artifact is a `.war` file.

These values will be used in the plugin configuration: `file: 'target/vprofile-v2.war'` and `type: 'war'`.

**Connection to the overall system**: This file was created by the `mvn install -DskipTests` command in the Build stage. Maven's `install` phase compiles the code, packages it into a WAR (as defined in the project's `pom.xml`), and places it in the `target/` directory.

***

## Step 2: Find the Plugin Syntax

The instructor looks up the **Nexus Artifact Uploader** plugin documentation to get the correct Pipeline syntax. He checks the official documentation (which shows the plugin name and options in a Jenkins pipeline example), looks at GitHub examples, and also uses AI tools to see a usage example. [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

The structure he finds is:

```groovy
nexusArtifactUploader(
    nexusVersion: '...',
    protocol: '...',
    nexusUrl: '...',
    groupId: '...',
    version: '...',
    repository: '...',
    credentialsId: '...',
    artifacts: [
        [artifactId: '...', classifier: '', file: '...', type: '...']
    ]
)
```

He copies this template and will customize every parameter for the VProfile project. [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

***

## Step 3: Add the "Publish to Nexus" Stage to the Pipeline Code

The new stage is inserted **after the Quality Gate stage** in the existing pipeline. The instructor finds where the Quality Gate stage's closing curly brace is and adds the new stage below it, still inside the `stages { }` block. [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

Here is the complete new stage as it appears in the final pipeline: [\[172. PAAC_...onar_Nexus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.%20PAAC_CI_Sonar_Nexus.txt)

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
                [artifactId: 'vproapp',
                 classifier: '',
                 file: 'target/vprofile-v2.war',
                 type: 'war']
            ]
        )
    }
}
```

Let's break down every part of this stage:

### The Stage Container

```groovy
stage("Publish to Nexus") {
    steps {
        ...
    }
}
```

*   **`stage("Publish to Nexus")`** — Defines a new stage with the display name "Publish to Nexus." This name appears in Jenkins' stage view.
*   **`steps { }`** — Contains the actual plugin call. There is only one step in this stage: the `nexusArtifactUploader()` call.

### The Plugin Call — Parameter by Parameter

**`nexusVersion: 'nexus3'`** — We are running Nexus version 3. The plugin supports both Nexus 2 and 3, and they use different APIs, so this must be specified correctly. The instructor confirms: *"Nexus 3, that's the version that is correct."* [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

**`protocol: 'http'`** — Communication protocol. Our Nexus is running plain HTTP (no SSL). The instructor confirms: *"Protocol, http, that is also correct."* [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

**`nexusUrl: '172.31.21.185:8081'`** — The Nexus server address. This is the **private IP address** of the Nexus EC2 instance, followed by Nexus's default port `8081`. To get this value, you go to the **AWS Console**, select the Nexus EC2 instance, and copy its **Private IPv4 address**. [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

**Critical warning**: Do **NOT** include `http://` in this value. The protocol is already specified in the `protocol` parameter. The instructor explicitly warns about this. [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

> 🔍 **Deep Dive (Optional)**
>
> The reason a private IP is used (instead of a public IP) is that both Jenkins and Nexus are running in the same AWS VPC (Virtual Private Cloud). Communication within a VPC uses private IPs, which are stable (they don't change on instance stop/start in most configurations) and don't incur data transfer charges. Public IPs can change when instances are stopped and restarted (unless you use Elastic IPs), which would break the pipeline.

**`groupId: 'QA'`** — A label for the artifact group. In Maven conventions, this is typically a reverse domain (e.g., `com.vprofile`). The instructor simplifies it to `'QA'` to indicate this is from the QA/CI pipeline. [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

**`version: "${env.BUILD_ID}-${BUILD_TIMESTAMP}"`** — The dynamic version string. This is one of the most important parameters. Let's break it down: [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

*   **Double quotes `"..."`** — Required for string interpolation in Groovy. If you used single quotes, the variables would not be resolved.
*   **`${env.BUILD_ID}`** — References the Jenkins built-in environment variable `BUILD_ID`, which is the build number (1, 2, 3, ...).
*   **`-`** — A literal hyphen separating the two parts.
*   **`${BUILD_TIMESTAMP}`** — References the variable provided by the Build Timestamp plugin, which gives the formatted date/time of the build start.

The result for build #2 on May 5th, 2026 at 21:11 would be something like: `2-26-05-05_21-11`.

**`repository: 'vprofile-repo'`** — The exact name of the repository in Nexus where the artifact will be stored. This was created in a previous lecture. The instructor verifies by navigating to Nexus: *"That is the one that we created in Nexus."* [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

**`credentialsId: 'nexuslogin'`** — The ID of a Jenkins credential (type: Username with Password) that stores the Nexus admin username and password. This credential was created in Jenkins' credential store in a previous lecture. The plugin uses it to authenticate the upload request. [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

**`artifacts: [...]`** — An array (list) of artifact definitions. Each artifact is a map (key-value pairs) enclosed in square brackets: [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt), [\[172. PAAC_...onar_Nexus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.%20PAAC_CI_Sonar_Nexus.txt)

```groovy
[artifactId: 'vproapp',
 classifier: '',
 file: 'target/vprofile-v2.war',
 type: 'war']
```

*   **`artifactId: 'vproapp'`** — The name of the artifact in Nexus. The instructor chooses `'vproapp'` as a short name for VProfile Application.
*   **`classifier: ''`** — Empty. Classifiers are used to distinguish variants (like `sources`, `javadoc`). Not needed here.
*   **`file: 'target/vprofile-v2.war'`** — The path to the file in the Jenkins workspace. This is the WAR file verified in Step 1.
*   **`type: 'war'`** — The packaging type / file extension. [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

### Indentation and Formatting

The instructor spends time **fixing indentation** after pasting the copied plugin code. He makes the `artifacts` array vertical (one key per line) for readability, aligns closing brackets and parentheses with their opening counterparts, and ensures curly braces for `steps` and `stage` are on their own lines. [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

This is a practical habit: Jenkinsfiles are deeply nested, and poor indentation makes them nearly impossible to debug. The instructor explicitly takes time to make the code "look good."

***

## Step 4: Configure the BUILD\_TIMESTAMP Format in Jenkins

The `BUILD_TIMESTAMP` variable needs a format configured in Jenkins. Navigate to: **Jenkins Dashboard → Manage Jenkins → System** (scroll to the bottom or search for "BUILD\_TIMESTAMP"). [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

The instructor modifies the default timestamp format to:

    yy-MM-dd_HH-mm

Breaking this down: [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

*   **`yy`** — Two-digit year (e.g., `26` for 2026). The instructor changes the default four-digit year (`yyyy`) to two digits to keep the version string shorter.
*   **`-`** — Literal hyphen separator.
*   **`MM`** — Two-digit month (01–12).
*   **`-`** — Literal hyphen.
*   **`dd`** — Two-digit day of month (01–31).
*   **`_`** — Literal underscore separating date from time.
*   **`HH`** — Two-digit hour in 24-hour format (00–23).
*   **`-`** — Literal hyphen (the instructor replaces the default colon or other separator with a hyphen).
*   **`mm`** — Two-digit minute (00–59).

The instructor explicitly **removes seconds** from the default format because minute-level precision is sufficient for artifact versioning. [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

**Example output**: For a build on May 5, 2026 at 9:30 PM → `26-05-05_21-30`.

The instructor notes: *"You can give other old format also if you wish to."* — meaning this format is a personal choice and you can customize it. [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

**Save** the Jenkins system configuration after making this change.

***

## Step 5: Verify Network Access — Security Group Configuration

Before running the pipeline, you must ensure Jenkins can reach Nexus on port 8081. Both are on AWS EC2. [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

1.  Go to the **AWS Console** → EC2 → find the **Nexus instance** → click on its **Security Group**.
2.  Click **Edit Inbound Rules**.
3.  The instructor finds port 8081 is open from "anywhere" (`0.0.0.0/0`). He tightens this:
    *   **Change** the existing 8081 rule's source to **his own IP** (so he can still access the Nexus web UI from his browser).
    *   **Add** a new inbound rule: port `8081`, source = **Jenkins Security Group** (select the security group attached to the Jenkins instance). This allows Jenkins to communicate with Nexus on 8081. [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)
4.  **Save rules**.

**What this achieves**: Only the instructor's IP and Jenkins can reach Nexus on port 8081. All other traffic is blocked. This is a security best practice — minimal access, explicitly granted.

**How to verify**: If this is misconfigured, the pipeline will fail at the "Publish to Nexus" stage with a connection timeout or connection refused error.

***

## Step 6: Create and Run the Pipeline Job

Now everything is configured. Time to create the job and run it: [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

1.  **Copy the entire pipeline code** from your editor (the full pipeline including all existing stages plus the new Nexus stage).
2.  Go to **Jenkins Dashboard → New Item**.
3.  Name it **`vprofile-ci-pipeline`**.
4.  Select **Pipeline** as the item type.
5.  Click **OK**.
6.  Scroll down to the **Pipeline** section and **paste** the pipeline script.
7.  Click **Save**.
8.  Click **Build Now**. [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

The pipeline will execute all stages sequentially: Fetch Code → Build → Unit Test → Checkstyle Analysis → Sonar Code Analysis → Quality Gate → **Publish to Nexus**. [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

The instructor pauses the recording while the pipeline runs (it takes some time because of all the stages — building, testing, code analysis, quality gate check, and finally uploading). [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

### A Hiccup — Jenkins Disk Space

The instructor mentions he had "a few hiccups" — Jenkins ran out of disk space. He notes this **should not happen** for the student because the course instructions specify **20 GB of EBS volume** for the Jenkins instance. This is a practical reminder: CI pipelines that build, test, and analyze Java projects consume significant disk space (Maven downloads dependencies, SonarQube generates reports, artifacts accumulate). Insufficient disk is a common cause of mysterious build failures. [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

> ⚠️ **Expert Note (Optional)**
>
> In production Jenkins environments, disk space management is an ongoing concern. Old build artifacts, workspace leftovers, and Maven local repository caches accumulate over time. Common mitigations include: configuring Jenkins to discard old builds (in job settings → "Discard old builds"), running periodic workspace cleanup, using external artifact storage (like Nexus or S3) instead of Jenkins archiving, and monitoring disk usage with Jenkins plugins like the Disk Usage plugin.

***

## Step 7: Verify the Upload in Nexus

After the pipeline completes successfully: [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

### Check from Jenkins:

Click on the **"Publish to Nexus"** stage in the stage view, and examine its console output. You should see a line saying **"Uploading artifact"** followed by a URL. This URL uses the **private IP**, so you cannot click it directly from your browser. To access it, you would need to replace the private IP with the Nexus instance's **public IP**. [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

### Check from Nexus:

1.  Open the **Nexus web UI** in your browser (using the public IP and port 8081).
2.  Click **Browse** (in the left sidebar).
3.  Select **`vprofile-repo`** from the repository list. [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

You should see the artifact listed. The artifact name follows the pattern:

    vproapp-<BUILD_ID>.<TIMESTAMP>.war

For example: **`vproapp-2.26-05-05_21-11.war`** [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

Breaking this down:

*   **`vproapp`** — The `artifactId` we configured.
*   **`2`** — The `BUILD_ID` (second build).
*   **`26-05-05_21-11`** — The `BUILD_TIMESTAMP` in the format we configured.
*   **`.war`** — The artifact type. [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

Nexus also provides a **download link** for each artifact. Clicking it downloads the WAR file directly. [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

***

## Step 8: Run the Pipeline Multiple Times to Verify Versioning

The instructor recommends running the pipeline **a few more times**, with at least **one minute between runs** (so the timestamp differs). Each run should produce a **new artifact with a new version** in Nexus. [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

For example:

*   Run 1: `vproapp-1.26-05-05_21-00.war`
*   Run 2: `vproapp-2.26-05-05_21-05.war`
*   Run 3: `vproapp-3.26-05-05_21-11.war`

Each has a different `BUILD_ID` and a different `BUILD_TIMESTAMP`. In Nexus, all three coexist — none overwrites the other. This is the core value of versioned artifact storage. [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

**Connection to the overall system**: This versioning allows deployment pipelines to pull a **specific version** of the artifact. If version 3 has a bug, you can deploy version 2 instead. If you need to audit what was deployed to production last Tuesday, you can trace it back to the exact build and timestamp.

***

## Step 9: The Complete Pipeline Code (All Stages)

Here is the full pipeline as it exists after this lecture, with all stages: [\[172. PAAC_...onar_Nexus \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.%20PAAC_CI_Sonar_Nexus.txt)

```groovy
pipeline {
    agent any
    tools {
        maven "MAVEN3.9"
        jdk "JDK17"
    }
    stages {
        stage('Fetch code') {
            steps {
                git branch: 'atom', url: 'https://github.com/hkhcoder/vprofile-project.git'
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
        stage('Sonar Code analysis') {
            environment {
                scannerHome = tool 'sonar8.0';
            }
            steps {
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
    }
}
```

***

## What Comes Next (As Stated by the Instructor)

The instructor outlines what's still needed to make this a truly complete CI pipeline: [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

*   **Notifications** — The very next lecture will cover how to send notifications (email, Slack, etc.) when the pipeline fails, so developers and DevOps engineers know what went wrong and where.
*   **Build Triggers** — Will be covered later. Currently the pipeline runs only on manual "Build Now" clicks. In a real CI setup, it should trigger automatically on Git pushes or on a schedule.

The instructor also provides practical advice for shutting down instances: if you're continuing to the next lecture, **keep Jenkins running** but you can shut down Nexus and SonarQube (they're not needed for the notifications lecture). If you're stopping for the day, **shut everything down** to avoid unnecessary AWS costs. [\[172.-Nexus-PAAC-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/172.-Nexus-PAAC-Demo.txt)

***

This completes the full reconstruction of the video content — covering the theory behind artifact versioning and Nexus uploads, and every practical step from verifying the workspace artifact through to confirming versioned artifacts in Nexus. Would you like me to save this as a downloadable markdown file?
