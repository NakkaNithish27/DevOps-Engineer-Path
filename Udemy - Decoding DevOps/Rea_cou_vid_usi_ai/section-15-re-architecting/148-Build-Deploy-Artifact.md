# 🧠 Build & Deploy Artifact — vprofile Re-Architected Application on AWS Beanstalk

**Source**: [148-build-and-deploy-artifact.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt?EntityRepresentationId=5b65e3b6-7820-4f21-ae31-2f891ad974f1) — Video caption reconstruction [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

***

# 🧠 SECTION 1: THEORY (DEEP LEARNING MODE)

## 1.1 The Build-and-Deploy Pipeline — What This Lecture Achieves

At this stage in the re-architected vprofile project, all backend managed services already exist: **Amazon RDS** (MySQL), **Amazon MQ** (RabbitMQ), and **ElastiCache** (Memcached). An Elastic Beanstalk environment is also running with Tomcat instances behind a load balancer. What is missing is the **application artifact** — the compiled `.war` file that Beanstalk needs to actually serve the vprofile application. This lecture bridges the gap between "infrastructure exists" and "application is live" by building the source code locally, injecting real backend connection details into it, and deploying the resulting artifact to Beanstalk. [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

The fundamental concept here is that the application source code contains a **configuration file** (`application.properties`) that holds placeholder hostnames for backend services (like `db01`, `rmq01`). In the local Vagrant setup, those hostnames resolved via local DNS. In AWS, those hostnames must be replaced with the **actual AWS service endpoints** — the RDS endpoint, the Amazon MQ broker URL, the ElastiCache configuration endpoint. Without this replacement, the application will deploy successfully but fail to connect to any backend service. [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

***

## 1.2 The application.properties File — The Application's Service Registry

The file `src/main/resources/application.properties` is the single configuration file where the vprofile Java application looks up all its backend connection details. It contains entries for:

* **Database**: connection URL (protocol + hostname + port), username, password
* **Memcached**: endpoint hostname, port (11211)
* **RabbitMQ**: endpoint hostname, port, username, password

In the source code repository, these values contain **local hostnames** (like `db01`, `rmq01`) from the Vagrant-based local setup. For the AWS re-architected deployment, every local hostname must be replaced with the corresponding **AWS managed service endpoint**. The port numbers may also differ — notably, Amazon MQ uses port **5671** while the original local RabbitMQ configuration uses **5672**. Missing this single-digit difference will cause the RabbitMQ connection to fail silently. [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

The structure of the database URL follows the pattern: `mysql://<RDS_ENDPOINT>:3306`. The Memcached entry uses the ElastiCache configuration endpoint with port 11211. The RabbitMQ entry uses the Amazon MQ broker URL (the portion after `//` in the connection string) with port 5671. [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

⚠️ **Expert Note**: Any mistake in this file — a wrong endpoint, a typo in the password, a wrong port number — will result in the application deploying and running (Tomcat starts fine) but failing at runtime when it tries to reach backend services. The symptom is a deployed application that loads the login page but cannot authenticate users (DB unreachable) or cache data (Memcached unreachable). The fix cycle is: correct the file → rebuild the artifact → redeploy. This makes careful copy-pasting and verification critical before building. [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

***

## 1.3 The Build Process — Maven and the .war Artifact

The vprofile application is a Java web application built with **Apache Maven**. The build command `mvn install` compiles the source code, runs any tests, and packages everything into a **`.war` file** (Web Application Archive) — specifically `vprofile-v2.war`, located in the `target/` folder after a successful build. [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

The build has strict version requirements: **Maven 3.9.9** and **Java 17 or higher**. If different versions are installed, the build may fail or produce an incompatible artifact. On Windows, **Chocolatey** (`choco uninstall` / `choco install`) is used to manage versions. On MacBook, **Brew** is used. The instructor references a separate software installation lecture in the prerequisites for exact commands. [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

The build happens **locally on your machine** — not on any AWS instance. This is a deliberate architectural choice: you build locally, then upload the artifact to Beanstalk. This separates the build environment from the runtime environment, which is a standard CI/CD pattern even though here it is done manually. [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

🔍 **Deep Dive**: The `mvn install` command does more than just compile. It executes the full Maven lifecycle: validate → compile → test → package → verify → install. The `install` phase also places the artifact in the local Maven repository (`~/.m2/repository`), but for this use case, the important output is the `.war` file in `target/`. If the build fails, the `target/` folder will either be missing or contain no `.war` file — that is the first verification point.

***

## 1.4 Elastic Beanstalk Deployment — Upload and Deploy Mechanism

Beanstalk provides a direct **"Upload and deploy"** button in the environment console. You select the `.war` file from your local machine, give it a **version label** (a human-readable identifier like `vprofile-rearch-beanapp-version-1.9`), and click Deploy. Beanstalk handles the rest — uploading the artifact to S3 internally, distributing it to instances, and managing the deployment process. [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

The version label is for your tracking purposes — it can be any string. The instructor uses a descriptive name with a version number, but notes it is "just some random number." In production, this would follow a versioning convention tied to your CI/CD pipeline. [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

***

## 1.5 Rolling Deployment — How Beanstalk Updates Multiple Instances

The Beanstalk environment in this project has **two instances** behind the load balancer, and the deployment policy is configured as **rolling with a 50% batch size**. This means Beanstalk deploys to **one instance at a time** (50% of 2 = 1). [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

The deployment flow operates through the **target group health check** mechanism:

1. Beanstalk selects the first batch (Instance 1) and begins deploying the new artifact to it
2. During deployment, Instance 1 becomes **unhealthy** in the target group (it's being updated)
3. The load balancer **drains** Instance 1 — it stops sending new traffic to it while existing connections finish
4. Once Instance 1's deployment completes and the instance passes the health check (becomes **healthy**), Beanstalk proceeds to the next batch
5. Instance 2 goes through the same cycle

This ensures **zero-downtime deployment** — at any point during the process, at least one instance is healthy and serving traffic. The "draining" state visible in the Target Groups console is the observable evidence of this mechanism in action. [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

The Events tab in the Beanstalk console shows real-time progress: "Batch 1, starting application deployment" with the specific instance ID, followed by batch 2. This is the monitoring surface for deployment progress. [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

🔍 **Deep Dive**: The deployment policy can be changed at the time of deployment as well (not just in environment configuration). The instructor shows the deployment preference options during the upload step but keeps the existing rolling/50% configuration. Other policies include "All at once" (faster but causes downtime), "Rolling with additional batch" (spins up extra instances to maintain full capacity), and "Immutable" (creates entirely new instances, swaps, then terminates old ones).

***

## 1.6 HTTPS with ACM Certificate — Securing the Connection

After successful deployment, the application is accessible via the Beanstalk URL on HTTP, but the browser shows **"Not secure."** To enable HTTPS, two things are needed:

1. **An ACM (AWS Certificate Manager) certificate** — this must already exist (created in a previous lecture). It is a TLS/SSL certificate for your domain.
2. **An HTTPS listener on the load balancer** — Beanstalk's load balancer initially only has an HTTP (port 80) listener. You must add an HTTPS (port 443) listener and attach the ACM certificate to it.

The HTTPS listener is added through Beanstalk's **Configuration → Instance traffic and scaling → Load balancer settings → Listeners**. You add a new listener with protocol HTTPS, port 443, select the ACM certificate (e.g., `hkhinfoteck.xyz`), and choose an SSL policy (e.g., `2021-06`). After saving, you must click **Apply** — saving alone does not trigger the change. Beanstalk then modifies the load balancer and target group to support the new listener. [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

⚠️ **Expert Note**: If you have not purchased a domain and don't have an ACM certificate, you can still verify the application fully over HTTP — login, database connectivity, and caching all work the same way. HTTPS is about transport security, not application functionality. The instructor explicitly offers this as an alternative path. [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

***

## 1.7 Custom Domain with CNAME Record

To access the application via a friendly URL (like `vprorearch.hkhinfoteck.xyz`) instead of the long Beanstalk-generated URL, a **CNAME DNS record** is created in the domain registrar (GoDaddy in this case). A CNAME maps a name to another name — it maps your custom subdomain to the Beanstalk endpoint URL. [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

| DNS Record Type | Name         | Value                     |
| --------------- | ------------ | ------------------------- |
| **CNAME**       | `vprorearch` | Beanstalk environment URL |

After saving the record, DNS propagation takes some time. Once propagated, `https://vprorearch.hkhinfoteck.xyz` resolves to the Beanstalk load balancer, the ACM certificate validates the connection, and the browser shows a secure padlock. [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

***

## 1.8 End-to-End Verification — What a Successful Deployment Proves

The verification sequence after deployment confirms the entire stack is working:

1. **Login page loads** → Tomcat is serving the application artifact correctly
2. **Login succeeds** (username: `admin_vp`, password: `admin_vp`) → **RDS MySQL connectivity is verified** — the application authenticated against the `accounts` database
3. **User data pages load** → Database read operations work
4. **Memcached verification page** → Shows "Data is inserted in cache" → **ElastiCache connectivity is verified**

Each verification step implicitly tests a different backend service connection configured in `application.properties`. If login fails, the database configuration is wrong. If caching fails, the Memcached configuration is wrong. The RabbitMQ connection is not explicitly tested in this verification but would manifest in message-dependent features. [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

***

## 1.9 Where This Fits — The Bigger Picture

This lecture completes the application deployment for the re-architected vprofile project. All AWS managed services (RDS, ElastiCache, Amazon MQ) are now connected and verified. The next lecture introduces **Amazon CloudFront** — a CDN service that distributes traffic globally, allowing a global audience to access the application regardless of which AWS region hosts the servers. [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (GUIDED EXECUTION MODE)

## What We Are Building

We are building the vprofile Java application artifact locally, injecting real AWS backend service endpoints into its configuration, deploying it to an existing Elastic Beanstalk environment, adding HTTPS via ACM certificate, mapping a custom domain, and verifying the entire application stack end-to-end. The final outcome: the vprofile application is live, secure (HTTPS), accessible via a custom domain, and connected to all AWS managed backend services. [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

***

## Step 1: Collect All Backend Service Information

Before touching any code, gather every piece of connection information from the AWS console. You will need all of these to edit `application.properties`.

### 1a. RDS Endpoint

Go to **Amazon RDS** → select your RDS instance → copy the **Endpoint** (the hostname). You should already have the **username** (`admin`) and **password** (saved during RDS creation) in your sticky notes. [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

### 1b. Amazon MQ (RabbitMQ) Broker URL

Go to **Amazon MQ** → select your broker → scroll to **Connections** → find the URL. Copy **only the part after `//`** (the hostname portion). [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

**Critical**: Note the port number — it is **5671**, not 5672. The `application.properties` file has 5672 by default (from local setup). You **must** change this to 5671. [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

Also confirm your RabbitMQ credentials. The instructor used username `rabbit` with a password set during broker creation. [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

### 1c. ElastiCache (Memcached) Endpoint

Go to **ElastiCache** → **Resources** → **Memcached caches** → select your cache → copy the **Configuration endpoint**. Verify port **11211** is present — this matches the default in the application configuration, so no port change is needed. [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

### Summary of Collected Information

Save all of these in a sticky note or text file:

```
RDS Endpoint:        <your-rds-endpoint>
RDS Username:        admin
RDS Password:        <your-saved-password>
RDS Port:            3306

MQ Endpoint:         <broker-hostname-after-//>
MQ Port:             5671  ← NOT 5672
MQ Username:         rabbit
MQ Password:         <your-saved-password>

ElastiCache Endpoint: <your-cache-endpoint>
ElastiCache Port:     11211
```

**Connection to system flow**: These values will be injected into the source code configuration before building. [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

***

## Step 2: Clone the Source Code

Go to `github.com/hkhcoder/vprofile-project` → copy the **HTTPS** URL.

Open **VSCode** → click **Source Control** (sidebar) → **Clone Repository** → paste the URL → hit Enter → select destination folder (e.g., `F:\hkhcoder`). If an old clone exists, delete it first. [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

**Switch to the correct branch**: Click the branch indicator in VSCode's bottom bar → select **`awsrefactor`** (all lowercase, one word). This branch contains the code compatible with the re-architected AWS setup. [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

⚠️ This is a **different branch** from the lift-and-shift project (`aws-lift-and-shift`). Using the wrong branch will produce an artifact that doesn't work with the managed services architecture.

***

## Step 3: Edit application.properties

Navigate in VSCode to: **`src/main/resources/application.properties`** [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

Make the following replacements carefully:

### Database Section

Replace the existing `db01` hostname with the RDS endpoint:

```
jdbc.url=jdbc:mysql://<RDS_ENDPOINT>:3306/accounts
jdbc.username=admin
jdbc.password=<YOUR_RDS_PASSWORD>
```

* The format is `mysql://` followed by the endpoint, then `:3306`
* Username and password must match what was set during RDS creation [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

### Memcached Section

Replace the existing hostname with the ElastiCache configuration endpoint:

```
memcached.active.host=<ELASTICACHE_ENDPOINT>
memcached.active.port=11211
```

* Port 11211 is already correct — no change needed [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

### RabbitMQ Section

Replace the existing `rmq01` hostname with the Amazon MQ broker hostname:

```
rabbitmq.address=<AMAZON_MQ_HOSTNAME>
rabbitmq.port=5671
rabbitmq.username=rabbit
rabbitmq.password=<YOUR_MQ_PASSWORD>
```

* **Port must be changed from 5672 to 5671** — this is the most commonly missed detail [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

**After all edits**: Review the file one more time. Verify each endpoint is in the correct field. A single wrong value means the application will deploy but fail at runtime, requiring you to fix, rebuild, and redeploy.

Save the file: **Ctrl + S**. [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

**Connection to system flow**: The application will read these values at runtime to connect to backend services. This is the only configuration step — everything else is build and deploy. [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

***

## Step 4: Set Up the Terminal in VSCode

Press **Ctrl + Shift + P** → type `default profile` → select **Terminal: Select Default Profile**. [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

* On **Windows**: select **Git Bash**
* On **MacBook**: select **Terminal** (the default macOS terminal)

Then open the terminal: **View → Terminal**. The terminal should open at the repository root path, showing the `awsrefactor` branch. [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

***

## Step 5: Verify Build Tool Versions

Run:

```bash
mvn -version
```

* **`mvn`** — invokes Maven
* **`-version`** — prints version information for Maven and the JDK it's using

**Expected output**:

* Maven version: **3.9.9**
* Java version: **17 or higher**

If versions are different: [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

* **Windows**: use `choco uninstall <package>` then `choco install <package>` with the correct version. Check the software installation lecture for exact commands.
* **MacBook**: use **Brew**. Same lecture reference.

⚠️ **Expert Note**: Version mismatches are a common silent failure. The build might succeed with a different Java version but produce a `.war` file that doesn't run correctly on the Beanstalk Tomcat environment (which expects Java 17 compatibility). Always verify before building. [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

***

## Step 6: Build the Artifact

Run:

```bash
mvn install
```

* **`mvn`** — invokes the Maven build tool
* **`install`** — executes the full Maven build lifecycle (compile → test → package → install)

**What happens internally**: Maven reads `pom.xml`, resolves dependencies, compiles all Java source files, runs unit tests, packages the compiled code and resources (including your edited `application.properties`) into a `.war` file, and places it in the `target/` directory. [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

**Expected result**: Build ends with `BUILD SUCCESS`. Two verification points:

1. A `target/` folder appears in the project root
2. Inside it: **`vprofile-v2.war`** — this is the deployable artifact [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

If the build fails, check: Maven version, Java version, internet connectivity (Maven downloads dependencies), and any syntax errors if you accidentally modified source files.

**Connection to system flow**: This `.war` file is what gets uploaded to Beanstalk next. [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

***

## Step 7: Deploy the Artifact to Elastic Beanstalk

Go to **Elastic Beanstalk** in the AWS console → select your environment.

Click **Upload and deploy** → **Choose file** → navigate to your project's `target/` folder → select **`vprofile-v2.war`**. [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

In the **Version label** field, enter a descriptive label:

```
vprofile-rearch-beanapp-version-1.9
```

(Any descriptive string works — this is for your tracking.) [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

**Deployment preferences** will show your configured policy (rolling, 50% batch size). You can change this at deploy time if needed, but keep the defaults.

Click **Deploy**. [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

**What happens internally**: Beanstalk uploads the `.war` to S3, then initiates a rolling deployment. With 2 instances and 50% batch size:

1. **Batch 1**: Beanstalk deploys to Instance 1 → Instance 1 goes unhealthy (draining state in Target Group) → load balancer routes all traffic to Instance 2
2. Instance 1 deployment completes → health check passes → Instance 1 becomes healthy
3. **Batch 2**: Same process for Instance 2
4. Both instances healthy → deployment complete [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

**Monitoring deployment**:

* **Events tab** in Beanstalk console: shows "Batch 1, starting application deployment" with instance IDs, then batch 2
* **Target Groups** (EC2 console): shows instance states changing between healthy → draining → unhealthy → healthy

The deployment takes several minutes. Wait until the Events tab shows **"Application update completed."** The environment health should return to **OK (green)**. [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

***

## Step 8: Verify Basic Deployment

Click the **Beanstalk environment URL** (displayed at the top of the environment page). The vprofile **login page** should load. At this point the connection is HTTP (browser shows "Not secure"). [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

If you do not have a domain/ACM certificate, you can perform full verification now:

* Login with **`admin_vp`** / **`admin_vp`** → verifies RDS connectivity
* Check Memcached page → should show "Data is inserted in cache" → verifies ElastiCache connectivity [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

If login fails → the `application.properties` database section has an error. Fix it, rebuild (`mvn install`), and redeploy.

***

## Step 9: Add HTTPS Listener (Requires Domain + ACM Certificate)

Go to **Beanstalk → Configuration** → scroll to **Instance traffic and scaling** → click **Edit** → scroll to **Load balancer settings → Listeners**. [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

Click **Add listener**:

| Field               | Value                                                 |
| ------------------- | ----------------------------------------------------- |
| **Protocol**        | HTTPS                                                 |
| **Port**            | 443 (type manually if not auto-populated)             |
| **SSL certificate** | Select your ACM certificate (e.g., `hkhinfoteck.xyz`) |
| **SSL policy**      | `2021-06` (or current recommended)                    |

Click **Save**, then **Apply** (saving without applying does nothing — this is a two-step commit). [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

Beanstalk will update the load balancer and target group configuration. This takes a few minutes. [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

**Connection to system flow**: The load balancer now accepts HTTPS traffic on 443 and terminates TLS using the ACM certificate. [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

***

## Step 10: Create CNAME Record for Custom Domain

Copy the **Beanstalk environment URL** (the long auto-generated hostname).

Go to your **domain registrar** (GoDaddy or equivalent) → manage DNS for your domain → **Add New Record**: [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

| Field     | Value                                           |
| --------- | ----------------------------------------------- |
| **Type**  | CNAME                                           |
| **Name**  | `vprorearch` (or any subdomain name you choose) |
| **Value** | The Beanstalk environment URL                   |

Click **Save**. [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

DNS propagation takes some time (minutes to hours depending on TTL).

**Connection to system flow**: After propagation, `https://vprorearch.<yourdomain>` → CNAME resolves to Beanstalk URL → load balancer → HTTPS with ACM certificate → application. [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

***

## Step 11: Full Verification Over HTTPS

After DNS propagation, access:

```
https://vprorearch.<yourdomain>
```

**Verification checklist**:

| Check                                         | What It Proves                  | Expected Result                 |
| --------------------------------------------- | ------------------------------- | ------------------------------- |
| Browser padlock icon → "Connection is secure" | HTTPS + ACM certificate working | Secure, valid certificate shown |
| Login page loads                              | Tomcat serving artifact         | vprofile login form visible     |
| Login with `admin_vp` / `admin_vp`            | **RDS MySQL connected**         | User dashboard loads            |
| Browse user data pages                        | Database reads working          | Data visible                    |
| Memcached verification page                   | **ElastiCache connected**       | "Data is inserted in cache"     |

 [\[148-build-...y-artifact \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/148-build-and-deploy-artifact.txt)

If any check fails, trace backward: HTTPS issue → check listener/certificate. Login fails → check `application.properties` DB section. Cache fails → check Memcached endpoint/port. Fix → rebuild → redeploy.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

## End-to-End Flow

```
Collect endpoints → Edit config → Build artifact → Deploy to Beanstalk → Add HTTPS → Map domain → Verify
```

## Backend Service Information Collection Map

```
RDS       → Endpoint hostname + port 3306 + admin/<password>
Amazon MQ → Broker URL (after //) + port 5671 ← NOT 5672 + rabbit/<password>
ElastiCache → Configuration endpoint + port 11211 (no change)
```

## Configuration File: application.properties

```
Location: src/main/resources/application.properties
Branch:   awsrefactor (NOT aws-lift-and-shift)

Replacements:
  db01  → RDS endpoint         | port 3306 (same)
  rmq01 → Amazon MQ hostname   | port 5672 → 5671 ← CHANGE
  mc01  → ElastiCache endpoint  | port 11211 (same)
  
+ Update credentials for DB and MQ
```

## Port Trap

```
Local setup RabbitMQ: 5672
Amazon MQ:            5671  ← off-by-one, silent connection failure
Memcached:            11211 (same in both environments)
MySQL:                3306  (same in both environments)
```

## Build Chain

```
Prerequisites:
  Maven 3.9.9 + Java 17+
  Windows: Chocolatey | Mac: Brew

Verify:  mvn -version
Build:   mvn install
Output:  target/vprofile-v2.war

Build fails? → Check versions, internet, pom.xml
```

## Deployment Mechanism

```
Beanstalk Console → Upload and deploy → Choose .war → Version label → Deploy

Policy: Rolling, 50% batch
2 instances → 1 at a time

Deployment state flow (per instance):
  Healthy → Draining → Unhealthy (deploying) → Healthy

Monitoring:
  Beanstalk Events tab: batch progress + instance IDs
  Target Groups:        health state transitions

Zero-downtime: at least 1 instance always healthy
```

## HTTPS Setup Chain

```
Prerequisite: ACM certificate (from earlier lecture) + purchased domain

Beanstalk → Configuration → Instance traffic and scaling → Edit
  → Load balancer listeners → Add listener
    Protocol: HTTPS | Port: 443 | Certificate: ACM | Policy: 2021-06
  → Save → Apply (both steps required!)
```

## Custom Domain Chain

```
Domain registrar (GoDaddy etc.) → Manage DNS → Add Record
  Type: CNAME
  Name: vprorearch (subdomain)
  Value: Beanstalk environment URL

Result: https://vprorearch.<domain> → Beanstalk LB → HTTPS → App
```

## Verification → Backend Service Proof Map

```
Login page loads        → Tomcat + artifact OK
Login succeeds          → RDS MySQL connected ✓
Data pages render       → DB reads work ✓
"Data inserted in cache"→ ElastiCache Memcached connected ✓
Padlock + "secure"      → HTTPS + ACM certificate ✓
```

## Fix-Rebuild-Redeploy Cycle

```
Backend connection failure?
  → Fix application.properties
  → mvn install (rebuild)
  → Upload and deploy (redeploy)
  → Re-verify
```

## Architecture Position

```
                    [CloudFront] ← next lecture
                         │
                    [Custom Domain CNAME]
                         │
                    [Load Balancer]
                    HTTPS:443 + ACM cert
                     /          \
               [Instance 1]  [Instance 2]   ← Beanstalk (Tomcat)
                     │
              application.properties
              /        |          \
         [RDS]    [ElastiCache]  [Amazon MQ]
         MySQL     Memcached     RabbitMQ
         :3306     :11211        :5671
```

## Reusable Engineering Patterns

```
1. CONFIG INJECTION BEFORE BUILD
   Edit config → Build → Deploy
   Config is baked into the artifact at build time
   Pattern: connection details injected at the source level, not at runtime

2. ROLLING DEPLOYMENT WITH HEALTH-GATE
   Deploy batch → wait for healthy → next batch
   Health check = gate between batches
   Pattern: health-aware sequential rollout

3. DRAIN-BEFORE-REPLACE
   Load balancer drains instance → then deployment proceeds
   Pattern: graceful traffic removal before state change

4. OBSERVATION SURFACE SEPARATION
   Events tab = deployment progress (application layer)
   Target Groups = instance health (infrastructure layer)
   Pattern: monitor both layers to understand full deployment state

5. ENDPOINT COLLECTION → CONFIGURATION → BUILD → DEPLOY
   Gather managed service outputs → inject into app config → compile → ship
   Pattern: managed service endpoints are dynamic inputs to application config

6. SAVE + APPLY TWO-STEP COMMIT
   Saving config ≠ applying config (Beanstalk)
   Pattern: staged commit in managed platforms — prepare then execute

7. VERIFICATION-BY-FEATURE
   Each app feature implicitly tests a different backend service
   Login = DB | Cache page = Memcached | Padlock = HTTPS
   Pattern: functional verification as infrastructure validation
```

## What Comes Next

```
This lecture: Artifact deployed + HTTPS + domain + verified
Next lecture: Amazon CloudFront (CDN) → global traffic distribution
  "Does not matter where you host your servers... use CloudFront 
   to deliver your services around the world"
```

***

That completes the full reconstruction of the build-and-deploy artifact lecture. The entire vprofile re-architected stack is now live and verified. Would you like me to generate Anki flashcards from this material, or run a fill-in-the-blank recall test? 🚀
