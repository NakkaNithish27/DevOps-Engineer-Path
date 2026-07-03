# 🎓 Deep Learning Material: SSL Certificates, HTTPS, and Final DNS Setup — Securing the GCP Load Balancer with TLS and Domain Resolution

**Source:** Video lecture on SSL certificate creation, HTTPS proxy setup, and DNS configuration on GCP (from [300-ssl-certificates-https-and-final-dns-setup.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/300-ssl-certificates-https-and-final-dns-setup.txt?EntityRepresentationId=9a382c12-718f-4516-941a-03888947ace6) caption file) [\[300-ssl-ce...-dns-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/300-ssl-certificates-https-and-final-dns-setup.txt)

**Video Context:** This is the final infrastructure lecture in the GCP vProfile project — it transforms the existing HTTP load balancer into a fully secured HTTPS endpoint with a valid SSL certificate and public domain name. The instructor walks through the complete certificate lifecycle on GCP: DNS authorization (proving domain ownership), certificate creation via Certificate Manager, certificate map creation, HTTPS proxy creation, HTTPS forwarding rule creation, and DNS A-record setup in GoDaddy. The lecture also provides a critical recap of the entire load balancer traffic flow architecture (client → forwarding rule → HTTP/HTTPS proxy → URL map → backend service → managed instance group → instances in private subnet). This is where the project becomes production-resembling — HTTPS with a trusted certificate from Google Trust Services.

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — The Existing Load Balancer Architecture Recap

Before adding HTTPS, the instructor recaps the complete GCP load balancer traffic flow that was built in previous lectures. Understanding this architecture is essential for knowing where the certificate fits: [\[300-ssl-ce...-dns-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/300-ssl-certificates-https-and-final-dns-setup.txt)

**Request flow:** Client → **Forwarding Rule** (port 80) → **HTTP Proxy** → **URL Map** → **Backend Service** → **Managed Instance Group** (instances running vProfile on port 8080)

The instructor clarifies the "front end" and "back end" terminology, which has **two levels of meaning** in this architecture: [\[300-ssl-ce...-dns-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/300-ssl-certificates-https-and-final-dns-setup.txt)

* **vProfile front end** = the load balancer + application servers (receives external requests)
* **vProfile back end** = database, Memcache, services in private subnets
* **Load balancer front end** = forwarding rule + proxy (internet-facing)
* **Load balancer back end** = managed instance group (the actual application instances)

The URL map is the **routing layer** — it maps the HTTP proxy to the backend service, telling the load balancer: "for requests arriving at this proxy, send them to this group of instances." [\[300-ssl-ce...-dns-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/300-ssl-certificates-https-and-final-dns-setup.txt)

***

## 1.2 — Why HTTPS and SSL Certificates Are Needed

In production, users access applications via **HTTPS** — a secure, encrypted connection. HTTPS requires an **SSL/TLS certificate** that proves the domain's identity. Without a valid certificate, browsers show security warnings, and the connection is not encrypted. [\[300-ssl-ce...-dns-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/300-ssl-certificates-https-and-final-dns-setup.txt)

The instructor frames this simply: *"in production, in real time, we definitely have a URL that will be HTTPS, secure connection."* The certificate proves that the domain (e.g., `hkhinfotech.xyz`) is legitimate and owned by the entity claiming it. [\[300-ssl-ce...-dns-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/300-ssl-certificates-https-and-final-dns-setup.txt)

A **Certificate Authority (CA)** issues certificates after verifying domain ownership. The instructor mentions several CAs: *"a certificate authority like Google or Amazon or CERT Manager. There are many authorities like that."* In this lecture, Google's own CA (**Google Trust Services**) is used through GCP's Certificate Manager service. [\[300-ssl-ce...-dns-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/300-ssl-certificates-https-and-final-dns-setup.txt)

***

## 1.3 — DNS Authorization: Proving Domain Ownership

Before GCP will issue a certificate for your domain, you must **prove you own it**. This is done through **DNS authorization** — GCP gives you a challenge (a specific DNS record), and you must create that record in your domain registrar (GoDaddy in this case). If GCP can verify the record exists, your ownership is proven. [\[300-ssl-ce...-dns-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/300-ssl-certificates-https-and-final-dns-setup.txt)

The challenge is a **CNAME record** with a specific format: [\[300-ssl-ce...-dns-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/300-ssl-certificates-https-and-final-dns-setup.txt)

* **Name:** `_acme-challenge.<subdomain>` (before the domain name)
* **Value:** A data string provided by GCP's DNS authorization response

The `_acme-challenge` prefix is part of the **ACME protocol** (Automatic Certificate Management Environment) — a standard protocol for automated certificate issuance. The instructor doesn't name the protocol, but the `_acme-challenge` record name is its signature. [\[300-ssl-ce...-dns-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/300-ssl-certificates-https-and-final-dns-setup.txt)

The instructor emphasizes removing trailing dots when copying values from GCP's output to GoDaddy: *"Make sure there is no dot and the domain name here"* and *"Make sure you remove that dot, that full stop at the end."* Trailing dots in DNS records can cause resolution failures. [\[300-ssl-ce...-dns-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/300-ssl-certificates-https-and-final-dns-setup.txt)

***

## 1.4 — Certificate Manager: GCP's Certificate Lifecycle Service

GCP's **Certificate Manager** handles the entire certificate lifecycle. The process involves four distinct objects: [\[300-ssl-ce...-dns-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/300-ssl-certificates-https-and-final-dns-setup.txt)

1. **DNS Authorization** — the proof-of-ownership mechanism
2. **Certificate** — the actual SSL/TLS certificate, linked to the DNS authorization
3. **Certificate Map** — a container/placeholder that holds certificates and makes them selectable by load balancer components
4. **Certificate Map Entry** — links a specific certificate to a specific hostname within a map

The instructor explains the map's purpose: *"a certificate map entry that is basically just a placeholder to keep this certificate from where we can choose it in our load balancer."* [\[300-ssl-ce...-dns-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/300-ssl-certificates-https-and-final-dns-setup.txt)

The certificate goes through states: after creation, it's in a pending/provisioning state. Once GCP verifies the DNS authorization (checks that the CNAME record resolves correctly), the certificate transitions to **`AUTHORIZED`** and **`ACTIVE`** status. The instructor checks this with `describe`: *"you should see the status authorized and status active."* [\[300-ssl-ce...-dns-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/300-ssl-certificates-https-and-final-dns-setup.txt)

***

## 1.5 — HTTPS Proxy vs. HTTP Proxy: What Changes

The existing architecture has an **HTTP proxy** handling unencrypted traffic on port 80. To support HTTPS, you create an **HTTPS proxy** — this is a separate component that handles TLS termination (decrypts the HTTPS traffic) and forwards the decrypted request to the same URL map. [\[300-ssl-ce...-dns-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/300-ssl-certificates-https-and-final-dns-setup.txt)

The HTTPS proxy needs two things the HTTP proxy didn't: [\[300-ssl-ce...-dns-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/300-ssl-certificates-https-and-final-dns-setup.txt)

1. The **URL map** (same one used by HTTP proxy — the routing doesn't change)
2. The **certificate map** (the TLS certificate for encrypting/decrypting traffic)

The HTTPS forwarding rule then listens on **port 443** (standard HTTPS port) and routes traffic to the HTTPS proxy, which uses the certificate for TLS and the URL map for routing. [\[300-ssl-ce...-dns-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/300-ssl-certificates-https-and-final-dns-setup.txt)

***

## 1.6 — DNS A-Record: Making the Domain Resolve to the Load Balancer

The final step is creating a **DNS A-record** in GoDaddy that maps the subdomain (e.g., `vpro-gcp.hkhinfotech.xyz`) to the **static IP** of the load balancer. An A-record maps a domain name to an IP address (unlike a CNAME which maps name to name). [\[300-ssl-ce...-dns-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/300-ssl-certificates-https-and-final-dns-setup.txt)

The static IP was created in a previous lecture and is retrieved with `gcloud compute addresses describe`. Once the A-record is published (which can take minutes to an hour for DNS propagation), the domain resolves to the load balancer, and users can access the application via `https://vpro-gcp.hkhinfotech.xyz`. [\[300-ssl-ce...-dns-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/300-ssl-certificates-https-and-final-dns-setup.txt)

The instructor verifies the complete chain works: the web page loads, the browser shows "Connection is secure", and the certificate is issued by **Google Trust Services**. [\[300-ssl-ce...-dns-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/300-ssl-certificates-https-and-final-dns-setup.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building and Why

We are adding **HTTPS support** to the GCP load balancer by creating an SSL certificate through GCP Certificate Manager, proving domain ownership via DNS authorization in GoDaddy, creating an HTTPS proxy and forwarding rule, and setting up the DNS A-record to point the domain to the load balancer. The final outcome: the vProfile application is accessible via `https://<subdomain>.<domain>` with a valid, browser-trusted SSL certificate from Google Trust Services.

***

## Step 1: Create DNS Authorization

**What we're doing:** Starting the domain ownership proof process.

```bash
gcloud certificate-manager dns-authorizations create auth-<subdomain> \
  --domain=<domain>
```

* `certificate-manager dns-authorizations create` — creates a DNS authorization object
* `auth-<subdomain>` — name for this authorization (e.g., `auth-gcp`)
* `--domain=<domain>` — the domain to authorize (e.g., `hkhinfotech.xyz`) [\[300-ssl-ce...-dns-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/300-ssl-certificates-https-and-final-dns-setup.txt)

**Describe it to get the challenge details:**

```bash
gcloud certificate-manager dns-authorizations describe auth-<subdomain>
```

**Key output:** A `dnsResourceRecord` section containing: [\[300-ssl-ce...-dns-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/300-ssl-certificates-https-and-final-dns-setup.txt)

* **name:** `_acme-challenge.<subdomain>.<domain>` — the CNAME record name
* **data:** a long string — the CNAME record value
* **type:** CNAME

**You need both the name and data values for the next step.**

***

## Step 2: Create the CNAME Record in GoDaddy

**What we're doing:** Proving domain ownership by creating the challenge record.

1. Go to **GoDaddy** → **My Products** → **Domains** → your domain → **DNS** [\[300-ssl-ce...-dns-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/300-ssl-certificates-https-and-final-dns-setup.txt)
2. Click **Add New Record**
3. **Type:** CNAME
4. **Name:** Copy the `_acme-challenge` portion from the describe output (everything before the domain name). **Remove any trailing dot.** [\[300-ssl-ce...-dns-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/300-ssl-certificates-https-and-final-dns-setup.txt)
5. **Value:** Paste the `data` string from the describe output. **Remove the trailing dot (full stop) at the end.** [\[300-ssl-ce...-dns-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/300-ssl-certificates-https-and-final-dns-setup.txt)
6. Click **Save** [\[300-ssl-ce...-dns-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/300-ssl-certificates-https-and-final-dns-setup.txt)

**Common mistakes:**

* Leaving a trailing dot in the name or value → DNS resolution fails
* Including the full domain name in the CNAME name field (GoDaddy auto-appends the domain) [\[300-ssl-ce...-dns-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/300-ssl-certificates-https-and-final-dns-setup.txt)

***

## Step 3: Create the SSL Certificate

**What we're doing:** Requesting GCP to issue a certificate, linked to the DNS authorization.

```bash
gcloud certificate-manager certificates create cert-<subdomain> \
  --domains="*.<domain>" \
  --dns-authorizations=auth-<subdomain>
```

* `certificates create cert-<subdomain>` — creates a certificate named `cert-<subdomain>`
* `--domains="*.<domain>"` — wildcard certificate covering all subdomains
* `--dns-authorizations=auth-<subdomain>` — links to the DNS authorization created in Step 1 [\[300-ssl-ce...-dns-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/300-ssl-certificates-https-and-final-dns-setup.txt)

GCP will verify the CNAME record (the ACME challenge) and issue the certificate. **This takes a few minutes.** [\[300-ssl-ce...-dns-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/300-ssl-certificates-https-and-final-dns-setup.txt)

***

## Step 4: Create Certificate Map and Entry

**What we're doing:** Creating a container to hold the certificate, making it usable by the load balancer.

**Create the map:**

```bash
gcloud certificate-manager maps create <map-name>
```

* `<map-name>` — any name you choose (e.g., `cert-map-<subdomain>`) <cite>turn23search3</cite>

**Add the certificate to the map:**

```bash
gcloud certificate-manager maps entries create <entry-name> \
  --map=<map-name> \
  --certificates=cert-<subdomain> \
  --hostname=<full-hostname>
```

* `--map` — the map created above
* `--certificates` — the certificate created in Step 3
* `--hostname` — the full domain (e.g., `vpro-gcp.hkhinfotech.xyz`) [\[300-ssl-ce...-dns-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/300-ssl-certificates-https-and-final-dns-setup.txt)

***

## Step 5: Verify Certificate Is Active

```bash
gcloud certificate-manager certificates describe cert-<subdomain>
```

**Expected output:** [\[300-ssl-ce...-dns-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/300-ssl-certificates-https-and-final-dns-setup.txt)

* `status: AUTHORIZED`
* `state: ACTIVE`

**If not yet active:** Wait a few more minutes and check again. DNS propagation of the CNAME record must complete before GCP can verify. [\[300-ssl-ce...-dns-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/300-ssl-certificates-https-and-final-dns-setup.txt)

***

## Step 6: Create HTTPS Proxy

**What we're doing:** Creating a new proxy that handles TLS-encrypted traffic using the certificate.

```bash
gcloud compute target-https-proxies create vprofile-https-proxy \
  --url-map=vprofile-url-map-<subdomain> \
  --certificate-map=<map-name>
```

* `target-https-proxies create` — creates an HTTPS proxy (distinct from the existing HTTP proxy)
* `--url-map` — the same URL map used by the HTTP proxy (routing rules are shared)
* `--certificate-map` — the certificate map containing the SSL certificate [\[300-ssl-ce...-dns-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/300-ssl-certificates-https-and-final-dns-setup.txt)

***

## Step 7: Create HTTPS Forwarding Rule

**What we're doing:** Creating a forwarding rule that listens for HTTPS traffic and sends it to the HTTPS proxy.

```bash
gcloud compute forwarding-rules create <forwarding-rule-name> \
  --target-https-proxy=vprofile-https-proxy \
  --address=<static-ip-name> \
  --global
```

* `--target-https-proxy` — the HTTPS proxy created in Step 6
* `--address` — the static IP allocated for the load balancer
* `--global` — this is a global forwarding rule [\[300-ssl-ce...-dns-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/300-ssl-certificates-https-and-final-dns-setup.txt)

**This may take some time to provision.** [\[300-ssl-ce...-dns-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/300-ssl-certificates-https-and-final-dns-setup.txt)

***

## Step 8: Create DNS A-Record in GoDaddy

**What we're doing:** Pointing the domain name to the load balancer's static IP.

**Get the load balancer IP:**

```bash
gcloud compute addresses describe <lb-ip-name> --global
```

Copy the IP address from the output. [\[300-ssl-ce...-dns-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/300-ssl-certificates-https-and-final-dns-setup.txt)

**Create the A-record in GoDaddy:**

1. **Add New Record** → **Type: A**
2. **Name:** `vpro-gcp` (or your subdomain) [\[300-ssl-ce...-dns-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/300-ssl-certificates-https-and-final-dns-setup.txt)
3. **Value:** the load balancer static IP
4. **Save** [\[300-ssl-ce...-dns-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/300-ssl-certificates-https-and-final-dns-setup.txt)

***

## Step 9: Verify the Complete Setup

**Wait** a few minutes to an hour for DNS propagation. [\[300-ssl-ce...-dns-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/300-ssl-certificates-https-and-final-dns-setup.txt)

**Access in browser:**

```
https://vpro-gcp.<your-domain>
```

**Expected results:** <cite>turn23search3</cite>

* vProfile web page loads fully functional
* Browser shows **"Connection is secure"** (padlock icon)
* Certificate details show **"Issued by: Google Trust Services"**

**Connection to system flow:** This completes the entire project architecture — from DNS resolution through HTTPS to the load balancer, through the URL map to the backend instances in private subnets, connecting to the database and caching services. [\[300-ssl-ce...-dns-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/300-ssl-certificates-https-and-final-dns-setup.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🔷 Complete HTTPS Traffic Flow (Final Architecture)

```
USER (browser)
  │
  ▼
DNS (GoDaddy A-record: vpro-gcp.domain → LB static IP)
  │
  ▼
FORWARDING RULE (port 443, HTTPS)
  │
  ▼
HTTPS PROXY (TLS termination using certificate)
  │  Certificate from: Google Trust Services
  │  Certificate Map → Certificate Map Entry → Certificate
  │
  ▼
URL MAP (routes proxy → backend service)
  │
  ▼
BACKEND SERVICE
  │
  ▼
MANAGED INSTANCE GROUP (vProfile app on port 8080)
  │  Private subnet instances
  │
  ├──► Database (private subnet)
  ├──► Memcache (private subnet)
  └──► Other backend services
```

***

## 🔷 Certificate Creation Pipeline

```
1. DNS AUTHORIZATION
   gcloud certificate-manager dns-authorizations create auth-<sub>
     → outputs: _acme-challenge CNAME name + data

2. CNAME RECORD IN GODADDY
   Type: CNAME
   Name: _acme-challenge.<sub> (remove trailing dot)
   Value: <data string> (remove trailing dot)

3. CERTIFICATE
   gcloud certificate-manager certificates create cert-<sub>
     --domains="*.<domain>"
     --dns-authorizations=auth-<sub>
   → Wait for ACTIVE status

4. CERTIFICATE MAP
   gcloud certificate-manager maps create <map-name>

5. CERTIFICATE MAP ENTRY
   gcloud certificate-manager maps entries create <entry>
     --map=<map-name>
     --certificates=cert-<sub>
     --hostname=<full-hostname>

6. VERIFY
   gcloud certificate-manager certificates describe cert-<sub>
   → status: AUTHORIZED, state: ACTIVE
```

***

## 🔷 HTTPS Load Balancer Components (Added in This Lecture)

```
EXISTING (from previous lectures):
  ├── Static IP (global)
  ├── HTTP Proxy → URL Map → Backend Service → MIG
  └── HTTP Forwarding Rule (port 80)

ADDED (this lecture):
  ├── DNS Authorization (proves domain ownership)
  ├── Certificate (SSL/TLS from Google Trust Services)
  ├── Certificate Map + Entry (makes cert selectable)
  ├── HTTPS Proxy (TLS termination + same URL map)
  ├── HTTPS Forwarding Rule (port 443 → HTTPS proxy)
  └── DNS A-Record (domain → LB static IP)
```

***

## 🔷 GCP Certificate Manager Object Hierarchy

```
DNS Authorization
  └── proves domain ownership via ACME challenge

Certificate
  ├── linked to DNS Authorization
  ├── covers: *.<domain> (wildcard)
  └── states: PROVISIONING → AUTHORIZED + ACTIVE

Certificate Map
  └── Certificate Map Entry
        ├── links certificate to hostname
        └── referenced by HTTPS Proxy
```

***

## 🔷 HTTP vs. HTTPS Proxy Comparison

```
HTTP PROXY:                     HTTPS PROXY:
  port 80                         port 443
  no certificate                  certificate map required
  unencrypted                     TLS termination
  same URL map ──────────────── same URL map
  same backend service ──────── same backend service
```

***

## 🔷 DNS Records Created in GoDaddy (Total for Project)

```
RECORD    NAME                         VALUE                    PURPOSE
──────    ──────────────────           ──────────────────       ──────────────────
CNAME     _acme-challenge.<sub>       <GCP challenge data>     Certificate validation
A         vpro-gcp                    <LB static IP>           Domain → Load Balancer
```

***

## 🔷 Trailing Dot Warning

```
GCP describe output may include trailing dots:
  name: _acme-challenge.gcp.hkhinfotech.xyz.    ← REMOVE dot
  data: xxxxxxxxxxxxxxxxxxxxx.                    ← REMOVE dot

GoDaddy will FAIL to resolve records with trailing dots.
Always strip trailing dots when copy-pasting from GCP to GoDaddy.
```

***

## 🔷 Complete gcloud Commands Sequence

```bash
# 1. DNS Authorization
gcloud certificate-manager dns-authorizations create auth-<sub> --domain=<domain>
gcloud certificate-manager dns-authorizations describe auth-<sub>

# 2. [Manual: create CNAME in GoDaddy]

# 3. Certificate
gcloud certificate-manager certificates create cert-<sub> \
  --domains="*.<domain>" --dns-authorizations=auth-<sub>

# 4. Certificate Map + Entry
gcloud certificate-manager maps create <map-name>
gcloud certificate-manager maps entries create <entry> \
  --map=<map-name> --certificates=cert-<sub> --hostname=<hostname>

# 5. Verify
gcloud certificate-manager certificates describe cert-<sub>

# 6. HTTPS Proxy
gcloud compute target-https-proxies create vprofile-https-proxy \
  --url-map=<url-map> --certificate-map=<map-name>

# 7. HTTPS Forwarding Rule
gcloud compute forwarding-rules create <rule-name> \
  --target-https-proxy=vprofile-https-proxy --address=<ip-name> --global

# 8. Get LB IP + create A-record in GoDaddy
gcloud compute addresses describe <ip-name> --global
```

***

## 🔷 Verification Checklist

```
✅ DNS Authorization: describe shows dnsResourceRecord
✅ CNAME record: created in GoDaddy (no trailing dots)
✅ Certificate: status AUTHORIZED, state ACTIVE
✅ Certificate Map: created with entry linked to cert + hostname
✅ HTTPS Proxy: created with URL map + certificate map
✅ HTTPS Forwarding Rule: created with static IP
✅ A-Record: created in GoDaddy (subdomain → LB IP)
✅ Browser: https://subdomain.domain loads with padlock
✅ Certificate: issued by Google Trust Services
```

***

## 🔷 Reusable Engineering Pattern: Certificate-Secured Service Endpoint

```
PATTERN: Domain Ownership Proof → Certificate → TLS Termination → DNS Resolution

1. PROVE OWNERSHIP
   Challenge-response via DNS record (ACME protocol)
   CA provides challenge → you create DNS record → CA verifies

2. ISSUE CERTIFICATE
   CA signs certificate for your domain
   Certificate = cryptographic proof of domain identity

3. ATTACH TO PROXY/LB
   Certificate enables TLS termination at the edge
   Proxy decrypts HTTPS → forwards plain HTTP to backend

4. DNS RESOLUTION
   A-record points domain to load balancer IP
   Users access via https://domain → LB → backend

This pattern is IDENTICAL across clouds:
  AWS:  ACM certificate → ALB HTTPS listener → Route 53 A-record
  GCP:  Certificate Manager → HTTPS proxy → GoDaddy A-record
  Azure: App Service certificate → Application Gateway → Azure DNS

The components differ, the pattern is the same:
  prove → certify → terminate TLS → resolve DNS
```

This lecture completes the project's security layer — the application is now accessible over a trusted HTTPS connection with a domain name, matching production standards. [\[300-ssl-ce...-dns-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/300-ssl-certificates-https-and-final-dns-setup.txt)
