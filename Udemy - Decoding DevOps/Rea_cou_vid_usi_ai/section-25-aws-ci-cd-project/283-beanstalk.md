# 🌱 AWS Elastic Beanstalk — Vprofile Environment Setup — Deep Learning Material

**Source:** Video caption file — [283-beanstalk.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt?EntityRepresentationId=91a852a1-3f66-40be-bfec-d9a6a510c862) [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

**Video Context:** The instructor sets up an AWS Elastic Beanstalk environment to run the Vprofile Java application on Tomcat. This is not a from-scratch introduction to Beanstalk — it builds on a previous re-architecting project where the service role and instance profile were already created. The focus is on every configuration decision made during environment creation: key pair, platform, custom configuration, VPC/subnets, volume type (with a critical GP3 workaround), auto scaling, load balancer, session stickiness, and rolling update deployment policy. RDS creation is deferred to the next lecture.

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 What Elastic Beanstalk Is — The Orchestration Layer

Elastic Beanstalk is not a new infrastructure component — it is an **orchestration service** that creates and manages other AWS services on your behalf. When you create a Beanstalk environment, it provisions EC2 instances, an Auto Scaling Group, an Application Load Balancer, a Target Group, Security Groups, and CloudWatch monitoring — all the components that in previous lectures were created manually, one by one. [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

The core value proposition: instead of individually creating and wiring together an ALB, target group, ASG, launch template, security groups, and instances (as done in earlier lectures), you describe what you want through Beanstalk's configuration wizard, and Beanstalk creates, connects, and manages everything as a single unit called an **environment**. You deploy your application artifact (a WAR file for Tomcat), and Beanstalk handles the infrastructure.

The instructor's configuration choices throughout this lecture map directly to the individual services covered earlier: the Auto Scaling settings correspond to the ASG hands-on lecture, the load balancer settings correspond to the ELB lecture, the instance type and key pair correspond to EC2 basics. Beanstalk is the convergence point where all those individual concepts come together under a single management layer.

***

## 1.2 Application vs. Environment — The Two-Level Structure

Beanstalk organizes resources in a two-level hierarchy: [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

**Application** — the top-level container. The instructor names it `Vprofile`. An application represents your software project. It holds one or more environments.

**Environment** — a specific deployment of the application. The instructor names it `Vprofile-prod-11`. An environment represents a running version of your application with all its infrastructure. You can have multiple environments (e.g., `Vprofile-dev`, `Vprofile-staging`, `Vprofile-prod`) under the same application, each with different configurations, instance sizes, or scaling policies.

The **environment domain name** becomes the URL for accessing the application. The instructor gives it the same name as the environment and checks availability because "this will be the URL, and we have to make sure it's unique." This domain becomes a CNAME under `elasticbeanstalk.com`. Since it's globally unique, "you cannot use the same name that I have given" — each student must choose a different name or add different numbers. [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

***

## 1.3 Web Server Environment Type

The instructor selects **Web server environment**. This is one of two Beanstalk environment types. A web server environment is designed for applications that serve HTTP requests — it provisions a load balancer, auto scaling group, and EC2 instances that handle incoming web traffic. The other type (worker environment, not selected here) is designed for background processing tasks that consume messages from a queue. [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

The choice is driven by the application's nature: Vprofile is a web application accessed through a browser, so it needs a web server environment.

***

## 1.4 Platform Selection — Tomcat on Amazon Linux 2023

The **platform** tells Beanstalk what runtime environment your application needs. The instructor selects **Tomcat** because "our Vprofile application runs on Tomcat." The specific version is **Tomcat 10 with Corretto 21** (Corretto is Amazon's distribution of the JDK), running on **Amazon Linux 2023**. [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

This is a critical alignment: your platform must match your application's requirements. A Java web application built for Tomcat must run on a Tomcat platform. The platform selection determines what software is pre-installed on the EC2 instances that Beanstalk launches — in this case, Java 21 (Corretto) and Tomcat 10 on Amazon Linux 2023.

***

## 1.5 Custom Configuration — Why Not Default

The instructor explicitly selects **Custom configuration** instead of the default. The reason: "We'll have load balanced instance, multiple instances with the load balancer." [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

The default Beanstalk configuration creates a **single instance** environment — one EC2 instance with no load balancer and no auto scaling. This is suitable for development or testing but not for production-like setups. Custom configuration allows you to specify a **load-balanced, auto-scaling** environment with multiple instances, which is what the Vprofile production setup requires.

***

## 1.6 Service Role and Instance Profile — IAM Permissions

Two IAM entities are required: [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

**Service Role** — the permissions that Beanstalk itself needs to manage AWS resources on your behalf. When Beanstalk creates EC2 instances, configures load balancers, or manages auto scaling, it needs IAM permissions to do so. The service role grants these permissions. The instructor selects "Use an existing service role" — this role was created in the earlier re-architecting project.

**Instance Profile** — the permissions that the EC2 instances themselves have. When the Vprofile application running on the instance needs to access other AWS services (like S3, or in this case potentially RDS), it uses the permissions attached through the instance profile. The instructor selects `vprofile-bean-role`.

The instructor notes: "If you don't see this, make sure you watch that lecture and create this role." These roles are prerequisites — without them, Beanstalk either can't create resources (missing service role) or the application can't access AWS services it needs (missing instance profile). [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

***

## 1.7 VPC and Subnet Configuration — Network Placement

The instructor selects the VPC from the dropdown and activates **public IP address** for instances. This means each EC2 instance launched by Beanstalk will receive a public IP, making it accessible from the internet (through the load balancer). [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

For subnets, the instructor selects **all available subnets**: "When the instance gets launched, it can go to any of the zones. So we will have minimum two instances. So it's going to divide these two instances in two Availability Zones." [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

This is the same multi-AZ distribution concept from the ASG lecture — Beanstalk distributes instances across availability zones for high availability. If one AZ has a problem, instances in other AZs continue serving traffic.

***

## 1.8 Root Volume — The GP3 vs. Container Default Problem

This is the most operationally critical piece of configuration advice in the lecture. The instructor explicitly warns: "There's some recent issues with Beanstalk. It is trying to use Launch Configuration, which is outdated, and you'll get an error. That Beanstalk should be using Launch Template." [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

The workaround: change the root volume from **Container Default** to **General Purpose 3 (GP3)**. When you select GP3, Beanstalk uses a **Launch Template** (the modern mechanism). When you leave it as Container Default, Beanstalk falls back to **Launch Configuration** (deprecated), which causes errors.

This is a practical gotcha that can block the entire exercise. The fix is simple (select GP3), but the failure mode is confusing if you don't know about it.

⚠️ **Expert Note:** Launch Configurations were AWS's older mechanism for defining instance launch parameters (before Launch Templates). AWS has deprecated them, and they're being phased out. But some Beanstalk configurations still default to the old path. Selecting GP3 forces the modern path. This is a transitional issue that may be resolved in future Beanstalk updates, but as of the video's recording, it's a real blocker.

***

## 1.9 Auto Scaling Configuration — Load Balanced with Boundaries

The instructor changes the scaling type from **Single instance** to **Load balanced**. This tells Beanstalk to create an Auto Scaling Group and an Application Load Balancer, instead of just a single standalone instance. [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

The scaling parameters set:

* **Minimum:** 2 instances
* **Maximum:** 4 instances (the instructor notes "you can keep maximum as 2 as well — we are anyways not going to scale out, we'll just deploy the application on multiple instances")

**Instance type:** The instructor removes `t2.small` (which Beanstalk may suggest by default) and explicitly selects **`t2.micro`** — "because that comes under Free tier." [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

**Scaling triggers:** Left at default. These are the CloudWatch-based metrics that trigger scale-out/scale-in events (similar to the target tracking policy from the ASG lecture).

***

## 1.10 Load Balancer Configuration

**Visibility:** Public — the load balancer is internet-facing, accessible from outside.

**Type:** Application Load Balancer, Dedicated. The instructor selects this explicitly. "Dedicated" means the ALB is created specifically for this Beanstalk environment, not shared with other environments.

**Listeners:** Default (port 80 HTTP). [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

***

## 1.11 Session Stickiness — Application-Specific Requirement

The instructor navigates to **Processes**, selects the default process, edits it, and enables **Session stickiness**. The explanation is precise and important: [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

"We will have two instances. So what stickiness will do is — when we access our application through the load balancer, and let's say we go to instance number 1, stickiness will hold that session for us. If we don't have stickiness, then it is going to bounce between these instances." [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

The problem: Vprofile is a "very simple" application that doesn't implement token-based authentication. When a user logs in, the session is stored on the specific Tomcat instance that handled the login. If the next request goes to a different instance (as a load balancer normally distributes), that instance doesn't have the session — the user appears logged out. "If it jumps to another instance, we'll lose the authentication."

Session stickiness solves this by instructing the load balancer to send all requests from the same user to the **same backend instance** for the duration of their session. The ALB achieves this by setting a cookie that identifies which instance the user is "stuck" to.

🔍 **Deep Dive:** Stickiness is a trade-off. It solves session persistence for simple applications but **undermines the load balancer's ability to distribute traffic evenly**. If many users happen to get stuck to one instance, that instance gets overloaded while others sit idle. In production applications, the proper solution is to **externalize session storage** (to Redis, Memcached, or a database) so any instance can serve any request — making stickiness unnecessary. The instructor explicitly frames stickiness as a requirement specific to this simple Vprofile application, not a general best practice. [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

***

## 1.12 Rolling Updates — Deployment Strategy

The instructor configures the deployment policy as **Rolling** with a batch size of **50%**. The behavior: when deploying a new version of the application, Beanstalk updates instances in batches. With 2 instances and 50%, one instance is updated at a time — the other continues serving traffic. [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

The instructor provides production guidance: "In real-time production cases, you will have multiple instances, and percentage of deployment should be not more than 25%. Mostly in production, it's just 10%. Let's say you have 10 instances, so 10% means one instance at a time." [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

The reasoning: smaller batch sizes reduce risk. If the new deployment has a bug, only a small fraction of instances are affected at any time. With 10% batches, a bad deployment only impacts 1 out of 10 instances before you can detect the problem and roll back. With 50%, half your fleet is affected immediately.

The alternative to percentage is a **fixed number** — you can specify "update 1 instance at a time" regardless of fleet size. [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

***

## 1.13 Tags and Resource Naming

The instructor adds a tag: **Project: vprofile**. He notes: "You cannot use a name tag because that tag is already taken. When we create application, it anyways uses that tag." Beanstalk automatically applies a Name tag to its resources, so manually adding another Name tag would conflict. The Project tag serves as a secondary organizational label. [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

***

## 1.14 Security Groups — Auto-Created

The instructor notes that Beanstalk "will create its own security groups" and keeps the defaults. Beanstalk automatically creates security groups for the load balancer and for the instances, with appropriate rules to allow traffic from the ALB to the instances. This is one of the "managed" aspects — you don't need to manually configure the security group chain. [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

***

## 1.15 What Happens After Submit — And the RDS Bridge

After clicking Submit, "it is going to take some time to launch this application." Beanstalk begins creating all the infrastructure: EC2 instances, ASG, ALB, target groups, security groups, CloudWatch alarms — everything. [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

The instructor bridges to the next lecture: "By the time, we will create RDS." This implies the Vprofile application also needs a database, which will be created separately (not managed by Beanstalk) while the environment provisions.

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are creating a **production-like Elastic Beanstalk environment** for the Vprofile Java web application: a load-balanced, auto-scaled Tomcat environment with multiple instances across availability zones, session stickiness for authentication, and rolling deployment capability. The final outcome: a fully managed infrastructure accessible via a unique Beanstalk URL, ready to receive the Vprofile application artifact. [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

***

## Step 1: Create a Key Pair

Navigate to **EC2 Console → Key Pairs → Create Key Pair**. [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

**Settings:**

* **Name:** `vprobeankey`
* **Format:** default (`.pem`)

Click **Create Key Pair**. Download the `.pem` file.

**Why:** This key pair will be used to SSH into the Beanstalk EC2 instances for troubleshooting. The instructor mentions "we have a use case for that, and we'll do that in some time." [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

**Connection to flow:** The key pair will be referenced in the Beanstalk environment configuration.

***

## Step 2: Navigate to Beanstalk and Create Application

Search for **Elastic Beanstalk** in the AWS console. Click **Create Application**. [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

### 2a. Environment Tier:

Select **Web server environment**. [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

### 2b. Application Name:

Enter: `Vprofile`

### 2c. Environment Name:

Enter: `Vprofile-prod-11` (add unique numbers — the instructor adds `11`)

### 2d. Domain:

Enter the same name as the environment. Click **Check Availability** to verify the domain is unique. [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

**Critical:** This domain becomes the URL (`Vprofile-prod-11.elasticbeanstalk.com`). It must be globally unique. If it's taken, change the numbers.

**Common mistake:** Using the exact same name as the instructor. You must choose your own unique identifier.

### 2e. Platform:

* **Platform:** Tomcat
* **Platform branch:** Tomcat 10 with Corretto 21 running on Amazon Linux 2023 [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

### 2f. Configuration:

Select **Custom configuration** (not the default preset).

Change the environment type to **Load balanced** (this option appears in the custom configuration). [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

Click **Next**.

***

## Step 3: Configure Service Access (IAM)

### 3a. Service Role:

Select **Use an existing service role** → choose the Beanstalk service role created in the re-architecting project. [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

**If you don't see this role:** You must go back to the re-architecting project lecture and create it first. This is a hard prerequisite.

### 3b. Key Pair:

Select `vprobeankey` (created in Step 1). [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

### 3c. Instance Profile:

Select `vprofile-bean-role`. [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

Click **Next**.

***

## Step 4: Configure Networking

### 4a. VPC:

Select your VPC from the dropdown. [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

### 4b. Public IP:

Set to **Activated** — instances will have public IP addresses.

### 4c. Subnets:

Select **all available subnets**. This allows Beanstalk to distribute instances across all availability zones. With 2 instances, they'll be placed in 2 different AZs for high availability. [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

### 4d. Tags:

Click **Add new tag**:

* **Key:** `Project`
* **Value:** `vprofile`

**Do NOT use `Name` as the key** — Beanstalk auto-assigns the Name tag. Using it manually causes a conflict. [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

Click **Next**.

***

## Step 5: Configure Instance and Scaling

### 5a. Root Volume — CRITICAL:

Change from **Container Default** to **General Purpose 3 (GP3)**. [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

⚠️ **This is mandatory.** If you leave it as Container Default, Beanstalk will attempt to use the deprecated Launch Configuration mechanism and **the creation will fail with an error**. GP3 forces Beanstalk to use Launch Templates (the modern mechanism). [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

### 5b. Security Groups:

Keep defaults — Beanstalk creates its own security groups automatically. [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

### 5c. Auto Scaling Group:

Change from **Single instance** to **Load balanced**.

* **Minimum instances:** `2`
* **Maximum instances:** `4` (or `2` if you want to stay minimal) [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

### 5d. Instance Type:

**Remove** `t2.small` if pre-selected. **Add** `t2.micro` — this stays within the Free Tier. [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

### 5e. Scaling Triggers:

Keep **Default**. [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

### 5f. Load Balancer:

* **Visibility:** Public
* **Type:** Application Load Balancer, **Dedicated**
* **Listeners:** Default (port 80) [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

### 5g. Session Stickiness:

Navigate to **Processes** → select the default process → **Actions → Edit**.

Under **Sessions**, **enable Session stickiness**. [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

Click **Save**.

**Why this is needed:** The Vprofile application doesn't use token-based auth. Without stickiness, users bounce between instances and lose their login session. Stickiness pins each user to the instance that handled their login. (See Theory §1.11.)

### 5h. Rolling Updates:

* **Deployment policy:** Rolling
* **Batch size type:** Percentage
* **Batch size:** `50%` (with 2 instances, this means 1 instance at a time) [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

**Production guidance from the instructor:** In production with many instances, use 10-25%. With 10 instances, 10% = 1 instance at a time. Smaller batches = less risk per deployment cycle. [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

Everything else: keep **Default**.

Click **Next**.

***

## Step 6: Review and Submit

Review all settings on the summary page. Verify: [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

* ✅ Platform: Tomcat 10, Corretto 21, Amazon Linux 2023
* ✅ Service role and instance profile selected
* ✅ Key pair: vprobeankey
* ✅ VPC with all subnets, public IP activated
* ✅ Root volume: GP3 (NOT Container Default)
* ✅ Auto Scaling: Load balanced, min 2, max 4, t2.micro
* ✅ ALB: Public, dedicated, port 80
* ✅ Session stickiness: Enabled
* ✅ Rolling updates: 50%
* ✅ Tag: Project = vprofile

If anything is wrong, click **Edit** on that section to fix it.

Click **Submit**. [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

**What happens:** Beanstalk begins provisioning the entire environment — EC2 instances, ASG, ALB, target groups, security groups, CloudWatch configuration. This takes several minutes.

**While waiting:** The instructor creates the RDS database in the next lecture (the Vprofile app needs a database, and it's created outside Beanstalk).

**Verification (after provisioning completes):**

1. Environment status shows **"OK"** (green) in the Beanstalk console
2. The environment URL (`Vprofile-prod-11.elasticbeanstalk.com`) loads in a browser (initially showing a default Beanstalk page or Tomcat page until the application artifact is deployed)
3. EC2 console shows 2 running instances with the name tag from the environment
4. Load Balancer console shows an active ALB
5. Target Group shows 2 healthy targets

**Common failure:** If you left the root volume as Container Default → the environment creation fails with a Launch Configuration error. Fix: delete the failed environment, recreate with GP3 selected. [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🗺️ Beanstalk = Managed Orchestration of Known Components

```
WHAT BEANSTALK CREATES FOR YOU:
┌─────────────────────────────────────────────────────────┐
│  Elastic Beanstalk Environment (Vprofile-prod-11)       │
│                                                          │
│  ┌──────────────────────┐                                │
│  │ Application Load     │  ← Public, Dedicated, :80     │
│  │ Balancer (ALB)       │  ← Stickiness ENABLED         │
│  └──────────┬───────────┘                                │
│             │ forwards to                                │
│  ┌──────────▼───────────┐                                │
│  │ Target Group         │  ← auto-populated by ASG      │
│  └──────────┬───────────┘                                │
│             │ contains                                   │
│  ┌──────────▼───────────┐                                │
│  │ Auto Scaling Group   │  ← Min:2, Max:4, t2.micro     │
│  │ ┌────────┐┌────────┐ │  ← Across all AZs             │
│  │ │ EC2    ││ EC2    │ │  ← Tomcat 10 + Corretto 21    │
│  │ │ Inst 1 ││ Inst 2 │ │  ← Amazon Linux 2023          │
│  │ └────────┘└────────┘ │  ← Public IP: Activated        │
│  └──────────────────────┘                                │
│  + Security Groups (auto-created)                        │
│  + CloudWatch Monitoring                                 │
│  + Rolling Deployment (50% batches)                      │
│                                                          │
│  EXTERNAL (created separately):                          │
│  └── RDS Database (next lecture)                         │
└─────────────────────────────────────────────────────────┘

YOU manage: application code (WAR file)
BEANSTALK manages: all infrastructure
```

***

## ⚡ Configuration Decisions — Quick Recall

```
APPLICATION:    Vprofile
ENVIRONMENT:    Vprofile-prod-11 (unique domain, check availability)
TYPE:           Web server environment
PLATFORM:       Tomcat 10, Corretto 21, Amazon Linux 2023
CONFIGURATION:  Custom (not default → need load balanced)

IAM:
  Service Role:    existing Beanstalk service role
  Instance Profile: vprofile-bean-role
  Key Pair:        vprobeankey

NETWORK:
  VPC:             default
  Public IP:       Activated
  Subnets:         ALL (multi-AZ distribution)

VOLUME:
  Root:            GP3 ← ⚠️ CRITICAL (NOT Container Default)
                   Container Default → Launch Config (deprecated) → ERROR
                   GP3 → Launch Template (modern) → WORKS

SCALING:
  Type:            Load balanced (NOT single instance)
  Min: 2 | Max: 4
  Instance:        t2.micro (free tier, remove t2.small)
  Triggers:        Default

LOAD BALANCER:
  Visibility:      Public
  Type:            ALB, Dedicated
  Listener:        Port 80
  Stickiness:      ENABLED (Vprofile needs it for session persistence)

DEPLOYMENT:
  Policy:          Rolling
  Batch:           50% (= 1 instance at a time with 2 instances)
  Production rec:  10-25% in real environments

TAGS:
  Project: vprofile
  ⚠️ Do NOT use Name tag (auto-assigned by Beanstalk)
```

***

## 🔗 Beanstalk Hierarchy

```
Application (Vprofile)
  └── Environment (Vprofile-prod-11)
        ├── URL: Vprofile-prod-11.elasticbeanstalk.com (globally unique)
        ├── Platform: Tomcat 10 / Corretto 21 / Amazon Linux 2023
        ├── Infrastructure: ALB + ASG + EC2 + SG + CloudWatch
        └── Deployment: Rolling 50%
```

***

## 🔒 Session Stickiness — Why and When

```
PROBLEM:
  User logs in → request hits Instance 1 → session stored on Instance 1
  Next request → LB sends to Instance 2 → NO session → user logged out

SOLUTION: Session Stickiness
  LB sets cookie → pins user to same instance for session duration
  All requests from same user → same backend instance

SCOPE: Required for Vprofile (no token-based auth, simple session)

TRADE-OFF:
  ✅ Fixes session persistence for simple apps
  ❌ Uneven load distribution (users cluster on one instance)
  
BETTER ALTERNATIVE (production):
  Externalize sessions (Redis/Memcached) → stickiness unnecessary
```

***

## ⚠️ GP3 Workaround — Critical Operational Fix

```
ROOT VOLUME SELECTION:
  Container Default → Beanstalk uses Launch Configuration (DEPRECATED)
                    → CREATION FAILS with error
  
  GP3              → Beanstalk uses Launch Template (MODERN)
                    → CREATION SUCCEEDS

ACTION: Always select GP3 for root volume in Beanstalk
STATUS: Known issue at time of recording, may be fixed later
```

***

## 🔄 Rolling Deployment — Batch Size Logic

```
FLEET SIZE: 2 instances
BATCH: 50% → 1 instance at a time
FLOW: Update Instance 1 → verify → Update Instance 2

PRODUCTION GUIDANCE:
  10 instances × 10% = 1 at a time (safest)
  10 instances × 25% = 2-3 at a time (faster)
  ⚠️ Larger batch = more risk if deployment is bad
  
ALTERNATIVE: Fixed number instead of percentage
```

***

## 📦 IAM Roles — Two Distinct Purposes

```
SERVICE ROLE:
  WHO: Beanstalk service itself
  DOES: Create/manage EC2, ALB, ASG, SG, CloudWatch
  SCOPE: Infrastructure management permissions

INSTANCE PROFILE:
  WHO: EC2 instances launched by Beanstalk
  DOES: Access AWS services the app needs (S3, RDS, etc.)
  SCOPE: Application-level permissions

BOTH required. Neither works without the other.
Created in previous re-architecting project lecture.
```

***

## 🧹 Prerequisite Checklist (Before Starting)

```
□ Key pair created (vprobeankey)
□ Beanstalk service role exists (from re-architecting project)
□ Instance profile exists (vprofile-bean-role)
□ VPC available with subnets
□ All other VMs shut down (free tier resource limits)
```

***

## 🏗️ Reusable Engineering Patterns

**Pattern 1: Orchestration Over Manual Assembly**
Beanstalk creates the same components you'd build manually (ALB, ASG, TG, SG, instances) but manages them as a single declarative unit. The pattern: when a well-understood infrastructure topology is repeated frequently, wrap it in an orchestrator that accepts configuration and produces the full stack. This same pattern appears in CloudFormation, Terraform, Kubernetes Helm charts, and Docker Compose.

**Pattern 2: Platform-Application Alignment**
The platform (Tomcat 10 / Corretto 21) must match the application's runtime requirements. Misalignment (e.g., deploying a Java 21 app on a Java 8 platform) causes runtime failures. This "runtime contract" pattern applies to any deployment: Docker base images, Lambda runtimes, Kubernetes pod specs — the execution environment must match the application's expectations.

**Pattern 3: Workaround Documentation as Operational Knowledge**
The GP3 workaround is not in any official architecture diagram. It's operational knowledge gained from encountering a real failure. Documenting workarounds (why something fails, what the fix is, and when it might become unnecessary) is as important as documenting the intended design. Real-world systems always have these gaps between documentation and reality.

**Pattern 4: Deployment Risk Proportional to Batch Size**
Rolling deployments with smaller batches expose fewer instances to risk at any moment. The trade-off is speed vs. safety: 10% batches are safe but slow (10 cycles to update 10 instances), while 50% is fast but risky (half your fleet runs new code immediately). Production defaults to the conservative end (10-25%).

***

## 🎯 One-Line System Summary

> **Elastic Beanstalk creates a managed Tomcat environment — provisioning ALB, ASG, EC2 instances, security groups, and monitoring from a single configuration wizard — requiring correct IAM roles, GP3 volume selection (to avoid the Launch Configuration bug), session stickiness for Vprofile's simple auth model, and rolling deployment at 50% batch size, with RDS created separately in the next lecture.** [\[283-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/283-beanstalk.txt)
