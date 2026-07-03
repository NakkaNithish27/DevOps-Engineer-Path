# 🧠 GCP Managed Instance Group (MIG) — Instance Templates, Auto Scaling & Production Compute

**Source:** *298. Building a Managed Instance Group (MIG)* — GCP vProfile Project Series (Video Caption Reconstruction)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 Why a Managed Instance Group Exists — The Auto Scaling Problem

At this point in the GCP vProfile project, a custom image exists with the fully configured Tomcat application, backend services (Cloud SQL, Memorystore) are running, and DNS is configured. But so far, there's only a way to launch **one** instance manually from that image. In production, a single instance is neither scalable nor highly available — if it crashes, the application goes down. If traffic spikes, a single instance can't handle the load.

A **Managed Instance Group (MIG)** solves this by managing a fleet of identical VM instances created from the same template. It maintains a desired number of instances (size), replaces failed instances automatically, and — critically — can **auto-scale**: adding instances when load increases and removing them when load decreases. This is GCP's equivalent of **AWS Auto Scaling Group** (as established in the GCP Introduction lecture, §288).

The MIG is the compute layer that sits between the backend services (Cloud SQL, Memorystore) and the load balancer (configured in the next lecture). It's the **scalable application tier**.

***

## 1.2 Instance Template — The Blueprint for Every Instance

Before creating a MIG, you need an **Instance Template**. A template is a pre-defined configuration that specifies **everything** about how an instance should be launched: machine type, image, subnet, region, network tags, whether it gets an external IP, and other settings. Every instance the MIG creates will be an exact copy of this template.

The template itself does not create any instance — it's purely a **configuration object**. It defines the "what" and "how" of instance creation. The MIG then uses this template to create and manage actual instances.

This maps directly to **AWS Launch Template**, which serves the identical purpose: define instance configuration once, use it repeatedly through the Auto Scaling Group.

### Machine Type Selection — Build vs. Run

The instructor makes a deliberate machine type decision that reveals an important operational principle. When the custom image was created (in the previous lecture), a **larger instance type** was used (e2-medium or e2-small) because the build process — installing Tomcat, deploying the application, running builds — required more compute resources. But for the template that will be used in production to **run** the Tomcat service, **e2-micro** is sufficient.

This is a cost optimization pattern: use larger instances for build/configuration tasks (temporary, one-time cost), and smaller instances for runtime (ongoing, repeated cost through auto-scaling). The instructor frames it: *"To create the image we mentioned e2-medium or e2-small because there was the build process and all those things were happening, so we needed a bigger instance type. But just to run the Tomcat service, e2-micro will be fine."*

### The `--no-address` Flag — Private Subnet Discipline

The template includes `--no-address`, which ensures instances launched from this template do **not** receive an external (public) IP address. The instructor emphasizes this as a critical rule: *"All the time, whenever you launch instances in the private subnet, if you are working on public-private subnet in the VPC, when you launch instances in the private subnet, always make sure there is `--no-address` so it does not get any external IP address."*

This is not just a configuration detail — it's a **security discipline**. Instances in private subnets should never have public IPs. If they did, they would be directly reachable from the internet, defeating the purpose of the private subnet architecture (see VPC Design lecture, §264). The `--no-address` flag enforces this at the template level, ensuring every instance the MIG creates respects the private subnet design.

### Network Tags — Firewall Rule Association

The template specifies `--tags=app`, which applies the same **firewall rule tag** used throughout the project. In GCP, firewall rules are associated with instances via tags (equivalent to AWS security group attachment). By tagging instances with `app`, the two firewall rules configured earlier in the project automatically apply to every instance the MIG creates.

> 🔍 **Deep Dive:** The template encapsulates the **entire operational identity** of a production instance: what it runs (image), how powerful it is (machine type), where it lives (subnet, region), how it's secured (no external IP, firewall tags). By defining all of this in a template, you guarantee that every instance in the fleet is identical — no configuration drift, no manual mistakes. This is the infrastructure equivalent of a class definition in object-oriented programming: the template is the class, each instance is an object.

***

## 1.3 Managed Instance Group — The Fleet Controller

The MIG is the component that actually creates, manages, and scales instances using the template. When you create a MIG, you specify:

* **Template** — Which instance template to use
* **Zone** — Where to deploy (e.g., `us-central1-a`)
* **Size** — The initial number of instances to create

In this lecture, the MIG is created with a **size of 2** — it immediately launches two VM instances from the template. These instances appear in the Compute Engine section with status **"Ready."**

At this point (before auto-scaling is configured), the MIG is effectively a **static group** — it maintains exactly 2 instances. If one crashes, the MIG replaces it. But it won't add more under load or remove any when idle.

***

## 1.4 Auto Scaling — Dynamic Capacity Management

After creating the MIG with a fixed size, the instructor adds **auto-scaling parameters** as a separate step. Auto-scaling transforms the MIG from a static group into a dynamic, load-responsive fleet. The configuration defines:

**Minimum replicas** — The lowest number of instances the MIG will maintain, even under zero load. This is your baseline capacity.

**Maximum replicas** — The upper limit. The MIG will never create more instances than this, regardless of load. This is your cost ceiling.

**Scaling triggers** — The conditions that cause the MIG to add or remove instances. Two triggers are configured:

### Trigger 1: CPU Utilization (Target: 0.6 = 60%)

If the **average CPU utilization across all instances** exceeds 60%, the MIG starts **scaling out** (adding instances). When CPU drops below the target, it **scales in** (removing instances). The instructor explains: *"If the CPU utilization goes above 60%, it's going to start scaling out, and this will be 60% of all the instances."*

### Trigger 2: Load Balancing Utilization (Target: 0.8 = 80%)

If the **load balancer utilization** exceeds 80%, the MIG scales out. The instructor notes: *"Mostly for the load balancer that serves the HTTP/HTTPS request, this trigger is set."* This trigger responds to the actual traffic load rather than just CPU — a more direct measure of application demand.

The instructor acknowledges: *"We don't have any load balancer yet. We're going to set it later."* The trigger is configured proactively — it won't activate until the load balancer is created and connected in the next lecture, but the scaling policy is already in place.

> ⚠️ **Expert Note:** Having **two triggers** provides defense in depth. CPU-based scaling catches compute-heavy scenarios (complex processing, inefficient queries). Load-balancing-based scaling catches traffic-heavy scenarios (many concurrent lightweight requests that individually don't spike CPU but collectively overwhelm capacity). In production, it's common to have both.

***

## 1.5 The Complete Compute Architecture at This Point

With the MIG configured, the compute architecture for the vProfile project is:

```
Instance Template (vprofile-template)
  → defines: e2-micro, custom image, private subnet, no external IP, app tag
       ↓
Managed Instance Group (vprofile-mig)
  → zone: us-central1-a
  → size: 2 (initial)
  → auto-scaling: min/max replicas
  → triggers: CPU > 60% OR LB utilization > 80%
       ↓
2+ VM instances running Tomcat (vProfile app)
  → connect to Cloud SQL (MySQL) via private DNS
  → connect to Memorystore (Memcached) via private DNS
```

What remains: the **load balancer** as the front-end entry point that routes internet traffic to this MIG. The instructor positions this: *"We are very close to completing our project. Load balancer, front-end part is remaining."*

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building and Why

We are creating a **Managed Instance Group (MIG)** for the vProfile application on GCP. This involves three commands executed in sequence: create an Instance Template (the VM blueprint), create the MIG (the fleet of instances), and configure auto-scaling (dynamic capacity). By the end, two VM instances are running the application with auto-scaling policies ready to respond to load.

**Final outcome:** A MIG named `vprofile-mig` with 2 running instances, auto-scaling configured with CPU (60%) and load balancing (80%) triggers, ready to be connected to a load balancer in the next lecture.

***

## Step 1: Create the Instance Template

```bash
gcloud compute instance-templates create vprofile-template \
  --machine-type=e2-micro \
  --image=vprofile-image \
  --subnet=<private-subnet-name> \
  --region=us-central1 \
  --no-address \
  --tags=app
```

**Command breakdown:**

* `gcloud compute instance-templates create` — The GCloud CLI command to create an instance template.
* `vprofile-template` — The name of the template. Referenced later when creating the MIG.
* `--machine-type=e2-micro` — The VM size. e2-micro is sufficient for running Tomcat in production. (Smaller than the e2-medium/e2-small used during image creation — see Theory §1.2 for the build-vs-run reasoning.)
* `--image=vprofile-image` — The custom image created in the previous lecture, containing the fully configured Tomcat application.
* `--subnet=<private-subnet-name>` — The private subnet where instances will launch. Instances live in the private subnet for security.
* `--region=us-central1` — The GCP region.
* `--no-address` — **Critical flag.** Ensures no external/public IP is assigned. Mandatory for private subnet instances (see Theory §1.2).
* `--tags=app` — Applies the `app` network tag, which associates the two firewall rules configured earlier in the project with every instance created from this template.

**Expected result:** Template created quickly — it's just configuration metadata, not an actual instance.

**Verification:** Navigate to **Compute Engine → Instance Templates** in the GCP console. The `vprofile-template` should be visible.

**Common mistakes:**

| Mistake                                   | Consequence                                                     | Fix                                                   |
| ----------------------------------------- | --------------------------------------------------------------- | ----------------------------------------------------- |
| Forgetting `--no-address`                 | Instances get public IPs in private subnet — security violation | Always include for private subnet templates           |
| Wrong image name                          | Template references a non-existent image — MIG creation fails   | Verify image name: `gcloud compute images list`       |
| Wrong tag name                            | Firewall rules don't apply — instances unreachable or unsecured | Match the exact tag used in firewall rule definitions |
| Using build-time machine type (e2-medium) | Unnecessary cost at scale — each MIG instance costs more        | Use e2-micro for runtime; larger types only for build |

**Connection to flow:** The template is the input for the MIG. Without it, the MIG has no blueprint to create instances from.

***

## Step 2: Create the Managed Instance Group

```bash
gcloud compute instance-groups managed create vprofile-mig \
  --zone=us-central1-a \
  --template=vprofile-template \
  --size=2
```

**Command breakdown:**

* `gcloud compute instance-groups managed create` — Creates a managed instance group (the `managed` keyword distinguishes it from an unmanaged instance group).
* `vprofile-mig` — The name of the MIG.
* `--zone=us-central1-a` — The specific availability zone. The MIG and its instances live in this zone.
* `--template=vprofile-template` — References the template created in Step 1.
* `--size=2` — The initial number of instances to create immediately.

**What happens internally:** GCP reads the template, launches 2 VM instances in `us-central1-a` with the specified configuration (e2-micro, custom image, private subnet, no external IP, app tag). The instances boot, start Tomcat, and connect to Cloud SQL and Memorystore via private DNS.

**Expected result:** Two instances created and shown with status **"Ready"**.

**Verification:**

1. **Console:** Compute Engine → Instance Groups → `vprofile-mig` → should show 2 instances.
2. **Console:** Compute Engine → VM Instances → should show 2 new VMs with names auto-generated by the MIG.

**Connection to flow:** The MIG now exists with a fixed size of 2. Auto-scaling is added next to make it dynamic.

***

## Step 3: Configure Auto Scaling

```bash
gcloud compute instance-groups managed set-autoscaling vprofile-mig \
  --zone=us-central1-a \
  --max-num-replicas=<max> \
  --min-num-replicas=<min> \
  --target-cpu-utilization=0.6 \
  --target-load-balancing-utilization=0.8
```

**Command breakdown:**

* `gcloud compute instance-groups managed set-autoscaling` — Adds auto-scaling policies to an existing MIG.
* `vprofile-mig` — The MIG to configure.
* `--zone=us-central1-a` — Must match the zone used during MIG creation.
* `--max-num-replicas=<max>` — Maximum number of instances the MIG can scale to. This is your cost ceiling.
* `--min-num-replicas=<min>` — Minimum number of instances maintained at all times. This is your baseline capacity.
* `--target-cpu-utilization=0.6` — **Trigger 1:** Scale out when average CPU across all instances exceeds 60%. Scale in when it drops below.
* `--target-load-balancing-utilization=0.8` — **Trigger 2:** Scale out when load balancer utilization exceeds 80%. This trigger won't activate until the load balancer is created and connected (next lecture).

**Expected result:** Auto-scaling configured successfully. Status shows **"Active"** in the console.

**Verification:** Compute Engine → Instance Groups → `vprofile-mig` → Autoscaling section should show the configured parameters.

**Operational note on trigger 2:** The load balancing utilization trigger is configured proactively. It references a load balancer that doesn't exist yet. This is valid — the trigger simply has no data to act on until the LB is connected. Once the LB is created in the next lecture and connected to this MIG, the trigger becomes active.

> ⚠️ **Expert Note:** The two triggers operate independently — **either** one firing causes a scale-out. The MIG scales to satisfy the most demanding trigger. This means even if CPU is low but the LB is overwhelmed (many lightweight requests), scaling still happens. And vice versa.

***

## Post-Step Status Summary

After completing all three steps:

| Component                               | Status              | Location                            |
| --------------------------------------- | ------------------- | ----------------------------------- |
| Instance Template (`vprofile-template`) | Created             | Compute Engine → Instance Templates |
| MIG (`vprofile-mig`)                    | Active, 2 instances | Compute Engine → Instance Groups    |
| Auto Scaling                            | Active              | Configured on MIG                   |
| VM Instances                            | 2 running, Ready    | Compute Engine → VM Instances       |

**What remains:** The load balancer (front-end) to route internet traffic to the MIG. This is the final piece of the project architecture.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Three-Step Build Sequence

```
STEP 1: Instance Template (blueprint)
  gcloud compute instance-templates create vprofile-template
    --machine-type=e2-micro       ← runtime size (smaller than build)
    --image=vprofile-image         ← custom image from previous lecture
    --subnet=private               ← private subnet
    --no-address                   ← NO public IP (private subnet rule)
    --tags=app                     ← firewall rule association

STEP 2: Managed Instance Group (fleet)
  gcloud compute instance-groups managed create vprofile-mig
    --zone=us-central1-a
    --template=vprofile-template   ← uses Step 1
    --size=2                       ← immediately creates 2 VMs

STEP 3: Auto Scaling (dynamic capacity)
  gcloud compute instance-groups managed set-autoscaling vprofile-mig
    --max-num-replicas=<max>
    --min-num-replicas=<min>
    --target-cpu-utilization=0.6          ← scale at 60% CPU
    --target-load-balancing-utilization=0.8  ← scale at 80% LB util
```

***

## Component Relationship Chain

```
Custom Image (vprofile-image)
    ↓ referenced by
Instance Template (vprofile-template)
    ↓ used by
Managed Instance Group (vprofile-mig)
    ↓ creates & manages
2+ VM Instances (Tomcat + vProfile app)
    ↓ connect to
Cloud SQL + Memorystore (via private DNS)

NEXT: Load Balancer → routes internet traffic → MIG
```

***

## AWS ↔ GCP Mapping (This Lecture)

```
AWS Launch Template        =  GCP Instance Template
AWS Auto Scaling Group     =  GCP Managed Instance Group (MIG)
AWS ASG scaling policies   =  gcloud set-autoscaling command
AWS target tracking        =  --target-cpu-utilization / --target-load-balancing-utilization
```

***

## Auto Scaling Trigger Model

```
TRIGGER 1: CPU Utilization
  threshold: 0.6 (60%)
  scope: average across ALL instances in MIG
  scale out: CPU > 60%
  scale in:  CPU < 60%

TRIGGER 2: Load Balancing Utilization
  threshold: 0.8 (80%)
  scope: load balancer serving this MIG
  scale out: LB util > 80%
  scale in:  LB util < 80%
  NOTE: inactive until LB is created + connected (next lecture)

LOGIC: either trigger fires → scale out
       most demanding trigger determines instance count
```

***

## Instance Template Configuration Map

```
vprofile-template
  ├── machine-type: e2-micro      ← RUNTIME size (cost optimized)
  ├── image: vprofile-image        ← pre-configured app image
  ├── subnet: private              ← private subnet (security)
  ├── region: us-central1
  ├── no-address: true             ← NO public IP (mandatory for private subnet)
  └── tags: app                    ← applies firewall rules
```

***

## Machine Type Decision Pattern

```
BUILD PHASE (image creation):
  e2-medium / e2-small → more CPU/RAM for install, build, compile
  ONE-TIME cost → temporary instance → deleted after image capture

RUN PHASE (MIG production):
  e2-micro → sufficient for running Tomcat service
  ONGOING cost → multiplied by instance count × uptime

RULE: use larger for build, smaller for run
```

***

## Private Subnet Instance Discipline

```
Private subnet instance MUST have:
  --no-address                    ← no external/public IP
  
WHY:
  Public IP on private subnet instance = security violation
  Defeats purpose of private subnet architecture
  Instance becomes directly reachable from internet

RULE: "All the time, whenever you launch instances in the private subnet,
       always make sure there is --no-address"
```

***

## Verification Locations

```
Instance Template  →  Compute Engine → Instance Templates
MIG                →  Compute Engine → Instance Groups → shows instance count
VM Instances       →  Compute Engine → VM Instances → status: Ready
Auto Scaling       →  Instance Groups → select MIG → Autoscaling section → Active
```

***

## Project Status After This Lecture

```
✅ VPC (4 subnets, Cloud NAT, Cloud Router)
✅ Bastion Host (public subnet)
✅ Cloud SQL (MySQL 8) + Memorystore (Memcached)
✅ Private DNS Zones (name → IP)
✅ App VM → Custom Image (vprofile-image)
✅ Instance Template (vprofile-template)
✅ Managed Instance Group (vprofile-mig, 2 instances, auto-scaling)

⬜ Load Balancer (HTTPS, SSL cert, URL map, A record) ← NEXT LECTURE
   "We are in the end game now"
```

***

## Reusable Engineering Pattern: Template → Fleet → Policy

```
PATTERN:
  1. TEMPLATE    → define the instance blueprint (image, size, network, security)
  2. FLEET       → create a group of identical instances from the template
  3. POLICY      → add dynamic scaling rules to the fleet

WHY THIS ORDER:
  Template must exist before fleet (fleet needs blueprint)
  Fleet must exist before policy (policy needs something to scale)
  Separation of concerns: WHAT to create vs. HOW MANY vs. WHEN to change

WHERE ELSE:
  AWS:        Launch Template → Auto Scaling Group → Scaling Policies
  Kubernetes: Pod Template (in Deployment) → ReplicaSet → HPA
  Azure:      VM Scale Set image → Scale Set → Autoscale rules
  Docker:     Dockerfile → docker-compose replicas → scaling policies

UNIVERSAL STRUCTURE:
  Blueprint → Fleet Controller → Scaling Policy
  (static definition) → (instance management) → (dynamic behavior)
```

***

## One-Line Mental Reload Trigger

> *"Instance Template (e2-micro, custom image, private subnet, --no-address, app tag) → MIG creates 2 instances → set-autoscaling adds CPU 60% + LB 80% triggers — template is the blueprint, MIG is the fleet, auto-scaling is the policy — load balancer connects next."*

This single sentence reconstructs the three-step build sequence, every key template parameter, the initial MIG size, both scaling triggers with thresholds, the component relationship hierarchy, and the project's current position. [\[298-buildi...-group-mig \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/298-building-a-managed-instance-group-mig.txt)
