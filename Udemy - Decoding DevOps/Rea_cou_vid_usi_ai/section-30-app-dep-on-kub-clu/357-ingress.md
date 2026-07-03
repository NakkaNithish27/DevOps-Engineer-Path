# ☸️ Kubernetes Ingress — Routing External Traffic to Internal Services — Deep Learning Material

**Source:** *Ingress* (Video Lecture Caption File) [\[357-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/357-ingress.txt)

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

## 1.1 The Problem — Internal Services Cannot Receive External Traffic

In the previous lectures, we created Kubernetes Services of type **ClusterIP**. A ClusterIP service provides a stable endpoint for pods — it acts as an internal load balancer, distributing traffic across pod replicas. But ClusterIP is **internal only**. It's accessible within the Kubernetes cluster but completely invisible to the outside world. [\[357-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/357-ingress.txt)

The vprofile application's Tomcat service needs to be **publicly accessible** — users from the internet need to reach it. The problem is: how do you connect external traffic from the internet to an internal ClusterIP service inside the Kubernetes cluster?

You could create a Service of type `LoadBalancer`, which provisions a cloud load balancer (like an AWS ALB) for each service. But this is wasteful — if you have 10 microservices, you'd create 10 separate load balancers, each with its own cost and management overhead. The real need is: **one external load balancer** with intelligent routing rules that direct traffic to different internal services based on the URL, hostname, or path. [\[357-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/357-ingress.txt)

***

## 1.2 Ingress Controller — The Bridge Between External and Internal

An **Ingress Controller** is a Kubernetes component that manages external access to services inside the cluster. It sits at the boundary between the internet and the cluster, performing two critical functions: [\[357-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/357-ingress.txt)

**1. It manages the external load balancer.** The Ingress Controller automatically creates and configures a cloud load balancer (like an AWS Application Load Balancer). You don't create the load balancer manually — the controller provisions it for you.

**2. It reads Ingress rules and configures routing.** You write Ingress objects (YAML definitions) that describe routing rules (hostname X goes to service A, path /videos goes to service B). The Ingress Controller reads these rules and configures the load balancer accordingly.

The instructor describes the architecture: "The ingress controller can set up that communication, can manage the external load balancer for you and connect it with the internal load balancer." The "internal load balancer" is the ClusterIP service. The "external load balancer" is the cloud ALB that the Ingress Controller creates. [\[357-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/357-ingress.txt)

The instructor uses the **NGINX Ingress Controller** — one of the most popular Ingress Controllers. Others exist (Traefik, HAProxy, AWS ALB Ingress Controller), but NGINX is widely used and well-documented.

🔍 **Deep Dive:**
The Ingress Controller is itself a set of pods running inside the Kubernetes cluster. When you install it, you apply a definition file that creates all the necessary pods, services, and configurations. The instructor notes: "Creating ingress controller is pretty easy. You download the definition file and simply run it. It creates all the pods and everything for it. Basically, it gives you a ready-made automated setup where you can just write the Ingress rule and decide what redirects where." The controller is infrastructure; the Ingress rules are your application-specific routing configuration.

***

## 1.3 The Traffic Flow — End to End

The complete traffic path for a request reaching the vprofile application: [\[357-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/357-ingress.txt)

```
User (internet) → Application Load Balancer (created by Ingress Controller)
  → Kubernetes Node → Ingress Controller (reads rules, routes request)
    → ClusterIP Service (vproapp-service) → Pod (Tomcat container)
```

The instructor highlights the key gap that Ingress fills: "We connect the application load balancer and forward the request to the node. But when it comes to the node, it does not know what to do with it." Without an Ingress Controller, traffic arriving at a node has no routing logic — it doesn't know which service to forward to. The Ingress Controller provides that routing intelligence. [\[357-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/357-ingress.txt)

***

## 1.4 Ingress Rules — Host-Based and Path-Based Routing

An **Ingress** is a Kubernetes object (kind: `Ingress`) that defines routing rules. Rules can be based on two dimensions: [\[357-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/357-ingress.txt)

**Host-based routing:** Route based on the hostname in the URL. If the request is for `vprofile.mydomain.com`, route to service A. If it's for `api.mydomain.com`, route to service B. The instructor creates a rule for `vprofile.mydomain.com` that routes to the `vproapp-service`.

**Path-based routing:** Route based on the URL path. Under the same hostname, `/videos` can go to one service while `/payment` goes to another. The instructor shows examples: `/bar` routes to service1, `/foo` routes to service2. [\[357-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/357-ingress.txt)

**Combined:** You can have both — hostname-based rules with path-based sub-routing under each hostname. This is extremely powerful for microservices architectures where many APIs need to be exposed through a single external endpoint.

The instructor emphasizes the microservices use case: "This is an amazing thing for microservices. In microservices, you have many APIs that you need to expose to the outside world. So you can have all those rules of your APIs, especially now, path-based. /videos goes here, /payment goes there, can have separate clusters of your services." [\[357-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/357-ingress.txt)

***

## 1.5 Ingress Object Structure

The Ingress object has a specific YAML structure: [\[357-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/357-ingress.txt)

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: vpro-ingress
  annotations: ...
spec:
  ingressClassName: nginx
  rules:
    - host: vprofile.mydomain.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: vproapp-service
                port:
                  number: 8080
```

**Key fields explained:**

**`apiVersion: networking.k8s.io/v1`** — Ingress is in the networking API group, not the core API.

**`ingressClassName: nginx`** — specifies which Ingress Controller should handle this rule. A cluster can have **multiple** Ingress Controllers (the instructor notes: "you can have multiple ingress controllers in your Kubernetes cluster"). The `ingressClassName` selects which one processes this particular Ingress object.

**`rules`** — a list of routing rules. Each rule has a `host` (optional — for hostname-based routing) and `http.paths` (for path-based routing within that host). [\[357-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/357-ingress.txt)

**`backend.service.name`** — the ClusterIP service to route traffic to. In this case, `vproapp-service` — the Tomcat service.

**`backend.service.port.number`** — the port on the service (8080 for Tomcat).

**`path: /`** — matches the root path. Since no additional paths are specified, all requests to the hostname are routed to this single backend. For microservices, you would add multiple paths (`/login`, `/videos`, `/payment`), each pointing to a different backend service. [\[357-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/357-ingress.txt)

***

## 1.6 DNS Configuration — Connecting the Domain to the Load Balancer

The instructor mentions a DNS step: after the Ingress Controller creates the ALB, you need to add a DNS record in your domain registrar (GoDaddy, Route53, etc.) that maps `vprofile.mydomain.com` to the ALB's endpoint. The instructor says: "We are going to add this rule in the GoDaddy, in the domain registrar, that this vprofile, this domain matches to the load balancer endpoint." [\[357-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/357-ingress.txt)

Without this DNS record, users can't reach the application by hostname — they'd need the raw ALB URL. The DNS record completes the chain: human-readable domain name → ALB → Ingress Controller → ClusterIP Service → Pod.

***

## 1.7 Ingress Controller vs. Ingress — Two Different Things

A common source of confusion: [\[357-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/357-ingress.txt)

**Ingress Controller** = the software component (a set of pods) that watches for Ingress objects and configures the load balancer accordingly. You install it once per cluster (or once per controller type). It's the **engine**.

**Ingress** = a Kubernetes object that defines routing rules. You create as many Ingress objects as you need — one per application or one per set of routes. It's the **configuration** that the engine reads.

The controller is the infrastructure; the Ingress objects are the rules. Without a controller, Ingress objects are just inert YAML — nothing reads or acts on them.

***

## 1.8 One Load Balancer, Many Rules — The Cost and Architecture Advantage

The instructor highlights a key architectural benefit: "Under same external load balancer, one external load balancer, you can have multiple rules like that set through ingress." Instead of one load balancer per service (expensive, hard to manage), you have one load balancer managed by the Ingress Controller, with all routing handled by Ingress rules. [\[357-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/357-ingress.txt)

This is the same concept as a reverse proxy (like Nginx in a traditional setup) — one entry point with routing rules that dispatch to different backend services. The Ingress Controller automates what you would manually configure in a reverse proxy.

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

## What We Are Building

We are writing an Ingress definition file that creates a routing rule: requests for `vprofile.mydomain.com` on path `/` are routed to the `vproapp-service` (Tomcat ClusterIP service) on port 8080. In the next lecture, we will install the NGINX Ingress Controller, apply this rule, and verify the full traffic flow from internet to pod. [\[357-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/357-ingress.txt)

***

## Step 1: Understand the Existing Service

Before writing the Ingress rule, confirm the target service exists. The Tomcat application is exposed through a ClusterIP service named `vproapp-service` on port 8080. This service was created in a previous lecture. [\[357-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/357-ingress.txt)

The Ingress rule will route external traffic **to this service**. The service, in turn, routes to the Tomcat pods using label selectors (as covered in the Service lecture).

***

## Step 2: Write the Ingress Definition File

Open the Ingress definition file:

```bash
vim appingress.yaml
```

Write the following content: [\[357-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/357-ingress.txt)

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: vpro-ingress
  annotations:
    nginx.ingress.kubernetes.io/... : ...
spec:
  ingressClassName: nginx
  rules:
    - host: vprofile.mydomain.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: vproapp-service
                port:
                  number: 8080
```

**Line-by-line breakdown:**

* `apiVersion: networking.k8s.io/v1` — the Ingress API version. Ingress is in the `networking.k8s.io` API group (not `v1` core API like Pods).

* `kind: Ingress` — the object type.

* `metadata.name: vpro-ingress` — a descriptive name for this Ingress object.

* `metadata.annotations` — the instructor refers to this as "the skeleton." Annotations provide additional configuration to the Ingress Controller (NGINX-specific settings like timeouts, SSL redirect behavior, etc.). [\[357-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/357-ingress.txt)

* `spec.ingressClassName: nginx` — selects the NGINX Ingress Controller. This field tells Kubernetes: "Use the NGINX controller to process this Ingress rule." If you had multiple controllers, this field determines which one handles this rule.

* `rules` — the list of routing rules. We have one rule.

* `host: vprofile.mydomain.com` — **host-based routing**. This rule applies only when the request's `Host` header matches this domain. **You must replace `mydomain.com` with your actual domain** — this domain will be configured in your DNS registrar to point to the ALB. [\[357-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/357-ingress.txt)

* `http.paths` — path-based routing within this host. We have one path.

* `path: /` — matches the root path (and all sub-paths with `Prefix` type). Since there's only one path rule, all requests to this hostname go to the same backend.

* `backend.service.name: vproapp-service` — the target ClusterIP service name. Must exactly match the service name from the service definition file.

* `backend.service.port.number: 8080` — the port on the service. Tomcat listens on 8080. [\[357-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/357-ingress.txt)

**Save the file.** This file will be committed to the source code repository and applied to the cluster in the next lecture.

***

## Step 3: Plan the DNS Configuration (Done in Next Lecture)

After the Ingress Controller creates the ALB, you will need to: [\[357-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/357-ingress.txt)

1. Get the ALB's DNS name/endpoint from the Ingress Controller
2. Go to your domain registrar (GoDaddy, Route53, etc.)
3. Create a CNAME record: `vprofile.mydomain.com` → `<ALB-DNS-name>`

This maps the human-readable hostname to the load balancer, completing the traffic chain.

***

## Step 4: Install the NGINX Ingress Controller (Done in Next Lecture)

The controller installation is a single `kubectl apply` command using a definition file provided by the NGINX project: [\[357-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/357-ingress.txt)

```bash
kubectl apply -f <nginx-ingress-controller-definition-URL>
```

This creates all the necessary pods, services, roles, and configurations for the NGINX Ingress Controller. Once running, the controller watches for Ingress objects and provisions/configures the ALB automatically.

***

## Step 5: Apply the Ingress Rule (Done in Next Lecture)

```bash
kubectl apply -f appingress.yaml
```

After this, the Ingress Controller reads the rule, configures the ALB to route `vprofile.mydomain.com` traffic to the `vproapp-service` on port 8080. [\[357-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/357-ingress.txt)

**Verification (to be done in next lecture):**

* Check the Ingress object: `kubectl get ingress`
* Check the ALB was created in AWS console
* Access `vprofile.mydomain.com` in a browser → application should appear

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

## The Core Problem and Solution

```
ClusterIP Service = internal only (pods ↔ pods)
  ↓ need external access
Ingress Controller = manages external load balancer
Ingress Object = routing rules (host/path → service)
  ↓ result
Internet → ALB → Ingress Controller → ClusterIP Service → Pod
```

## Full Traffic Flow

```
User browser
  → DNS: vprofile.mydomain.com → ALB endpoint
    → ALB (created by Ingress Controller, in AWS)
      → Kubernetes Node
        → Ingress Controller (reads rules, routes)
          → ClusterIP Service: vproapp-service:8080
            → Pod: Tomcat container

WITHOUT Ingress Controller:
  traffic arrives at node → "does not know what to do with it"
```

## Ingress Controller vs. Ingress Object

```
INGRESS CONTROLLER (infrastructure):
  - set of pods running in cluster
  - installed once (kubectl apply -f <definition-URL>)
  - manages external load balancer automatically
  - watches for Ingress objects and acts on them
  - example: NGINX Ingress Controller

INGRESS OBJECT (configuration):
  - YAML definition with routing rules
  - created per application / per route set
  - host-based routing (which domain?)
  - path-based routing (which URL path?)
  - points to backend ClusterIP services

Controller = engine
Ingress = rules the engine reads
Without controller → Ingress objects do nothing
```

## Routing Types

```
HOST-BASED:
  host: vprofile.mydomain.com → service A
  host: api.mydomain.com → service B

PATH-BASED:
  path: /videos → service C
  path: /payment → service D
  path: /login → service E

COMBINED:
  host: foo.bar.com
    /bar → service1
    /foo → service2
```

## Ingress YAML Structure

```yaml
apiVersion: networking.k8s.io/v1    ← networking API group
kind: Ingress
metadata:
  name: vpro-ingress
spec:
  ingressClassName: nginx            ← which controller handles this
  rules:
    - host: vprofile.mydomain.com    ← host-based routing
      http:
        paths:
          - path: /                  ← path-based routing
            backend:
              service:
                name: vproapp-service  ← target ClusterIP service
                port:
                  number: 8080         ← service port
```

## DNS Chain

```
Domain registrar (GoDaddy/Route53):
  vprofile.mydomain.com → CNAME → ALB DNS name

Without DNS record: must use raw ALB URL
With DNS record: users access via human-readable domain
```

## One Load Balancer, Many Rules

```
Traditional:
  Service A → Load Balancer A ($$)
  Service B → Load Balancer B ($$)
  Service C → Load Balancer C ($$)

With Ingress:
  Service A ─┐
  Service B ─┤→ ONE Load Balancer ($)
  Service C ─┘   (rules handle routing)

Cost efficient + centrally managed
```

## ingressClassName — Controller Selection

```
Cluster can have MULTIPLE ingress controllers:
  - nginx
  - traefik
  - aws-alb

ingressClassName: nginx → THIS rule is handled by NGINX controller
ingressClassName: traefik → THIS rule is handled by Traefik controller

Allows different controllers for different use cases
```

## Microservices Routing Pattern

```
ONE Ingress, MANY paths:
  /videos   → video-service pods
  /payment  → payment-service pods
  /auth     → auth-service pods
  /catalog  → catalog-service pods

ALL behind single ALB
Ingress rules = API gateway routing
```

## Setup Sequence (This + Next Lecture)

```
1. Write Ingress definition (appingress.yaml)     ← THIS LECTURE
2. Commit to source code repository
3. Launch Kubernetes cluster (kops)
4. Install NGINX Ingress Controller (kubectl apply)
5. Apply all definition files (kubectl apply -f)
6. Get ALB endpoint from Ingress
7. Add DNS CNAME record: domain → ALB
8. Access application via domain name
```

## Key Relationships

```
Ingress rule → references → ClusterIP Service (by name + port)
ClusterIP Service → selects → Pods (by label)
Ingress Controller → reads → Ingress rules
Ingress Controller → creates → ALB (automatically)
DNS record → maps → domain to ALB endpoint

Change service name in Ingress → must match actual service name
Wrong service name → 404 / 502 errors
```

## Reusable Engineering Patterns

**1. Reverse Proxy as Kubernetes-Native Object**

```
Traditional: Nginx reverse proxy config → upstream blocks → backends
Kubernetes:  Ingress object → rules → backend services

Same concept (single entry point, rule-based routing)
Different mechanism (declarative YAML vs. config files)
Ingress Controller automates what you'd manually configure
```

**2. Single Entry Point, Multiple Backends**

```
ONE external load balancer → MANY internal services
Routing logic in rules, not in infrastructure

Same pattern:
  AWS ALB listener rules (path/host → target groups)
  Nginx server blocks (location → proxy_pass)
  API Gateway (routes → lambda/services)
```

**3. Controller Pattern (Watch + Act)**

```
Ingress Controller continuously watches for Ingress objects
  → new Ingress created → controller configures ALB
  → Ingress updated → controller updates ALB
  → Ingress deleted → controller removes ALB config

Same pattern as:
  Deployment controller watches pods
  ReplicaSet controller watches replica count
  Any Kubernetes controller: watch desired state → reconcile actual state
```

***

*This completes the full reconstruction. Theory explains the gap between ClusterIP (internal) and external access, how the Ingress Controller bridges that gap, and the host-based and path-based routing models. Practical walks through writing the Ingress definition file and previews the DNS and controller installation steps. The Compression Map enables instant recall of the full traffic flow, the controller-vs-object distinction, and the single-entry-point routing pattern that makes Ingress essential for microservices architectures.* [\[357-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/357-ingress.txt)
