# 🎓 Deep Learning Material: Security Code Scanning & Artifacts in GitLab CI/CD

**Source:** [198-security-and-artifacts.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198-security-and-artifacts.txt?EntityRepresentationId=9fa3c12d-738c-4ccf-a09b-1627f2e110b0) (video caption) + [198.SecurityScan.yml](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198.SecurityScan.yml?EntityRepresentationId=9631d37b-4b7e-4483-b1c3-083970ae4e9a) (pipeline configuration) — Video lecture covering security code scanning using Trivy in a GitLab CI/CD pipeline, the Docker entrypoint problem with tool-specific images, saving build and scan outputs as artifacts, parallel job execution via `needs`, quality gates with exit codes, and a failure notification stage. [\[198-securi...-artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198-security-and-artifacts.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198.SecurityScan.yml)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 Why Security Code Scanning Exists in a Pipeline

Before you publish an artifact — before your compiled application goes anywhere near production — there must be a stage that examines your code and its dependencies for known security vulnerabilities. This is not optional in professional environments. If your source code contains patterns like SQL injection, cross-site scripting (XSS), or insecure function calls, those are flaws **in your code**. If your application depends on open-source libraries (pulled in via Maven, npm, pip, etc.) that have known CVEs (Common Vulnerabilities and Exposures), those are flaws **in your supply chain**. Both categories can be caught automatically by scanning tools before the artifact is ever built or deployed. [\[198-securi...-artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198-security-and-artifacts.txt)

The video introduces two distinct categories of scanning. **SAST (Static Application Security Testing)** scans your actual source code for security issues — it reads the code without executing it and looks for dangerous patterns. **SCA (Software Composition Analysis)** scans your open-source dependencies for known vulnerabilities — it checks the libraries you import against vulnerability databases. Some tools do one, some do both, and some extend further into container images and infrastructure-as-code. [\[198-securi...-artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198-security-and-artifacts.txt)

***

## 1.2 The Tool Landscape

The video lists several tools to give context for what exists in the market:

* **Snyk** — Can do both SAST and SCA. Scans source code and open-source dependencies for security vulnerabilities.
* **SonarQube / SonarCloud** — Primarily for code quality analysis, but also includes security scanning capabilities. The instructor references using SonarQube with proper quality gates in a separate DevOps projects course.
* **Semgrep** — A lightweight SAST tool focused on pattern-matching in source code.
* **Trivy** — Very popular in container environments. Scans container images, file systems (source code), and infrastructure-as-code (Terraform, CloudFormation, Kubernetes manifests, Helm charts). [\[198-securi...-artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198-security-and-artifacts.txt)

The tool chosen for this lecture is **Trivy**, specifically for file system scanning (source code and its dependencies), not container image scanning. The video explicitly notes that Trivy *can* scan container images too, but here it is used to scan the source code directory. [\[198-securi...-artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198-security-and-artifacts.txt)

⚠️ **Expert Note**
The instructor emphasizes that the specific tool varies by project and organization. What matters is understanding **how** to integrate any scanning tool into the pipeline structure. The pipeline pattern (pull tool image → run scan → capture output → decide pass/fail) is transferable across all tools. Security teams often dictate which tool to use; the DevOps engineer's job is to integrate it correctly. The instructor also recommends doing independent research on available tools, as this knowledge is valuable both operationally and in interviews. [\[198-securi...-artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198-security-and-artifacts.txt)

***

## 1.3 The Entrypoint Problem — Why Tool-Specific Docker Images Can Fail

This is the most conceptually important topic in the video, and the instructor explicitly says "listen to this carefully."

In GitLab CI, each job runs inside a Docker container created from a specified image. When you specify `image: aquasec/trivy:latest`, GitLab pulls that image, runs a container from it, and then executes whatever you put in the `script:` block. The problem is that many tool-specific images (images built specifically for tools like Trivy) are designed to run that tool **as their entrypoint**. An entrypoint is the first command a Docker container executes when it starts. For the Trivy image, the entrypoint is the `trivy` binary itself. [\[198-securi...-artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198-security-and-artifacts.txt)

Now here's where it breaks. When GitLab runs your `script:` command inside the container, the command you write gets **appended to the entrypoint**. If the entrypoint is `trivy` and your script says `trivy fs --format json ...`, the actual command that executes becomes: `trivy trivy fs --format json ...`. This is `trivy` called twice — which is an invalid command. Trivy interprets `trivy` (the second one) as a subcommand, doesn't recognize it, and prints a usage/help message and fails. [\[198-securi...-artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198-security-and-artifacts.txt)

The error message you see is not intuitive. It says something like "unknown command" followed by usage instructions. The video warns: whenever you see an error message that shows "usage is so and so," it is **usually** an entrypoint collision — the container's built-in command conflicting with your explicitly written command. [\[198-securi...-artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198-security-and-artifacts.txt)

**The fix:** Override the entrypoint to empty. In the GitLab CI YAML, instead of just writing `image: aquasec/trivy:latest`, you use the expanded image syntax:

```yaml
image:
  name: aquasec/trivy:latest
  entrypoint: [""]
```

Setting `entrypoint: [""]` tells Docker: "Do not run any default command when the container starts. Just start the container empty and wait for my script." Now when GitLab injects `trivy fs --format json ...`, it runs cleanly because there is no conflicting entrypoint prepended. [\[198-securi...-artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198-security-and-artifacts.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198.SecurityScan.yml)

🔍 **Deep Dive**
This is why the `image:` key in the YAML has a nested structure (`name:` and `entrypoint:`) instead of a simple string value. The simple form `image: maven:3.9.9-eclipse-temurin-17` works for general-purpose images (like Maven or Ubuntu) because those images typically use a shell (`/bin/sh` or `/bin/bash`) as their entrypoint — which naturally accepts any command you pass. But specialized tool images set the tool binary as the entrypoint, creating this collision. The instructor also mentions an alternative approach: instead of using the tool-specific image, you could use a base image like Ubuntu or Debian, install the tool yourself inside the container, and then run the command. This avoids the entrypoint problem entirely but takes longer because of the installation step. The tool-image approach with `entrypoint: [""]` is faster and preferred. [\[198-securi...-artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198-security-and-artifacts.txt)

***

## 1.4 Parallel Job Execution with `needs`

By default, GitLab CI stages run sequentially — all jobs in stage 1 complete before any job in stage 2 starts. But within the same stage, or even across stages, you can use the `needs` keyword to create **explicit dependency chains** that allow jobs to run as soon as their specific prerequisites are met, regardless of stage ordering.

In this pipeline, both the `test-job` and `security-scan` job declare `needs: [build-job]`. This means: "I only depend on `build-job`. The moment `build-job` finishes, start me." Since both jobs declare the same dependency and neither depends on the other, they start simultaneously and run **in parallel**. The video confirms this by showing the pipeline execution: after the build job completes, both test and security scan execute at the same time, and security finishes before the test job because scanning is faster. [\[198-securi...-artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198-security-and-artifacts.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198.SecurityScan.yml)

Without `needs`, the test job (stage: `test`) would complete entirely before the security scan job (stage: `security`) could begin, because `test` is listed before `security` in the `stages:` declaration. `needs` overrides this stage-order constraint and enables parallelism based on actual data dependencies. [\[198-securi...-artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198-security-and-artifacts.txt)

***

## 1.5 Artifacts — Persisting Job Outputs Beyond Container Lifetime

When a GitLab CI job finishes, the container that ran it is destroyed. Everything inside that container — compiled files, scan reports, logs — disappears. If you need to keep any file beyond the job's lifetime (to download it, to pass it to a later job, or to archive it), you must declare it as an **artifact**.

Artifacts are declared in the YAML under the `artifacts:` key. You specify the file paths you want to preserve. After the job completes, GitLab extracts those files from the container and stores them on the GitLab server, where they can be downloaded from the pipeline UI. [\[198-securi...-artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198-security-and-artifacts.txt)

In this pipeline, two jobs produce artifacts:

1. **build-job** produces the compiled WAR file. The artifact path is `target/*.war` — using a wildcard to match whatever WAR file Maven produces in the `target/` directory. You could also use the exact filename (`target/vprofile-v2.war`) or even broader patterns like `*.jar` if you had multiple outputs. [\[198-securi...-artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198-security-and-artifacts.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198.SecurityScan.yml)

2. **security-scan** produces the Trivy scan report. The artifact path is `trivy-results.json` — the exact filename specified in the Trivy command's `--output` flag. [\[198-securi...-artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198-security-and-artifacts.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198.SecurityScan.yml)

Both jobs use `when: always` for their artifacts. This means: save the artifact regardless of whether the job passed or failed. This is important because even if the security scan finds critical vulnerabilities and the job "fails," you still want the report — that's the whole point. Similarly, even if something goes wrong during build, you might want partial outputs for debugging. [\[198-securi...-artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198-security-and-artifacts.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198.SecurityScan.yml)

***

## 1.6 The Trivy Command — What Each Part Does

The command used in the security scan job is:

```bash
trivy fs --format json --exit-code 0 --vuln-type os,library --output trivy-results.json .
```

Understanding each component:

* **`trivy`** — The scanner binary.
* **`fs`** — Subcommand for "file system." Tells Trivy to scan the local file system (source code and dependencies) rather than a container image. The video explicitly says "we are scanning file system, just the source code, not the container image."
* **`--format json`** — Output the results in JSON format (structured, machine-readable).
* **`--exit-code 0`** — This is the **quality gate control**. Exit code 0 means: "Even if vulnerabilities are found, return success (exit code 0)." This makes the job always pass, regardless of scan results. If you set `--exit-code 1`, Trivy returns exit code 1 when it finds vulnerabilities above the configured severity, which makes GitLab treat the job as **failed**.
* **`--vuln-type os,library`** — Scan for two categories: operating system-level vulnerabilities and library/dependency vulnerabilities.
* **`--output trivy-results.json`** — Write the results to this file instead of stdout.
* **`.`** (dot at the end) — The scan target: the current working directory. In a GitLab CI container, the current working directory contains the cloned source code of your repository. [\[198-securi...-artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198-security-and-artifacts.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198.SecurityScan.yml)

🔍 **Deep Dive**
The video also shows an extended version of the command with severity filtering: `--severity medium,high,critical` (using `-f` flag). This tells Trivy to only flag vulnerabilities at these severity levels. Combined with `--exit-code 1`, this creates a proper quality gate: "fail the job if any medium, high, or critical vulnerabilities are found." The instructor demonstrates this conceptually but reverts to `--exit-code 0` for the lecture, noting that proper quality gates are covered in depth in a separate DevOps projects course using SonarQube. [\[198-securi...-artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198-security-and-artifacts.txt)

***

## 1.7 The `after_script` Block

`after_script:` defines commands that run **after** the main `script:` block completes, regardless of whether the script succeeded or failed. In this pipeline, both the build job and the security scan job use `after_script: - ls -la` — simply listing directory contents. The video says this is just to demonstrate the feature; in real pipelines, you would use `after_script` for cleanup tasks, additional reporting, or post-processing needed before the artifact is captured. [\[198-securi...-artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198-security-and-artifacts.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198.SecurityScan.yml)

***

## 1.8 Notify-on-Failure — Conditional Job Execution

The final job in the pipeline is `notify-on-failure`. It belongs to the `notify` stage (the last stage) and uses `when: on_failure`. This is a GitLab CI keyword that means: "only run this job if any previous job in the pipeline has failed." If all jobs succeed, this job is skipped entirely. [\[198-securi...-artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198-security-and-artifacts.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198.SecurityScan.yml)

In the video, the notification is just an `echo` command — it mimics what a real notification would look like. In production, this would be replaced with a command that sends an actual notification to Slack, email, PagerDuty, or another alerting system. The point is to demonstrate the **pipeline pattern**: scan → evaluate → notify on failure. [\[198-securi...-artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198-security-and-artifacts.txt)

***

## 1.9 The Stage Declaration Requirement — A Real Error Caught Live

The video captures a real pipeline failure caused by a missing stage declaration. The `security-scan` job declares `stage: security`, but the `stages:` block at the top of the YAML did not include `security`. GitLab rejects the pipeline with: *"YAML invalid error, security scan job chosen stage security does not exist."* Every stage referenced by any job **must** be declared in the top-level `stages:` list. The fix was adding `- security` to the `stages:` block. This error is shown deliberately to teach the relationship between the `stages:` declaration and individual job `stage:` assignments. [\[198-securi...-artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198-security-and-artifacts.txt)

***

## 1.10 DevSecOps — The Broader Context

The instructor closes by framing the broader concept: when security scanning, quality gates, and vulnerability management are integrated directly into the CI/CD pipeline (rather than being a separate manual process), the practice is called **DevSecOps** — Development + Security + Operations. Security code scanning is described as "one of the very mandatory stages in DevSecOps." The message is that DevOps engineers who can work with security teams and integrate scanning tools into pipelines are practicing DevSecOps, which is increasingly expected in professional environments. [\[198-securi...-artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198-security-and-artifacts.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are adding two new capabilities to an existing GitLab CI/CD pipeline that already has build and test stages: (1) a **security scanning stage** using Trivy that runs in parallel with the test stage and produces a vulnerability report, and (2) **artifact preservation** so that both the compiled WAR file and the scan report survive beyond the pipeline run and can be downloaded. We also add a **failure notification stage** that triggers only when something goes wrong. The final pipeline has four stages: `build → test + security (parallel) → notify (on failure only)`. [\[198-securi...-artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198-security-and-artifacts.txt)

***

## Step 1: Add the Security Scan Job to `.gitlab-ci.yml`

Open your `.gitlab-ci.yml` file in VS Code. After the existing `test-job` block, add the security scan job.

**1a. Write the job definition:**

```yaml
security-scan:
  stage: security
  image:
    name: aquasec/trivy:latest
    entrypoint: [""]
  needs: [build-job]
  script:
    - trivy fs --format json --exit-code 0 --vuln-type os,library --output trivy-results.json .
  after_script:
    - ls -la
  artifacts:
    paths:
      - trivy-results.json
    when: always
```

 [\[198-securi...-artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198-security-and-artifacts.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198.SecurityScan.yml)

Let's break down every line:

**`security-scan:`** — The job name. Chosen to clearly describe its purpose. This is the identifier used elsewhere (e.g., in `needs` or pipeline UI).

**`stage: security`** — Assigns this job to a stage called `security`. This stage must also be declared in the top-level `stages:` list (Step 3 covers this).

**`image:`** — Uses the expanded syntax instead of a simple string. This is necessary because we need to override the entrypoint.

**`name: aquasec/trivy:latest`** — The Docker image from Docker Hub. Contains the Trivy binary pre-installed.

**`entrypoint: [""]`** — Overrides the image's default entrypoint (which is the `trivy` binary) to empty. Without this, the container would prepend `trivy` to your script command, resulting in `trivy trivy fs ...`, which fails. This is the fix for the entrypoint collision problem (explained in Theory §1.3). [\[198-securi...-artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198-security-and-artifacts.txt)

**`needs: [build-job]`** — This job depends only on `build-job`. It will start immediately after `build-job` completes, running in parallel with `test-job` (which has the same `needs` declaration).

**`script:`** — The Trivy scan command. Each part:

| Fragment                      | Purpose                                                                       |
| ----------------------------- | ----------------------------------------------------------------------------- |
| `trivy`                       | The scanner binary                                                            |
| `fs`                          | Scan mode: file system (source code), not container image                     |
| `--format json`               | Output format: JSON (structured, parseable)                                   |
| `--exit-code 0`               | Always return success, even if vulnerabilities found (no quality gate)        |
| `--vuln-type os,library`      | Scan for OS and library/dependency vulnerabilities                            |
| `--output trivy-results.json` | Write results to this file                                                    |
| `.`                           | Scan target: current working directory (where GitLab cloned your source code) |

 [\[198-securi...-artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198-security-and-artifacts.txt)

**`after_script: - ls -la`** — Runs after the main script. Here it just lists files (placeholder for real post-processing).

**`artifacts:`** — Declares `trivy-results.json` as an artifact so it persists after the container is destroyed. `when: always` ensures the artifact is saved even if the job fails.

***

## Step 2: Add the `needs` Keyword to the Test Job

The `test-job` already exists, but to enable parallel execution with the security scan, it also needs an explicit `needs` declaration.

Add this line inside the `test-job` block:

```yaml
test-job:
  stage: test
  needs: [build-job]
  # ... rest of existing config
```

 [\[198-securi...-artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198-security-and-artifacts.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198.SecurityScan.yml)

**What this achieves:** Both `test-job` and `security-scan` declare `needs: [build-job]`. Neither depends on the other. GitLab will start both as soon as `build-job` completes, and they will run **simultaneously**.

**Without `needs`:** The pipeline would run sequentially by stage order — all `test` stage jobs would finish before any `security` stage jobs begin. `needs` breaks this stage-sequential constraint.

***

## Step 3: Declare the New Stages in the `stages:` Block

The top-level `stages:` block must include every stage used by any job. Add `security` and `notify`:

```yaml
stages:
  - build
  - test
  - security
  - notify
```

 [\[198-securi...-artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198-security-and-artifacts.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198.SecurityScan.yml)

⚠️ **Common mistake caught in the video:** If you forget to add `- security` here but use `stage: security` in the job, GitLab rejects the entire pipeline with: *"YAML invalid error — security scan job chosen stage security does not exist."* This was demonstrated as a live error in the video. Every `stage:` value referenced by any job must appear in this list. [\[198-securi...-artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198-security-and-artifacts.txt)

***

## Step 4: Add Artifacts to the Build Job

The build job produces a WAR file but wasn't saving it as an artifact. Add the `after_script` and `artifacts` blocks:

```yaml
build-job:
  stage: build
  # ... existing config ...
  script:
    - echo "Building the project..."
    - mvn install
  after_script:
    - ls -la
  artifacts:
    paths:
      - target/*.war
    when: always
```

 [\[198-securi...-artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198-security-and-artifacts.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198.SecurityScan.yml)

**`target/*.war`** — The Maven build produces a WAR file in the `target/` directory. The wildcard `*` matches any WAR filename. You could use the exact name (`target/vprofile-v2.war`) or broader patterns (`*.jar`) depending on your needs. [\[198-securi...-artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198-security-and-artifacts.txt)

**`when: always`** — Save the artifact whether the build passed or failed. Useful for debugging failed builds.

***

## Step 5: Add the Notify-on-Failure Job

Add the notification job after the security scan block:

```yaml
notify-on-failure:
  stage: notify
  script:
    - echo "🚨 Build or Test job failed for $PROJECT_NAME! Please check logs."
  when: on_failure
```

 [\[198-securi...-artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198-security-and-artifacts.txt), [\[myoffice.a...enture.com\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198.SecurityScan.yml)

**`when: on_failure`** — This is a job-level keyword (not inside `artifacts`). It means: "Only execute this job if any previous job in the pipeline has failed." If everything succeeds, this job is skipped.

**`script:`** — Just an `echo` mimicking a notification. In production, replace with an actual notification command (Slack webhook, email API call, etc.). [\[198-securi...-artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198-security-and-artifacts.txt)

***

## Step 6: Commit, Push, and Observe

**6a. Save the file:** `Ctrl + S` in VS Code. [\[198-securi...-artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198-security-and-artifacts.txt)

**6b. Commit and push:**

```bash
git add .gitlab-ci.yml
git commit -m "Add security scan stage and artifacts"
git push
```

**6c. Observe the pipeline in GitLab UI:**

Navigate to your project → **CI/CD → Pipelines**. Watch the execution:

1. **Build job** runs first.
2. After build completes, **test job** and **security scan** start **simultaneously**.
3. Security scan typically finishes before the test job (scanning is faster than running unit tests + checkstyle).
4. If all succeed, the notify job is **skipped**.
5. If any job fails, the notify job executes. [\[198-securi...-artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198-security-and-artifacts.txt)

**6d. If the first push fails with a YAML error:**

Check the error message. If it says a stage "does not exist," go back and ensure the `stages:` block includes all referenced stage names. Fix, commit, push again. [\[198-securi...-artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198-security-and-artifacts.txt)

***

## Step 7: Download and Inspect Artifacts

**7a. Navigate to the pipeline in GitLab UI.**

On the pipeline page, you will see artifact download links for both `build-job` and `security-scan`. [\[198-securi...-artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198-security-and-artifacts.txt)

**7b. Download the build artifact:**

Click the download link for `build-job`. It downloads as a ZIP file. Extract it to find the WAR file (e.g., `vprofile-v2.war`). [\[198-securi...-artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198-security-and-artifacts.txt)

**7c. Download the security scan artifact:**

Click the download link for `security-scan`. It downloads as a ZIP file. Extract it to find `trivy-results.json`. Open it — it contains a structured JSON report of all vulnerabilities found in the source code and its dependencies. [\[198-securi...-artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198-security-and-artifacts.txt)

**Connection to larger flow:** These artifacts are the tangible outputs of the pipeline. The WAR file is the deployable application. The JSON report is the security assessment. In a complete pipeline, the next stages would use the WAR file to build a Docker image (the next lecture) and the JSON report to enforce quality gates.

***

## Step 8: Understanding Quality Gates (Conceptual Execution)

The video demonstrates quality gate options without implementing them permanently.

**To enable a quality gate (fail on vulnerabilities):**

Change `--exit-code 0` to `--exit-code 1` in the Trivy command. Optionally add severity filtering:

```bash
trivy fs --format json --exit-code 1 --severity medium,high,critical --vuln-type os,library --output trivy-results.json .
```

 [\[198-securi...-artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198-security-and-artifacts.txt)

| Change                            | Effect                                                                                      |
| --------------------------------- | ------------------------------------------------------------------------------------------- |
| `--exit-code 1`                   | Trivy returns exit code 1 if vulnerabilities are found → GitLab marks the job as **failed** |
| `--severity medium,high,critical` | Only flag vulnerabilities at these severity levels (ignore low/informational)               |

When the security scan job fails, `notify-on-failure` triggers, and the pipeline does not proceed to later stages. This is the complete pattern: **scan → evaluate → gate → notify**. [\[198-securi...-artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198-security-and-artifacts.txt)

⚠️ **Expert Note**
Quality gate configuration is tool-specific. Trivy uses `--exit-code` and `--severity`. SonarQube uses quality gate profiles configured in the SonarQube server. Each tool has its own mechanism. The pipeline pattern (scan → gate → notify) is universal; the implementation details vary. [\[198-securi...-artifacts \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/198-security-and-artifacts.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Pipeline Architecture

```
stages: [build, test, security, notify]

build-job ──────────┬──→ test-job          (parallel, needs: build-job)
  (mvn install)     │
  artifact: *.war   └──→ security-scan     (parallel, needs: build-job)
                           (trivy fs .)
                           artifact: trivy-results.json
                                │
                                ▼
                         notify-on-failure  (when: on_failure — skipped if all pass)
```

***

## The Entrypoint Problem (Critical Mental Model)

```
Tool image (e.g., aquasec/trivy) has ENTRYPOINT = trivy

Without fix:
  Container starts → runs: trivy (entrypoint) + trivy fs ... (your script)
  Actual command:   trivy trivy fs ...  ← BROKEN
  Error:            "unknown command" / "usage: ..."

Fix:
  entrypoint: [""]  → nullifies default command
  Container starts → runs: trivy fs ... (your script only)
  Actual command:   trivy fs ...  ← CORRECT

Alternative (slower): Use base image (Ubuntu/Debian) → install tool → run command
```

***

## Trivy Command Breakdown

```
trivy fs --format json --exit-code 0 --vuln-type os,library --output trivy-results.json .
  │    │       │              │              │                      │                    │
  │    │       │              │              │                      │                    └─ scan target: CWD (source code)
  │    │       │              │              │                      └─ write to this file
  │    │       │              │              └─ what to scan for: OS + library vulns
  │    │       │              └─ quality gate: 0=always pass, 1=fail if vulns found
  │    │       └─ output format
  │    └─ mode: file system (not container image)
  └─ binary
```

***

## Artifact Preservation

```
Job output lives inside container → container destroyed after job → output LOST

Solution: artifacts:
  paths: [file]     → extracted from container, stored on GitLab server
  when: always      → save even if job fails

Build:    target/*.war          → deployable application
Security: trivy-results.json   → vulnerability report
```

***

## Parallel Execution via `needs`

```
Default (stage-sequential):    build → test → security → notify
                                        (waits for test to finish)

With needs: [build-job]:       build → test      ┐ (parallel)
                                     → security  ┘

Rule: needs declares ACTUAL dependency, not stage order
      Both jobs need only build-job → both start when build-job finishes
```

***

## Quality Gate Control Flow

```
--exit-code 0:  scan → report → PASS (always)          → no notification
--exit-code 1:  scan → report → FAIL (if vulns found)  → notify-on-failure triggers

Optional severity filter:  --severity medium,high,critical
  → only flag vulns at these levels
  → combined with exit-code 1 = production quality gate
```

***

## `when:` Keyword — Two Different Contexts

```
artifacts:
  when: always     → save artifact regardless of job pass/fail

notify-on-failure:
  when: on_failure → run this JOB only if a previous job failed
```

Same keyword, different scopes. Don't confuse them.

***

## Stage Declaration Requirement

```
stages:         ← MUST list every stage name used by any job
  - build
  - test
  - security    ← forgot this → "YAML invalid, stage does not exist"
  - notify

Job uses stage: security → must exist in stages: list
```

***

## Image Syntax — Simple vs Expanded

```
Simple (general images):
  image: maven:3.9.9-eclipse-temurin-17     ← shell entrypoint, no conflict

Expanded (tool images):
  image:
    name: aquasec/trivy:latest              ← tool entrypoint, needs override
    entrypoint: [""]

Rule: Use expanded when the image's entrypoint IS the tool you're calling
```

***

## Security Scanning Tool Landscape

```
Tool         │ Capability
─────────────┼─────────────────────────────────────
Snyk         │ SAST + SCA (code + dependencies)
SonarQube    │ Code quality + security
Semgrep      │ Lightweight SAST
Trivy        │ FS + container images + IaC (Terraform, K8s, Helm)
```

SAST = scans YOUR code (SQL injection, XSS, insecure functions)
SCA  = scans YOUR DEPENDENCIES (known CVEs in Maven/npm/pip libraries)

***

## DevSecOps Positioning

```
DevOps pipeline + security scanning integrated = DevSecOps

Security scan = mandatory stage BEFORE publishing artifact
Position: after build, before deploy/publish
```

***

## Complete YAML Structure (Reference)

```yaml
stages: [build, test, security, notify]

build-job:        stage: build     │ image: maven     │ script: mvn install
                  artifacts: target/*.war (when: always)

test-job:         stage: test      │ needs: [build-job] │ script: mvn test + checkstyle

security-scan:    stage: security  │ needs: [build-job]
                  image: aquasec/trivy (entrypoint: [""])
                  script: trivy fs ... → trivy-results.json
                  artifacts: trivy-results.json (when: always)

notify-on-failure: stage: notify   │ when: on_failure  │ script: echo / slack / email
```

***

## Key Engineering Patterns

| Pattern                       | Manifestation                                                                                                |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------ |
| **Entrypoint nullification**  | Override tool image entrypoint to prevent command collision — transferable to any tool-specific Docker image |
| **Parallel-after-dependency** | `needs` enables fan-out parallelism from a single prerequisite job                                           |
| **Artifact persistence**      | Explicitly declare outputs to survive ephemeral container lifecycle                                          |
| **Quality gate as exit code** | Tool exit code → pipeline pass/fail decision → notification trigger chain                                    |
| **Conditional execution**     | `when: on_failure` creates reactive pipeline behavior without complex logic                                  |
| **Stage-as-contract**         | Every stage must be declared before use — enforces pipeline structure integrity                              |
| **Scan-before-publish**       | Security assessment before artifact release — the core DevSecOps gate pattern                                |

***

## Project Continuity

```
BEFORE: build + test stages existed
THIS:   + security scan (Trivy) + artifacts (WAR + JSON) + notify-on-failure
NEXT:   Build and publish Docker image (next lecture)
```

***

This completes the full reconstruction. **Theory** builds understanding of the entrypoint problem, scanning categories, and quality gates. **Practical** gives you every line of YAML and every operational step to reproduce the pipeline. The **Compression Map** lets you mentally reload the entire system — from pipeline architecture to the entrypoint fix — in under two minutes. Let me know if you'd like Anki flashcards or any section expanded! 🚀
