# AWS Elastic Beanstalk — vProfile Refactoring Project (Environment Setup)

**Source:** Video caption file — *"Elastic Beanstalk Environment Setup"* (from the vProfile AWS Refactoring course) [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — What Is Elastic Beanstalk and What Problem Does It Solve?

To understand Beanstalk, you must first remember what it took to deploy the vProfile Tomcat application in the Lift and Shift project: create a security group, create a key pair, launch an EC2 instance, install Tomcat on it, create a target group, create an Application Load Balancer, build and upload the artifact to S3, deploy it to Tomcat manually, and then — once everything was verified — create an AMI, a Launch Template, and an Auto Scaling Group. That was a long chain of individually managed components, each requiring separate configuration, verification, and maintenance. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

**Elastic Beanstalk gives you all of this as a single suite.** When you create a Beanstalk environment and select Tomcat, it provisions the EC2 instance(s), the Auto Scaling Group, the AMI management, the S3 bucket for artifacts, CloudWatch monitoring, logs — everything. And it's very easy to tweak settings whenever needed, and "super easy to do the deployment." [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

Beanstalk is described as "an easy to use service for deploying and scaling web applications and services" that supports Java, .NET, PHP, Node.js, Python, Ruby, Go, and Docker. The Docker support is particularly significant — in a later project when the vProfile application is containerized as Docker images, those images can also run on Beanstalk. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

A critical economic fact: **there is no additional charge for Elastic Beanstalk itself**. You pay only for the underlying resources it provisions — EC2 instances, EBS volumes, load balancers, etc. Beanstalk as an orchestration and automation layer is free. This means the convenience and automation it provides comes at zero extra cost compared to managing the same resources manually. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

🔍 **Deep Dive:**
Beanstalk is not a new type of infrastructure — it is an **orchestration layer** on top of the same AWS resources you would use manually. Underneath a Beanstalk environment, there are real EC2 instances, real ALBs, real ASGs, real security groups, real S3 buckets. The difference is that Beanstalk creates, configures, monitors, and manages all of them as a unified environment. You interact with the environment as a single entity rather than managing each component individually. This is why the key pair still exists — "in case you need to login" to the underlying EC2 instance for troubleshooting, the infrastructure is still accessible. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

***

## 1.2 — Beanstalk Application vs. Environment

Beanstalk introduces two levels of organization that are important to distinguish. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

A **Beanstalk Application** is the top-level container — it represents your project or product. Under one application, you can have **multiple Environments**. Each environment represents a different deployment stage: dev, test, staging, production. Each environment is a complete, independent stack — its own EC2 instances, its own ASG, its own load balancer, its own S3 bucket, everything. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

This means you can have a single Beanstalk application called "vprofile" with separate environments for development, testing, and production — each with different instance sizes, scaling configurations, and deployed artifact versions. The environments are fully isolated from each other. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

The environment also gets a **unique URL** (domain) to access the application. This URL must be globally unique across all of Beanstalk — you must check its availability before proceeding. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

***

## 1.3 — IAM Roles for Beanstalk: Service Role vs. Instance Profile

Beanstalk requires **two distinct IAM roles**, and understanding their separation is critical because they serve fundamentally different purposes. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

**Service Role** — This is the role that the Beanstalk service itself assumes to manage AWS resources on your behalf. When Beanstalk creates EC2 instances, configures load balancers, sets up auto scaling, manages deployments — it uses the service role's permissions to do all of that. This is the `aws-elasticbeanstalk-service-role`. If it doesn't exist, you can create it directly from the Beanstalk creation wizard by clicking the "Create Role" button — the wizard auto-selects the correct policies and names the role for you. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

**Instance Profile Role** — This is the role attached to the **EC2 instances** that Beanstalk launches. It defines what the instances themselves are allowed to do — access S3, write to CloudWatch, interact with other AWS services, etc. Beanstalk can create a default instance profile role, but the video explicitly warns: "that role lacks some permission which will be a problem for our project." Therefore, you create a custom role manually before creating the Beanstalk environment. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

The custom instance profile role requires four specific policies:

1. **AdministratorAccess-AWSElasticBeanstalk** — broad Beanstalk administrative permissions
2. **AWSElasticBeanstalkCustomPlatformforEC2Role** — permissions for custom platform operations
3. **AWSElasticBeanstalkRoleSNS** — permissions for SNS notifications
4. **AWSElasticBeanstalkWebTier** — permissions for web tier operations (S3 artifact access, log publishing, etc.)

The role is created with the EC2 use case (because it's attached to EC2 instances) and named `vprofile-Rearch-bean-role`. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

⚠️ **Expert Note:**
The distinction between service role and instance profile is a fundamental AWS IAM pattern. The service role governs what the **management plane** (Beanstalk itself) can do. The instance profile governs what the **data plane** (the actual running instances) can do. In production, these should follow the principle of least privilege — the instance profile should only have the permissions the application actually needs, not broad administrative access. The video uses broader permissions for simplicity in a learning project. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

***

## 1.4 — Platform Selection: Tomcat, Corretto, and Version Branches

When creating a Beanstalk environment, you select a **platform** — the runtime your application needs. For vProfile, the platform is **Tomcat**. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

Within the Tomcat platform, you select a **platform branch**, which defines the specific versions of Tomcat and the Java runtime. The video selects **Tomcat 10 with Corretto 21** (Java 21). Corretto is Amazon's distribution of OpenJDK — so "Corretto 21 means Java 21 with Tomcat 10 on top of it." [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

The **platform version** is kept at the recommended default — this is the specific AMI and configuration AWS maintains for that branch. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

**Application code** is initially set to **Sample Application** — a placeholder. The actual vProfile artifact will be uploaded later. This is a practical decision: get the environment running first with a known-good sample, verify everything works, then deploy your custom application. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

***

## 1.5 — The GP3 Volume and Launch Template vs. Launch Configuration Issue

This is a critical operational detail that the video explicitly warns about. When configuring the root volume for Beanstalk EC2 instances, you must change from **"Container Default"** to **General Purpose 3 (GP3)**. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

The reason is a compatibility issue: if you select "Container Default," Beanstalk will attempt to use a **Launch Configuration** to launch instances. Launch Configurations are an older, **outdated** AWS feature that has been superseded by **Launch Templates**. Using Launch Configurations now causes errors. Selecting GP3 forces Beanstalk to use Launch Templates, which is the current and correct behavior. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

This is not a storage performance decision — it's a **compatibility workaround**. The video calls this out as "some recent issues with Beanstalk" where the container default triggers the wrong instance launch mechanism. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

⚠️ **Expert Note:**
This is a real-world example of how managed services can have subtle operational gotchas. AWS has been deprecating Launch Configurations in favor of Launch Templates, but not all Beanstalk configurations have been updated to default to the new behavior. Selecting GP3 is the workaround that ensures modern Launch Template usage. This is the kind of issue you only discover by running into the error or by being warned (as the video does). [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

***

## 1.6 — Load Balanced vs. Single Instance: Capacity Configuration

Beanstalk offers two fundamental environment types: **Single Instance** (one EC2 instance, no load balancer) and **Load Balanced** (multiple instances behind a load balancer with auto scaling). [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

For production use (and for this project), **Load Balanced** is selected. This automatically creates an Application Load Balancer and an Auto Scaling Group. The video configures minimum 2 instances and maximum 4. The minimum of 2 is chosen for two reasons: (1) a load balancer needs at least 2 instances to meaningfully distribute traffic, and (2) the instructor wants to demonstrate deployment strategies that require multiple instances. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

An important operational note: "You can anytime change these things. Maximum number, minimum number. You can anytime change." Beanstalk allows runtime reconfiguration of capacity parameters without recreating the environment. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

***

## 1.7 — Port Behavior: Beanstalk Tomcat Runs on Port 80, Not 8080

This is a key difference from the Lift and Shift project that can cause confusion. In a standard Tomcat installation on EC2, Tomcat runs on **port 8080** by default. In the Lift and Shift project, the ALB listened on port 443 (HTTPS) and routed traffic to port 8080 on the Tomcat instances. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

**In Beanstalk, Tomcat runs on port 80.** The load balancer also listens on port 80 and routes requests to port 80 on the EC2 instances. This is a Beanstalk-specific configuration — Beanstalk's platform sets up Tomcat to run behind a reverse proxy (typically Nginx) on port 80, not on the raw Tomcat default of 8080. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

Later in the project, the listener will be changed to HTTPS (port 443), but the initial setup uses HTTP on port 80. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

***

## 1.8 — Load Balancer Type: Application vs. Network

The video briefly covers the choice between Application Load Balancer (ALB) and Network Load Balancer (NLB). [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

**Application Load Balancer** is selected because it is designed for HTTP/HTTPS traffic, which is what a web application serves. It operates at Layer 7 (application layer) and can make routing decisions based on URL paths, headers, and other HTTP attributes.

**Network Load Balancer** is described as "high performing, gives you static IP, really amazing but expensive." NLB operates at Layer 4 (transport layer) and handles raw TCP/UDP traffic with extremely low latency. It's mentioned for awareness but not used because it's overkill and more expensive for this use case. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

***

## 1.9 — Scaling Triggers for Web Applications

The Auto Scaling Group within Beanstalk uses scaling triggers to decide when to add or remove instances. The two most commonly used metrics for web applications are **CPU Utilization** and **Network Out**. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

**Network Out** gets a particularly useful explanation in this video. For web applications, Network Out represents the amount of data the servers are sending back to users. When more users access the application, the servers respond more, generating more outbound network traffic. So increasing Network Out directly correlates with increasing user load. Conversely, decreasing Network Out means fewer users are active. This makes Network Out "a very, very much apt trigger to scale out or scale in for web applications." [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

***

## 1.10 — Decoupled vs. Coupled RDS

Beanstalk offers the option to create an RDS database instance as part of the Beanstalk environment. However, the video explicitly chooses **not** to use this feature and instead uses the RDS instance that was created separately in a previous step. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

The reason is **decoupling**. If RDS is created as part of the Beanstalk environment, the database lifecycle is tied to the environment lifecycle — if you delete the Beanstalk environment, the database could be deleted with it. By creating RDS separately, "we can manage both separately." The database persists independently of the Beanstalk environment. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

The video notes that Beanstalk has recently added an option to decouple RDS even when created through Beanstalk, but the safer and more established practice is to create it separately from the beginning. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

***

## 1.11 — Enhanced Health Reporting

Beanstalk offers two levels of health reporting: **Basic** and **Enhanced**. The video selects **Enhanced** and explains its importance specifically for deployments. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

With enhanced health reporting, Beanstalk collects detailed health metrics from each instance. During a deployment, Beanstalk uses these metrics to verify that an instance is healthy **before proceeding to deploy to the next instance**. This is critical for rolling deployments — if the first instance fails after receiving the new code, enhanced health reporting detects this and can stop the deployment before it breaks the remaining instances. Without enhanced reporting, Beanstalk has limited visibility into whether the deployment is actually working. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

***

## 1.12 — Deployment Policies: The Five Strategies

This is the most conceptually rich topic in the entire lecture. Beanstalk offers five deployment policies, each representing a different tradeoff between speed, cost, safety, and user impact. Understanding these is essential not just for Beanstalk but as general deployment engineering knowledge — the video notes these are "very interesting topic for DevOps engineers or even architects" and relevant for interviews. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

### All at Once

The simplest and fastest policy. If you have 10 instances, Beanstalk takes **all 10 down simultaneously**, deploys the new code to all of them, and brings them all back. This results in **definite downtime** — the application is completely unavailable during the update. It's the cheapest option (no extra instances) and the fastest (everything updates in one pass), but it's only acceptable for non-production environments where downtime is tolerable. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

### Rolling

Beanstalk updates instances in **batches**. You specify the batch size as either a fixed number or a percentage. With 10 instances and a 20% batch size, Beanstalk takes 2 instances out of the load balancer, deploys the new code, brings them back, then moves to the next 2. During the update, your capacity is reduced by the batch size — 8 out of 10 instances are serving traffic while 2 are being updated. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

The video warns: "You cannot afford to give 50%. Reducing your application capacity to 50% is very bad. User will feel that lag and your application may even hang halt. So 10%, 20% is fair enough." The batch size directly determines how much capacity reduction your users experience. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

### Rolling with Additional Batch

This solves the capacity reduction problem of standard Rolling. Instead of taking existing instances offline, Beanstalk **launches new instances first** with the updated code, adds them to the load balancer, and then removes the same number of old instances. With 10 instances and a 20% batch, Beanstalk adds 2 new upgraded instances (total becomes 12), then removes 2 old ones (back to 10), and continues. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

"At the time of the upgrade you will have more instances, not less." After the upgrade completes, the instance count returns to the original. This is safer than standard Rolling because capacity is never reduced, but it costs more because you're temporarily paying for extra instances. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

### Immutable

The safest policy. Beanstalk creates an **entirely new set of instances** (all 10) with the updated code. Once all new instances are healthy, traffic is routed to the new set, and the old set is terminated. At no point is the old environment modified — if anything goes wrong with the new instances, the old ones are still running untouched. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

"Safest one but expensive" — during the transition, you're paying for double the instances. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

### Traffic Splitting (Canary Testing)

The most sophisticated policy. Beanstalk launches a small number of new instances with the updated code and routes only a **percentage of traffic** (e.g., 10%) to them. This lets you verify the new version works correctly with real user traffic before committing to a full rollout. If the new version has problems, only a small percentage of users are affected. If everything is good, Beanstalk gradually shifts more traffic until the rollout is complete. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

The video explicitly calls this **canary testing** and flags it as "one of the interview questions." The name comes from the "canary in the coal mine" concept — you send a small amount of traffic to the new version to detect problems early before they affect everyone. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

The video recommends reading the official Beanstalk deployment policy documentation for deeper understanding.

🔍 **Deep Dive:**
The five deployment policies form a **spectrum from speed to safety**:

```
All at Once → Rolling → Rolling + Batch → Immutable → Traffic Splitting
   FASTEST                                                  SAFEST
   CHEAPEST                                              MOST EXPENSIVE
   DOWNTIME                                              ZERO RISK
```

Each step along this spectrum adds protection but increases cost and deployment time. The choice depends on the specific project's tolerance for downtime, budget, and risk appetite. For the project, **Rolling with 50% batch size** is selected — with only 2 minimum instances, 50% means 1 instance at a time, which is reasonable for a learning environment. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

***

## 1.13 — Stickiness in Beanstalk

Stickiness (session affinity) is configured within the Beanstalk health check / processes settings — the same concept covered in the ASG lecture for the Lift and Shift project. The vProfile application stores authentication state locally on the instance, so a user connected to one instance must continue being routed to that same instance. Without stickiness, refreshing the page routes to a different instance and the user is logged out. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

The video notes this applies not only to vProfile but also "in many other applications. If you're working in some project, that may be the case." [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

***

## 1.14 — Environment Properties

Beanstalk allows you to set **environment variables** (called environment properties) that are available to the application at runtime. These can include database connection strings, port numbers, feature flags, or any configuration value. This mechanism lets you externalize configuration from the application code — the same artifact can behave differently depending on the environment properties set in each Beanstalk environment (dev vs. production, for example). [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

The video mentions this feature but does not use it for this project. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

***

## 1.15 — Automatic Updates (Minor and Patch)

Beanstalk can automatically apply **minor and patch updates** to the platform — for example, a new minor version of Tomcat or a security patch to the Java runtime. Whether to enable this depends on the project's change management requirements. The video keeps the default (enabled for minor and patch) but notes: "It depends. For your project, you want to do automatic updates or not." [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

***

## 1.16 — CloudWatch Monitoring Interval

Beanstalk integrates with CloudWatch for monitoring. The monitoring interval can be set to **5 minutes** (free) or **1 minute** (paid). The video keeps 5 minutes — sufficient for most purposes and free tier eligible. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are creating an Elastic Beanstalk environment for the vProfile application as part of the Refactoring project. The final outcome: a fully managed environment with Tomcat EC2 instances behind an Application Load Balancer, auto scaling, S3 artifact storage, CloudWatch monitoring — all provisioned and managed by Beanstalk as a single unit. Once this environment is running, we can deploy the application artifact with a single click. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

***

## Execution Flow Overview

```
Step 1: Create IAM Instance Profile Role
Step 2: (If needed) Create/Verify Beanstalk Service Role
Step 3: Create Beanstalk Application and Environment
        ├── Application info + Platform
        ├── Service access (roles + key pair)
        ├── Networking (VPC, public IP, subnets)
        ├── Database (skip — already created separately)
        ├── Tags
        ├── Instance settings (GP3 volume, monitoring, SG)
        ├── Capacity (load balanced, min/max, instance type)
        ├── Scaling triggers
        ├── Load balancer (ALB, port 80, stickiness)
        ├── Monitoring (enhanced)
        ├── Deployment policy (rolling, 50%)
        └── Submit
Step 4: Wait for environment creation
```

***

### Step 1: Create IAM Instance Profile Role

**What we are doing:** Creating a custom IAM role that will be attached to every EC2 instance Beanstalk launches.

**Why:** Beanstalk's auto-created default role lacks necessary permissions for this project. We need a role with the correct Beanstalk-specific policies.

**Execution:**

1. Navigate to **IAM → Roles → Create Role**.
2. **Trusted entity type:** AWS Service.
3. **Use case:** EC2. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)
4. Click **Next**.
5. **Search for policies** — search the word `bean` and select these four policies:
   * `AdministratorAccess-AWSElasticBeanstalk`
   * `AWSElasticBeanstalkCustomPlatformforEC2Role`
   * `AWSElasticBeanstalkRoleSNS`
   * `AWSElasticBeanstalkWebTier` [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)
6. Click **Next**.
7. **Role name:** `vprofile-Rearch-bean-role`
8. **Description:** same as the name.
9. Click **Create Role**. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

**How to verify:** The role appears in the IAM Roles list with the four policies attached.

**Important:** Remember this role name — you must select it as the instance profile during Beanstalk creation.

**Connection to flow:** This role is selected in Step 3 during Beanstalk environment configuration. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

***

### Step 2: Create/Verify Beanstalk Service Role

**What we are doing:** Ensuring the AWS Elastic Beanstalk service role exists.

**Why:** This is the role Beanstalk itself uses to manage AWS resources (create EC2, configure ALB, manage ASG, etc.). It's separate from the instance profile role.

**Execution:**

* If the service role already exists in IAM, it will appear in the Beanstalk creation dropdown. No action needed.
* If it does **not** exist (dropdown is empty after refresh), click the **"Create Role"** button directly in the Beanstalk creation wizard. It auto-selects the correct policies and names the role. Click **Create Role**, then go back and refresh the dropdown. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

**How to verify:** The `aws-elasticbeanstalk-service-role` (or equivalent) appears in the Service Role dropdown.

***

### Step 3: Create Beanstalk Application and Environment

**What we are doing:** Creating the complete Beanstalk environment — this is the main step that provisions the entire frontend tier.

**Execution (in order of configuration screens):**

***

**3a — Application and Environment Basics:**

1. Navigate to **Elastic Beanstalk → Create Application**.
2. **Environment tier:** Web Server Environment (our application is a website). [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)
3. **Application name:** Give a meaningful name.
4. **Environment name:** This represents the deployment stage (dev, test, staging, production). One application can have multiple environments. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)
5. **Domain:** Enter a name (e.g., `vPro-re-arch`). This becomes the URL to access the application. **You must click "Check Availability"** — this domain must be globally unique. If it's taken, choose a different name. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)
6. **Platform:** Tomcat.
7. **Platform branch:** Tomcat 10, Corretto 21 (Java 21 with Tomcat 10). [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)
8. **Platform version:** Keep the recommended version.
9. **Application code:** Sample Application (we'll upload the real artifact later).
10. **Presets:** Custom Configuration (not Single Instance — we need load balancing and auto scaling). [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)
11. Click **Next**.

***

**3b — Service Access Configuration:**

1. **Service Role:** Select the `aws-elasticbeanstalk-service-role` (created/verified in Step 2).
2. **Instance Profile:** Select `vprofile-Rearch-bean-role` (created in Step 1).
3. **EC2 Key Pair:** Select your key pair (e.g., `vprofile-prod-key`). [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)
4. **Make sure you select all these options** — missing any of them (especially the instance profile) will cause permission failures later.
5. Click **Next**.

***

**3c — Networking:**

1. **VPC:** Select the default VPC. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)
2. **Instance settings → Public IP Address:** **Activate** this. The EC2 instances need public IPs to be accessible. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)
3. **Subnets:** Select all availability zones. (If you get an error later about an unavailable zone, come back and uncheck that specific zone.) [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)
4. **Database:** Do **NOT** select anything. The RDS database was created separately and is decoupled from Beanstalk. Beanstalk can create a coupled RDS instance, but this ties the database lifecycle to the environment lifecycle — not recommended. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)
5. **Tags:** Add a tag: Key = `Project`, Value = `vprofile`. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)
6. Click **Next**.

***

**3d — Instance Settings:**

1. **Root Volume:** ⚠️ **Change from "Container Default" to General Purpose 3 (GP3).** This is critical — container default causes Beanstalk to use the outdated Launch Configuration mechanism, which results in an error. GP3 forces the correct Launch Template mechanism. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)
2. **CloudWatch Monitoring:** Keep 5 minutes (free). One-minute monitoring is available but not free. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)
3. **Security Group:** Leave as-is — let Beanstalk create its own security group. You'll edit its rules later (to allow backend access). [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

***

**3e — Capacity:**

1. **Environment type:** Load Balanced (not Single Instance). This creates an ALB and an ASG. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)
2. **Minimum instances:** `2` — load balancer needs at least 2 for meaningful distribution, and we need 2+ to demonstrate deployment strategies.
3. **Maximum instances:** `4` (can be changed anytime). [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)
4. **Instance type:** Find and select **t2.micro** (free tier). Remove any other instance types that may be pre-selected (like t2.small). [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)
5. **Scaling triggers:** The defaults use CPU utilization or Network Out. Both are effective for web applications (see Theory 1.9 for the Network Out explanation). [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

***

**3f — Load Balancer:**

1. **Visibility:** Public (internet-facing). [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)
2. **All zones selected.**
3. **Load balancer type:** Application Load Balancer. (Network Load Balancer is high-performing with static IPs but expensive — not needed here.) [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)
4. **Listeners:** Port 80 (HTTP). Note: **In Beanstalk, Tomcat runs on port 80, not 8080** — this is different from the Lift and Shift project. The LB listens on 80 and routes to 80 on EC2. HTTPS (443) will be added later. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)
5. **Processes → Edit the default process:**
   * **Enable Stickiness.** Required for vProfile's local session authentication (same reason as the Lift and Shift project — see previous lecture's Theory 1.10).
   * **Save.** [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

***

**3g — Monitoring and Deployment:**

1. **Health reporting:** Set to **Enhanced**. Critical for deployment safety — Beanstalk checks instance health before proceeding to the next instance during rolling deployments. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)
2. **Updates:** Keep minor and patch updates enabled (or disable based on your project's change management policy). [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)
3. **Email notification:** Optionally provide an email address for environment change notifications. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)
4. **Deployment Policy:** Select **Rolling**. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)
5. **Batch size:** `50%`. With minimum 2 instances, this means 1 instance at a time. With maximum 4, it means 2 at a time. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)
6. **Environment properties:** Skip — not needed for this project. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

***

**3h — Review and Submit:**

1. Review all settings: instance profile role, service role, networking, security group, instance count, volume type (GP3!), deployment policy, stickiness.
2. Click **Submit**. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

**What happens internally:** Beanstalk begins provisioning all resources — EC2 instances, ALB, ASG, S3 bucket, CloudWatch alarms, security groups. This takes several minutes.

**How to verify:** The Beanstalk dashboard shows the environment being created. Once complete, the environment health should show green ("Ok"). You can navigate to EC2, Load Balancers, and Auto Scaling Groups in the AWS console to see the individual resources Beanstalk created. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

**Common mistakes:**

* Forgetting to select the instance profile role → instances lack permissions.
* Leaving "Container Default" volume → Launch Configuration error.
* Not activating public IP → instances unreachable.
* Not enabling stickiness → users get logged out on page refresh.
* Selecting a non-free-tier instance type → unexpected charges.

**Connection to flow:** After the environment is created and verified, the next step (in the following lecture) is to build the vProfile artifact with backend endpoint information and deploy it to this Beanstalk environment. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

⚠️ **Expert Note:**
The environment creation can fail for various reasons — unavailable availability zones, IAM permission issues, or resource limits. If creation fails, check the Beanstalk events log (in the environment dashboard) for the specific error. Beanstalk events are the primary debugging tool for environment-level issues. For the availability zone error specifically, go back to the networking step and uncheck the problematic zone. [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## System Identity

```
COMPONENT: Elastic Beanstalk Environment for vProfile
PURPOSE:   Managed frontend tier — replaces manual EC2 + ALB + ASG + S3 setup
CORE IDEA: One service gives you everything the Lift & Shift project required
           individually: instances, LB, ASG, S3, monitoring, deployment
COST:      Beanstalk itself = FREE. You pay only for underlying resources.
```

 [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

***

## Lift & Shift (Manual) → Beanstalk (Managed): What Gets Replaced

```
MANUAL (Lift & Shift)              →  BEANSTALK (Refactoring)
──────────────────────                ─────────────────────────
Create Security Group              →  Auto-created by Beanstalk
Create Key Pair                    →  Still manual (for SSH if needed)
Launch EC2 + Install Tomcat        →  Auto-provisioned (platform selection)
Create Target Group                →  Auto-created
Create ALB                         →  Auto-created
Create AMI                         →  Managed internally
Create Launch Template             →  Managed internally
Create ASG                         →  Auto-created (configurable)
S3 bucket for artifact             →  Auto-created
Build + S3 upload + manual deploy  →  One-click artifact upload
CloudWatch setup                   →  Auto-integrated
```

 [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

***

## Two IAM Roles (Distinct Purposes)

```
ROLE 1: Service Role (aws-elasticbeanstalk-service-role)
  WHO USES IT: Beanstalk service itself (management plane)
  WHAT IT DOES: Creates/manages EC2, ALB, ASG, etc.
  HOW CREATED: Via Beanstalk wizard "Create Role" button (auto-configured)

ROLE 2: Instance Profile (vprofile-Rearch-bean-role)
  WHO USES IT: EC2 instances launched by Beanstalk (data plane)
  WHAT IT DOES: S3 access, CloudWatch, SNS, platform operations
  HOW CREATED: Manually in IAM → EC2 use case → 4 policies:
    ├── AdministratorAccess-AWSElasticBeanstalk
    ├── AWSElasticBeanstalkCustomPlatformforEC2Role
    ├── AWSElasticBeanstalkRoleSNS
    └── AWSElasticBeanstalkWebTier

⚠️ Default Beanstalk-created instance role = INSUFFICIENT for this project
```

 [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

***

## Beanstalk Hierarchy

```
Beanstalk Application (project-level container)
  └── Environment 1 (dev)     ← full independent stack
  └── Environment 2 (staging) ← full independent stack
  └── Environment 3 (prod)    ← full independent stack

Each Environment =
  ├── EC2 instance(s) with Tomcat
  ├── Application Load Balancer
  ├── Auto Scaling Group
  ├── S3 bucket (artifacts)
  ├── CloudWatch alarms
  ├── Security groups (auto-created)
  └── Unique URL (must be globally unique)
```

 [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

***

## GP3 Volume Workaround (Critical)

```
Container Default → Launch Configuration (OUTDATED) → ERROR ❌
GP3               → Launch Template (CURRENT)        → WORKS ✅

RULE: Always select GP3 for root volume in Beanstalk.
```

 [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

***

## Port Difference: Beanstalk vs. Lift & Shift

```
Lift & Shift:  ALB (443) → Tomcat EC2 (8080)
Beanstalk:     ALB (80)  → Tomcat EC2 (80)    ← Beanstalk configures Tomcat on 80
               (later: ALB 443 HTTPS added)
```

 [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

***

## Deployment Policies: Speed ↔ Safety Spectrum

```
POLICY                        DOWNTIME  CAPACITY   COST      SAFETY   ROLLBACK
─────────────────────────────────────────────────────────────────────────────────
All at Once                   YES       0% (all    Cheapest  Lowest   Manual
                                        down)
Rolling                       NO        Reduced    Normal    Medium   Complex
                                        (batch %)
Rolling + Additional Batch    NO        Never      Higher    Good     Better
                                        reduced    (extra
                                                   instances)
Immutable                     NO        Never      Highest   Very     Easy
                                        reduced    (2x       High     (old set
                                                   instances)          intact)
Traffic Splitting (Canary)    NO        Never      High      Highest  Easiest
                                        reduced                       (% based)

PROJECT CHOICE: Rolling, 50% batch → min 2 = 1 at a time, max 4 = 2 at a time
```

 [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

***

## Decoupled RDS Decision

```
Coupled RDS (via Beanstalk):
  └── DB lifecycle TIED to environment lifecycle
  └── Delete environment → risk deleting DB ❌

Decoupled RDS (created separately):
  └── DB lifecycle INDEPENDENT
  └── Delete environment → DB persists ✅
  └── Used in this project
```

 [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

***

## Key Configuration Decisions Summary

```
Platform:        Tomcat 10 + Corretto 21 (Java 21)
App code:        Sample first → upload real artifact later
Preset:          Custom (load balanced, not single instance)
Public IP:       Activated ← required for accessibility
Volume:          GP3 ← avoids Launch Configuration error
Monitoring:      5 min (free) + Enhanced health reporting
LB type:         ALB (not NLB — cheaper, apt for HTTP)
Stickiness:      ON ← vProfile local session auth
Capacity:        min=2, max=4, t2.micro
Deployment:      Rolling, 50%
Database:        NOT created via Beanstalk (decoupled)
Env properties:  Not used
```

 [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

***

## Execution Dependency Chain

```
1. Create Instance Profile Role (IAM)     ← needed before Beanstalk
2. Verify/Create Service Role (IAM)       ← needed before Beanstalk
3. Create Beanstalk Environment            ← references both roles + key pair
     │
     ├── Auto-provisions: EC2, ALB, ASG, SG, S3, CloudWatch
     │
     ▼
4. [NEXT LECTURE] Build artifact → Deploy to Beanstalk (one-click)
```

 [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

***

## Reusable Engineering Patterns

| Pattern                                      | Manifestation                                                                                             |
| -------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| **Orchestration Layer**                      | Beanstalk = free automation layer over existing AWS resources                                             |
| **Management Plane / Data Plane Separation** | Service Role (manages infra) vs. Instance Profile (runs on infra)                                         |
| **Decoupled Stateful Services**              | RDS created independently — survives environment deletion                                                 |
| **Progressive Deployment Strategies**        | All-at-once → Rolling → Rolling+Batch → Immutable → Canary                                                |
| **Sample-First, Customize-Later**            | Deploy sample app → verify environment → deploy real artifact                                             |
| **Compatibility Workaround**                 | GP3 selection to force Launch Template over deprecated Launch Config                                      |
| **Environment-as-Unit**                      | Single Beanstalk environment = entire frontend stack (instances + LB + ASG + S3 + monitoring)             |
| **Multi-Environment Application**            | One application → multiple isolated environments (dev/staging/prod)                                       |
| **Enhanced Health Gating**                   | Enhanced monitoring gates deployment progression — won't proceed to next batch if current batch unhealthy |
| **Configuration Externalization**            | Environment properties allow runtime config without rebuilding artifact                                   |

 [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

***

## One-Line System Reconstruction

> **A Beanstalk environment replaces the entire Lift & Shift frontend (EC2 + ALB + ASG + S3 + CloudWatch) with a single managed unit using Tomcat 10/Corretto 21, two IAM roles (service role for management, instance profile for EC2), GP3 volumes (to avoid launch config errors), rolling deployment at 50%, enhanced health reporting for deployment gating, stickiness for session affinity, and a decoupled separately-managed RDS — all configurable and redeployable with one click.** [\[146-beanstalk \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/146-beanstalk.txt)

***

This completes the full reconstruction of the Beanstalk Environment Setup lecture. It connects directly to the Refactoring Introduction (previous lecture) — where the architecture was planned — and leads into the next lecture where the artifact is built and deployed. Let me know if you'd like any section expanded or adjusted! 🚀
