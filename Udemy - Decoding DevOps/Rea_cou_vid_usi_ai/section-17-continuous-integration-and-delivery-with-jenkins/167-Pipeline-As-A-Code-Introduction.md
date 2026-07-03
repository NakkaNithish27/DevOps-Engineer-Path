# Pipeline as a Code — Introduction & First Pipeline Build

> **Source**: [167.-Pipeline-As-A-Code-Introduction.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt?EntityRepresentationId=2b1cbbed-d6da-49cb-bfe5-bfa29fd930d3) (caption transcript) + [167. PipelineCodeDemo.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.%20PipelineCodeDemo.txt?EntityRepresentationId=99dcb6d2-2c36-4cc5-a7df-ebf2e57bf54e) (pipeline code resource) [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt), [\[167. Pipel...neCodeDemo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.%20PipelineCodeDemo.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1. Pipeline as a Code — The Core Idea

**Pipeline as a Code** is Jenkins' approach to defining your entire CI/CD pipeline not through the GUI (clicking buttons, filling forms), but through a **text file called a Jenkinsfile** (capital **J**). This file contains all the instructions Jenkins needs to automatically set up and execute your pipeline. [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)

The fundamental problem it solves is **manual, fragile, GUI-dependent pipeline configuration**. In traditional Jenkins, you create a "freestyle" job by filling in forms — selecting Git, typing a branch name, choosing build steps, adding post-build actions. This works, but it has critical weaknesses: it's not version-controlled, it's hard to reproduce, it can't be reviewed in a pull request, and it doesn't travel with your source code. Pipeline as a Code eliminates all of these problems by moving the pipeline definition into a file that lives **inside your source code repository** or can be written directly into the Jenkins job configuration. [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)

The Jenkinsfile defines the **stages** in your CI/CD pipeline. Every job you create in Jenkins will have its stages defined inside this file — fetching code, building, testing, deploying, analyzing, and so on. [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)

> 🔍 **Deep Dive (Optional)**
>
> The fact that a Jenkinsfile can live in your source code repository is architecturally significant. It means your pipeline definition is versioned alongside your application code. If you roll back your application to a previous commit, you also roll back the pipeline to whatever it looked like at that point. This is the essence of "infrastructure as code" applied to CI/CD — the pipeline is not a separate, fragile entity managed through a web UI; it is a first-class citizen of your codebase.

***

## 2. Jenkinsfile — Language, Syntax, and the Two Approaches

A Jenkinsfile is a **plain text file**. It uses its own **domain-specific language (DSL)** that is very close to **Groovy**, but — and this is an important point the instructor emphasizes — **you do not need to know Groovy to write a Jenkinsfile**. The DSL is purpose-built and approachable. [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)

There are **two syntax styles**: [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)

1.  **Scripted Pipeline** — the older approach, more flexible but more complex, uses raw Groovy constructs.
2.  **Declarative Pipeline** — the modern, recommended approach. It is more structured, easier to read, and is described as **"the way forward."** The instructor explicitly states: *"Declarative is the way forward now and we are going to use declarative in this project."* [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)

The entire video and all practical work use **Declarative Pipeline** syntax exclusively.

> ⚠️ **Expert Note (Optional)**
>
> In real-world projects, you will almost always encounter Declarative syntax in new pipelines. Scripted syntax still exists in legacy projects. The key difference: Declarative enforces a rigid structure (`pipeline { agent { } stages { } }`), which makes it easier to read and validate. Scripted gives you full Groovy power but at the cost of readability and standardization. If you encounter a Jenkinsfile that starts with `node { }` instead of `pipeline { }`, that's scripted syntax.

***

## 3. The Anatomy of a Declarative Pipeline — Block by Block

The instructor walks through the **entire structure** of a Declarative Pipeline, block by block. Understanding this hierarchy is essential before writing any code. [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)

### 3.1 `pipeline { }` — The Outermost Block

Everything lives inside the `pipeline` block. It is the **main container**. You write `pipeline` followed by opening and closing curly braces, and every other directive, setting, and stage goes inside it. Nothing meaningful exists outside this block. [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)

### 3.2 `agent` — Where the Pipeline Runs

The `agent` directive tells Jenkins **which machine (node) should execute this pipeline**. Jenkins has a concept of a master server and slave agents (covered in detail later in the course). You can specify a particular agent by its label, or you can say `agent any`, which means: "run this pipeline on any available node, including the master itself." [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)

In the video, since no external agents are set up yet, the instructor uses `agent any`. [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)

> 🔍 **Deep Dive (Optional)**
>
> The `agent` block is more powerful than just `any` or a label. In production pipelines, you can specify `agent { docker { image 'maven:3.9' } }` to run the pipeline inside a Docker container, or `agent { label 'linux && java17' }` to target nodes with specific capabilities. The `agent` can also be set at the stage level, meaning different stages can run on different machines — useful when, for example, your build runs on Linux but your deployment targets a Windows server.

### 3.3 `tools { }` — Declaring Build Tools

The `tools` block is where you declare the tools your pipeline needs — such as **Maven** or **JDK**. These tools must already be configured in Jenkins' **Global Tool Configuration** (Manage Jenkins → Tools). The name you use in the `tools` block must **exactly match** the name you gave the tool in that configuration. [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)

For example, if you named your Maven installation `MAVEN3.9` in Global Tool Configuration, you must write exactly `maven "MAVEN3.9"` in your Jenkinsfile. Same for JDK — if it's named `JDK17`, you write `jdk "JDK17"`. [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt), [\[167. Pipel...neCodeDemo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.%20PipelineCodeDemo.txt)

> ⚠️ **Expert Note (Optional)**
>
> A common mistake is a mismatch between the tool name in `tools { }` and the name in Global Tool Configuration. Jenkins will fail the build with a confusing error if the name doesn't match exactly — including case sensitivity. Always copy-paste the tool name directly from Jenkins' configuration page.

### 3.4 `environment { }` — Setting Variables

The `environment` block lets you define **environment variables** that can be used throughout your pipeline stages. The instructor mentions this as a concept and gives the example of Nexus-related variables (used in later lectures). The pattern is simple: `VARIABLE_NAME = "value"`, and then you reference it in your steps using `${VARIABLE_NAME}`. [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)

This block is not used in the first demo pipeline but becomes critical in real-world pipelines where you need to pass credentials, URLs, version numbers, and other dynamic values.

### 3.5 `stages { }` → `stage('Name') { }` → `steps { }` — The Execution Hierarchy

This is the **core execution structure** of any pipeline, and the instructor explains it in a very deliberate, layered way: [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)

*   **`stages { }`** is the container that holds **all** your individual stages. There is exactly one `stages` block per pipeline.
*   Inside `stages`, you have **multiple `stage('Name') { }` blocks**. Each stage represents a logical phase of your CI/CD process — for example, one stage to clone code, one to build, one to test, one to deploy, one to run code analysis, one to publish artifacts.
*   Inside each `stage`, you have **`steps { }`**, which is where the **actual commands and plugin calls** go. This is where you write shell commands (`sh 'mvn install'`), call Git plugins (`git branch: 'main', url: '...'`), or invoke any other Jenkins plugin.

The hierarchy is strict and must be respected: `pipeline → stages → stage → steps`. [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)

### 3.6 `post { }` — Post-Build Actions Inside a Stage

After the `steps` block inside a stage, you can optionally add a **`post` block**. This is the Pipeline-as-Code equivalent of "Post-Build Actions" in freestyle jobs. Inside `post`, you can define conditional blocks like: [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)

*   **`success { }`** — executes only if the stage completed successfully.
*   (Other conditions exist like `failure`, `always`, `changed`, etc., though only `success` is demonstrated in this video.)

The instructor uses `post { success { } }` to archive the WAR artifact after a successful build. [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)

***

## 4. Pipeline Script vs. Pipeline Script from SCM

When you create a Pipeline job in Jenkins, you get two options for providing the pipeline code: [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)

1.  **Pipeline script** — You paste the Jenkinsfile content directly into a text area in the Jenkins job configuration. This is what the instructor uses for the first demo. It's quick for testing but doesn't give you version control.

2.  **Pipeline script from SCM** — Jenkins fetches the Jenkinsfile from your source code repository (e.g., Git). You provide the repository URL, branch, credentials, and the **script path** (the filename, typically `Jenkinsfile`). This is the production-grade approach because the pipeline definition lives with the code and is version-controlled. [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)

> 🔍 **Deep Dive (Optional)**
>
> "Pipeline script from SCM" is the true realization of Pipeline as a Code. When you configure it, Jenkins will: (1) clone your repository, (2) look for the file at the specified script path (default: `Jenkinsfile` at the repo root), (3) parse and execute it. This means any changes to the pipeline go through the same code review process as application changes — pull requests, approvals, history tracking.

***

## 5. Writing Pipeline Code — Documentation, AI, and the Right Mindset

The instructor makes several important points about **how to approach writing Jenkinsfiles** in practice: [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)

*   **Plugin documentation** is the primary reference. Every Jenkins plugin that supports Pipeline will have documentation showing the exact syntax for using it in a Jenkinsfile. For example, the Git plugin documentation shows how to write `git branch: '...', url: '...'`.
*   **The Jenkins official documentation** has a "Getting Started with Pipeline" guide that walks through the syntax step by step — agent, stages, steps, everything.
*   **Google and ChatGPT** are legitimate tools for generating Jenkinsfile code. The instructor demonstrates asking ChatGPT: *"Write me a Jenkinsfile that will fetch the code from GitHub, build it with Maven, and upload the artifact to S3 bucket"* — and it produces a working pipeline.
*   **However** — and the instructor is emphatic about this — AI-generated pipeline code is only useful **if you already understand the basics**. You need to understand what agents, stages, steps, tools, and environment variables are. You need to know Maven, Git, AWS, etc. Otherwise you cannot make changes, debug failures, or adapt the code. The instructor's exact framing: *"Not like any Tom, Dick and Harry can come to ChatGPT and become a DevOps or write a Pipeline code from scratch without even understanding anything."* [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)
*   **Pipeline code is a one-time effort per project.** You write it once, and then you update it as needed. It's not something you rewrite from scratch daily.

> ⚠️ **Expert Note (Optional)**
>
> This is a genuinely important production insight. In real teams, the Jenkinsfile is typically written once by a senior engineer or DevOps lead, committed to the repo, and then maintained incrementally. New team members modify existing pipelines far more often than they write new ones. Understanding the structure and being able to read/debug a Jenkinsfile is more practically valuable than memorizing syntax.

***

## 6. Viewing Pipeline Execution in Jenkins

When a Pipeline job runs, Jenkins provides a **stage view** — a visual representation showing each stage as a column, with its status (success, failure, in progress). The instructor notes that stages appear in this view **only after they execute** — so you won't see the "Build" stage column until the pipeline actually reaches it. [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)

Each stage in the stage view is **clickable**. Clicking on a stage shows its specific console output — not the entire job's output, just that stage. There's also a dropdown to see the full console output for that stage. This is significantly better than scrolling through one massive console log trying to find where things went wrong. [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)

The instructor also makes a practical note about debugging: when something goes wrong, you should look at the **console output** — the actual logs — not just a screenshot of a failed stage view. [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)

***

## 7. Jenkinsfile in a Real Repository

The instructor navigates to the source code repository (the HKH Coder VProfile project on GitHub) and shows that it contains a **Jenkinsfile** in the repository root. This file contains a more complex pipeline with stages for code analysis (SonarQube), publishing artifacts, and more. The instructor acknowledges that it looks complex ("gibberish") at first glance but reassures that it's all built from the same basic syntax — and much of it is simply **copied from plugin documentation with modifications**. [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are building a **basic Jenkins Declarative Pipeline** that performs three stages: [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt), [\[167. Pipel...neCodeDemo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.%20PipelineCodeDemo.txt)

1.  **Fetch Code** — Clone a Java project from a GitHub repository.
2.  **Unit Test** — Run Maven unit tests on the code.
3.  **Build** — Compile and package the code into a WAR artifact, skipping tests (since they already ran), and archive the artifact on success.

This is a foundational CI pipeline. In real-world systems, this is the starting point for every Java-based CI/CD workflow. Once this works, you extend it with code analysis (SonarQube), quality gates, artifact versioning, artifact storage (Nexus), and deployment — all of which the instructor says will come in later lectures. [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)

The final outcome: a working Pipeline job in Jenkins that you can trigger with "Build Now," and it will automatically clone, test, build, and archive your Java application. [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)

***

## Step 1: Prepare Your Editor — VSCode with Jenkinsfile Extensions

Before writing any pipeline code, the instructor sets up **Visual Studio Code (VSCode)** as the editor. You can use any text editor, but if you use VSCode, the instructor recommends installing extensions for proper syntax highlighting. [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)

Go to the **Extensions** panel in VSCode (the square icon on the left sidebar, or `Ctrl+Shift+X`), search for **"Jenkinsfile"**, and install either the **Jenkinsfile** extension or **Jenkinsfile Support**. You can also install the **Groovy** extension for additional highlighting support. [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)

These extensions give you color-coded syntax highlighting for the Jenkinsfile DSL — making it much easier to see the structure of curly braces, keywords, and strings.

Once installed, create a new file: **File → New Text File**, then **Save** it with the name **`Jenkinsfile`** (capital **J**, no file extension). [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)

**Why this matters**: Proper highlighting prevents one of the most common mistakes in Jenkinsfile writing — mismatched curly braces. With dozens of nested blocks, a single misplaced `}` can break the entire pipeline, and without highlighting, it's very difficult to spot.

***

## Step 2: Write the `pipeline { }` Block

The very first thing you write is the outermost container: [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)

```groovy
pipeline {

}
```

Type `pipeline`, then open curly brace `{`, press Enter, then close curly brace `}`. Position your cursor between the braces — **everything else you write goes inside here**. [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)

*   **`pipeline`** — This keyword tells Jenkins: "Everything inside these braces is my pipeline definition." It is mandatory and there is exactly one per Jenkinsfile.
*   **`{` and `}`** — These define the scope. Every directive (agent, tools, stages) must be inside this scope.

***

## Step 3: Define the Agent

Inside the `pipeline` block, write: [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)

```groovy
agent any
```

*   **`agent`** — Declares where this pipeline should execute.
*   **`any`** — Tells Jenkins: "Run this on any available node — master or slave, I don't care." Since we don't have any external agents set up yet, this effectively means it runs on the Jenkins server itself. [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)

**How this connects**: In later stages of the course, when Jenkins agents (slave nodes) are configured, you'll replace `any` with specific labels to target particular machines. For now, `any` is the simplest and correct choice.

***

## Step 4: Declare the Tools

Immediately after `agent any`, write the `tools` block: [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt), [\[167. Pipel...neCodeDemo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.%20PipelineCodeDemo.txt)

```groovy
tools {
    maven "MAVEN3.9"
    jdk "JDK17"
}
```

*   **`tools { }`** — Opens the tools declaration block.
*   **`maven "MAVEN3.9"`** — Tells Jenkins: "This pipeline needs Maven, and the specific installation to use is the one named `MAVEN3.9`."
*   **`jdk "JDK17"`** — Tells Jenkins: "This pipeline needs JDK, and the specific installation to use is the one named `JDK17`."

**Critical detail**: The strings `"MAVEN3.9"` and `"JDK17"` are **not arbitrary names**. They must exactly match the names configured in **Jenkins → Manage Jenkins → Tools → Maven Installations / JDK Installations**. The instructor explicitly navigates to Jenkins to verify: *"Maven installations. We have given this Maven 3.9 all in caps. Let me copy that."* and *"JDK all in caps and 17."* [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)

**How to verify**: Go to Jenkins dashboard → Manage Jenkins → Tools. Scroll to Maven installations and JDK installations. Copy the exact name string and paste it into your Jenkinsfile. Do not type it from memory.

**What happens internally**: When Jenkins encounters the `tools` block, it ensures those tools are available on the agent before any stage runs. If the tool is configured for automatic installation, Jenkins will download and install it. If it's a local installation, Jenkins sets the appropriate `PATH` and environment variables so that commands like `mvn` and `java` resolve correctly.

***

## Step 5: Create the `stages { }` Container and First Stage — Fetch Code

After the `tools` block, write: [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt), [\[167. Pipel...neCodeDemo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.%20PipelineCodeDemo.txt)

```groovy
stages {
    stage('Fetch code') {
        steps {
            git branch: 'atom', url: 'https://github.com/hkhcoder/vprofile-project.git'
        }
    }
}
```

Let's break this down completely:

*   **`stages { }`** — The container for all stages. Exactly one per pipeline.
*   **`stage('Fetch code') { }`** — Defines one stage. The string `'Fetch code'` in single quotes is the **display name** that appears in Jenkins' stage view. You can name it anything meaningful.
*   **`steps { }`** — Inside the stage, this is where actual commands go.
*   **`git branch: 'atom', url: 'https://github.com/hkhcoder/vprofile-project.git'`** — This is a call to the **Git plugin**. The syntax follows a specific pattern used by Jenkins plugins in Pipeline code:

    *   **`git`** — The plugin name (lowercase).
    *   **`branch: 'atom'`** — A named parameter. `branch` is the parameter name, `'atom'` is the value. This tells the Git plugin which branch to check out.
    *   **`,`** — Parameters are comma-separated.
    *   **`url: 'https://github.com/hkhcoder/vprofile-project.git'`** — Another named parameter specifying the repository URL. [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)

**How this maps to freestyle jobs**: In a freestyle job, you would click "Source Code Management → Git," then fill in the repository URL field and the branch field. In Pipeline code, you're doing the exact same thing — just with `parameter: 'value'` syntax instead of form fields. The instructor explicitly draws this parallel. [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)

**Where to find plugin syntax**: The documentation for each Jenkins plugin provides the Pipeline syntax. For the Git plugin, you'd look at its official documentation page, which shows all available parameters (`branch`, `url`, `credentialsId`, `changelog`, etc.) and their usage.

**What happens internally**: Jenkins clones the specified Git repository, checks out the `atom` branch, and places the source code in the workspace directory on the agent. All subsequent stages operate on this workspace.

***

## Step 6: Second Stage — Unit Test

After the closing `}` of the first stage (but still inside `stages { }`), add: [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt), [\[167. Pipel...neCodeDemo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.%20PipelineCodeDemo.txt)

```groovy
stage('UNIT TEST') {
    steps {
        sh 'mvn test'
    }
}
```

*   **`stage('UNIT TEST') { }`** — A new stage named "UNIT TEST."
*   **`steps { }`** — The command container.
*   **`sh 'mvn test'`** — This is the **shell step**:
    *   **`sh`** — A built-in Pipeline step that executes a shell command on the agent. It runs whatever string you pass to it as a Bash command (on Linux agents).
    *   **`'mvn test'`** — The actual shell command. `mvn test` tells Maven to execute the **test phase** of the Maven lifecycle, which compiles the code and runs all unit tests. [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)

**Practical tip from the instructor**: He creates this stage by **copying the previous stage block and modifying it** — changing the stage name and replacing the Git plugin call with `sh 'mvn test'`. This is a practical workflow when writing Jenkinsfiles: copy an existing stage, paste, modify. The instructor explicitly says: *"How easy was that to create the next stage? Just need to know what you're doing and be careful on opening and closing."* [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)

**What happens internally**: Maven reads the `pom.xml` in the workspace (cloned in the previous stage), compiles the source code, compiles the test code, and runs all tests. If any test fails, the step fails, the stage fails, and the pipeline stops (by default).

***

## Step 7: Third Stage — Build with Post Action

This is the most complex stage in the demo. Add after the Unit Test stage: [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt), [\[167. Pipel...neCodeDemo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.%20PipelineCodeDemo.txt)

```groovy
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
```

### The `steps` block:

*   **`sh 'mvn install -DskipTests'`** — Runs a shell command:
    *   **`mvn install`** — Executes the Maven **install** phase. In Maven's lifecycle, `install` executes **all preceding phases**: `validate`, `compile`, `test`, `package`, `verify`, and then `install`. This means it would normally run tests again.
    *   **`-DskipTests`** — This is a **Maven option** (the `-D` flag sets a Java system property). `skipTests` tells Maven to skip the test execution phase. The instructor's reasoning: *"We already executed mvn test before this, right? So I want to skip the test, because if I run mvn install, install phase is going to execute all the previous phases including test."* [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)
    *   **`-D` syntax**: Any Maven option you want to pass uses the `-D` prefix, immediately followed (no space) by the property name. So `-DskipTests`, not `-D skipTests`.

> 🔍 **Deep Dive (Optional)**
>
> There's a subtle but important distinction: `-DskipTests` skips test *execution* but still *compiles* the test classes. If you wanted to skip even compilation of tests, you'd use `-Dmaven.test.skip=true`. In most CI pipelines, `-DskipTests` is the correct choice because you want the test code to compile (catching compilation errors) but not re-run tests that already passed in a previous stage.

### The `post` block:

*   **`post { }`** — Placed inside the stage, **after** the `steps` block closes. This defines actions that run after the stage's steps complete.
*   **`success { }`** — A conditional block inside `post`. The actions inside `success` only execute if the stage's steps completed successfully (exit code 0, no exceptions). [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)
*   **`echo 'Now Archiving it...'`** — Prints a message to the console output. `echo` is a built-in Pipeline step for logging/messaging.
*   **`archiveArtifacts artifacts: '**/target/*.war'`** — This calls the **Archive Artifacts** plugin:
    *   **`archiveArtifacts`** — The plugin step name.
    *   **`artifacts: '**/target/*.war'`** — A named parameter. The value `**/target/*.war` is a file pattern (Ant-style glob):
        *   **`**`** — Match any directory at any depth.
        *   **`/target/`** — Look inside `target` directories (Maven's default output directory).
        *   **`*.war`** — Match any file with a `.war` extension. [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt), [\[167. Pipel...neCodeDemo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.%20PipelineCodeDemo.txt)

**What happens internally**: After `mvn install` succeeds, Maven produces a `.war` file in the `target/` directory. The `archiveArtifacts` step finds this file and stores it in Jenkins' artifact storage, making it downloadable from the Jenkins job page. This is the Pipeline equivalent of the "Archive the artifacts" post-build action in freestyle jobs. [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)

***

## Step 8: The Complete Pipeline Code

Here is the full Jenkinsfile as written in the video: [\[167. Pipel...neCodeDemo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.%20PipelineCodeDemo.txt)

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
        stage('UNIT TEST') {
            steps {
                sh 'mvn test'
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
    }
}
```

**Verify the structure**: `pipeline` → contains `agent`, `tools`, `stages`. `stages` → contains three `stage` blocks. Each `stage` → contains `steps`. The third stage also has `post { success { } }`. [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt), [\[167. Pipel...neCodeDemo \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.%20PipelineCodeDemo.txt)

***

## Step 9: Create and Run the Pipeline Job in Jenkins

1.  Go to the **Jenkins dashboard**.
2.  Click **"New Item"**.
3.  Enter the name: **`VProfile Pipeline`** (or any meaningful name).
4.  Select the item type: **Pipeline** (not Freestyle, not Multibranch — just "Pipeline").
5.  Click **OK**. [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)
6.  Scroll down to the **Pipeline** section in the job configuration.
7.  In the **Definition** dropdown, keep it as **"Pipeline script"** (not "Pipeline script from SCM" — we'll use that approach later).
8.  Paste your entire Jenkinsfile content into the **Script** text area.
9.  Click **Save**.
10. Click **"Build Now"** on the left sidebar. [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)

**What happens internally**: Jenkins parses the Declarative Pipeline, validates the structure, resolves the tools (sets up Maven and JDK paths), selects an agent, and then executes stages sequentially: Fetch code → Unit Test → Build. [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)

***

## Step 10: Viewing the Results

After triggering the build: [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)

*   The **Stage View** appears on the job page, showing columns for each stage. Stages appear **only after they start executing** — so initially you'll see "Fetch code," then "UNIT TEST" appears when it begins, then "Build."
*   **Clicking on a stage** in the stage view shows that stage's specific output — not the full job log, just the logs for that stage. There is also a **dropdown** to see the complete console output for that individual stage.
*   The **full Console Output** (accessible from the build's page → Console Output) shows everything sequentially. The instructor emphasizes: when something goes wrong, **read the console output** — not just the stage view screenshot. [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)

**How to verify success**: All three stages should show green (success). The archived WAR artifact should be available on the build page as a downloadable link. The console output should end with "Finished: SUCCESS."

***

## Step 11: Understanding "Pipeline Script from SCM" (For Future Use)

The instructor briefly shows the alternative: instead of pasting code directly, you select **"Pipeline script from SCM"** in the job configuration. This reveals fields for: [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)

*   **SCM type**: Git (or others)
*   **Repository URL**: Your Git repository
*   **Branch**: Which branch to check out
*   **Credentials**: If the repo is private
*   **Script Path**: The filename Jenkins should look for — default is `Jenkinsfile`, but it's configurable. [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)

This is the production-grade approach and will be used in later lectures. For this introductory demo, the direct "Pipeline script" approach is used for simplicity.

***

## What Comes Next (As Stated by the Instructor)

The instructor explicitly outlines the roadmap for upcoming lectures: [\[167.-Pipel...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/167.-Pipeline-As-A-Code-Introduction.txt)

*   **Code analysis** (SonarQube integration)
*   **Quality gates** (automated pass/fail based on code quality thresholds)
*   **Artifact versioning** (semantic versioning of build outputs)
*   **Artifact storage in Nexus** (enterprise artifact repository)
*   All described as **"real-time stuff"** — production-grade pipeline stages.

***

This completes the full reconstruction of the video content. The material covers every concept explained, every command demonstrated, every decision justified, and every practical step executed — structured for deep learning with skippable optional depth where appropriate.
