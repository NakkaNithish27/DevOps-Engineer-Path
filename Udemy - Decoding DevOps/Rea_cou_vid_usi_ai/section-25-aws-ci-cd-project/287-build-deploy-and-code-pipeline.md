# 🚀 AWS CodePipeline — Build, Deploy & CI/CD Pipeline — Deep Learning Material

**Source:** *Build, Deploy and Code Pipeline* (Video Lecture Caption File) [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

## 1.1 What AWS CodePipeline Is — The AWS-Native CI/CD Orchestrator

AWS CodePipeline is AWS's **continuous integration and continuous delivery (CI/CD) service**. It does the same thing Jenkins does — automates the software release process — but it's a fully managed AWS service. You define **stages** (source, build, test, deploy), and CodePipeline orchestrates the flow between them: when code changes are detected, it automatically fetches the code, builds it, optionally tests it, and deploys it to the target environment. [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)

The instructor positions this explicitly: "Same like what we do in Jenkins. We create pipeline in Jenkins. Similar way in AWS, we use AWS CodePipeline." The key difference is that CodePipeline is deeply integrated with AWS services — CodeBuild for building, Beanstalk for deploying, CodeCommit/Bitbucket/GitHub for source — while Jenkins is platform-agnostic and requires plugins for AWS integration.

The instructor also makes a broader pedagogical point: "Once you know how to do CI/CD from Jenkins, you can do CI/CD from any other tool, any other cloud." The CI/CD concepts are transferable; only the tool-specific configuration changes. This section exists to demonstrate that portability. [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)

***

## 1.2 The Architecture — Four Components Connected by CodePipeline

The system being built has four distinct components, and CodePipeline is the orchestrator that connects them: [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)

**1. Source — Bitbucket:** The vprofile source code lives in a Bitbucket repository on the `aws-ci` branch. CodePipeline monitors this branch for commits. When a new commit is detected, it triggers the pipeline. The connection to Bitbucket was established in a previous lecture (via AWS CodeConnections).

**2. Build — CodeBuild:** A CodeBuild project (also created in a previous lecture) reads the buildspec file, executes the build commands (including `sed` commands to inject RDS connection details into `application.properties`), and produces a deployable artifact (a `.war` file).

**3. Deploy — Elastic Beanstalk:** The Beanstalk environment (created in a previous lecture) receives the artifact and deploys it to EC2 instances behind a load balancer. The deployment uses a **rolling update** strategy — with 2 instances and 50% batch size, one instance is updated at a time.

**4. Database — RDS:** The vprofile application connects to RDS using credentials embedded in the `application.properties` file during the build step. The successful login in the application proves the entire chain works. [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)

***

## 1.3 The CodePipeline Creation Options

When creating a pipeline, AWS offers several templates: [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)

* **Deployment** — pre-configured for deployment workflows (push to ECR, deploy to ECS, CloudFormation, Terraform)
* **Continuous Integration** — pre-configured for build/test workflows
* **Automation** — for operational automation
* **Build custom pipeline** — full control over every stage

The instructor selects **Build custom pipeline** because the pipeline needs a specific source (Bitbucket), build (CodeBuild), and deploy (Beanstalk) combination that doesn't match any template. [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)

***

## 1.4 The Service Role Problem — Missing Beanstalk Permissions

When CodePipeline is created, it automatically creates an **IAM service role** — a role that CodePipeline assumes to interact with other AWS services. This role needs permissions for every service in the pipeline: CodeBuild (to trigger builds), CodeConnections (to access Bitbucket), and Beanstalk (to deploy). [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)

The instructor identifies a current issue: **the auto-created role does not include Beanstalk permissions.** The instructor says: "Recently, this role does not create any permission for Beanstalk, or deployment will fail." This means the deployment stage will fail with a permissions error unless you manually add the Beanstalk policy to the role after pipeline creation. [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)

The fix is straightforward: find the role in IAM, attach the `AdministratorAccess-AWSElasticBeanstalk` managed policy. But the instructor deliberately lets the pipeline run first (and stops it before it fails) to demonstrate the awareness and fix workflow — in real operations, you encounter these permission gaps frequently and must know how to diagnose and fix them.

🔍 **Deep Dive:**
The service role's policies after creation include: CodeBuild permissions, CodeConnections permissions, and CodePipeline permissions — but no Beanstalk permissions. Each policy corresponds to one integration. The gap exists because AWS periodically changes what the auto-generated role includes. This is a common AWS pattern: auto-generated roles may not cover all use cases, and you often need to supplement them. The instructor shows two ways to find the role name: from the pipeline creation screen, or from Pipeline → Settings after creation. [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)

***

## 1.5 Event-Driven Triggering — Commits as Pipeline Triggers

CodePipeline monitors the configured source (Bitbucket, `aws-ci` branch) for new commits. When a commit is detected, it's treated as an **event** that automatically triggers the pipeline. No manual intervention is needed — the pipeline runs every time code is pushed. [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)

The instructor demonstrates this at the end of the lecture: making a trivial commit to `README.md` in Bitbucket triggers the pipeline immediately. The instructor notes: "As soon as I made a commit, triggered the pipeline." This is the CI/CD feedback loop in action — code change → automatic build → automatic deploy. [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)

***

## 1.6 Build Failure Debugging — The Sed Command Error

Before creating the pipeline, the instructor tests the CodeBuild project independently and it **fails**. The failure occurs in the **pre-build stage** due to a malformed `sed` command in the buildspec file. [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)

The error message: `"sed -e expression, unterminated s command."` The `sed` substitution command requires three forward slashes as delimiters: `s/search/replace/`. The buildspec file was missing the final forward slash, so `sed` couldn't determine where the replacement string ended — it's an "unterminated" command. [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)

The instructor's debugging approach:

1. Check **Phase Details** first (not build logs — the logs can hang the browser)
2. If the phase shows failure, then go to **Build Logs**
3. Click **Tail Logs** to jump to the end of the log
4. Look for the error message and trace back to where it started
5. Identify the problematic command
6. Fix it in the build project settings (Edit → update the buildspec)
7. Run the build again to verify the fix [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)

This is a universal debugging pattern: check the phase summary first (fast, high-level), then drill into logs only when needed (detailed, slower). Don't start with the full logs — they can be overwhelming and slow to load.

***

## 1.7 Rolling Deployment in Beanstalk

When the pipeline deploys to Beanstalk, the deployment uses a **rolling update** strategy. The Beanstalk environment has 2 instances and the batch size is 50% (configured during Beanstalk creation). This means: deploy to 1 instance first (batch 1: 1 out of 2), verify it's healthy, then deploy to the second instance. [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)

The instructor observes in the Beanstalk console: "Batch 1: Starting application deployment command." This rolling approach ensures that at least one instance is always serving traffic during the deployment — there's no full outage. If the deployment to the first instance fails, the second instance is still running the old version. [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)

***

## 1.8 Proving the Deployment — Login Validates the Full Chain

After deployment, the instructor accesses the Beanstalk environment URL, which redirects to the load balancer. The vprofile application login page appears. Logging in with `admin_vp` / `admin_vp` **succeeds**, which proves: [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)

1. The artifact was built correctly (CodeBuild)
2. The artifact was deployed to Beanstalk (CodePipeline deploy stage)
3. The application started successfully (Beanstalk/Tomcat)
4. The `application.properties` file contains correct RDS connection details (the `sed` commands worked)
5. The application connected to RDS successfully (the login query hit the database)

The instructor notes: "We don't have RabbitMQ and Memcached or Elasticsearch, anything. We just wanted to prove the CodePipeline deployment." The scope is intentionally limited — the goal is proving the CI/CD chain, not running a full production stack. [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)

***

## 1.9 Cleanup Order — Dependency-Aware Deletion

The cleanup has a specific order driven by **resource dependencies**: [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)

**The critical dependency:** The RDS security group has a rule referencing the Beanstalk security group. If you try to delete the Beanstalk environment without first removing this rule, the deletion fails because AWS won't delete a security group that is referenced by another security group's rules. The instructor explicitly warns: "When you try to delete the Beanstalk environment, it's going to fail because it will say that the security group is referred somewhere else and it will stop the deletion process." [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)

This is the **reverse** of the temporal dependency pattern seen during creation: during creation, you couldn't add the cross-reference rule until both SGs existed; during deletion, you must **remove** the cross-reference rule before deleting either SG.

The instructor also notes that some resources (like the CodeBuild project and Bitbucket repository) don't cost money when idle — "As long as you don't run the build, it's not going to have any charge." You can keep them for convenience since recreation is more effort than the zero-cost storage. [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

## What We Are Building

We are creating an end-to-end CI/CD pipeline using AWS CodePipeline that automatically: detects code changes in Bitbucket → builds the artifact using CodeBuild → deploys the artifact to Elastic Beanstalk. After this, every commit to the `aws-ci` branch in Bitbucket automatically triggers a full build and deployment cycle. [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)

***

## Step 1: Test the CodeBuild Project (Expect Failure)

Go to **CodeBuild** in the AWS console. Open the build project created in the previous lecture.

Click **Start Build**.

Immediately click **Phase Details** — do NOT stay on Build Logs (large log output can hang the browser). [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)

**Wait for the build to complete.** It will **fail** in the **pre-build stage**.

**Diagnose the failure:**

1. Click **Build Logs** (now that the build is complete, the logs won't stream endlessly)
2. Click **Tail Logs** to jump to the end
3. Find the error: `sed -e expression, unterminated s command`
4. This means a `sed` substitution command in the buildspec file is missing the closing forward slash delimiter [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)

**The sed command structure:**

```
sed s/SEARCH/REPLACE/
      ↑      ↑       ↑
   delimiter delimiter delimiter (3 forward slashes required)
```

The buildspec file is missing the final `/`. The `sed` command can't determine where the replacement string ends.

***

## Step 2: Fix the Buildspec File

Go back to the build project. Click **Edit**.

Navigate to the **buildspec** section. Find the malformed `sed` command. Add the missing forward slash `/` at the end of the substitution. [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)

Click **Update Project**.

***

## Step 3: Re-run the Build (Verify Fix)

Click **Start Build** again. Click **Phase Details** and wait.

**Expected result:** `BUILD SUCCEEDED` — all phases complete successfully. [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)

**Connection to the flow:** The build project is now verified and ready to be integrated into the pipeline.

***

## Step 4: Create the CodePipeline

Navigate to **CodePipeline** (search in the AWS console or find it under Developer Tools → Pipeline → Pipelines).

Click **Create Pipeline**. [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)

**Choose Creation Options:** Select **Build custom pipeline** → click **Next**.

**Pipeline settings:**

| Setting       | Value                             |
| ------------- | --------------------------------- |
| Pipeline name | `vprocicdpipeline`                |
| Service role  | New service role (auto-generated) |

**⚠️ Important:** Copy the service role name displayed on this page — you'll need it later to add Beanstalk permissions. [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)

Click **Next**.

***

## Step 5: Configure the Source Stage

| Setting         | Value                                                        |
| --------------- | ------------------------------------------------------------ |
| Source provider | Bitbucket (via the connection created in a previous lecture) |
| Connection      | Select the existing connection name                          |
| Repository      | Select the vprofile repository                               |
| Branch          | `aws-ci`                                                     |
| Trigger         | Code change detected as event → triggers pipeline            |

Click **Next**. [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)

***

## Step 6: Configure the Build Stage

Click **Other build providers** (not the inline command option).

| Setting        | Value                                                   |
| -------------- | ------------------------------------------------------- |
| Build provider | AWS CodeBuild                                           |
| Project name   | Select the CodeBuild project (created and tested above) |
| Build type     | Single build                                            |

Other options visible: ECR and Jenkins — CodePipeline can integrate with Jenkins as a build provider, showing the tool interoperability. [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)

Click **Next**.

***

## Step 7: Skip the Test Stage

The test stage is optional. You can select a CodeBuild project for testing, code analysis, or other quality checks. The instructor has no test project configured.

Click **Skip** / **Next** to proceed without a test stage. [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)

***

## Step 8: Configure the Deploy Stage

| Setting         | Value                                     |
| --------------- | ----------------------------------------- |
| Deploy provider | AWS Elastic Beanstalk                     |
| Application     | Select the vprofile Beanstalk application |
| Environment     | Select the Beanstalk environment          |

Click **Next**. [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)

***

## Step 9: Review and Create

Review all stages. If everything looks correct, click **Create Pipeline**.

**Immediately after creation:** The pipeline auto-triggers and starts executing. [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)

**Stop the execution** (it will fail at the deploy stage due to missing Beanstalk permissions):

Click **Stop execution** → select the in-progress execution → click **Stop**. [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)

***

## Step 10: Fix the IAM Service Role — Add Beanstalk Permissions

Go to **IAM → Roles**.

**Find the role:** Search for the role name you copied in Step 4. If you didn't copy it, go to CodePipeline → your pipeline → **Settings** — the role name is listed there. [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)

Click on the role. You'll see existing policies:

* CodeBuild permissions ✓
* CodeConnections permissions ✓
* CodePipeline permissions ✓
* **Beanstalk permissions ✗** (missing)

Click the **Add permissions** dropdown → **Attach policies**.

Search for `Beanstalk`. Select **`AdministratorAccess-AWSElasticBeanstalk`**. Click **Add Permission**. [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)

***

## Step 11: Trigger the Pipeline

Go back to **CodePipeline → your pipeline**.

Click **Release Change** → **Release**.

If you encounter an error on the page, open CodePipeline from a fresh browser tab. [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)

**Monitor the pipeline stages:**

1. **Source stage:** Fetches code from Bitbucket (`aws-ci` branch) — completes quickly
2. **Build stage:** CodeBuild executes the buildspec — takes a few minutes
3. **Deploy stage:** Beanstalk receives the artifact and starts deployment [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)

**In the Beanstalk console:** You'll see "Batch 1: Starting application deployment command" — the rolling deployment updating one instance at a time (2 instances, 50% batch = 1 instance per batch).

**Wait for deployment to complete.** The instructor pauses recording and resumes when done. [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)

***

## Step 12: Verify the Deployment

Go to the **Beanstalk environment** → click the environment **URL**.

The vprofile application login page should appear. [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)

**Login credentials:**

* Username: `admin_vp`
* Password: `admin_vp`

**Successful login proves:**

* Artifact built correctly (CodeBuild)
* Deployed to Beanstalk (CodePipeline)
* `application.properties` has correct RDS connection info (sed commands worked)
* Application connected to RDS (login query succeeded) [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)

***

## Step 13: Test the Automatic Trigger — Commit to Bitbucket

Go to **Bitbucket** → navigate to the `aws-ci` branch.

Open `README.md` → click **Edit**. [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)

Make a trivial change (add or remove a character in the second line). Enter a commit message. Click **Commit**.

**Go to CodePipeline immediately.** The pipeline should already be triggered — the source stage starts automatically in response to the commit event. [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)

The pipeline proceeds through source → build → deploy automatically. This confirms the event-driven CI/CD loop is working.

***

## Step 14: Cleanup

**Cleanup order matters due to security group cross-references.** [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)

**1. Delete RDS:**

* Go to **RDS** → select your database → **Actions → Delete**
* **Uncheck** "Create final snapshot"
* Check "I acknowledge"
* Type `delete me` → click **Delete**

**2. Remove the cross-reference security group rule:**

* Go to **EC2 → Security Groups** → find the RDS security group
* **Edit inbound rules** → remove the rule that references the Beanstalk security group
* **Save rules**
* **Why:** If this rule remains, Beanstalk deletion will fail because its security group is still referenced [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)

**3. Delete Beanstalk:**

* Go to **Elastic Beanstalk → Applications** → select your application
* **Actions → Delete application**
* This deletes the environment first (instances, load balancer, security groups), then the application

**4. Delete CodePipeline:**

* Go to **CodePipeline** → select your pipeline → **Delete Pipeline** → confirm

**5. Delete CodeBuild (optional — no charges when idle):**

* Go to **CodeBuild** → select the build project → delete
* The instructor notes: "As long as you don't run the build, it's not going to have any charge." You can keep it since you have the buildspec file and can recreate it quickly. [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)

**6. Keep Bitbucket repository** — useful for future recreation of the pipeline.

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

## Full Pipeline Architecture

```
BITBUCKET (aws-ci branch)
  │ commit detected (event trigger)
  ▼
[CodePipeline — orchestrator]
  │
  ├── SOURCE STAGE: fetch code from Bitbucket
  │
  ├── BUILD STAGE: CodeBuild
  │     → reads buildspec file
  │     → sed injects RDS connection details
  │     → mvn builds artifact (.war)
  │
  ├── (TEST STAGE: skipped — optional CodeBuild/other)
  │
  └── DEPLOY STAGE: Elastic Beanstalk
        → rolling update (50% batch = 1 of 2 instances)
        → application connects to RDS
```

## CodePipeline = AWS-Native Jenkins

```
Jenkins pipeline stages    ↔  CodePipeline stages
Jenkins plugins            ↔  AWS service integrations
Jenkinsfile                ↔  Pipeline configuration (console/CLI)
Jenkins SCM polling/webhook ↔  Bitbucket event trigger

"Once you know how to do CI/CD from Jenkins,
 you can do CI/CD from any other tool, any other cloud."
```

## Pipeline Creation Flow

```
1. Choose: Build custom pipeline
2. Name + service role (auto-created — COPY ROLE NAME)
3. Source: Bitbucket → connection → repo → branch (aws-ci)
4. Build: Other providers → CodeBuild → select project
5. Test: skip (optional)
6. Deploy: Elastic Beanstalk → application → environment
7. Review → Create Pipeline
8. STOP execution immediately
9. Fix IAM role → add Beanstalk permissions
10. Release Change → full pipeline runs
```

## Service Role Permission Gap

```
Auto-created role includes:
  ✓ CodeBuild
  ✓ CodeConnections
  ✓ CodePipeline
  ✗ Beanstalk (MISSING — deploy will fail)

FIX:
  IAM → Roles → find role name → Attach policies
  → AdministratorAccess-AWSElasticBeanstalk

Find role name:
  Option 1: copy during creation
  Option 2: Pipeline → Settings → role name shown
```

## Build Failure Debugging Flow

```
Start Build → Phase Details (NOT build logs — browser may hang)
  ↓
Phase shows failure (pre-build)
  ↓
Build Logs → Tail Logs (jump to end)
  ↓
Find error: "sed -e expression, unterminated s command"
  ↓
Root cause: missing trailing / in sed substitution
  sed s/SEARCH/REPLACE/  ← needs 3 delimiters
  sed s/SEARCH/REPLACE   ← broken (unterminated)
  ↓
Fix: Edit build project → update buildspec → add /
  ↓
Re-run build → SUCCESS
```

## Deployment Verification Chain

```
Beanstalk URL → login page appears → login succeeds
                                        ↓
Proves: artifact built ✓
        deployed to Beanstalk ✓
        application.properties correct (sed worked) ✓
        RDS connection works ✓
```

## Event-Driven Trigger

```
Commit to aws-ci branch (even README.md change)
  → Bitbucket event detected by CodePipeline
    → Pipeline auto-triggers
      → Source → Build → Deploy (fully automatic)

No manual intervention needed after pipeline creation
```

## Rolling Deployment (Beanstalk)

```
2 instances, 50% batch
  → Batch 1: deploy to instance 1 (instance 2 serves traffic)
  → Verify healthy
  → Batch 2: deploy to instance 2
  → Both instances on new version

Zero-downtime deployment
```

## Cleanup Order (Dependency-Aware)

```
1. RDS → delete (uncheck snapshot, acknowledge)
2. RDS SG → REMOVE rule referencing Beanstalk SG
     ↑ CRITICAL: if skipped → Beanstalk deletion FAILS
     "security group is referred somewhere else"
3. Beanstalk → delete application (deletes environment + app)
4. CodePipeline → delete
5. CodeBuild → optional (no charges when idle)
6. Bitbucket repo → KEEP (free, useful for recreation)

Reverse of creation temporal dependency:
  Creation: can't add cross-ref until both SGs exist
  Deletion: must REMOVE cross-ref before deleting either SG
```

## Pipeline Creation Options

```
Deployment:     push to ECR, deploy to ECS/CloudFormation/Terraform
CI:             build tools
Automation:     operational workflows
Custom: ★      full control over source/build/test/deploy
```

## Build Stage Provider Options

```
CodeBuild (AWS native)
Jenkins (external)
ECR (container image push)
```

## Resources — Cost vs. Free When Idle

```
COSTS MONEY (running):
  RDS, Beanstalk (EC2 + LB), NAT gateway, Elastic IP

NO CHARGE (idle):
  CodeBuild project (only charges per build minute)
  CodePipeline (charges per active pipeline per month — minimal)
  Bitbucket repository (free tier)
```

## Reusable Engineering Patterns

**1. Orchestrator Connects Independent Services**

```
CodePipeline doesn't build or deploy — it ORCHESTRATES
  Source service (Bitbucket) → provides code
  Build service (CodeBuild) → produces artifact
  Deploy service (Beanstalk) → runs artifact

Same pattern: Jenkins pipeline, GitLab CI, GitHub Actions
The orchestrator's value = connecting stages + triggering flow
```

**2. Auto-Generated Roles Need Manual Completion**

```
AWS auto-creates service roles with partial permissions
Newer integrations may not be included
ALWAYS verify role permissions match all pipeline stages

Pattern: trust-but-verify on auto-generated configurations
Same in: CloudFormation-generated roles, Terraform default policies
```

**3. Test Before Integrating**

```
Test CodeBuild independently → verify it works
THEN integrate into CodePipeline

Pattern: validate each component in isolation
         before wiring them into a pipeline
Same in: unit test before integration test, 
         test Ansible role before adding to playbook
```

**4. Cross-Reference Cleanup = Reverse of Creation**

```
Creation: create A → create B → add rule A→B
Deletion: remove rule A→B → delete B → delete A

Forgetting to remove cross-references → deletion blocked
Same pattern: any system with referential integrity
  (security groups, DNS records, IAM role attachments)
```

***

*This completes the full reconstruction. Theory explains CodePipeline's role as an orchestrator, the service role permission gap, and the event-driven trigger model. Practical walks through every step from build debugging to pipeline creation to cleanup. The Compression Map enables instant recall of the full pipeline architecture, the permission fix workflow, and the dependency-aware cleanup order.* [\[287-build-...e-pipeline \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/287-build-deploy-and-code-pipeline.txt)
