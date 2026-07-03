# 🧠 Docker ENTRYPOINT vs CMD — Container Process Control & Argument Override Mechanics

**Source:** *308. ENTRYPOINT and CMD* — Docker Series (Video Caption Reconstruction + Command Reference)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 Why This Lecture Exists — The ENTRYPOINT/CMD Confusion

Docker images define the process that runs when a container starts. Two Dockerfile instructions control this: **CMD** and **ENTRYPOINT**. Both specify what happens when you `docker run` an image, but they behave differently, can be used separately or together, and their interaction creates the most common source of confusion in Dockerfile writing. The instructor created a dedicated lecture to resolve this: *"Usually there is a confusion between these two."*

The lecture uses three deliberately simple Dockerfiles — each doing nothing more than printing text — to isolate the behavioral difference between CMD, ENTRYPOINT, and the combination of both. The simplicity is intentional: by stripping away all application complexity, the only thing you observe is how these two instructions control the container's process.

***

## 1.2 CMD — Command and Argument Together

The **CMD** instruction defines the **default command** that runs when a container starts. In its exec form (JSON array), it takes both the command and its arguments:

```dockerfile
FROM ubuntu:latest
CMD ["echo", "hello"]
```

Here, `echo` is the **command** (the binary/shell command to execute) and `hello` is the **argument** to that command. When you `docker run printer:v1`, the container executes `echo hello`, prints `hello`, and exits.

CMD defines the **complete default behavior** — both what to run and what to pass to it. There's nothing for the user to add; the container knows exactly what to do.

The critical behavioral characteristic of CMD: it is **entirely overridable**. If you run `docker run printer:v1 ls`, Docker replaces the entire CMD (`echo hello`) with `ls`. The CMD acts as a default that applies only when the user doesn't specify anything else. This override behavior is important but is not the focus of this lecture — the focus is on how CMD interacts with ENTRYPOINT.

***

## 1.3 ENTRYPOINT — Command Without Argument (User Must Supply)

The **ENTRYPOINT** instruction defines the **fixed command** that always runs when the container starts. In the second Dockerfile:

```dockerfile
FROM ubuntu:latest
ENTRYPOINT ["echo"]
```

Here, only the command `echo` is specified — there is **no argument**. When you `docker run printer:v2`, the container runs `echo` with no arguments, which produces an empty line (echo with no text simply outputs a blank line).

The key behavioral insight: when ENTRYPOINT has a command but no argument, **the user must provide the argument** at runtime. Running `docker run printer:v2 hello` causes the container to execute `echo hello` — the user-provided `hello` becomes the argument to the ENTRYPOINT command.

The instructor states the rule clearly: *"In a Dockerfile, or when you docker inspect any image and you see ENTRYPOINT has a command but does not have any argument, that means the user needs to pass the argument."*

This makes ENTRYPOINT fundamentally different from CMD in its design intent. CMD says "here's the complete default behavior." ENTRYPOINT says "here's the fixed command; you tell me what to do with it."

> 🔍 **Deep Dive:** ENTRYPOINT has **higher priority** than CMD. Unlike CMD, ENTRYPOINT cannot be overridden simply by appending arguments to `docker run`. To override an ENTRYPOINT, you must use the `--entrypoint` flag explicitly. This priority relationship is the architectural reason why ENTRYPOINT is used for the command that must always run, while CMD provides the flexible, overridable part.

***

## 1.4 ENTRYPOINT + CMD Together — Fixed Command with Default Overridable Argument

The third Dockerfile combines both instructions:

```dockerfile
FROM ubuntu:latest
ENTRYPOINT ["echo"]
CMD ["hello"]
```

When used together, the roles split clearly: **ENTRYPOINT provides the command** and **CMD provides the default argument**. When you `docker run printer:v3`, the container executes `echo hello` — ENTRYPOINT's `echo` + CMD's `hello`.

The immediate reaction might be: *"What's the big deal? We could have just used CMD with both command and argument, same as the first Dockerfile."* The instructor anticipates this: *"You will say, what's the big deal? I mean, we could have given just CMD command and argument, same like our first Dockerfile. But watch this."*

The difference is **argument overridability**. When you run `docker run printer:v3 hi`, the CMD portion (`hello`) is **replaced** by the user-provided argument (`hi`), but the ENTRYPOINT (`echo`) remains fixed. The container executes `echo hi`. Running `docker run printer:v3 hello world` executes `echo hello world`. Running `docker run printer:v3` with no argument uses the CMD default: `echo hello`.

This creates a powerful pattern: **the command is locked (ENTRYPOINT), the default argument is provided (CMD), and the user can override the argument without touching the command.**

The instructor identifies two primary use cases for combining ENTRYPOINT and CMD:

**Use Case 1: Fixed command + default overridable argument** — Exactly what the lecture demonstrates. ENTRYPOINT has the command, CMD has the default argument. Users can change what the command operates on without changing the command itself.

**Use Case 2: Initialization script + main process** — ENTRYPOINT runs an initialization script that sets up the environment first, and CMD specifies the actual container process that starts afterward. This is common in production images where a startup script needs to run before the main application.

***

## 1.5 The Priority Rule — The Single Most Important Takeaway

The instructor closes with the foundational rule: *"Just keep one thing in mind: ENTRYPOINT will have higher priority, and then comes CMD."*

This priority manifests in two ways:

1. **When both are present:** ENTRYPOINT defines the command, CMD provides arguments to it. CMD's role shifts from "define the entire default command" to "define the default arguments for ENTRYPOINT."

2. **At runtime override:** Arguments provided to `docker run` override CMD but not ENTRYPOINT. ENTRYPOINT can only be overridden with the explicit `--entrypoint` flag.

This priority relationship is the architectural key to understanding all ENTRYPOINT/CMD behavior.

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building and Why

We are building and running **three Docker images** from three separate Dockerfiles to observe the exact behavioral differences between CMD alone, ENTRYPOINT alone, and ENTRYPOINT + CMD combined. Each image simply prints text — the minimal possible container action — to isolate the instruction behavior from any application complexity.

**Final outcome:** Understanding through direct observation of how `docker run` output changes based on which Dockerfile instructions are used and what runtime arguments are provided.

***

## Step 0: Get the Files onto the Docker Engine

The lecture resources contain a zip file with the three Dockerfiles. Copy it to your Docker engine and extract:

```bash
scp -i <keypath> <zipfilepath> username@<IP>:/home/username/
ssh -i <keypath> username@<IP>
```

```bash
unzip EntryCMD.zip
cd EntryCMD/
ls
```

**Expected directory structure:**

```
EntryCMD/
├── cmd/
│   └── Dockerfile
├── entry/
│   └── Dockerfile
└── entrycmd/
    └── Dockerfile
```

Three directories, each containing a Dockerfile demonstrating one pattern.

***

## Step 1: Build and Run CMD-Only Dockerfile (printer:v1)

### Examine the Dockerfile:

```bash
cat cmd/Dockerfile
```

**Contents:**

```dockerfile
FROM ubuntu:latest
CMD ["echo", "hello"]
```

CMD provides both the command (`echo`) and the argument (`hello`).

### Build the image:

```bash
docker build -t printer:v1 cmd/
```

**Command breakdown:**

* `docker build` — Build a Docker image from a Dockerfile
* `-t printer:v1` — Tag the image as `printer` with version `v1`
* `cmd/` — The build context directory (contains the Dockerfile). Note: the instructor first accidentally provides the full Dockerfile path (`cmd/Dockerfile`) instead of just the directory, then corrects to `cmd/`.

**Verify the image:**

```bash
docker images
```

**Expected:** `printer` image with tag `v1` appears in the list.

### Run the container:

```bash
docker run printer:v1
```

**Expected output:**

```
hello
```

**What happened:** The container started, executed `echo hello` (from the CMD instruction), printed `hello`, and exited.

**Connection to flow:** This establishes the baseline — CMD with command + argument produces a complete default behavior.

***

## Step 2: Build and Run ENTRYPOINT-Only Dockerfile (printer:v2)

### Examine the Dockerfile:

```bash
cat entry/Dockerfile
```

**Contents:**

```dockerfile
FROM ubuntu:latest
ENTRYPOINT ["echo"]
```

ENTRYPOINT provides only the command (`echo`), no argument.

### Build the image:

```bash
docker build -t printer:v2 entry/
```

**Verify:**

```bash
docker images
```

**Expected:** `printer` image with tag `v2` appears.

### Run without argument:

```bash
docker run printer:v2
```

**Expected output:** An empty line (blank). `echo` with no arguments outputs a newline character and nothing else.

### Run with user-provided argument:

```bash
docker run printer:v2 hello
```

**Expected output:**

```
hello
```

**What happened:** The user-provided `hello` became the argument to the ENTRYPOINT command `echo`. The container executed `echo hello`.

**Key observation:** With ENTRYPOINT-only (no CMD), the user **must** provide the argument. Without it, the command runs but produces no useful output.

***

## Step 3: Build and Run ENTRYPOINT + CMD Dockerfile (printer:v3)

### Examine the Dockerfile:

```bash
cat entrycmd/Dockerfile
```

**Contents:**

```dockerfile
FROM ubuntu:latest
ENTRYPOINT ["echo"]
CMD ["hello"]
```

ENTRYPOINT provides the command, CMD provides the default argument.

### Build the image:

```bash
docker build -t printer:v3 entrycmd/
```

### Run without argument (uses CMD default):

```bash
docker run printer:v3
```

**Expected output:**

```
hello
```

**What happened:** No user argument → CMD's `hello` is used as the argument to ENTRYPOINT's `echo` → `echo hello`.

### Run with override argument:

```bash
docker run printer:v3 hi
```

**Expected output:**

```
hi
```

**What happened:** User provided `hi` → CMD's `hello` is **overridden** → ENTRYPOINT `echo` + user argument `hi` → `echo hi`.

### Run with multiple arguments:

```bash
docker run printer:v3 hello world
```

**Expected output:**

```
hello world
```

**What happened:** User provided `hello world` → CMD replaced → `echo hello world`.

### Run again with no argument (confirm default still works):

```bash
docker run printer:v3
```

**Expected output:**

```
hello
```

**What happened:** No override → CMD default `hello` is used → `echo hello`.

**Key observation:** The ENTRYPOINT (`echo`) is **fixed** across all runs. Only the CMD portion changes — either using its default or being overridden by user input. This is the core behavioral difference from CMD-only: the command itself is protected from override.

***

## Behavior Comparison Table

| Run Command                          | v1 (CMD only)       | v2 (ENTRYPOINT only) | v3 (ENTRYPOINT + CMD)          |
| ------------------------------------ | ------------------- | -------------------- | ------------------------------ |
| `docker run printer:<v>`             | `hello`             | *(empty line)*       | `hello` (CMD default)          |
| `docker run printer:<v> hi`          | Replaces entire CMD | `hi`                 | `hi` (CMD overridden)          |
| `docker run printer:<v> hello world` | Replaces entire CMD | `hello world`        | `hello world` (CMD overridden) |

> ⚠️ **Expert Note:** For v1 (CMD only), `docker run printer:v1 hi` would **not** run `echo hi`. It would try to execute `hi` as a command — because CMD is entirely replaced, not just its argument. With v3 (ENTRYPOINT + CMD), `docker run printer:v3 hi` correctly runs `echo hi` because ENTRYPOINT (`echo`) is preserved and only CMD (`hello`) is replaced. This is the critical operational difference.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Three Dockerfiles — Three Behaviors

```
CMD ONLY (v1):
  Dockerfile:  CMD ["echo", "hello"]
  docker run:  echo hello → "hello"
  Override:    docker run printer:v1 ls → runs "ls" (ENTIRE CMD replaced)

ENTRYPOINT ONLY (v2):
  Dockerfile:  ENTRYPOINT ["echo"]
  docker run:  echo → (empty line)
  With arg:    docker run printer:v2 hello → echo hello → "hello"
  Rule:        user MUST provide argument

ENTRYPOINT + CMD (v3):
  Dockerfile:  ENTRYPOINT ["echo"]  CMD ["hello"]
  docker run:  echo hello → "hello" (CMD = default arg)
  Override:    docker run printer:v3 hi → echo hi → "hi" (CMD overridden)
  No arg:      echo hello → uses CMD default
  Rule:        ENTRYPOINT = fixed command, CMD = default overridable argument
```

***

## The Priority Rule

```
ENTRYPOINT > CMD

ENTRYPOINT = FIXED (cannot be overridden by docker run arguments)
CMD        = FLEXIBLE (overridden by any arguments after image name)

To override ENTRYPOINT: must use --entrypoint flag (explicit)
To override CMD: just append arguments to docker run (implicit)
```

***

## Role Assignment When Both Are Present

```
ENTRYPOINT = the COMMAND (what to execute)
CMD        = the DEFAULT ARGUMENT (what to pass to the command)

Container executes: ENTRYPOINT + CMD (or ENTRYPOINT + user args)

USER PROVIDES ARGS?
  YES → ENTRYPOINT + user args    (CMD ignored)
  NO  → ENTRYPOINT + CMD default  (CMD used)
```

***

## Two Use Cases for ENTRYPOINT + CMD

```
USE CASE 1: Fixed command + default overridable argument
  ENTRYPOINT ["echo"]
  CMD ["hello"]
  → command locked, argument flexible

USE CASE 2: Init script + main process
  ENTRYPOINT ["init-script.sh"]
  CMD ["start-app"]
  → init runs first, then main process starts
```

***

## Override Behavior Comparison

```
docker run printer:v1 ls
  CMD only → entire CMD replaced → runs "ls" (not echo)

docker run printer:v3 hi
  ENTRYPOINT+CMD → only CMD replaced → runs "echo hi" (echo preserved)

KEY DIFFERENCE:
  CMD override = replaces EVERYTHING (command + args)
  ENTRYPOINT+CMD override = replaces ONLY the argument (command stays)
```

***

## Build Commands Reference

```bash
docker build -t printer:v1 cmd/        # CMD only
docker build -t printer:v2 entry/      # ENTRYPOINT only
docker build -t printer:v3 entrycmd/   # ENTRYPOINT + CMD
```

***

## Test Matrix

```
docker run printer:v1                  → "hello"
docker run printer:v2                  → (empty line)
docker run printer:v2 hello            → "hello"
docker run printer:v3                  → "hello"     (CMD default)
docker run printer:v3 hi               → "hi"        (CMD overridden)
docker run printer:v3 hello world      → "hello world" (CMD overridden)
```

***

## Decision Map: When to Use What

```
Need a complete default command, no user input expected?
  → CMD ["command", "arg"]

Need user to ALWAYS provide arguments?
  → ENTRYPOINT ["command"]

Need a fixed command with a sensible default that users CAN override?
  → ENTRYPOINT ["command"] + CMD ["default-arg"]

Need an init script before main process?
  → ENTRYPOINT ["init.sh"] + CMD ["main-process"]
```

***

## Reusable Engineering Pattern: Fixed Controller + Flexible Parameter

```
PATTERN:
  FIXED part:    the operation/command (ENTRYPOINT)
  FLEXIBLE part: the parameter/input (CMD, overridable at runtime)

RESULT:
  The system always performs the same TYPE of action
  But users can change WHAT it operates on
  A sensible DEFAULT exists when users provide nothing

WHERE ELSE:
  • CLI tools: git <fixed-subcommand> <user-args>
  • Functions: function name is fixed, parameters are flexible
  • API endpoints: endpoint path is fixed, query params are flexible
  • Kubernetes: container command (fixed) + args (overridable)
  • Shell aliases: alias locks the command, user adds arguments
```

***

## One-Line Mental Reload Trigger

> *"ENTRYPOINT = fixed command (higher priority), CMD = default argument (overridable by user at docker run) — together they create a locked command with flexible default arguments; CMD alone is entirely replaceable; ENTRYPOINT alone requires user to supply arguments."*

This single sentence reconstructs the priority rule, the role assignment when both are present, the override behavior of each instruction individually, and the user-responsibility model of ENTRYPOINT-only images. [\[308-entryp...nt-and-cmd \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/308-entrypoint-and-cmd.txt), [\[308.EntrypointVsCmd \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/308.EntrypointVsCmd.txt)
