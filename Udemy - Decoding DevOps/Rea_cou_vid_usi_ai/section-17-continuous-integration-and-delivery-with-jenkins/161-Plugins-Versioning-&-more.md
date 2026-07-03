# Jenkins Plugins, Versioning & Variables — Deep Learning Material

**Source:** [161.-Plugins,-Versioning-&-more.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt?EntityRepresentationId=09cd39ac-910f-46c5-965a-8c06a24ba819) [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1. Jenkins Plugins — Extending Jenkins' Capabilities

Jenkins, by itself, is a core automation engine. It can build, it can run shell commands, it can schedule jobs — but it cannot do everything out of the box. It doesn't natively know how to upload artifacts to AWS S3, generate timestamps in custom formats, integrate with Nexus, or connect with hundreds of other tools in the DevOps ecosystem. This is where **plugins** come in. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

A plugin is a self-contained piece of software that you install into Jenkins to add new functionality. Think of Jenkins as a smartphone — the core OS handles the basics, but you install apps (plugins) to do specific things. Need to push artifacts to S3? Install the S3 publisher plugin. Need a timestamp variable? Install the Build Timestamp plugin. Jenkins' entire power in real-world DevOps comes from its plugin ecosystem — there are thousands of plugins covering nearly every integration and workflow you can think of. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

The plugin system exists because no single tool can anticipate every team's toolchain. Instead of bloating Jenkins with every possible feature, the architecture delegates specialized functionality to plugins. This keeps the core lightweight and lets teams install only what they need. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

**How plugins work at a high level:** When you install a plugin, Jenkins loads it into its runtime. The plugin registers itself — it might add new build steps, new post-build actions, new configuration options, or new environment variables. Once installed, the plugin's features appear in the Jenkins UI wherever they're relevant. For example, after installing the S3 publisher plugin, a new option called "Publish artifact to S3 bucket" appears in the Post-build Actions dropdown of your job configuration. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

> 🔍 **Deep Dive (Optional)**
>
> Plugins in Jenkins are packaged as `.hpi` or `.jpi` files. When you install a plugin through the UI, Jenkins downloads it from the official Jenkins Update Center (a curated repository of verified plugins). The plugin is placed in the `$JENKINS_HOME/plugins/` directory. Jenkins may or may not require a restart depending on the plugin. Some plugins are "hot-loadable" and take effect immediately; others require a Jenkins restart. The Jenkins UI will tell you if a restart is needed after installation.

***

## 2. Plugin Management — Installing, Listing, Disabling, and Updating

Jenkins provides a dedicated management interface for plugins, accessible via **Manage Jenkins → Plugins**. This interface has four sections: [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

**Updates** — Shows plugins that are already installed but have newer versions available. Keeping plugins updated is important because updates often fix bugs, patch security vulnerabilities, and add compatibility with newer Jenkins versions. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

**Available Plugins** — This is where you search for and install new plugins. You type a plugin name (or a keyword related to what you need), browse the results, check the box next to the desired plugin, and click Install. For example, searching "S3" returns the S3 publisher plugin and potentially other S3-related plugins. You pick the one that matches your use case. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

**Installed Plugins** — Lists every plugin currently installed in your Jenkins instance. From here, you can **disable** plugins you no longer need. Disabling a plugin deactivates its functionality without removing it entirely, so you can re-enable it later if needed. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

**Advanced Settings** — This section allows you to upload a plugin manually. If a plugin was developed in-house, obtained from a third party, or isn't available in the public Jenkins Update Center, you can upload its `.hpi` file directly using the "Choose file" option. This is how organizations deploy custom-built plugins. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

> ⚠️ **Expert Note (Optional)**
>
> The search functionality in the Available Plugins section is not always robust. The video explicitly calls this out — "the search is not so good, so you need to give proper names." If you can't find a plugin by keyword, a practical approach is to Google the plugin name (e.g., "timestamp plugin in Jenkins") to find the exact plugin name, then search for that exact name in Jenkins. This is a common real-world workflow. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

***

## 3. Plugin Dependencies — Why You Can't Always Disable Freely

Plugins do not always exist in isolation. Some plugins depend on other plugins to function. When you install a plugin, Jenkins automatically installs its dependencies — plugins that the primary plugin requires. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

The video gives a concrete example: when you install the S3 publisher plugin, Jenkins also installs the **Amazon Web Services SDK :: Minimal** plugin automatically. You didn't ask for it — Jenkins pulled it in because S3 publisher needs the AWS SDK to communicate with AWS services. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

This dependency chain has a direct consequence for disabling plugins: **you cannot disable a dependency plugin while the plugin that depends on it is still enabled.** In the example, you cannot disable "Amazon Web Services SDK :: Minimal" until you first disable the S3 publisher plugin. Jenkins enforces this to prevent broken states where a plugin tries to call functionality from a disabled dependency. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

> 🔍 **Deep Dive (Optional)**
>
> This is a tree-like dependency structure. Plugin A depends on Plugin B, which may depend on Plugin C. To disable C, you must first disable B, and to disable B, you must first disable A. When disabling plugins, always work from the top of the dependency tree downward. The Jenkins UI helps here — if you try to disable a plugin that others depend on, it won't let you and will indicate which plugins are blocking the action.

***

## 4. Jenkins Built-in Variables

Jenkins provides a set of **built-in environment variables** that are automatically available in every job run. These variables are populated by Jenkins itself at runtime and carry metadata about the current build. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

Key built-in variables mentioned in the video: [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

| Variable      | What It Contains                                                         |
| ------------- | ------------------------------------------------------------------------ |
| `BUILD_ID`    | The numeric ID of the current build (increments with each run: 1, 2, 3…) |
| `BUILD_URL`   | The full URL to the current build's page in Jenkins                      |
| `JAVA_HOME`   | The path to the Java installation Jenkins is using                       |
| `JENKINS_URL` | The base URL of the Jenkins instance                                     |
| `JOB_NAME`    | The name of the job being executed                                       |

These variables exist so that your build steps can dynamically reference build-specific information without hardcoding. For example, instead of manually numbering your artifacts, you can use `$BUILD_ID` to automatically assign a unique, incrementing number to each build output. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

You reference these variables in shell commands using the `$VARIABLE_NAME` syntax (e.g., `$BUILD_ID`). Jenkins substitutes the actual value at runtime. The full list of built-in variables is documented on `jenkins.io` under "Using Environment Variables." [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

***

## 5. Variable Injection via Plugins

Beyond the built-in variables, Jenkins allows you to **inject additional variables** through plugins. This is a powerful extensibility mechanism — if Jenkins doesn't natively provide a variable you need, there's likely a plugin that adds it. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

The video demonstrates this with the **Build Timestamp plugin**. Once installed, this plugin adds a new variable called `BUILD_TIMESTAMP` to every job run. This variable contains the date and time when the build was triggered, formatted according to a pattern you configure globally. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

The concept here is important: **plugins don't just add UI features or build steps — they can also enrich the variable environment.** This means your shell commands, pipeline scripts, and other build steps gain access to new dynamic data simply by installing a plugin. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

***

## 6. Parameterized Builds — User-Supplied Variables

Built-in variables and plugin-injected variables are automatic — Jenkins generates their values. But sometimes you need a variable whose value is **decided by the person triggering the build**. This is the concept of a **parameterized build**. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

When you check "This project is parameterized" in a job's configuration, Jenkins changes the build trigger from "Build Now" to **"Build with Parameters."** Instead of immediately starting, Jenkins presents a form where the user must enter values for the defined parameters before the build begins. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

The video demonstrates a **String Parameter** — the simplest type. You define a parameter name (e.g., `VERSION`), an optional default value (used if the user doesn't provide input), and an optional description. Once defined, this parameter becomes available as `$VERSION` in your build steps. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

This is how teams implement controlled versioning — instead of relying on auto-incrementing build IDs, a release engineer can explicitly specify "2.3.6" as the version when triggering the build. The video specifically uses **semantic versioning** (major.minor.patch format like `2.3.6`) as an example of user-supplied version input. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

> 🔍 **Deep Dive (Optional)**
>
> If you enable parameterized builds but want the job to also be runnable without manual input (e.g., via automated triggers), you should set a sensible **default value**. If no default is set and the job is triggered automatically, the parameter will be empty, which could break your build steps. Alternatively, you can uncheck "This project is parameterized" to revert back to the standard "Build Now" behavior — the video demonstrates this when switching from parameterized builds to timestamp-based versioning. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

***

## 7. Artifact Versioning — The Problem and the Approach

Every time a Jenkins build job runs, it produces an artifact (e.g., `vprofile-v2.war`). If the job runs multiple times, the new artifact **overwrites** the previous one in the workspace. You lose the old version. In real-world systems, this is unacceptable — you need to maintain multiple versions of artifacts for rollbacks, auditing, debugging, and release management. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

The solution is **versioning** — giving each artifact a unique name that includes a version identifier. The video explores three approaches to this, each progressively more sophisticated: [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

1.  **`BUILD_ID`-based versioning** — Automatic, uses Jenkins' incrementing build number. Simple but not semantically meaningful (version "3" tells you nothing about what changed). [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)
2.  **Parameterized versioning** — User-supplied, allows semantic version numbers like `2.3.6`. Meaningful but requires manual input. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)
3.  **Timestamp-based versioning** — Automatic, uses the build's date/time. Useful when you need chronological ordering of artifacts. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

The video explicitly notes that **Jenkins itself is not the right place to store versioned artifacts long-term.** Jenkins' workspace is a temporary build area. The proper next step is to move artifacts to a dedicated artifact repository like **Nexus** or a cloud storage service like **AWS S3**. This is covered later in the course. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

> ⚠️ **Expert Note (Optional)**
>
> In production environments, versioning is rarely done with just `BUILD_ID` or timestamps. Teams typically use a combination: semantic version from the code repository (often derived from Git tags), plus a build number or commit hash for traceability. The approaches shown in this video are foundational exercises to build familiarity with Jenkins variables and dynamic naming — the real-world versioning mechanisms (with Nexus, Maven versioning, Git tags) come later. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

***

## 8. Build Timestamp Plugin — Configuration and Format Patterns

The Build Timestamp plugin, once installed, requires global configuration before use. You configure it via **Manage Jenkins → System (Configure Global Settings)**. After installation, a new section appears: **Enable BUILD\_TIMESTAMP**, with fields for Timezone and Pattern. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

The **pattern** defines how the timestamp is formatted. The default pattern uses `yyyy-MM-dd_HH-mm-ss` (year-month-date\_hour-minute-seconds). The video changes this to a custom format: `dd-MM-yy_HH-mm` (date-month-last two digits of year\_hour-minute). [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

There is no enforced standard for the format — the video explicitly says "there is no hard and fast rule in this. Use your own format if you wish." The format you choose should match your team's conventions and what makes the artifact names readable and sortable for your use case. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

> 🔍 **Deep Dive (Optional)**
>
> When using timestamp-based versioning, make sure there is a **minimum interval of one minute** between job runs if your format only goes down to the minute level (like `HH-mm`). If two builds run within the same minute, they'll get the same timestamp, defeating the purpose of unique versioning. If you need finer granularity, include seconds (`ss`) in your pattern. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

***

## 9. Artifact Publishing to S3 — A Preview

The video briefly previews how versioned artifacts can be pushed to AWS S3 using the S3 publisher plugin that was installed earlier. After installing the plugin, a new Post-build Action appears: **"Publish artifact to S3 bucket."** This action requires you to specify the source files, the destination S3 bucket, and authentication credentials. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

For authentication, you have two options: provide AWS credentials directly in Jenkins, or **attach an IAM role with S3 full access to the Jenkins EC2 instance** (the more secure, recommended approach in AWS environments). [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

The video explicitly states this is just a preview — "you don't need to do this, I mean if you want as an exercise, do it. We'll be doing this later." The full S3 and Nexus integration is covered in later lectures. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

In this practical session, we are building a **versioned artifact pipeline in Jenkins**. We start with a basic build job that produces a `.war` file, then progressively add versioning mechanisms — first automatic (using build IDs and timestamps), then manual (using parameterized inputs). Along the way, we install and configure plugins, work with Jenkins variables, and set up the groundwork for artifact storage. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

**Why this matters:** In real-world CI/CD, every build must produce a uniquely identifiable artifact. Without versioning, you can't track which code is deployed where, can't roll back safely, and can't audit your release history. This exercise builds the foundational skills for managing build outputs professionally.

**Final outcome:** A Jenkins job that creates uniquely versioned `.war` files in a `versions/` directory, using dynamic variables (build ID, user-supplied version, or timestamp). [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

***

## Step 1: Navigate to the Plugins Section

Go to the Jenkins Dashboard. Click on **Manage Jenkins** in the left sidebar. On the management page, locate and click **Plugins**. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

This opens the plugin management interface with four tabs: Updates, Available Plugins, Installed Plugins, and Advanced Settings. This is your central hub for all plugin operations in Jenkins. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

***

## Step 2: Search and Install the S3 Publisher Plugin

Click on the **Available Plugins** tab. In the search bar, type `S3`. You will see results including **S3 publisher** and potentially other S3-related plugins. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

Select the plugin that matches your use case — in this case, the S3 publisher plugin (for uploading build artifacts to AWS S3 buckets). Check the box next to it and click **Install**. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

**What happens internally:** Jenkins downloads the plugin `.hpi` file from the Jenkins Update Center, along with any dependency plugins it requires (e.g., Amazon Web Services SDK :: Minimal). All downloaded plugins are placed in `$JENKINS_HOME/plugins/` and loaded into Jenkins' runtime. After installation, new S3-related options become available in job configurations. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

**How to verify:** After installation, go to any job's configuration → Post-build Actions. You should now see **"Publish artifact to S3 bucket"** as an available option. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

***

## Step 3: Explore Installed Plugins and Understand Dependencies

Click on the **Installed Plugins** tab. This shows all currently installed plugins. Try to disable the **Ant Plugin** — you'll notice you can, because no other plugin depends on it. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

Now try to disable **Amazon Web Services SDK :: Minimal**. You cannot, because the S3 publisher plugin depends on it. To disable it, you would first need to disable the S3 publisher plugin. This demonstrates the plugin dependency chain in action. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

***

## Step 4: Explore Advanced Settings (Custom Plugin Upload)

Click on the **Advanced Settings** tab. Here you see the option to **Choose file** and upload a plugin manually. This is used when: [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

*   Your organization developed a custom plugin internally
*   You obtained a plugin from a third-party developer
*   The plugin isn't available in the public Jenkins Update Center

You upload the `.hpi` file, and Jenkins installs it just like any other plugin.

***

## Step 5: Create a New Job for Versioned Artifacts

Go back to the Dashboard. Click **New Item**. Enter the name: `buildartifact`. Select **Freestyle project**. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

In the **"Copy from"** field at the bottom, type `Vprofile Build` (the name of your existing build job). This copies all configuration from the existing job, saving you from reconfiguring source code, Maven goals, etc. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

**What to modify:** Scroll to the end of the configuration. **Remove** the "Archive the Artifact" post-build action. The existing build step (Maven) will still build the artifact. We are going to add our own versioning step after the build. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

***

## Step 6: Add a Shell Step for BUILD\_ID-Based Versioning

In the Build section, click **Add build step → Execute shell**. Enter the following commands: [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

```bash
mkdir -p versions
cp target/vprofile-v2.war versions/vpro$BUILD_ID.war
```

**Line-by-line breakdown:**

**`mkdir -p versions`** [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

*   `mkdir` — Creates a directory.
*   `-p` — The "parents" flag. If the `versions` directory already exists, this flag prevents an error. Without `-p`, running `mkdir versions` a second time would throw "folder already exists" and fail the build. Always use `-p` when creating directories in automated scripts.
*   `versions` — The directory name where versioned artifacts will be stored.

**`cp target/vprofile-v2.war versions/vpro$BUILD_ID.war`** [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

*   `cp` — Copy command.
*   `target/vprofile-v2.war` — The source file. This is the artifact produced by Maven in the `target/` directory.
*   `versions/vpro$BUILD_ID.war` — The destination. `$BUILD_ID` is a Jenkins built-in variable that resolves to the current build number (1, 2, 3, etc.) at runtime. So the first run produces `vpro1.war`, the second `vpro2.war`, and so on.

**Save** the job and **run it three times.** [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

**How to verify:** Go to the job → **Workspace → versions/**. You should see three files: `vpro1.war`, `vpro2.war`, `vpro3.war`. You can also check the **Console Output** of any build — it will show the `cp` command with the resolved filename (e.g., `vpro3.war`). [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

**Connection to the overall system:** This demonstrates that `$BUILD_ID` provides automatic, unique versioning with zero manual input. But the version numbers are just incrementing integers — they carry no semantic meaning.

***

## Step 7: Configure Parameterized Build for User-Supplied Versioning

Go to the job configuration. Check the box **"This project is parameterized."** Click **Add Parameter → String Parameter.** [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

Configure the parameter:

*   **Name:** `VERSION` (this becomes the variable name, referenced as `$VERSION`)
*   **Default Value:** (optional — the value used if the user doesn't provide input)
*   **Description:** (optional — explains what this parameter is for) [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

Now scroll down to the Execute Shell section. **Comment out** the `BUILD_ID` line by adding `#` at the beginning (so it becomes `#cp target/vprofile-v2.war versions/vpro$BUILD_ID.war`). Add a new line: [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

```bash
cp target/vprofile-v2.war versions/vpro$VERSION.war
```

**Save** the job. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

**What changes in the UI:** The "Build Now" button is replaced by **"Build with Parameters."** Clicking it presents a form where you enter the `VERSION` value. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

**Test it:** Click "Build with Parameters." Enter `2.3.6` as the version. Click **Build.** [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

**How to verify:** Go to Workspace → versions/. You should see `vpro2.3.6.war`. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

> ⚠️ **Expert Note (Optional)**
>
> The video notes that the resulting filename `vpro2.3.6.war` would look cleaner with a separator — like `vpro-2.3.6.war` — between the prefix and the version number. In production, always include a hyphen or underscore separator for readability and to avoid ambiguity in parsing. You would change the command to: `cp target/vprofile-v2.war versions/vpro-$VERSION.war`. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

***

## Step 8: Install the Build Timestamp Plugin

Go to **Dashboard → Manage Jenkins → Plugins → Available Plugins.** Search for `Build Timestamp`. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

If the search doesn't find it easily, remember that Jenkins' plugin search can be finicky — try the exact name with proper spacing (`Build Timestamp`). Alternatively, Google "timestamp plugin in Jenkins" to find the exact plugin name first. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

Select the **Build Timestamp** plugin. Its description states: "Adds BUILD\_TIMESTAMP to Jenkins variable and system properties." Check the box and click **Install.** Jenkins may also install additional dependencies (like SSH server components). [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

**What this plugin does:** It adds a new environment variable `BUILD_TIMESTAMP` to every build, containing the date/time of when the build was triggered. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

***

## Step 9: Configure the Build Timestamp Format

Go to **Dashboard → Manage Jenkins → System** (Configure global settings). [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

After installing the Build Timestamp plugin, a new section appears: **Enable BUILD\_TIMESTAMP.** It has two fields: [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

*   **Timezone** — Set to your desired timezone.
*   **Pattern** — The format pattern for the timestamp.

The default pattern is something like `yyyy-MM-dd_HH-mm-ss`. The video changes it to: [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

    dd-MM-yy_HH-mm

**Pattern breakdown:**

*   `dd` — Day of the month (two digits)
*   `MM` — Month (two digits)
*   `yy` — Year (last two digits)
*   `_` — Literal underscore separator
*   `HH` — Hour in 24-hour format
*   `mm` — Minutes

Click **Save.** [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

***

## Step 10: Use BUILD\_TIMESTAMP for Versioning

Go back to the `buildartifact` job configuration. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

First, **uncheck "This project is parameterized"** so the job goes back to "Build Now" mode (no parameter prompt). [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

In the Execute Shell section, comment out the previous `$VERSION` line and add: [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

```bash
cp target/vprofile-v2.war versions/vpro$BUILD_TIMESTAMP.war
```

`$BUILD_TIMESTAMP` will resolve to the formatted date/time string (e.g., `05-05-26_14-07`). **Save** the job. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

**Run the job two or three times**, with at least **one minute between each run** (since the format only includes hours and minutes, runs within the same minute would produce identical filenames). [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

**How to verify:** Go to Workspace → versions/. You should see files like `vpro05-05-26_14-07.war`, `vpro05-05-26_14-08.war`, etc. — each with a unique timestamp. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

***

## Step 11: Preview — Publishing Artifacts to S3

Go to the job configuration. Scroll to **Post-build Actions → Add post-build action.** You should see **"Publish artifact to S3 bucket"** (available because we installed the S3 plugin earlier). [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

This action requires: [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

*   **Source** — The file(s) to upload (e.g., `versions/*.war`)
*   **Destination S3 bucket** — The target bucket name
*   **Credentials** — Either AWS credentials configured in Jenkins, or an **IAM role with S3 full access attached to the Jenkins EC2 instance**

The video explicitly states: **do not configure this now** — it's shown as a preview. The full S3 and Nexus artifact management workflow is covered in later lectures. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

**Connection to the overall system:** The versioned artifacts we've been creating in the `versions/` directory are stored locally on the Jenkins server. In production, you would never leave artifacts there. The next step in a real CI/CD pipeline is to push them to a dedicated artifact repository (Nexus) or cloud storage (S3), which is what this post-build action enables. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

***

***

## 📌 Summary of Key Takeaways

The video covers three interconnected concepts that form the foundation for Jenkins pipeline work: [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)

1.  **Plugins** — Jenkins' extensibility mechanism. Install from Available Plugins, manage from Installed Plugins, upload custom ones from Advanced Settings. Always be aware of dependency chains when disabling.

2.  **Variables** — Jenkins has built-in variables (`BUILD_ID`, `BUILD_URL`, `JOB_NAME`, etc.), plugin-injected variables (`BUILD_TIMESTAMP`), and user-supplied parameters (`VERSION`). All are referenced with `$VARIABLE_NAME` syntax.

3.  **Versioning** — Use dynamic variables to give each artifact a unique name. `BUILD_ID` for simple auto-increment, parameterized `VERSION` for semantic control, `BUILD_TIMESTAMP` for chronological tracking. Always move versioned artifacts to proper storage (S3/Nexus) — Jenkins workspace is not a repository.

The video closes with an important note: **"Things will get very serious from coming lectures"** — these foundational concepts (plugins, variables, shell commands, job configuration) are prerequisites for Jenkins Pipeline code, which is the next topic in the course. [\[161.-Plugi...ing-&-more \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/161.-Plugins,-Versioning-%26-more.txt)
