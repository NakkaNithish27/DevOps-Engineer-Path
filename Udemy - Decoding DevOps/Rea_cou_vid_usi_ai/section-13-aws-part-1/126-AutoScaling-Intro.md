# 🎓 Deep Learning Material: AWS Auto Scaling Groups — Introduction

*Reconstructed from video captions — [126. Autoscaling Group Introduction.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/126.%20Autoscaling%20Group%20Introduction.txt?EntityRepresentationId=1a37ee19-1dd0-4c7a-bb77-c0c20629bb86)* [\[126. Autos...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/126.%20Autoscaling%20Group%20Introduction.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

## 1.1 What Auto Scaling Groups Are and Why They Exist

An Auto Scaling Group (ASG) is an AWS service that **automatically adjusts the number of EC2 instances** running in a group based on real-time demand. Instead of you manually watching traffic, deciding when to add servers, launching them, and then remembering to shut them down when traffic drops — the ASG does all of this autonomously. [\[126. Autos...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/126.%20Autoscaling%20Group%20Introduction.txt)

This solves two problems simultaneously:

**Performance:** When load increases (e.g., more users, higher CPU usage), the ASG launches additional instances to absorb the demand. The application doesn't slow down or crash because capacity grows to meet the load.

**Cost:** When load decreases, the ASG terminates excess instances so you're not paying for idle servers. Capacity shrinks to match actual need.

These two goals — maintain performance and control cost — are in natural tension. Auto Scaling Groups resolve this tension by making capacity **dynamic** instead of static. You don't choose a fixed number of servers and hope it's right; you define rules and boundaries, and the system adjusts within those boundaries automatically.

The video emphasizes that ASG is easy to understand **if you already know EC2 and CloudWatch**, because ASG doesn't exist in isolation — it is an **integration layer** that connects and orchestrates services you already understand: EC2 for compute, CloudWatch for monitoring, Launch Templates for instance configuration, and Scaling Policies for decision logic. [\[126. Autos...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/126.%20Autoscaling%20Group%20Introduction.txt)

***

## 1.2 The Component Architecture — How ASG Integrates with Other Services

An Auto Scaling Group is not a standalone system. It is a **coordinator** that ties together four distinct AWS components, each with a specific role: [\[126. Autos...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/126.%20Autoscaling%20Group%20Introduction.txt)

### 1.2.1 Launch Configuration / Launch Template — "How to Create Instances"

The ASG needs to know **what kind of instance to launch** when it decides to add capacity. It gets this information from a **Launch Configuration** or a **Launch Template** — the same launch template used in the ELB (Elastic Load Balancer) exercise from previous sessions. The launch template defines the AMI, instance type, key pair, security group, user data, and all other instance parameters. The ASG doesn't make these decisions — it simply reads the template and launches instances exactly as specified. [\[126. Autos...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/126.%20Autoscaling%20Group%20Introduction.txt)

This is a **separation of concerns**: the launch template knows *what* to create; the ASG knows *when* and *how many* to create. Changing the instance configuration (e.g., upgrading the AMI) means updating the launch template, not the ASG itself.

### 1.2.2 CloudWatch Alarms — "When to Act"

The ASG monitors resources through **CloudWatch**, AWS's monitoring service. You select a **metric** to watch — the video uses **CPU utilization** as the primary example. CloudWatch continuously measures this metric across the instances in the ASG. When the metric crosses a defined **threshold** (e.g., CPU goes above 60%), CloudWatch triggers an **alarm**. This alarm is the signal that tells the ASG "something changed — take action." [\[126. Autos...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/126.%20Autoscaling%20Group%20Introduction.txt)

Alarms work in both directions: one alarm for scaling **out** (load is too high, add capacity) and another for scaling **in** (load is low, remove capacity). You must create alarms for both — the ASG doesn't know when to act without them. [\[126. Autos...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/126.%20Autoscaling%20Group%20Introduction.txt)

### 1.2.3 Scaling Policies — "How Much to Adjust"

When a CloudWatch alarm fires, the ASG consults its **scaling policies** to determine the specific action. Scaling policies define the **magnitude** of the response: how many instances to add or remove. [\[126. Autos...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/126.%20Autoscaling%20Group%20Introduction.txt)

The video describes two approaches: [\[126. Autos...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/126.%20Autoscaling%20Group%20Introduction.txt)

**Step scaling (manual policy definition):** You define explicit rules tied to metric thresholds. For example:

* CPU > 60% → launch 2 additional instances
* CPU > 80% → launch 4 additional instances
* CPU drops → remove 2, 3, or 4 instances as per your rules

This gives you granular control — different levels of response for different severity levels.

**Auto-managed scaling:** You let the ASG "handle all that for you" — AWS determines the optimal scaling actions based on the target metric. You specify the target (e.g., keep CPU at 50%), and the ASG figures out how many instances to add or remove to maintain that target.

### 1.2.4 The ASG Itself — Capacity Boundaries

The ASG defines three capacity parameters that create a **bounded operating range**: [\[126. Autos...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/126.%20Autoscaling%20Group%20Introduction.txt)

**Minimum size:** The absolute floor — the ASG will **never** terminate instances below this number. If minimum is 1, at least one instance will always be running regardless of how low the load drops. This protects against the ASG removing all instances and leaving you with zero capacity. [\[126. Autos...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/126.%20Autoscaling%20Group%20Introduction.txt)

**Desired capacity:** The number of instances the ASG **normally maintains**. When the ASG is created, it launches instances to match the desired capacity. This is the "steady state" — the number of instances running when no alarms are triggered and no scaling actions are in progress. If desired capacity is 2, the ASG creates 2 instances at startup. [\[126. Autos...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/126.%20Autoscaling%20Group%20Introduction.txt)

**Maximum size:** The absolute ceiling — the ASG will **never** launch instances beyond this number, no matter how high the load goes. If maximum is 4, the ASG will not create a 5th instance even if CPU is at 100%. This is the cost-control boundary — it prevents runaway scaling from generating unlimited charges. [\[126. Autos...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/126.%20Autoscaling%20Group%20Introduction.txt)

The relationship: **minimum ≤ desired ≤ maximum**. The desired capacity floats between minimum and maximum based on scaling policy actions. Scaling out increases desired toward maximum; scaling in decreases desired toward minimum.

> 🔍 **Deep Dive:** The minimum size is a **safety net**, not just a lower bound. Consider what happens without it: if traffic drops to zero and the scaling policy removes all instances, there are zero servers running. When traffic returns, there's nothing to receive it — and nothing to generate the CloudWatch metric that would trigger scaling out. The minimum ensures at least one instance is always alive to detect returning demand and serve as the seed for scale-out. This is a **liveness guarantee** built into the ASG design.

***

## 1.3 The Complete Operational Cycle

Putting all components together, the ASG operates as a continuous feedback loop: [\[126. Autos...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/126.%20Autoscaling%20Group%20Introduction.txt)

1. **ASG launches instances** using the launch template to reach the desired capacity
2. **CloudWatch monitors** the selected metric (e.g., CPU utilization) across these instances
3. **Metric crosses threshold** → CloudWatch alarm triggers
4. **Alarm activates scaling policy** → policy specifies how many instances to add or remove
5. **ASG executes the scaling action** — launches new instances (from launch template) or terminates existing ones
6. **Capacity adjusts** — desired capacity changes within the min/max boundaries
7. **CloudWatch continues monitoring** the new state → cycle repeats

This is a **closed-loop control system**: monitor → detect → decide → act → monitor again. The ASG is the controller, CloudWatch is the sensor, the scaling policy is the decision logic, and the launch template is the execution blueprint.

> ⚠️ **Expert Note:** The video frames step scaling with specific examples (CPU > 60% → 2 instances, > 80% → 4 instances). This graduated response is important: not all load spikes are equal. A gentle increase needs a gentle response; a sudden spike needs an aggressive response. Step scaling gives you this proportionality. Without it, you either over-scale (wasteful) or under-scale (still degraded) for every event.

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

## What We Are Building

This lecture is the **conceptual introduction** — the hands-on setup begins in the next lecture. However, the video establishes the complete architecture and decision framework that directly feeds into the practical work.

***

## Decision Framework 1: Capacity Sizing

When creating an ASG, you must specify three values. Here's how to think about each: [\[126. Autos...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/126.%20Autoscaling%20Group%20Introduction.txt)

**Minimum size** — Ask: "What is the absolute least number of instances I need to keep the application alive?" This is your safety floor. Typical starting point: 1 (for non-critical workloads) or 2 (for high-availability requirements).

**Desired capacity** — Ask: "Under normal, average-day load, how many instances do I need?" This is what the ASG launches at startup and maintains during steady state. The video example: desired = 2.

**Maximum size** — Ask: "What is the maximum I'm willing to pay for, even under peak load?" This is your cost ceiling. The video example: maximum = 4.

**Example configuration from the video:**

```
Minimum:  1 instance  (never go below this)
Desired:  2 instances (normal operating state)
Maximum:  4 instances (never exceed this, even under peak)
```

***

## Decision Framework 2: Choosing the Scaling Metric

The metric you select determines **what the ASG reacts to**. The video uses CPU utilization as the example. The decision: [\[126. Autos...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/126.%20Autoscaling%20Group%20Introduction.txt)

* **CPU utilization** — the most common metric. Suitable when your application's performance correlates directly with CPU load.

The threshold values (e.g., 60%, 80%) determine when scaling actions trigger. Lower thresholds = more aggressive scaling (scales sooner, maintains better performance, costs more). Higher thresholds = more conservative scaling (scales later, saves money, risks brief performance dips).

***

## Decision Framework 3: Scaling Policy Style

**Step scaling (you define the rules):** [\[126. Autos...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/126.%20Autoscaling%20Group%20Introduction.txt)

```
CPU > 60%  → Add 2 instances
CPU > 80%  → Add 4 instances
CPU < 40%  → Remove 2 instances
CPU < 20%  → Remove 4 instances
```

Use this when you need **precise control** over the scaling response at different load levels.

**Auto-managed scaling (AWS handles it):**

You specify a target metric value (e.g., "keep average CPU at 50%"), and AWS figures out the optimal number of instances. Use this when you want simplicity and trust the algorithm.

***

## Decision Framework 4: What to Prepare Before Creating an ASG

Based on the video's component architecture, you need these pre-existing resources: [\[126. Autos...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/126.%20Autoscaling%20Group%20Introduction.txt)

1. **Launch Template** (or Launch Configuration) — already created in the ELB exercise. Defines AMI, instance type, key pair, security group, user data.
2. **CloudWatch Alarms** — will be created as part of the ASG setup. Define the metric, thresholds, and alarm actions.
3. **Scaling Policies** — defined within the ASG configuration. Link to CloudWatch alarms.

The launch template is **reused** from the ELB section — the same template that launches web servers behind the load balancer can now power the ASG. This demonstrates how AWS components compose together: one launch template serves both the ELB target group and the ASG.

> ⚠️ **Expert Note:** The video mentions both "launch configuration" and "launch template." Launch configurations are the older mechanism; launch templates are the newer, recommended replacement with more features (versioning, multiple instance types). In practice, always prefer launch templates. AWS still supports launch configurations but they are essentially legacy. [\[126. Autos...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/126.%20Autoscaling%20Group%20Introduction.txt)

***

## Architecture Preview for the Lab

```
CloudWatch (monitors CPU utilization)
     │
     ├── Alarm: CPU > threshold → triggers scale-out policy
     └── Alarm: CPU < threshold → triggers scale-in policy
            │
            ▼
Auto Scaling Group
     ├── Min: 1 | Desired: 2 | Max: 4
     ├── Launch Template → defines instance config
     │
     ├── [Instance 1]  ← always running (min=1)
     ├── [Instance 2]  ← normal state (desired=2)
     ├── [Instance 3]  ← added during scale-out
     └── [Instance 4]  ← added during peak (max=4)
```

**Connection to previous lectures:** The instances launched by the ASG are the same web server instances from the ELB exercise. The ASG sits behind the load balancer — the ALB distributes traffic across whatever instances the ASG currently has running. When the ASG scales out, new instances register with the ALB's target group. When it scales in, terminated instances are deregistered. The ALB and ASG work as a **unified scaling system**.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

## 🏗️ ASG = Integration Layer (Not Standalone)

```
AUTO SCALING GROUP
  │
  ├── USES: Launch Template      → HOW to create instances
  ├── USES: CloudWatch Alarms    → WHEN to act
  ├── USES: Scaling Policies     → HOW MUCH to adjust
  └── DEFINES: Capacity Bounds   → WITHIN WHAT LIMITS
```

## 🔄 Closed-Loop Control Cycle

```
Launch Template → ASG creates instances (desired capacity)
                       │
                CloudWatch monitors metric (CPU)
                       │
                Metric crosses threshold
                       │
                Alarm triggers
                       │
                Scaling Policy executes
                       │
              ┌────────┴────────┐
              │                 │
         SCALE OUT          SCALE IN
    (add instances)     (remove instances)
              │                 │
              └────────┬────────┘
                       │
                CloudWatch continues monitoring
                       │
                   (cycle repeats)
```

## 📐 Capacity Boundaries

```
MINIMUM ──────── DESIRED ──────── MAXIMUM
   1                2                 4

   │                │                 │
   └── Safety       └── Steady       └── Cost
       floor            state            ceiling

MINIMUM: Never terminate below this (liveness guarantee)
DESIRED: Normal running count (startup target)
MAXIMUM: Never launch above this (cost protection)

Relationship: min ≤ desired ≤ max
Scaling moves DESIRED between MIN and MAX
```

## 🎛️ Scaling Policy Types

```
STEP SCALING (you define):
  CPU > 60%  → +2 instances
  CPU > 80%  → +4 instances
  CPU < 40%  → -2 instances
  = Graduated response, precise control

AUTO-MANAGED (AWS defines):
  Target: "Keep CPU at 50%"
  AWS calculates instance count
  = Simpler, less control
```

## 🔗 Component Dependency Chain

```
Launch Template ← defines → Instance configuration (AMI, type, SG, key)
       │
       ▼
ASG ← uses template to → Launch/Terminate instances
       │
       ▼
CloudWatch ← monitors → Instance metrics (CPU, etc.)
       │
       ▼
Alarm ← triggers when → Metric crosses threshold
       │
       ▼
Scaling Policy ← determines → How many instances to add/remove
       │
       ▼
ASG ← executes → Launch or terminate (within min/max bounds)
```

## 🌐 ASG + ELB Integration (from previous lectures)

```
[Users] → [ALB] → distributes traffic → [ASG Instances]

ASG scales out → new instance registers with ALB target group
ASG scales in  → terminated instance deregistered from ALB

ALB handles ROUTING
ASG handles CAPACITY
Together = elastic, self-healing web tier
```

## 📋 CloudWatch Alarms — Dual Direction

```
SCALE OUT ALARM:
  Metric: CPU > 60% for X minutes → add instances
  Purpose: Maintain PERFORMANCE

SCALE IN ALARM:
  Metric: CPU < 20% for X minutes → remove instances
  Purpose: Maintain COST EFFICIENCY

Both required. Without scale-out = degraded performance.
Without scale-in = wasted money.
```

## 🧩 Pre-Requisites for ASG Creation

```
BEFORE creating ASG, you need:
  ✅ Launch Template (from ELB exercise — reusable)
  ✅ Know: min, desired, max values
  ✅ Know: which metric to monitor (CPU typical)
  ✅ Know: threshold values for alarms
  ✅ Know: scaling policy type (step or auto)

DURING ASG creation:
  → CloudWatch alarms created
  → Scaling policies defined
  → Capacity bounds set
  → Launch template selected
```

## 🔁 Reusable Engineering Patterns

| Pattern                    | Manifestation                                                                                      |
| -------------------------- | -------------------------------------------------------------------------------------------------- |
| **Closed-loop control**    | Monitor → Detect → Decide → Act → Monitor again. Universal automation feedback loop.               |
| **Bounded autonomy**       | ASG acts autonomously BUT within min/max bounds. Freedom with guardrails.                          |
| **Separation of concerns** | Template = what to create. ASG = when/how many. CloudWatch = when to signal. Policy = how much.    |
| **Component reuse**        | Same launch template powers both ELB targets and ASG instances. One blueprint, multiple consumers. |
| **Dual-goal optimization** | Scale out for performance + scale in for cost. Two opposing pressures balanced by one system.      |
| **Graduated response**     | Step scaling: small problem → small reaction. Big problem → big reaction. Proportional action.     |
| **Safety floor**           | Minimum size prevents scaling to zero — liveness guarantee. Always at least one instance alive.    |

## ⚡ Key Gotchas for Fast Recall

```
❌ No minimum set (or min=0)         → ASG can scale to ZERO instances, total outage
✅ Minimum ≥ 1                       → At least one instance always alive

❌ No scale-in alarm                 → Instances never removed, cost grows indefinitely
✅ Both scale-out AND scale-in alarms → Performance AND cost managed

❌ Create new launch template for ASG → Unnecessary duplication
✅ Reuse existing launch template     → Same template works for ELB + ASG

❌ One threshold for all load levels  → Over-reacts or under-reacts
✅ Step scaling with multiple thresholds → Proportional response

❌ Maximum too high without awareness → Runaway scaling = massive bill
✅ Maximum = explicit cost ceiling    → Caps maximum spend
```

***

This completes the full reconstruction of the AWS Auto Scaling Groups Introduction video. Want me to generate Anki flashcards (CSV) from this material, or process another caption file? [\[126. Autos...troduction \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/126.%20Autoscaling%20Group%20Introduction.txt)
