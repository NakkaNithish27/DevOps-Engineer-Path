# 🎓 Deep Learning Material: Configuring the GCP Global HTTP/HTTPS Load Balancer

**Source:** [299-configuring-the-global-http-https-load-balancer.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/299-configuring-the-global-http-https-load-balancer.txt?EntityRepresentationId=72c949c4-e970-4963-afe5-ca8c99fe4996) — Video lecture covering the complete configuration of a GCP Global Application Load Balancer: setting named ports on the MIG, creating health checks, creating and attaching the backend service, creating the URL map, creating the target HTTP proxy, reserving a static public IP, creating the forwarding rule, and verifying the full end-to-end flow from browser to application to Cloud SQL and Memcache. [\[299-config...d-balancer \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/299-configuring-the-global-http-https-load-balancer.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 What We Are Connecting — The Backend-to-Frontend Chain

At this point in the project, the managed instance group (MIG) already exists. It auto-scales instances in the private subnet of the VPC, running the vProfile application on Tomcat at port 8080. But these instances have no public exposure — no traffic can reach them from the internet. The load balancer is the bridge. Its job is to receive internet traffic on a public IP and route it to the healthy instances in the MIG. [\[299-config...d-balancer \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/299-configuring-the-global-http-https-load-balancer.txt)

In GCP, the load balancer is not a single monolithic resource. It is assembled from **five distinct components**, each created separately and then connected:

1. **Named Ports** on the MIG (telling the LB which port the app listens on)
2. **Health Check** (probing instance health)
3. **Backend Service** (combining MIG + health check + port into a target)
4. **URL Map** (routing rules: which request goes to which backend)
5. **Target HTTP Proxy + Forwarding Rule** (the public-facing entry point)

The instructor explicitly compares this to AWS: in AWS, you create a target group (which bundles port + health check + instances) and an ALB listener — two main resources. In GCP, the same logical setup requires five separate resources connected together. The instructor acknowledges: "Little confusing compared to AWS, but doable." [\[299-config...d-balancer \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/299-configuring-the-global-http-https-load-balancer.txt)

***

## 1.2 Named Ports — Telling the Load Balancer About the MIG's Port

Before the load balancer can send traffic to the MIG, it needs to know **what port and protocol** the instances use. The MIG itself doesn't inherently advertise this information. You must explicitly set **named ports** on the MIG — a mapping that says: "The protocol name `http` corresponds to port `8080` on these instances." [\[299-config...d-balancer \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/299-configuring-the-global-http-https-load-balancer.txt)

This named port is referenced later when creating the backend service. The backend service uses the **name** (`http`), not the port number directly. This indirection allows the port number to be changed in one place (the named port definition) without updating every reference. [\[299-config...d-balancer \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/299-configuring-the-global-http-https-load-balancer.txt)

***

## 1.3 Health Check — Probing Instance Liveness

The health check is a standalone GCP resource. When created, it is **not attached to anything** — it is just a configuration that defines: what protocol to use (HTTP), what port to probe (8080), and what path to check (root `/`). The health check is configured as **global** because this is a global load balancer. [\[299-config...d-balancer \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/299-configuring-the-global-http-https-load-balancer.txt)

The health check only becomes active when it is referenced by a backend service. Once attached, GCP starts sending probe requests to each instance in the MIG at the specified port and path. If an instance responds successfully, it is marked **healthy** and receives traffic. If it fails, it is marked unhealthy and removed from rotation. [\[299-config...d-balancer \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/299-configuring-the-global-http-https-load-balancer.txt)

The port 8080 and path `/` are chosen because the vProfile application runs on Tomcat, which listens on 8080 and serves the application at the root path. The health check must match where the actual application responds — if the path were wrong (e.g., `/health` when no such endpoint exists), all instances would appear unhealthy even though they are running fine. [\[299-config...d-balancer \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/299-configuring-the-global-http-https-load-balancer.txt)

***

## 1.4 Backend Service — The GCP Equivalent of AWS Target Group

The **backend service** is the central organizing resource for the load balancer's backend. It is created as an empty container that references the health check and port name. Then, the MIG is **added** to the backend service in a separate command. [\[299-config...d-balancer \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/299-configuring-the-global-http-https-load-balancer.txt)

This two-step process (create empty backend → add MIG to backend) is important to understand. The backend service is not the MIG itself — it is a **wrapper** that:

* Knows which health check to use
* Knows which port name to use (the named port set on the MIG)
* Contains one or more instance groups (you could attach multiple MIGs from different zones for multi-zone load balancing)

In AWS terminology, the backend service is the **target group**. The instructor makes this comparison explicitly and repeatedly: "In the load balancing we have backend service as the target group." [\[299-config...d-balancer \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/299-configuring-the-global-http-https-load-balancer.txt)

After the MIG is attached, the backend service immediately starts using the health check to evaluate instance health. In the video, the instructor refreshes the console and sees "4 of 4 are healthy" — the health check probes are running and reporting status. The instructor notes that the MIG scaled to 4 instances (instead of the expected 2), but defers investigation to complete the setup first. [\[299-config...d-balancer \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/299-configuring-the-global-http-https-load-balancer.txt)

***

## 1.5 URL Map — The Layer 7 Routing Table

The URL map is the routing decision point. It is a table that maps incoming request patterns to backend services. When a request arrives, the URL map evaluates it and determines which backend service should handle it. [\[299-config...d-balancer \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/299-configuring-the-global-http-https-load-balancer.txt)

In this project, the URL map has a single **default service** — the backend service created in the previous step. This means: all requests, regardless of path, are routed to the same backend. However, the URL map architecture supports multiple entries — you could have `/api` going to one backend and `/static` going to another. This is what makes it a **Layer 7** load balancer. [\[299-config...d-balancer \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/299-configuring-the-global-http-https-load-balancer.txt)

The URL map is not directly exposed to the internet. It sits behind the **target proxy**, which is the actual frontend-facing component. [\[299-config...d-balancer \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/299-configuring-the-global-http-https-load-balancer.txt)

***

## 1.6 Target HTTP Proxy — The Frontend Face

The **target HTTP proxy** is GCP's way of creating the frontend listener for the load balancer. It is the component that receives incoming HTTP traffic and passes it to the URL map for routing decisions. The proxy is mapped to the URL map at creation time. [\[299-config...d-balancer \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/299-configuring-the-global-http-https-load-balancer.txt)

In AWS, this functionality is built into the ALB listener — you don't create a separate proxy resource. In GCP, it is a separate, explicit resource. For HTTPS, you would create a **target HTTPS proxy** instead (covered in the next lecture). The instructor notes: "This is what we need to do in GCP. We don't need to do this in the AWS load balancer. It comes built in." [\[299-config...d-balancer \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/299-configuring-the-global-http-https-load-balancer.txt)

***

## 1.7 Static Public IP — Why It Must Be Reserved

The load balancer needs a **static public IP** so that DNS can permanently point to it. If the IP were ephemeral (dynamic), it could change, and the DNS entry would become stale — users would get connection errors. [\[299-config...d-balancer \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/299-configuring-the-global-http-https-load-balancer.txt)

The static IP is reserved as a **global** address (because this is a global load balancer). Once reserved, it is attached to the forwarding rule. The IP is also used to create a DNS A record in the domain registrar (GoDaddy in this project): `vprogcp.hkhinfotek.xyz → <static IP>`. [\[299-config...d-balancer \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/299-configuring-the-global-http-https-load-balancer.txt)

***

## 1.8 Forwarding Rule — The Final Assembly Point

The **forwarding rule** is the last resource that brings everything together. It binds:

* The **static IP** (where internet traffic arrives)
* The **port** (80 for HTTP)
* The **target HTTP proxy** (which connects to the URL map, which connects to the backend, which connects to the MIG)

The forwarding rule's name becomes the **visible name of the load balancer** in the GCP console. Before the forwarding rule exists, the load balancer appears in the console with the URL map's name. After the forwarding rule is created, the proper load balancer name appears. [\[299-config...d-balancer \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/299-configuring-the-global-http-https-load-balancer.txt)

The forwarding rule is configured as **global** to match the global nature of the load balancer, the static IP, and the backend service. [\[299-config...d-balancer \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/299-configuring-the-global-http-https-load-balancer.txt)

🔍 **Deep Dive**
The use of a shell variable for the IP address (`$ELB_IP`) in the forwarding rule command is worth noting. The `gcloud compute addresses create` command creates the IP with a **name** (e.g., `vprofile-elb-ip`). The forwarding rule's `--address` flag takes this name, not the actual IP number. GCP resolves the name to the IP internally. The `describe` command is used separately to view the actual IP number for DNS configuration. [\[299-config...d-balancer \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/299-configuring-the-global-http-https-load-balancer.txt)

***

## 1.9 Verification — End-to-End Flow Confirmation

After the forwarding rule is created, the entire chain is active: internet → static IP → forwarding rule → HTTP proxy → URL map → backend service → MIG → healthy instances → Tomcat:8080 → vProfile application. [\[299-config...d-balancer \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/299-configuring-the-global-http-https-load-balancer.txt)

The instructor verifies by:

1. Accessing the load balancer IP in a browser → the vProfile login page appears.
2. Logging in with credentials (`admin_vp` / `admin_vp`) → successful login confirms **Cloud SQL** connectivity (the app reads user data from the database).
3. Clicking "All Users" → user list loads, confirming database reads.
4. Clicking a user ID → first access shows "data is from db and data is inserted in cache" (Cloud SQL read + Memcache write).
5. Clicking the same user again → shows "data is from cache" — confirming **Memorystore (Memcache)** connectivity and caching behavior. [\[299-config...d-balancer \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/299-configuring-the-global-http-https-load-balancer.txt)

This verification chain confirms: load balancer routing works, instances are healthy, the application starts correctly, Cloud SQL is accessible via VPC Peering, and Memcache is accessible via VPC Peering. The instructor notes that RabbitMQ/ElasticCache were not configured, but Memcache was. [\[299-config...d-balancer \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/299-configuring-the-global-http-https-load-balancer.txt)

⚠️ **Expert Note**
The instructor warns: "It will take some time. So if you don't see this, wait for some time. Make sure you check the health status of your instance group." The load balancer needs time to propagate the forwarding rule and for health checks to pass. If the page doesn't load immediately, the first troubleshooting step is to verify instance health in the MIG console, not to assume the configuration is wrong. [\[299-config...d-balancer \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/299-configuring-the-global-http-https-load-balancer.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are assembling the GCP Global Application Load Balancer by creating five resources in sequence — named ports, health check, backend service (with MIG attached), URL map, and target HTTP proxy with forwarding rule — then verifying the full end-to-end flow from browser to the vProfile application to Cloud SQL and Memcache. The final outcome: accessing the load balancer's public IP in a browser shows the vProfile login page, and login/data operations confirm database and cache connectivity. [\[299-config...d-balancer \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/299-configuring-the-global-http-https-load-balancer.txt)

***

## Step 1: Set Named Ports on the MIG

```bash
gcloud compute instance-groups managed set-named-ports vprofile-app01-mig \
  --zone=us-central1-a \
  --named-ports=http:8080
```

 [\[299-config...d-balancer \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/299-configuring-the-global-http-https-load-balancer.txt)

| Part                                     | Meaning                            |
| ---------------------------------------- | ---------------------------------- |
| `gcloud compute instance-groups managed` | Operate on managed instance groups |
| `set-named-ports`                        | Define a protocol-to-port mapping  |
| `vprofile-app01-mig`                     | The MIG name                       |
| `--zone=us-central1-a`                   | The zone where the MIG was created |
| `--named-ports=http:8080`                | Map the name `http` to port `8080` |

**What this does:** Tells the load balancer that instances in this MIG serve HTTP traffic on port 8080. This named port (`http`) will be referenced by the backend service.

**Expected output:** Confirmation that named ports are set.

***

## Step 2: Create the Health Check

```bash
gcloud compute health-checks create http vprofile-app01-hc \
  --global \
  --port=8080 \
  --request-path=/
```

 [\[299-config...d-balancer \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/299-configuring-the-global-http-https-load-balancer.txt)

| Part                        | Meaning                                     |
| --------------------------- | ------------------------------------------- |
| `health-checks create http` | Create an HTTP-type health check            |
| `vprofile-app01-hc`         | Name of the health check                    |
| `--global`                  | Global scope (matches global load balancer) |
| `--port=8080`               | Probe port 8080 (Tomcat)                    |
| `--request-path=/`          | Check the root path (no subfolders)         |

**What this does:** Creates a health check configuration. It is NOT attached to anything yet — it's a standalone definition.

**Verification:** Go to GCP Console → Compute Engine → Health Checks. You should see `vprofile-app01-hc` listed. At this point, "In use by" will be empty. [\[299-config...d-balancer \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/299-configuring-the-global-http-https-load-balancer.txt)

***

## Step 3: Create the Backend Service

```bash
gcloud compute backend-services create vprofile-app01-backend \
  --global \
  --protocol=HTTP \
  --port-name=http \
  --health-checks=vprofile-app01-hc
```

 [\[299-config...d-balancer \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/299-configuring-the-global-http-https-load-balancer.txt)

| Part                                | Meaning                                            |
| ----------------------------------- | -------------------------------------------------- |
| `backend-services create`           | Create a backend service                           |
| `vprofile-app01-backend`            | Name of the backend service                        |
| `--global`                          | Global scope                                       |
| `--protocol=HTTP`                   | Protocol for communication with instances          |
| `--port-name=http`                  | References the named port set on the MIG in Step 1 |
| `--health-checks=vprofile-app01-hc` | Attach the health check from Step 2                |

**What this does:** Creates an empty backend service with a health check attached. No instances are connected yet.

**Verification:** Go to Health Checks → `vprofile-app01-hc`. "In use by" should now show `vprofile-app01-backend`. Clicking it takes you to Load Balancing, where the backend service appears. [\[299-config...d-balancer \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/299-configuring-the-global-http-https-load-balancer.txt)

***

## Step 4: Attach the MIG to the Backend Service

```bash
gcloud compute backend-services add-backend vprofile-app01-backend \
  --global \
  --instance-group=vprofile-app01-mig \
  --instance-group-zone=us-central1-a
```

 [\[299-config...d-balancer \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/299-configuring-the-global-http-https-load-balancer.txt)

| Part                                  | Meaning                                              |
| ------------------------------------- | ---------------------------------------------------- |
| `add-backend`                         | Add an instance group to an existing backend service |
| `vprofile-app01-backend`              | The backend service to add to                        |
| `--instance-group=vprofile-app01-mig` | The MIG to attach                                    |
| `--instance-group-zone=us-central1-a` | Zone where the MIG lives                             |

**What this does:** Connects the MIG to the backend service. The health check immediately begins probing instances.

**Verification:** Refresh the load balancing page. The backend should now show the MIG with health status (e.g., "4 of 4 healthy"). [\[299-config...d-balancer \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/299-configuring-the-global-http-https-load-balancer.txt)

**Connection to larger flow:** The backend is now fully configured — MIG + health check + backend service. Next: create the frontend routing.

***

## Step 5: Create the URL Map

```bash
gcloud compute url-maps create vprofile-app01-url-map \
  --default-service=vprofile-app01-backend
```

 [\[299-config...d-balancer \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/299-configuring-the-global-http-https-load-balancer.txt)

| Part                                       | Meaning                                    |
| ------------------------------------------ | ------------------------------------------ |
| `url-maps create`                          | Create a URL map (routing table)           |
| `vprofile-app01-url-map`                   | Name of the URL map                        |
| `--default-service=vprofile-app01-backend` | All requests go to this backend by default |

**What this does:** Creates the routing table. All incoming requests are mapped to the backend service. For more complex setups, you could add path-based rules, but this project uses a single default route. [\[299-config...d-balancer \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/299-configuring-the-global-http-https-load-balancer.txt)

***

## Step 6: Create the Target HTTP Proxy

```bash
gcloud compute target-http-proxies create vprofile-app01-http-proxy \
  --url-map=vprofile-app01-url-map
```

 [\[299-config...d-balancer \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/299-configuring-the-global-http-https-load-balancer.txt)

| Part                               | Meaning                                   |
| ---------------------------------- | ----------------------------------------- |
| `target-http-proxies create`       | Create an HTTP proxy (frontend listener)  |
| `vprofile-app01-http-proxy`        | Name of the proxy                         |
| `--url-map=vprofile-app01-url-map` | Map this proxy to the URL map from Step 5 |

**What this does:** Creates the frontend-facing component that receives HTTP traffic and passes it to the URL map for routing. This is the GCP-specific resource that doesn't exist as a separate entity in AWS.

**Verification:** At this point, a load balancer entry should appear in the GCP console (Load Balancing page), showing as "Application Load Balancer" with the URL map name. [\[299-config...d-balancer \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/299-configuring-the-global-http-https-load-balancer.txt)

***

## Step 7: Reserve a Static Public IP

```bash
gcloud compute addresses create vprofile-elb-ip \
  --global
```

 [\[299-config...d-balancer \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/299-configuring-the-global-http-https-load-balancer.txt)

| Part               | Meaning                      |
| ------------------ | ---------------------------- |
| `addresses create` | Reserve a static IP address  |
| `vprofile-elb-ip`  | Name for the IP resource     |
| `--global`         | Global scope (for global LB) |

**View the actual IP:**

```bash
gcloud compute addresses describe vprofile-elb-ip --global
```

Note the IP address from the output — you'll need it for DNS configuration (GoDaddy A record). [\[299-config...d-balancer \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/299-configuring-the-global-http-https-load-balancer.txt)

***

## Step 8: Create the Forwarding Rule (Final Assembly)

```bash
gcloud compute forwarding-rules create vprofile-http-elb \
  --global \
  --target-http-proxy=vprofile-app01-http-proxy \
  --ports=80 \
  --address=vprofile-elb-ip
```

 [\[299-config...d-balancer \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/299-configuring-the-global-http-https-load-balancer.txt)

| Part                                            | Meaning                                           |
| ----------------------------------------------- | ------------------------------------------------- |
| `forwarding-rules create`                       | Create the entry point for traffic                |
| `vprofile-http-elb`                             | Name of the forwarding rule (becomes the LB name) |
| `--global`                                      | Global scope                                      |
| `--target-http-proxy=vprofile-app01-http-proxy` | Connect to the HTTP proxy from Step 6             |
| `--ports=80`                                    | Listen on port 80 (HTTP)                          |
| `--address=vprofile-elb-ip`                     | Use the static IP from Step 7                     |

**What this does:** This is the final piece that makes the load balancer functional. It binds the static IP + port 80 to the HTTP proxy, completing the chain: `IP:80 → proxy → URL map → backend → MIG → instances`.

**Note:** If you do NOT have a domain name, this is the last command. You can access the application via the static IP directly. HTTPS with a proper URL is covered in the next lecture. [\[299-config...d-balancer \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/299-configuring-the-global-http-https-load-balancer.txt)

***

## Step 9: Verify the Complete Setup

**9a. Access via browser:**

Navigate to `http://<static-IP>` in your browser. The vProfile login page should appear. If it doesn't, wait a few minutes — the load balancer needs time to propagate. [\[299-config...d-balancer \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/299-configuring-the-global-http-https-load-balancer.txt)

**9b. Verify Cloud SQL connectivity:**

Login with `admin_vp` / `admin_vp`. Successful login = application can read from Cloud SQL via VPC Peering. [\[299-config...d-balancer \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/299-configuring-the-global-http-https-load-balancer.txt)

**9c. Verify Memcache connectivity:**

Click "All Users" → click any user ID. First access shows: **"data is from db and data is inserted in cache"** (read from database, written to cache). Click the same user again: **"data is from cache"** (read from Memcache directly). [\[299-config...d-balancer \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/299-configuring-the-global-http-https-load-balancer.txt)

**Troubleshooting:**

| Symptom             | Check                                                          |
| ------------------- | -------------------------------------------------------------- |
| Page doesn't load   | Wait 2-5 minutes, then check MIG health status                 |
| Login fails         | Cloud SQL connectivity — verify VPC Peering is active          |
| Cache not working   | Memorystore connectivity — verify VPC Peering for Memcache     |
| Instances unhealthy | Check Tomcat is running on port 8080, health check path is `/` |

 [\[299-config...d-balancer \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/299-configuring-the-global-http-https-load-balancer.txt)

**Connection to larger flow:** The HTTP load balancer is now fully functional. The next lecture adds HTTPS with certificate termination and a proper domain URL.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Component Assembly Chain (Build Order)

```
Step 1: MIG set-named-ports (http:8080)
          ↓
Step 2: Health Check (HTTP, port 8080, path /)  [standalone, unattached]
          ↓
Step 3: Backend Service (references health check + port name)  [empty]
          ↓
Step 4: Add MIG to Backend Service  → health checks begin probing
          ↓
Step 5: URL Map (default-service → backend)  [routing table]
          ↓
Step 6: Target HTTP Proxy (references URL map)  [frontend listener]
          ↓
Step 7: Static Public IP (global)  [reserved for DNS]
          ↓
Step 8: Forwarding Rule (binds IP:80 → HTTP proxy)  [FINAL ASSEMBLY]
```

***

## Traffic Flow (Runtime)

```
Browser → http://<static-IP>:80
  → Forwarding Rule (port 80)
    → Target HTTP Proxy
      → URL Map (default → backend)
        → Backend Service
          → Health Check filters unhealthy
            → MIG (healthy instances only)
              → Instance (private subnet, Tomcat:8080)
                → vProfile App
                  → Cloud SQL (VPC Peering) + Memcache (VPC Peering)
```

***

## GCP LB Resources → AWS Equivalents

```
GCP                          AWS
──────────────────────       ──────────────────────
Named Ports on MIG           Target Group port config
Health Check                 Target Group health check
Backend Service              Target Group
URL Map                      Listener Rules
Target HTTP Proxy            (built into ALB listener)
Forwarding Rule              ALB Listener + LB itself
Static IP                    Elastic IP / ALB DNS

GCP: 5+ separate resources to create and connect
AWS: ~2 resources (target group + listener)
```

***

## Command Reference (All 8 Commands)

```bash
# 1. Named ports
gcloud compute instance-groups managed set-named-ports vprofile-app01-mig \
  --zone=us-central1-a --named-ports=http:8080

# 2. Health check
gcloud compute health-checks create http vprofile-app01-hc \
  --global --port=8080 --request-path=/

# 3. Backend service (empty)
gcloud compute backend-services create vprofile-app01-backend \
  --global --protocol=HTTP --port-name=http --health-checks=vprofile-app01-hc

# 4. Attach MIG to backend
gcloud compute backend-services add-backend vprofile-app01-backend \
  --global --instance-group=vprofile-app01-mig --instance-group-zone=us-central1-a

# 5. URL map
gcloud compute url-maps create vprofile-app01-url-map \
  --default-service=vprofile-app01-backend

# 6. HTTP proxy
gcloud compute target-http-proxies create vprofile-app01-http-proxy \
  --url-map=vprofile-app01-url-map

# 7. Static IP
gcloud compute addresses create vprofile-elb-ip --global

# 8. Forwarding rule
gcloud compute forwarding-rules create vprofile-http-elb \
  --global --target-http-proxy=vprofile-app01-http-proxy \
  --ports=80 --address=vprofile-elb-ip
```

***

## Resource Names Quick Reference

```
MIG:              vprofile-app01-mig          (zone: us-central1-a)
Health Check:     vprofile-app01-hc           (global, HTTP, 8080, /)
Backend Service:  vprofile-app01-backend      (global)
URL Map:          vprofile-app01-url-map
HTTP Proxy:       vprofile-app01-http-proxy
Static IP:        vprofile-elb-ip             (global)
Forwarding Rule:  vprofile-http-elb           (global, port 80)
```

***

## Resource Lifecycle States

```
Health Check:     created → unattached → attached to backend (Step 3)
Backend Service:  created empty → MIG added (Step 4) → health checks active
URL Map:          created → linked to backend
HTTP Proxy:       created → linked to URL map
Forwarding Rule:  created → binds IP + port + proxy → LB becomes ACTIVE

Nothing works until the forwarding rule connects everything
```

***

## Verification Sequence

```
1. Browser → http://<IP>          → vProfile login page loads
2. Login admin_vp/admin_vp        → Cloud SQL working (VPC Peering)
3. Click All Users → click user   → "data from db, inserted in cache"
4. Click same user again          → "data from cache" → Memcache working

If page doesn't load: wait 2-5 min + check MIG health status
```

***

## Conceptual Model: Two-Phase Create Pattern

```
BACKEND PHASE (Steps 1-4):
  Named ports → Health check → Backend service → Attach MIG
  Result: backend ready to receive traffic, health probes active

FRONTEND PHASE (Steps 5-8):
  URL map → HTTP proxy → Static IP → Forwarding rule
  Result: public entry point active, routes to backend

Backend MUST exist before frontend can reference it
```

***

## Key Engineering Patterns

| Pattern                               | Manifestation                                                                                           |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| **Decomposed assembly**               | LB is 5+ resources connected in sequence — each atomic, each independently inspectable                  |
| **Empty-then-attach**                 | Backend service created empty, then MIG added — same for health check (created, then referenced)        |
| **Named indirection**                 | Port is named (`http`), not numbered directly — name referenced by backend service, number lives on MIG |
| **Health-check-as-separate-resource** | Not embedded in backend — can be reused, inspected, and modified independently                          |
| **Global scope chain**                | Health check, backend, URL map, proxy, IP, forwarding rule — ALL global for a global LB                 |
| **Static IP for DNS stability**       | Ephemeral IP would break DNS — static IP reserved before forwarding rule                                |
| **Verify at each layer**              | Console checked after health check, after backend, after forwarding rule — incremental validation       |

***

## Project Continuity

```
BEFORE: VPC + PSA/Peering + Cloud SQL + Memcache + MIG (all configured)
THIS:   HTTP Load Balancer (backend + frontend) → app accessible on public IP
NEXT:   HTTPS termination with certificate + proper domain URL
AFTER:  Cleanup (destroy all resources)
```

***

This completes the full reconstruction. **Theory** explains each GCP load balancer component and how they connect. **Practical** gives you every `gcloud` command with breakdowns and the exact verification sequence. The **Compression Map** lets you reload the 8-step assembly chain, the traffic flow, and the complete command reference in under a minute. Let me know if you'd like Anki flashcards or any section expanded! 🚀
