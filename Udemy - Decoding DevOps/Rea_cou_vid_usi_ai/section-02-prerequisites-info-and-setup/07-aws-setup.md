# AWS Account Setup — Complete Deep Learning Material

*Reconstructed from the video lecture on AWS prerequisite setup* [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1. AWS Console — The Web Management Interface

The **AWS Console** is the browser-based graphical interface through which you interact with all AWS services. When the lecture says "console," it specifically means this web UI accessible at `aws.amazon.com/console`. Every AWS service — compute, storage, networking, security, monitoring — can be managed from this single interface. The console is the primary control plane for human operators; it is where you launch servers, configure permissions, view bills, and set alarms. For beginners, the console is the entry point to the entire AWS ecosystem. Everything done in this lecture happens inside the console. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

***

## 2. Root User — The God-Level Account

When you sign up for AWS with an email address and password, you create what AWS calls the **root user**. This is the most powerful identity in the entire AWS account. The root user has **unrestricted, irrevocable access** to every service, every resource, every billing detail, and every administrative function. It cannot be limited by any policy — it is above all permission boundaries. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

This power is precisely why the root user is dangerous for everyday use. If the root user credentials are compromised, the attacker has total control — they can spin up expensive resources, delete everything, or lock you out entirely. AWS's own security model strongly discourages using the root user for routine operations. The root user should only be used for a narrow set of tasks: **billing management, account-level support cases, and managing IAM users**. For all other AWS activities — launching servers, configuring services, deploying applications — you create and use IAM users instead. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

🔍 **Deep Dive:** The root user is tied to the email address used during sign-up. This email becomes the account's identity anchor. Unlike IAM users, the root user cannot be deleted or have its permissions reduced through policies. This is an architectural decision by AWS — the root user exists as an emergency-access identity. In production organizations, root user credentials are often locked in a physical vault, and MFA hardware tokens (not phone apps) are used.

***

## 3. IAM — Identity and Access Management

**IAM** is the AWS service that controls **who** can do **what** within your AWS account. It is the central authorization and authentication system. IAM lets you create users, assign permissions, and enforce security boundaries. Without IAM, every person would need root credentials, which is unacceptable from a security standpoint. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

IAM solves three fundamental problems: **(1)** It allows multiple people to use a single AWS account with separate identities. **(2)** It enforces the principle of least privilege — each user gets only the permissions they need. **(3)** It provides an audit trail of who did what. In this lecture, IAM is used to create a user called "IT admin" with administrator access. This user becomes the day-to-day operational identity, replacing the root user for all service consumption. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

### IAM Policies and Permissions

Permissions in IAM are controlled through **policies** — JSON documents that define what actions are allowed or denied on which resources. When the lecture assigns "Administrator Access" to the IT admin user, it attaches a predefined AWS policy that grants full access to all services. This is a broad permission set, appropriate for a personal learning account but dangerous in production. Policies can be attached or removed from users at any time, giving you dynamic control over access. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

🔍 **Deep Dive:** IAM operates on a deny-by-default model. A new IAM user with no policies attached can log in but cannot do anything — no service access, no resource creation, nothing. Permissions must be explicitly granted. The "Administrator Access" policy is a managed policy provided by AWS that effectively says "allow all actions on all resources." In real organizations, you would create custom policies scoped to specific services and actions.

⚠️ **Expert Note:** In production environments, administrator access is rarely given to individual users. Instead, role-based access control (RBAC) with scoped policies is used. The lecture explicitly warns to be very careful with both root and IT admin credentials since both have full access in this setup.

***

## 4. Account Alias — Human-Readable Login URL

Every AWS account has a numeric **Account ID** (a 12-digit number). By default, the IAM login URL contains this numeric ID. An **account alias** replaces this numeric ID with a human-readable name in the login URL, making it easier to remember and share. This is configured inside the IAM service dashboard. The alias is cosmetic — it does not change the account ID or affect any functionality. It simply provides a friendlier login URL for IAM users. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

***

## 5. Multi-Factor Authentication (MFA) — The Security Layer

**MFA** adds a second verification factor on top of your password. Even if an attacker obtains your password, they cannot log in without the time-based code generated by your authenticator device. The lecture uses **Google Authenticator**, a phone app that generates a new 6-digit code every 30 seconds. The setup process involves scanning a QR code from AWS, which establishes a shared secret between AWS and the app. From that point on, every login requires both the password and the current 6-digit code. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

The lecture sets up MFA on **both** the root user and the IAM user. This is critical — securing only one leaves the other vulnerable. The two MFA codes shown during setup (entering two consecutive codes) is AWS's way of confirming the time synchronization between the authenticator app and AWS's servers is correct. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

🔍 **Deep Dive:** MFA works on the TOTP (Time-based One-Time Password) algorithm. The QR code encodes a shared secret key. Both the authenticator app and AWS use this key combined with the current time to independently generate the same 6-digit code. Because the code changes every 30 seconds, a stolen code is useless after that window. AWS asks for two consecutive codes during setup to verify the clock sync is accurate.

***

## 6. AWS Regions — Geographic Service Clusters

AWS operates infrastructure in multiple **regions** worldwide — each region is a geographically isolated cluster of data centers. The lecture instructs you to switch to **US East 1 (North Virginia)** immediately after account creation. This is not arbitrary — North Virginia is AWS's oldest and most feature-complete region. It has the **widest service availability** (new services launch here first), **full free tier eligibility**, and is generally the **cheapest** region. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

A critical detail: the **billing alarm in CloudWatch can only be viewed in the North Virginia region**, even though it monitors billing for the entire account. This is because billing metrics are aggregated globally but surfaced only in US East 1. If you are in any other region, you simply won't see the billing metric when creating the alarm. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

⚠️ **Expert Note:** Region selection has real consequences in production. Data residency laws may require certain data to stay in specific geographic regions. Latency-sensitive applications should be deployed in regions closest to their users. But for learning purposes, North Virginia is the universally recommended default.

***

## 7. AWS Free Tier vs. Paid Plan — The Account Type Decision

During sign-up, AWS presents two plans: a **free tier plan** (limited to certain services for a fixed period) and a **paid plan** (full access to all services with pay-as-you-go pricing). Both plans provide **$200 in credits** ($100 at signup + $100 after completing certain steps). The lecture recommends the **paid plan** because the free plan restricts which services you can access, while the paid plan gives you full free tier access *plus* the ability to scale into paid services when needed. The key insight: choosing "paid" does not mean you will be charged — 99% of the course uses free tier services. The paid plan simply removes artificial service restrictions. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

***

## 8. CloudWatch — The Monitoring Service

**CloudWatch** is AWS's centralized monitoring service. It collects metrics from all AWS resources in your account — CPU usage of servers, network traffic, storage consumption, and critically, **billing data**. CloudWatch can trigger **alarms** when metrics cross defined thresholds. In this lecture, CloudWatch is used exclusively for billing monitoring: if the estimated bill exceeds $5, an alarm fires and sends an email notification. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

CloudWatch does not act alone for notifications — it integrates with **SNS (Simple Notification Service)**. When an alarm triggers, CloudWatch pushes the alert to an SNS topic, which then delivers it to subscribers (in this case, an email address). This is a decoupled architecture: CloudWatch detects the condition, SNS handles the delivery. The SNS topic created during this setup is reusable — you can attach it to other alarms or notifications later. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

🔍 **Deep Dive:** The alarm operates on the "Total Estimated Charge" metric under the Billing namespace. This metric aggregates all charges across all services and regions into a single number. The alarm evaluates this metric against the threshold (≥ $5) and transitions between OK → ALARM states. The SNS topic requires **subscription confirmation** — until you click the confirmation link in your email, notifications will show as "pending" and will not be delivered.

***

## 9. SSL/TLS Certificates — Trust on the Internet

The final section introduces **public certificates**. A certificate is a digital document that proves a domain belongs to its claimed owner. When you visit `https://amazon.com`, your browser checks the site's certificate to confirm it's genuinely Amazon and not an impersonator. Certificates are issued by **Certificate Authorities (CA)** — trusted entities that verify domain ownership. Amazon itself is one such authority. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

The lecture uses **AWS Certificate Manager (ACM)** to request a free public certificate for a custom domain. ACM is the AWS service that handles certificate creation, storage, and renewal. Public certificates from ACM are free; private certificates are paid. The certificate is requested for `*.yourdomain.com` (wildcard format), which means it covers the base domain and all subdomains. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

### DNS Validation — Proving Domain Ownership

To prove you own the domain, AWS uses **DNS validation**. AWS provides a **CNAME record** (a DNS record that maps one name to another) that you must add to your domain's DNS settings at your domain registrar (like GoDaddy). When AWS queries the domain's DNS and finds the expected CNAME record, it confirms you control the domain and issues the certificate. This validation can take time — especially for newly purchased domains, up to **48 hours**. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

🔍 **Deep Dive:** The CNAME record for validation contains a unique key-value pair generated by ACM. The "name" field is a token specific to your certificate request, and the "value" points to an AWS validation endpoint. When adding this record in your registrar, you must **remove your domain name from the end of the CNAME name** (registrars auto-append it) and **remove trailing dots** from both name and value fields. Failing to do this is the most common reason validation gets stuck in "pending" state.

⚠️ **Expert Note:** The wildcard certificate (`*.domain.com`) is a deliberate choice — it allows you to use the same certificate for any subdomain you create later (e.g., `app.domain.com`, `api.domain.com`) without requesting new certificates. In production, certificate management is critical — expired or misconfigured certificates cause HTTPS failures and browser security warnings.

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are setting up a fully secured, monitored AWS account ready for DevOps learning. The final outcome: a working AWS account with a dedicated IAM user for daily operations, MFA on both root and IAM accounts, a billing alarm that emails you if charges exceed $5, and optionally, a public SSL certificate for a custom domain. After this setup, you never touch the root user again for regular work. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

***

## Step 1: Create the AWS Account

Navigate to `aws.amazon.com/console` or search "AWS Free Tier account" in your browser. Click **Create Account**. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

1. Enter your **email address** — this becomes the root user identity permanently tied to this account.
2. Give the account a **name** (any descriptive name).
3. Click **Verify email address** → check your inbox for the verification code → enter it → click **Verify**.
4. Set a **root user password** — make it long, with alphanumeric characters and symbols. Click **Continue**. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

**Plan Selection:** Choose **Paid Plan**. Despite the name, you will primarily use free tier services. The paid plan gives unrestricted access to all services and the same $200 credits ($100 immediate + $100 after completing onboarding steps). The free plan limits which services you can access. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

5. Select **Personal** account type. Fill in your full name, address, city, postal code. Click **Agree and Continue**.
6. Enter **credit/debit card details** — required for verification only. AWS will temporarily deduct $1 (or ₹2 for Indian cards), which is refunded.
7. Select primary purpose as **Academic**, ownership type as **Individual**. Complete identity verification via **SMS** or voice call — enter the received code.
8. Select **Basic Support** (free) — the other plans are for production workloads needing AWS support team assistance. Click **Complete Sign Up**. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

**Verification:** Click **Sign in to console**. Log in with your email and password. If any service (like EC2) shows errors or the dashboard doesn't load, wait a few minutes — account activation can take time. If errors persist, go to **Support Center** (via the support button) and raise a ticket or chat with AWS support to check activation status. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

**Connection to system flow:** You now have a working AWS account with root user access. The next steps secure this account before any services are used.

***

## Step 2: Switch to North Virginia Region

After logging in, find the **region dropdown** (top-right area of the console) and switch to **US East (N. Virginia) / us-east-1**. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

This is essential because: North Virginia has the widest service availability, full free tier support, is the cheapest region, and — critically — **billing metrics in CloudWatch are only visible in this region**. Keep this region selected throughout the course unless explicitly instructed otherwise. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

***

## Step 3: Create an Account Alias in IAM

Search for **IAM** in the console search bar and open the IAM service dashboard. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

1. Find **Account Alias** on the dashboard.
2. Click **Create**.
3. Enter a preferred name (alphabetic, memorable) — this replaces the numeric Account ID in your IAM login URL.
4. Click **Create Alias**. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

**Result:** Your IAM login URL changes from `https://<12-digit-ID>.signin.aws.amazon.com/console` to `https://<your-alias>.signin.aws.amazon.com/console`. Note this URL — IAM users will use it to log in.

***

## Step 4: Set Up MFA for the Root User

Still in the **IAM dashboard**, locate the **MFA** section for the root account. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

1. Click **Add MFA**.
2. Give the MFA device a name (e.g., your phone's name).
3. Select **Authenticator App**.
4. Click **Show QR Code** — a QR code appears on screen. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

On your phone:
5\. Open **Google Authenticator** (install from App Store / Play Store if not installed).
6\. Tap the **+** button → **Scan QR Code** → scan the code displayed on screen.
7\. The app generates a 6-digit code. Enter it in the first MFA code field on AWS.
8\. **Wait** for the code to refresh (every 30 seconds), then enter the **new** 6-digit code in the second field.
9\. Click **Add MFA**. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

**Verification:** The MFA status for root user should now show as active/assigned. From now on, every root user login will require the Google Authenticator code.

⚠️ **Expert Note:** If you lose access to your phone/authenticator app, recovering root access is extremely difficult. In production, organizations use hardware MFA tokens and store backup codes securely.

***

## Step 5: Create an IAM User

Navigate to **IAM → Users → Create User**. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

1. **User name:** Enter a name (the lecture uses `IT admin`).
2. Check **Provide user access to AWS Management Console** — this enables browser-based login for this user.
3. Select **Auto-generated password** (or set a custom one).
4. Check **User must create a new password at next sign-in** — forces password reset on first login.
5. Click **Next**. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

**Permissions:**
6\. On the permissions page, search for and select **AdministratorAccess** — this AWS-managed policy grants full access to all services.
7\. Click **Next** → **Create User**. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

**Critical output:** After creation, you'll see three pieces of information:

* **Console sign-in URL** (the alias URL from Step 3)
* **Username**
* **Auto-generated password**

**Save all three immediately.** The password is shown only once. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

**Connection to system flow:** This IAM user replaces root for all daily AWS operations. Root is now reserved only for billing, IAM management, and support.

***

## Step 6: Set Up MFA for the IAM User

Go to **IAM → Users → click on the user (IT admin) → Security Credentials tab**. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

1. Find **MFA device** → follow the exact same process as Step 4 (name the device, authenticator app, scan QR, enter two consecutive codes, add MFA).

**Important:** In Google Authenticator, this will appear as a **separate entry** from the root user MFA. Each identity has its own independent MFA code. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

***

## Step 7: Test IAM User Login

1. **Log out** of the root account.
2. Navigate to the **IAM login URL** (the alias URL from Step 3).
3. Enter the IAM **username** and **auto-generated password**.
4. You will be prompted to **reset the password** — enter the old password and set a new one.
5. Enter the **MFA code** from Google Authenticator (the IAM user's entry, not the root user's).
6. After successful login, confirm you're in **North Virginia** region. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

**Then:** Log out of the IAM user and log back in with the **root user** — we need root access for the next step (billing alarm setup).

***

## Step 8: Configure Billing Preferences

While logged in as **root user**, click the **account dropdown (top-right) → Billing and Cost Management**. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

The dashboard may show "data unavailable" for forecasts on a fresh account — this is normal.

**Explore Bills:** Go to the **Bills** section to see detailed monthly breakdowns by region and service. Use this anytime to check what's costing money. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

**Configure Preferences:**

1. Scroll down to **Billing Preferences**.
2. **Free Tier Alerts** — should be automatically enabled.
3. Click **Edit** next to PDF Invoices → enable **PDF invoices delivered by email** → **Update**.
4. Click **Alert Preferences** → enter your **email address** → check **Receive CloudWatch billing alerts** → **Update**. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

**Connection to system flow:** This step enables the infrastructure (CloudWatch billing metric collection) that the alarm in the next step depends on. Without enabling CloudWatch billing alerts here, the billing metric won't be available in CloudWatch.

***

## Step 9: Create the CloudWatch Billing Alarm

Navigate to **CloudWatch** (search in console). **Confirm you are in US East 1 (N. Virginia)** — billing metrics are only visible here. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

1. Go to **All Alarms → Create Alarm → Select Metric**.
2. Click **Billing → Total Estimated Charge**.
3. Select your **currency** (e.g., USD) → **Select Metric**.
4. Scroll down → set condition to **Greater or Equal to** → enter threshold: `5` (meaning $5).
5. Click **Next**. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

**Configure Notification:**
6\. Click **Create New Topic** (this creates an SNS topic).
7\. **Topic name:** Enter a name (e.g., `admin_email`).
8\. **Email endpoint:** Enter your email address.
9\. Click **Create Topic** → **Next**.
10\. **Alarm name:** Enter a name (e.g., `billing_alarm`). Add optional description.
11\. Click **Next** → **Create Alarm**. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

**Confirm Subscription (CRITICAL):**
12\. Go to the **inbox** of the email you entered.
13\. Find the AWS SNS confirmation email → click **Confirm Subscription**.
14\. Back in CloudWatch, click on the billing alarm → go to the **Actions** tab → verify the notification shows as active (not "pending"). Refresh if needed — may take a minute. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

**Verification:** The alarm should be in **OK** state (since your bill is currently $0). If your bill ever reaches ≥$5, it transitions to **ALARM** state and sends you an email.

🔍 **Deep Dive:** The SNS topic (`admin_email`) is a persistent, reusable resource. Once confirmed, you can attach it to any future CloudWatch alarm or other AWS service that supports SNS notifications. This is the publish-subscribe pattern — CloudWatch publishes alerts, SNS delivers them to all confirmed subscribers.

***

## Step 10: Request a Public SSL Certificate (Optional — requires a purchased domain)

If you purchased a domain in a previous lecture, this step creates a public certificate for it. If not, skip this and return before the AWS projects section. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

Navigate to **AWS Certificate Manager (ACM)** — search "Certificate Manager" in the console. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

1. Click **Request a Certificate**.
2. Select **Public Certificate** (free). Do NOT select private (paid). Click **Next**.
3. **Fully Qualified Domain Name:** Enter `*.yourdomain.com` (e.g., `*.hcinfotech.xyz`). The wildcard `*` covers all subdomains.
4. **Validation Method:** Select **DNS Validation**.
5. Click **Request**. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

**Status:** The certificate shows **Pending Validation**. To validate, you must add a CNAME record to your domain's DNS settings.

**Add the CNAME Record in Your Domain Registrar (e.g., GoDaddy):**

6. In ACM, locate the **CNAME name** and **CNAME value** provided for your certificate.
7. Log into your domain registrar (e.g., GoDaddy → My Products → your domain → **DNS**).
8. Click **Add New Record**.
9. **Type:** Select **CNAME**.
10. **Name field:** Paste the CNAME name from ACM. **Important modifications:**
    * **Remove your domain name** from the end (registrars auto-append it).
    * **Remove the trailing dot (`.`)** at the end.
11. **Value field:** Paste the CNAME value from ACM.
    * **Remove the trailing dot (`.`)** at the end.
12. Click **Save**. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

**Do NOT modify any existing DNS records** — only add the new one.

**Validation Timeline:** For newly purchased domains, validation can take up to **48 hours**. You do not need to wait — proceed with the course and check back later. The certificate status will change from "Pending Validation" to "Issued" once AWS confirms the CNAME record. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

⚠️ **Expert Note:** The most common mistake is not properly trimming the CNAME name. If your domain is `example.com` and the CNAME name from ACM is `_abc123.example.com.`, you should enter only `_abc123` in the Name field (the registrar appends `.example.com` automatically). Getting this wrong leaves the certificate permanently stuck in "Pending Validation."

***

## Step 11: Final State — Switch to IAM User for All Future Work

After completing all steps:

1. Log out of root user.
2. Log in with the **IAM user** via the alias URL.
3. Confirm **North Virginia** region is selected.
4. Use this IAM user for **all** AWS activities going forward. [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

**Root user usage going forward is limited to:**

* Billing and cost management
* Managing IAM users (creating/deleting)
* AWS support cases [\[14-aws-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/14-aws-setup.txt)

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## System Architecture — What Was Built

```
AWS Account (Root User = God Mode)
├── Security Layer
│   ├── Root User + MFA (Google Authenticator)
│   └── IAM User ("IT admin") + MFA + AdministratorAccess Policy
│       └── Account Alias → human-readable login URL
│
├── Monitoring Layer
│   ├── Billing Preferences (PDF invoices + Free Tier alerts)
│   └── CloudWatch Alarm (Total Estimated Charge ≥ $5)
│       └── → SNS Topic ("admin_email") → Email Notification
│           └── Requires: Subscription Confirmation (email click)
│
└── Certificate Layer (Optional)
    └── ACM Public Certificate (*.domain.com)
        └── DNS Validation → CNAME record in Domain Registrar
            └── Pending → Issued (up to 48hrs)
```

***

## Identity Hierarchy

```
Root User (email + password + MFA)
  │
  ├── Unrestricted access — cannot be limited
  ├── USE ONLY FOR: Billing, IAM mgmt, Support
  │
  └── Creates → IAM User (username + password + MFA)
                  │
                  ├── Controlled by Policies (attached/removed dynamically)
                  ├── AdministratorAccess policy = full access (current setup)
                  └── USE FOR: All daily AWS operations
```

***

## Operational Flow — Login Decision

```
Need billing/support/IAM mgmt? → Root User login (email + password + MFA)
Everything else?               → IAM User login (alias URL + username + password + MFA)
```

***

## CloudWatch Alarm — Cause/Effect Chain

```
AWS Services consumed → Charges accumulate → "Total Estimated Charge" metric updated
  → CloudWatch evaluates metric against threshold (≥ $5)
    → Threshold breached? → Alarm state triggers
      → Publishes to SNS Topic
        → SNS delivers to confirmed email subscriber
          → You receive email notification → Check Bills → Clean up resources
```

**Prerequisite chain:**

```
Enable "CloudWatch billing alerts" in Billing Preferences
  → Billing metric becomes available in CloudWatch (US-East-1 ONLY)
    → Alarm can be created on this metric
      → SNS topic must be created + subscription confirmed
        → Alarm fully operational
```

***

## Certificate Validation — Interaction Chain

```
ACM generates CNAME (name + value)
  → You add CNAME to Domain Registrar DNS settings
    → AWS queries your domain's DNS
      → Finds matching CNAME? → Ownership confirmed → Certificate: Issued
      → Not found?            → Stays: Pending Validation
```

**CNAME Entry Pitfalls:**

```
Name field: Remove domain suffix (registrar auto-appends) + Remove trailing dot
Value field: Remove trailing dot
Do NOT touch existing DNS records
```

***

## Region Rule

```
Default: US East 1 (N. Virginia) — always
  ├── Widest service availability
  ├── Full free tier eligibility
  ├── Cheapest
  └── ONLY region where billing metrics appear in CloudWatch
```

***

## Reusable Engineering Patterns

| Pattern                           | Where It Appears                                                                                                                                     |
| --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Separation of privilege**       | Root (admin-of-admins) vs IAM (daily operator) — never use highest privilege for routine work                                                        |
| **Defense in depth**              | Password + MFA on both identities — layered security, not single-point trust                                                                         |
| **Publish-Subscribe decoupling**  | CloudWatch (publisher) → SNS Topic (broker) → Email (subscriber) — detection decoupled from delivery                                                 |
| **Threshold-based alerting**      | Metric → Threshold → Alarm → Action — generic pattern for any monitoring system                                                                      |
| **Proof-of-ownership via DNS**    | Add a challenge record → Authority verifies → Trust established — same pattern used across SSL, domain verification, email authentication (SPF/DKIM) |
| **Reusable notification channel** | SNS topic created once, reused across multiple alarms/services                                                                                       |
| **Wildcard scoping**              | `*.domain.com` certificate — single credential covers all subdomains, reducing management overhead                                                   |

***

## Quick Recall — Execution Sequence

```
1. Sign up (email → root user created)
2. Choose Paid Plan (full access, still free tier eligible)
3. Switch to N. Virginia
4. IAM → Create Account Alias
5. IAM → Root MFA (Google Authenticator)
6. IAM → Create User (IT admin + AdministratorAccess)
7. IAM → IAM User MFA
8. Test IAM login → reset password → log back as root
9. Billing Preferences → Enable PDF invoices + CloudWatch billing alerts
10. CloudWatch → Create Alarm (Billing ≥ $5) → SNS topic → Confirm email subscription
11. (Optional) ACM → Request public cert → DNS validation via CNAME in registrar
12. Log out root → Log in as IAM user → N. Virginia → Ready
```

***

## Key Numbers to Remember

| Item                             | Value                     |
| -------------------------------- | ------------------------- |
| Credits received                 | $100 + $100 (after steps) |
| Temporary card deduction         | $1 / ₹2 (refunded)        |
| Recommended billing threshold    | $5                        |
| MFA code rotation                | Every 30 seconds          |
| DNS validation time (new domain) | Up to 48 hours            |
| Billing metrics visible in       | US-East-1 only            |

***

This completes the full reconstruction of the video lecture into deep learning material. The three sections are designed to be complementary: Theory builds your mental model, Practical gives you confident execution capability, and the Compression Map lets you rapidly reload the entire system architecture weeks or months later without re-reading everything. 🚀
