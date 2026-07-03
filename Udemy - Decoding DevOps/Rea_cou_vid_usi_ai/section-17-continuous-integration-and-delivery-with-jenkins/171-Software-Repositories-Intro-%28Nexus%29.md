# 🎓 Software Repositories — Introduction to Nexus (Lecture 171)

**Video Title:** Software Repositories Intro (Nexus)
**Context:** This lecture is part of a CI/CD pipeline series. At this point, Jenkins can already fetch code from Git, build it with Maven, and analyze it with SonarQube. The next missing piece is **storing the built artifact** in a centralized repository. This lecture introduces the concept of software repositories, explains why Nexus exists, and walks through creating a Nexus repository and storing its credentials in Jenkins — preparing for the pipeline integration that follows in the next lecture. [\[171.-Softw...ro-(Nexus) \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/171.-Software-Repositories-Intro-%28Nexus%29.txt)

***

***

## 🧠 SECTION 1: THEORY — Deep Learning Mode

***

### 1. The Pipeline So Far — Why We Need a Repository Now

The instructor opens by establishing exactly where we are in the CI pipeline journey: **"We can now build the software, test it, and analyze the code. The next step is to upload the artifact to Nexus Repository."** [\[171.-Softw...ro-(Nexus) \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/171.-Software-Repositories-Intro-%28Nexus%29.txt)

This is a critical framing statement. Up to this point, the pipeline does three things:

1.  **Fetch** the source code (from Git, using the Git plugin).
2.  **Build** the code (using Maven, producing an artifact like a `.war` or `.jar` file).
3.  **Analyze** the code (using SonarQube, checking for bugs, vulnerabilities, and code smells).

But after the build completes, the artifact sits on the Jenkins server's local filesystem. This is a problem. Jenkins is a **transient automation server** — it is not designed to be a permanent storage location. If Jenkins crashes, gets redeployed, or runs out of disk space, those artifacts are gone. More importantly, other systems (staging servers, production servers, deployment scripts) need to **pull** that artifact from somewhere reliable. That "somewhere" is a **software repository**, and in this course, that repository is **Nexus**. [\[171.-Softw...ro-(Nexus) \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/171.-Software-Repositories-Intro-%28Nexus%29.txt)

***

### 2. What Is Nexus OSS Sonatype — The Concept of a Software Repository

The instructor introduces Nexus with a clear definition: **"Nexus OSS Sonatype is a software repository. As the name says, it's a place to store and retrieve softwares."** [\[171.-Softw...ro-(Nexus) \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/171.-Software-Repositories-Intro-%28Nexus%29.txt)

A **software repository** is a centralized server whose sole purpose is to store, version, and distribute software packages and build artifacts. Think of it as a warehouse for software — just as a physical warehouse stores products that can be shipped to customers, a software repository stores build outputs that can be deployed to servers.

**Nexus OSS** (Open Source Software) by **Sonatype** is one of the most widely used repository managers in the DevOps world. The "OSS" designation means there is a free, open-source version available (alongside a paid "Pro" version with additional features). It runs on **Java**, which is why the Nexus server setup script (from a previous lecture) included a step to install Java as a prerequisite. [\[171.-Softw...ro-(Nexus) \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/171.-Software-Repositories-Intro-%28Nexus%29.txt)

***

### 3. The Two Core Use Cases of a Software Repository

The video makes an important distinction — a software repository like Nexus serves **two** purposes, not just one:

**Use Case 1: Storing Artifacts (Upload)**
After your CI pipeline builds the application, the resulting artifact (e.g., a `.war` file for a Java web app) needs to be stored somewhere centralized, versioned, and retrievable. You **upload** this artifact to Nexus. This is the primary use case for this course. [\[171.-Softw...ro-(Nexus) \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/171.-Software-Repositories-Intro-%28Nexus%29.txt)

**Use Case 2: Downloading Dependencies (Proxy/Cache)**
When you run a command like `mvn install`, Maven downloads project dependencies (libraries, frameworks) from the internet — typically from Maven Central Repository. But in an organization, you can configure Maven to download those dependencies from **your own Nexus repository** instead. Nexus acts as a local cache/proxy: it fetches the dependency from the internet the first time, stores it locally, and serves it from its local cache for all subsequent requests. [\[171.-Softw...ro-(Nexus) \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/171.-Software-Repositories-Intro-%28Nexus%29.txt)

The instructor explicitly states: **"In this example, we will see how to store our artifact to the repository"** — making it clear that while both use cases exist, this lecture focuses on the first one. [\[171.-Softw...ro-(Nexus) \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/171.-Software-Repositories-Intro-%28Nexus%29.txt)

> 🔍 **Deep Dive (Optional):**
> Why would an organization use Nexus as a dependency proxy instead of downloading directly from the internet? Several reasons: **Speed** — downloading from a local network server is faster than the internet. **Reliability** — if Maven Central goes down or has network issues, your builds still work because dependencies are cached locally. **Security** — the organization can control and audit exactly which dependencies are allowed, blocking vulnerable or unauthorized libraries. **Bandwidth** — hundreds of developers downloading the same libraries from the internet wastes bandwidth; a local proxy downloads each library only once.

***

### 4. Types of Repositories — The Format Landscape

Nexus is not limited to one type of software. The video lists several repository formats that Nexus supports:

| Format       | What It Stores               | Ecosystem           |
| ------------ | ---------------------------- | ------------------- |
| **Maven**    | `.jar`, `.war`, `.pom` files | Java projects       |
| **apt**      | `.deb` packages              | Debian/Ubuntu Linux |
| **yum**      | `.rpm` packages              | RHEL/CentOS Linux   |
| **NuGet**    | `.nupkg` packages            | .NET projects       |
| **npm**      | JavaScript packages          | Node.js / frontend  |
| **Docker**   | Container images             | Docker / Kubernetes |
| **RubyGems** | `.gem` packages              | Ruby projects       |

The instructor's key message: **"Based on what kind of project you work, you will have that kind of repositories that you will use to store or retrieve softwares."** This means Nexus is a universal repository manager — it adapts to your technology stack. [\[171.-Softw...ro-(Nexus) \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/171.-Software-Repositories-Intro-%28Nexus%29.txt)

The video also specifically mentions Docker: **"Docker to store and retrieve Docker images. We'll see in next lectures how to do that for Docker as well."** This foreshadows that later in the course, Nexus will also be used as a **Docker registry** — a place to push and pull Docker container images. [\[171.-Softw...ro-(Nexus) \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/171.-Software-Repositories-Intro-%28Nexus%29.txt)

***

### 5. Hosted vs. Proxy vs. Group — The Three Repository Types

When creating a repository in Nexus, you must choose one of **three types**. The video explains this clearly when the instructor reaches the repository creation screen:

**Hosted Repository:**
This is a repository where **you upload your own artifacts**. It is your organization's internal storage. When Jenkins builds an artifact and pushes it to Nexus, it goes into a hosted repository. The instructor says: **"Our use case is to store the artifact, so you have to use hosted."** [\[171.-Softw...ro-(Nexus) \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/171.-Software-Repositories-Intro-%28Nexus%29.txt)

**Proxy Repository:**
This type acts as a **middleman** between your internal systems and an external repository (like Maven Central). When a developer or build tool requests a dependency, Nexus checks if it has a cached copy. If yes, it serves it locally. If not, it fetches it from the external source, caches it, and then serves it. The instructor says: **"If your use case is to download dependencies from the repository, then you set proxy."** [\[171.-Softw...ro-(Nexus) \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/171.-Software-Repositories-Intro-%28Nexus%29.txt)

**Group Repository:**
This type **combines multiple repositories** (both hosted and proxy) under a single URL. Instead of configuring your build tool to point to multiple repositories individually, you point it to one group repository, and Nexus internally routes requests to the appropriate underlying repository. The instructor briefly mentions: **"Group is to group both the repositories together."** [\[171.-Softw...ro-(Nexus) \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/171.-Software-Repositories-Intro-%28Nexus%29.txt)

> 🔍 **Deep Dive (Optional):**
> In a real-world enterprise Nexus setup, a typical Maven configuration looks like this: You have a **hosted** repository for your internal artifacts, a **proxy** repository that caches Maven Central, and a **group** repository that wraps both. Developers configure their `settings.xml` to point to the group URL only. When Maven needs an internal artifact, the group routes to hosted. When it needs an external library, the group routes to the proxy (which fetches from Maven Central if needed). This gives a single, clean entry point for all dependency resolution.

***

### 6. Artifact Versioning — Why Repositories Track Versions

The instructor makes a brief but important statement: **"We will be also using it to version, so we'll have multiple versions of our artifact."** [\[171.-Softw...ro-(Nexus) \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/171.-Software-Repositories-Intro-%28Nexus%29.txt)

This is a fundamental reason repositories exist. Every time your CI pipeline builds the application, it produces an artifact. But you don't want to overwrite the previous artifact — you want to keep **every version**. If version 2.5 has a bug, you need to be able to roll back to version 2.4. Nexus stores each version separately, identified by a combination of **groupId**, **artifactId**, and **version** (the Maven coordinate system for Java projects). This versioning capability turns Nexus into an auditable history of every build your pipeline has ever produced.

***

### 7. The Deployment Flow — What Happens After the Artifact Is Stored

The instructor describes what happens after the artifact reaches Nexus: **"Once the artifact is stored in the repository, upstream or an automation script can fetch that artifact and deploy it to the server."** [\[171.-Softw...ro-(Nexus) \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/171.-Software-Repositories-Intro-%28Nexus%29.txt)

This is the bridge between **CI (Continuous Integration)** and **CD (Continuous Deployment/Delivery)**. The CI pipeline's job ends when the tested, analyzed artifact is safely stored in Nexus. From there, a **separate process** — whether it's another pipeline, a deployment tool like Ansible, or a manual script — pulls that specific artifact version from Nexus and deploys it to the target server (staging, production, etc.).

The word **"upstream"** here refers to any system or process that consumes the artifact after it's stored. Nexus sits in the middle: the CI pipeline pushes artifacts in, and the deployment process pulls artifacts out.

***

### 8. Credentials Management — Why Jenkins Needs Nexus Credentials

To upload an artifact to Nexus, Jenkins needs to **authenticate** — it needs a username and password that Nexus will accept. But you never hardcode credentials directly in pipeline code. Instead, Jenkins has a **Credentials** store — a secure vault where you save credentials once, give them an ID, and then reference that ID in your pipeline code. The pipeline code never contains the actual password; it only contains the credential ID (e.g., `nexuslogin`), and Jenkins resolves it at runtime. [\[171.-Softw...ro-(Nexus) \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/171.-Software-Repositories-Intro-%28Nexus%29.txt)

The instructor explicitly warns: **"You never share username and password like that"** — acknowledging that he's showing the password on screen only because these are temporary lab instances that will be deleted. In real environments, credentials are tightly controlled and never exposed. [\[171.-Softw...ro-(Nexus) \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/171.-Software-Repositories-Intro-%28Nexus%29.txt)

***

***

## ⚙️ SECTION 2: PRACTICAL — Guided Execution Mode

***

### What We Are Building

In this practical section, we are doing **two things**:

1.  **Creating a Maven hosted repository in Nexus** — this is the actual storage location where our CI pipeline will upload built artifacts.
2.  **Storing Nexus credentials in Jenkins** — so that Jenkins can authenticate with Nexus when it needs to upload artifacts via pipeline code.

**Why it matters:** Without a repository, the artifact has nowhere to go after the build. Without stored credentials, the pipeline cannot authenticate with Nexus. These two steps are prerequisites for the pipeline integration that happens in the next lecture.

**Final outcome:** A repository named `vprofile-repo` exists in Nexus, and a credential entry named `nexuslogin` exists in Jenkins, ready to be referenced in pipeline code. [\[171.-Softw...ro-(Nexus) \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/171.-Software-Repositories-Intro-%28Nexus%29.txt)

***

### Step 1: Access the Nexus Server

The instructor already has the Nexus server running from a previous lecture. He takes the server's **public IP address** and accesses it on **port 8081** in a web browser. [\[171.-Softw...ro-(Nexus) \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/171.-Software-Repositories-Intro-%28Nexus%29.txt)

Nexus, by default, runs on port **8081**. The URL format is:

    http://<nexus-server-public-ip>:8081

If you're running Nexus on AWS (as in this course), the "public IP" is the EC2 instance's public IPv4 address, which you can find in the AWS EC2 console. Make sure the security group for the Nexus instance allows **inbound traffic on port 8081** — this was configured in a previous lecture.

**What you should see:** The Nexus web UI loads, showing the Nexus Repository Manager dashboard.

***

### Step 2: Sign In to Nexus

Click on **Sign In** (typically in the top-right corner of the Nexus UI). Log in with the **username and password** that were set during the initial Nexus setup in a previous lecture. [\[171.-Softw...ro-(Nexus) \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/171.-Software-Repositories-Intro-%28Nexus%29.txt)

After signing in, the instructor points out **two main sections** in the Nexus UI:

1.  **Browse** (the search/magnifying glass icon) — used to browse and explore the contents of repositories.
2.  **Settings** (the gear/cog icon) — used to manage repositories, users, roles, and other configurations.

For creating a new repository, we need the **Settings** section. [\[171.-Softw...ro-(Nexus) \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/171.-Software-Repositories-Intro-%28Nexus%29.txt)

***

### Step 3: Navigate to Repository Management

Click on the **Settings** icon (gear icon). Then go to **Repositories**. [\[171.-Softw...ro-(Nexus) \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/171.-Software-Repositories-Intro-%28Nexus%29.txt)

You will see a list of **existing repositories** — these are default repositories that Nexus creates during installation (e.g., `maven-central`, `maven-releases`, `maven-snapshots`, `nuget-hosted`, etc.). We are not going to use these defaults for our project; instead, we are creating a **new, dedicated repository** for our application. [\[171.-Softw...ro-(Nexus) \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/171.-Software-Repositories-Intro-%28Nexus%29.txt)

***

### Step 4: Create a New Maven Hosted Repository

Click the **Create repository** button. Nexus presents a list of **recipe types** — these are the repository format + type combinations you can choose from (e.g., `maven2 (hosted)`, `maven2 (proxy)`, `maven2 (group)`, `docker (hosted)`, `npm (proxy)`, etc.). [\[171.-Softw...ro-(Nexus) \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/171.-Software-Repositories-Intro-%28Nexus%29.txt)

Select **`maven2 (hosted)`**.

**Why `maven2 (hosted)`?**

*   **`maven2`** because our project is a Java/Maven project, and the artifact produced (e.g., a `.war` file) follows Maven conventions.
*   **`(hosted)`** because our use case is to **store/upload** our own artifact — not to proxy external dependencies or group repositories together. [\[171.-Softw...ro-(Nexus) \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/171.-Software-Repositories-Intro-%28Nexus%29.txt)

After selecting `maven2 (hosted)`, you are taken to a configuration form. The only field the instructor fills in is the **Name**:

    vprofile-repo

This is the repository name. It can be anything meaningful, but the instructor chooses `vprofile-repo` because the project being built throughout this course is called **vprofile**. [\[171.-Softw...ro-(Nexus) \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/171.-Software-Repositories-Intro-%28Nexus%29.txt)

Leave all other settings at their defaults and scroll down to click **Create repository**.

**Expected result:** The new repository `vprofile-repo` appears in the repository list. It is now an empty hosted repository, ready to receive artifacts.

**Connection to the overall pipeline:** This repository is the **destination** where Jenkins will push the built artifact. In the next lecture, the pipeline code will reference this repository name to tell Nexus exactly where to store the artifact.

> 🔍 **Deep Dive (Optional):**
> Among the default settings you're leaving unchanged is the **Version Policy**, which can be `Release`, `Snapshot`, or `Mixed`. For a learning/lab setup, the default (`Release`) works fine. In production, you'd typically have separate repositories for releases (stable, finalized versions) and snapshots (in-development, unstable versions). Maven treats these differently — snapshot versions can be overwritten, but release versions are typically immutable.

***

### Step 5: Navigate to Jenkins Credentials

Now switch to the **Jenkins** dashboard. The goal is to store the Nexus username and password in Jenkins' credential store so the pipeline can use them securely. [\[171.-Softw...ro-(Nexus) \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/171.-Software-Repositories-Intro-%28Nexus%29.txt)

From the Jenkins dashboard:

1.  Click **Manage Jenkins** (in the left sidebar).
2.  Find and click **Credentials**. [\[171.-Softw...ro-(Nexus) \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/171.-Software-Repositories-Intro-%28Nexus%29.txt)

This opens the Jenkins credential management interface. Click on the **Global credentials** scope (typically shown as `(global)` under the Jenkins store). This is the scope visible to all Jenkins jobs and pipelines. [\[171.-Softw...ro-(Nexus) \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/171.-Software-Repositories-Intro-%28Nexus%29.txt)

**What you'll see:** Any previously stored credentials appear here. The instructor notes that the **`sonartoken`** credential is already present — this is the secret text credential that was created in a previous lecture for SonarQube integration. We are now adding a **second** credential for Nexus. [\[171.-Softw...ro-(Nexus) \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/171.-Software-Repositories-Intro-%28Nexus%29.txt)

***

### Step 6: Add the Nexus Credential

Click **Add Credentials** (the button to create a new credential entry). Fill in the form as follows: [\[171.-Softw...ro-(Nexus) \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/171.-Software-Repositories-Intro-%28Nexus%29.txt)

| Field           | Value                    | Explanation                                                                                                                                       |
| --------------- | ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Kind**        | `Username with password` | Because Nexus authenticates using a traditional username + password combination (unlike SonarQube, which used a secret text/token).               |
| **Username**    | `Admin`                  | The Nexus admin username set during Nexus installation.                                                                                           |
| **Password**    | `admin123`               | The Nexus admin password set during installation.                                                                                                 |
| **ID**          | `nexuslogin`             | A unique identifier for this credential. This is the string you will reference in your pipeline code. The instructor specifies **all lowercase**. |
| **Description** | `nexuslogin`             | A human-readable description. The instructor sets it to the same value as the ID for simplicity.                                                  |

Click **Create**. [\[171.-Softw...ro-(Nexus) \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/171.-Software-Repositories-Intro-%28Nexus%29.txt)

**Why the ID matters:** In your Jenkinsfile (pipeline code), when you need to authenticate with Nexus, you will reference this credential by its **ID** — `nexuslogin`. Jenkins will look up this ID in its credential store, retrieve the actual username and password, and use them for authentication. The pipeline code never contains the raw password.

The instructor emphasizes: **"Do remember the name of this credential, `nexuslogin`. Otherwise, you can come here and check. We're going to put this in the pipeline code."** [\[171.-Softw...ro-(Nexus) \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/171.-Software-Repositories-Intro-%28Nexus%29.txt)

> ⚠️ **Expert Note (Optional):**
> The instructor uses `Admin` / `admin123` and openly acknowledges this is only acceptable because these are temporary lab instances: **"I'm telling you the password because anyways, I'm going to delete these instances once my work is done. But you never share username and password like that."** In production, you would use strong, unique passwords, potentially integrate with LDAP/Active Directory, and restrict who can view or manage Jenkins credentials through role-based access control. [\[171.-Softw...ro-(Nexus) \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/171.-Software-Repositories-Intro-%28Nexus%29.txt)

***

### Step 7: Verify and Prepare for the Next Step

At this point, two things are now in place:

1.  ✅ **Nexus** has a repository named `vprofile-repo` — ready to receive artifacts.
2.  ✅ **Jenkins** has a credential named `nexuslogin` — ready to authenticate with Nexus.

The instructor closes with: **"In the next lecture, we'll see how to write the pipeline code to upload our artifact to Nexus Repository."** This means the actual pipeline integration — writing the Jenkinsfile stage that uses the `nexuslogin` credential to upload the built `.war` file to `vprofile-repo` — is covered in the following lecture. [\[171.-Softw...ro-(Nexus) \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/171.-Software-Repositories-Intro-%28Nexus%29.txt)

***

***

## 🧭 End-to-End Pipeline Context Map

To see where this lecture fits in the bigger picture:

    ┌──────────────────────────────────────────────────────────────────┐
    │                     CI PIPELINE FLOW                             │
    │                                                                  │
    │  1. FETCH CODE         ──→  Git plugin pulls from GitHub         │
    │  2. BUILD              ──→  Maven compiles & packages (.war)     │
    │  3. ANALYZE            ──→  SonarQube scans code quality         │
    │  4. UPLOAD ARTIFACT    ──→  Nexus stores the versioned artifact  │  ◄── THIS LECTURE
    │  5. DEPLOY (later)     ──→  Pull from Nexus → deploy to server  │
    │                                                                  │
    └──────────────────────────────────────────────────────────────────┘

This lecture sets up **step 4** — creating the repository and credentials. The next lecture will write the pipeline code that actually performs the upload. [\[171.-Softw...ro-(Nexus) \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/171.-Software-Repositories-Intro-%28Nexus%29.txt)

***

Would you like me to save this as a downloadable markdown file?
