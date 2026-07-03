# 🎓 Deep Learning Material: Kubernetes Ingress — External Access, Routing Rules & NGINX Controller

**Source:** [339-ingress.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339-ingress.txt?EntityRepresentationId=de86cee6-05fa-43ae-a23c-7d65417390cf) (video caption) + [339.ingress.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339.ingress.txt?EntityRepresentationId=304dd022-884d-42e4-ac03-ce8cf8f6d008) (steps/commands reference) — Video lecture covering Kubernetes Ingress: why Services alone are insufficient for external access, what Ingress is (Layer 7 routing rules for HTTP/HTTPS), the NGINX Ingress Controller (a Pod + Network Load Balancer), the full setup flow (controller → deployment → service → DNS CNAME → ingress rules), path-based and host-based routing, and the complete live execution with the vProfile Tomcat application on AWS/kops. [\[339-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339-ingress.txt), [\[339.ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339.ingress.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 Why Services Are Not Enough

In previous lectures, Kubernetes Services of type **NodePort** and **LoadBalancer** were used to expose applications externally. These work, but they operate at **Layer 4** (TCP/UDP level) — they route traffic based on port numbers only. When you have many applications, especially **microservices**, you need routing decisions based on **URL paths** (e.g., `/api` goes to one service, `/web` goes to another) or **hostnames** (e.g., `app1.example.com` vs `app2.example.com`). Services cannot do this. They can only forward traffic from one port to one backend. [\[339-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339-ingress.txt)

This is the gap Ingress fills. It operates at **Layer 7** (HTTP/HTTPS level), understanding URL paths, hostnames, and HTTP methods, and routing traffic to different internal Services based on configurable rules. [\[339-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339-ingress.txt)

***

## 1.2 What Ingress Is

Ingress is a Kubernetes **API object** (like Pod, Service, Deployment) that manages **external access to services in a cluster**, specifically HTTP and HTTPS traffic. Think of it as a **load balancer with routing rules** that sits in front of your internal Services. [\[339-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339-ingress.txt)

The architecture is layered:

```
User → Ingress (routing rules) → Service (ClusterIP) → Pod
```

The Service in this architecture is of type **ClusterIP** — a purely internal service with no external exposure. Ingress is what exposes it to the outside world. This is a key architectural point: the Service handles internal discovery and load balancing to Pods, while Ingress handles external routing and access control. [\[339-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339-ingress.txt)

Ingress can provide:

* **Load balancing** — distributing traffic across backend Pods.
* **SSL termination** — handling HTTPS connections at the Ingress level so that internal Kubernetes traffic doesn't need SSL certificates. "So the HTTPS based access, you can terminate the SSL connection on the ingress. So internally in Kubernetes, you don't need to handle it." [\[339-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339-ingress.txt)
* **Path-based routing** — different URL paths go to different Services.
* **Host-based routing** — different domain names go to different Services.

***

## 1.3 Ingress vs Ingress Controller — Two Separate Things

This is a critical distinction that causes confusion:

**Ingress** (the object) is a **set of rules** — a YAML definition that says "if the user accesses this host on this path, route to this service." It is just configuration. By itself, it does nothing. [\[339-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339-ingress.txt)

**Ingress Controller** is the **engine** that reads those rules and actually performs the routing. It is a running Pod (typically NGINX) that acts as a reverse proxy, plus a Service of type LoadBalancer that provides the external entry point. Without an Ingress Controller installed, Ingress rules have no effect. [\[339-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339-ingress.txt)

The instructor states: "You need an ingress controller" as a prerequisite. There are many types: NGINX (most common), Traefik, Ambassador, Contour, HAProxy, and cloud-specific controllers like AKS Application Gateway (Azure). The video uses the **NGINX Ingress Controller**. [\[339-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339-ingress.txt)

🔍 **Deep Dive**
When the NGINX Ingress Controller is installed on AWS, it creates:

* A **namespace** called `ingress-nginx`.
* **Pods** — three pods including the NGINX controller pod itself.
* A **Service of type LoadBalancer** — which provisions an AWS **Network Load Balancer** (NLB). Users access this NLB, and the controller routes requests based on Ingress rules.
* **Deployments**, **ReplicaSets**, and **Jobs** for managing the controller lifecycle.
* A **Target Group** in AWS pointing to the worker nodes on a NodePort.

The instructor verifies this by checking `kubectl get all -n ingress-nginx` and also verifying the NLB creation in the AWS console. [\[339-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339-ingress.txt)

***

## 1.4 The Ingress Definition File — Rules Configuration

An Ingress definition file has the standard four Kubernetes keys (`apiVersion`, `kind`, `metadata`, `spec`) with `kind: Ingress`. The `spec` section contains **rules**: [\[339.ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339.ingress.txt)

```yaml
kind: Ingress
metadata:
  name: vpro-ingress
  annotations:
    nginx.ingress.kubernetes.io/use-regex: "true"
spec:
  ingressClassName: nginx
  rules:
    - host: vprofile.groophy.in
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: my-app
                port:
                  number: 8080
```

 [\[339.ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339.ingress.txt)

**Key elements:**

**`ingressClassName: nginx`** — Specifies which Ingress Controller should handle these rules. If you have multiple controllers installed, this field selects the right one. [\[339-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339-ingress.txt)

**`rules`** — A list of routing rules. Each rule specifies:

* **`host`** — the domain name (e.g., `vprofile.groophy.in`). The request must arrive with this hostname.
* **`http.paths`** — a list of path-based routes. Each path specifies:
  * **`path`** — the URL path (e.g., `/`, `/login`, `/api`).
  * **`pathType`** — how the path is matched (`Prefix` means "starts with").
  * **`backend.service`** — which internal Service to route to, and on which port.

**`annotations`** — Controller-specific configuration. `nginx.ingress.kubernetes.io/use-regex: "true"` enables regex matching in paths (NGINX-specific). [\[339.ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339.ingress.txt)

The instructor emphasizes a mental model: **"We create Ingress for the Service."** When thinking about Ingress, focus on the Service — not the Pod, not the Deployment. The Ingress rule routes traffic to a Service, and the Service routes to Pods. Keep this clean separation in mind. [\[339-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339-ingress.txt)

***

## 1.5 Two Types of Routing Rules

### Path-Based Routing

Different URL paths route to different Services. If the user accesses `/api`, it goes to the API service. If they access `/web`, it goes to the web service. Multiple path entries under the same host create this behavior. [\[339-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339-ingress.txt)

### Host-Based Routing

Different domain names route to different Services. If the user accesses `app1.example.com`, it goes to service A. If they access `app2.example.com`, it goes to service B. Multiple rule entries with different `host` values create this behavior. [\[339-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339-ingress.txt)

The video demonstrates **both**: the host is `vprofile.groophy.in` and the path is first set to `/login` (then corrected to `/`). The instructor references the microservices architecture from earlier lectures where an API gateway (NGINX) routes `/api` to one backend and `/` to another — Ingress replaces that manual API gateway configuration with declarative Kubernetes rules. [\[339-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339-ingress.txt)

***

## 1.6 The `/login` vs `/` Path Lesson

The video demonstrates a live debugging moment. Initially, the Ingress path is set to `/login`. When accessed, the page loads but without CSS/images — because the vProfile application handles internal routing (it redirects `/` to `/login` itself). By setting the Ingress path to `/login`, only requests to exactly that path are forwarded, but the application's static resources (loaded from `/` and other paths) are not routed. [\[339-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339-ingress.txt)

The fix: change the path to `/` (root), which forwards **all** requests to the backend. The application handles its own internal routing from there. The instructor explains: "I don't need to mention /login because that application already routes it internally." [\[339-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339-ingress.txt)

This teaches an important rule: **Ingress path routing is for routing between different services (microservices), not for routing within a single application's internal paths.** If the application handles its own routing, set the Ingress path to `/`. Path-based routing at the Ingress level is for when different URL paths should go to entirely different backend services. [\[339-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339-ingress.txt)

***

## 1.7 The DNS CNAME Record

The Ingress Controller's NLB has an AWS DNS endpoint (a long `.elb.amazonaws.com` URL). To access the application via a human-readable domain name, you create a **CNAME record** in your domain registrar (GoDaddy in this case) that maps your desired hostname to the NLB's DNS endpoint. [\[339-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339-ingress.txt)

For example: `vprofile.groophy.in → CNAME → <NLB-endpoint>.elb.amazonaws.com`

This is different from the GCP project where a static IP was used with an A record. AWS NLBs provide DNS endpoints (not static IPs by default), so CNAME is the appropriate record type. [\[339-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339-ingress.txt)

⚠️ **Expert Note**
DNS records take time to propagate across the internet. The instructor pre-creates the CNAME record before showing the setup because of this delay: "I already created this record because it takes time to update over the internet." When testing, if the domain doesn't resolve immediately, wait. Also: "Make sure there is no extra full stop or anything at the end" of the NLB endpoint — a common copy-paste error. [\[339-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339-ingress.txt)

***

## 1.8 Project Context — Controller Already Exists

In a real project environment, the Ingress Controller and DNS records are **already set up** by the platform/infrastructure team. As a developer or DevOps engineer deploying a new application, you only need to: create your Deployment, create your ClusterIP Service, and create an Ingress rule for your Service. The instructor states: "If you're working in a project, controller will be already there and you will be adding new apps." [\[339-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339-ingress.txt)

***

## 1.9 Cost Warning — Network Load Balancer

The NGINX Ingress Controller creates an AWS Network Load Balancer, which is **not free**. After completing the exercise, you must delete the controller. Two deletion methods are shown: deleting the entire `ingress-nginx` namespace (`kubectl delete ns ingress-nginx`), or deleting via the same manifest used for installation (`kubectl delete -f <URL>`). Both remove the NLB and stop charges. [\[339-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339-ingress.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are setting up external HTTP access to the vProfile Tomcat application running in a Kubernetes cluster on AWS, using an NGINX Ingress Controller. The final outcome: users access `vprofile.groophy.in` in their browser → DNS resolves to the NLB → NGINX Ingress Controller routes the request based on rules → ClusterIP Service → vProfile Pod → login page appears. [\[339-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339-ingress.txt)

***

## The Six-Step Flow

```
1. Create Controller → 2. Create Deployment → 3. Create Service →
4. Create DNS CNAME → 5. Create Ingress → 6. Test
```

 [\[339.ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339.ingress.txt)

***

## Step 1: Install the NGINX Ingress Controller

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.1.3/deploy/static/provider/aws/deploy.yaml
```

 [\[339.ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339.ingress.txt)

| Part               | Meaning                                                                                                |
| ------------------ | ------------------------------------------------------------------------------------------------------ |
| `kubectl apply -f` | Create objects from a manifest file                                                                    |
| URL                | Remote manifest containing all controller resources (namespace, pods, service, deployment, RBAC, jobs) |
| `provider/aws`     | AWS-specific configuration (creates NLB, not just a generic LB)                                        |

**What happens internally:** Creates the `ingress-nginx` namespace, deploys the NGINX controller pods, creates a Service of type LoadBalancer (which provisions an AWS NLB), sets up RBAC permissions, and runs admission webhook jobs. [\[339-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339-ingress.txt)

**Verify:**

```bash
kubectl get ns
```

You should see `ingress-nginx` in the namespace list. [\[339-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339-ingress.txt)

```bash
kubectl get all -n ingress-nginx
```

You should see: pods (3), a service of type LoadBalancer with an external endpoint, deployments, replica sets, and jobs. [\[339-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339-ingress.txt)

Also check the **AWS console** → EC2 → Load Balancers. You should see a new Network Load Balancer being provisioned with a target group pointing to your worker nodes. [\[339-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339-ingress.txt)

**Wait** for the NLB health checks to pass (targets show "healthy") before proceeding.

***

## Step 2: Create the Deployment

```bash
vim vprodep.yaml
```

Content:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  selector:
    matchLabels:
      run: my-app
  replicas: 1
  template:
    metadata:
      labels:
        run: my-app
    spec:
      containers:
        - name: my-app
          image: imranvisualpath/vproappfix
          ports:
            - containerPort: 8080
```

 [\[339.ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339.ingress.txt)

Apply it:

```bash
kubectl apply -f vprodep.yaml
```

This creates one Pod running the vProfile Tomcat image on port 8080. Use your own Docker Hub image if you built one during containerization. [\[339-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339-ingress.txt)

***

## Step 3: Create the ClusterIP Service

```bash
vim vprosvc.yaml
```

Content:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app
spec:
  ports:
    - port: 8080
      protocol: TCP
      targetPort: 8080
  selector:
    run: my-app
  type: ClusterIP
```

 [\[339.ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339.ingress.txt)

Apply it:

```bash
kubectl apply -f vprosvc.yaml
```

**Verify the Service is working:**

```bash
kubectl get svc
kubectl describe svc my-app
```

The `describe` output must show **Endpoints** — the Pod IP and port (e.g., `10.244.x.x:8080`). If Endpoints is empty, the selector doesn't match the Pod labels. The Service must be in a working state before creating Ingress rules for it. [\[339-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339-ingress.txt)

***

## Step 4: Create DNS CNAME Record

**4a. Copy the NLB DNS endpoint:**

Go to AWS Console → EC2 → Load Balancers → copy the DNS name (e.g., `a1b2c3...elb.amazonaws.com`). [\[339-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339-ingress.txt)

**4b. Create the CNAME record in your domain registrar:**

In GoDaddy (or your provider): Add Record → Type: CNAME → Name: `vprofile` (or your chosen subdomain) → Value: paste the NLB DNS endpoint. [\[339-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339-ingress.txt)

⚠️ **No extra characters.** No trailing period, no extra spaces. Just the clean NLB endpoint. [\[339-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339-ingress.txt)

**4c. Wait** for DNS propagation (can take minutes to hours). The instructor pre-created this record for the demo. [\[339-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339-ingress.txt)

***

## Step 5: Create the Ingress Rule

```bash
vim vproingress.yaml
```

Content:

```yaml
kind: Ingress
metadata:
  name: vpro-ingress
  annotations:
    nginx.ingress.kubernetes.io/use-regex: "true"
spec:
  ingressClassName: nginx
  rules:
    - host: vprofile.groophy.in
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: my-app
                port:
                  number: 8080
```

 [\[339.ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339.ingress.txt)

**Replace `vprofile.groophy.in`** with your own domain/subdomain. Replace `my-app` and `8080` with your Service name and port if different.

Apply it:

```bash
kubectl apply -f vproingress.yaml
```

**Verify:**

```bash
kubectl get ingress
```

You should see the Ingress with the host and the NLB address. Use `--watch` to wait for the address to populate:

```bash
kubectl get ingress --watch
```

 [\[339-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339-ingress.txt), [\[339.ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339.ingress.txt)

***

## Step 6: Test in Browser

Navigate to `http://vprofile.groophy.in` (your domain). The vProfile login page should appear. [\[339-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339-ingress.txt)

**If the page loads but without CSS/images:** Your Ingress path might be set to `/login` instead of `/`. The application handles internal routing — set the Ingress path to `/`. [\[339-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339-ingress.txt)

**To fix:**

```bash
kubectl delete ingress vpro-ingress
```

Edit `vproingress.yaml` — change `path: /login` to `path: /`. Re-apply:

```bash
kubectl apply -f vproingress.yaml
```

 [\[339.ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339.ingress.txt)

***

## Step 7: Clean Up (IMPORTANT — Cost)

**Method 1 — Delete the namespace:**

```bash
kubectl delete ns ingress-nginx
```

Deletes everything in the namespace including the controller, pods, and the NLB. [\[339-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339-ingress.txt)

**Method 2 — Delete via manifest:**

```bash
kubectl delete -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.1.3/deploy/static/provider/aws/deploy.yaml
```

Reads the same manifest and deletes everything it created. Takes time to wait for NLB deletion. [\[339.ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339.ingress.txt)

⚠️ **Do not skip this.** The NLB incurs hourly charges. [\[339-ingress \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/339-ingress.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Ingress Architecture

```
INTERNET
  │
  │  DNS CNAME: vprofile.groophy.in → NLB endpoint
  │
  ▼
┌──────────────────────────────────────────┐
│  AWS Network Load Balancer               │
│  (created by ingress controller service) │
└──────────────┬───────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│  NGINX Ingress Controller (Pod)          │
│  namespace: ingress-nginx                │
│                                          │
│  RULES (from Ingress object):            │
│    host: vprofile.groophy.in             │
│      path: / → service: my-app:8080     │
└──────────────┬───────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│  Service: my-app (ClusterIP)             │
│  port: 8080 → targetPort: 8080          │
│  selector: run=my-app                    │
└──────────────┬───────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│  Pod: my-app (Tomcat:8080)               │
│  image: imranvisualpath/vproappfix       │
└──────────────────────────────────────────┘
```

***

## Ingress vs Ingress Controller

```
Ingress Object     = RULES (YAML config: host, path → service)
                     kind: Ingress
                     Does nothing alone

Ingress Controller = ENGINE (running Pod: NGINX)
                     + Service type LoadBalancer (NLB on AWS)
                     Reads rules, performs routing
                     MUST be installed first
```

***

## Six-Step Setup Flow

```
1. Install Controller     kubectl apply -f <controller-manifest-URL>
     ↓
2. Create Deployment      kubectl apply -f vprodep.yaml
     ↓
3. Create Service          kubectl apply -f vprosvc.yaml (ClusterIP)
     ↓                     verify: kubectl describe svc → Endpoints exist
4. Create DNS CNAME       domain registrar → hostname → NLB endpoint
     ↓
5. Create Ingress         kubectl apply -f vproingress.yaml
     ↓
6. Test                   browser → http://hostname → app loads

In real projects: steps 1 + 4 already done by platform team
You only do: 2 + 3 + 5
```

***

## Routing Types

```
PATH-BASED:
  /api   → api-service
  /web   → web-service
  /      → default-service

HOST-BASED:
  app1.example.com → service-a
  app2.example.com → service-b

Both can be combined in a single Ingress definition
```

***

## Ingress Rule Structure

```yaml
rules:
  - host: <domain>           ← hostname match
    http:
      paths:
        - path: /             ← URL path match
          pathType: Prefix    ← matching strategy
          backend:
            service:
              name: <svc>     ← ClusterIP service name
              port:
                number: 8080  ← service port
```

***

## Mental Model

```
"We create Ingress FOR the Service"

Focus chain:  Ingress → Service → Pod
                         ↑
              Think about THIS when writing Ingress rules

Service MUST be working (endpoints visible) BEFORE creating Ingress
```

***

## Path Routing Lesson

```
path: /login  → only /login forwarded → app's CSS/images on / NOT routed → broken
path: /       → ALL paths forwarded → app handles internal routing → works

Rule: Use / for single applications
      Use specific paths (/api, /web) for microservices routing between services
```

***

## Controller Internals (AWS)

```
kubectl apply -f <controller-URL> creates:
  Namespace:   ingress-nginx
  Pods:        3 (controller + admission webhook + jobs)
  Service:     type LoadBalancer → provisions AWS NLB
  Deployment:  manages controller pod
  Target Group: worker nodes on NodePort
```

***

## DNS Configuration

```
AWS NLB provides: DNS endpoint (not static IP)
  → CNAME record (not A record)
  → hostname → NLB endpoint

GoDaddy: Add Record → CNAME → name: vprofile → value: <NLB-endpoint>
⚠️ No trailing period, no extra spaces
⚠️ DNS propagation takes time
```

***

## Cleanup Commands

```bash
# Method 1: Delete namespace (quick)
kubectl delete ns ingress-nginx

# Method 2: Delete via manifest (precise)
kubectl delete -f <controller-manifest-URL>

⚠️ NLB costs money → ALWAYS clean up after testing
```

***

## Layer Comparison

```
Service (NodePort/LB):   Layer 4 — routes by PORT only
Ingress:                  Layer 7 — routes by HOST + PATH + HTTP rules

Service alone:   1 port → 1 backend
Ingress:         1 entry point → many backends via rules
```

***

## Key Engineering Patterns

| Pattern                                   | Manifestation                                                                                  |
| ----------------------------------------- | ---------------------------------------------------------------------------------------------- |
| **Rules object + Controller engine**      | Ingress = declarative rules; Controller = execution engine — separation of config from runtime |
| **Layer 7 over Layer 4**                  | Ingress adds HTTP-level intelligence on top of TCP-level Services                              |
| **ClusterIP + Ingress**                   | Internal services exposed externally via Ingress — no NodePort/LB needed per service           |
| **Single entry point, multiple backends** | One NLB → one controller → many services via path/host rules                                   |
| **Microservices routing pattern**         | Path-based routing replaces manual API gateway configuration                                   |
| **Platform vs application concern**       | Controller + DNS = platform team; Deployment + Service + Ingress rules = app team              |
| **Apply/Delete symmetry**                 | Same manifest URL used for both `apply` (create) and `delete` (cleanup)                        |

***

## Project Continuity

```
BEFORE: Pods, Services (NodePort, LoadBalancer, ClusterIP), Deployments
THIS:   Ingress — Layer 7 routing, NGINX controller, path/host-based rules
NEXT:   More Kubernetes objects (ConfigMaps, Secrets, Volumes, etc.)
```

***

This completes the full reconstruction. **Theory** explains the Ingress concept, the controller/rules separation, and both routing types. **Practical** walks through all six steps with exact commands, verification, and the `/login` vs `/` debugging lesson. The **Compression Map** gives you the architecture diagram, the six-step flow, and the routing rule template for instant recall. Let me know if you'd like Anki flashcards or any section expanded! 🚀
