# 🐳 Docker — Building Custom Images, Dockerfiles & Publishing to Docker Hub — Deep Learning Material

**Source:** *Building Images* (Video Lecture Caption File) [\[307-building-images \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/307-building-images.txt)

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

## 1.1 Why Build Custom Docker Images — The Core Problem

So far in the course, we've pulled **official Docker images** from Docker Hub (like `nginx`, `mysql`, `ubuntu`) and run them as-is. But in real projects, you need images tailored to your application — specific packages installed, your application code deployed, your configuration files in place. You need **custom images**. [\[307-building-images \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/307-building-images.txt)

The solution is the same pattern seen across the course in different technologies: take a base artifact, customize it, and capture the result. In AWS, you launch an EC2 instance, configure it, and create an AMI. In GCP, you launch a VM, run a startup script, and create a custom image. In Docker, you write a **Dockerfile**, and Docker builds a custom image from it. The Dockerfile is the recipe; the image is the output.

The instructor draws a direct analogy: "Just like we have `pom.xml` for Maven which builds the artifact, similarly here we'll have Dockerfile that is going to build an image for us." Maven takes source code + `pom.xml` → produces a `.war` artifact. Docker takes a base image + Dockerfile → produces a custom image. The pattern is: **declarative specification → build process → deployable artifact**. [\[307-building-images \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/307-building-images.txt)

***

## 1.2 The Dockerfile — Instruction Set for Image Building

A Dockerfile (capital `D`, no extension) is a text file containing a sequence of **instructions** that tell Docker how to build the image. The instructor emphasizes: "pretty simple, no programming, just instruction and their values." Each instruction is a keyword followed by its arguments. [\[307-building-images \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/307-building-images.txt)

### FROM — The Base Image

Every Dockerfile starts with `FROM`. It specifies the **base image** — the starting point for your custom image. You take an existing official image (Ubuntu, CentOS, Node, Python, etc.) and layer your customizations on top. The instructor uses `FROM ubuntu:latest`. [\[307-building-images \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/307-building-images.txt)

The base image comes from Docker Hub (or another registry). Using official images as bases is recommended because they're maintained, patched, and trusted.

### LABEL — Metadata Tags

Labels are **key-value pairs** that add metadata to the image — author name, project name, version, description. The instructor compares them to AWS tags: "Just like we have tags on AWS." They don't affect the image's behavior; they provide organizational information for humans and tools. [\[307-building-images \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/307-building-images.txt)

### RUN — Execute Commands During Build

`RUN` is the instruction that **makes changes** to the image. It executes a command inside the container being built — installing packages, creating directories, downloading files, modifying configurations. Each `RUN` instruction creates a new **layer** in the image. [\[307-building-images \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/307-building-images.txt)

**Critical optimization:** The instructor explains that every `RUN` instruction creates a separate layer, and "it's a good practice to have less layers as possible." You should combine related commands into a single `RUN` using `&&`:

```dockerfile
RUN apt update && apt install apache2 git -y
```

Instead of:

```dockerfile
RUN apt update
RUN apt install apache2 git -y
```

Both produce the same result, but the first creates one layer while the second creates two. Fewer layers = smaller image, faster pulls. [\[307-building-images \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/307-building-images.txt)

### ADD vs. COPY — Getting Files Into the Image

Both `ADD` and `COPY` place files from the host into the image during build. The critical difference: [\[307-building-images \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/307-building-images.txt)

**COPY** — takes a file and places it in the specified location inside the image. No processing, no extraction. Just a direct copy.

**ADD** — does everything COPY does, plus: it can download files from a URL, and it can **automatically extract archives** (`.tar`, `.tar.gz`, etc.) into the destination directory. If you give ADD a tarball, it untars the contents into the destination. If you give COPY the same tarball, it places the `.tar.gz` file itself (still compressed) in the destination. [\[307-building-images \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/307-building-images.txt)

The instructor demonstrates this distinction practically: the website template is archived as `nano.tar.gz`. Using `ADD nano.tar.gz /var/www/html` extracts the website files into the HTML directory. Using `COPY` would dump the compressed archive file there — not what we want.

### CMD — What Runs When the Container Starts

`CMD` specifies the **default command** that executes when a container is started from this image (when you run `docker run`). It defines what process the container runs. The format is a JSON array (Python list syntax): [\[307-building-images \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/307-building-images.txt)

```dockerfile
CMD ["apache2ctl", "-D", "FOREGROUND"]
```

**Important constraint:** You cannot use `systemctl start apache2` or the `service` command inside a Docker container — those commands rely on systemd, which doesn't run inside containers. Instead, you must use the **binary directly** and run it in the **foreground**. The `-D FOREGROUND` flag tells Apache to stay in the foreground instead of daemonizing — because if the main process backgrounds itself, Docker thinks the container has nothing to do and stops it. [\[307-building-images \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/307-building-images.txt)

🔍 **Deep Dive:**
The FOREGROUND flag is critical and the instructor encounters the exact failure mode when it's misspelled. Without the foreground flag (or with a typo), Apache daemonizes (backgrounds itself), the container's main process exits, and Docker stops the container immediately. The container appears in `docker ps -a` with status `Exited`. This is the most common reason Docker containers exit immediately after starting: the CMD process backgrounds itself.

### ENTRYPOINT — Higher Priority Than CMD

`ENTRYPOINT` is similar to `CMD` — it defines what command runs when the container starts. The difference: if both are present, ENTRYPOINT has **higher priority**. ENTRYPOINT defines the executable, and CMD provides default arguments to it. If a user passes arguments to `docker run`, those arguments override CMD but not ENTRYPOINT. [\[307-building-images \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/307-building-images.txt)

### EXPOSE — Declaring the Container's Port

`EXPOSE` declares which port the container's process listens on. It doesn't actually publish the port — it's **documentation** that tells users and tools which port to map. The actual port mapping happens at `docker run` time with `-p`. [\[307-building-images \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/307-building-images.txt)

The instructor explains the relationship: "a binary runs and creates a process. That process could be binding to a port number... whatever port the process is binding to, you have to give the same port in the expose." Apache binds to port 80, so `EXPOSE 80`.

### VOLUME — Declaring Persistent Storage

`VOLUME` declares a mount point that should be externalized. Data written to this path can be preserved even if the container is deleted. The instructor uses `/var/log/apache2` — the Apache log directory — as an example: "Maybe we don't want to lose the logs if you delete the container." [\[307-building-images \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/307-building-images.txt)

### WORKDIR — Setting the Default Directory

`WORKDIR` sets the working directory inside the container. When you `docker exec` a command, it runs from this directory. When you attach to the container, you land in this directory. The instructor sets it to `/var/www/html`. [\[307-building-images \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/307-building-images.txt)

### ENV, USER, ARG, ONBUILD — Additional Instructions

The instructor mentions these briefly: [\[307-building-images \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/307-building-images.txt)

* **ENV** — sets environment variables inside the container (persists at runtime)
* **USER** — specifies which user runs the process (security practice — avoid running as root)
* **ARG** — defines variables that users can pass at **build time** (not runtime — that's ENV)
* **ONBUILD** — specifies instructions that execute only when this image is used as a base image for another Dockerfile. It's a "delayed instruction" mechanism.

***

## 1.3 The Non-Interactive Build Problem

When building Docker images, the build process must be **completely non-interactive** — there's no human to answer prompts. The instructor hits this problem: the `apt install` command triggers a timezone configuration prompt (`tzdata`), which makes the build process hang waiting for input. [\[307-building-images \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/307-building-images.txt)

The solution: set the environment variable `DEBIAN_FRONTEND=noninteractive` using the `ENV` instruction in the Dockerfile. This tells `apt` and related tools to skip all interactive prompts and use default values. Without this, any package that requires user input during installation will freeze the build process.

***

## 1.4 Image Layers — How Docker Builds Internally

Each instruction in the Dockerfile that modifies the filesystem (`RUN`, `ADD`, `COPY`) creates a new **layer**. A Docker image is a stack of read-only layers. When you push an image to Docker Hub, only the **new layers** (the ones you added on top of the base image) are uploaded — the base image layers already exist on Docker Hub and are referenced, not re-uploaded. [\[307-building-images \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/307-building-images.txt)

The instructor observes this during the push: "So just pushing two layers... Other images are from Ubuntu. So it's just going to mount it from same Docker Hub registry." The Ubuntu layers are already on Docker Hub; only the custom layers (package installations and the application artifact) need to be uploaded. This layer-sharing mechanism makes Docker images efficient to store and transfer.

***

## 1.5 Failed Builds — Dangling Images

When a Docker build fails partway through, Docker creates a **dangling image** — an unnamed, untagged image representing the partial build state. The instructor sees this: "There is also one more image. You won't see any name to it. This is the failed image." These should be cleaned up with `docker rmi <image-id>`. [\[307-building-images \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/307-building-images.txt)

***

## 1.6 Docker Hub — Public and Private Image Registries

**Docker Hub** is the default public registry for Docker images. You can create an account, push your images, and make them available to anyone in the world (public) or only to authenticated users (private). [\[307-building-images \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/307-building-images.txt)

**Image naming convention for pushing:** To push an image to Docker Hub, the image name must be prefixed with your **account name**: `<account>/<image>:<tag>`. For example: `kubeimran/nanoimage:v2`. Without this prefix, Docker doesn't know which account to push to. [\[307-building-images \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/307-building-images.txt)

You can either:

1. Build with the correct name from the start: `docker build -t kubeimran/nanoimage:v2 .`
2. Re-tag an existing image: `docker tag nanoimage:v2 kubeimran/nanoimage:v2`

The instructor notes that re-running `docker build` with a new name but the same Dockerfile doesn't actually rebuild — it reuses the cached layers and just tags the image. "It's not going to run an actual build process. It's just going to tag the image." The image IDs are identical — they're the same image with different names. [\[307-building-images \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/307-building-images.txt)

**Public vs. Private repositories:** Free Docker Hub accounts get one private repository. Public repositories are unlimited. Public means anyone can `docker pull` the image. The instructor uses public for this exercise.

**Authentication:** Before pushing, you must `docker login` from the Docker engine to authenticate with Docker Hub. [\[307-building-images \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/307-building-images.txt)

***

## 1.7 The Full Containerization Workflow

The instructor explicitly names what this process is: **containerization**. "This is called containerization. We have seen how we used to run on EC2 instance. We know how to run it on VMs. If you know that and you know Docker concepts, you know Dockerfile, you can also containerize an application." [\[307-building-images \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/307-building-images.txt)

The workflow is: take an application that traditionally runs on a VM → write a Dockerfile that replicates the setup → build the image → push to a registry → anyone can run it anywhere with a single `docker run` command.

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

## What We Are Building

We are containerizing a website (from tooplate.com) by writing a Dockerfile that builds a custom Ubuntu+Apache image with the website deployed inside it. We then build the image, test it, push it to Docker Hub, and demonstrate that anyone can pull and run it. [\[307-building-images \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/307-building-images.txt)

***

## Step 1: Set Up the Working Directory

SSH into the Docker engine (EC2 instance).

```bash
mkdir images
cd images
```

Create a project subdirectory:

```bash
mkdir nano
```

 [\[307-building-images \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/307-building-images.txt)

***

## Step 2: Download and Prepare the Website Template

Go to **tooplate.com** in your browser. Choose a template (the instructor selects "Nanofolio"). Press **F12** (developer tools), click Download, and copy the download URL from the Network tab.

**Download on the Docker engine:**

```bash
wget <template-download-URL>
```

**Install unzip if needed:**

```bash
apt install unzip -y
```

**Extract:**

```bash
unzip <filename>.zip
```

**Convert to tarball:** Docker's `ADD` instruction can auto-extract `.tar.gz` but not `.zip`. We need the archive in tar format: [\[307-building-images \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/307-building-images.txt)

```bash
cd <extracted-directory>
tar czvf nano.tar.gz *
```

* `tar` — the archive command
* `c` — create archive
* `z` — compress with gzip
* `v` — verbose (show files being archived)
* `f nano.tar.gz` — output filename
* `*` — archive everything in the current directory

**Move the tarball to the project directory and clean up:**

```bash
mv nano.tar.gz ../nano/
cd ../nano/
```

Remove the extracted files and zip (only the tarball is needed). [\[307-building-images \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/307-building-images.txt)

***

## Step 3: Write the Dockerfile

```bash
vim Dockerfile
```

**Note:** Capital `D` in Dockerfile — this is the convention Docker expects.

Write the following content: [\[307-building-images \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/307-building-images.txt)

```dockerfile
FROM ubuntu:latest
LABEL author="Your Name"
LABEL project="nano"
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install apache2 git -y
CMD ["apache2ctl", "-D", "FOREGROUND"]
EXPOSE 80
WORKDIR /var/www/html
VOLUME /var/log/apache2
ADD nano.tar.gz /var/www/html
```

**Line-by-line breakdown:**

* `FROM ubuntu:latest` — base image: Ubuntu, latest tag
* `LABEL author="Your Name"` — metadata tag for the author
* `LABEL project="nano"` — metadata tag for the project name
* `ENV DEBIAN_FRONTEND=noninteractive` — prevents interactive prompts during `apt install` (the `tzdata` prompt would freeze the build without this)
* `RUN apt update && apt install apache2 git -y` — installs Apache and Git in a single layer (combined with `&&` for layer efficiency)
* `CMD ["apache2ctl", "-D", "FOREGROUND"]` — starts Apache in the foreground when the container runs. **FOREGROUND must be spelled correctly with an E** — the instructor's first build failed because of a typo here
* `EXPOSE 80` — declares that Apache listens on port 80
* `WORKDIR /var/www/html` — sets the default working directory
* `VOLUME /var/log/apache2` — exports the log directory for persistence
* `ADD nano.tar.gz /var/www/html` — copies the tarball and **automatically extracts** it into the HTML directory (ADD extracts, COPY would not)

Save and quit (`:wq`). [\[307-building-images \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/307-building-images.txt)

⚠️ **Expert Note:**
The tarball must be in the **same directory** as the Dockerfile (or a subdirectory). Docker build context is the directory specified in the `docker build` command (`.` for current directory). Files outside this context are not accessible during the build.

***

## Step 4: Build the Image (First Attempt — Will Fail)

```bash
docker build -t nanoimage .
```

* `docker build` — initiates the image build process
* `-t nanoimage` — tags the image with the name `nanoimage` (no tag specified, defaults to `latest`)
* `.` — the build context (current directory, where the Dockerfile is)

**Expected failure:** The build hangs at the `apt install` step, prompting for timezone configuration (`tzdata`). Press `Ctrl+C` to abort. [\[307-building-images \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/307-building-images.txt)

**Fix:** Add `ENV DEBIAN_FRONTEND=noninteractive` to the Dockerfile (before the `RUN apt install` line).

**Clean up the failed image:**

```bash
docker images
```

You'll see a `<none>` image — the dangling image from the failed build.

```bash
docker rmi <image-id>
```

 [\[307-building-images \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/307-building-images.txt)

***

## Step 5: Build the Image (Second Attempt — Typo Will Cause Runtime Failure)

After adding the `ENV` line, rebuild:

```bash
docker build -t nanoimage .
```

**Expected:** Build completes successfully. [\[307-building-images \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/307-building-images.txt)

**Test the image:**

```bash
docker run -d --name nanowebsite -p 9080:80 nanoimage
```

* `-d` — detached mode (background)
* `--name nanowebsite` — container name
* `-p 9080:80` — map host port 9080 to container port 80
* `nanoimage` — the image to run

**Check the container:**

```bash
docker ps -a
```

**Expected failure:** Container shows `Exited` status. The CMD has a typo — `FOREGROUND` is misspelled (missing the `E`). Apache starts, can't parse the flag, and exits. The container stops. [\[307-building-images \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/307-building-images.txt)

***

## Step 6: Fix and Rebuild (Third Attempt — Success)

**Fix the Dockerfile:** Correct the CMD to `"FOREGROUND"` (with the E).

**Clean up:**

```bash
docker rm nanowebsite
docker rmi nanoimage
```

**Rebuild with a version tag:**

```bash
docker build -t nanoimg:v2 .
```

Adding `:v2` tags the image explicitly instead of defaulting to `latest`. [\[307-building-images \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/307-building-images.txt)

**Test again:**

```bash
docker run -d --name nanowebsite -p 9080:80 nanoimg:v2
```

**Verify:**

```bash
docker ps
```

Container should show `Up` status. [\[307-building-images \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/307-building-images.txt)

**Access the website:** Open a browser → `http://<ec2-public-ip>:9080`

**Expected:** The Nanofolio template website appears. This confirms the containerization is successful — Apache is running, the website files were extracted correctly by `ADD`, and port mapping is working. [\[307-building-images \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/307-building-images.txt)

***

## Step 7: Push the Image to Docker Hub

**Rebuild with the Docker Hub account prefix:**

```bash
docker build -t kubeimran/nanoimage:v2 .
```

Replace `kubeimran` with your Docker Hub account name. This doesn't re-execute the build — Docker uses cached layers and just tags the image. [\[307-building-images \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/307-building-images.txt)

**Verify both images exist:**

```bash
docker images
```

Both `nanoimg:v2` and `kubeimran/nanoimage:v2` appear with the **same image ID** — they're the same image with different names.

**Login to Docker Hub:**

```bash
docker login
```

Enter your Docker Hub username and password. [\[307-building-images \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/307-building-images.txt)

**Push:**

```bash
docker push kubeimran/nanoimage:v2
```

**Expected output:** Docker pushes only the new layers (your customizations). The Ubuntu base layers already exist on Docker Hub and are referenced, not re-uploaded. [\[307-building-images \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/307-building-images.txt)

**Verify on Docker Hub:** Login to Docker Hub in a browser. You should see the `nanoimage` repository with tag `v2`.

***

## Step 8: Test Pulling and Running the Public Image

**Remove all local copies:**

```bash
docker stop nanowebsite
docker rm nanowebsite
docker rmi kubeimran/nanoimage:v2
docker rmi nanoimg:v2
```

**Run directly from Docker Hub:**

```bash
docker run -d --name nanowebsite -p 9080:80 kubeimran/nanoimage:v2
```

Docker pulls the image from Docker Hub (since it's no longer local), creates a container, and starts it. [\[307-building-images \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/307-building-images.txt)

**Verify:** Access `http://<ec2-public-ip>:9080` — the website appears.

The instructor emphasizes: "Now anybody in the world runs this command, anybody, they will have exactly the same image as I am having. They'll have exactly same container as I'm running." This is Docker's portability promise — identical environments everywhere. [\[307-building-images \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/307-building-images.txt)

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

## Dockerfile = Image Recipe

```
pom.xml → Maven → .war artifact
Dockerfile → docker build → Docker image

Declarative specification → build process → deployable artifact
```

## Dockerfile Instructions — Complete Reference

```
FROM    base image (always first)           FROM ubuntu:latest
LABEL   metadata key-value pairs            LABEL author="name"
ENV     environment variables               ENV DEBIAN_FRONTEND=noninteractive
RUN     execute command (creates layer)     RUN apt update && apt install -y
CMD     default runtime command [json]      CMD ["binary", "-flag"]
ENTRYPOINT  runtime command (higher priority than CMD)
EXPOSE  declare listening port              EXPOSE 80
WORKDIR set default directory               WORKDIR /var/www/html
VOLUME  declare persistent mount point      VOLUME /var/log/apache2
ADD     copy + extract archives + URL       ADD app.tar.gz /dest/
COPY    copy only (no extraction)           COPY file.txt /dest/
ARG     build-time variables
USER    specify runtime user
ONBUILD delayed instruction (for child images)
```

## ADD vs. COPY

```
ADD:  file → destination (extracts .tar.gz, downloads URLs)
COPY: file → destination (raw copy only, no processing)

ADD nano.tar.gz /var/www/html  → extracts contents into html/
COPY nano.tar.gz /var/www/html → places nano.tar.gz file in html/
```

## CMD / ENTRYPOINT Rules

```
CMD:        default command, overridable by docker run args
ENTRYPOINT: fixed command, NOT overridable
Both:       ENTRYPOINT = executable, CMD = default arguments

CRITICAL: process MUST run in FOREGROUND
  CMD ["apache2ctl", "-D", "FOREGROUND"]
  If process daemonizes → container exits immediately
  Exited container = CMD process backgrounded or crashed
```

## Layer Optimization

```
EACH RUN/ADD/COPY = new layer
Fewer layers = smaller image, faster pull

BAD:  RUN apt update
      RUN apt install apache2 -y     → 2 layers

GOOD: RUN apt update && apt install apache2 -y  → 1 layer
```

## Non-Interactive Build

```
Problem: apt install triggers interactive prompts (tzdata)
         → build hangs → must Ctrl+C

Fix: ENV DEBIAN_FRONTEND=noninteractive
     (must appear BEFORE the RUN apt install)
```

## Docker Build Command

```
docker build -t <name>:<tag> <context-path>
  -t = tag (name:version)
  . = current directory as build context

docker build -t nanoimg:v2 .
docker build -t kubeimran/nanoimage:v2 .
  ↑ account prefix required for Docker Hub push
```

## Common Build/Run Failures

```
Build hangs at apt install:
  → missing ENV DEBIAN_FRONTEND=noninteractive

Container exits immediately after start:
  → CMD process daemonized (missing FOREGROUND flag)
  → typo in CMD command
  → check: docker ps -a → status "Exited"

"No such file" during ADD/COPY:
  → file not in build context directory
  → wrong relative path

Dangling <none> image after failed build:
  → docker rmi <image-id> to clean up
```

## Push to Docker Hub Flow

```
1. Image name MUST be: <account>/<image>:<tag>
   docker build -t kubeimran/nanoimage:v2 .
   (reuses cache if same Dockerfile — just re-tags)

2. docker login (username + password)

3. docker push kubeimran/nanoimage:v2
   → pushes only NEW layers (your customizations)
   → base image layers already on Docker Hub (referenced, not re-uploaded)

4. Verify: Docker Hub web UI → repository appears

Public repo: anyone can docker pull
Private repo: only authenticated users (1 free, more paid)
```

## Image Identity

```
docker build -t nanoimg:v2 .
docker build -t kubeimran/nanoimage:v2 .

docker images → SAME image ID, SAME size
They ARE the same image with different name tags
Re-building with same Dockerfile = re-tagging (cache hit)
```

## Full Containerization Workflow

```
1. Prepare artifact (download template → tar czvf → .tar.gz)
2. Write Dockerfile (FROM + RUN + CMD + ADD + EXPOSE)
3. docker build -t name:tag .
4. docker run -d -p hostport:containerport name:tag
5. Verify (browser → http://host:port)
6. docker build -t account/name:tag .  (re-tag for Hub)
7. docker login
8. docker push account/name:tag
9. Anyone: docker run account/name:tag → identical container

"If you know how to run on VMs and you know Dockerfile,
 you can containerize an application."
```

## Verification Sequence

```
docker ps        → container running (Up status) ✓
docker ps -a     → if Exited → CMD problem
browser → http://<ip>:<port> → website appears ✓
docker images    → image exists with correct name/tag ✓
Docker Hub web   → repository + tag visible ✓
```

## Reusable Engineering Patterns

**1. Base + Customize + Capture = Reusable Artifact**

```
AWS:    base AMI → configure → create AMI
GCP:    base image → startup script → snapshot → custom image
Docker: base image → Dockerfile → docker build → custom image

Pattern: start from a trusted base, layer customizations, capture result
         The artifact is reusable; the build process is repeatable
```

**2. Foreground Process = Container Lifecycle**

```
Container lives as long as its main process runs
Process daemonizes → container exits → appears broken

Rule: CMD must run the process in the FOREGROUND
Same in: any container orchestration (K8s pods, ECS tasks)
```

**3. Layer Sharing = Efficient Distribution**

```
Push only new layers → base layers already in registry
Pull only missing layers → reuse locally cached layers

Pattern: content-addressable storage + deduplication
Same in: Git (shared objects), package managers (cached deps)
```

***

*This completes the full reconstruction. Theory explains every Dockerfile instruction, the layer model, and the non-interactive build requirement. Practical walks through every step from artifact preparation through three build attempts (with real failures and fixes) to Docker Hub publishing. The Compression Map enables instant recall of all instructions, the ADD vs. COPY distinction, the foreground process rule, and the full containerization workflow.* [\[307-building-images \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/307-building-images.txt)
