# 📘 GitHub Actions Quickstart — Part 2: Debugging, Artifacts, Environments, Secrets & Variables — Deep Learning Material

*Reconstructed from video lecture: [187-quickstart-part-2.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt?EntityRepresentationId=b7107013-ec26-4deb-9359-9e238d7f7edb)* [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

***

## 🧠 SECTION 1: THEORY (Deep Learning Mode)

### The Runtime Nature of GitHub Actions Runners

The lecture reveals a critically important characteristic of GitHub Actions that fundamentally shapes how you design workflows: **runners are ephemeral**. When you specify `runs-on: ubuntu-latest`, GitHub provisions a fresh virtual machine, sets up the runner software, downloads any actions you reference (like `actions/checkout`), and executes your job. The moment the job completes — success or failure — **everything built on that runner is destroyed**. The VM is torn down. Files, build artifacts, compiled binaries, downloaded dependencies — all gone. [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

This is not a side effect; it is by design. Each job starts from a completely clean state, which guarantees reproducibility (no leftover state from previous builds) and security (no credential leakage between jobs). But it creates a practical challenge: if you build something valuable during a job (like a compiled application, a WAR file, a Docker image), you must **explicitly extract and store it** before the job ends. This is where **artifacts** come in — the lecture mentions that you can define artifacts in your workflow, and then you can see and download them from the Actions UI. Without explicitly defining artifact storage, your build output simply vanishes. [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

The lecture also shows what happens automatically behind the scenes when a job starts. Clicking into a completed job reveals steps the runner performs on its own: "Set up job" shows the current runner version, runner image, provisioner, and operating system details. It also downloads the actions you referenced (like `actions/checkout`). You did not write these setup steps — the runner handles them automatically. Your defined steps (like code checkout and Maven build) execute after this automatic setup completes. [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

> 🔍 **Deep Dive (Optional)**
>
> The phrase "ubuntu-latest" is resolved by GitHub to a specific runner image at execution time. The image comes pre-loaded with common tools (Git, Docker, various language runtimes), but the exact tool versions can change as GitHub updates the image. This means a workflow that works today might behave differently months later if a pre-installed tool version changes. For production stability, some teams pin to a specific runner image version rather than using `latest`.

***

### Workflow Structure Recap: Workflow → Jobs → Steps

The lecture reinforces the structural hierarchy through direct observation of a running workflow. When you click on a workflow run in the Actions tab, you see the **jobs** defined in that workflow — in this case, `build` and `testing`. Clicking into a job reveals its **steps**: both the ones you defined (code checkout, Maven build) and the ones the runner adds automatically (set up job, download actions, post-cleanup). [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

The important conceptual point here is that **what you write** in your YAML file and **what actually executes** on the runner are not identical. The runner wraps your steps with its own infrastructure steps. Understanding this distinction matters when debugging — a failure in "Set up job" means something is wrong with the runner or action resolution, while a failure in your named step means something is wrong with your code or commands.

***

### Action Versioning: A Critical Source of Failure

Actions in GitHub Actions are versioned using Git tags (e.g., `v4`, `v5`). When you reference `actions/checkout@v4`, you are telling GitHub to fetch version 4 of the checkout action from its repository. The lecture demonstrates what happens when you reference a **non-existent version**: specifying `actions/checkout@v16` causes the workflow to fail immediately with "unable to resolve action — unable to find version v16." [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

This failure happens **before any of your steps execute**. The runner cannot even set up the job because it cannot download the action it needs. The error is clear, but the root cause is important to understand: action versions are not arbitrary numbers you choose — they must correspond to actual tagged releases in the action's GitHub repository. [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

The lecture makes a pointed real-world observation: **when using AI tools (ChatGPT, Copilot, Amazon Q, etc.) to generate workflow code, the version numbers are frequently wrong.** This is the instructor's personal experience. AI tools may hallucinate version numbers that don't exist, or reference outdated versions. The solution is to always verify action versions by going to the **GitHub Marketplace**, searching for the action (e.g., "checkout"), and checking the current version in the documentation or example code. The lecture demonstrates this: the marketplace shows `checkout` with `v4` in one place and `v5` in the example — both work, but you need to verify. [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

> ⚠️ **Expert Note**
>
> Version tags like `v4` and `v5` are **major version** tags. Action maintainers also publish more specific tags (e.g., `v4.1.7`). Using a major version tag means you automatically get patch and minor updates within that major version. Using a precise tag gives you exact reproducibility but requires manual updates. For most workflows, major version tags are sufficient.

***

### Trigger Mechanics: Push on Main Branch

The lecture confirms the trigger behavior configured in Part 1: the workflow is set to run "when there is a push on the main branch," and the working branch is the main branch. Therefore, **every commit and push to main automatically triggers the workflow**. This is demonstrated repeatedly — every time the instructor saves changes and pushes, the workflow appears in the Actions tab and begins executing. [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

This is the fundamental CI trigger pattern: code change → automatic pipeline execution → immediate feedback. The feedback loop is tight — push, wait, see results.

***

### Debugging Failed Workflows

The lecture deliberately introduces two errors to teach debugging. This is one of the most valuable sections because real-world workflows fail frequently, and knowing how to diagnose failures quickly is an essential skill. [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

**Error 1: Invalid action version (`checkout@v16`)**
The workflow fails at the infrastructure level — the runner cannot resolve the action. The error message is: "unable to resolve action — unable to find version v16." This error appears in the job's output when you click into the failed job. The fix: go to the GitHub Marketplace, find the correct version, and update the workflow. [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

**Error 2: Invalid command (`maven` instead of `mvn`)**
After fixing the version error, the workflow progresses further but fails at the testing job. The command `maven test` fails because the correct command is `mvn test` — there is no binary called `maven` on the runner, only `mvn`. The error message is clear: "maven: command not found." [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

The lecture highlights an important debugging navigation pattern: **you can see failure indicators at the workflow level** (a red X next to the run), but for detailed information, **you must click into the specific job and then into the specific step that failed**. The step-level view shows the exact error message and the exact point of failure. [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

> 🔍 **Deep Dive (Optional)**
>
> The two errors demonstrate two fundamentally different failure categories. The version error is an **infrastructure-level failure** — the job cannot even start because a dependency cannot be resolved. The command error is a **runtime failure** — the job starts successfully, but a step fails during execution. Distinguishing between these categories speeds up debugging: if the job never starts, look at action references and runner configuration; if a specific step fails, look at the commands and their environment.

***

### Environments: Infrastructure-Aware Configuration

GitHub Actions supports **environments** — named contexts that represent infrastructure deployment targets like `dev`, `QA`, `staging`, and `production`. Environments are created in the repository's **Settings → Environments** section. [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

The core problem environments solve is **configuration variation across deployment targets**. A workflow may use the same variable name (e.g., `DATABASE_URL`), but its value differs depending on whether you're deploying to dev or production. Without environments, you would need separate workflow files or complex conditional logic. With environments, you define the variable once per environment, use the same variable name in your workflow, and the correct value is injected based on which environment the job targets. [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

Environments also carry **protection rules** that control which jobs can access them: [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

*   **No restriction** — any job in any workflow can use this environment's variables and secrets
*   **Protected branches only** — only jobs triggered from protected branches (like `main`) can use this environment. Since protected branches typically require pull request reviews before merging, this ensures production secrets are only accessible through reviewed code paths
*   **Specific branches and tags** — you define an explicit list of branches and tags that can access this environment [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

> 🔍 **Deep Dive (Optional)**
>
> The protection rule mechanism creates a security boundary between your code and your sensitive configuration. Even if someone creates a rogue branch with a workflow that references the `production` environment, the protection rules prevent that branch from accessing production secrets. This is a critical security feature for organizations where multiple developers can push code.

***

### Secrets vs. Variables: Encrypted vs. Plaintext Configuration

Within each environment (and also at the repository level), you can store two types of configuration data: **secrets** and **variables**. [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

**Secrets** are for sensitive data — access keys, passwords, tokens, private keys. They are stored **encrypted**. Once saved, the value **cannot be viewed again** — not even by the person who created it. If you go to edit a secret, you can only **update** the value; you cannot see the current value. This is a deliberate security measure: secrets are write-only from the UI perspective. In workflows, secret values are masked in logs to prevent accidental exposure. [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

**Variables** are for non-sensitive configuration — feature flags, service URLs, version numbers, region names. They are stored as **plaintext**. You can view, edit, and update their values at any time. [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

The lecture demonstrates the behavioral difference: editing a secret shows an empty value field (you can replace but not read); editing a variable shows the current value and lets you modify it. [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

Both secrets and variables are called in your workflow using special syntax (e.g., `${{ secrets.SECRET_NAME }}` and `${{ vars.VARIABLE_NAME }}`), which will be used in upcoming lectures.

***

### The Broader GitHub Actions Ecosystem

The lecture closes by pointing to the larger ecosystem of pre-built workflows available in GitHub Actions. Navigating to **Actions → New Workflow** reveals a catalog of starter workflows for various use cases: Docker image builds, deployments to ECS, GKE, OpenShift, Octopus Deploy, and many more. The instructor notes that when first learning GitHub Actions, studying these sample workflows with their different settings was a primary learning method. [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

The lecture also acknowledges that AI coding assistants (ChatGPT, Copilot, Amazon Q) can now generate workflow code, but emphasizes that **hands-on understanding of workflow mechanics and settings** should come before relying on AI-generated code — especially given the version accuracy issues mentioned earlier. [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

***

## ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

### What We Are Building

In this practical section, we are **exploring, debugging, and extending** a GitHub Actions workflow that was created in Part 1. We deliberately break the workflow in two different ways, diagnose the failures, fix them, and then set up **environments, secrets, and variables** in the repository settings. By the end, you understand how to navigate workflow results, debug failures at different levels, find correct action versions, and configure environment-scoped secrets and variables for use in future workflows. [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

The upcoming lectures will use this foundation to build meaningful workflows: cloning source code, building, testing, building Docker images, and uploading them to Amazon ECR. [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

***

### Step 1: Examining the Completed Workflow Run

After the workflow from Part 1 completes successfully, navigate to the **Actions** tab in your GitHub repository. You see all workflow runs listed. Click on the completed workflow run. [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

You'll see the jobs defined in the workflow — in this case, **build** and **testing**. Click on the **build** job to see its detailed output. [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

Inside the job, you'll see multiple steps:

*   **Set up job** — automatically added by the runner. Shows the runner version, runner image, provisioner, and OS. Also downloads referenced actions (e.g., `actions/checkout`). You did not write this step.
*   **Code Checkout** — your first defined step. Clones the source code.
*   **Maven Build** — your second defined step. Runs the Maven build command.
*   Additional auto-generated steps (post-cleanup, etc.) [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

**Key observation:** The runner handles all infrastructure setup automatically. You only defined two steps (checkout and build), but the runner added its own steps around them. Everything running on this VM is **ephemeral** — it is destroyed when the job completes. If you need to preserve build outputs, you must define artifacts explicitly. [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

**Verify the workflow file in your repository:** Navigate to your repository's code. You should see a `.github/workflows` directory containing your workflow YAML file. The file shows the trigger configuration (push on main branch) confirming that every push to main triggers this workflow. [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

***

### Step 2: Introduce Error 1 — Wrong Action Version

To learn debugging, we deliberately introduce a version error. Edit the workflow file and change the checkout action version to a non-existent version: [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

```yaml
- uses: actions/checkout@v16
```

This version does not exist. Also introduce a second error (we'll observe both): change `mvn` to `maven` in the test command: [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

```yaml
- run: maven test
```

Save, commit, and push. The push to main triggers the workflow automatically. [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

***

### Step 3: Diagnose the First Failure

Navigate to **Actions**. The workflow run shows a failure (red X). Click into it. The **build** job has failed. Click into the build job. [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

The error message reads: **"Unable to resolve action — unable to find version v16."** [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

This failure occurs **before any of your steps execute**. The runner tried to download `actions/checkout@v16` and could not find it. The job never started.

**How to find the correct version:**

1.  Go to the **GitHub Marketplace** (github.com/marketplace)
2.  Search for `checkout`
3.  Find the `actions/checkout` action
4.  Check the current version — the documentation or examples will show the correct tag (e.g., `v4` or `v5`) [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

The lecture verifies that both `v4` (used in Part 1) and `v5` (shown in the marketplace example) work. [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

**Fix:** Change the version to `v5`:

```yaml
- uses: actions/checkout@v5
```

Save, commit, and push. [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

***

### Step 4: Diagnose the Second Failure

After fixing the version, the workflow triggers again. This time, the **build** job (or whichever job uses checkout) succeeds — `v5` resolves correctly. But the **testing** job fails. [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

**Navigation pattern for debugging:** Before clicking into the job, you can already see a failure indicator at the workflow level. But for detail, click into the **testing** job, then click on the **specific step** that failed. [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

The error: **"maven: command not found"** [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

The correct binary name is `mvn`, not `maven`. The runner has Maven installed, but the executable is called `mvn`.

**Fix:** Change the command back to the correct form:

```yaml
- run: mvn test
```

Save, commit, and push. The workflow triggers again and this time completes successfully. [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

> ⚠️ **Expert Note**
>
> The lecture uses these errors to make a broader point: **AI-generated workflow code frequently contains wrong version numbers.** Always verify action versions against the GitHub Marketplace before trusting generated code. This applies to ChatGPT, GitHub Copilot, Amazon Q, and any other coding assistant. [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

***

### Step 5: Set Up an Environment

Navigate to your repository's **Settings** (not the account settings — the repository settings). In the left sidebar, find **Environments** (accessible via Settings → Secrets and variables → Actions → Environments link, or directly under Settings). [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

Click **"New environment."** Enter a name — the lecture uses `production`. Click **"Configure environment."** [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

You now see environment settings: [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

*   **No restriction** (default) — any job can use this environment
*   **Protected branches only** — only jobs from protected branches (like main) can access it
*   **Selected branches and tags** — you define an explicit allowlist

For now, leave the default (no restriction). The important thing is that the environment exists — it serves as a container for environment-specific secrets and variables. [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

***

### Step 6: Store a Secret in the Environment

Scroll down in the environment configuration page. Click **"Manage environment secrets"** (or the "Add secret" button). Select your environment. [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

*   **Name** — enter a name for the secret (e.g., `AWS_ACCESS_KEY`)
*   **Value** — enter the secret value (e.g., the actual access key)
*   Click **"Add secret"** [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

The secret is now stored encrypted. If you return to edit it, **you cannot see the current value** — you can only replace it with a new value. This is the encrypted storage behavior: write-only from the UI. [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

***

### Step 7: Store a Variable in the Environment

Similarly, click **"Add variable"** (or navigate to the variables tab). [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

*   **Name** — enter a variable name (e.g., `DEPLOY_REGION`)
*   **Value** — enter the value (e.g., `us-east-1`)
*   Click **"Add variable"** [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

Unlike secrets, if you return to edit this variable, **you can see its current value** and modify it. Variables are plaintext — suitable for non-sensitive configuration only. [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

**Connection to the overall system:** Secrets and variables stored here will be referenced in workflow YAML files in upcoming lectures using `${{ secrets.SECRET_NAME }}` and `${{ vars.VARIABLE_NAME }}` syntax. The environment scoping ensures the correct values are injected based on which environment a job targets.

***

### Step 8: Explore Sample Workflows

Navigate to **Actions → New Workflow**. GitHub presents a catalog of starter workflows organized by use case: Docker image builds, deployments to ECS, GKE, OpenShift, Octopus Deploy, and many more. [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

Click **"Configure"** on any of them (e.g., "Docker image") to see the workflow YAML — but **do not commit** anything. Just study the structure, settings, triggers, and steps used. Click **"Cancel changes"** when done. [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

This is a recommended learning exercise: browse different workflows, observe their patterns, and build familiarity with the range of GitHub Actions capabilities before the upcoming hands-on lectures. [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)

***

## 🧠 SECTION 3: MENTAL COMPRESSION MAP

### System Architecture

    GitHub Repository
    ├── .github/workflows/
    │   └── workflow.yml          ← trigger: push on main
    │
    ├── Settings
    │   ├── Environments
    │   │   └── production
    │   │       ├── Secrets (encrypted, write-only view)
    │   │       └── Variables (plaintext, readable)
    │   └── Protection Rules
    │       ├── No restriction
    │       ├── Protected branches only
    │       └── Selected branches/tags
    │
    └── Actions Tab
        └── Workflow Runs
            └── Jobs (build, testing)
                └── Steps (auto + user-defined)

***

### Execution Flow

    Push to main
      → GitHub provisions runner (ubuntu-latest)
        → Runner auto-setup (version, image, OS)
          → Downloads referenced actions (checkout@v5)
            → Executes user-defined steps (checkout → build → test)
              → Job completes
                → Runner VM DESTROYED (ephemeral)
                  → Artifacts survive ONLY if explicitly defined

***

### Failure Taxonomy

    Failure Type 1: INFRASTRUCTURE (before steps execute)
      Cause: Invalid action version, runner unavailable
      Signal: "unable to resolve action"
      Fix: Verify version in GitHub Marketplace
      
    Failure Type 2: RUNTIME (during step execution)
      Cause: Wrong command, missing tool, code error
      Signal: "command not found", exit code != 0
      Fix: Check command syntax, tool availability on runner

**Debug navigation:** Workflow run (overview) → Job (which job failed) → Step (exact failure point + error message)

***

### Secrets vs Variables

                    Secrets              Variables
    Storage:        Encrypted            Plaintext
    View after      NO (write-only)      YES (read/write)
      save:
    Use case:       Keys, passwords,     Regions, URLs,
                    tokens               feature flags
    Workflow        ${{ secrets.NAME }}  ${{ vars.NAME }}
      syntax:

***

### Environment Protection Chain

    Environment (e.g., "production")
      │
      ├── No restriction → any job, any branch
      ├── Protected branch only → main (requires PR review) → secrets accessible
      └── Selected branches/tags → explicit allowlist → secrets accessible

**Core security idea:** Environments gate access to secrets based on *which code path* triggered the workflow.

***

### Key Engineering Patterns

**Ephemeral Compute Pattern**
Runner = disposable VM. Clean state in, destroyed after. Artifacts must be explicitly extracted. No state leaks between runs.

**Version Resolution Pattern**
`action@tag` → GitHub resolves tag → downloads action. Non-existent tag = hard failure before execution. Always verify against Marketplace, never trust AI-generated versions.

**Configuration Scoping Pattern**
Same variable name → different values per environment. Workflow code stays constant; environment injects correct config at runtime.

**Write-Only Secret Pattern**
Secrets: store encrypted → cannot read back → can only replace. Prevents UI-based exfiltration. Logs mask secret values automatically.

***

### Upcoming System Extension

    Current:  Checkout → Build → Test (basic CI)
        ↓
    Next:     Checkout → Build → Test → Docker Build → Push to ECR (container CI/CD)

Foundation established: workflow mechanics, debugging, environments, secrets/variables → ready for real deployment pipelines. [\[187-quicks...art-part-2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/187-quickstart-part-2.txt)
