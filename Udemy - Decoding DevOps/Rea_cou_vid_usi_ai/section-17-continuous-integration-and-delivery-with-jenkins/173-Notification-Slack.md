# 📘 Notifications with Slack in Jenkins CI/CD — Deep Learning Material

*Reconstructed from video lecture: [173.-Notification,-Slack.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt?EntityRepresentationId=b00ee525-587b-45b9-a9d7-6f0b71770d21) with pipeline code reference: [173. PAAC\_SlackNotifications.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.%20PAAC_SlackNotifications.txt?EntityRepresentationId=2a702773-c183-4440-ad84-5daa795e8e02)*

***

## 🧠 SECTION 1: THEORY (Deep Learning Mode)

### The Missing Piece: Why Notifications Matter in a CI Pipeline

The lecture opens with a critical observation about the pipeline built so far. The entire continuous integration pipeline — fetching code from GitHub, building with Maven, running unit tests, performing Checkstyle analysis, running SonarQube code analysis, enforcing a quality gate, and publishing artifacts to Nexus — is functionally complete. Every *stage* works. But the pipeline is still missing something at its **start** and at its **end**. [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

At the **start**, the pipeline is triggered manually — someone clicks a button in Jenkins to run it. In a true CI pipeline, the pipeline should trigger **automatically** when a developer makes a commit to the repository. This will be addressed in a future lecture. [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

At the **end**, there is no feedback mechanism. Whether the pipeline passes or fails, nobody is notified. In a real DevOps environment, this is unacceptable. Teams need to know immediately when a build succeeds (so they can proceed with confidence) or when it fails (so they can investigate and fix the issue quickly). **Notifications** are the mechanism that closes this feedback loop, and that is the focus of this lecture. [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

The key insight here is that notifications are not a "nice-to-have" — they are a fundamental part of any production CI/CD pipeline. A pipeline that runs silently and requires someone to manually check its status defeats the purpose of automation.

***

### Jenkins Notification Ecosystem

Jenkins has a rich ecosystem of notification plugins that allow you to send build results to a wide variety of platforms. The lecture demonstrates this by navigating to **Dashboard → Manage Jenkins → Plugins → Available Plugins** and searching for "notification." The results reveal a long list of options: [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

*   **DingTalk** — popular in Chinese tech organizations
*   **Google Chat Notification** — for Google Workspace environments
*   **Webhooks** — generic webhook-based notification
*   **CloudBees Docker Registry** — Docker-related notifications
*   **Slack Upload** — Slack-specific
*   **Jabber** — XMPP-based messaging
*   **Amazon SNS** — AWS Simple Notification Service
*   **Skype** — Microsoft Skype
*   **SMS Notifications** — text message alerts
*   **Zoom** — Zoom Chat integration
*   And many more

The lecture emphasizes that the list "goes on and on." The choice of notification tool depends on what your organization uses for collaboration. In this lecture, **Slack** is chosen. [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

***

### What Is Slack and Why It Matters

The lecture briefly introduces Slack for anyone unfamiliar: it is a very popular collaboration tool used widely in the IT industry. At its core, it functions like a chat application, but it goes far beyond simple messaging — you can send files, integrate with external services (like Jenkins), organize conversations into **channels**, and build automated workflows. [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

Two Slack concepts are essential for this integration:

**Workspace** — A workspace represents your organization or team. It is the top-level container in Slack. When you create a Slack account, you create or join a workspace. The workspace has a unique name (e.g., `hkhinfotech`) and a corresponding URL (e.g., `hkhinfotechworkspace.slack.com`). [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

**Channel** — Within a workspace, communication happens in channels. A channel is a dedicated space for a specific topic, project, or team. You can add colleagues to a channel and everyone in it can see the messages. For this integration, a channel named `devopscicd` is created (or used) to receive Jenkins build notifications. [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

> 🔍 **Deep Dive (Optional)**
>
> Slack channels can be public (anyone in the workspace can join) or private (invite-only). For CI/CD notifications, a dedicated channel is the standard practice — it keeps build noise separate from general team discussions. In larger organizations, you might have separate channels for different pipelines, environments (dev, staging, prod), or severity levels.

***

### The Integration Model: Jenkins → Slack

For Jenkins to send messages to a Slack channel, a trust relationship must be established. This works through a **Slack App** — specifically, the **Jenkins CI** app available in the Slack App Marketplace. When you install this app into your Slack workspace and associate it with a channel, Slack generates a **token**. This token is what Jenkins uses to authenticate when sending messages. [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

The integration flow is:

1.  Install the **Slack Notification** plugin in Jenkins (gives Jenkins the ability to send Slack messages)
2.  Install the **Jenkins CI** app in Slack (gives Slack the ability to receive from Jenkins)
3.  Associate the app with a specific channel and obtain a **token**
4.  Store the token in Jenkins as a credential
5.  Configure the Slack workspace name and channel in Jenkins system settings
6.  Reference the channel and use the `slackSend` step in your pipeline code [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

This is a one-time setup. Once configured, any pipeline in that Jenkins instance can send notifications to the configured Slack channel (or any other channel, if specified in the pipeline code).

***

### Notification as a Post Action, Not a Stage

A crucial conceptual point the lecture makes is that **notification is not an extra stage**. It is a **post action** (referred to as "post installation step" in the lecture). [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

In a Jenkinsfile, stages are the sequential blocks of work: fetch code, build, test, analyze, publish. These are the *tasks* of the pipeline. But notifications are different — they are **meta-actions** that report on the outcome of those tasks. Regardless of whether the pipeline succeeds or fails, you want the notification to fire. If you placed it as a regular stage, it would only execute if all preceding stages passed. By placing it in the `post` block **outside of all stages**, it runs after the pipeline completes, no matter the result. [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

The `post` block sits at the same level as the `stages` block — inside the `pipeline` block but not inside any individual stage. Within `post`, the `always` block ensures the notification code executes in every scenario: success, failure, unstable, or aborted. [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

***

### The COLOR\_MAP Function: Dynamic Color Coding

The lecture introduces a Groovy map (function) called `COLOR_MAP` that drives the visual feedback in Slack notifications. Slack messages can include a colored sidebar — **green** for success, **red** for failure — providing an instant visual indicator. [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

The `COLOR_MAP` is defined **before** the `pipeline` block (at the top of the Jenkinsfile) and maps Jenkins build results to Slack color values:

```groovy
def COLOR_MAP = [
    'SUCCESS': 'good',
    'FAILURE': 'danger',
]
```

 [\[173. PAAC_...ifications \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.%20PAAC_SlackNotifications.txt)

*   `'SUCCESS'` maps to `'good'` — which Slack renders as **green**
*   `'FAILURE'` maps to `'danger'` — which Slack renders as **red**

The lecture explains the flow clearly: `currentBuild.currentResult` returns the string `SUCCESS` or `FAILURE`. This string is passed as a key to `COLOR_MAP`, which returns either `good` or `danger`. That returned value is then passed to the `color` parameter of `slackSend`, and Slack renders the appropriate color. [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

> 🔍 **Deep Dive (Optional)**
>
> `COLOR_MAP` is a standard Groovy Map (key-value data structure), not technically a "function" in the strict sense — it's a variable holding a map literal. When you access `COLOR_MAP['SUCCESS']`, Groovy looks up the key `'SUCCESS'` and returns the value `'good'`. The `def` keyword in Groovy declares a variable. Placing this outside the `pipeline` block makes it available as a script-level variable accessible throughout the Jenkinsfile.

***

### The slackSend Step: Anatomy of the Notification

The actual notification is sent using the `slackSend` pipeline step, which is provided by the Slack Notification plugin. It accepts three key parameters in this usage: [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

```groovy
slackSend channel: '#devopscicd',
    color: COLOR_MAP[currentBuild.currentResult],
    message: "*${currentBuild.currentResult}:* Job ${env.JOB_NAME} build ${env.BUILD_NUMBER} \n More info at: ${env.BUILD_URL}"
```

 [\[173. PAAC_...ifications \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.%20PAAC_SlackNotifications.txt)

**`channel`** — Specifies which Slack channel receives the message. The `#` prefix is standard Slack channel notation. This must match an actual channel in your workspace. [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

**`color`** — The sidebar color of the Slack message. As explained above, this is dynamically resolved through `COLOR_MAP[currentBuild.currentResult]`. [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

**`message`** — The text content of the notification. The lecture constructs a message that includes:

*   `currentBuild.currentResult` — the build outcome (SUCCESS or FAILURE), wrapped in `*...*` for bold formatting in Slack
*   `env.JOB_NAME` — the name of the Jenkins job/pipeline
*   `env.BUILD_NUMBER` — the build number
*   `env.BUILD_URL` — a clickable link back to the Jenkins build page for checking logs

The lecture notes that you can construct this message however you want and include whatever variables you like — this is just one useful pattern. [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

***

### What Comes Next: The Bigger Picture

The lecture closes by placing this work in context. With notifications added, the continuous integration pipeline now has all its functional components. The next focus area is **automatic triggering** (making the pipeline run on commits rather than manual clicks) and then **containerization** — not just publishing the WAR artifact to Nexus, but building **Docker images** with the artifact inside them and publishing those images. This marks the transition from pure CI into the container-based delivery workflow. [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

***

## ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

### What We Are Building

In this practical section, we are adding **Slack-based notifications** to an existing Jenkins CI pipeline. When the pipeline finishes — whether it succeeds or fails — a message will be automatically sent to a Slack channel with the build result, job name, build number, and a link to the Jenkins build page. Success messages appear with a green sidebar; failure messages appear with a red sidebar. [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

This is the final functional piece of the CI pipeline. After this, the pipeline will not only execute all stages (fetch, build, test, analyze, quality gate, publish) but also **report its outcome** to the team in real time.

***

### Step 1: Install the Slack Notification Plugin in Jenkins

We need the Slack Notification plugin so Jenkins gains the ability to send messages to Slack. [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

**Navigate to:** Dashboard → **Manage Jenkins** → **Plugins** → **Available Plugins**

Search for `Slack Notification`. Find the plugin in the results, put a **check mark** next to it, and click **Install**. [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

This plugin provides the `slackSend` pipeline step that we will use in our Jenkinsfile. Without it, Jenkins has no built-in capability to communicate with Slack.

***

### Step 2: Create a Slack Account and Workspace

If you don't already have a Slack account, you need to create one. [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

1.  Search for **Slack login** in your browser
2.  Click **Sign up** (the lecture uses **Continue with Google** for convenience)
3.  After logging in, you'll see the option to **Create a workspace**

**Configure the workspace:**

*   **What's the name of your company or team?** — Enter your workspace name (e.g., `hkhinfotech`). This name represents your project or organization. [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)
*   **What's your name?** — Enter your display name (e.g., `Hkh admin`)
*   **Add your team** — You can add team members' email addresses or **Skip this step** for now
*   **What's your team working on right now?** — Enter a channel name: `devopscicd`. Click **Next**. [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

After completing setup, you'll have:

*   A **workspace** (e.g., `hkhinfotech`) — this is the top-level container
*   A **channel** (e.g., `devopscicd`) — this is where notifications will be delivered [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

Take note of both names — you will need them when configuring Jenkins.

***

### Step 3: Install the Jenkins CI App in Slack and Get the Token

For Slack to accept messages from Jenkins, we need to install the **Jenkins CI** app inside Slack and generate an authentication token. [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

1.  In your browser, search for **Slack apps**

2.  You should find the **Slack App Marketplace** (add apps to Slack)

3.  Search for **Jenkins**

4.  Find **Jenkins CI** and click **Add to Slack** [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

5.  **Select a channel** — choose the channel you created earlier (`devopscicd`)

6.  Click **Add Jenkins CI integration** [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

7.  A configuration page appears with many steps. Scroll down until you find the **Token** field.

8.  **Copy the token** — this is the authentication credential Jenkins will use to send messages [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

9.  Click **Save settings**

The lecture recommends temporarily saving the token in a sticky note or text editor, because you'll need to paste it into Jenkins in the next step. [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

**Also note the workspace identifier:**
Go back to the Slack app, click the dropdown in the top-left corner. You'll see the workspace URL. The part you need is the subdomain portion — for example, from `hkhinfotechworkspace.slack.com`, you need `hkhinfotechworkspace`. Do **not** include `.slack.com`. [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

***

### Step 4: Configure Slack Integration in Jenkins System Settings

Now we connect Jenkins to Slack by providing the workspace name, the token, and the default channel. [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

**Navigate to:** Manage Jenkins → **System**

Scroll down to find the **Slack** section (usually near the bottom of the page). [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

**Configure the following fields:**

**Workspace:** Paste the workspace identifier you copied (e.g., `hkhinfotechworkspace`). Remember — only the subdomain part, **not** the full `.slack.com` URL. [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

**Credential (Token):** Click **Add** → **Jenkins** to create a new credential:

*   **Kind**: Select **Secret text** (appropriate for a single token value)
*   **Secret**: Paste the token you copied from the Slack Jenkins CI app configuration page
*   **ID**: `slacktoken`
*   **Description**: `slacktoken`
*   Click **Add** [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

⚠️ **Critical:** After creating the credential, you must **manually select it** from the dropdown. It will not be auto-selected. The lecture demonstrates this exact mistake — testing the connection without selecting the credential first results in a "no credential" error. [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

**Default channel:** Enter `#devopscicd` (the channel name with the `#` prefix). [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

**Test the connection:** Click **Test Connection**. If everything is configured correctly, it will report **Success**. You will also see a test message appear in your Slack channel — confirming the end-to-end connectivity works. [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

Click **Save**.

***

### Step 5: Add the Notification Code to the Pipeline

Now we add the actual notification logic to the Jenkinsfile. This involves two pieces of code: the `COLOR_MAP` definition at the top, and the `post` block at the bottom. [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

#### 5a. Define the COLOR\_MAP (Top of Jenkinsfile)

Place this **before** the `pipeline {` block — at the very top of the file: [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

```groovy
def COLOR_MAP = [
    'SUCCESS': 'good',
    'FAILURE': 'danger',
]
```

 [\[173. PAAC_...ifications \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.%20PAAC_SlackNotifications.txt)

This creates a Groovy map that translates Jenkins build result strings into Slack color codes. `'good'` renders as green in Slack; `'danger'` renders as red. [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

#### 5b. Add the Post Block (After All Stages)

The `post` block goes **outside** of the `stages { }` block but **inside** the `pipeline { }` block. Structurally: [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

```groovy
pipeline {
    agent any
    stages {
        // ... all your stages ...
    }
    post {
        always {
            echo 'Slack Notifications.'
            slackSend channel: '#devopscicd',
                color: COLOR_MAP[currentBuild.currentResult],
                message: "*${currentBuild.currentResult}:* Job ${env.JOB_NAME} build ${env.BUILD_NUMBER} \n More info at: ${env.BUILD_URL}"
        }
    }
}
```

 [\[173. PAAC_...ifications \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.%20PAAC_SlackNotifications.txt)

Let's break down every component:

**`post { }`** — This block defines actions that run **after** all stages complete, regardless of which stage was the last to execute. [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

**`always { }`** — Inside `post`, the `always` block guarantees execution in every scenario — success, failure, unstable, or aborted. This is essential because you want notifications for *all* outcomes, not just successes. [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

**`echo 'Slack Notifications.'`** — A simple print statement to the Jenkins console log, confirming that the notification step is being executed. This is useful for debugging if notifications stop working. [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

**`slackSend`** — The pipeline step provided by the Slack Notification plugin. Its parameters:

*   **`channel: '#devopscicd'`** — The target Slack channel. Must match an actual channel in your workspace. The `#` prefix is standard Slack notation. [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

*   **`color: COLOR_MAP[currentBuild.currentResult]`** — Dynamically resolves the color. `currentBuild.currentResult` returns `SUCCESS` or `FAILURE`. This is used as a key in `COLOR_MAP`, returning `good` (green) or `danger` (red). [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

*   **`message:`** — The notification text. The message uses Groovy string interpolation (`${...}`) to embed dynamic values:
    *   `*${currentBuild.currentResult}:*` — Build result in **bold** (Slack uses `*...*` for bold)
    *   `Job ${env.JOB_NAME}` — The pipeline/job name
    *   `build ${env.BUILD_NUMBER}` — The build number
    *   `\n More info at: ${env.BUILD_URL}` — A newline followed by a clickable link to the Jenkins build page [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

> ⚠️ **Expert Note**
>
> The channel name in the `slackSend` step must be **exactly correct**. The lecture demonstrates a real debugging scenario: the notification failed because the channel name had an extra letter `S` (`devopscicds` instead of `devopscicd`). The pipeline itself showed the post action running, but the Slack message never arrived. The fix was simply correcting the typo in the pipeline code. Always double-check channel names — typos in channel names fail silently (no error in Jenkins, just no message in Slack). [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

***

### Step 6: Testing a Successful Build Notification

To test, the lecture uses the existing **Vprofile-CI-Pipeline** job: [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

1.  Navigate to the job → **Configure**
2.  Replace the entire pipeline script with the new code (which includes all existing stages plus the `COLOR_MAP` and `post` block)
3.  Verify the channel name is correct
4.  **Save** and **Build Now**

After the pipeline completes successfully, check the Slack channel. You should see a message with:

*   A **green sidebar** (indicating success)
*   The text: **SUCCESS:** Job \[job-name] build \[build-number]
*   A link to the Jenkins build URL [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

The lecture confirms this works — the green-colored success message appears in the `devopscicd` channel with a clickable URL for checking logs. [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

***

### Step 7: Testing a Failed Build Notification

To verify that failure notifications also work (with red color), the lecture intentionally creates a stage that will fail: [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

```groovy
stage('test slack'){
    steps{
        sh 'NotARealCommand'
    }
}
```

 [\[173. PAAC_...ifications \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.%20PAAC_SlackNotifications.txt)

This stage runs `NotARealCommand` in the shell. Since this is not a real command, the shell returns "command not found," which causes the stage to fail, which causes the entire pipeline to fail. The `post` → `always` block still executes, and the notification is sent with the `FAILURE` result. [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

The lecture creates a **new pipeline** for this test (rather than modifying the existing one):

1.  **New Item** → name it `slackTest` → select **Pipeline** → **OK**
2.  Paste the full pipeline code (with the fake failing stage included at the beginning)
3.  **Save** and **Build Now** [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

The pipeline fails at the `test slack` stage (as expected). Check the Slack channel — you should see:

*   A **red sidebar** (indicating failure)
*   The text: **FAILURE:** Job slackTest build \[build-number] [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

This confirms the full notification system works bidirectionally — green for success, red for failure.

> 🔍 **Deep Dive (Optional)**
>
> The reason the notification still fires even when the pipeline fails is entirely due to the `always` block inside `post`. Jenkins has several conditional post blocks: `always` (runs no matter what), `success` (runs only on success), `failure` (runs only on failure), `unstable`, `changed`, etc. By using `always`, we guarantee the notification fires regardless of outcome. If you wanted *different* messages for success vs. failure (not just different colors, but different text), you could use separate `success { }` and `failure { }` blocks inside `post`.

***

### Connection to the Overall System

With Slack notifications in place, the CI pipeline now has a complete feedback loop: [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

*   ✅ **Code Fetch** (GitHub) → **Build** (Maven) → **Unit Test** (Maven) → **Checkstyle** (Maven) → **SonarQube Analysis** → **Quality Gate** → **Publish to Nexus** → **Slack Notification** [\[173. PAAC_...ifications \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.%20PAAC_SlackNotifications.txt)

Two things remain before this pipeline is truly production-grade:

1.  **Automatic triggering** — replacing manual "Build Now" clicks with automatic builds on Git commits (covered in a future lecture) [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)
2.  **Containerization** — beyond publishing WAR artifacts to Nexus, the next phase involves building **Docker images** containing the artifact and publishing those images. This transitions the workflow from traditional artifact management into container-based delivery. [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt)

***

### Full Pipeline Code Reference

For completeness, here is the entire pipeline as shown in the resource file, with all stages and the notification system integrated: [\[173. PAAC_...ifications \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.%20PAAC_SlackNotifications.txt)

```groovy
def COLOR_MAP = [
    'SUCCESS': 'good',
    'FAILURE': 'danger',
]

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
    }
    post {
        always {
            echo 'Slack Notifications.'
            slackSend channel: '#devopscicd',
                color: COLOR_MAP[currentBuild.currentResult],
                message: "*${currentBuild.currentResult}:* Job ${env.JOB_NAME} build ${env.BUILD_NUMBER} \n More info at: ${env.BUILD_URL}"
        }
    }
}
```

*(Note: The `test slack` stage with `NotARealCommand` was only used for testing failure notifications and is not part of the production pipeline.)* [\[173.-Notif...ion,-Slack \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.-Notification,-Slack.txt), [\[173. PAAC_...ifications \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/173.%20PAAC_SlackNotifications.txt)
