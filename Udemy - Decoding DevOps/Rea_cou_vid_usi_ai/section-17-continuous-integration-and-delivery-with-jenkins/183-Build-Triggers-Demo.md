# Jenkins Build Triggers — Automating Pipeline Execution

> **Source**: [183.-Build-Triggers-Demo.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt?EntityRepresentationId=7de8eb9a-9516-4e4e-802f-6eedc544d10d) (caption transcript) + [183. Build+Triggers+Remotely.docx](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B2C57A7E2-985E-44AE-99EF-4D5AE99C5333%7D\&file=183.%20Build%2BTriggers%2BRemotely.docx\&action=default\&mobileredirect=true\&EntityRepresentationId=28aa8352-846c-4233-b937-d854a0e94aa9) (resource document) + [183. Build+Triggers+Remotely.pdf](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.%20Build+Triggers+Remotely.pdf?EntityRepresentationId=133065c6-044d-41f8-8f2c-03a518de18a0) (resource PDF) [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt), [\[183. Build...s+Remotely \| Word\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B2C57A7E2-985E-44AE-99EF-4D5AE99C5333%7D&file=183.%20Build%2BTriggers%2BRemotely.docx&action=default&mobileredirect=true), [\[183. Build...s+Remotely \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.%20Build+Triggers+Remotely.pdf)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1. The Core Problem — Why Build Triggers Exist

Up to this point in the course, every pipeline and job has been executed by clicking **"Build Now"** manually. This is acceptable during development and testing, but it is fundamentally incompatible with the philosophy of DevOps and CI/CD. The entire purpose of continuous integration is that pipelines run **automatically** in response to events — a code commit, a schedule, an external system's request. If a human must click a button to start the pipeline, the "continuous" in continuous integration is broken. [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

**Build triggers** are Jenkins' mechanism for automating when and how a job or pipeline starts executing. Instead of manual intervention, you configure a trigger that tells Jenkins: "Start this job when X happens." The instructor demonstrates five distinct trigger types in this video, each solving a different automation scenario. [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

***

## 2. Git Webhook — GitHub Pushes to Jenkins

### What It Is

A **Git Webhook** (referred to as a "forced trigger" by the instructor) is a mechanism where **GitHub actively notifies Jenkins** whenever a specific event occurs in the repository. The most common event is a **push** (a commit being pushed to the repository), but webhooks can be configured for many other events — branch creation, comments on commits, deployments, pull requests, and more. [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

### Why It Exists

The problem is simple: Jenkins doesn't know when a developer pushes code to GitHub. Without a webhook, Jenkins would have to constantly check GitHub ("Has anything changed? Has anything changed?"), which is inefficient. A webhook flips this: **GitHub tells Jenkins** the moment something happens. This is event-driven automation — the pipeline starts within seconds of a code push, with zero polling overhead. [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

### How It Works Internally

The mechanism works in three parts:

1.  **You register a webhook URL in GitHub** — this URL points to your Jenkins server, specifically to the endpoint `http://<JENKINS_IP>:8080/github-webhook/`. When an event occurs, GitHub sends an HTTP POST request (a **JSON payload**) to this URL containing details about the event (who pushed, which branch, what changed, etc.). [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

2.  **Jenkins receives the payload** — Jenkins has a built-in endpoint (`/github-webhook/`) that listens for these incoming POST requests. When it receives one, it examines the payload to determine which repository triggered the event.

3.  **Jenkins matches the event to a job** — Any job that is configured with the trigger **"GitHub hook trigger for GITScm polling"** and whose Git SCM configuration matches the repository in the payload will be triggered. Jenkins starts the build automatically. [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

### The Two Configuration Points

This trigger requires configuration on **both sides** — GitHub and Jenkins:

*   **GitHub side**: Repository Settings → Webhooks → Add webhook → provide the Jenkins URL with `/github-webhook/` at the end.
*   **Jenkins side**: Job Configure → Build Triggers → check **"GitHub hook trigger for GITScm polling"**. [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

### Verification

After adding the webhook in GitHub, you can refresh the Webhooks page. A **green check mark** (✓) means the webhook was delivered successfully — GitHub sent a test ping to Jenkins and received a valid response. A **red cross mark** (✗) means delivery failed. [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

GitHub also provides a **"Recent Deliveries"** section where you can inspect the exact JSON payload that was sent, the response code Jenkins returned, and retry failed deliveries.

### Common Mistakes and Failure Scenarios

The instructor explicitly calls out several troubleshooting points: [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

*   **Wrong URL** — The URL must be exactly `http://<JENKINS_IP>:8080/github-webhook/` with a **trailing forward slash**. No spelling mistakes. The instructor emphasizes: *"Make sure there is a forward slash at the end, no spelling mistake, exactly as it is."*
*   **Wrong content type** — The content type must be set to **`application/json`**. Other content types may not be parsed correctly by Jenkins.
*   **Jenkins Security Group blocking GitHub** — This is a critical AWS-specific point. If the Jenkins Security Group allows port 8080 only from your personal IP, GitHub's servers cannot reach Jenkins. Port **8080 must be allowed from anywhere** (or at least from GitHub's IP ranges) for webhooks to work. The instructor says: *"If it's just your IP, then GitHub will not be able to reach your Jenkins server."*
*   **Secret field** — The instructor explicitly says: *"Don't need to mention any secret here."* For this setup, the secret field is left empty.

> 🔍 **Deep Dive (Optional)**
>
> GitHub webhooks support a rich set of event types beyond just `push`. When configuring the webhook, you get three options:
>
> *   **Just the push event** — triggers only on pushes (this is what the instructor selects).
> *   **Everything** — triggers on every possible event (creates a lot of noise).
> *   **Let me select individual events** — gives granular control. The instructor briefly shows options like "branch or tag creation," "comments on commits," "deployments," and notes *"there are many options over here."*
>
> In production, you typically use "Just the push event" for CI pipelines and select individual events only when you need specialized workflows (e.g., trigger a deployment pipeline on release creation).

> ⚠️ **Expert Note (Optional)**
>
> The security implication of opening port 8080 to the world for webhooks is significant. In production Jenkins environments, this is often mitigated by: (1) using a reverse proxy (like Nginx) with HTTPS in front of Jenkins, (2) whitelisting only GitHub's known IP ranges in the security group (GitHub publishes these in their API metadata), or (3) using a webhook relay service. The open-to-anywhere approach is acceptable for learning environments but should not be used in production.

***

## 3. Poll SCM — Jenkins Checks GitHub

### What It Is

**Poll SCM** is a trigger where **Jenkins periodically checks your source code repository** (the SCM — Source Code Manager) for new commits. If Jenkins detects a change since the last check, it triggers the job. If nothing has changed, it does nothing and checks again at the next interval. [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

### How It Differs from Webhooks

The instructor describes Poll SCM as **"similar but the opposite"** of the Git Webhook. With a webhook, GitHub pushes a notification to Jenkins (GitHub initiates). With Poll SCM, Jenkins pulls — it actively and repeatedly asks GitHub: "Are there new commits?" (Jenkins initiates). Both achieve the same end result (a build triggers when code changes), but the mechanism and efficiency differ. [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

### How It Works Internally

1.  You configure a **schedule** (in cron format) in the job's Build Triggers section.
2.  At every scheduled interval, Jenkins connects to the Git repository configured in the job's SCM section.
3.  Jenkins compares the latest commit hash in the repository with the commit hash from the last build.
4.  If they differ (meaning new commits exist), Jenkins triggers the build.
5.  If they're the same, Jenkins logs "no changes" and waits for the next interval. [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

### The Cron Job Format

The schedule uses the standard **cron format** with five fields. The instructor maps them explicitly: [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

    MINUTE  HOUR  DAY_OF_MONTH  MONTH  DAY_OF_WEEK

*   **MINUTE** — 0–59
*   **HOUR** — 0–23
*   **DAY\_OF\_MONTH** — 1–31
*   **MONTH** — 1–12
*   **DAY\_OF\_WEEK** — 0–7 (where 0 and 7 are Sunday, 1 is Monday)

A `*` (star) in any field means "every" — so `* * * * *` means **every minute of every hour of every day of every month of every day of the week**. The instructor uses this five-star pattern for the demo so the effect is visible immediately. [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

### Verification

Jenkins provides a **"Git Polling Log"** link on the job page when Poll SCM is enabled. Clicking it shows you the history of every poll — when Jenkins checked, whether it found changes, and what it did. The instructor demonstrates: after enabling `* * * * *`, the polling log initially says it checked but *"did not find any change in your repository."* After pushing a new commit, the next poll cycle shows *"changes found"* and the job enters a pending state before executing. [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

> 🔍 **Deep Dive (Optional)**
>
> Poll SCM is inherently less efficient than webhooks because Jenkins must repeatedly connect to the Git server, even when nothing has changed. For a single job polling every minute, this is negligible. But in large Jenkins installations with hundreds of jobs, each polling frequently, the cumulative load on both Jenkins and the Git server can become significant. This is why webhooks are the preferred trigger for most CI/CD pipelines — they are event-driven and create zero unnecessary traffic. Poll SCM is useful when webhooks are not possible (e.g., the Git server is behind a firewall that Jenkins can reach but that cannot push to Jenkins).

***

## 4. Build Periodically — Scheduled Execution (No SCM Check)

### What It Is

**Build Periodically** is a trigger that runs the job **at a specific scheduled time**, regardless of whether any code has changed. It does not check the source code repository at all — it simply executes the job on schedule, like a cron job on a Linux server. [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

### How It Differs from Poll SCM

The instructor draws a clear distinction: Poll SCM checks GitHub and only runs if there are changes. Build Periodically **does not check GitHub** — it just runs the job at the scheduled time, unconditionally. The instructor says: *"Scheduled job, which is similar to Poll SCM but it is not going to check your source code manager, or your GitHub. It will just run the job at that particular time."* [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

### Use Cases

This is used for jobs that need to run on a regular cadence regardless of code changes — nightly builds, periodic cleanup tasks, scheduled deployments to non-production environments, periodic health checks, or report generation.

### The Cron Format Example

The instructor constructs a real-world example: **run every weeknight at 8:30 PM**: [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

    30 20 * * 1-5

Breaking this down:

*   **`30`** — Minute 30 (half past the hour).
*   **`20`** — Hour 20 (8:00 PM in 24-hour format).
*   **`*`** — Every day of the month (1–31).
*   **`*`** — Every month (1–12).
*   **`1-5`** — Monday through Friday. The instructor explains: *"Zero is Sunday, one is Monday. So it's like Monday to Friday."* [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

### Shared Foundation

The instructor explicitly connects all three time-based triggers (Poll SCM, Build Periodically, and the cron concept): *"Poll SCM and build periodically, all three are same"* — meaning they all use the same cron job format that was already learned in the bash scripting section of the course. [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

***

## 5. Remote Trigger — Triggering Jenkins from Anywhere

### What It Is

A **remote trigger** allows you to start a Jenkins job from **anywhere** — from a script, from another Jenkins server, from your laptop, from some other server — using an HTTP request (specifically, a `curl` command). As long as you have network access to the Jenkins server, you can trigger any job remotely. [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

### Why It Exists

This is the most flexible trigger. Webhooks are tied to GitHub. Poll SCM and Build Periodically are time-based. But remote triggers are **universal** — any system that can make an HTTP request can trigger a Jenkins job. The instructor emphasizes the breadth: *"You can run it from a script. And when it says script, it's not just bash, it could be Python, Ruby, any programming language, Ansible, from anywhere you can run that command."* [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

### The Three Components

The instructor (and the resource document) break down the remote trigger into **three components** that must be assembled: [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt), [\[183. Build...s+Remotely \| Word\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B2C57A7E2-985E-44AE-99EF-4D5AE99C5333%7D&file=183.%20Build%2BTriggers%2BRemotely.docx&action=default&mobileredirect=true)

#### Component 1: Job URL with Token

Every Jenkins job can be configured to accept remote build requests by enabling **"Trigger builds remotely"** in the job's Build Triggers section. You provide an **authentication token** (any name you choose — the instructor uses `mybuildtoken`). Jenkins then generates a URL in this format: [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

    http://<JENKINS_IP>:8080/job/<JOB_NAME>/build?token=<TOKEN_NAME>

This URL is the endpoint you'll hit to trigger the build. The token in the URL acts as a first layer of authentication — only requests with the correct token are accepted.

#### Component 2: API Token (User Authentication)

The Jenkins user (e.g., `admin`) needs an **API token** for authentication. This is generated inside Jenkins: click your username dropdown (top right) → **Configure** → scroll to **API Token** → click **Add New Token** → click **Generate**. Copy the generated token immediately (it's shown only once). [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

The API token is stored in the format: `username:token` — for example, `admin:116ce8f1ae914b477d0c74a68ffcc9777c`. [\[183. Build...s+Remotely \| Word\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B2C57A7E2-985E-44AE-99EF-4D5AE99C5333%7D&file=183.%20Build%2BTriggers%2BRemotely.docx&action=default&mobileredirect=true)

This is the second layer of authentication — it proves you are an authorized Jenkins user.

#### Component 3: CRUMB (CSRF Protection)

Jenkins has **CSRF (Cross-Site Request Forgery) protection** enabled by default. To make a remote API call, you must include a **CRUMB** — a special token that Jenkins generates to verify the request is legitimate and not a forged cross-site attack. [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

The CRUMB is generated by hitting a special Jenkins API endpoint using the `wget` command: [\[183. Build...s+Remotely \| Word\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B2C57A7E2-985E-44AE-99EF-4D5AE99C5333%7D&file=183.%20Build%2BTriggers%2BRemotely.docx&action=default&mobileredirect=true), [\[183. Build...s+Remotely \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.%20Build+Triggers+Remotely.pdf)

```bash
wget -q --auth-no-challenge --user username --password password --output-document - 'http://JENKINS_IP:8080/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,":",//crumb)'
```

This command returns a string like: `Jenkins-Crumb:8cb80f4f56d6d35c2121a1cf35b7b501`. [\[183. Build...s+Remotely \| Word\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B2C57A7E2-985E-44AE-99EF-4D5AE99C5333%7D&file=183.%20Build%2BTriggers%2BRemotely.docx&action=default&mobileredirect=true)

> 🔍 **Deep Dive (Optional)**
>
> The CRUMB is Jenkins' CSRF protection mechanism. When Jenkins receives an API request, it checks whether the request includes a valid CRUMB in the header. This prevents attackers from tricking your browser into making unauthorized requests to Jenkins. The CRUMB is tied to your Jenkins session and the specific Jenkins instance. The `crumbIssuer` API endpoint generates this token by combining your authentication with a server-side secret. Without it, Jenkins rejects POST requests from external sources — which is why simply hitting the job URL in a browser or a plain `curl` without the CRUMB header would fail.

### The Final Combined Command

All three components are assembled into a single `curl` command: [\[183. Build...s+Remotely \| Word\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B2C57A7E2-985E-44AE-99EF-4D5AE99C5333%7D&file=183.%20Build%2BTriggers%2BRemotely.docx&action=default&mobileredirect=true), [\[183. Build...s+Remotely \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.%20Build+Triggers+Remotely.pdf)

```bash
curl -I -X POST http://username:APItoken@JENKINS_IP:8080/job/JOB_NAME/build?token=TOKENNAME -H "Jenkins-Crumb:CRUMB"
```

Breaking this down completely:

*   **`curl`** — The command-line HTTP client.
*   **`-I`** — Tells curl to show only the HTTP response headers (not the body). Useful for seeing the HTTP status code.
*   **`-X POST`** — Specifies this is a POST request (Jenkins requires POST for build triggers, not GET).
*   **`http://username:APItoken@...`** — HTTP Basic Authentication embedded in the URL. The `username:APItoken` before the `@` sign authenticates the request as the Jenkins user. This is Component 2.
*   **`JENKINS_IP:8080/job/JOB_NAME/build?token=TOKENNAME`** — The job URL with the build token. This is Component 1.
*   **`-H "Jenkins-Crumb:CRUMB"`** — An HTTP header containing the CRUMB value. The `-H` flag adds a custom header to the request. This is Component 3. [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

The instructor notes that this trigger has **full authentication** — the combination of job token, API token, and CRUMB ensures that only authorized users with the correct credentials can trigger the job remotely. [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

***

## 6. Build After Other Projects — Downstream Triggering

### What It Is

The **"Build after other projects are built"** trigger causes a job to run automatically **when another specified job completes**. This creates a **dependency chain** — Job B runs only after Job A finishes. [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

### Why It Exists

In real-world CI/CD systems, pipelines are often split into multiple jobs rather than one monolithic pipeline. For example, you might have a build job, a test job, a deployment job, and a notification job — each as separate Jenkins jobs. The downstream trigger allows you to chain them: when the build job finishes, the test job starts automatically, and so on. [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

### How It Works

In the **downstream job's** configuration (the one that should run second), go to Build Triggers and select **"Build after other projects are built."** Then type the name of the **upstream job** (the one that should run first). Jenkins auto-completes the job name as you type. When the upstream job finishes, Jenkins automatically triggers the downstream job. [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

The instructor demonstrates this by creating a simple **"test job"** (freestyle, with just `echo test test test` as the build step) and configuring it to run after the existing build job. After running the build job, the console output shows: *"Triggering new build of a test job."* And the test job's build history shows job ID 1 — triggered automatically. [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

***

## 7. Instructor's Summary — Which Triggers to Use

The instructor closes with an important practical framing: *"So these are some popular Jenkins triggers. As I said, there are more. But these triggers are more than enough to create any successful pipeline."* [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

The five triggers covered are:

1.  **GitHub Webhook** — event-driven, GitHub pushes to Jenkins
2.  **Poll SCM** — Jenkins periodically checks GitHub
3.  **Build Periodically** — scheduled execution, no SCM check
4.  **Remote Trigger** — HTTP request from anywhere
5.  **Build After Other Projects** — downstream chaining

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are configuring **five different build triggers** on Jenkins jobs to demonstrate every major way a Jenkins pipeline can be started automatically. The goal is to move from "click Build Now" to fully automated pipeline execution triggered by code commits, schedules, remote scripts, or upstream job completion. [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

**Why it matters**: In production CI/CD, no one clicks "Build Now." Pipelines must start automatically. Understanding all trigger types lets you choose the right one for any scenario — webhook for real-time CI, scheduled for nightly builds, remote for cross-system integration, downstream for job chaining.

**Final outcome**: By the end, the Jenkins job will trigger automatically via a GitHub push (webhook), on a polling schedule (Poll SCM), at a fixed time (Build Periodically), from a command line anywhere (Remote Trigger), and as a downstream reaction to another job completing. [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

***

## Trigger 1: GitHub Webhook

### Step 1.1: Get the Jenkins URL

Copy the Jenkins server URL up to and including the port: `http://<JENKINS_IP>:8080`. This is the base URL that GitHub will use to reach Jenkins. [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

### Step 1.2: Configure the Webhook in GitHub

Navigate to your **GitHub repository** (not your GitHub account settings — the **repository** settings). The instructor emphasizes this distinction: *"This is repository setting, not account setting."* [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

1.  Click **Settings** (on the repository page).
2.  Click **Webhooks** in the left sidebar.
3.  Click **Add webhook**.
4.  In the **Payload URL** field, paste the Jenkins URL and append `/github-webhook/`:

<!---->

    http://<JENKINS_IP>:8080/github-webhook/

**Critical**: There must be a **forward slash at the end** (`/`). The instructor explicitly warns: *"Make sure there is a forward slash at the end, no spelling mistake, exactly as it is."* [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

5.  Set **Content type** to **`application/json`**. [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)
6.  Leave the **Secret** field empty — the instructor says: *"Don't need to mention any secret here."*
7.  Under "Which events would you like to trigger this webhook?", select **"Just the push event"** — this means the webhook fires only when code is pushed to the repository. [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)
8.  Click **Add webhook**.

### Step 1.3: Verify Webhook Delivery

Refresh the Webhooks page in GitHub. Look for a **green check mark** (✓) next to the webhook — this means GitHub successfully delivered a test ping to Jenkins. [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

If you see a **red cross mark** (✗), troubleshoot:

*   Verify the URL is correct (including the trailing `/`).
*   Verify the content type is `application/json`.
*   **Check the Jenkins Security Group in AWS** — port 8080 must be open from anywhere (or at least from GitHub's IP ranges). If it's restricted to only your personal IP, GitHub's servers cannot reach Jenkins. [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

You can also click **Recent Deliveries** to inspect the exact JSON payload that was sent and the response Jenkins returned.

### Step 1.4: Enable the Trigger in Jenkins

Go to the **Jenkins job** → **Configure** → scroll to **Build Triggers** → check **"GitHub hook trigger for GITScm polling"** → **Save**. [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

This tells Jenkins: "When a GitHub webhook payload arrives for a repository that matches this job's Git configuration, trigger this job."

### Step 1.5: Test It

Note the current build ID (e.g., job ID 1). Now go to your local clone of the repository and make a commit: [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

```bash
touch testfile.txt
git add .
git commit -m "test trigger one"
git push origin master
```

Go back to Jenkins — a new build (job ID 2) should appear, triggered automatically by the push. [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

**What happened internally**: You pushed to GitHub → GitHub sent a POST request with a JSON payload to `http://<JENKINS_IP>:8080/github-webhook/` → Jenkins received it → Jenkins matched the repository URL to the job → Jenkins triggered the build.

***

## Trigger 2: Poll SCM

### Step 2.1: Disable the Previous Trigger

In the Jenkins job configuration, **uncheck** "GitHub hook trigger for GITScm polling" (so it doesn't interfere with testing the new trigger). [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

### Step 2.2: Enable Poll SCM

Check **"Poll SCM"**. A **Schedule** text field appears. Enter the cron expression: [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

    * * * * *

This means: every minute, every hour, every day, every month, every day of the week — effectively, Jenkins checks for new commits **every minute**. The instructor uses this aggressive schedule so the effect is visible during the demo.

Click **Save**. [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

### Step 2.3: Observe the Polling Log

On the job page, you should now see a **"Git Polling Log"** link. Click it. It shows that Jenkins checked the repository but **"did not find any change."** [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

### Step 2.4: Make a Commit and Wait

In your local repository: [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

```bash
touch testfile2.txt
git add .
git commit -m "test trigger two"
git push origin master
```

Now wait up to one minute. Go back to the Git Polling Log — it should now show **"changes found."** The job enters a **pending state** and then starts executing. The instructor observes: *"See that, changes found, and you see the job ID three, it's in pending state, it will start in a moment."* [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

### Key Difference from Webhook

The instructor reiterates: *"Here Jenkins will be checking every minute. And GitHub webhook, whenever there is a commit, GitHub will send a JSON payload which will trigger your job."* Both achieve the same result — a build on code change — but the mechanism is fundamentally different (pull vs. push). [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

***

## Trigger 3: Build Periodically

### Step 3.1: Disable Poll SCM, Enable Build Periodically

In the job configuration, **uncheck** "Poll SCM." Check **"Build periodically."** [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

### Step 3.2: Enter a Schedule

The instructor demonstrates a real-world schedule — **every weeknight at 8:30 PM**: [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

    30 20 * * 1-5

*   `30` — minute 30
*   `20` — 8:00 PM (24-hour format)
*   `*` — every day of the month
*   `*` — every month
*   `1-5` — Monday (1) through Friday (5). The instructor explains the day mapping: *"Zero is Sunday, one is Monday."* [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

Click **Save**.

The instructor doesn't wait for this to trigger (it would require waiting until 8:30 PM) but confirms the concept is clear and uses the same cron format already learned. [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

**Key difference from Poll SCM**: Build Periodically does **not** check the repository for changes. It simply runs the job at the scheduled time, unconditionally.

***

## Trigger 4: Remote Trigger

This is the most complex trigger, requiring three preparatory steps before the final command can be executed. The instructor says: *"This can get slightly complicated, but if you stay with me, follow the document, it will work."* [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

### Step 4.1: Generate the Job URL with Token

1.  Go to the **Jenkins job** → **Configure** → **Build Triggers**.
2.  Check **"Trigger builds remotely (e.g., from scripts)"**.
3.  In the **Authentication Token** field, enter a token name. The instructor uses: **`mybuildtoken`**. [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)
4.  Jenkins shows a URL pattern. Copy it. The URL looks like:

<!---->

    http://<JENKINS_IP>:8080/job/<JOB_NAME>/build?token=mybuildtoken

5.  **Save** the job configuration. [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)
6.  Paste this URL into a text editor (the instructor uses Sublime Text) — you'll assemble all pieces here.

Replace `JENKINS_URL` with the actual Jenkins IP up to port 8080. Remove any extra trailing slash. The token name `mybuildtoken` should already be in the URL. [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

### Step 4.2: Generate an API Token for the Jenkins User

1.  In Jenkins, click on your **username dropdown** (top right corner of the page).
2.  Click **Configure**. [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)
3.  Scroll to **API Token**.
4.  Click **Add New Token**.
5.  Click **Generate**.
6.  **Copy the generated token immediately** — it is shown only once.
7.  Paste it in your text editor in the format: [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

<!---->

    admin:<generated_token>

Replace `admin` with your actual Jenkins username if it's different. The format is `username:token`. [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

### Step 4.3: Generate the CRUMB

The CRUMB requires running a `wget` command. The instructor provides this command (also in the resource document): [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt), [\[183. Build...s+Remotely \| Word\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B2C57A7E2-985E-44AE-99EF-4D5AE99C5333%7D&file=183.%20Build%2BTriggers%2BRemotely.docx&action=default&mobileredirect=true)

```bash
wget -q --auth-no-challenge --user admin --password <your_password> --output-document - 'http://<JENKINS_IP>:8080/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,":",//crumb)'
```

Breaking down every part:

*   **`wget`** — A command-line utility for making HTTP requests and downloading files.
*   **`-q`** — Quiet mode; suppresses wget's own progress output, showing only the result.
*   **`--auth-no-challenge`** — Sends authentication credentials proactively without waiting for the server to challenge. Required because Jenkins' crumb issuer endpoint needs authentication.
*   **`--user admin`** — The Jenkins username.
*   **`--password <your_password>`** — The Jenkins login password (not the API token — the actual login password). [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)
*   **`--output-document -`** — The hyphen (`-`) tells wget to output the result to stdout (the terminal) instead of saving it as a file.
*   **`'http://<JENKINS_IP>:8080/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,":",//crumb)'`** — The Jenkins CRUMB API endpoint. The `xpath` parameter tells the API to return the crumb in the format `Jenkins-Crumb:<value>`.

**Critical formatting note**: This entire command must be on **one line**. The instructor warns multiple times about ensuring there are no accidental line breaks: *"Make sure you remove the new line character"* and *"Make sure this is all in just one line, not multiple lines."* [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

#### Installing wget on Windows (Git Bash)

The instructor notes that `wget` is **not available by default on Windows** but is available on macOS terminals. For Windows users using Git Bash: [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

1.  Search the internet for **"wget for Git Bash"**.
2.  Find the link from **eternallybored.org**.
3.  Download the **64-bit ZIP file**.
4.  Open the ZIP file.
5.  Extract **`wget.exe`** to: **`C:\Program Files\Git\mingw64\bin\`** [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)
6.  Close and reopen Git Bash for the change to take effect.

After extraction, `wget` is available in Git Bash.

#### Run the Command

Paste the complete `wget` command (with your actual username, password, and Jenkins IP filled in) into **Git Bash** and press Enter. The output is the CRUMB — something like: [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt), [\[183. Build...s+Remotely \| Word\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B2C57A7E2-985E-44AE-99EF-4D5AE99C5333%7D&file=183.%20Build%2BTriggers%2BRemotely.docx&action=default&mobileredirect=true)

    Jenkins-Crumb:8cb80f4f56d6d35c2121a1cf35b7b501

Copy this entire string and paste it into your text editor.

### Step 4.4: Assemble and Execute the Final cURL Command

You now have all three components. The final command template is: [\[183. Build...s+Remotely \| Word\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B2C57A7E2-985E-44AE-99EF-4D5AE99C5333%7D&file=183.%20Build%2BTriggers%2BRemotely.docx&action=default&mobileredirect=true), [\[183. Build...s+Remotely \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.%20Build+Triggers+Remotely.pdf)

```bash
curl -I -X POST http://username:APItoken@JENKINS_IP:8080/job/JOB_NAME/build?token=TOKENNAME -H "Jenkins-Crumb:CRUMB"
```

The instructor fills in each placeholder from the text editor where all values were saved: [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

1.  Replace `username:APItoken` with the `admin:<generated_token>` from Step 4.2.
2.  Replace `@JENKINS_IP:8080/job/JOB_NAME/build?token=TOKENNAME` with the job URL from Step 4.1.
3.  Replace `Jenkins-Crumb:CRUMB` with the CRUMB value from Step 4.3.

**Critical formatting**: No space between the API token and the `@` sign. The instructor catches this: *"No space here."* The entire command must be properly joined. [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

A completed example looks like: [\[183. Build...s+Remotely \| Word\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7B2C57A7E2-985E-44AE-99EF-4D5AE99C5333%7D&file=183.%20Build%2BTriggers%2BRemotely.docx&action=default&mobileredirect=true)

```bash
curl -I -X POST http://admin:110305ffb46e298491ae082236301bde8e@52.15.216.180:8080/job/vprofile-Code-Analysis/build?token=mybuildtoken -H "Jenkins-Crumb:8cb80f4f56d6d35c2121a1cf35b7b501"
```

### Step 4.5: Test It

Note the current build ID in Jenkins (e.g., job ID 3). [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

Copy the assembled `curl` command and paste it into **Git Bash** (or any terminal). Hit Enter.

Go to Jenkins — a new build (job ID 4) should appear, triggered remotely. The instructor confirms: *"Fourth job. That got triggered."* [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

**What this means**: That `curl` command can now be embedded in **any script or automation tool** — Bash, Python, Ruby, Ansible, another Jenkins server, a monitoring system — anywhere. As long as the system has network access to Jenkins, it can trigger the job with full authentication. [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

> ⚠️ **Expert Note (Optional)**
>
> In practice, the CRUMB can expire or change if Jenkins is restarted or if CSRF settings are modified. Some production setups disable CSRF protection for API calls (not recommended) or use Jenkins' newer API token authentication which doesn't require a CRUMB. Also, storing credentials directly in `curl` commands (especially in scripts) is a security risk — in production, use secret management tools (Jenkins credentials binding, HashiCorp Vault, AWS Secrets Manager) to inject credentials at runtime rather than hardcoding them.

***

## Trigger 5: Build After Other Projects Are Built

### Step 5.1: Create a Downstream Test Job

The instructor creates a simple job to serve as the downstream (dependent) job: [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

1.  **Jenkins Dashboard → New Item**.
2.  Name: **`test job`**.
3.  Select: **Freestyle project**.
4.  Click **OK**.
5.  Scroll to **Build Steps** → **Add build step** → **Execute shell**.
6.  Enter:

```bash
echo test test test
```

7.  Click **Save**. [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

This is a minimal job — its only purpose is to demonstrate that it gets triggered automatically.

### Step 5.2: Configure the Downstream Trigger

1.  Go to the **test job** → **Configure** → **Build Triggers**.
2.  Check **"Build after other projects are built"**.
3.  In the **Projects to watch** field, start typing the name of the upstream job (the build job). Jenkins auto-completes: *"See that, it shows the job name."* Select it. [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)
4.  Click **Save**.

### Step 5.3: Test It

Run the **upstream build job** (the main job). When it completes, check its console output — you should see: **"Triggering new build of a test job."** [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

Navigate to the **test job** — it should show a new build (job ID 1), triggered automatically by the upstream job's completion.

The instructor confirms: *"It triggered the test job, if you go to test job, you will see the test job. Job ID one. That got triggered."* [\[183.-Build...ggers-Demo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/183.-Build-Triggers-Demo.txt)

**Connection to the overall system**: This trigger type is how you create **job chains** — build → test → deploy → notify, each as separate jobs that trigger in sequence. While Pipeline-as-Code (Jenkinsfile) handles this within a single pipeline, the "Build after other projects" trigger is useful
