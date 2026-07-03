# 🎓 Deep Learning Material: AWS Application Load Balancer & DNS Configuration

**Source:** [137. Load Balancer & DNS.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/137.%20Load%20Balancer%20%26%20DNS.txt?EntityRepresentationId=6f6b5c7e-f861-43c2-a638-1bc392054c0f) — Video caption reconstruction covering AWS Application Load Balancer creation, Target Group setup, HTTPS with ACM certificates, GoDaddy DNS CNAME mapping, health check verification, and end-to-end service validation for a multi-tier vProfile application stack. [\[137. Load...ncer & DNS \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/137.%20Load%20Balancer%20%26%20DNS.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 Why a Load Balancer Exists in This Architecture

At this point in the project, multiple backend services have already been installed and configured — Tomcat (application server), MySQL (database), RabbitMQ (message broker), and Memcache (caching layer). Each service runs on its own EC2 instance. The Tomcat instance (app01) serves the vProfile web application on port 8080. A user *could* access this application directly by hitting the instance's public IP on port 8080. The video even demonstrates this — navigating to `http://<app01-public-ip>:8080` and getting the login page.

But this direct-access model has serious problems. The instance IP can change. There is no SSL/TLS encryption. There is no way to distribute traffic across multiple instances if you scale horizontally. There is no health-aware routing — if the instance goes down, there is no mechanism to detect that and redirect. The load balancer solves all of these problems by becoming the **single stable entry point** between the outside world and the backend application tier. Users never talk to instances directly. They talk to the load balancer, and the load balancer routes to healthy instances. [\[137. Load...ncer & DNS \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/137.%20Load%20Balancer%20%26%20DNS.txt)

***

## 1.2 The Target Group Concept

Before you create a load balancer, AWS requires you to define **where** the load balancer should send traffic. This destination is called a **Target Group**. A target group is a logical collection of targets (in this case, EC2 instances) that receive traffic from the load balancer.

The critical configuration detail is the **port number on the target group**. The load balancer listens on its own ports (80, 443), but the *targets* (instances) may run services on completely different ports. Here, Tomcat runs on port **8080**, not port 80. So the target group must be configured with protocol HTTP and port **8080**. This tells the load balancer: "When you forward traffic to these instances, send it to port 8080." [\[137. Load...ncer & DNS \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/137.%20Load%20Balancer%20%26%20DNS.txt)

The target group also contains a **health check** configuration. The health check is the mechanism by which the load balancer continuously verifies whether each registered instance is actually capable of serving traffic. By default, the health check assumes port 80. Since Tomcat runs on 8080, you must **override** the health check port to 8080 as well. This is done under "Advanced health check settings." If you miss this, the load balancer will probe port 80, get no response, and mark the instance as **unhealthy** — meaning it will never route traffic there, even though Tomcat is perfectly functional. [\[137. Load...ncer & DNS \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/137.%20Load%20Balancer%20%26%20DNS.txt)

There is a third place where port 8080 must be specified: when you register the actual instance into the target group. On the registration screen, after selecting app01, you must confirm the port is 8080 before clicking "Include as pending below." So port 8080 appears in **three distinct places** during target group creation: the target group port, the health check override, and the instance registration port. Missing any one of them breaks the routing chain. [\[137. Load...ncer & DNS \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/137.%20Load%20Balancer%20%26%20DNS.txt)

🔍 **Deep Dive**
The health check is not instantaneous. AWS performs **multiple consecutive health checks** before transitioning a target's status from "unhealthy" to "healthy" (or vice versa). This means that even after everything is configured correctly, you must wait and refresh the console. The target will initially show as "initial" or "unhealthy" and only transition to "healthy" after passing the required number of consecutive checks (controlled by the healthy threshold setting). This prevents flapping — rapidly toggling between healthy and unhealthy due to transient network issues. [\[137. Load...ncer & DNS \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/137.%20Load%20Balancer%20%26%20DNS.txt)

***

## 1.3 Application Load Balancer (ALB) — Listeners, Routing, and Security Groups

The Application Load Balancer (ALB) is specifically designed for HTTP and HTTPS traffic. It operates at Layer 7 (application layer), which means it understands HTTP headers, paths, and hostnames — though in this project, we use simple forwarding without advanced routing rules.

The ALB is configured with **listeners**. A listener defines what port and protocol the load balancer accepts incoming connections on. In this setup, two listeners are created:

* **HTTP on port 80** — for unencrypted traffic.
* **HTTPS on port 443** — for encrypted traffic (requires a certificate).

Both listeners route to the **same target group** (vprofile-las-tg). This means regardless of whether the user connects via HTTP or HTTPS, the load balancer forwards the request to Tomcat on port 8080 on the backend instance. The encryption terminates at the load balancer (this is called **SSL termination** — an implicit concept in this video). The connection between the load balancer and the instance is plain HTTP on 8080. [\[137. Load...ncer & DNS \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/137.%20Load%20Balancer%20%26%20DNS.txt)

The ALB must be placed in a **VPC** and mapped to **all available availability zones**. This ensures the load balancer can route traffic to instances in any AZ, providing resilience. The ALB also requires a **security group**. The default security group is removed and replaced with a purpose-built load balancer security group (created in a previous lecture). This security group controls what traffic can reach the load balancer itself (typically port 80 and 443 from the internet). [\[137. Load...ncer & DNS \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/137.%20Load%20Balancer%20%26%20DNS.txt)

⚠️ **Expert Note**
The security group chain is critical: the load balancer security group allows inbound 80/443 from the internet. The application instance security group (app01) allows inbound 8080 **from the load balancer security group** — not from the internet. This creates a layered security model where the instance is never directly exposed. The temporary rule added for testing (8080 from "my IP") should be removed after verification. [\[137. Load...ncer & DNS \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/137.%20Load%20Balancer%20%26%20DNS.txt)

***

## 1.4 HTTPS and the ACM Certificate

HTTPS requires a **TLS/SSL certificate** that proves the server's identity to the browser. AWS provides these certificates for free through **AWS Certificate Manager (ACM)**. However, the ACM certificate must match the domain name you intend to use. In this video, the domain is `hkhinfoteck.xyz`, purchased from GoDaddy. The ACM certificate was created in a prerequisites lecture to cover this domain.

When you add an HTTPS listener (port 443) on the ALB, AWS requires you to attach a certificate. Under "Default SSL/TLS certificate," you select "From ACM," and a dropdown shows all available certificates. You select the one matching your domain. Without this certificate, the HTTPS listener cannot be created. [\[137. Load...ncer & DNS \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/137.%20Load%20Balancer%20%26%20DNS.txt)

The video explicitly states that if you don't want to buy a domain, you can skip the HTTPS part entirely. You can still create the load balancer with only the HTTP listener on port 80 and access the application using the load balancer's DNS name directly. You just won't get encrypted connections. [\[137. Load...ncer & DNS \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/137.%20Load%20Balancer%20%26%20DNS.txt)

🔍 **Deep Dive**
After deployment, the video verifies the certificate by navigating to `https://vprofileapp.hkhinfoteck.xyz` and clicking the padlock icon in the browser. The certificate details show: issued **for** `hkhinfoteck.xyz`, issued **by** Amazon. This entire trust chain — domain ownership → ACM certificate → ALB HTTPS listener → browser trust — is what makes the connection show as "secure." The certificate information displayed in the browser is pulled from what ACM provisioned and what was attached to the load balancer. [\[137. Load...ncer & DNS \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/137.%20Load%20Balancer%20%26%20DNS.txt)

***

## 1.5 DNS — The CNAME Record and Domain-to-Load-Balancer Mapping

The load balancer, once created, receives an AWS-generated DNS name (endpoint). This is a long, ugly hostname like `vprofile-las-elb-xxxxxxx.us-east-1.elb.amazonaws.com`. No user should have to type this. The solution is **DNS mapping** — creating a human-friendly domain name that points to the load balancer endpoint.

This is done by creating a **CNAME record** in the domain's DNS settings. A CNAME (Canonical Name) record maps one domain name to another domain name. In GoDaddy's DNS management:

* **Type:** CNAME
* **Name:** `vprofileapp` (this becomes the subdomain, so the full URL is `vprofileapp.hkhinfoteck.xyz`)
* **Value:** the load balancer's DNS name (endpoint copied from the AWS console)

Once saved, when a user navigates to `vprofileapp.hkhinfoteck.xyz`, the DNS system resolves the CNAME to the load balancer endpoint, and the request reaches the ALB. Combined with the ACM certificate, this enables `https://vprofileapp.hkhinfoteck.xyz` with a trusted, secure connection. [\[137. Load...ncer & DNS \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/137.%20Load%20Balancer%20%26%20DNS.txt)

Users who did not purchase a domain can still access the application by directly pasting the load balancer endpoint URL into the browser. This works for HTTP but will not provide a valid HTTPS connection (the certificate won't match the AWS-generated hostname). [\[137. Load...ncer & DNS \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/137.%20Load%20Balancer%20%26%20DNS.txt)

***

## 1.6 End-to-End Service Verification Pattern

The video demonstrates a systematic verification of every tier in the multi-service stack through the web application itself:

**Database (MySQL):** Logging in with credentials `admin_vp` / same password. The login succeeds because user credentials are stored in MySQL. A successful login proves the Tomcat application can reach the MySQL database. [\[137. Load...ncer & DNS \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/137.%20Load%20Balancer%20%26%20DNS.txt)

**RabbitMQ:** After login, the application shows that a queue has been generated. This confirms the application's connection to the RabbitMQ message broker is functional. [\[137. Load...ncer & DNS \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/137.%20Load%20Balancer%20%26%20DNS.txt)

**Memcache:** Clicking "All Users" and selecting a user shows the message "data is from DB and data is inserted in cache." Going back and clicking the **same user again** shows "data is from cache." This proves two things — Memcache is reachable, and the caching logic is working correctly (first request fetches from DB and populates cache; second request serves from cache). [\[137. Load...ncer & DNS \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/137.%20Load%20Balancer%20%26%20DNS.txt)

This is not random clicking — it is a deliberate **service connectivity validation sequence**. Each action tests a different backend connection through the application layer.

***

## 1.7 The Autoscaling Foreshadow

The video closes by noting that while everything works, the architecture still lacks **automatic scaling**. If user load increases, there is currently only one Tomcat instance. The next lecture will cover **Auto Scaling Groups** — the mechanism to automatically launch additional instances and register them with the load balancer's target group when demand rises. The load balancer is already designed to handle multiple targets; autoscaling fills that capability. [\[137. Load...ncer & DNS \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/137.%20Load%20Balancer%20%26%20DNS.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are connecting an AWS Application Load Balancer to a running Tomcat instance, configuring it with both HTTP and HTTPS listeners, mapping a custom domain via DNS, and verifying end-to-end connectivity across all backend services (MySQL, RabbitMQ, Memcache). The final outcome: users access `https://vprofileapp.<yourdomain>` in a browser, hit the load balancer, get routed to Tomcat on port 8080, and interact with a fully functional multi-tier application — all through a secure, production-style entry point. [\[137. Load...ncer & DNS \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/137.%20Load%20Balancer%20%26%20DNS.txt)

***

## Step 1: Verify Tomcat Is Responding (Pre-Check)

Before building any load balancer infrastructure, confirm the application actually works.

**1a. Add a temporary security group rule:**

Navigate to **EC2 → Security Groups → app01 security group → Edit Inbound Rules**.

The security group already has a rule allowing port 8080 from the load balancer security group. Add one more rule:

| Type       | Port | Source |
| ---------- | ---- | ------ |
| Custom TCP | 8080 | My IP  |

Click **Save rules**. [\[137. Load...ncer & DNS \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/137.%20Load%20Balancer%20%26%20DNS.txt)

**1b. Access Tomcat directly:**

Copy the **public IP** of the app01 instance. Open a browser and navigate to:

```
http://<app01-public-ip>:8080
```

You should see the vProfile login page. This confirms Tomcat is running and the application is deployed. [\[137. Load...ncer & DNS \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/137.%20Load%20Balancer%20%26%20DNS.txt)

**1c. Understand this is temporary:**

This direct access is only for testing. In the production flow, users will never hit this IP directly. After confirming, you can close this tab. The temporary "My IP" rule should ideally be removed later. [\[137. Load...ncer & DNS \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/137.%20Load%20Balancer%20%26%20DNS.txt)

***

## Step 2: Create the Target Group

Navigate to **EC2 → Load Balancing → Target Groups → Create target group**.

**2a. Choose target type:**

Select **Instances**. [\[137. Load...ncer & DNS \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/137.%20Load%20Balancer%20%26%20DNS.txt)

**2b. Configure target group basics:**

| Setting           | Value             |
| ----------------- | ----------------- |
| Target group name | `vprofile-las-tg` |
| Protocol          | HTTP              |
| Port              | **8080**          |

The port is 8080 because that is where Tomcat listens — not the default 80. [\[137. Load...ncer & DNS \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/137.%20Load%20Balancer%20%26%20DNS.txt)

**2c. Configure health check:**

Scroll down to **Health checks**. Expand **Advanced health check settings**.

Override the health check port: change from "traffic port" (or default 80) to **8080**.

This ensures the load balancer probes port 8080 when checking instance health. If left at 80, the health check will fail because nothing listens on port 80 on the instance. [\[137. Load...ncer & DNS \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/137.%20Load%20Balancer%20%26%20DNS.txt)

**2d. Register the instance:**

Click **Next**. On the registration screen:

1. Find **app01** in the instance list.
2. Put a **check mark** on it.
3. Confirm the port field shows **8080**.
4. Click **"Include as pending below."**

Verify that the "Review targets" section at the bottom shows: `app01`, port `8080`. If it shows a different port or a different instance, remove it and re-add correctly. [\[137. Load...ncer & DNS \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/137.%20Load%20Balancer%20%26%20DNS.txt)

**2e. Finalize:**

Click **Create target group**.

**Connection to larger flow:** The target group is now ready to receive traffic from the load balancer. The ALB will reference this target group in its listener configuration. [\[137. Load...ncer & DNS \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/137.%20Load%20Balancer%20%26%20DNS.txt)

***

## Step 3: Create the Application Load Balancer

Navigate to **EC2 → Load Balancing → Load Balancers → Create Load Balancer**.

**3a. Select load balancer type:**

Choose **Application Load Balancer** (for HTTP/HTTPS traffic). Click **Create**. [\[137. Load...ncer & DNS \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/137.%20Load%20Balancer%20%26%20DNS.txt)

**3b. Basic configuration:**

| Setting            | Value              |
| ------------------ | ------------------ |
| Load balancer name | `vprofile-las-elb` |

**3c. Network mapping:**

* Select the correct **VPC**.
* Select **all available Availability Zones**. This gives the ALB cross-AZ reach. [\[137. Load...ncer & DNS \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/137.%20Load%20Balancer%20%26%20DNS.txt)

**3d. Security group:**

* **Remove** the default security group.
* **Select** the load balancer security group created in the earlier security group lecture. [\[137. Load...ncer & DNS \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/137.%20Load%20Balancer%20%26%20DNS.txt)

**3e. Configure Listener 1 — HTTP:**

| Setting        | Value                        |
| -------------- | ---------------------------- |
| Protocol       | HTTP                         |
| Port           | 80                           |
| Default action | Forward to `vprofile-las-tg` |

This is set by default. [\[137. Load...ncer & DNS \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/137.%20Load%20Balancer%20%26%20DNS.txt)

**3f. Configure Listener 2 — HTTPS (optional, requires domain + ACM certificate):**

Click **"Add listener."**

| Setting        | Value                        |
| -------------- | ---------------------------- |
| Protocol       | HTTPS                        |
| Port           | 443 (auto-filled)            |
| Default action | Forward to `vprofile-las-tg` |

Scroll down to **"Default SSL/TLS certificate"**:

* Source: **From ACM**
* Select your certificate from the dropdown (e.g., `hkhinfoteck.xyz`).

If you don't have a domain or ACM certificate, skip this listener entirely. The load balancer will still work on port 80. [\[137. Load...ncer & DNS \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/137.%20Load%20Balancer%20%26%20DNS.txt)

**3g. Skip optional features:**

AWS WAF and Global Accelerator options appear. Skip these. [\[137. Load...ncer & DNS \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/137.%20Load%20Balancer%20%26%20DNS.txt)

**3h. Finalize:**

Click **Create load balancer**.

The load balancer status will show **"Provisioning"**. This takes a few minutes to transition to **"Active."** [\[137. Load...ncer & DNS \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/137.%20Load%20Balancer%20%26%20DNS.txt)

**Connection to larger flow:** The ALB is now the front door. It listens on 80/443, terminates SSL, and forwards to Tomcat on 8080 via the target group.

***

## Step 4: Configure DNS (CNAME Record in GoDaddy)

*Skip this step if you don't own a domain.*

**4a. Copy the load balancer DNS name:**

In the AWS console, click on your load balancer. Copy the **DNS name** (endpoint). [\[137. Load...ncer & DNS \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/137.%20Load%20Balancer%20%26%20DNS.txt)

**4b. Go to your domain registrar:**

Log into **GoDaddy** (or whichever registrar holds your domain). Navigate to **My Products → your domain → DNS**. [\[137. Load...ncer & DNS \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/137.%20Load%20Balancer%20%26%20DNS.txt)

**4c. Add a CNAME record:**

Click **Add New Record**.

| Setting | Value                                 |
| ------- | ------------------------------------- |
| Type    | CNAME                                 |
| Name    | `vprofileapp`                         |
| Value   | `<paste load balancer DNS name here>` |

Click **Save**. [\[137. Load...ncer & DNS \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/137.%20Load%20Balancer%20%26%20DNS.txt)

This means `vprofileapp.hkhinfoteck.xyz` now resolves to the load balancer.

**For users without a domain:** Simply copy the load balancer endpoint and paste it directly into the browser. HTTP will work; HTTPS will not (certificate mismatch). [\[137. Load...ncer & DNS \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/137.%20Load%20Balancer%20%26%20DNS.txt)

***

## Step 5: Verify Health and Access

**5a. Check target group health:**

Navigate to **EC2 → Target Groups → vprofile-las-tg → Targets tab**.

Click **Refresh**. The status should show **"healthy."** [\[137. Load...ncer & DNS \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/137.%20Load%20Balancer%20%26%20DNS.txt)

**If status shows "unhealthy," troubleshoot in this order:**

1. **Is Tomcat running?** SSH into app01 and verify the Tomcat service is active.
2. **Security group rules?** Does the app01 security group allow port 8080 **from the load balancer security group**?
3. **Health check port?** Is the health check override set to 8080 (not 80)?

If all three are correct, wait and refresh. The health check requires multiple consecutive passes before declaring healthy. [\[137. Load...ncer & DNS \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/137.%20Load%20Balancer%20%26%20DNS.txt)

**5b. Test HTTP access via load balancer:**

Paste the load balancer DNS endpoint into a browser:

```
http://<load-balancer-dns-name>
```

You should see the vProfile login page. The browser will show **"Not Secure"** because this is plain HTTP. [\[137. Load...ncer & DNS \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/137.%20Load%20Balancer%20%26%20DNS.txt)

**5c. Test HTTPS access via custom domain (if configured):**

```
https://vprofileapp.hkhinfoteck.xyz
```

The page should load with a **padlock icon**. Click the padlock → "Connection is secure" → "Certificate is valid." The certificate should show: issued for `hkhinfoteck.xyz`, issued by Amazon. [\[137. Load...ncer & DNS \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/137.%20Load%20Balancer%20%26%20DNS.txt)

**5d. Verify certificate on load balancer:**

In AWS console → Load Balancer → Listeners → click **HTTPS:443** → **Certificates**. Your ACM certificate should be listed there. [\[137. Load...ncer & DNS \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/137.%20Load%20Balancer%20%26%20DNS.txt)

***

## Step 6: End-to-End Service Verification

This step validates that every backend service is reachable through the application.

**6a. Verify MySQL (Database):**

On the login page, enter:

* Username: `admin_vp`
* Password: `admin_vp` (same)

If login succeeds → MySQL connection is working (user credentials are stored in the database). [\[137. Load...ncer & DNS \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/137.%20Load%20Balancer%20%26%20DNS.txt)

**6b. Verify RabbitMQ:**

After login, observe the application dashboard. It should show that a **queue is generated**. This confirms connectivity to the RabbitMQ message broker. [\[137. Load...ncer & DNS \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/137.%20Load%20Balancer%20%26%20DNS.txt)

**6c. Verify Memcache:**

1. Click **"All Users."**
2. Select **any user** → message shows: *"data is from DB, data is inserted in cache."*
3. Go **back**.
4. Click the **same user again** → message shows: *"data is from cache."*

First click: DB fetch + cache write. Second click: cache hit. This proves Memcache is connected and functioning. [\[137. Load...ncer & DNS \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/137.%20Load%20Balancer%20%26%20DNS.txt)

**Connection to larger flow:** All four tiers (Load Balancer → Tomcat → MySQL/RabbitMQ/Memcache) are verified. The architecture is fully operational. The next step (covered in the next lecture) is adding an Auto Scaling Group so the number of Tomcat instances scales with demand.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Architecture Flow

```
User Browser
    │
    ▼
[ DNS: vprofileapp.hkhinfoteck.xyz ]
    │  (CNAME → ALB endpoint)
    ▼
[ Application Load Balancer (vprofile-las-elb) ]
    ├── Listener: HTTP :80   ──→ Target Group (vprofile-las-tg)
    └── Listener: HTTPS :443 ──→ Target Group (vprofile-las-tg)
                  │                        │
          ACM Certificate             Instance: app01
          (SSL termination)           Port: 8080 (Tomcat)
                                           │
                                     ┌─────┼──────┐
                                     ▼     ▼      ▼
                                   MySQL  RabbitMQ  Memcache
```

***

## Port Map (Critical)

```
Internet → ALB:  80 (HTTP), 443 (HTTPS)
ALB → Instance:  8080 (Tomcat)
Health Check:    8080 (overridden, NOT default 80)
```

**8080 appears in 3 places during target group creation:**

1. Target group port
2. Health check override
3. Instance registration port

***

## Security Group Chain

```
Internet ──[80,443]──→ LB Security Group ──[8080]──→ App Security Group ──→ app01
                                                          │
                                            Temporary: 8080 from "My IP" (test only)
```

Rule: Instances never directly exposed. All traffic funneled through ALB.

***

## HTTPS Trust Chain

```
Domain (GoDaddy) → ACM Certificate (Amazon) → ALB HTTPS:443 Listener → Browser padlock
```

No domain / No certificate → skip HTTPS listener → HTTP-only access via ALB endpoint.

***

## Target Group Health Check — Troubleshooting Sequence

```
Unhealthy?
    ├── 1. Is Tomcat service running on app01?
    ├── 2. Does app01 SG allow 8080 FROM LB SG?
    ├── 3. Is health check port overridden to 8080?
    └── 4. Wait + refresh (multiple checks needed before "healthy")
```

***

## End-to-End Verification Sequence

```
Action                          → Validates
─────────────────────────────────────────────
Login succeeds (admin_vp)       → MySQL connection ✓
Dashboard shows queue generated → RabbitMQ connection ✓
Click user → "data from DB"    → DB read + Memcache write ✓
Click same user → "from cache" → Memcache read ✓
```

***

## ALB Creation Sequence (Operational)

```
1. Create Target Group (instances, port 8080, health check 8080, register app01:8080)
2. Create ALB (name, VPC, all AZs, LB security group)
3. Add Listener HTTP:80 → target group
4. Add Listener HTTPS:443 → target group + ACM certificate
5. Create
6. Wait for "Active" status
7. Copy DNS name → CNAME record in domain registrar
8. Verify health → verify HTTP → verify HTTPS → verify all services
```

***

## Key Engineering Patterns

| Pattern                            | Manifestation                                                                       |
| ---------------------------------- | ----------------------------------------------------------------------------------- |
| **Stable entry point abstraction** | ALB decouples users from instance IPs; IPs change, ALB endpoint stays               |
| **Port translation**               | External ports (80/443) ≠ internal port (8080); ALB bridges the gap                 |
| **SSL termination**                | Encryption ends at ALB; backend traffic is plain HTTP (simpler, faster)             |
| **Health-gated routing**           | ALB only routes to targets that pass health checks; unhealthy = excluded            |
| **Layered security**               | Each tier has its own SG; traffic flows through narrow, defined channels            |
| **Progressive verification**       | Test component → build next layer → verify again; never assume                      |
| **Multi-check stabilization**      | Health status requires multiple consecutive passes to prevent flapping              |
| **Infrastructure-as-entry-point**  | ALB is the prerequisite for autoscaling; targets are dynamic, entry point is stable |

***

## Next Dependency

```
ALB + Target Group (done) → Auto Scaling Group (next lecture)
    ASG will auto-register new Tomcat instances into the target group
    ALB already supports multiple targets — ASG fills that capacity
```

***

This completes the full reconstruction. Each section serves a distinct purpose — **Theory** builds understanding of *why* and *how*, **Practical** gives you the exact execution path to reproduce it, and the **Compression Map** lets you reload the entire system in minutes during future revision. Let me know if you'd like any section expanded or a flashcard export for Anki! 🚀
