# 📘 VProfile Application Setup — Tomcat Service, Maven Build & Artifact Deployment

**Source:** Caption file covering the Tomcat 10 service setup, Maven-based source code build, and artifact deployment for the VProfile Java web application on the app server VM. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 The Two-Step Nature of Application Server Setup

Setting up Tomcat for VProfile is a **two-step process**: first, you set up the **Tomcat service itself** (the engine), and second, you **build and deploy the application** (the payload). These are fundamentally different activities. Step one creates the infrastructure — a running, managed Tomcat process. Step two produces and places the actual application code so Tomcat can serve it. The video emphasizes this separation explicitly because confusing the two is a common source of misunderstanding. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

The Tomcat service setup covered here is the same procedure taught in the earlier "Systemctl & Tomcat 10" lecture. The video references that lecture as a prerequisite and notes it explains the setup in detail. This project applies the same procedure within the context of the multi-VM VProfile deployment.

***

## 1.2 Tomcat as a Binary-Based Service (No Package Manager Installation)

Unlike most services that can be installed via the system package manager (`dnf install ...`), **Tomcat 10 does not have a direct package manager installation**. You cannot simply run `dnf install tomcat10`. Instead, you must **download the binary tarball directly** from Apache and set it up manually. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

This is a critical distinction. Package-manager-installed services come pre-configured with systemd integration, default directories, and user accounts. When you install from a binary, you must create all of this yourself: the user account, the home directory, the ownership, and the systemd service file. This manual setup is more work, but it gives you full control over the version and configuration — which is why it is the standard approach for Tomcat in production environments.

> 🔍 **Deep Dive**
> The binary-download approach is common across many Java ecosystem tools. Maven (also covered in this video) follows the same pattern — downloaded as a zip, extracted, and used directly from its binary path. This "download binary → extract → configure → create service wrapper" pattern is a recurring infrastructure setup model. It applies to Tomcat, Maven, Jenkins, Nexus, SonarQube, and many other tools in the DevOps ecosystem. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

***

## 1.3 The Tomcat User and Home Directory Model

When you set up a binary-based service, you create a **dedicated system user** to own and run it. For Tomcat, this user is called `tomcat`, and its home directory is `/usr/local/tomcat/`. The user is created **without a login shell**, meaning no one can log into the system as this user — it exists purely to own files and run the Tomcat process. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

The `useradd` command that creates this user simultaneously creates the home directory folder. Then, the extracted Tomcat binary contents are copied into that folder, and ownership is assigned to the `tomcat` user recursively. This ensures that the Tomcat process (running as user `tomcat`) has the necessary file permissions to read its own configuration and serve applications.

> ⚠️ **Expert Note**
> After copying files into `/usr/local/tomcat/`, the ownership defaults to `root` (the user who ran the `cp` command). You **must** explicitly change ownership to `tomcat:tomcat` — otherwise Tomcat cannot read/write its own files, leading to permission-denied errors at runtime. The video verifies this with `ls -l` before and after the `chown` command. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

***

## 1.4 The Systemd Service File — Making a Binary Manageable

A binary sitting in a folder is not a "service" from the operating system's perspective. To manage it with `systemctl` (start, stop, restart, enable on boot), you must create a **systemd service file** — a configuration file that tells systemd how to run the process. For Tomcat, this file is placed at a systemd-recognized location and named `tomcat.service`. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

The service file name directly determines the systemctl command name: because the file is `tomcat.service`, you use `systemctl start tomcat`, `systemctl enable tomcat`, etc. After creating or modifying any systemd service file, you **must** run `systemctl daemon-reload` — this tells systemd to re-read its configuration and recognize the new/changed service. Without this reload, systemd doesn't know the file exists or has changed. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

***

## 1.5 Source Code, Build, and Artifact — The Application Lifecycle

The VProfile source code is Java code stored in a Git repository. **Source code cannot run directly on Tomcat.** It must be **compiled and packaged** into a format Tomcat understands. This transformation process is called **building**, and the tool that performs it is **Maven**. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

The build lifecycle in this context is:

1. **Source code** (human-readable Java files) → cloned from Git (branch: `local`)
2. **Maven build** (`mvn install`) → compiles the code and packages it
3. **Artifact** (`vprofile-v2.war`) → the output package, a WAR file
4. **Deployment** → copy the WAR file into Tomcat's `webapps/` directory

A **WAR file** (Web Application Archive) is the Java equivalent of a tar.gz or zip — it is an archive format specifically designed for Java web applications. Tomcat knows how to read WAR files: when a WAR file appears in the `webapps/` directory, Tomcat automatically **extracts** it into a folder and begins serving the application. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

The video explicitly acknowledges this is a lot to absorb at this stage and reassures that Maven, build tools, and CI/CD concepts will be covered extensively later. For now, the mental model is: **pull code → build with Maven → deploy artifact to Tomcat**.

> 🔍 **Deep Dive**
> Tomcat's auto-extraction behavior is a form of **hot deployment**. Tomcat watches its `webapps/` directory and, upon detecting a new or changed WAR file, extracts it on the fly and serves the application without necessarily requiring a service restart. The video confirms this: restarting Tomcat after deployment is "not mandatory" because Tomcat extracts the artifact and creates the folder automatically. However, restarting is a common practice for a clean state. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

***

## 1.6 Maven — The Build Tool

Maven is a **build automation tool** for Java projects. It takes source code and transforms it into deployable artifacts. Like Tomcat, Maven is an **Apache project** and is installed by **downloading the binary** (a zip file), extracting it, and running it directly from its binary path. There is no `dnf install maven` equivalent used here. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

The video also notes that **Apache httpd** (the web server) is also from Apache — so three key tools in this project (httpd/Nginx's upstream concept, Tomcat, Maven) share the Apache foundation. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

### The Memory Workaround

Maven's build process requires memory. The VM used in this project has **low memory**, and Maven will fail with an "out of memory" error if run directly. The workaround is to set an environment variable (`MAVEN_OPTS`) that tells Maven it has 512 MB of memory available. The video explains this candidly: the VM doesn't actually have that much free memory, but the variable tells Maven it *can* use up to 512 MB if needed. This prevents the out-of-memory failure. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

> ⚠️ **Expert Note**
> The `export MAVEN_OPTS=...` approach is a session-scoped workaround — it only lasts for the current shell session. In production CI/CD pipelines, JVM memory settings are typically configured permanently in Maven's configuration files or in the build server's environment. The "fooling around" described here is a practical hack for resource-constrained lab VMs. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

***

## 1.7 application.properties — The Backend Configuration File

This is the **most architecturally significant file** in the application. `application.properties` is located at `src/main/resources/application.properties` within the source code, and it contains **all the connection details** that the VProfile application uses to reach its backend services. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

It answers the questions: Where is the database? What are the credentials? Where is Memcached? Where is RabbitMQ? Without this file, the application has no idea how to connect to anything.

The file contains:

| Configuration        | Value           | Meaning                                        |
| -------------------- | --------------- | ---------------------------------------------- |
| `jdbc.url`           | `db01:3306`     | Database host (`db01`) and MySQL port (`3306`) |
| Database name        | `accounts`      | The database created during MySQL setup        |
| DB username          | `admin`         | The MySQL user created earlier                 |
| DB password          | `admin123`      | The MySQL password set earlier                 |
| Memcached host       | `mc01:11211`    | Memcached hostname and default port            |
| RabbitMQ host        | `rmq01:5672`    | RabbitMQ hostname and default AMQP port        |
| RabbitMQ credentials | `test` / `test` | RabbitMQ username and password                 |

 [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

The hostnames (`db01`, `mc01`, `rmq01`) are **not IP addresses** — they are resolved to IP addresses through the `/etc/hosts` file entries that were configured during VM setup earlier in the project. This is the connection between the networking setup and the application configuration: the host file entries make these names resolvable. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

The video makes several critical points about this file:

* **Everything connects back.** The database name `accounts`, the user `admin`, the password `admin123` — these were all set up during the MySQL configuration step. The application.properties file is where those choices are *consumed*. If you changed anything during MySQL setup, you must update this file to match. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

* **This file will change across projects.** In AWS migration, Docker, Kubernetes, and other projects later in the course, this same file will be modified to point to different backends. It is a **recurring configuration surface** throughout the entire course. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

* **In real-time work, you must know where this file is.** The video strongly emphasizes memorizing the path (`src/main/resources/application.properties`). In any real project, knowing where backend configurations live is an essential operational skill. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

* **The file gets baked into the artifact.** When you build the package with Maven, this configuration file is included inside the WAR file. This means the backend connection details are determined at **build time**, not runtime (though the video notes that sometimes variables are used instead). [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

> 🔍 **Deep Dive**
> The `application.properties` file is the **single point of coupling** between the application layer and all backend services. It is the operational glue of the entire VProfile architecture. Every service setup step done earlier (MySQL user/password/database, Memcached port, RabbitMQ user/password) was preparing for the values consumed by this file. If any backend detail is wrong here, the application will fail to connect — and the error will appear at the application level, not the backend level, making it harder to diagnose without understanding this file's role. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

***

## 1.8 Artifact Deployment — The ROOT Convention

Tomcat serves applications from its `webapps/` directory. By default, it contains a `ROOT` folder — this is Tomcat's **default application** (the welcome page you see when you access Tomcat). To deploy your own application as the default, you **remove the existing ROOT folder** and **copy your WAR file as `ROOT.war`**. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

The naming matters: `ROOT.war` tells Tomcat to serve this application at the root URL path (`/`). When Tomcat detects `ROOT.war`, it extracts it into a `ROOT` folder automatically. After extraction, you must ensure the extracted folder has `tomcat:tomcat` ownership, because the extraction process may create files owned by a different user. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

***

## 1.9 Firewall Note

The video briefly mentions firewall rules but states that for this project, the firewall is not started and there are no firewall rules to configure. Running or not running firewall commands does not matter for this project. Firewall configuration is deferred to a later section. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are setting up the **application server** for VProfile by: (1) installing and configuring **Tomcat 10** as a systemd-managed service, (2) downloading **Maven** and building the VProfile source code into a deployable WAR artifact, and (3) deploying that artifact onto Tomcat so it serves as the default web application. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

## Why It Matters

The app server is the core of the VProfile stack — it hosts the actual Java application that users interact with. Without this step, all the backend services (MySQL, Memcached, RabbitMQ) set up earlier have nothing to serve.

## Final Operational Outcome

Tomcat running as a managed service, hosting the VProfile application, connected to all backend services via `application.properties`, accessible on its default port.

***

## Phase 1: Tomcat Service Setup

***

### Step 1: Update System and Install Prerequisites

**What we're doing:** Preparing the OS with required packages before Tomcat installation.

```bash
dnf update -y
```

Updates all system packages to their latest versions. `-y` auto-confirms prompts. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

```bash
dnf install epel-release -y
```

Installs the EPEL (Extra Packages for Enterprise Linux) repository, which provides additional packages not in the base repos. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

```bash
dnf install java-17-openjdk java-17-openjdk-devel -y
```

Installs **JDK 17** (Java Development Kit). Tomcat is a Java application — it cannot run without a JVM. The JDK is required (not just the JRE) because Maven will also need it to compile Java source code. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

```bash
dnf install git wget -y
```

Installs **git** (to clone the source code repository) and **wget** (to download binary files from URLs). [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

**Connection to flow:** These are foundational dependencies — without them, no subsequent step works.

***

### Step 2: Download and Extract Tomcat 10 Binary

**What we're doing:** Getting the Tomcat binary since there is no package-manager installation available.

```bash
cd /tmp
```

Move to the `/tmp` directory — a standard temporary workspace for downloads. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

```bash
wget <Tomcat-10-tarball-URL>
```

`wget` downloads the file at the given URL. The URL points to the Apache Tomcat 10 tarball (`.tar.gz`). The exact URL is copied from the course reference material. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

**Common mistake:** The video shows a copy-paste issue where the URL was split or malformed. Ensure the URL is a **single continuous string** with `wget` in front of it. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

```bash
tar -xzvf apache-tomcat-*.tar.gz
```

**Breakdown:** `tar` is the archive tool. `-x` = extract, `-z` = decompress gzip, `-v` = verbose (show files), `-f` = file to operate on. This produces a folder containing the Tomcat binary. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

**Verification:** After extraction, you should see the `apache-tomcat-*` folder in `/tmp`.

***

### Step 3: Create the Tomcat User and Home Directory

**What we're doing:** Creating a dedicated system user to own and run Tomcat.

```bash
useradd --home-dir /usr/local/tomcat --shell /sbin/nologin tomcat
```

**Breakdown:** `useradd` creates a new user. `--home-dir /usr/local/tomcat` sets the home directory (and creates the folder). `--shell /sbin/nologin` prevents interactive login. `tomcat` is the username. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

**What happens internally:** Two things are created simultaneously — the user account in `/etc/passwd` and the directory `/usr/local/tomcat/` on the filesystem.

**Connection to flow:** This directory becomes the permanent home for all Tomcat files, and the user becomes the owner of the Tomcat process.

***

### Step 4: Copy Tomcat Binary to Home Directory and Set Ownership

**What we're doing:** Moving the extracted binary into its permanent location and assigning correct ownership.

```bash
cp -r /tmp/apache-tomcat-*/* /usr/local/tomcat/
```

**Breakdown:** `cp` = copy. `-r` = recursive (copies all subdirectories and files). Copies everything from the extracted folder into the Tomcat home directory. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

**Verification (before ownership fix):**

```bash
ls -l /usr/local/tomcat/
```

At this point, all files are owned by **root** (because root ran the `cp` command). [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

**Fix ownership:**

```bash
chown -R tomcat:tomcat /usr/local/tomcat/
```

**Breakdown:** `chown` = change ownership. `-R` = recursive. `tomcat:tomcat` = user:group. Applies to everything inside `/usr/local/tomcat/`. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

**Verification (after ownership fix):**

```bash
ls -l /usr/local/tomcat/
```

Everything should now show `tomcat tomcat` as owner and group. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

**Common mistake:** Forgetting the `chown` step. Tomcat runs as user `tomcat` — if files are owned by `root`, Tomcat cannot read them, causing startup failures.

***

### Step 5: Create the Systemd Service File

**What we're doing:** Making Tomcat manageable via `systemctl` by writing a service definition file.

```bash
vim /etc/systemd/system/tomcat.service
```

Open (or create) the service file in the systemd directory. Enter insert mode (`i`), paste the service file content from the course reference material (the "black section" shown on screen), then save and quit (`:wq`). [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

**Why this location:** `/etc/systemd/system/` is where custom systemd unit files live. The filename `tomcat.service` determines the service name used with `systemctl`.

**Connection to flow:** Without this file, `systemctl start tomcat` would return "unit not found."

***

### Step 6: Reload Systemd, Start, and Enable Tomcat

```bash
systemctl daemon-reload
```

**Why:** Tells systemd to re-scan its unit files and recognize the newly created `tomcat.service`. This is **mandatory** after creating or modifying any service file. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

```bash
systemctl start tomcat
```

Starts the Tomcat process. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

```bash
systemctl enable tomcat
```

Configures Tomcat to start automatically on system boot. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

**Verification:**

```bash
systemctl status tomcat
```

Should show `active (running)`. Press `Q` to exit the status view. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

**Connection to flow:** Phase 1 is complete — Tomcat is running as a managed service. It is currently serving the default Tomcat welcome page. Next, we replace that with the VProfile application.

***

## Phase 2: Maven Setup and Application Build

***

### Step 7: Download and Extract Maven

**What we're doing:** Installing the build tool needed to compile the VProfile source code.

```bash
cd /tmp
wget <Maven-binary-zip-URL>
```

Downloads the Maven binary as a zip file (also from Apache). [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

```bash
unzip apache-maven-*.zip
```

Extracts the Maven binary. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

```bash
cp -r apache-maven-*/ /usr/local/maven3.9
```

Copies the Maven folder to a permanent location. The path `/usr/local/maven3.9` is chosen by convention — nothing special about this specific location. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

**Connection to flow:** Maven is now available at `/usr/local/maven3.9/bin/mvn` — this full path is used to invoke it since it's not in the system PATH.

***

### Step 8: Set Maven Memory Workaround

**What we're doing:** Preventing an out-of-memory error during the build.

```bash
export MAVEN_OPTS="-Xmx512m"
```

**Breakdown:** `export` sets an environment variable for the current session. `MAVEN_OPTS` is a variable Maven reads for JVM options. `-Xmx512m` tells the JVM it can use up to 512 MB of heap memory. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

**Why:** The VM has low memory. Without this, Maven's build process crashes with an out-of-memory error. The variable tells the JVM it *can* allocate up to 512 MB if needed. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

**Common mistake:** Forgetting this step and getting a cryptic memory error during `mvn install`.

***

### Step 9: Clone the VProfile Source Code

```bash
git clone -b local <repository-URL>
```

Clones the VProfile project repository, specifically the **`local` branch**. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

```bash
cd vprofile-project
ls
```

Enter the project directory. You should see the `src` folder (among others) — this contains the application source code. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

***

### Step 10: Verify application.properties

**What we're doing:** Checking that the backend configuration file has the correct connection details for all services set up in previous lectures.

```bash
vim src/main/resources/application.properties
```

**Critical prerequisite:** You must be inside the `vprofile-project` directory before running this command. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

**What to verify:** [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

* `jdbc.url` → `db01:3306` and database name `accounts`
* DB username → `admin`, password → `admin123`
* Memcached → `mc01:11211`
* RabbitMQ → `rmq01:5672`, user `test`, password `test`

**No changes needed** for this project — the default values match the backend services already configured. But **you must know this file exists and what it contains.** [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

**Connection to flow:** This file gets baked into the artifact during the Maven build. If values are wrong here, the built application will fail to connect to backends.

***

### Step 11: Build the Source Code with Maven

```bash
/usr/local/maven3.9/bin/mvn install
```

**Breakdown:** `/usr/local/maven3.9/bin/mvn` is the full path to the Maven binary (since it's not in the system PATH). `install` is the Maven build phase — it compiles the source code, runs tests, and packages the result into an artifact. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

**What happens internally:** Maven reads the project's `pom.xml` (not explicitly discussed but implied), resolves dependencies, compiles Java classes, and packages everything into a WAR file. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

**This step takes significant time.** The video pauses recording and resumes after completion. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

**Verification after completion:**

```bash
ls
```

A new directory called **`target`** should appear. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

```bash
ls target/
```

Inside `target/`, you should see **`vprofile-v2.war`** — this is the artifact, the deployable package. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

**Common failure:** Out-of-memory error → ensure Step 8 was completed. Build failure → ensure JDK 17 was installed in Step 1.

**Connection to flow:** The artifact is ready. Next, we deploy it to Tomcat.

***

## Phase 3: Artifact Deployment

***

### Step 12: Remove Default Tomcat Application

**What we're doing:** Clearing the way for VProfile to become the default application.

```bash
rm -rf /usr/local/tomcat/webapps/ROOT
```

**Breakdown:** `rm` = remove. `-r` = recursive. `-f` = force (no confirmation prompt). Deletes the `ROOT` folder — Tomcat's default welcome application. You can run this from any directory since the path is absolute. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

***

### Step 13: Copy Artifact to Tomcat webapps

**What we're doing:** Deploying the VProfile artifact as Tomcat's default application.

**Prerequisite:** Ensure you are in the `vprofile-project` directory (where `target/` exists). [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

```bash
cp target/vprofile-v2.war /usr/local/tomcat/webapps/ROOT.war
```

**Breakdown:** Copies the WAR file and renames it to `ROOT.war`. The `ROOT` name is what makes it the default application — Tomcat serves `ROOT` at the base URL path (`/`). [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

**What happens automatically:** Tomcat detects the new WAR file in `webapps/`, extracts it on the fly into a `ROOT` folder, and begins serving the application. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

**Verification:**

```bash
ls /usr/local/tomcat/webapps/
```

You should see both `ROOT.war` (the file you copied) and a `ROOT` folder (auto-extracted by Tomcat). [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

***

### Step 14: Fix Ownership of Extracted Files

```bash
chown -R tomcat:tomcat /usr/local/tomcat/webapps/ROOT
```

The auto-extracted `ROOT` folder may have files owned by a different user. This ensures Tomcat can read everything. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

***

### Step 15: Restart Tomcat and Verify

```bash
systemctl restart tomcat
```

Restarts the Tomcat service for a clean state. The video notes this is **not strictly mandatory** (Tomcat hot-deploys), but it's good practice. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

**Final verification:**

```bash
systemctl status tomcat
```

Should show `active (running)`. Press `Q` to quit. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

**Connection to flow:** The application server is now complete. VProfile is running on Tomcat, connected to all backend services. The next and final step in the project is setting up **Nginx** as the frontend. [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🏗️ Two-Phase Architecture

```
APP SERVER SETUP
├── Phase 1: TOMCAT SERVICE (the engine)
│   ├── dnf update → epel-release → JDK 17 → git, wget
│   ├── wget Tomcat tarball → extract → /tmp
│   ├── useradd tomcat (home=/usr/local/tomcat, nologin)
│   ├── cp extracted binary → /usr/local/tomcat/
│   ├── chown -R tomcat:tomcat /usr/local/tomcat/
│   ├── vim /etc/systemd/system/tomcat.service (paste content)
│   └── daemon-reload → start → enable → status ✓
│
├── Phase 2: MAVEN BUILD (source → artifact)
│   ├── wget Maven zip → unzip → cp to /usr/local/maven3.9
│   ├── export MAVEN_OPTS="-Xmx512m" (memory hack)
│   ├── git clone -b local <repo> → cd vprofile-project
│   ├── VERIFY: vim src/main/resources/application.properties
│   ├── /usr/local/maven3.9/bin/mvn install (SLOW)
│   └── OUTPUT: target/vprofile-v2.war (artifact)
│
└── Phase 3: DEPLOY ARTIFACT (artifact → Tomcat)
    ├── rm -rf /usr/local/tomcat/webapps/ROOT
    ├── cp target/vprofile-v2.war → .../webapps/ROOT.war
    ├── Tomcat auto-extracts ROOT.war → ROOT folder
    ├── chown -R tomcat:tomcat .../webapps/ROOT
    └── systemctl restart tomcat → status ✓
```

 [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

***

## 🔗 application.properties — The Coupling File

```
src/main/resources/application.properties
│
├── jdbc.url → db01:3306 / database: accounts / admin:admin123
├── memcached → mc01:11211
├── rabbitmq  → rmq01:5672 / test:test
│
├── Hostnames (db01, mc01, rmq01) → resolved via /etc/hosts
├── Credentials/DB names → must match what was set during backend setup
├── Gets BAKED INTO the WAR artifact at build time
└── CHANGES across projects: AWS, Docker, K8s (recurring config surface)
```

 [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

***

## ⚡ Key Cause → Effect Chains

```
No dnf package for Tomcat 10
  → Must download binary manually
    → Must create user, homedir, service file manually
      → Must chown after every file copy

Low VM memory
  → Maven mvn install fails (OOM)
    → export MAVEN_OPTS="-Xmx512m" (session workaround)

New/modified systemd service file
  → systemctl daemon-reload REQUIRED
    → Without it: "unit not found" or stale config

WAR copied as ROOT.war
  → Tomcat auto-extracts to ROOT folder
    → Becomes default app at URL path /
    → Extracted files may have wrong ownership → chown needed
```

 [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

***

## 🔄 Binary-Install Pattern (Reusable)

```
APPLIES TO: Tomcat, Maven, Jenkins, Nexus, SonarQube, ...

wget/curl binary archive
  → extract (tar/unzip)
    → cp to /usr/local/<tool>/
      → create dedicated user (nologin)
        → chown -R user:user /usr/local/<tool>/
          → create systemd service file (if needed)
            → daemon-reload → start → enable
```

 [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

***

## 📦 Source → Artifact → Deployment Flow

```
Git repo (branch: local)
  → clone → vprofile-project/
    → src/main/resources/application.properties (VERIFY)
      → mvn install (compile + package)
        → target/vprofile-v2.war (WAR artifact)
          → rm default ROOT → cp as ROOT.war → chown
            → Tomcat serves VProfile at /
```

 [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

***

## 🔑 Critical Paths to Memorize

```
Tomcat home:           /usr/local/tomcat/
Tomcat webapps:        /usr/local/tomcat/webapps/
Tomcat service file:   /etc/systemd/system/tomcat.service
Maven binary:          /usr/local/maven3.9/bin/mvn
App config:            src/main/resources/application.properties
Artifact:              target/vprofile-v2.war
```

 [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

***

## 🧩 Validation Checkpoints

```
After Tomcat install:   systemctl status tomcat → active (running)
After file copy:        ls -l /usr/local/tomcat/ → owned by tomcat
After mvn install:      ls target/ → vprofile-v2.war exists
After artifact deploy:  ls .../webapps/ → ROOT.war + ROOT folder
After final restart:    systemctl status tomcat → active (running)
```

 [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

***

## 🧭 Position in Project Flow

```
Previous VMs (done)         This VM (app01)              Next
─────────────────           ─────────────────            ─────
db01  (MySQL)         →     Tomcat + VProfile app   →    Nginx (web frontend)
mc01  (Memcached)           ↑ connects to all backends
rmq01 (RabbitMQ)            via application.properties
```

 [\[68-app-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/68-app-setup.txt)

***

This completes the app server setup. The VProfile application is now live on Tomcat, wired to all backend services through `application.properties`. The final piece — **Nginx** as the frontend web server — is covered in the next lecture. 🚀
