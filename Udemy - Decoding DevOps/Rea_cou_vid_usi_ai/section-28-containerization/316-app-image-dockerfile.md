# Multi-Stage Dockerfile — App Image (Tomcat + Maven) — Deep Learning Material

**Source:** [316-app-image-dockerfile.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt?EntityRepresentationId=b1b3827d-f0de-4ff3-9eeb-df2fdd5de1d8) (VTT Caption File) [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 The Problem — Building and Hosting an Application in Docker

The vprofile application is a Java web application that must be **built** (compiled from source code into a deployable artifact using Maven) and then **hosted** (served to users via a Tomcat web server). In a traditional setup, you would install Maven, build the artifact, install Tomcat, and deploy the artifact into Tomcat's `webapps` directory — all on the same server. In Docker, the naive approach would be to do the same: take a single image, install Maven in it, clone the source code, build the artifact, and also run Tomcat in the same image. [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

The problem with this approach is **image bloat**. Maven is a build tool — it downloads enormous numbers of dependencies during the build process. All those dependencies, plus Maven itself, would be baked permanently into the final image. But the running application doesn't need Maven or its dependencies. It only needs the **artifact** (the `.war` file). Including build tools in the runtime image makes the image unnecessarily heavy, slower to pull, and larger to store. [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

This is the exact problem that **multi-stage Docker builds** solve.

***

## 1.2 Multi-Stage Dockerfile — The Core Concept

A multi-stage Dockerfile uses **two or more `FROM` instructions** within a single Dockerfile. Each `FROM` instruction begins a new **stage** — an independent build context with its own base image. The critical capability is that you can **copy artifacts from one stage into another** without carrying over the entire filesystem, tools, or dependencies of the source stage. [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

In this lecture, the Dockerfile has exactly two stages:

**Stage 1 — Build Stage (Maven image)**
This stage uses a Maven base image. Inside this stage, the source code is cloned from Git, the branch is checked out, and `mvn install` is executed to produce the artifact. This stage exists **only** to generate the `.war` file. The Maven image, the source code, and all downloaded dependencies are used during the build but are **not carried forward** to the final image. The stage is given a name using the `AS` keyword (e.g., `AS build_image`) so that the next stage can reference it. [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

**Stage 2 — Runtime Stage (Tomcat image)**
This stage uses a Tomcat base image. It first removes the default Tomcat application, then uses the `COPY --from=build_image` instruction to pull **only the artifact** from Stage 1 into the Tomcat `webapps` directory. The final image produced by `docker build` is this Tomcat image — lightweight, containing only Tomcat and the application artifact, with no trace of Maven or build dependencies. [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

The instructor states the rule explicitly: *"Whenever you have an application that needs to be built and then hosted, you need to have a multi-stage Dockerfile."* This applies universally — for Node.js, Java, Go, or any language where building and running are separate concerns. You build in one stage and host in another. [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

> 🔍 **Deep Dive**
> The `AS build_image` name on the first `FROM` instruction creates a **named reference** to the container that runs during that stage. When `docker build` executes, each stage creates a temporary container. The `COPY --from=build_image` instruction in Stage 2 reaches back into Stage 1's container filesystem to extract the specified file. Once the build completes, Stage 1's container and all its contents are discarded — only the final stage becomes the output image. This is why the final image is small: it inherits nothing from Stage 1 except what was explicitly copied. [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

***

## 1.3 Dockerfile Instructions Used

### `FROM` — Base Image Declaration

Every Dockerfile stage begins with `FROM`. It specifies the base image for that stage. In a multi-stage Dockerfile, multiple `FROM` instructions appear. The `AS <name>` suffix gives the stage a name for cross-stage referencing. [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

### `RUN` — Execute Commands During Build

The `RUN` instruction executes shell commands inside the build container. Each `RUN` instruction creates a **new layer** in the image. The instructor emphasizes a critical best practice: **combine related commands into a single `RUN` instruction** using `&&` (logical AND) instead of writing separate `RUN` instructions for each command. [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

The reason: every separate `RUN` instruction adds a layer to the image, increasing image size and complexity. Combining commands with `&&` keeps everything in a single layer. For example, `cd vprofile-project && git checkout containers && mvn install` is one `RUN` instruction and one layer, whereas three separate `RUN` instructions would create three layers. [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

### `COPY --from=<stage>` — Cross-Stage File Transfer

The `COPY` instruction normally copies files from the host machine into the image. But with the `--from=<stage-name>` flag, it copies files **from a previous build stage's container**. This is the mechanism that makes multi-stage builds work — it is the bridge between the build stage and the runtime stage. [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

In this Dockerfile: `COPY --from=build_image vprofile-project/target/vprofile-v2.war /usr/local/tomcat/webapps/ROOT.war` — this reaches into the build stage's container, navigates to the Maven output directory, extracts the `.war` file, and places it into the Tomcat webapps directory with the name `ROOT.war`. [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

### `EXPOSE` — Port Declaration

The `EXPOSE` instruction declares which port the containerized process listens on. For Tomcat, this is `8080`. The instructor notes that this instruction is **not strictly mandatory** for this Tomcat image because the base Tomcat image already declares it. However, it is included because in real scenarios, you might need to run on a different port or your configuration might specify a different port. Explicitly stating it serves as documentation and ensures clarity. [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

### `CMD` — Process Start Command

The `CMD` instruction specifies the command that runs when a container starts from this image. For Tomcat, it is `catalina.sh run` — the script that starts the Tomcat service. Like `EXPOSE`, this is already present in the base Tomcat image, but the instructor includes it to demonstrate the syntax and for cases where you might need to run a custom script instead. [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

The `CMD` format is a JSON array: `["catalina.sh", "run"]`. The command and its arguments/options are each separate strings within the array, enclosed in double quotes and separated by commas, all within square brackets. [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

***

## 1.4 Tomcat Image — Key Details

The official Tomcat Docker image from Docker Hub runs the Tomcat service on port **8080**. The Tomcat home directory inside the image is at **`/usr/local/tomcat/`** (also referred to as `CATALINA_BASE`). Within this directory, the `webapps/` folder is where application artifacts (`.war` files) are deployed. [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

The default Tomcat image comes with a **default application** pre-installed in `webapps/`. This default application must be **removed** before deploying your own artifact, otherwise both applications would coexist. The removal command is `rm -rf /usr/local/tomcat/webapps/*` — delete everything inside webapps. [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

The artifact is deployed as `ROOT.war` — naming it `ROOT` makes it the **default application** that Tomcat serves at the root URL path (`/`). [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

The instructor points out how to discover these details: check the **Docker Hub documentation** for the official image. If the documentation is insufficient or if you are using an unofficial image, you can pull the image, run a container from it, log into the container, and explore the filesystem manually. This R\&D approach is sometimes necessary. [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

***

## 1.5 Build Artifact Path

When Maven runs `mvn install` on the vprofile source code, the artifact is generated at `vprofile-project/target/vprofile-v2.war`. This path is inside the **build stage container** — it exists only within the Maven container's filesystem during the build. The `COPY --from` instruction must reference this exact path to extract the artifact. [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

***

## 1.6 Dockerfile Skeleton and Naming Conventions

The source code repository (branch: `containers`) contains a pre-created **folder structure** for Docker files: a `Docker-files/` directory with subdirectories for each service — `app/`, `db/`, `web/`. Each subdirectory contains a `Dockerfile` (initially empty). [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

Two important conventions: [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

* The file **must** be named `Dockerfile` with a **capital D**. Docker looks for this exact filename by default during `docker build`.
* In real-time projects, you need to create this skeleton structure yourself — the instructor created it in advance as scaffolding.

***

## 1.7 Why Multi-Stage Reduces Image Size — The Engineering Reasoning

The instructor explains this with particular emphasis. If you built the artifact inside the same image that runs Tomcat (single-stage approach), the final image would contain:

* The Tomcat runtime ✓ (needed)
* Your application artifact ✓ (needed)
* Maven binary ✗ (not needed at runtime)
* All Maven dependencies downloaded during build ✗ (not needed at runtime)
* The source code ✗ (not needed at runtime)
* Git ✗ (not needed at runtime)

With multi-stage, the final image contains **only** Tomcat and the artifact. Everything else — Maven, dependencies, source code — exists only in Stage 1's temporary container and is discarded after the build. The result is a dramatically smaller, cleaner, more secure production image. [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

The instructor generalizes this principle: *"If you have Node.js, you will have a separate Node.js container to build the artifact and another Node.js to run the artifact."* The pattern is universal across languages and frameworks. [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are writing a **multi-stage Dockerfile** for the vprofile application's **app image**. This Dockerfile will use a Maven image to clone the source code and build the artifact, then use a Tomcat image to host the artifact. The final image is a lightweight Tomcat container serving the vprofile application on port 8080. The Docker build itself is not executed in this lecture — only the Dockerfile is written. Building happens in a later lecture after all Dockerfiles (app, db, web) are complete. [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

***

## Step 0: Environment Setup

Open **VS Code**. Ensure you are in the cloned source code repository and on the **`containers`** branch. Navigate to the folder structure: [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

```
Docker-files/
├── app/
│   └── Dockerfile    ← we are writing this
├── db/
│   └── Dockerfile
└── web/
    └── Dockerfile
```

The `Dockerfile` in `app/` is currently empty. This is where we write our instructions. [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

**Naming requirement:** The file must be named `Dockerfile` with a **capital D**. Docker expects this exact name by default when you run `docker build`. [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

***

## Step 1: Gather Required Information

Before writing the Dockerfile, you need two pieces of information that were identified in a previous lecture:

| Component          | Image                                      | Source     |
| ------------------ | ------------------------------------------ | ---------- |
| Build tool         | Maven (with specific tag from setup docs)  | Docker Hub |
| Application server | Tomcat (with specific tag from setup docs) | Docker Hub |

**Find Tomcat details on Docker Hub:** Search for "Tomcat" on Docker Hub → official image page. Key information: [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

* Service runs on port **8080**
* `CATALINA_BASE` (home directory): `/usr/local/tomcat/`
* Artifact deployment path: `/usr/local/tomcat/webapps/`
* Artifact naming: `ROOT.war` makes it the default root application

**From the project setup documentation:** [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

* The artifact must be built using Maven with `mvn install`
* Before building, `application.properties` changes may be needed (database endpoints, etc.)
* The source code is cloned from Git, branch `containers`
* After `mvn install`, the artifact is at `vprofile-project/target/vprofile-v2.war`
* The artifact is copied to Tomcat's webapps as `ROOT.war`

***

## Step 2: Write Stage 1 — Build Stage (Maven)

This stage clones the source code and builds the artifact.

```dockerfile
FROM <maven-image:tag> AS build_image
RUN git clone <repository-url> && cd vprofile-project && git checkout containers && mvn install
```

**Line-by-line breakdown:**

**`FROM <maven-image:tag> AS build_image`**

| Part                | Meaning                                                                  |
| ------------------- | ------------------------------------------------------------------------ |
| `FROM`              | Declares the base image for this stage                                   |
| `<maven-image:tag>` | The Maven Docker image with specific tag (from your setup documentation) |
| `AS build_image`    | Names this stage `build_image` so Stage 2 can reference it               |

**`RUN git clone <repository-url> && cd vprofile-project && git checkout containers && mvn install`**

| Part                      | Meaning                                                           |
| ------------------------- | ----------------------------------------------------------------- |
| `RUN`                     | Executes the following shell commands during image build          |
| `git clone <url>`         | Clones the vprofile source code repository into the container     |
| `&&`                      | Chains commands — next command runs only if the previous succeeds |
| `cd vprofile-project`     | Changes into the cloned directory                                 |
| `git checkout containers` | Switches to the `containers` branch                               |
| `mvn install`             | Builds the artifact (compiles, tests, packages into `.war` file)  |

 [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

**Why all commands are chained with `&&` instead of separate `RUN` instructions:** Each `RUN` creates a new image layer. Multiple `RUN` instructions = multiple layers = larger image size + more complexity. Combining commands with `&&` keeps everything in **one layer**. The instructor explicitly warns against writing separate `RUN` instructions for each command. [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

**What happens when Docker executes this stage:** Docker brings up a temporary container from the Maven image, runs the chained commands inside it, and the resulting filesystem (containing the built artifact at `vprofile-project/target/vprofile-v2.war`) is available for the next stage to reference. [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

***

## Step 3: Write Stage 2 — Runtime Stage (Tomcat)

This stage creates the final lightweight image.

```dockerfile
FROM <tomcat-image:tag>
RUN rm -rf /usr/local/tomcat/webapps/*
COPY --from=build_image vprofile-project/target/vprofile-v2.war /usr/local/tomcat/webapps/ROOT.war
EXPOSE 8080
CMD ["catalina.sh", "run"]
```

**Line-by-line breakdown:**

**`FROM <tomcat-image:tag>`**

| Part                 | Meaning                                                                     |
| -------------------- | --------------------------------------------------------------------------- |
| `FROM`               | Starts a new stage with the Tomcat base image                               |
| `<tomcat-image:tag>` | The official Tomcat image with specific tag (from your setup documentation) |

No `AS` name is needed here — this is the final stage and produces the output image. [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

**`RUN rm -rf /usr/local/tomcat/webapps/*`**

| Part                          | Meaning                                           |
| ----------------------------- | ------------------------------------------------- |
| `RUN`                         | Executes the command during build                 |
| `rm -rf`                      | Recursively force-remove files and directories    |
| `/usr/local/tomcat/webapps/*` | All contents inside the default webapps directory |

**Why:** The base Tomcat image ships with a default application in `webapps/`. This must be removed before deploying our artifact, otherwise the default app would interfere. [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

**Common mistake:** Writing `webapp` instead of `webapps` (missing the 's'). The instructor catches this spelling mistake during the lecture. The correct path has `webapps` (plural). [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

**`COPY --from=build_image vprofile-project/target/vprofile-v2.war /usr/local/tomcat/webapps/ROOT.war`**

| Part                                      | Meaning                                                                                    |
| ----------------------------------------- | ------------------------------------------------------------------------------------------ |
| `COPY`                                    | Copies files into the image                                                                |
| `--from=build_image`                      | Source is the **Stage 1 container** (named `build_image`), not the host machine            |
| `vprofile-project/target/vprofile-v2.war` | The artifact path inside Stage 1's container filesystem                                    |
| `/usr/local/tomcat/webapps/ROOT.war`      | Destination path inside the Tomcat image; `ROOT.war` makes it the default root application |

This is the **critical multi-stage instruction** — it reaches back into Stage 1's container, extracts only the `.war` file, and places it into Stage 2's image. Nothing else from Stage 1 (Maven, dependencies, source code) is carried over. [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

**`EXPOSE 8080`**

| Part     | Meaning                                              |
| -------- | ---------------------------------------------------- |
| `EXPOSE` | Declares that the container will listen on port 8080 |
| `8080`   | Tomcat's default service port                        |

**Note:** This is already declared in the base Tomcat image, so it is technically redundant here. The instructor includes it for explicitness and for cases where your configuration uses a different port. [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

**`CMD ["catalina.sh", "run"]`**

| Part                     | Meaning                                                                 |
| ------------------------ | ----------------------------------------------------------------------- |
| `CMD`                    | Specifies the default command to execute when a container starts        |
| `["catalina.sh", "run"]` | JSON array format — `catalina.sh` is the command, `run` is the argument |

**Format rule:** The command, its options, and arguments are each separate double-quoted strings within square brackets, separated by commas. [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

**Note:** Like `EXPOSE`, this is already present in the base Tomcat image. The instructor includes it to demonstrate the syntax and for situations where you need to run a custom script instead. [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

***

## Step 4: Save the Dockerfile

Press **Ctrl+S** in VS Code to save the file. [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

**What's next:** The Dockerfile is written but **not yet built**. In upcoming lectures, Dockerfiles for the DB image and Web image will be written. Once all Dockerfiles are complete, `docker build` will be executed to build all images.

***

## The Complete Dockerfile (for reference)

```dockerfile
FROM <maven-image:tag> AS build_image
RUN git clone <repository-url> && cd vprofile-project && git checkout containers && mvn install

FROM <tomcat-image:tag>
RUN rm -rf /usr/local/tomcat/webapps/*
COPY --from=build_image vprofile-project/target/vprofile-v2.war /usr/local/tomcat/webapps/ROOT.war
EXPOSE 8080
CMD ["catalina.sh", "run"]
```

 [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

**How to discover image details for unknown images:**

1. **Official images** → read Docker Hub documentation (ports, volume paths, env vars)
2. **Unofficial images** → pull the image, run a container, log into it (`docker exec -it <name> bash`), and explore the filesystem manually. The instructor explicitly recommends this R\&D approach when documentation is insufficient. [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

> ⚠️ **Expert Note**
> If you are unsure where the default application resides in the Tomcat image, or what the `CATALINA_BASE` path is, you can verify by running `docker inspect <tomcat-image:tag>` (as covered in the Docker Volumes lecture) to find volume paths, exposed ports, and CMD/Entrypoint. Alternatively, run a temporary container and explore: `docker run -it --rm <tomcat-image:tag> bash` and `ls /usr/local/tomcat/webapps/`. [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Core Identity

```
Multi-stage Dockerfile = Build artifact in one stage, host it in another
  Purpose: Produce a lightweight runtime image without build tools/dependencies
  Rule: "Whenever you need to build AND host → multi-stage Dockerfile"
```

 [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

***

## Why Multi-Stage Exists

```
Single-stage approach:
  Tomcat + Maven + dependencies + source code + artifact = HEAVY image
                     ↑ not needed at runtime ↑

Multi-stage approach:
  Stage 1 (discarded): Maven + dependencies + source code → produces artifact
  Stage 2 (kept):      Tomcat + artifact ONLY             → LIGHT image

  COPY --from bridges the gap
```

 [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

***

## Two-Stage Architecture

```
STAGE 1: BUILD                          STAGE 2: RUNTIME
─────────────                           ────────────────
FROM maven AS build_image               FROM tomcat
  │                                       │
  ├── git clone source code               ├── rm -rf webapps/* (remove defaults)
  ├── git checkout containers             │
  ├── mvn install                         ├── COPY --from=build_image
  │                                       │     artifact.war → webapps/ROOT.war
  └── Artifact created at:               │
      vprofile-project/                   ├── EXPOSE 8080
        target/                           └── CMD ["catalina.sh", "run"]
          vprofile-v2.war                 
                    │                              │
                    └──── COPY --from ────────────┘
                    
DISCARDED after build                   BECOMES the final image
```

 [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

***

## Dockerfile Instructions Map

```
FROM    → base image for stage (+ AS name for cross-referencing)
RUN     → execute commands during build (creates layers)
COPY    → copy files into image (--from=stage for cross-stage)
EXPOSE  → declare listening port
CMD     → default start command (JSON array format)
```

 [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

***

## Layer Optimization Rule

```
BAD (3 layers):                    GOOD (1 layer):
  RUN cd dir                         RUN cd dir && git checkout branch && mvn install
  RUN git checkout branch
  RUN mvn install

  More layers = larger image + more complexity
  Combine with && = single layer
```

 [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

***

## Tomcat Key Paths

```
CATALINA_BASE:        /usr/local/tomcat/
Artifact location:    /usr/local/tomcat/webapps/ROOT.war
Default app:          /usr/local/tomcat/webapps/*  ← must rm -rf before deploy
Service port:         8080
Start command:        catalina.sh run
ROOT.war naming:      serves at root URL path (/)
```

 [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

***

## Artifact Path (Build Stage)

```
git clone → vprofile-project/
  └── mvn install → target/
                      └── vprofile-v2.war  ← this is what COPY --from extracts
```

 [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

***

## Dockerfile File Conventions

```
Name:      Dockerfile (capital D — mandatory)
Location:  Docker-files/<service>/Dockerfile
Structure: Docker-files/
             ├── app/Dockerfile  ← this lecture
             ├── db/Dockerfile   ← next lecture
             └── web/Dockerfile  ← upcoming
Branch:    containers
```

 [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

***

## CMD Format

```
CMD ["command", "argument1", "argument2"]
     ^^^^^^^^   ^^^^^^^^^^   ^^^^^^^^^^
     double-quoted strings, comma-separated, in square brackets
```

 [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

***

## Image Discovery Approaches

```
Official image → Docker Hub documentation → ports, volumes, env vars, paths
Unofficial image → docker inspect <image:tag>  → metadata extraction
                 → docker run -it <image:tag> bash → manual filesystem exploration
```

 [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

***

## Universal Multi-Stage Pattern

```
Language-agnostic:
  Java:    Maven/Gradle (build) → Tomcat/JRE (run)
  Node.js: Node (build)        → Node/Nginx (run)
  Go:      Go SDK (build)      → Scratch/Alpine (run)
  
  Pattern: Build-tool image AS builder → Runtime image COPY --from=builder

  Build image = temporary, heavy, has tools
  Runtime image = permanent, light, has only artifact
```

 [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

***

## Common Mistakes

```
webapp vs webapps  → spelling: must be "webapps" (plural)
Separate RUN cmds  → creates extra layers → combine with &&
Missing capital D   → "dockerfile" won't be found by docker build
Single-stage build  → image bloat with Maven + dependencies
Forgetting rm -rf   → default Tomcat app coexists with yours
```

 [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

***

## Reusable Engineering Patterns

**Build/Run Separation Pattern (Multi-Stage)**

```
Build environment ≠ Runtime environment
  Build: heavy tools, dependencies, source code → produces artifact
  Run: minimal runtime + artifact only
  
  Bridge: COPY --from extracts ONLY what's needed
  Principle: the runtime should never contain build tools
  
  Recurrence: CI/CD pipelines (CodeBuild phases), compiled languages,
              any system where creation tools ≠ execution tools
```

**Layer Minimization Pattern**

```
Each mutation instruction (RUN) = new image layer
  More layers = larger image + slower pulls + more complexity
  
  Solution: chain commands with && into single RUN
  Trade-off: readability vs layer count (prefer fewer layers)
```

**Named Stage Reference Pattern**

```
AS <name> → creates addressable reference in multi-step process
  Downstream steps reference by name, not by position
  
  Recurrence: Terraform modules, Ansible roles, pipeline stage names,
              any system where outputs of one phase feed into another
```

 [\[316-app-im...dockerfile \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/316-app-image-dockerfile.txt)

***

This completes the full reconstruction of the App Image Dockerfile lecture. **Theory** explains the why and mechanics of multi-stage builds, **Practical** walks through every Dockerfile instruction with full breakdown, and the **Compression Map** enables rapid future recall of the architecture, patterns, and key paths. Let me know if you'd like any section refined! 🚀
