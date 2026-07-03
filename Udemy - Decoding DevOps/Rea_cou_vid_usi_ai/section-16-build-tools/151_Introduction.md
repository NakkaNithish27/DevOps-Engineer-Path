# Maven — The Build Tool (Introduction)

**Source:** Video caption file — *"Maven Introduction"* (from a DevOps/AWS course) [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — What Is a Build Process?

Before understanding Maven, you must understand the problem it solves — the **build process** itself. [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

Developers write source code. They are creating a product — a web application, a mobile app, any software. They keep committing changes to this source code regularly, and with each change, they need to verify that their code still works. This verification involves a chain of steps, and that chain is the build process.

The build process, in its full form, consists of these steps:

**Compile** — The source code is converted from human-readable programming language (Java, .NET, C, C#) into machine-processable output. This applies specifically to **compiled languages** — languages where the code must be translated before it can run. For Java, the compiler `javac` takes `.java` source files and produces `.class` files (bytecode). This step doesn't apply the same way to interpreted languages like Python or Ruby, which don't have a separate compilation step. [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

**Test** — After compilation, the code is tested. These are **unit tests** — tests written by the developers themselves to verify that individual units of their code work as expected. This is explicitly **not software testing** in the QA sense. A unit test checks a small, isolated piece of code: a function, a method, a class. The unit testing framework runs all test cases and returns results (pass/fail). Importantly, you don't need to deploy or even package the code to run unit tests — they operate directly on the compiled source code. [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

**Package** — If compilation succeeds and tests pass, the compiled output is packaged into a distributable archive. The packaging format depends on the target platform and language:

* **Java web applications** → WAR (Web Application Archive) or JAR (Java Archive)
* **Windows software** → EXE or MSI
* **Interpreted languages** (Python, Ruby) → ZIP or TAR (since there's no compiled output, the source itself is archived) [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

**Health Check / Code Analysis** — Developers may also run code analysis to find upcoming bugs or security vulnerabilities in the code. This is a quality gate step that catches problems before the code reaches production. [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

The critical insight: developers don't just write code — they must **regularly** run this entire build process with every commit. Compiling, testing, packaging, analyzing — over and over again. If done manually, this is "too much work if they have to do it very regularly." This repetitive burden is exactly the problem that build tools solve. [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

***

## 1.2 — What Are Build Tools and Why Do They Exist?

Build tools **automate the build process**. Instead of manually running the compiler, then manually running the tests, then manually packaging the output — you define what you want in a configuration file, run a single command, and the build tool executes all the steps automatically in the correct order. [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

The choice of build tool depends on the **programming language** and the **target platform**. The developers or software architects decide which build tool to use and set up the build process. The major build tools mentioned:

* **Maven** — for Java. Configuration in XML format. This is what the course uses because the vProfile project is a Java application.
* **Ant** — also for Java, but older and more scripting-heavy. "In general, Maven supersedes Ant."
* **Gradle** — for Java/JVM languages. Configuration in Groovy format. A more modern alternative to Maven.
* **MSBuild** — Microsoft Build Engine. Used for Microsoft product codebases (.NET, C#, etc.).
* **NANT** — another Windows build tool.
* **Make** — builds executable programs like RPM packages, system-level binaries, or any program executed directly on the operating system. [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

The pattern across all of these: **configuration file** (XML, Groovy, Makefile) + **command** → automated build. The format and tool differ, but the underlying concept is identical. [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

***

## 1.3 — What Is Maven Specifically?

Maven is a build tool for Java. You define your project's structure, dependencies, versioning, and build instructions in an XML file called **pom.xml** (Project Object Model). Then you run Maven commands, and Maven executes the build phases automatically. [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

Maven is the build tool used throughout this course because the vProfile application is a Java source code project. Every time the vProfile artifact (WAR file) was built in previous projects — whether for Lift and Shift or Refactoring — Maven was the tool that compiled the code, ran the tests, and packaged it into the deployable WAR file. [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

***

## 1.4 — Maven Phases: The Build Lifecycle

Maven organizes the build process into a sequence of **phases**. These phases form a lifecycle — an ordered chain where each phase builds on the previous ones. The phases, in order: [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

1. **validate** — Checks that the project directory structure is correct and all necessary information (configuration, metadata) is available. No compilation happens here — it's a sanity check before work begins.

2. **compile** — Uses the Java compiler to compile the source code into `.class` files.

3. **test** — Executes the unit testing framework against the compiled code. Runs all unit test cases and returns pass/fail results. The code doesn't need to be packaged or deployed for this — tests run against the compiled classes directly.

4. **package** — Takes the compiled code and packages it into the distributable format defined in `pom.xml`. For a web application, this produces a WAR file. For a library, this produces a JAR file.

5. **integration-test** — Runs integration tests (tests that verify how different components work together, potentially requiring deployment to a test environment).

6. **verify** — Runs quality checks on the integration test results to confirm that quality criteria have been met.

7. **install** — Downloads all dependencies and stores them in the **local repository** (a local cache on the developer's machine). Dependencies are libraries and packages that the source code depends on — they're declared in `pom.xml`. Maven downloads them from remote Maven repositories on the internet. The install phase caches them locally so they don't need to be re-downloaded on every build.

8. **deploy** — Takes the packaged artifact and pushes it to a **remote repository** where it can be shared with other developers, team members, or DevOps engineers who need to deploy it to servers. [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

***

## 1.5 — Phase Cascading: The Critical Behavioral Rule

The most important behavioral rule of Maven phases: **if you trigger any phase, Maven automatically executes all previous phases first.** [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

If you run `mvn package`, Maven doesn't just package — it first runs validate, then compile, then test, and then package. If you run `mvn test`, it runs validate, compile, then test. If you run `mvn deploy`, it runs the entire lifecycle from validate through deploy. [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

This cascading behavior means you don't need to run each phase individually. You specify the **target phase**, and Maven handles everything that needs to happen before it. This is a fundamental design principle: the build lifecycle is a pipeline where each phase depends on the successful completion of all prior phases. [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

🔍 **Deep Dive:**
The cascading also means that if any earlier phase fails, subsequent phases don't execute. If compilation fails, testing never runs. If tests fail, packaging never happens. This creates a natural **fail-fast** pipeline — problems are caught at the earliest possible point, and the build stops immediately rather than producing a broken artifact. [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

***

## 1.6 — The pom.xml File

The **pom.xml** (Project Object Model) is the central configuration file for a Maven project. It is the build file — the single source of truth that defines everything about the project's build process. [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

What pom.xml contains:

* **Dependencies** — the libraries and packages the source code needs. Maven reads these and downloads them from remote Maven repositories.
* **Packaging method** — whether the output should be WAR, JAR, or another format. This determines what the `package` phase produces.
* **Versioning mechanism** — how the project's version is tracked and incremented.
* **Plugins** — additional tools that extend Maven's capabilities (e.g., code analysis plugins, deployment plugins).
* **Build instructions** — any customization of how phases execute.

The pom.xml is created and maintained by the developers or software architects. As a DevOps engineer, you read and use it — you typically don't write it from scratch, but you need to understand what it contains because it controls the build output you deploy. [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

***

## 1.7 — Maven Dependencies and Repository System

When a Java project depends on external libraries (logging frameworks, database drivers, utility libraries, etc.), those dependencies are declared in `pom.xml`. Maven has a **repository system** that manages these dependencies automatically. [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

When you execute any Maven phase (e.g., `mvn test`), Maven checks the dependencies listed in `pom.xml`. If they're not already present locally, Maven **downloads them from the internet** — from remote Maven repositories (like Maven Central). The `install` phase specifically downloads all dependencies and caches them in a **local repository** on your machine so subsequent builds don't need to re-download them. [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

This repository system means you don't manually download and manage JAR files. You declare what you need in `pom.xml`, and Maven resolves, downloads, and caches everything automatically. [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

***

## 1.8 — The Clean Phase

The video mentions the `clean` phase separately from the main lifecycle. The command `mvn clean deploy` first executes `clean` (which removes output from previous builds — clearing the `target` directory), and then executes the full lifecycle up to `deploy`. [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

Clean is part of a separate lifecycle (the "clean lifecycle") that has its own phases: pre-clean, clean, post-clean. It's commonly combined with build phases to ensure a fresh build from scratch — removing any stale compiled files from previous builds. [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

***

## 1.9 — Maven from a DevOps Perspective

The video explicitly frames the DevOps relationship to Maven: "This is majorly developers' work. As a DevOps, we should be aware about a few things on a build tool like Maven." [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

As a DevOps engineer, you don't write pom.xml files or define build processes. The developers or architects do that. But you need to understand:

* What the build phases are and what they produce
* How to run Maven commands to trigger builds
* What the pom.xml file controls (so you know what to expect as output)
* How dependencies are resolved (because network access to Maven repositories may be needed in your CI/CD pipelines)
* Which phase to run for your specific need (e.g., `mvn install` for a full local build, `mvn package` for just producing the artifact)

The developers will tell you "which phase you need to run and what to expect." Your job is to automate and execute the build in CI/CD pipelines, not to design the build process itself. [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Learning

This is an introductory lecture — the hands-on Maven installation and command execution happens in the next lecture. However, this lecture establishes the practical foundation: understanding the commands you will run, what they do, and what to expect. The video covers Maven installation on both Windows and Linux with different versions, the pom.xml file structure, and Maven commands — all of which will be executed in the following session. [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

***

## Key Maven Commands and Their Behavior

These are the commands referenced in the video. Understanding exactly what each does is essential for the hands-on work that follows. [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

***

### `mvn validate`

```
mvn validate
```

**What it does:** Checks that the project directory structure is correct and all necessary metadata/configuration is present. Does not compile, test, or produce any output.

**When to use:** As a quick sanity check before running a full build — verifying the project is structurally sound. [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

**What happens internally:** Maven reads the pom.xml, verifies required fields are present, checks directory layout conventions. If anything is misconfigured, it fails immediately with an error message.

***

### `mvn compile`

```
mvn compile
```

**What it does:** Runs validate first (cascading), then compiles the Java source code using `javac`, producing `.class` files.

**Cascading:** validate → compile. [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

***

### `mvn test`

```
mvn test
```

**What it does:** Runs validate → compile → test. Executes the unit testing framework against the compiled code. Returns pass/fail results for all test cases.

**Important:** No packaging or deployment happens. Tests run against compiled classes directly. Dependencies are downloaded from remote Maven repositories if not already cached locally.

**What to expect:** Console output showing each test case and its result (pass/fail/skip). A failed test causes the build to fail — no subsequent phases run. [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

***

### `mvn package`

```
mvn package
```

**What it does:** Runs validate → compile → test → package. Produces the distributable archive (WAR/JAR) as defined in pom.xml.

**This is the most commonly used command in the vProfile project context.** When you "build the artifact" in the Lift and Shift or Refactoring projects, you're running something equivalent to `mvn package` (or `mvn install`) to produce the WAR file that gets deployed to Tomcat. [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

**Output:** The packaged artifact appears in the `target/` directory within the project folder.

***

### `mvn install`

```
mvn install
```

**What it does:** Runs validate → compile → test → package → integration-test → verify → install. Downloads all dependencies and caches them in the local Maven repository (`~/.m2/repository` on Linux, `C:\Users\<user>\.m2\repository` on Windows). [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

**When to use:** When you want a full build with all dependencies cached locally. This is the command referenced in the Refactoring project when building the vProfile artifact: `mvn install` ensures all dependencies are resolved and the artifact is built.

***

### `mvn deploy`

```
mvn deploy
```

**What it does:** Runs the entire lifecycle (validate through deploy). After packaging, pushes the artifact to a remote repository for sharing.

**When to use:** In CI/CD pipelines where the built artifact needs to be published to a shared artifact repository (like Nexus or Artifactory) for other teams to consume. [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

***

### `mvn clean deploy`

```
mvn clean deploy
```

**What it does:** First runs the `clean` lifecycle (removes previous build output from `target/` directory), then runs the full build lifecycle up to deploy.

**Why combine clean:** Ensures a completely fresh build — no stale compiled files from previous builds contaminating the new build. This is a best practice for CI/CD pipelines where reproducibility matters. [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

***

### `mvn verify`

```
mvn verify
```

**What it does:** Runs validate → compile → test → package → integration-test → verify. Checks integration test results against quality criteria. [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

***

## How to Find Maven Documentation

The video references the official Maven Build Lifecycle documentation. To find it: search Google for **"Build Lifecycle Maven"** and you'll reach the official Apache Maven documentation page. This page covers all phases, command-line usage, packaging options, plugin configuration, and lifecycle bindings. [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

The video recommends reading it but adds: "You really don't need to spend too much time on this. This is majorly developers' work." As a DevOps engineer, awareness is sufficient — deep expertise in pom.xml authoring is the developer's domain. [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

***

## Connection to Previous Projects

Every time the vProfile artifact was built in previous project lectures — whether for Lift and Shift (build locally → upload to S3 → deploy to EC2) or Refactoring (build with backend endpoints → deploy to Beanstalk) — Maven was the build tool executing the process. The `application.properties` file that was updated with backend endpoints is part of the Maven project, and the `mvn install` or `mvn package` command is what compiled everything and produced the WAR file. [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

⚠️ **Expert Note:**
In real CI/CD pipelines (Jenkins, GitHub Actions, etc.), the Maven command is typically `mvn clean install` or `mvn clean package` — always with `clean` first to ensure reproducible builds. The pipeline automates what was done manually on the laptop in the Lift and Shift project. Understanding Maven commands is prerequisite knowledge for the CI/CD lectures that follow in the course. [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## System Identity

```
TOOL:    Maven
TYPE:    Build tool for Java
PURPOSE: Automate the build process (compile → test → package → deploy)
CONFIG:  pom.xml (XML format)
CONTEXT: Used throughout this course to build the vProfile WAR artifact
```

 [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

***

## The Build Process (Universal Pattern)

```
Source Code (Java, .NET, C, etc.)
    │
    ▼
COMPILE → language-specific compiler (javac for Java)
    │      produces: .class files (Java), .obj files (C), etc.
    ▼
TEST → unit tests (developer-written, not QA testing)
    │    tests code WITHOUT packaging or deploying
    ▼
PACKAGE → archive into distributable format
    │      Java web app → WAR
    │      Java library → JAR
    │      Windows → EXE / MSI
    │      Interpreted (Python/Ruby) → ZIP / TAR
    ▼
HEALTH CHECK / CODE ANALYSIS → find bugs + security vulnerabilities

PROBLEM: Doing this manually on every commit = too much work
SOLUTION: Build tools automate the entire chain
```

 [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

***

## Build Tool Landscape

```
LANGUAGE/TARGET          BUILD TOOL       CONFIG FORMAT
─────────────────────────────────────────────────────────
Java                     Maven            XML (pom.xml)
Java                     Ant              XML (more scripting)
Java/JVM                 Gradle           Groovy
Microsoft/.NET           MSBuild          XML
Windows                  NANT             XML
System executables/RPM   Make             Makefile

RULE: Language + target → determines build tool
      Developers/architects choose the tool
      DevOps executes and automates it
```

 [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

***

## Maven Phase Lifecycle (Ordered Pipeline)

```
validate → compile → test → package → integration-test → verify → install → deploy

CASCADING RULE:
  Triggering ANY phase → automatically runs ALL previous phases first

  mvn validate   = validate
  mvn compile    = validate → compile
  mvn test       = validate → compile → test
  mvn package    = validate → compile → test → package
  mvn install    = validate → ... → install
  mvn deploy     = validate → ... → deploy (full chain)

SEPARATE LIFECYCLE:
  clean (removes previous build output)
  mvn clean deploy = clean first, then full build lifecycle
```

 [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

***

## Phase Details (Quick Reference)

```
validate         → project structure + metadata check (sanity check)
compile          → javac compiles .java → .class files
test             → runs unit testing framework (no deploy/package needed)
package          → .class files → WAR/JAR (format defined in pom.xml)
integration-test → tests across components (may need deployment)
verify           → quality gate on integration test results
install          → download dependencies → cache in local repo (~/.m2/)
deploy           → push artifact to remote repo (for sharing)
```

 [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

***

## pom.xml: Central Configuration

```
pom.xml (Project Object Model)
  ├── Dependencies      → external libraries needed (auto-downloaded)
  ├── Packaging method  → WAR, JAR, etc. (controls package phase output)
  ├── Versioning        → project version tracking
  ├── Plugins           → extend Maven capabilities
  └── Build instructions→ customization of phase behavior

WHO WRITES IT: Developers / Software Architects
WHO USES IT:   DevOps (runs Maven commands, automates in CI/CD)
```

 [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

***

## Maven Dependency Flow

```
pom.xml declares dependencies
        │
        ▼
Maven checks local repo (~/.m2/repository)
        │
   Found? ──YES──→ Use cached version
        │
       NO
        │
        ▼
Download from remote Maven repositories (internet)
        │
        ▼
Cache in local repo (won't re-download next time)
```

 [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

***

## Fail-Fast Pipeline Behavior

```
validate FAIL → STOP (nothing runs)
compile FAIL  → STOP (no tests, no package)
test FAIL     → STOP (no packaging of broken code)
package FAIL  → STOP (no distribution of broken artifact)

PRINCIPLE: Problems caught at earliest possible phase
           Broken code never reaches packaging or deployment
```

 [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

***

## Connection to Course Projects

```
Lift & Shift:
  Local machine → mvn install → WAR file → S3 → Tomcat EC2

Refactoring:
  Update application.properties with endpoints
    → mvn install → WAR file → Beanstalk (one-click deploy)

CI/CD (upcoming):
  Jenkins → mvn clean install → automated build pipeline

Maven is the BRIDGE between source code and deployable artifact
```

 [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

***

## DevOps vs. Developer Responsibility

```
DEVELOPER:                          DEVOPS:
  ├── Writes source code              ├── Runs Maven commands
  ├── Writes unit tests               ├── Automates build in CI/CD
  ├── Creates pom.xml                 ├── Understands phase output
  ├── Defines dependencies            ├── Ensures network access to repos
  ├── Chooses packaging format        ├── Deploys the produced artifact
  └── Sets up build process           └── Monitors build pipeline

BOUNDARY: DevOps doesn't author pom.xml — DevOps executes and automates
```

 [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

***

## Reusable Engineering Patterns

| Pattern                             | Manifestation                                                         |
| ----------------------------------- | --------------------------------------------------------------------- |
| **Ordered Pipeline with Cascading** | Triggering any phase auto-runs all predecessors                       |
| **Fail-Fast**                       | Build stops at first failure — broken code never progresses           |
| **Configuration-Driven Automation** | pom.xml defines everything → single command executes                  |
| **Dependency Resolution + Caching** | Declare deps → auto-download → local cache → reuse                    |
| **Separation of Concerns**          | Developers define build process; DevOps automates and executes it     |
| **Clean Build (Reproducibility)**   | `mvn clean` removes stale output → ensures fresh, deterministic build |
| **Build Tool ↔ Language Binding**   | Each language ecosystem has its canonical build tool                  |

 [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

***

## One-Line System Reconstruction

> **Maven automates the Java build lifecycle (validate → compile → test → package → install → deploy) via pom.xml configuration, where triggering any phase cascades through all predecessors, dependencies are auto-resolved from remote repos and cached locally, and the output WAR/JAR artifact is what gets deployed to Tomcat/Beanstalk in the vProfile project pipeline.** [\[151. Introduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/151.%20Introduction.txt)

***

This completes the full reconstruction of the Maven Introduction lecture. It provides the foundational build tool knowledge that connects the "build the artifact" step referenced in every previous project (Lift and Shift, Refactoring) to the actual tool and process behind it — and sets up the hands-on Maven lecture that follows. Let me know if you'd like any section expanded or adjusted! 🚀
