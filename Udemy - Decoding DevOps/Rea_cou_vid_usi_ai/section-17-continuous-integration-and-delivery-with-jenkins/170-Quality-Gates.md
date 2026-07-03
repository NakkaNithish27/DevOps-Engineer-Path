# 🎓 SonarQube Quality Gates — Deep Learning Material

*Reconstructed from video lecture #170 and its accompanying pipeline resource*

***

## 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

### 1. What Is a Quality Gate?

A **Quality Gate** is a set of rules (conditions) that you define in SonarQube to determine whether your code meets the minimum acceptable quality standard before it can proceed further in the pipeline. Think of it as a checkpoint — your code analysis results are measured against the thresholds you configure, and the gate either **passes** or **fails** based on whether your code stays within those boundaries. [\[170.-Quality-Gates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.-Quality-Gates.txt)

The core idea is **tolerance thresholds**. Every project has a different appetite for risk. Some projects may tolerate a few security issues during early development; others (e.g., banking, healthcare) may tolerate zero. A quality gate lets you encode that tolerance into an automated, enforceable rule. You define exactly how many security issues, reliability issues, or other code quality violations are acceptable. If the code analysis results exceed any of those thresholds, the quality gate fails. [\[170.-Quality-Gates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.-Quality-Gates.txt)

This is critical in CI/CD because without a quality gate, SonarQube merely *reports* issues — it doesn't *block* anything. The pipeline would happily continue deploying code riddled with vulnerabilities. The quality gate is the mechanism that transforms SonarQube from a passive reporting tool into an active gatekeeper. [\[170.-Quality-Gates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.-Quality-Gates.txt)

> 🔍 **Deep Dive (Optional)**
>
> SonarQube evaluates quality gates on two scopes: **Overall Code** (the entire codebase) and **New Code** (only the code changed since a defined baseline). When you add a condition, you choose which scope it applies to. In this video, the condition is added on "overall code," meaning the entire project's security issues are counted — not just those introduced in the latest commit. This distinction matters in real projects where you inherit legacy code with pre-existing issues. [\[170.-Quality-Gates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.-Quality-Gates.txt)

***

### 2. Default Quality Gate: Sonar Way

Every SonarQube installation ships with a built-in quality gate called **Sonar Way**. When you create a project, it automatically uses this default gate. Sonar Way comes with a pre-configured set of conditions that SonarQube considers best practice. [\[170.-Quality-Gates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.-Quality-Gates.txt)

If you go to any project's settings and click on **Quality Gate**, it will display which gate is currently active. By default, it reads: *"Use the Sonar Way built-in Quality Gate."* You don't have to stay with this default — you can create custom quality gates and assign them per project. [\[170.-Quality-Gates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.-Quality-Gates.txt)

> ⚠️ **Expert Note (Optional)**
>
> In production environments, teams almost always create custom quality gates tailored to their project's compliance and risk requirements. The Sonar Way default is a reasonable starting point, but it may be too lenient or too strict depending on your organization's standards. The video explicitly notes that understanding all the available Sonar rules in depth is outside the scope of this course and depends on your specific job requirements — but knowing *how* to create, configure, and assign quality gates is essential. [\[170.-Quality-Gates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.-Quality-Gates.txt)

***

### 3. Custom Quality Gates — Creation and Conditions

You can create your own quality gate by navigating to **Quality Gates** in the SonarQube UI and clicking **Create**. You give it a name (in this video: `vprofile-qg`), and SonarQube initializes it with some default rules and values. You can then remove all the defaults and add your own conditions from scratch. [\[170.-Quality-Gates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.-Quality-Gates.txt)

A condition follows this logic: **"Quality Gate fails when \[metric] is \[operator] \[value]."** For example: *"Quality Gate fails when security issues is greater than 2."* This means if SonarQube detects 3 or more security issues in the overall code, the gate fails. [\[170.-Quality-Gates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.-Quality-Gates.txt)

After creating the gate, you must **assign** it to your project. Go to the project → Quality Gate → select your custom gate → Save. Until you do this, the project still uses the default Sonar Way. [\[170.-Quality-Gates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.-Quality-Gates.txt)

***

### 4. Quality Gate Integration in the Pipeline — The Missing Link

Here is a crucial concept that many beginners miss: **setting a quality gate in SonarQube alone does nothing to your Jenkins pipeline**. By default, the pipeline's Sonar analysis stage simply uploads the scan results to the SonarQube server. It does not check whether the quality gate passed or failed. The pipeline will succeed regardless of code quality. [\[170.-Quality-Gates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.-Quality-Gates.txt)

To make the pipeline **react** to the quality gate result, you need an additional stage in your Jenkinsfile — the **Quality Gate stage**. This stage uses the `waitForQualityGate` step, which pauses the pipeline and polls SonarQube for the quality gate verdict. The parameter `abortPipeline: true` means that if the quality gate fails, the entire pipeline is aborted (marked as failed). [\[170.-Quality-Gates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.-Quality-Gates.txt), [\[170. PAAC_...alityGates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.%20PAAC_SonarQualityGates.txt)

The stage is wrapped in a `timeout` block (set to 1 hour in this case) to prevent the pipeline from hanging indefinitely if SonarQube is unreachable or slow to respond. [\[170. PAAC_...alityGates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.%20PAAC_SonarQualityGates.txt)

```groovy
stage("Quality Gate") {
    steps {
        timeout(time: 1, unit: 'HOURS') {
            waitForQualityGate abortPipeline: true
        }
    }
}
```

 [\[170. PAAC_...alityGates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.%20PAAC_SonarQualityGates.txt)

> 🔍 **Deep Dive (Optional)**
>
> The `waitForQualityGate` step works asynchronously. When the Sonar analysis stage completes, the results are uploaded to SonarQube, which then processes them in the background. The quality gate evaluation is not instant — SonarQube needs to finish its server-side computation. The `waitForQualityGate` step polls the SonarQube API repeatedly until a result is available or the timeout is reached. This is why the timeout is important: without it, a SonarQube outage would lock your pipeline forever. [\[170.-Quality-Gates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.-Quality-Gates.txt), [\[170. PAAC_...alityGates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.%20PAAC_SonarQualityGates.txt)

***

### 5. Webhooks — How SonarQube Talks Back to Jenkins

This is the second piece of the puzzle that makes quality gate integration work. When the Sonar analysis is complete and the quality gate has been evaluated, SonarQube needs to **notify Jenkins** of the result. But how does SonarQube know where Jenkins is? The answer is **webhooks**. [\[170.-Quality-Gates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.-Quality-Gates.txt)

A webhook is a callback URL — you tell SonarQube: "When you have a quality gate result, send an HTTP POST to this URL." The URL format for Jenkins is:

    http://<Jenkins-Private-IP>:8080/sonarqube-webhook

The `/sonarqube-webhook` path is a specific endpoint exposed by the SonarQube plugin on Jenkins. It must be typed exactly — no trailing slash, no spelling variations. [\[170.-Quality-Gates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.-Quality-Gates.txt)

You configure this in SonarQube under **Project Settings → Webhooks → Create**. You give it a name (e.g., `jenkins-ci-webhook`) and provide the URL. [\[170.-Quality-Gates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.-Quality-Gates.txt)

> ⚠️ **Expert Note (Optional)**
>
> The webhook uses Jenkins' **private IP**, not the public one. This is because in a typical AWS setup, both Jenkins and SonarQube are in the same VPC, and internal communication should happen over the private network for security and cost reasons. If you use the public IP, it may work but introduces unnecessary network hops and potential security exposure. The video specifically says "Jenkins private IP" — follow this guidance. [\[170.-Quality-Gates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.-Quality-Gates.txt)

***

### 6. Security Group Configuration — Allowing the Webhook Traffic

Even after configuring the webhook URL, the HTTP request from SonarQube to Jenkins can be blocked at the network level if the AWS Security Group rules don't allow it. Jenkins must allow **inbound traffic on port 8080** from the **SonarQube Security Group**. [\[170.-Quality-Gates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.-Quality-Gates.txt)

This was already configured in a previous lecture, but the video emphasizes **verifying** it again before testing. You go to the Jenkins Security Group → Edit Inbound Rules → confirm that port 8080 is open and the source is specifically the SonarQube Security Group (not `0.0.0.0/0`). [\[170.-Quality-Gates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.-Quality-Gates.txt)

> 🔍 **Deep Dive (Optional)**
>
> Using Security Group references (instead of IP addresses) as sources in AWS inbound rules is a best practice. It means "allow traffic from any instance that belongs to this security group." This is dynamic — if SonarQube's IP changes (e.g., after a reboot), the rule still works because it's tied to the group membership, not a static IP. [\[170.-Quality-Gates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.-Quality-Gates.txt)

***

### 7. Quality Gate Pass vs. Fail — Interpreting Results

When the quality gate **fails**, the Jenkins pipeline stage shows an error. Clicking into it reveals the message: *"the quality gate is error"* — this means the pipeline was aborted due to quality gate failure. On the SonarQube side, the project page shows **Failed** with a breakdown of which condition was violated. In this video, the project had **3 security issues**, which exceeded the threshold of **2**, causing the failure. [\[170.-Quality-Gates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.-Quality-Gates.txt)

When the quality gate **passes**, the pipeline continues to the next stages normally. The SonarQube project page shows **Passed**. [\[170.-Quality-Gates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.-Quality-Gates.txt)

***

## ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

### What We Are Building

We are adding **quality gate enforcement** to an existing Jenkins CI pipeline for the **vprofile** project. The pipeline already fetches code from GitHub, builds it with Maven, runs unit tests, performs Checkstyle analysis, and uploads a SonarQube code scan. What it does **not** do yet is check whether the code *passes* the quality gate. We are going to: [\[170.-Quality-Gates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.-Quality-Gates.txt)

1.  Create a custom quality gate in SonarQube with a deliberately tight rule (to force a failure).
2.  Assign it to the vprofile project.
3.  Add a Quality Gate stage to the Jenkins pipeline.
4.  Set up a webhook so SonarQube can report results back to Jenkins.
5.  Verify the security group allows the webhook traffic.
6.  Run the pipeline and observe the failure.
7.  Reset the quality gate so the pipeline passes for future lectures.

The final outcome: a pipeline that **automatically aborts** if code quality doesn't meet the defined standards. [\[170.-Quality-Gates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.-Quality-Gates.txt)

***

### Step 1: Check the Current Quality Gate Assignment

Navigate to your **vprofile project** in SonarQube. Go to **Project Settings → Quality Gate**. You will see it currently says *"Use the Sonar Way built-in Quality Gate."* This confirms the project is using the default gate, and no custom gate has been assigned yet. [\[170.-Quality-Gates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.-Quality-Gates.txt)

***

### Step 2: Create a Custom Quality Gate

Go to the top-level **Quality Gates** page in SonarQube (not inside a project — this is a global setting). Click **Create**. Enter the name:

    vprofile-qg

(The video uses uppercase `QG`-style naming.) Click **Create**. SonarQube will populate the new gate with some default rules and values. **Remove all of them** — we want to start clean and add only the condition we need for this exercise. [\[170.-Quality-Gates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.-Quality-Gates.txt)

***

### Step 3: Add a Custom Condition

Before adding a condition, you need to know what threshold to set. Go back to the **vprofile project** overview. Look at the **Security** section under Open Issues — you'll see **3 security issues** currently exist. [\[170.-Quality-Gates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.-Quality-Gates.txt)

Now go back to **Quality Gates → vprofile-qg**. Click **Add Condition** on **Overall Code**. Configure it as:

*   **Quality Gate fails when:** Security Issues
*   **Operator:** is greater than
*   **Value:** `2`

Click **Add Condition**. [\[170.-Quality-Gates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.-Quality-Gates.txt)

This means: if there are more than 2 security issues, the gate fails. Since the project currently has 3, this will **deliberately trigger a failure** — which is exactly what we want for testing. [\[170.-Quality-Gates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.-Quality-Gates.txt)

***

### Step 4: Assign the Custom Quality Gate to the Project

Go to the **vprofile project → Project Settings → Quality Gate**. From the dropdown, select **vprofile-qg** (your custom gate). Click **Save**. The project is now governed by your custom rule instead of Sonar Way. [\[170.-Quality-Gates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.-Quality-Gates.txt)

***

### Step 5: Add the Quality Gate Stage to the Pipeline Script

Open the Jenkins pipeline configuration. The existing pipeline ends after the **Sonar Code analysis** stage. You need to add a new stage **after** it. The stage comes from the SonarQube documentation (the same source used in the previous lecture for the Sonar scanner configuration). [\[170.-Quality-Gates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.-Quality-Gates.txt)

Here is the complete stage to add:

```groovy
stage("Quality Gate") {
    steps {
        timeout(time: 1, unit: 'HOURS') {
            // Parameter indicates whether to set pipeline to UNSTABLE if Quality Gate fails
            // true = set pipeline to UNSTABLE, false = don't
            waitForQualityGate abortPipeline: true
        }
    }
}
```

 [\[170. PAAC_...alityGates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.%20PAAC_SonarQualityGates.txt)

**Breakdown of every part:**

*   `stage("Quality Gate")` — declares a new pipeline stage named "Quality Gate." This name appears in the Jenkins stage view.
*   `steps { ... }` — the block containing the actual actions for this stage.
*   `timeout(time: 1, unit: 'HOURS')` — wraps the quality gate check in a 1-hour timeout. If SonarQube doesn't respond within an hour, the pipeline fails gracefully instead of hanging.
*   `waitForQualityGate abortPipeline: true` — the core step. It polls SonarQube for the quality gate result. If the gate status is "ERROR" (failed), and `abortPipeline` is `true`, the pipeline is aborted. If you set it to `false`, the pipeline would be marked UNSTABLE but would continue. [\[170.-Quality-Gates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.-Quality-Gates.txt), [\[170. PAAC_...alityGates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.%20PAAC_SonarQualityGates.txt)

**Placement in the pipeline:** This stage must go **after** the Sonar Code analysis stage and **before** the closing braces of `stages` and `pipeline`. The video emphasizes checking your brace structure carefully:

*   The innermost `}` closes `timeout`
*   The next `}` closes `steps`
*   The next `}` closes the `stage`
*   After that, you should see only **two** closing braces: one for `stages` and one for `pipeline` [\[170.-Quality-Gates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.-Quality-Gates.txt)

The complete pipeline with all stages (from the resource file) looks like this:

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
    }
}
```

 [\[170. PAAC_...alityGates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.%20PAAC_SonarQualityGates.txt)

> ⚠️ **Expert Note (Optional)**
>
> The video instructor notes: *"Hopefully there are no syntax errors because I have not checked it against any tool."* In real work, always validate your Jenkinsfile syntax before committing. Jenkins provides a Pipeline Linter (`/pipeline-model-converter/validate` endpoint), and many IDEs have Groovy/Jenkinsfile linting plugins. A single misplaced brace can fail the entire pipeline at parse time. If you have any doubts, the instructor recommends downloading the lecture resource file and using the pre-written pipeline. [\[170.-Quality-Gates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.-Quality-Gates.txt)

***

### Step 6: Configure the Webhook in SonarQube

This step is essential — without it, the `waitForQualityGate` step will time out because SonarQube has no way to notify Jenkins of the result.

In SonarQube, go to **Project Settings → Webhooks** (for the vprofile project). Click **Create**. [\[170.-Quality-Gates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.-Quality-Gates.txt)

Fill in:

*   **Name:** `jenkins-ci-webhook`
*   **URL:** `http://<Jenkins-Private-IP>:8080/sonarqube-webhook`

To get the Jenkins Private IP: go to your **AWS Console → EC2 → select the Jenkins instance → copy its Private IPv4 address**. Paste it into the URL in place of `<Jenkins-Private-IP>`. [\[170.-Quality-Gates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.-Quality-Gates.txt)

**Critical details about the URL:**

*   Must start with `http://` (not `https://` unless you've configured SSL on Jenkins)
*   Port is `8080` (Jenkins' default port)
*   The path `/sonarqube-webhook` must be spelled exactly — no trailing forward slash, no typos
*   This is the endpoint the SonarQube Jenkins plugin exposes to receive webhook callbacks [\[170.-Quality-Gates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.-Quality-Gates.txt)

Click **Create** to save the webhook.

***

### Step 7: Verify Security Group Rules in AWS

Go to the **AWS Console → EC2 → Security Groups → Jenkins Security Group → Inbound Rules → Edit**. Confirm there is a rule that allows:

*   **Port:** 8080
*   **Source:** The SonarQube Security Group

Search for the SonarQube Security Group by name to verify it's the correct one. If the rule exists and points to the right source, no changes are needed — just close. The video confirms: *"I don't need to save anything because it was already as a test."* [\[170.-Quality-Gates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.-Quality-Gates.txt)

***

### Step 8: Run the Pipeline and Observe Failure

Go to the Jenkins job → **Configure**. Select all the existing pipeline script, delete it, and paste the new pipeline (with the Quality Gate stage included). Click **Save**. Click **Build Now**. [\[170.-Quality-Gates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.-Quality-Gates.txt)

Go to **Stages** view to watch progress. The pipeline will proceed through Fetch code → Build → Unit Test → Checkstyle → Sonar Code analysis → **Quality Gate**. At the Quality Gate stage, it will pause while waiting for SonarQube's verdict. [\[170.-Quality-Gates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.-Quality-Gates.txt)

**Expected result:** The pipeline **fails**. Click on the failed Quality Gate stage. The log shows: *"the quality gate is error"* — meaning the quality gate condition was violated, and the pipeline was aborted as configured. [\[170.-Quality-Gates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.-Quality-Gates.txt)

**Verification on SonarQube:** Go to **Projects → vprofile**. The project status should show **Failed** (refresh if needed). Under **Overall Code**, it shows **1 fail** — specifically, **3 security issues is greater than 2**, which matches the condition we set. [\[170.-Quality-Gates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.-Quality-Gates.txt)

This confirms the entire chain works: pipeline uploads results → SonarQube evaluates the quality gate → SonarQube notifies Jenkins via webhook → Jenkins aborts the pipeline. [\[170.-Quality-Gates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.-Quality-Gates.txt)

***

### Step 9: Reset the Quality Gate (Important for Continuation)

If you leave the custom quality gate active, the pipeline will **always fail** for subsequent lectures. You have two options: [\[170.-Quality-Gates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.-Quality-Gates.txt)

**Option A — Switch back to the default gate:**
Go to **Projects → vprofile → Quality Gate** → select **Sonar Way** (the default) → **Save**.

**Option B — Relax the threshold:**
Go to **Quality Gates → vprofile-qg** → change the security issues threshold from `2` to `5` (or any number higher than the current 3 issues). Since 3 is less than 5, the gate will pass. [\[170.-Quality-Gates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.-Quality-Gates.txt)

After making either change, go back to Jenkins and click **Build Now** again. **Verify the pipeline passes successfully** — this is critical for the next lectures in the course. [\[170.-Quality-Gates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.-Quality-Gates.txt)

***

### How It All Connects

Here is the complete flow, end to end:

    Jenkins Pipeline starts
        → Fetches code from GitHub
        → Builds with Maven
        → Runs Unit Tests
        → Runs Checkstyle
        → Sonar Scanner uploads results to SonarQube Server
        → Quality Gate stage: Jenkins waits (polls SonarQube)
            → SonarQube evaluates quality gate conditions
            → SonarQube sends result to Jenkins via webhook
        → If PASS → pipeline continues
        → If FAIL → pipeline aborts (abortPipeline: true)

The quality gate is the enforcement point where **code quality standards meet automation**. Without it, code analysis is informational. With it, code analysis becomes a hard gate that blocks bad code from progressing through your CI/CD pipeline. [\[170.-Quality-Gates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.-Quality-Gates.txt), [\[170. PAAC_...alityGates \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/170.%20PAAC_SonarQualityGates.txt)

***

Want me to save this as a downloadable Markdown file?
