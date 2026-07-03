# 🔧 Maven Build Tool — Hands-On Deep Learning Material

**Source:** *Maven Hands-on* (Video Lecture Caption File) [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

## 1.1 What Makes a Project a Maven Project — The pom.xml File

When you look at a source code repository and see a file called `pom.xml` at the root level, that immediately tells you: **this is a Maven project**. The `pom.xml` (Project Object Model) is Maven's single source of truth — it contains all the metadata Maven needs to build, test, and package the project. The actual Java source code lives inside the `src` folder, written by developers. The `pom.xml` is the bridge between the developer's code and the build system's execution. [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

When a developer first creates a Java project with Maven, they initialize the Maven project structure, which auto-generates the `pom.xml`. From that point on, developers keep modifying this file — adding dependencies, changing versions, configuring plugins — and push it to the repository along with the source code. As a DevOps engineer, you don't write this file, but you must be able to **read it, understand its structure, and make changes when required** (e.g., fixing a version incompatibility). [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

***

## 1.2 XML Syntax in pom.xml — The Minimum You Must Understand

The `pom.xml` is written in XML. The fundamental pattern is: an **opening tag** like `<version>`, a **value** like `v2`, and a **closing tag** like `</version>` (note the forward slash in the closing tag). Everything between the opening and closing tags is the data for that element. [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

XML elements can be **nested** (cascading). For example, `<properties>` opens a block, and inside it you have many individual elements like `<spring.version>6.0.1</spring.version>` and `<mysql.connector.version>8.0.33</mysql.connector.version>`. These nested elements inside `<properties>` act as **variables** — they define values that can be referenced elsewhere in the file.

Inside the `<dependencies>` block, each `<dependency>` entry specifies three key identifiers: `<groupId>`, `<artifactId>`, and `<version>`. The version field can reference a variable defined in properties using the syntax `${spring.version}`, which resolves to the value `6.0.1` defined earlier. This variable mechanism avoids hardcoding the same version number in dozens of places — change it once in properties, and every dependency referencing it updates automatically. [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

The instructor emphasizes: you don't need to fully understand every XML element, but you **must** be able to navigate the structure, find specific values (like version numbers), and modify them when needed for troubleshooting.

***

## 1.3 Dependencies — What They Are and How Maven Handles Them

A dependency is an external library or module that the project's source code needs in order to compile, test, or run. The developers declare every dependency in the `<dependencies>` section of `pom.xml`, specifying exactly which library (by group ID and artifact ID) and which version they need. [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

When you run a Maven command that needs these dependencies (like `mvn install`), Maven reads the dependency list from `pom.xml` and **downloads them automatically** from a remote repository. By default, this is the **Global Maven Repository** (Maven Central) — the public, internet-hosted repository from which Maven pulls libraries. [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

A critical concept the instructor highlights: **a dependency can itself have many dependencies** (called transitive dependencies). So when Maven downloads one library, that library's own `pom.xml` may list 10 more libraries it needs, and those may need even more. This is why you see a "huge list of files getting downloaded" — Maven resolves the entire dependency tree recursively. [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

Downloaded dependencies are stored locally in the `.m2/repository` folder inside your home directory (`~/.m2/repository`). This is Maven's **local cache**. Once downloaded, Maven doesn't re-download them unless you explicitly delete them or change versions. [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

🔍 **Deep Dive:**
The instructor mentions that in some projects, you can have your own **proxy repository** (like Nexus or Artifactory) instead of downloading directly from Maven Central. This is a common enterprise pattern: the proxy repository sits between your build server and the internet, caching dependencies locally and allowing you to host private/internal libraries that aren't on Maven Central. The instructor references showing this in a DevOps projects course.

⚠️ **Expert Note:**
Sometimes you **need** to delete the local `.m2/repository` cache — specifically when changing Maven versions, switching JDK versions, or fixing dependency corruption. The instructor demonstrates this: `rm -rf ~/.m2/repository/*`. After clearing, the next Maven command re-downloads everything fresh. This is a legitimate troubleshooting step, not a destructive action.

***

## 1.4 Maven Phases — The Build Lifecycle

Maven operates through a sequence of **phases** that form a build lifecycle. Each phase performs a specific task, and crucially, **running a later phase automatically executes all previous phases**. The phases demonstrated in this lecture: [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

**`validate`** — Checks that the project structure is correct and all necessary information is available. It does not compile or download anything — it just validates the directory structure and `pom.xml` integrity.

**`test`** — Compiles the source code and executes **unit test cases** written by the developers. For Java projects, these are typically JUnit tests. After running, it generates test reports in the `target` folder. The instructor notes that deeper analysis of these test reports will be covered in Jenkins lectures.

**`install`** — This is the phase that does the heavy lifting. Because it's a later phase, running `mvn install` automatically executes validate, compile, test, and package first, then installs the final artifact into the local `.m2` repository. During this process, Maven downloads all dependencies, compiles the code, runs tests, and creates the final packaged artifact (in this case, a `.war` file). [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

**`clean`** — This is not a lifecycle phase in the same chain — it's a separate lifecycle. `clean` **removes the `target` folder**, which contains all output from previous builds. Running `mvn clean install` first wipes the output, then runs the full install lifecycle from scratch. Important: `clean` only removes the `target` folder — it does **not** remove the `.m2/repository` dependencies. To clear dependencies, you must manually delete the `.m2/repository` contents. [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

***

## 1.5 The Target Folder — Maven's Output Directory

Every Maven command that produces output writes it to the `target` folder inside the project directory. After `mvn test`, the target folder contains test reports. After `mvn install`, it contains the compiled classes, test reports, and the **final artifact** — in this case, `vprofile-v2.war`. [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

The `.war` file (Web Application Archive) is the deployable artifact — an archive format (essentially a zip) of the compiled application ready to be deployed to a server like Tomcat. The **name and version** of this artifact (`vprofile-v2`) are **not hardcoded by Maven** — they come directly from the `pom.xml` file. Maven reads the `<name>`, `<version>`, and `<packaging>` elements to determine what to name the output file and what format to package it in. [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

***

## 1.6 JDK vs. JRE — Why the Distinction Matters

Two Java packages exist: **JRE** (Java Runtime Environment) and **JDK** (Java Development Kit). JRE is sufficient to **run** a Java application — it contains the Java Virtual Machine and standard libraries. JDK includes everything in JRE **plus** development tools like the compiler (`javac`), debugger, and other utilities needed to **build** Java code. [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

For build operations (what we're doing), **JDK is required**. If you install only JRE, Maven will fail because it needs the compiler that only JDK provides. The instructor searches the package manager and explicitly points out both packages (`openjdk-17-jdk` vs. `openjdk-17-jre`) to make this distinction visible.

***

## 1.7 Version Responsibility — The DevOps/Developer Contract

The instructor makes a clear operational principle: **it is the developer's responsibility to tell you what versions of tools are required**, and it is your responsibility as a DevOps engineer to install and configure those exact versions. You need to get this version list from the developers: Java version, Maven version, Node version (for Node.js projects), or whatever the build stack requires. The developers have this information because they already build on their local machines. [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

This is a communication contract, not a technical one. If you install the wrong version, the build may fail with errors that are difficult to diagnose. The correct versions are not something you guess — you ask.

***

## 1.8 Troubleshooting Build Failures — Two Categories

The instructor demonstrates two fundamentally different types of build failures: [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

**1. Resource errors (not build errors):** The `Java heap space` error occurs when the JVM running Maven doesn't have enough memory to complete the build. The EC2 instance only had \~579MB available. This is **not** a problem with the code or dependencies — it's an infrastructure limitation. The fix is the environment variable `export MAVEN_OPTS="-Xmx1024m"`, which tells Maven's JVM to allocate up to 1024MB (1GB) of heap memory. The instructor notes something important: the machine doesn't actually have 1GB free, but it works because the JVM doesn't necessarily use all allocated memory — it's a maximum limit, and with swap and virtual memory, the OS manages it. The instructor explicitly says: "Don't worry. It's not going to cause any other harm. We just focus on the build." [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

**2. Dependency/compatibility errors (actual build errors):** The instructor deliberately introduces a failure by downgrading the Jacoco plugin version to `8.8.8`. Jacoco is a code coverage tool that instruments Java bytecode. Version `8.8.8` doesn't support Java 21 — versions prior to `0.8.11` lack Java 21 compatibility. The build produces errors like "error while instrumenting" with Jacoco references. The fix is upgrading the Jacoco version in `pom.xml` to a version that supports the JDK being used. [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

🔍 **Deep Dive:**
The instructor's approach to diagnosing the Jacoco error is operationally significant: he copies the error message, the output of `mvn -version` (showing Maven and Java versions), and the entire `pom.xml` content, then pastes all of it into ChatGPT. The key principle: **give the AI tool as much context as possible** — the error alone isn't enough; the tool versions and the full configuration file provide the context needed for an accurate diagnosis. The instructor also mentions Amazon Q Developer in VS Code as another AI option for this workflow.

***

## 1.9 Switching JDK Versions — The Alternatives System

You can have **multiple JDK versions installed simultaneously** on the same machine. The system has a concept of a "default" Java version, and you can switch between installed versions. On Ubuntu, the command is `update-java-alternatives` or the interactive `update-alternatives --config java`, which presents a numbered menu of installed JDK versions. You select the number corresponding to the version you want, and it becomes the system default. [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

The instructor installs both JDK 21 and JDK 17, then switches between them to demonstrate that the vprofile project builds successfully with both. After switching, `java -version` confirms the active version.

***

## 1.10 Installing a Non-Default Maven Version — Binary Download Approach

Unlike JDK, Maven version switching is **not as straightforward** on Linux. The package manager (`apt`) provides one version of Maven (3.8.7 in this case). If you need a different version (like 3.9.9), you must: [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

1. Download the Maven binary archive from the **Apache Maven archive** (`archive.apache.org`)
2. Extract the tarball
3. Place the extracted folder in a system location (the instructor uses `/usr/local/bin/maven3.9`)
4. Use the **full path** to the new Maven's `mvn` binary when running commands

The key difference from JDK: there's no convenient "alternatives" switcher for Maven. If you want to use a non-default Maven version, you specify its complete binary path instead of just typing `mvn`. For example: `/usr/local/bin/maven3.9/bin/mvn clean install`. [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

The instructor says you *could* set it as the system default, but "it's really not required. Why it's not required — that we'll learn in Jenkins." This implies that in Jenkins, the build tool version is configured per job, not at the OS level — Jenkins manages its own tool installations.

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

## What We Are Building

We are setting up a **Java build environment** on an EC2 instance, cloning the vprofile source code, installing the required tools (JDK + Maven), and building the project through various Maven phases. Along the way, we deliberately trigger and fix two types of build failures, learn to switch between JDK versions, and install a non-default Maven version from binary. The final outcome is a successfully built `vprofile-v2.war` artifact. [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

***

## Step 1: Launch an EC2 Instance

Go to **AWS Management Console → EC2 → Launch instance**.

| Setting        | Value                                            |
| -------------- | ------------------------------------------------ |
| Name           | `builder`                                        |
| OS             | Ubuntu 2024                                      |
| Instance type  | t2.micro                                         |
| Key pair       | Create new: `build-key`, `.pem` format           |
| Security group | Create new: `build-SG`, SSH (port 22) from My IP |

Click **Launch instance**. Wait for the instance to reach "Running" state. [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

**Why Ubuntu specifically?** The instructor notes: "base OS can be anything. But you need to have the right version of your tools and then the dependencies will get installed on them." Ubuntu is chosen for this demonstration; Amazon Linux 2023 will be used later. The package manager commands differ between distros, but the build concepts remain identical.

***

## Step 2: SSH Into the Instance

Copy the **public IP** of the instance from the EC2 console.

```bash
ssh -i ~/Downloads/build-key ubuntu@<PUBLIC_IP>
```

* `ssh` — the SSH client command
* `-i ~/Downloads/build-key` — specifies the private key file (downloaded when creating the key pair)
* `ubuntu` — the default username for Ubuntu AMIs
* `@<PUBLIC_IP>` — the instance's public IP address

When prompted "Are you sure you want to continue connecting?", type `yes`. [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

Once connected, switch to root user for administrative operations:

```bash
sudo -i
```

***

## Step 3: Update Package Lists and Install JDK

```bash
apt update
```

This refreshes the local package index so `apt` knows the latest available packages and versions. Always run this before installing anything.

**Search for available JDK packages:**

```bash
apt search jdk | grep 17
```

* `apt search jdk` — lists all packages matching "jdk" (produces a huge list)
* `| grep 17` — filters the output to show only lines containing "17"

You'll see `openjdk-17-jdk` (the development kit) and `openjdk-17-jre` (the runtime only). We need **JDK**, not JRE. [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

**Install JDK 21 first:**

```bash
apt install openjdk-21-jdk -y
```

* `apt install` — installs a package
* `openjdk-21-jdk` — the OpenJDK 21 development kit package
* `-y` — automatically confirms the installation prompt

**Verify the installation:**

```bash
java -version
```

Expected output should show `openjdk version "21.x.x"`. [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

***

## Step 4: Install Maven

```bash
apt install maven
```

Maven is available in Ubuntu 24's default repositories, so no additional repository configuration is needed. [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

**Verify Maven version and its linked JDK:**

```bash
mvn -version
```

This shows two critical pieces of information: the **Maven version** (3.8.7) and the **Java version** it's using (JDK 21, the default). Maven uses whatever Java is set as the system default. [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

***

## Step 5: Clone the Source Code

```bash
git clone https://github.com/hkhcoder/vprofile-project.git
```

Go to `github.com/hkhcoder/vprofile-project` in your browser. Click the **Code** dropdown → select **HTTPS** (make sure it's HTTPS, not SSH) → copy the URL. This is a public repository, so no authentication is needed. [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

**Enter the project directory:**

```bash
cd vprofile-project
```

**Verify you're in the correct location:**

```bash
pwd
ls
```

You should see `pom.xml` and the `src` folder — these confirm you're in a Maven project root.

**Check the current branch:**

```bash
git status
```

You should be on the `local` branch (or any branch — the instructor notes most branches have the same source code for this exercise). If you need to switch branches:

```bash
git branch -a          # list all branches
git checkout <branch>  # switch to a specific branch
```

 [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

***

## Step 6: Run Maven Validate

```bash
mvn validate
```

* `mvn` — the Maven command-line tool
* `validate` — the first lifecycle phase; checks project structure and `pom.xml` integrity

**Expected output:** `BUILD SUCCESS` [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

**Common mistake the instructor demonstrates:** Misspelling the phase name (e.g., typing it wrong) produces: `Unknown lifecycle phase`. Maven doesn't guess — the phase name must be exact.

**Connection to the flow:** This confirms the project structure is valid before attempting more complex phases.

***

## Step 7: Run Maven Test

```bash
mvn test
```

This compiles the source code and executes **unit test cases** (JUnit tests written by the developers). Maven reads test configurations from `pom.xml`, compiles the test code from `src/test`, and runs it. [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

**After completion:**

```bash
ls
```

You should now see a `target` folder. This folder contains the test reports and compiled output. Deeper analysis of test reports is covered in Jenkins lectures. [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

***

## Step 8: Run Maven Install (First Attempt — Will Fail)

```bash
mvn install
```

Since `install` is a later phase, it automatically runs validate → compile → test → package → install. During this process, Maven **downloads all dependencies** from the Global Maven Repository. You'll see extensive download output with URLs pointing to `repo.maven.apache.org`. [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

**Where dependencies are stored:**

```bash
ls ~/.m2/repository/
```

This is Maven's local dependency cache. All downloaded libraries live here.

**Expected failure:** `BUILD FAILURE` with error: `Java heap space` — a resource error, not a code error. The t2.micro instance has only \~579MB available, which isn't enough for Maven's JVM to complete the packaging step (creating the `.war` archive). [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

***

## Step 9: Fix the Heap Space Error

```bash
export MAVEN_OPTS="-Xmx1024m"
```

* `export` — sets an environment variable for the current session and all child processes
* `MAVEN_OPTS` — Maven's recognized environment variable for JVM options
* `-Xmx1024m` — tells the JVM to allow up to 1024MB (1GB) of maximum heap memory

The machine doesn't actually have 1GB free, but the JVM doesn't allocate all of it upfront — it uses what it needs up to the maximum. The OS manages this through virtual memory. The instructor confirms: "It's not going to cause any other harm." [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

**Run install again:**

```bash
mvn install
```

**Expected output:** `BUILD SUCCESS` [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

**Verify the artifact:**

```bash
ls target/
```

You should see `vprofile-v2.war` — the final deployable artifact. The name `vprofile-v2` comes from the `<name>` and `<version>` elements in `pom.xml`. <cite>turn5search5</cite>

***

## Step 10: Clean the Environment and Demonstrate Dependency Reset

To start completely fresh (remove both output and cached dependencies):

```bash
rm -rf target
rm -rf ~/.m2/repository/*
```

* First command removes the build output folder
* Second command removes all cached dependencies (they'll be re-downloaded on next build)

Alternatively, to remove only the output:

```bash
mvn clean install
```

`clean` removes only the `target` folder, **not** the `.m2/repository` dependencies. Then `install` runs the full lifecycle. [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

***

## Step 11: Deliberately Introduce and Fix a Dependency Error

**Introduce the error:**

```bash
vim pom.xml
```

Search for `Jacoco` (a code coverage plugin). Change its version to `8.8.8`. Save and quit (`:wq`). [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

```bash
rm -rf target
rm -rf ~/.m2/repository/*
mvn install
```

**Expected result:** Build may complete but with errors during instrumentation — `error while instrumenting... jacoco 8.8.8`. This is a **compatibility error**: Jacoco version 8.8.8 doesn't support Java 21 (support was added in version 0.8.11). [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

**Diagnose using ChatGPT (or similar AI tool):**

1. Copy the error message
2. Copy the output of `mvn -version` (provides Maven and Java version context)
3. Copy the full `pom.xml` content (`cat pom.xml`)
4. Paste all three into the AI tool with context

The AI tool identifies the incompatibility and recommends upgrading Jacoco to 0.8.11 or later. [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

**Fix the error:**

```bash
vim pom.xml
```

Change the Jacoco version back to a compatible version (0.8.11+). Save and quit.

```bash
mvn clean install
```

**Expected output:** `BUILD SUCCESS` [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

⚠️ **Expert Note:**
The instructor's debugging workflow is the real takeaway: **error message + tool versions + full configuration = accurate AI diagnosis.** Providing only the error message leads to generic suggestions. Providing the full context (Maven version, Java version, `pom.xml`) allows the AI to pinpoint the exact incompatibility. This pattern applies to any build tool, not just Maven.

***

## Step 12: Install JDK 17 and Switch Between Versions

```bash
apt install openjdk-17-jdk -y
```

After installing, `java -version` still shows JDK 21 (the previously installed default). [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

**Switch to JDK 17:**

The instructor uses an AI tool to find the command. On Ubuntu:

```bash
update-alternatives --config java
```

This presents an interactive menu listing all installed Java versions with numbers (0, 1, 2). Type the number corresponding to JDK 17 and press Enter. [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

**Verify:**

```bash
java -version
```

Should now show `openjdk version "17.x.x"`.

**Test the build with JDK 17:**

```bash
cd vprofile-project
mvn clean install
```

Make sure you're in the project folder. The build should succeed — the instructor confirms the vprofile project works with both JDK 17 and 21. [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

***

## Step 13: Install a Non-Default Maven Version from Binary

Go to the Apache Maven archive. The instructor googles "download maven 3 from archive" and finds `archive.apache.org/dist/maven/maven-3/`.

Navigate to version `3.9.9` → `binaries` → right-click on `apache-maven-3.9.9-bin.tar.gz` → **Copy link address**. [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

```bash
cd /tmp
wget <paste-the-copied-URL>
```

* `cd /tmp` — download to the temporary folder to keep things clean
* `wget` — command-line download tool

**Extract the archive:**

```bash
tar xvf apache-maven-3.9.9-bin.tar.gz
```

* `tar` — archive extraction tool
* `x` — extract
* `v` — verbose (show files being extracted)
* `f` — file (followed by the filename)

**Move to a system location:**

```bash
cp -r apache-maven-3.9.9 /usr/local/bin/maven3.9
```

 [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

**Verify the new Maven binary:**

```bash
/usr/local/bin/maven3.9/bin/mvn -version
```

You must use the **full path** because this Maven isn't the system default. The default `mvn` command still points to the apt-installed 3.8.7.

**Build with the non-default Maven:**

```bash
cd ~/vprofile-project
/usr/local/bin/maven3.9/bin/mvn clean install
```

 [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

**Why not set it as default?** The instructor says this will be explained in Jenkins — Jenkins manages tool versions per build job, making OS-level defaults unnecessary.

***

## Step 14: Cleanup

After completing all exercises, **terminate the EC2 instance** from the AWS console to avoid charges. [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

## Maven Project Identity

```
pom.xml at root → this is a Maven project
src/ folder     → developer's Java source code
pom.xml         → Maven's instruction file (metadata, deps, plugins)
```

## pom.xml Structure

```
<version>v2</version>          → opening tag + data + closing tag (/ in close)
<properties>                   → variables block
  <spring.version>6.0.1        → variable definition
</properties>
<dependencies>                 → external libraries block
  <dependency>
    <groupId>...</groupId>
    <artifactId>...</artifactId>
    <version>${spring.version}</version>  → variable reference
  </dependency>
</dependencies>
```

## Maven Phase Chain

```
validate → compile → test → package → install
                                        ↑
Running any phase auto-executes ALL phases before it.

clean = separate lifecycle → removes target/ only (NOT .m2/repository)
mvn clean install = wipe output + full rebuild
```

## Input → Processing → Output Model

```
INPUT:    pom.xml (metadata + deps) + src/ (source code)
PROCESS:  Maven reads pom.xml → downloads deps → compiles → tests → packages
OUTPUT:   target/ folder → contains reports + artifact (vprofile-v2.war)

Artifact name/version/packaging → ALL from pom.xml
```

## Dependency Flow

```
pom.xml declares deps
  → Maven resolves (deps have deps → transitive tree)
    → Downloads from Global Maven Repo (repo.maven.apache.org)
      → Stores in ~/.m2/repository/ (local cache)

To force fresh download: rm -rf ~/.m2/repository/*
```

## JDK vs. JRE

```
JRE = run Java apps (JVM + libraries)
JDK = JRE + compiler + dev tools (javac, etc.)

Building requires JDK (Maven needs the compiler)
Running requires only JRE
```

## Tool Installation Map (Ubuntu)

```
JDK:   apt install openjdk-21-jdk -y
Maven: apt install maven
Clone: git clone <HTTPS URL>

Verify:
  java -version    → JDK version
  mvn -version     → Maven version + which JDK it's using
```

## Version Switching

```
JDK (straightforward):
  Install multiple: apt install openjdk-17-jdk + openjdk-21-jdk
  Switch: update-alternatives --config java → interactive menu → pick number
  Verify: java -version

Maven (NOT straightforward):
  Default: apt-installed version (mvn command)
  Non-default: download binary from archive.apache.org
    → extract tar → copy to /usr/local/bin/maven3.9
    → use FULL PATH: /usr/local/bin/maven3.9/bin/mvn
  Why not set default? → Jenkins manages tool versions per job
```

## Build Failure Diagnosis

```
ERROR TYPE 1: Resource error (not code problem)
  Symptom: "Java heap space"
  Cause: JVM out of memory (t2.micro = ~579MB)
  Fix: export MAVEN_OPTS="-Xmx1024m"
  Note: machine doesn't need 1GB free — JVM uses what it needs up to max

ERROR TYPE 2: Dependency/compatibility error (actual build problem)
  Symptom: "error while instrumenting... jacoco 8.8.8"
  Cause: plugin version incompatible with JDK version
  Fix: update version in pom.xml to compatible version
  Diagnosis: error msg + mvn -version + full pom.xml → feed to AI tool
```

## AI-Assisted Debugging Pattern

```
Collect:
  1. Error message (exact)
  2. Tool versions (mvn -version → shows Maven + Java)
  3. Full config file (cat pom.xml)

Feed ALL THREE to ChatGPT / Amazon Q / similar
→ Context-rich diagnosis → specific fix

Principle: more context = more accurate diagnosis
```

## DevOps/Developer Version Contract

```
Developer provides: required JDK version, Maven version, Node version, etc.
DevOps installs: exact specified versions

"It's your duty to get information from the developer
 on what version of the software or the tools are required."
```

## Clean Reset Sequences

```
Remove output only:      rm -rf target/  (or mvn clean)
Remove deps only:        rm -rf ~/.m2/repository/*
Remove both:             rm -rf target/ && rm -rf ~/.m2/repository/*
Clean rebuild:           mvn clean install (removes target, re-runs all phases)
Full clean rebuild:      rm -rf ~/.m2/repository/* && mvn clean install
```

## Reusable Engineering Patterns

**1. Declarative Build Specification**

```
pom.xml = WHAT to build (deps, versions, packaging)
Maven   = HOW to build (download, compile, test, package)

Developer declares intent → Build tool executes mechanics
Same pattern: Dockerfile, Terraform .tf, Kubernetes YAML
```

**2. Local Cache with Remote Fallback**

```
~/.m2/repository = local cache
Maven Central    = remote source of truth

First run: download from remote → cache locally
Next runs: use cache (fast, no network)
Cache corrupt/stale? → delete cache → re-download

Same pattern: npm node_modules, pip cache, Docker image layers
```

**3. Phase-Chain Execution (Cumulative Lifecycle)**

```
Running phase N auto-executes phases 1..N-1
→ No need to manually run earlier phases
→ Later phases are supersets of earlier phases

install = validate + compile + test + package + install
Same pattern: CI/CD pipeline stages with dependencies
```

**4. Resource Error vs. Logic Error Distinction**

```
Heap space / timeout / disk full = infrastructure problem
  → Fix the environment, not the code

Wrong version / missing dep / syntax error = build problem
  → Fix pom.xml or source code

First step in debugging: classify the error category
```

***

*This completes the full reconstruction. Theory explains Maven's architecture and dependency model. Practical walks through every command with troubleshooting. The Compression Map enables rapid reload of the entire Maven operational workflow, version management, and debugging patterns.* [\[152. Maven Hands-on \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/152.%20Maven%20Hands-on.txt)
