# 🎓 Deep Learning Material: Deploying the vProfile Application on a Kubernetes Cluster

**Source:** [359-deploy-app-on-k8s-cluster.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt?EntityRepresentationId=0a3297c0-2fd1-4f58-8b4f-dd01d1c7abab) (video caption) + [359.NginxIngressController.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359.NginxIngressController.txt?EntityRepresentationId=fccc8456-a69d-4dd0-8660-358ef282d6f2) (controller command) — Video lecture covering the complete end-to-end deployment of the vProfile application on a Kubernetes cluster: installing the NGINX Ingress Controller (which creates an ALB on AWS), creating the PVC (which provisions an EBS volume), deploying all manifests at once, validating every layer (pods, services, endpoints, PVC-to-EBS, ingress-to-ALB, DNS CNAME), troubleshooting techniques (describe, label selectors, delete-fix-recreate), and full application verification from browser through database and cache. [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt), [\[359.NginxI...Controller \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359.NginxIngressController.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 The Deployment Sequence — Why Order Matters

The deployment follows a strict dependency order. The **Ingress Controller** must be created first because it provisions the AWS Application Load Balancer (ALB), which takes time to become active. Then the **PVC** is created, which triggers the storage class to provision a 3GB EBS volume. Only after both the ALB is active and the PVC is available should the remaining manifests (deployments, services, ingress rules) be deployed. [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

The instructor explains the reasoning: the Ingress Controller creates the ALB and this load balancer needs to be in "active" status before the Ingress rules can map to it. The PVC needs to be "available" before the database deployment can mount it. Creating everything simultaneously would work (Kubernetes is eventually consistent), but waiting ensures you can verify each layer cleanly. [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

***

## 1.2 Storage Class — The Hidden Provisioner

When you create a PVC, the PVC itself doesn't create the EBS volume directly. A **Storage Class** does. The storage class is a Kubernetes object that acts as a **driver** — it defines the behind-the-scenes mechanism for provisioning volumes. [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

In a kops-created Kubernetes cluster on AWS, the default storage class uses the provisioner `ebs.csi.aws.com`. When a PVC references `storageClassName: default`, it tells the storage class to use this EBS CSI driver to create a 3GB EBS volume in the AWS account. You can see the storage class with `kubectl get sc`. [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

The instructor notes that you can reference the storage class by its actual name or by `default`, but warns: "This might change at the time you create the Kubernetes cluster with Kops, this might be a different name." The name depends on the cluster setup. In practice, the storage administrator manages the storage class — as a developer/DevOps engineer, you just need to know the storage class name to reference in your PVC. [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

🔍 **Deep Dive**
The PVC lifecycle: PVC created → storage class reads the claim → EBS CSI driver provisions an EBS volume in AWS → volume status becomes "available" → when a Pod mounts the PVC, the volume status changes to "in-use" and attaches to the worker node where the Pod is scheduled. You can verify the mapping by comparing the PVC ID (`kubectl get pvc`) with the EBS volume tags in the EC2 console — they should match. [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

***

## 1.3 Ingress Controller Creates the Load Balancer

The NGINX Ingress Controller deployment (`kubectl apply -f <URL>`) creates an **Application Load Balancer** (ALB) on AWS. This is visible in the AWS EC2 console under Load Balancers. The controller also creates a namespace `ingress-nginx` with pods, services, and other resources. [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

The ALB takes time to provision — the status transitions from "provisioning" to "active." The instructor waits for this before proceeding. Once active, the ALB has an endpoint URL that will be used in the DNS CNAME record. [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

***

## 1.4 Bulk Deployment with `kubectl create -f .`

Instead of applying each manifest individually, you can deploy all files in a directory at once using `kubectl create -f .` (the dot means current directory). Kubernetes reads every YAML file in the directory and creates all the objects. If a resource already exists (like the PVC created earlier), it throws an error for that specific resource but **continues creating the rest**. The error `DBPVC already exists` is expected and harmless. [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

After the bulk deployment, the instructor pauses for 10 minutes to allow all pods to pull images, start containers, and reach running state. [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

***

## 1.5 Service-to-Pod Validation — The Endpoint Check

The most important validation technique in this lecture: verifying that a Service is correctly connected to its Pod. This is done by checking **endpoints**. [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

When you run `kubectl describe svc <service-name>`, the output includes an `Endpoints` field. This field shows the **Pod IP address and container port** that the Service routes traffic to. If the Endpoints field is empty, the Service is NOT connected to any Pod — the most common cause is a **selector mismatch** (the label in the Service's selector doesn't match the label on the Pod). [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

The validation flow: get the Pod's IP with `kubectl describe pod <pod-name>` → note the IP. Then `kubectl describe svc <service-name>` → check Endpoints. The Pod IP should appear in the Endpoints list. If it matches, the Service is functional. If not, check the label selector. [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

***

## 1.6 Ingress Validation — ALB Mapping

The Ingress object's job is to **map the ALB endpoint to the Service**. When you run `kubectl get ingress`, you should see the host and the ALB address. Running `kubectl describe ingress <name>` shows the **backends** — the service name, port, and Pod IP addresses. [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

A critical operational detail: **you cannot access the application directly via the ALB endpoint URL.** The Ingress Controller checks the `host` field in the Ingress rule. If the incoming request's hostname doesn't match the rule's host, the request is rejected. The instructor demonstrates this: accessing the raw ALB endpoint shows a default page (not the app), but accessing `http://vprofile.hkhinfotek.xyz` (the configured hostname) works because it matches the Ingress rule. [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

The DNS CNAME record bridges this: `vprofile.hkhinfotek.xyz → CNAME → ALB endpoint`. When the user enters the hostname, DNS resolves it to the ALB, and the ALB forwards it to the Ingress Controller, which matches the hostname in the rule and routes to the correct Service. [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

***

## 1.7 The Delete-Fix-Recreate Workflow

When troubleshooting errors (wrong image name, wrong label, wrong configuration), you cannot simply edit most fields on a running Deployment. The correct workflow: [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

1. Identify the error using `kubectl describe pod <name>` → check Events section.
2. Fix the definition file (the YAML source code).
3. Delete the broken resource: `kubectl delete -f <filename>`.
4. Recreate it: `kubectl create -f <filename>` (or `kubectl apply -f <filename>`).

The instructor emphasizes: you cannot delete a Pod directly when it's managed by a Deployment — the Deployment will recreate it. You must delete the **Deployment** to stop the Pod from being recreated. Using `kubectl delete -f <deployment-file>` is the cleanest approach because it deletes whatever resource is defined in that specific file. [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

***

## 1.8 End-to-End Verification Chain

The instructor performs a complete verification of the entire stack by logging into the application:

1. **Ingress + DNS + ALB:** Accessing `http://vprofile.hkhinfotek.xyz` loads the login page → proves the full Ingress chain works.
2. **App Service + App Pod:** The login page renders → Tomcat is running, Service is routing correctly.
3. **DB Service + DB Pod + PVC/EBS:** Logging in with `admin_vp` succeeds → the application connected to MySQL, which read data from the EBS-backed PVC.
4. **RabbitMQ:** Clicking the RabbitMQ test shows "RabbitMQ initiated" → the MQ service and pod are working.
5. **Memcache:** Clicking "All Users" shows the user list. Clicking a user shows "data is inserted in cache." Clicking the same user again shows "data is coming from the cache" → Memcache service and pod are working, caching is functional. [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

The instructor notes: "From the user request till the storage EBS, we are verified by just logging in here." A single login action validates the entire chain: Ingress → Service → Pod → Database → Storage. [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

***

## 1.9 Real-World Perspective

The instructor closes with a real-world mapping: first you **containerize** the application (Dockerfiles + images), then you **write the Kubernetes manifests** (definition files), then you use tools like **Helm** and **CI/CD** for automation. This lecture completes the second step — the next steps (Helm, CI/CD) build on top of this foundation. [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are deploying the entire vProfile application stack (4 deployments, 4 services, 1 PVC, 1 secret, 1 ingress) onto a Kubernetes cluster on AWS, connecting it to an ALB via the NGINX Ingress Controller, configuring DNS, and verifying every layer from browser to storage. The final outcome: `http://vprofile.hkhinfotek.xyz` loads the vProfile app, login works (DB verified), caching works (Memcache verified), messaging works (RabbitMQ verified). [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

***

## Step 1: Install the NGINX Ingress Controller

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.1.3/deploy/static/provider/aws/deploy.yaml
```

 [\[359.NginxI...Controller \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359.NginxIngressController.txt)

**What happens:** Creates the `ingress-nginx` namespace, deploys the NGINX controller pods, creates a Service of type LoadBalancer which provisions an **AWS Application Load Balancer**. [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

**Verify namespace:**

```bash
kubectl get ns
```

You should see `ingress-nginx`. [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

**Verify pods are running:**

```bash
kubectl get all -n ingress-nginx
```

Some pods will show `Completed` (one-time jobs), and the controller pod should show `Running`. [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

**Verify ALB in AWS Console:**

Go to EC2 → Load Balancers. You should see a new ALB with status "provisioning." **Wait** until it changes to **"active"** before proceeding. [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

***

## Step 2: Create the PVC First (Separately)

Navigate to the kubedefs directory:

```bash
cd <repo>/kubedefs
```

Verify the PVC content:

```bash
cat db-pvc.yaml
```

Create the PVC:

```bash
kubectl create -f db-pvc.yaml
```

 [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

**Verify in Kubernetes:**

```bash
kubectl get pvc
```

Should show the PVC name, size (3GB), and status. [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

**Verify in AWS Console:**

Go to EC2 → Volumes. You should see a new 3GB EBS volume with a recent creation time. The PVC ID in the volume's tags should match the PVC name from `kubectl get pvc`. Status should be "available" (not yet attached to any instance). [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

**Connection:** When the database deployment runs and mounts this PVC, the EBS volume will be attached to the worker node running the database pod. [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

***

## Step 3: Deploy All Remaining Manifests at Once

Ensure the ALB is in "active" status, then:

```bash
kubectl create -f .
```

 [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

| Part                | Meaning                                 |
| ------------------- | --------------------------------------- |
| `kubectl create -f` | Create resources from files             |
| `.`                 | All YAML files in the current directory |

**Expected:** All resources are created. The PVC will throw an error (`already exists`) — this is expected and harmless. All other resources (deployments, services, secret, ingress) will be created. [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

**Wait \~10 minutes** for all pods to pull images and reach Running state. [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

***

## Step 4: Validate Pods

```bash
kubectl get pods
```

All four pods should show `Running` with `1/1` READY. [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

**If a pod shows errors:**

```bash
kubectl describe pod <pod-name>
```

Check the **Events** section at the bottom for error messages (wrong image name, pull errors, crash loops). [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

***

## Step 5: Validate Deployments

```bash
kubectl get deploy
```

All four deployments should show desired/current/available replicas matching. [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

***

## Step 6: Validate Services

```bash
kubectl get svc
```

All four ClusterIP services should be listed with their cluster IPs and ports. [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

***

## Step 7: Validate Service-to-Pod Connection (Endpoint Check)

**7a. Get the Pod IP:**

```bash
kubectl describe pod <app-pod-name>
```

Note the **IP** field (e.g., `10.244.x.x`) and the **container port** (e.g., `8080`). [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

**7b. Check the Service endpoints:**

```bash
kubectl describe svc vproapp-service
```

Look for the **Endpoints** field. It should show the Pod IP and port (e.g., `10.244.x.x:8080`). [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

**If Endpoints is empty:** The selector label doesn't match the Pod's label. Fix the label in the Service or Deployment definition file, delete, and recreate. [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

***

## Step 8: Validate PVC and Storage Class

```bash
kubectl get pvc
```

Note the PVC ID. Compare it with the EBS volume tag in the AWS EC2 console — they should match. [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

```bash
kubectl get sc
```

Should show the default storage class with provisioner `ebs.csi.aws.com`. This is the driver that created the EBS volume when the PVC was claimed. [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

***

## Step 9: Validate Ingress

```bash
kubectl get ingress
```

Should show the Ingress name, host, and the ALB address. If the address field is empty, the Ingress Controller is not working or the ALB is not yet active. [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

```bash
kubectl describe ingress <ingress-name>
```

Check: **Address** (ALB endpoint), **Backends** (service name + port + Pod IPs). [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

***

## Step 10: Create DNS CNAME Record

**10a. Copy the ALB endpoint** from `kubectl get ingress` or from the AWS console (Load Balancers). [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

**10b. In your domain registrar (GoDaddy):**

Add Record → Type: **CNAME** → Name: `vprofile` → Value: paste the ALB endpoint. Save. [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

⚠️ No extra characters or trailing periods in the endpoint value. [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

***

## Step 11: Test from Browser

**11a. Test direct ALB endpoint access:**

Navigate to `http://<ALB-endpoint>` in the browser. You should see a default page — **NOT** the vProfile app. This proves the Ingress host-matching rule works: without the correct hostname, the request is rejected. [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

**11b. Test with the correct hostname:**

Navigate to `http://vprofile.hkhinfotek.xyz` (your configured domain). The vProfile login page should load. [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

**11c. Verify database:**

Login with `admin_vp` / `admin_vp`. Successful login = DB service + DB pod + PVC/EBS all working. [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

**11d. Verify RabbitMQ:**

Click the RabbitMQ test link. Should show "RabbitMQ initiated." [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

**11e. Verify Memcache:**

Click "All Users" → click a user → "data is inserted in cache." Click the same user again → "data is coming from the cache." [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

***

## Troubleshooting: Delete-Fix-Recreate

If any resource has an error:

```bash
# 1. Identify the problem
kubectl describe pod <pod-name>    # check Events

# 2. Fix the YAML definition file in your editor

# 3. Delete the broken resource
kubectl delete -f <filename>.yaml

# 4. Recreate
kubectl create -f <filename>.yaml
```

 [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

⚠️ Don't delete a Pod directly if it's managed by a Deployment — the Deployment will recreate it. Delete the **Deployment** file instead: `kubectl delete -f <deployment-file>.yaml`. [\[359-deploy...8s-cluster \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/359-deploy-app-on-k8s-cluster.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Deployment Sequence

```
1. Ingress Controller    kubectl apply -f <controller-URL>
     ↓                   → creates ingress-nginx namespace
     ↓                   → provisions AWS ALB (wait for "active")
2. PVC                   kubectl create -f db-pvc.yaml
     ↓                   → storage class provisions 3GB EBS volume
     ↓                   → verify in EC2 → Volumes
3. All manifests         kubectl create -f .
     ↓                   → deploys, services, secret, ingress (PVC error = OK)
     ↓                   → wait ~10 min for pods to reach Running
4. DNS CNAME             domain registrar → vprofile → ALB endpoint
5. Test                  browser → http://hostname → login → verify all
```

***

## Validation Checklist

```
kubectl get pods          → all 4 Running, 1/1 READY
kubectl get deploy        → all 4 with correct replicas
kubectl get svc           → all 4 ClusterIP services listed
kubectl describe svc X    → Endpoints show Pod IP:port (NOT empty)
kubectl get pvc           → PVC bound, ID matches EBS volume tag
kubectl get sc            → default storage class with ebs.csi.aws.com
kubectl get ingress       → host + ALB address populated
kubectl describe ingress  → backends show service + pod IPs
Browser → hostname        → login page loads
Login admin_vp            → DB verified (through to EBS)
RabbitMQ link             → "initiated"
User → click → click      → "from db" → "from cache" (Memcache verified)
```

***

## PVC → EBS Provisioning Chain

```
PVC (db-pvc.yaml, 3GB, storageClassName: default)
  → Storage Class (default, provisioner: ebs.csi.aws.com)
    → EBS CSI Driver creates 3GB EBS volume in AWS
      → Status: available
        → Pod mounts PVC → EBS attaches to worker node → Status: in-use

Verify: kubectl get pvc → PVC ID == EBS volume tag in EC2 console
```

***

## Service-to-Pod Validation Pattern

```
kubectl describe pod <name>    → note IP (e.g., 10.244.x.x)
kubectl describe svc <name>    → check Endpoints field

Endpoints = Pod IP:port       → ✓ Service connected
Endpoints = <empty>           → ✗ Selector mismatch!

Fix: check labels in Deployment template vs Service selector
```

***

## Ingress Host-Matching Rule

```
Request with hostname vprofile.hkhinfotek.xyz
  → matches Ingress rule host: vprofile.hkhinfotek.xyz
    → routes to backend service → works ✓

Request with raw ALB endpoint URL
  → no Ingress rule matches this hostname
    → request REJECTED → default page shown ✗

DNS CNAME bridges: hostname → ALB endpoint
Ingress rule bridges: hostname → backend service
Both are required for external access to work
```

***

## Delete-Fix-Recreate Workflow

```
1. kubectl describe pod <name>     → read Events for error
2. Fix YAML source file            → correct mistake
3. kubectl delete -f <file>.yaml   → remove broken resource
4. kubectl create -f <file>.yaml   → deploy corrected version

⚠️ Pod managed by Deployment → delete the DEPLOYMENT file, not the Pod
```

***

## `kubectl create -f .` Behavior

```
Reads ALL .yaml files in current directory
Creates each resource
Already-exists → error for that resource, continues with rest
Idempotent alternative: kubectl apply -f . (updates if exists)
```

***

## Full Request Flow (Runtime Verification)

```
User → http://vprofile.hkhinfotek.xyz
  → DNS CNAME → ALB endpoint
    → ALB → Ingress Controller (NGINX pod)
      → Ingress rule: host match → vproapp-service:8080
        → ClusterIP Service → vproapp Pod (Tomcat)
          → login → vprodb-service → vprodb Pod (MySQL)
            → PVC → EBS volume (/var/lib/mysql)
          → users → vprocache-service → Memcache Pod
          → mq test → vpromq-service → RabbitMQ Pod
```

***

## Storage Class Quick Reference

```
kubectl get sc
  NAME      PROVISIONER          
  default   ebs.csi.aws.com      ← creates EBS volumes

PVC references: storageClassName: default
  → could also use the actual name (but "default" is safer)
  → name may change between cluster setups
  → storage admin manages this — you just need the name
```

***

## All Commands Used

```bash
# Ingress Controller
kubectl apply -f <controller-manifest-URL>
kubectl get ns
kubectl get all -n ingress-nginx

# PVC
kubectl create -f db-pvc.yaml
kubectl get pvc
kubectl get sc

# Bulk deploy
kubectl create -f .

# Validation
kubectl get pods
kubectl get deploy
kubectl get svc
kubectl describe pod <name>
kubectl describe svc <name>
kubectl get ingress
kubectl describe ingress <name>

# Troubleshooting
kubectl delete -f <file>.yaml
kubectl create -f <file>.yaml

# Cleanup
kubectl delete -f <controller-manifest-URL>
```

***

## End-to-End Verification (Single Login Test)

```
Login success = proves:
  ✓ Ingress → ALB → Controller → rule matching
  ✓ App Service → App Pod → Tomcat running
  ✓ DB Service → DB Pod → MySQL accessible
  ✓ PVC → EBS → data persisted
  ✓ DNS → CNAME → hostname resolution

RabbitMQ click = proves: MQ Service + MQ Pod
User click ×2 = proves: Memcache Service + Memcache Pod + caching
```

***

## Real-World Progression

```
1. Containerize (Dockerfiles + images)       ← done
2. Write K8s manifests (this lecture)         ← done
3. Helm (package management)                 ← next
4. CI/CD (automated deployment)              ← future
```

***

## Key Engineering Patterns

| Pattern                              | Manifestation                                                                                                      |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------ |
| **Provision-then-deploy**            | ALB + EBS created first, verified active, then manifests deployed — infrastructure before workload                 |
| **Endpoint validation**              | Service Endpoints field = the definitive test for Service→Pod connectivity — always check this                     |
| **Host-based access control**        | Ingress rejects requests without matching hostname — security through routing rules                                |
| **Bulk deploy with error tolerance** | `kubectl create -f .` skips already-existing resources, creates the rest                                           |
| **Delete-fix-recreate**              | Standard K8s troubleshooting: never edit in place for critical changes — delete and recreate from corrected source |
| **Single-action verification**       | One login validates the entire chain: Ingress → Service → Pod → DB → Storage                                       |
| **Storage abstraction**              | PVC → Storage Class → EBS CSI → EBS volume — developer claims storage, infrastructure provides it                  |

***

## Project Continuity

```
BEFORE: Source code overview (349), all manifests written
THIS:   Full deployment + validation + troubleshooting on live cluster
NEXT:   Cleanup lecture (delete all resources + ALB to stop charges)
FUTURE: Helm, CI/CD automation
```

***

This completes the full reconstruction. **Theory** explains the deployment order, storage class provisioning, endpoint validation, and host-matching behavior. **Practical** walks through every command, every verification step, and the complete browser test. The **Compression Map** gives you the deployment sequence, the validation checklist, and the full request flow for instant recall. Let me know if you'd like Anki flashcards or any section expanded! 🚀
