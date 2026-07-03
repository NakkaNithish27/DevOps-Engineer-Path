# 🎓 Deep Learning Material: AWS Elastic Load Balancer Hands-On Part 2 — Target Groups, ALB Creation, Health Checks, and Security Group Chaining

**Source:** Video lecture on ELB hands-on (from [122. ELB Hands On Part 2.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt?EntityRepresentationId=85ee24a9-5385-4337-a499-771b4b31894f) caption file) [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

**Video Context:** This is a dense, hands-on lecture where the instructor builds a complete load-balanced infrastructure from scratch: launches two EC2 instances from a launch template, creates a target group with health checks, creates an Application Load Balancer (ALB), hits a **real failure** caused by security group misconfiguration, diagnoses and fixes it live, verifies traffic routing, demonstrates maintenance operations, and performs cleanup. The deliberate failure-then-fix sequence is the most valuable part of the lecture — it teaches the **security group chaining pattern** that is critical in any production AWS architecture.

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — Target Group: The Intermediary Between Load Balancer and Instances

A **target group** is not just a collection of instances — it is a **group of instances combined with a health check mechanism**. The load balancer does not directly know about individual instances. Instead, the load balancer sends traffic to a target group, and the target group contains the registered instances that actually serve the traffic. [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

The instructor defines it precisely: *"Target group basically is just group of instances with health check. So you can register instance in the target group. You can also deregister from it. And load balancer is going to redirect the traffic to the target group which contains your instance."* [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

This introduces an architectural **indirection layer** between the load balancer and the compute instances. The load balancer doesn't need to know which specific instances exist — it only needs to know which target group to send traffic to. Instances can be added to or removed from the target group independently, without reconfiguring the load balancer itself. This decoupling is what enables zero-downtime maintenance: you deregister an instance, patch it, and register it back — the load balancer automatically adjusts. [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

Target groups can contain different target types: **instances**, **IP addresses**, **Lambda functions**, or even **another Application Load Balancer** (so one load balancer can route to another). The lecture focuses on instance-type targets. [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

***

## 1.2 — Health Checks: How the Load Balancer Knows Who Is Alive

The load balancer's most important operational behavior is that it **routes traffic only to healthy instances and avoids unhealthy ones**. But it cannot magically know whether an instance is healthy — it discovers this through **health checks**, which are periodic probes configured in the target group. [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

The instructor asks the right question: *"But the question is how does it know whether the instance is healthy or not? Well, that it knows through the health check."* [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

A health check is configured with several parameters, each of which has significant operational implications:

**Protocol and Port** — The health check accesses the instance using a specific protocol (HTTP or HTTPS) on a specific port. For a standard Apache/httpd web server, this is HTTP on port 80 (the default). If your service runs on a **non-default port** (like 8080, 8090, etc.), you must explicitly configure the health check to use that port by selecting "Override" instead of "Traffic port." The instructor emphasizes this: *"If you use non-default port like 8080, 90, anything else, any other service you're using, then make sure you update the port number."* [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

**Health Check Path** — By default, the health check hits the root path (`/`), which corresponds to the default web root directory (`/var/www/html`). But if your application serves content from a subdirectory (like `/images` or `/inner-peace`), you must configure the health check path to match. The instructor explains: *"if the website path is not just root directory, you can give slash and you can give the path."* The core principle is: **the health check path must point to a URL that your application actually serves successfully.** [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

**Healthy Threshold** — The number of consecutive successful health checks required before declaring an instance **healthy**. Default is 5. The instructor reduces it to 2 for faster feedback during the demo. Higher values mean more confidence but slower health detection. [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

**Unhealthy Threshold** — The number of consecutive failed health checks before declaring an instance **unhealthy**. Minimum is 2. The instructor strongly advises against using 1: *"One is definitely not recommended because sometimes due to high load and all the service does not respond and it goes unhealthy. And in the same moment, if the health check is done and the instance declares as unhealthy, that will be bad."* A single transient failure (network hiccup, momentary CPU spike) would cause a false unhealthy declaration, removing a perfectly good instance from rotation. [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

**Timeout** — How long to wait for a response before considering the health check failed. Default is 5 seconds. [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

**Interval** — The time between consecutive health checks. Default is 30 seconds. So with a healthy threshold of 2 and an interval of 30 seconds, it takes a minimum of 60 seconds (two checks, 30 seconds apart) for a newly registered instance to be declared healthy. [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

**Success Code** — The expected HTTP status code. Default is **200** (the standard HTTP success code). If your application returns a different success code, you must configure this accordingly. [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

> ⚠️ **Expert Note**
>
> The instructor delivers one of the most operationally valuable warnings in the lecture: *"I have seen many places where the services are live, healthy, running, but because of the misconfigured health check, the instances are unhealthy. So people waste time in fixing the service of the instance rather than focusing on the health check."* This is a real-world trap: when instances show as "unhealthy," the instinct is to SSH in and debug the application. But often the application is fine — the health check is simply pointing to the wrong port, wrong path, or wrong protocol. **Always verify the health check configuration before debugging the application.** [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

***

## 1.3 — Application Load Balancer (ALB): Architecture and Configuration

AWS offers multiple load balancer types: **Application Load Balancer (ALB)**, **Network Load Balancer (NLB)**, **Gateway Load Balancer (GLB)**, and the legacy **Classic Load Balancer**. The instructor notes that the Classic LB is simpler (no target group needed — just add instances directly) but offers fewer features. The ALB handles **HTTP and HTTPS traffic** and is the most commonly used type: *"Most of the cases you will have HTTP and HTTPS traffic and it's a pretty decent load balancer, very easy to configure."* [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

**Scheme: Internet-Facing vs. Internal** — An internet-facing ALB receives traffic from the public internet and routes it to your instances. An internal ALB is for service-to-service communication within your infrastructure: *"if you want it for some internal services that are used by some internal application, let's say you have a service running in an EC2 instance that wants to access some backend service. So for those backend services you can have an internal load balancer."* [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

**Availability Zones and Subnets** — The ALB must be deployed across one or more Availability Zones (AZs). Each AZ can have multiple subnets. In production, instances are typically distributed across multiple AZs for fault tolerance, and the load balancer routes to all of them. The instructor selects all available zones: *"you can have the load balancer that can route traffic to all these zones in a region."* The subnets shown are the **default subnets** in the AWS account's default VPC. [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

**Listeners** — A listener defines which port and protocol the load balancer listens on for incoming traffic, and which target group to forward it to. The default listener is HTTP on port 80. You can add additional listeners (e.g., HTTPS on port 443), each routing to potentially different target groups. The instructor mentions that HTTPS listeners require an **ACM (AWS Certificate Manager) certificate** for encryption — to be covered in a project lecture. [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

***

## 1.4 — Security Group Architecture: The Two-Layer Model and SG-to-SG Referencing

This is the **most important architectural concept** in the entire lecture, taught through a deliberate failure.

In a load-balanced setup, there are **two separate security groups** with distinct roles: [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

1. **Load Balancer Security Group** — Controls what traffic can reach the load balancer from the internet. For an internet-facing ALB serving HTTP, this needs port 80 open from anywhere (`0.0.0.0/0` for IPv4, `::/0` for IPv6). [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

2. **Instance Security Group** — Controls what traffic can reach the EC2 instances. This is where the critical design decision lies. [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

The instructor explicitly separates these: *"the load balancer should have its own separate security group. This is not the instance security group. This is the load balancer security group we are talking about."* [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

The failure scenario demonstrates why this matters. The instances had a security group that allowed port 80 **only from the instructor's personal IP address** (configured earlier for direct testing). The load balancer tried to route health check traffic to the instances on port 80, but the load balancer's traffic comes from the **load balancer's own IP** — which is NOT the instructor's personal IP. The instance security group blocked it. Result: health checks fail, instances are marked unhealthy, load balancer returns 503 errors. [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

The fix uses a powerful AWS feature: **security group referencing**. Instead of allowing port 80 from a specific IP address, you allow port 80 from **the load balancer's security group ID**. The rule says: *"any traffic coming from this security group on port 80 is allowed."* This means any resource (the load balancer) that has that security group attached is automatically allowed to send traffic to the instances. [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

> 🔍 **Deep Dive**
>
> Security group referencing is architecturally superior to IP-based rules for internal AWS communication. The load balancer's IP addresses can change (ALBs scale dynamically, adding and removing nodes). If you whitelist specific IPs, the rules break when the ALB scales. By referencing the security group, you create a **relationship-based rule** rather than an **address-based rule**. The rule remains valid regardless of how many ALB nodes exist or what IPs they use. This is the same pattern used throughout AWS: application tier SG references ALB SG, database tier SG references application tier SG — creating a **security group chain** that mirrors the traffic flow architecture. [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

***

## 1.5 — AWS WAF (Web Application Firewall) — Brief Mention

The instructor briefly mentions **AWS WAF** as an additional security layer that can be integrated with the ALB. WAF operates at the **application level** (Layer 7), unlike security groups which operate at the port/protocol level (Layer 3/4). WAF can prevent attacks like **DDoS, cross-site scripting (XSS)**, block traffic from specific locations or IP ranges, and apply many other application-level rules. It is a paid service. The instructor recommends exploring it when working with security teams but does not go deeper in this lecture. [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

***

## 1.6 — Register/Deregister: Zero-Downtime Maintenance Pattern

Once a target group is running, you can **deregister** an instance to remove it from the rotation (the load balancer stops sending traffic to it), perform maintenance (OS updates, package updates, configuration changes), and then **register** it back. During this time, the remaining instances continue serving traffic through the load balancer. This enables maintenance without user-facing disruption. [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building and Why

We are building a **complete load-balanced web infrastructure**: two EC2 instances behind an Application Load Balancer, with a target group managing health checks and traffic routing. The final outcome: a single DNS endpoint (the ALB's DNS name) that distributes incoming HTTP traffic across both instances, automatically avoiding any unhealthy instance. Along the way, we will hit a real security group misconfiguration, diagnose it, and fix it — which is the most operationally valuable part of the exercise.

***

## Step 1: Launch Two EC2 Instances from the Launch Template

**What we're doing:** Creating two identical web server instances using a previously created launch template.

1. Go to **EC2 → Launch Templates** → select the existing template [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)
2. **Actions → Launch instance from template**
3. Change the **Number of instances** to **2**
4. Scroll to **Tags** → set Name to `web000` (temporary; both instances get the same tag initially)
5. Click **Launch instance** [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

**Post-launch:** Go to Instances → rename the first instance to `web01` and the second to `web02` by clicking on the Name field. [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

**Connection to system flow:** These two instances are the backend servers that the load balancer will route traffic to. They must be running before we create the target group.

***

## Step 2: Create the Target Group

**What we're doing:** Creating a target group that groups our two instances and defines how the load balancer checks their health.

1. Go to **EC2 → Load Balancing → Target Groups** → **Create target group** [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

2. **Target type:** Instances [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

3. **Protocol:** HTTP — because our Apache web server serves HTTP traffic [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

4. **Port:** 80 — the default HTTP port, which is what Apache uses by default. If your service runs on a non-default port (8080, 8090, etc.), change this. [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

5. **Health check configuration:**

   | Setting             | Value                  | Why                                                            |
   | ------------------- | ---------------------- | -------------------------------------------------------------- |
   | Protocol            | HTTP                   | Matches the service protocol                                   |
   | Path                | `/`                    | Our site is served from the default web root (`/var/www/html`) |
   | Port                | Traffic port (80)      | Default; use "Override" only for non-default ports             |
   | Healthy threshold   | **2** (reduced from 5) | Faster healthy detection for demo; production may use higher   |
   | Unhealthy threshold | 2 (minimum)            | Two consecutive failures before declaring unhealthy            |
   | Timeout             | 5 seconds              | Wait time per check                                            |
   | Interval            | 30 seconds             | Time between checks                                            |
   | Success code        | 200                    | Standard HTTP success                                          |

    [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

6. **Target group name:** `inner-peace-TG` → click **Next** [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

7. **Register targets:** Select both `web01` and `web02` → click **"Include as pending below"** [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

   **Critical step:** You MUST click "Include as pending below" to actually register the instances. Simply selecting them is not enough — they must appear in the **Review targets** section at the bottom. The instructor emphasizes: *"once again you need to have these instances over here in the review target section. So you need to click on Include Pending below and make sure they're here."* [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

8. Verify the port shows **80** for both instances → click **Create target group** [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

**Connection to system flow:** The target group now exists with two registered instances. It will start running health checks, but without a load balancer attached, it's not receiving any external traffic yet.

***

## Step 3: Create the Application Load Balancer

**What we're doing:** Creating the ALB that will be the public-facing entry point, receiving internet traffic and routing it to the target group.

1. Go to **EC2 → Load Balancers** → **Create load balancer** [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

2. Select **Application Load Balancer** → click **Create** [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

3. **Name:** `inner-peace-ALB` [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

4. **Scheme:** Internet-facing (serves public internet traffic) [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

5. **Availability Zones:** Select **all available zones** — the instructor selects all default subnets across all AZs in us-east-1. This allows the ALB to route to instances in any zone. [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

6. **Security Group — Create a NEW one for the load balancer:**

   Click **"Create new security group"** link → opens a new tab: [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

   * **Name:** `inner-peace-elb-SG`
   * **Inbound rules:**
     * HTTP (port 80) from **Anywhere IPv4** (`0.0.0.0/0`)
     * HTTP (port 80) from **Anywhere IPv6** (`::/0`)
   * **Important:** Make sure you're editing **inbound rules**, not outbound rules [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)
   * Click **Create security group**

   Go back to the ALB creation page → **Refresh** the security group dropdown → select `inner-peace-elb-SG` → **uncheck the default security group**. [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

7. **Listener and Routing:**
   * Default listener: **HTTP : 80**
   * Forward to: select **inner-peace-TG** (the target group we just created) [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

8. Scroll down → click **Create Load Balancer** [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

**Expected state:** Load balancer shows **"Provisioning"**. Wait a few minutes until it changes to **"Active"**. [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

**Connection to system flow:** The ALB is now created and will start sending health check traffic to the target group instances. But — as we'll discover next — this traffic will be blocked.

***

## Step 4: Test and Encounter the Failure (503 Error)

**What we're doing:** Accessing the ALB's DNS endpoint to verify traffic routing.

1. Click on the load balancer → copy the **DNS name** [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)
2. Open it in a browser: `http://<ALB-DNS-name>`
3. **Expected result:** **503 Service Unavailable** (or blank page) [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

**Why it fails:** The instructor guides through the diagnosis:

1. **Check the target group:** Go to Target Groups → click on `inner-peace-TG` → Targets tab → both instances show **"unhealthy"** [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

2. **Verify the instances are actually working:** Copy one instance's public IP → `http://<public-IP>` in browser → **works fine**. The application is healthy. [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

3. **Identify what's between the health check and the instance:** The load balancer sends health check traffic to the instances on port 80. Something is blocking that traffic. [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

4. **Check the INSTANCE security group** (not the ALB security group): Go to the instance → Security tab → click the security group → Edit inbound rules → Port 80 is allowed **only from "My IP"** (the instructor's personal IP). The load balancer's health check traffic comes from the **ALB's network interface**, not from the instructor's IP. It's blocked. [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

The instructor walks through the reasoning: *"I am able to access the instance, but the load balancer is not."* This is because your browser sends traffic from your personal IP (which is whitelisted), but the ALB sends from its own IP (which is not). [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

**Key diagnostic principle:** For 503 errors from a load balancer, always check the **target group health status first**. If targets are unhealthy, the problem is between the ALB and the instances — usually the instance security group. [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

***

## Step 5: Fix the Security Group — SG-to-SG Referencing

**What we're doing:** Modifying the instance security group to allow traffic from the ALB's security group instead of a specific IP.

1. Go to the instance's security group → **Edit inbound rules** [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)
2. **Delete** the old port 80 rule (which allowed only "My IP")
3. **Add a new rule:**
   * Type: **HTTP** (auto-fills port 80)
   * Source: type `sg` in the search box → select **`inner-peace-elb-SG`** (the ALB's security group) [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)
   * Description: `allow from load balancer`
4. **Save rules** [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

**What this rule means:** Any traffic originating from a resource that has the `inner-peace-elb-SG` security group attached (i.e., the ALB) is allowed to reach the instances on port 80. This is a **relationship-based rule**, not an IP-based rule. [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

**Wait for health checks to pass:** The target group will re-evaluate instance health. With a healthy threshold of 2 and an interval of 30 seconds, it takes approximately **under 2 minutes** for instances to become healthy. The instructor confirms: *"In less than two minutes the instances are healthy."* [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

**Verify:** Refresh the target group → both instances now show **"healthy"**. [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

***

## Step 6: Verify Load Balancer Traffic Routing

**What we're doing:** Confirming the ALB now successfully routes traffic to the instances.

1. Go to the ALB → copy the **DNS name** [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)
2. Open in browser: `http://<ALB-DNS-name>`
3. **Expected result:** The website loads successfully. [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

**What's happening:** Internet traffic hits the ALB DNS → ALB checks which instances in the target group are healthy → routes the request to a healthy instance → instance responds → user sees the website.

***

## Step 7: Maintenance Operations — Register/Deregister

**What we're doing:** Understanding how to perform maintenance without disrupting users.

**To take an instance out of rotation:** [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

1. Go to Target Group → Targets tab
2. Select the instance → click **Deregister**
3. The ALB stops sending traffic to that instance
4. Perform maintenance (OS updates, package updates, config changes)
5. Click **Register targets** → select the instance → **Include as pending below** → register it back

**Other ALB modifications available:** Add/remove listeners, add/remove target groups, change security groups, change various attributes. The instructor encourages exploring these settings. [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

***

## Step 8: Cleanup — Proper Deletion Order

**What we're doing:** Removing all resources to avoid charges, in the correct dependency order.

**Deletion sequence:** [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

1. **Terminate EC2 instances:** Select instances → Instance State → Terminate. (The launch template is kept — it has no running cost and can be reused.) [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

2. **Delete the Load Balancer:** Select ALB → Actions → Delete → Confirm. (Must delete before target group, as the TG may show "in use" otherwise.) [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

3. **Delete the Target Group:** Select TG → Actions → Delete. (No charges for target groups, but clean up anyway.) [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

4. **Verify the dashboard:**
   * 0 running instances (2 in terminated state — temporary)
   * 0 load balancers
   * 0 elastic IPs
   * 0 volumes
   * 1 snapshot (tied to the AMI — cannot delete independently)
   * 1 AMI (keep for future lectures) [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

**Important:** The snapshot tied to the AMI cannot be deleted while the AMI exists. The instructor will show how to deregister the AMI and delete the snapshot later. [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

> ⚠️ **Expert Note**
>
> In production, the cleanup order matters for dependency reasons: you cannot delete a target group while a load balancer still references it (it shows "in use"), and you cannot delete a security group while it's attached to a running resource. Always work **top-down**: load balancer → target group → instances → security groups. Also, forgotten ALBs incur hourly charges even with no traffic — always verify cleanup via the EC2 dashboard. [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🔷 Complete Architecture (What We Built)

```
INTERNET
  │
  ▼
[ALB: inner-peace-ALB]
  │  DNS name = public endpoint
  │  SG: inner-peace-elb-SG (port 80 from anywhere)
  │  Listener: HTTP:80 → forwards to target group
  │
  ▼
[Target Group: inner-peace-TG]
  │  Health check: HTTP:80 on path /
  │  Healthy threshold: 2  |  Unhealthy threshold: 2
  │  Interval: 30s  |  Timeout: 5s  |  Success: 200
  │
  ├──► [web01]  SG: port 80 from inner-peace-elb-SG
  └──► [web02]  SG: port 80 from inner-peace-elb-SG
```

***

## 🔷 Traffic Flow

```
User browser → ALB DNS (port 80)
  → ALB checks target group for healthy instances
    → Routes to healthy instance (port 80)
      → Instance responds
        → ALB returns response to user
```

***

## 🔷 Health Check Flow

```
Target Group sends probe every 30s:
  HTTP GET → instance:80/  → expects 200

  ┌─ 200 returned? ──YES──► healthy_count++
  │                          healthy_count >= 2? → HEALTHY ✅
  │
  └─ No response / non-200 ──► unhealthy_count++
                                unhealthy_count >= 2? → UNHEALTHY ❌
                                
ALB routes traffic ONLY to HEALTHY instances
```

***

## 🔷 The Security Group Chain (Most Critical Pattern)

```
INTERNET ──► ALB SG (port 80 from 0.0.0.0/0)
                │
                ▼
             INSTANCE SG (port 80 from ALB SG)
             
Rule type: SG-to-SG reference (not IP-based)

WHY: ALB IPs change dynamically → IP rules break
     SG reference = relationship-based → always valid
```

***

## 🔷 The Failure → Diagnosis → Fix Chain

```
SYMPTOM: 503 from ALB endpoint
  │
  ▼
CHECK: Target Group → Targets → instances UNHEALTHY
  │
  ▼
VERIFY: Instance public IP works directly → app is fine
  │
  ▼
DIAGNOSE: What's between ALB health check and instance?
          → Instance Security Group!
          → Port 80 allowed only from "My IP"
          → ALB traffic comes from ALB's IP, not yours
  │
  ▼
FIX: Instance SG → delete IP rule → add SG reference rule
     Source = ALB security group ID
  │
  ▼
WAIT: ~2 health checks × 30s interval = ~60s
  │
  ▼
RESULT: Instances → HEALTHY → ALB routes traffic → site loads ✅
```

***

## 🔷 Health Check Configuration Map

```
PARAMETER          DEFAULT    MEANING
─────────────────  ─────────  ──────────────────────────────
Protocol           HTTP       How to probe
Port               80         Which port to check
Path               /          Which URL path
Healthy threshold  5 (→ 2)    Consecutive successes to declare healthy
Unhealthy thresh.  2          Consecutive failures to declare unhealthy
Timeout            5s         Max wait per probe
Interval           30s        Time between probes
Success code       200        Expected HTTP response code

MISCONFIGURATION TRAP:
  Service running fine + wrong health check config = instances marked UNHEALTHY
  → Fix the health check FIRST, not the application
```

***

## 🔷 Load Balancer Types (Quick Reference)

```
ALB (Application)  → HTTP/HTTPS (Layer 7) → most common, used here
NLB (Network)      → TCP/UDP (Layer 4) → ultra-low latency
GLB (Gateway)      → Network appliances → transparent routing
Classic            → Legacy, simple (no target group needed), fewer features
```

***

## 🔷 ALB Configuration Components

```
ALB
  ├── Name
  ├── Scheme: internet-facing | internal
  ├── AZs + Subnets (select zones for multi-AZ routing)
  ├── Security Group (ALB's own SG, NOT instance SG)
  ├── Listener(s)
  │     ├── HTTP:80  → Target Group A
  │     └── HTTPS:443 → Target Group B (+ ACM certificate)
  └── Optional integrations: CloudFront, WAF
```

***

## 🔷 Maintenance Pattern (Zero-Downtime)

```
Instance needs patching?
  │
  ├── Deregister from target group
  │     → ALB stops sending traffic
  │
  ├── Perform maintenance (OS update, package update, config)
  │
  └── Register back into target group
        → Health checks pass → ALB resumes sending traffic
        
No user disruption (other instances serve during maintenance)
```

***

## 🔷 Cleanup Order (Dependency-Aware)

```
1. Terminate instances (launch template preserved for reuse)
2. Delete Load Balancer (must go before TG)
3. Delete Target Group (may show "in use" if ALB still exists)
4. Verify dashboard: 0 running, 0 LB, 0 EIP, 0 volumes
5. Keep: AMI + snapshot (tied together, needed for future lectures)
   └── To fully delete later: deregister AMI → then delete snapshot
```

***

## 🔷 Reusable Engineering Pattern: Layered Security with Reference-Based Rules

```
PATTERN: Security Group Chaining

TIER 1 (Public)     → allows traffic from INTERNET
  │  SG rule: port X from 0.0.0.0/0
  │
  ▼
TIER 2 (Middle)     → allows traffic ONLY from Tier 1's SG
  │  SG rule: port X from SG-tier1
  │
  ▼
TIER 3 (Backend)    → allows traffic ONLY from Tier 2's SG
     SG rule: port Y from SG-tier2

Each tier trusts the tier above it by IDENTITY (SG), not by ADDRESS (IP).
IPs change; SG identity is stable.

This pattern applies to:
  Internet → ALB → App servers → Database  (this lecture)
  Internet → API Gateway → Lambda → DynamoDB
  Internet → CDN → Origin servers
```

**This is the single most transferable security architecture pattern from this lecture.** [\[122. ELB H...On Part 2 \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/122.%20ELB%20Hands%20On%20Part%202.txt)

***

## 🔷 Core Diagnostic Mental Model

```
503 from load balancer?
  → Always check TARGET GROUP HEALTH first
    → Instances unhealthy?
      → Verify app works via direct IP
        → App works? → Problem is BETWEEN ALB and instance
          → Check INSTANCE security group
          → Check health check config (port, path, protocol)
        → App broken? → Fix the application/service
```
