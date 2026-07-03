# 📘 GitHub Actions — Secrets, Docker & ECR Setup — Deep Learning Material

*Reconstructed from video lecture: [191-secrets-and-docker.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/191-secrets-and-docker.txt?EntityRepresentationId=e0e1863c-567b-4821-9089-9663877ac841)* [\[191-secret...and-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/191-secrets-and-docker.txt)

***

## 🧠 SECTION 1: THEORY (Deep Learning Mode)

### The Goal: Building and Pushing Docker Images from GitHub Actions

This lecture addresses a specific milestone in the GitHub Actions CI/CD pipeline: taking application source code, building a Docker image from it, and uploading that image to **Amazon ECR (Elastic Container Registry)**. However, this lecture focuses entirely on the **prerequisites and preparation** — the actual job creation happens in the next lecture. The prerequisites are: creating the ECR repository, setting up IAM authentication, securely storing credentials in GitHub, and adapting the Dockerfile for the pipeline context. [\[191-secret...and-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/191-secrets-and-docker.txt)

Understanding *why* each prerequisite exists and *how* it connects to the others is what separates mechanical setup from engineering understanding.

***

### Amazon ECR: The Docker Image Repository

Amazon ECR is a fully managed container image registry provided by AWS. Its role in this system is straightforward: it is the **storage destination** for the Docker images that the GitHub Actions workflow will build. When the pipeline builds a Docker image from the source code, that image needs to live somewhere accessible — somewhere that deployment services (like ECS, EKS, or other container orchestrators) can pull from. ECR serves that purpose. [\[191-secret...and-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/191-secrets-and-docker.txt)

The ECR repository is created in a specific AWS **region** — in this lecture, `us-east-1` (North Virginia). This region choice matters because the IAM credentials, the GitHub workflow configuration, and any downstream services consuming the image must all reference the same region. A repository created in `us-east-1` is not visible from `us-west-2` unless cross-region replication is configured. [\[191-secret...and-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/191-secrets-and-docker.txt)

The repository is given the name `vprofile-app-image`. This name becomes part of the full image URI that the workflow will use to push images (e.g., `<account-id>.dkr.ecr.us-east-1.amazonaws.com/vprofile-app-image`).

***

### IAM Access Keys: The Authentication Bridge

GitHub Actions runs on GitHub's infrastructure — not inside your AWS account. For a GitHub Actions workflow to interact with any AWS service (like pushing an image to ECR), it must **authenticate** with AWS. This authentication happens through **IAM access keys**: an Access Key ID and a Secret Access Key, which together function like a username and password for programmatic AWS access. [\[191-secret...and-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/191-secrets-and-docker.txt)

The lecture creates a dedicated IAM user named `actions-ecr` specifically for this purpose. This is a deliberate design choice — rather than using a personal AWS account's credentials or a shared admin key, a purpose-specific user is created with only the permissions it needs. The user is given the **EC2 Container Registry Full Access** managed policy, which grants complete access to ECR operations (create/read/update/delete repositories and images). [\[191-secret...and-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/191-secrets-and-docker.txt)

The lecture acknowledges that this is a broad permission: "sure we can fine tune it, but we are going to keep it normal for now." The fine-tuned alternative would be creating a **custom IAM policy** that grants access only to the specific repository (not all repositories in the account). The full-access policy is used for simplicity during learning. [\[191-secret...and-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/191-secrets-and-docker.txt)

The access keys are generated from the IAM user's **Security credentials** tab, selecting the **CLI** use case. AWS shows both keys once — the Secret Access Key is never displayed again after this point, mirroring the write-only pattern seen in GitHub Secrets. [\[191-secret...and-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/191-secrets-and-docker.txt)

> 🔍 **Deep Dive (Optional)**
>
> The IAM user → access key → GitHub secret chain represents a common **cross-platform authentication pattern**: when System A (GitHub) needs to act on System B (AWS), you create an identity in System B with scoped permissions, generate credentials for that identity, and store those credentials securely in System A. This same pattern appears in Jenkins (storing AWS credentials as Jenkins credentials), Terraform (using AWS provider with access keys), and virtually any CI/CD tool that interacts with cloud providers.

> ⚠️ **Expert Note**
>
> In production environments, IAM access keys for CI/CD are increasingly replaced by **OIDC (OpenID Connect) federation**. GitHub Actions supports OIDC natively — instead of storing long-lived access keys, the workflow requests a short-lived token from AWS using GitHub's identity provider. This eliminates the risk of leaked credentials entirely. The access key approach shown here is simpler to set up and understand, but OIDC is the recommended production pattern.

***

### GitHub Secrets and Variables: Environment-Scoped Credential Storage

The IAM access keys must be stored somewhere the GitHub Actions workflow can access them — but they must never appear in the workflow YAML file itself or in any repository file. This is where **GitHub Secrets** come in, as introduced conceptually in the previous lecture. [\[191-secret...and-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/191-secrets-and-docker.txt)

This lecture makes a critical architectural decision: the secrets are stored in the **`production` environment**, not at the repository level. This means any workflow job that wants to use these secrets must explicitly declare that it uses the `production` environment. This scoping provides two benefits: the secrets are only accessible to jobs that target the correct environment, and environment protection rules (configured in the previous lecture) can further restrict which branches and workflows can access them. [\[191-secret...and-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/191-secrets-and-docker.txt)

Two secrets are stored:

*   **`AWS_ACCESS_KEY_ID`** — the IAM access key ID
*   **`AWS_SECRET_ACCESS_KEY`** — the IAM secret access key [\[191-secret...and-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/191-secrets-and-docker.txt)

The lecture emphasizes naming: "name can be anything, but I'm using this name and the same name I need to mention in my workflow steps." The secret names you choose here must exactly match what your workflow code references via `${{ secrets.AWS_ACCESS_KEY_ID }}`. If you choose a different name, you must update the workflow code accordingly. [\[191-secret...and-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/191-secrets-and-docker.txt)

The **AWS region** is also needed by the workflow but is not sensitive — it's just a string like `us-east-1`. Therefore, it is stored as an **environment variable** (not a secret): `AWS_REGION = us-east-1`. This follows the principle established in the previous lecture: secrets for sensitive data (encrypted, write-only), variables for non-sensitive configuration (plaintext, readable). [\[191-secret...and-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/191-secrets-and-docker.txt)

The lecture adds an important consistency check: the region stored in the variable must match the region where the ECR repository was created. If your ECR repo is in `us-east-1` but your variable says `us-west-2`, the workflow will attempt to push to a non-existent repository in the wrong region and fail.

***

### The Dockerfile: Adapting for CI/CD Context

The lecture works with an existing Dockerfile located at `Docker-files/app/multistage/Dockerfile`. This is a **multi-stage Docker build** — a Dockerfile that uses multiple `FROM` instructions to create intermediate build stages, ultimately producing a lean final image. [\[191-secret...and-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/191-secrets-and-docker.txt)

The original Dockerfile was designed to clone the source code from a repository inside the container and then build it. But in the GitHub Actions context, the source code **already exists** — the workflow's checkout step has already cloned the repository onto the runner. Cloning it again inside the Docker build would be redundant and wasteful. The lecture modifies the Dockerfile to reflect this new context. [\[191-secret...and-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/191-secrets-and-docker.txt)

The key modifications are:

**1. Remove the clone lines.** The original Dockerfile had lines that fetched the source code from the repository. These are removed because the code is already present in the runner's working directory. [\[191-secret...and-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/191-secrets-and-docker.txt)

**2. Copy source code from the host into the container.** The replacement line is `COPY ./ /app`. This copies everything from the current working directory (on the runner) into the `/app` directory inside the container. [\[191-secret...and-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/191-secrets-and-docker.txt)

**3. Set the working directory.** `WORKDIR /app` tells Docker that all subsequent commands execute from `/app` inside the container. [\[191-secret...and-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/191-secrets-and-docker.txt)

**4. Run the build command.** `RUN mvn install` executes the Maven build inside the container. This generates the artifact `vprofile-v2.war` at the path `/app/target/vprofile-v2.war`. [\[191-secret...and-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/191-secrets-and-docker.txt)

**5. Fix the artifact copy path in the second stage.** The second stage of the multi-stage build copies the built artifact from the build stage into a Tomcat image. The `COPY --from=build-image` instruction must reference the correct path: `/app/target/vprofile-v2.war`. The lecture updates this path to match the new working directory structure. [\[191-secret...and-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/191-secrets-and-docker.txt)

An important detail the lecture highlights: the Docker image will be built from the **root directory** of the repository (not from inside the `Docker-files/app/multistage/` folder). This means `COPY ./` copies the entire repository root into the container — all source code, all configuration files, everything the Maven build needs. The `docker build` command in the workflow will specify the Dockerfile path but set the build context to the repository root.

> 🔍 **Deep Dive (Optional)**
>
> Multi-stage Docker builds solve a fundamental problem: build tools (Maven, JDK, source code) are needed to *create* the artifact, but they should not exist in the *final* image. The first stage (the build stage) has Maven, JDK, and source code — it compiles and packages the application. The second stage starts from a clean Tomcat image and copies *only* the compiled WAR file from the first stage. The final image contains only Tomcat + the WAR — no build tools, no source code, resulting in a smaller and more secure image.

***

## ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

### What We Are Building

We are setting up all the prerequisites for a GitHub Actions workflow job that will build a Docker image from application source code and push it to Amazon ECR. The prerequisites are: an ECR repository (the destination), IAM credentials (the authentication mechanism), GitHub secrets/variables (secure credential storage), and a modified Dockerfile (adapted for the CI/CD context). The actual workflow job is created in the next lecture — this lecture completes all the groundwork. [\[191-secret...and-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/191-secrets-and-docker.txt)

***

### Step 1: Create the Amazon ECR Repository

Log in to your **AWS Management Console**. Confirm you are in the correct region — the lecture uses **US East 1 (North Virginia)**. The region selector is in the top-right corner of the AWS console. [\[191-secret...and-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/191-secrets-and-docker.txt)

Search for **"Elastic Container Registry"** in the AWS services search bar and open it. Click **"Create a repository."** [\[191-secret...and-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/191-secrets-and-docker.txt)

*   **Repository name**: `vprofile-app-image`

Leave all other settings at their defaults and click **Create**. [\[191-secret...and-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/191-secrets-and-docker.txt)

**Verification:** The repository appears in the ECR repository list with the name `vprofile-app-image` and a URI in the format `<account-id>.dkr.ecr.us-east-1.amazonaws.com/vprofile-app-image`.

**Note the region.** You will need to store this exact region code (`us-east-1`) in a GitHub variable later. If you create the repository in a different region, use that region code instead.

***

### Step 2: Create an IAM User with ECR Permissions

Navigate to the **IAM** service in AWS. Go to **Users** → **Create user**. [\[191-secret...and-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/191-secrets-and-docker.txt)

*   **User name**: `actions-ecr`

Click **Next**. On the permissions page, select **Attach policies directly**. Search for `registry` in the policy search box. Find and select **`AmazonEC2ContainerRegistryFullAccess`**. [\[191-secret...and-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/191-secrets-and-docker.txt)

Click **Next** → **Create user**. [\[191-secret...and-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/191-secrets-and-docker.txt)

> ⚠️ **Expert Note**
>
> `AmazonEC2ContainerRegistryFullAccess` grants access to *all* ECR repositories in the account. For production, create a custom policy scoped to only the specific repository ARN. The lecture acknowledges this: "we can create our own policy and only give access to our repository." [\[191-secret...and-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/191-secrets-and-docker.txt)

***

### Step 3: Generate Access Keys

After creating the user, click on the user name (`actions-ecr`) to open their details. Go to the **Security credentials** tab. Scroll down to **Access keys** and click **Create access key**. [\[191-secret...and-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/191-secrets-and-docker.txt)

*   **Use case**: Select **CLI** (Command Line Interface)
*   Check the **"I understand"** acknowledgment
*   Click **Next** → **Create access key** [\[191-secret...and-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/191-secrets-and-docker.txt)

You will see two values:

*   **Access key ID** — e.g., `AKIAIOSFODNN7EXAMPLE`
*   **Secret access key** — e.g., `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`

**Do not close this page yet.** You need both values for the next step. The Secret Access Key is shown only once — if you lose it, you must generate a new key pair.

***

### Step 4: Store Credentials in GitHub Secrets

Navigate to your **GitHub repository** → **Settings** → scroll to **Secrets and variables** → click **Actions**. [\[191-secret...and-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/191-secrets-and-docker.txt)

Click **"Manage Environment Secrets"**. Select the **`production`** environment (created in the previous lecture). If you don't have it, create a new environment named `production` first. [\[191-secret...and-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/191-secrets-and-docker.txt)

**Add the first secret:**

*   Click **"Add environment secret"**
*   **Name**: `AWS_ACCESS_KEY_ID`
*   **Value**: paste the Access Key ID from the IAM console
*   Click **"Add secret"** [\[191-secret...and-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/191-secrets-and-docker.txt)

**Add the second secret:**

*   Click **"Add environment secret"**
*   **Name**: `AWS_SECRET_ACCESS_KEY`
*   **Value**: paste the Secret Access Key from the IAM console
*   Click **"Add secret"** [\[191-secret...and-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/191-secrets-and-docker.txt)

**Verification:** Both secrets appear in the list. You cannot view their values (encrypted, write-only) — only update them.

The naming matters: these exact names (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`) must match what the workflow references. If you choose different names, update the workflow code accordingly. [\[191-secret...and-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/191-secrets-and-docker.txt)

***

### Step 5: Store AWS Region as an Environment Variable

Still in the `production` environment settings, click **"Add environment variable"**. [\[191-secret...and-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/191-secrets-and-docker.txt)

*   **Name**: `AWS_REGION`
*   **Value**: `us-east-1` (or whichever region your ECR repository is in)
*   Click **"Add variable"** [\[191-secret...and-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/191-secrets-and-docker.txt)

**Consistency check:** Confirm this region matches where you created the ECR repository. Navigate back to the ECR console and verify the region in the URL or the console's region selector. A mismatch here will cause the workflow to fail when it tries to push to a non-existent repository in the wrong region.

**Connection to overall system:** The workflow job (next lecture) will declare `environment: production`, gaining access to `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` (as secrets), and `AWS_REGION` (as a variable). These three values are everything the AWS CLI/SDK needs to authenticate and target the correct region.

***

### Step 6: Modify the Dockerfile

Open your project in **VS Code**. Navigate to the Dockerfile at: [\[191-secret...and-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/191-secrets-and-docker.txt)

    Docker-files/app/multistage/Dockerfile

The original Dockerfile contains lines that clone the source code from a repository. In the GitHub Actions context, the source code already exists on the runner (checked out by the workflow). These clone lines are redundant.

**Modification 1 — Remove the clone lines.** Delete the two lines that fetch/clone the source code from the repository. [\[191-secret...and-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/191-secrets-and-docker.txt)

**Modification 2 — Add COPY instruction.** Replace them with:

```dockerfile
COPY ./ /app
```

This copies everything from the build context (the repository root on the runner) into the `/app` directory inside the container. The build context will be set to the repository root when `docker build` is invoked in the workflow. [\[191-secret...and-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/191-secrets-and-docker.txt)

**Modification 3 — Set the working directory:**

```dockerfile
WORKDIR /app
```

All subsequent commands (`RUN`, etc.) will execute from `/app`. [\[191-secret...and-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/191-secrets-and-docker.txt)

**Modification 4 — Run Maven build:**

```dockerfile
RUN mvn install
```

This executes inside the container from `/app` (where the source code now lives). It compiles the code and generates the artifact at `/app/target/vprofile-v2.war`. [\[191-secret...and-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/191-secrets-and-docker.txt)

**Modification 5 — Fix the COPY path in the second stage.** The second stage copies the artifact from the build stage into a Tomcat image. Update the source path to reflect the new directory structure:

```dockerfile
COPY --from=build-image /app/target/vprofile-v2.war <destination>
```

The path must be `/app/target/vprofile-v2.war` because:

*   `/app` is where the source code was copied
*   `/target` is created by `mvn install` inside the working directory
*   `vprofile-v2.war` is the artifact name generated by Maven [\[191-secret...and-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/191-secrets-and-docker.txt)

**Save the Dockerfile.** [\[191-secret...and-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/191-secrets-and-docker.txt)

**Common mistake:** If you build the Docker image from *inside* the `Docker-files/app/multistage/` directory, `COPY ./` would only copy files from that subfolder — missing all the source code. The workflow must build from the **repository root** and point to the Dockerfile using the `-f` flag or path argument.

***

### What Comes Next

All prerequisites are now in place: [\[191-secret...and-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/191-secrets-and-docker.txt)

*   ✅ ECR repository exists (`vprofile-app-image` in `us-east-1`)
*   ✅ IAM user exists (`actions-ecr`) with ECR full access
*   ✅ Access keys stored in GitHub Secrets (`production` environment)
*   ✅ Region stored in GitHub Variable (`production` environment)
*   ✅ Dockerfile adapted for CI/CD context (no clone, copies from runner)

The next lecture creates the **workflow job** that ties all of these together: checks out the code, builds the Docker image using this Dockerfile, authenticates with AWS using the stored secrets, and pushes the image to ECR.

***

## 🧠 SECTION 3: MENTAL COMPRESSION MAP

### Prerequisite Chain

    ECR Repository (AWS)
      → stores Docker images
      → region: us-east-1
      → name: vprofile-app-image
      
    IAM User (AWS)
      → name: actions-ecr
      → policy: AmazonEC2ContainerRegistryFullAccess
      → generates: Access Key ID + Secret Access Key
      
    GitHub Secrets (production env)
      → AWS_ACCESS_KEY_ID ← IAM Access Key ID
      → AWS_SECRET_ACCESS_KEY ← IAM Secret Access Key
      
    GitHub Variable (production env)
      → AWS_REGION = us-east-1 ← must match ECR repo region

    Dockerfile (modified)
      → removed: clone lines (redundant — code already on runner)
      → added: COPY ./ /app (from runner → container)
      → added: WORKDIR /app
      → kept: RUN mvn install → /app/target/vprofile-v2.war
      → fixed: COPY --from=build-image /app/target/vprofile-v2.war

***

### Cross-Platform Authentication Flow

    GitHub Actions Runner
      │
      │ needs to push image to AWS ECR
      │
      ├── Reads: secrets.AWS_ACCESS_KEY_ID     ← encrypted in GitHub
      ├── Reads: secrets.AWS_SECRET_ACCESS_KEY  ← encrypted in GitHub
      ├── Reads: vars.AWS_REGION                ← plaintext in GitHub
      │
      └── Authenticates → AWS IAM (user: actions-ecr)
            └── Policy: EC2ContainerRegistryFullAccess
                  └── Pushes image → ECR (vprofile-app-image)

***

### Dockerfile Transformation Logic

    BEFORE (standalone build):          AFTER (CI/CD pipeline build):
      Clone repo inside container         Source already on runner
      Build from cloned code              COPY ./ /app (host → container)
      Artifact at <clone-path>/target     WORKDIR /app
                                          RUN mvn install
                                          Artifact at /app/target/

    Multi-stage structure preserved:
      Stage 1 (build-image): Maven + JDK → compiles → /app/target/*.war
      Stage 2 (final):       Tomcat only → COPY --from=build-image → lean image

***

### Secret vs Variable Decision

    Sensitive?
      ├── YES → GitHub Secret (encrypted, write-only)
      │         AWS_ACCESS_KEY_ID
      │         AWS_SECRET_ACCESS_KEY
      │
      └── NO  → GitHub Variable (plaintext, readable)
                AWS_REGION

***

### Critical Consistency Constraints

    ECR region ←MUST MATCH→ AWS_REGION variable
    Secret names ←MUST MATCH→ workflow ${{ secrets.NAME }} references
    Dockerfile COPY path ←MUST MATCH→ docker build context (repo root)
    COPY --from path ←MUST MATCH→ WORKDIR + mvn install output path

***

### Reusable Engineering Pattern: Cross-Platform Service Integration

    1. Create RESOURCE in Target Platform (ECR repo in AWS)
    2. Create IDENTITY in Target Platform (IAM user with scoped policy)
    3. Generate CREDENTIALS for Identity (access keys)
    4. Store CREDENTIALS securely in Source Platform (GitHub Secrets)
    5. Store NON-SENSITIVE CONFIG in Source Platform (GitHub Variables)
    6. WORKFLOW references stored credentials → authenticates → operates on resource

    Pattern applies to: AWS, GCP, Azure, Docker Hub, any external service

 [\[191-secret...and-docker \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/191-secrets-and-docker.txt)
