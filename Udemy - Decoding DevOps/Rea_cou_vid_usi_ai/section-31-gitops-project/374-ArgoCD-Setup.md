# ☸️ ArgoCD Setup — AWS Load Balancer Controller, ArgoCD Installation & Ingress on EKS — Deep Learning Material

**Source:** *Argo CD Setup* (Video Lecture Caption File) + Supporting Hands-On Command Reference File [\[374-argo-cd-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374-argo-cd-setup.txt), [\[374.ArgoCDSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374.ArgoCDSetup.txt)

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

## 1.1 What We Are Setting Up — Two Controllers for Two Purposes

This lecture installs two critical controllers on the EKS cluster, each serving a distinct purpose: [\[374-argo-cd-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374-argo-cd-setup.txt)

**1. AWS Load Balancer Controller** — an Ingress Controller that creates and manages AWS Application Load Balancers (ALBs) from within Kubernetes. When you create an Ingress object with the class `alb`, this controller provisions a real AWS ALB, configures its listeners, target groups, and routing rules. Without it, Ingress objects referencing ALBs would do nothing — there's no component to act on them.

**2. ArgoCD** — a GitOps continuous delivery controller. ArgoCD watches a Git repository containing Helm charts (or Kubernetes manifests), and automatically deploys them to the cluster. It's the automation that replaces manual `kubectl apply` or `helm install` — instead of running commands, you push to Git, and ArgoCD detects the change and deploys it. The instructor describes it as: "the ArgoCD controller, which is going to fetch the Helm charts and deploy it in the EKS cluster." [\[374-argo-cd-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374-argo-cd-setup.txt)

Both controllers follow the same Kubernetes controller pattern (watch desired state → reconcile actual state), but they manage different things: the Load Balancer Controller manages AWS networking infrastructure; ArgoCD manages application deployments.

***

## 1.2 The AWS Load Balancer Controller — Why It Needs Special Permissions

The AWS Load Balancer Controller runs inside the Kubernetes cluster but needs to **create and manage AWS resources** (ALBs, target groups, security groups) that exist outside the cluster in the AWS account. This creates a permissions challenge: how does a pod inside Kubernetes get permission to call AWS APIs? [\[374-argo-cd-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374-argo-cd-setup.txt)

The solution is a three-step IAM chain:

**Step 1: IAM Policy** — defines what AWS actions the controller is allowed to perform (create/modify/delete load balancers, manage target groups, read VPC information, etc.). This policy is downloaded as a JSON file from the official AWS documentation and created in IAM. [\[374.ArgoCDSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374.ArgoCDSetup.txt)

**Step 2: IAM Service Account** — bridges Kubernetes and AWS IAM. An IAM service account is a Kubernetes service account that is linked to an IAM role. When a pod uses this service account, it automatically receives temporary AWS credentials with the permissions from the attached IAM role. The `eksctl create iamserviceaccount` command creates this bridge — it creates both the Kubernetes service account and the IAM role, and links them together. [\[374.ArgoCDSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374.ArgoCDSetup.txt)

**Step 3: Controller uses the service account** — when the Helm chart installs the Load Balancer Controller, it configures the controller pods to use the `aws-load-balancer-controller` service account. The controller pods inherit the IAM permissions, enabling them to call AWS APIs.

🔍 **Deep Dive:**
This IAM-to-Kubernetes bridge is called **IRSA (IAM Roles for Service Accounts)**. It's EKS-specific — in a self-managed Kubernetes cluster (like kops), you'd use node-level IAM roles or other mechanisms. IRSA is more secure because permissions are scoped to specific pods (via their service account), not to entire nodes. A pod that doesn't use the service account gets no AWS permissions.

***

## 1.3 Certificate Manager — Why It's Required Before the Load Balancer Controller

Before installing the Load Balancer Controller, **cert-manager** must be installed. Cert-manager is a Kubernetes add-on that manages TLS certificates — it can issue, renew, and configure certificates for services within the cluster. [\[374-argo-cd-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374-argo-cd-setup.txt)

The AWS Load Balancer Controller depends on cert-manager for its **webhook certificates**. The controller uses admission webhooks (Kubernetes mechanisms that intercept and validate API requests), and these webhooks require TLS certificates to function securely. Cert-manager provides and manages these certificates automatically.

The instructor shows that after installing cert-manager, you must **wait** for it to be fully ready before proceeding: [\[374.ArgoCDSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374.ArgoCDSetup.txt)

```bash
kubectl wait --for=condition=available --timeout=180s \
  deployment/cert-manager \
  deployment/cert-manager-cainjector \
  deployment/cert-manager-webhook \
  -n cert-manager
```

This `kubectl wait` command blocks until all three cert-manager deployments are available. Installing the Load Balancer Controller before cert-manager is ready will fail because the webhooks can't be set up without certificates.

***

## 1.4 The Kubeconfig File — Connecting kubectl to EKS

Before running any `kubectl` commands against the EKS cluster, you need the **kubeconfig file** — the configuration that tells kubectl how to authenticate and connect to the cluster. For EKS, you fetch this using: [\[374-argo-cd-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374-argo-cd-setup.txt)

```bash
aws eks update-kubeconfig --name vprofile-eks-cluster --region us-east-1
```

This command contacts the EKS API, retrieves the cluster's connection details (API server URL, certificate authority), and stores them in `~/.kube/config`. After this, `kubectl get pod` works — it knows where the cluster is and how to authenticate. [\[374-argo-cd-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374-argo-cd-setup.txt)

***

## 1.5 EKS Access Mode — A Prerequisite Configuration

The instructor begins with a prerequisite: go to the EKS cluster → Access → Manage, and ensure the authentication mode is set to **"EKS API and ConfigMap"** (not just ConfigMap). This must be done **before** the lecture begins, with a 5-minute wait afterward. [\[374-argo-cd-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374-argo-cd-setup.txt)

This setting controls how Kubernetes RBAC (Role-Based Access Control) integrates with AWS IAM. The "EKS API and ConfigMap" mode allows both the traditional `aws-auth` ConfigMap and the newer EKS API-based access entries to manage cluster access. The IAM service account for the Load Balancer Controller requires this mode to function correctly.

***

## 1.6 ArgoCD Installation — Helm-Based Deployment

ArgoCD is installed using **Helm** — the Kubernetes package manager. The instructor adds the ArgoCD Helm repository, then installs ArgoCD with a specific version (`9.5.2`) into a dedicated `argocd` namespace: [\[374-argo-cd-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374-argo-cd-setup.txt), [\[374.ArgoCDSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374.ArgoCDSetup.txt)

```bash
helm upgrade argocd argo/argo-cd --version 9.5.2 --install --create-namespace -n argocd
```

This single command creates the entire ArgoCD infrastructure: the ArgoCD server (web UI + API), the repo server (fetches Git repositories), the application controller (reconciles desired vs. actual state), and all supporting services, pods, and configurations. [\[374-argo-cd-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374-argo-cd-setup.txt)

The `helm upgrade --install` pattern is idempotent — if ArgoCD isn't installed, it installs it; if it's already installed, it upgrades it. This is the same pattern used for the Load Balancer Controller and is the standard way to manage Kubernetes applications with Helm.

***

## 1.7 The ArgoCD Ingress — HTTPS Access via ALB

To access ArgoCD from a browser, an **Ingress** must be created that connects the ArgoCD server service to an external ALB. This Ingress uses the AWS Load Balancer Controller (installed earlier) and includes several important annotations: [\[374-argo-cd-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374-argo-cd-setup.txt), [\[374.ArgoCDSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374.ArgoCDSetup.txt)

**`kubernetes.io/ingress.class: alb`** — selects the AWS ALB Ingress Controller (not NGINX).

**`alb.ingress.kubernetes.io/scheme: internet-facing`** — the ALB is publicly accessible from the internet.

**`alb.ingress.kubernetes.io/target-type: ip`** — the ALB routes directly to pod IPs (not node ports). This is more efficient and works with the VPC CNI plugin in EKS.

**`alb.ingress.kubernetes.io/certificate-arn: <ACM-ARN>`** — attaches an AWS Certificate Manager (ACM) SSL certificate to the ALB for HTTPS. You must replace this with your actual certificate ARN.

**`alb.ingress.kubernetes.io/listen-ports: '[{"HTTP":80},{"HTTPS":443}]'`** — the ALB listens on both port 80 and 443.

**`alb.ingress.kubernetes.io/ssl-redirect: '443'`** — HTTP requests on port 80 are automatically redirected to HTTPS on port 443.

**`alb.ingress.kubernetes.io/backend-protocol: HTTPS`** — the ALB communicates with the ArgoCD server using HTTPS (ArgoCD server runs on port 443 internally). [\[374.ArgoCDSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374.ArgoCDSetup.txt)

The Ingress rule specifies: host `argocd.<your-domain>` → service `argocd-server` → port 443.

***

## 1.8 DNS Configuration — CNAME Record for the Domain

After the Ingress creates the ALB, the ALB gets a DNS endpoint (a long AWS-generated hostname). To access ArgoCD via a human-readable URL (`https://argocd.yourdomain.com`), you create a **CNAME record** in your domain registrar (GoDaddy, Route53, etc.): [\[374-argo-cd-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374-argo-cd-setup.txt)

* **Type:** CNAME
* **Name:** `argocd` (this creates `argocd.yourdomain.com`)
* **Value:** the ALB DNS endpoint

The `argocd` name must match exactly what's in the Ingress rule's `host` field. After DNS propagation (a few minutes), accessing `https://argocd.yourdomain.com` routes through DNS → ALB → Ingress Controller → ArgoCD server service → ArgoCD server pod. [\[374-argo-cd-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374-argo-cd-setup.txt)

***

## 1.9 ArgoCD Initial Credentials — Secret-Based Password

ArgoCD stores its initial admin password in a **Kubernetes Secret** named `argocd-initial-admin-secret`. The password is base64-encoded and must be decoded to use: [\[374-argo-cd-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374-argo-cd-setup.txt), [\[374.ArgoCDSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374.ArgoCDSetup.txt)

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

The username is always `admin`. After first login, the instructor recommends resetting the password through the ArgoCD UI (User Info → Update Password). [\[374-argo-cd-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374-argo-cd-setup.txt)

***

## 1.10 Values You Must Customize

The instructor repeatedly emphasizes that several values must be replaced with your own: [\[374-argo-cd-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374-argo-cd-setup.txt)

* **AWS Account ID** — in the IAM service account command
* **Cluster name** — `vprofile-eks-cluster` (verify yours matches)
* **Region** — `us-east-1` (change if different)
* **VPC ID** — from the EKS cluster's networking section or the VPC console
* **ACM Certificate ARN** — from AWS Certificate Manager
* **Domain name** — in the Ingress rule's `host` field

Missing or incorrect values cause failures that are hard to debug — the instructor stresses checking each one before running the commands.

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

## What We Are Building

We are installing the AWS Load Balancer Controller (to provision ALBs from Kubernetes Ingress objects) and ArgoCD (to automate GitOps deployments) on an EKS cluster, then exposing ArgoCD through an HTTPS-secured ALB accessible via a custom domain. After this, ArgoCD is ready to fetch Helm charts from the Git repository and deploy the vprofile application. [\[374-argo-cd-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374-argo-cd-setup.txt)

***

## Prerequisite: EKS Access Mode

Go to **EKS → Clusters → your cluster → Access → Manage**. Ensure authentication mode is **"EKS API and ConfigMap"**. Save and wait 5 minutes. [\[374-argo-cd-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374-argo-cd-setup.txt)

***

## Step 1: Download the IAM Policy for the Load Balancer Controller

```bash
cd
curl -O https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/main/docs/install/iam_policy.json
```

* `cd` — navigate to home directory
* `curl -O` — downloads the file and saves it with its original name (`iam_policy.json`)

This JSON file defines all AWS permissions the Load Balancer Controller needs (manage ALBs, target groups, security groups, etc.). [\[374.ArgoCDSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374.ArgoCDSetup.txt)

***

## Step 2: Create the IAM Policy

```bash
aws iam create-policy \
  --policy-name AWSLoadBalancerControllerIAMPolicy \
  --policy-document file://iam_policy.json
```

* `aws iam create-policy` — creates a new IAM policy in your AWS account
* `--policy-name` — the policy name (use this exact name — referenced later)
* `--policy-document file://iam_policy.json` — the policy document from the downloaded file

**If the policy already exists:** The command fails with "EntityAlreadyExists." This is safe to ignore — the policy from a previous attempt is still valid. [\[374-argo-cd-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374-argo-cd-setup.txt)

***

## Step 3: Create the IAM Service Account

```bash
eksctl create iamserviceaccount \
  --cluster vprofile-eks-cluster \
  --namespace kube-system \
  --name aws-load-balancer-controller \
  --attach-policy-arn arn:aws:iam::<YOUR-ACCOUNT-ID>:policy/AWSLoadBalancerControllerIAMPolicy \
  --approve \
  --region us-east-1
```

**⚠️ Replace `<YOUR-ACCOUNT-ID>` with your 12-digit AWS account ID.** <cite>turn24search31</cite>

* `eksctl create iamserviceaccount` — creates a Kubernetes service account linked to an IAM role (IRSA)
* `--cluster` — the EKS cluster name
* `--namespace kube-system` — where the service account lives
* `--name aws-load-balancer-controller` — the service account name (must match what the Helm chart expects)
* `--attach-policy-arn` — attaches the policy created in Step 2
* `--approve` — auto-approve the CloudFormation stack creation

**This takes some time** (creates a CloudFormation stack behind the scenes). [\[374-argo-cd-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374-argo-cd-setup.txt)

***

## Step 4: Fetch the Kubeconfig File

```bash
aws eks update-kubeconfig --name vprofile-eks-cluster --region us-east-1
```

This fetches the cluster connection details and stores them in `~/.kube/config`. [\[374-argo-cd-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374-argo-cd-setup.txt)

**Verify:**

```bash
kubectl get pod
```

Should return results (even if empty) without connection errors. If it fails, check that the cluster name and region are correct. [\[374-argo-cd-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374-argo-cd-setup.txt)

***

## Step 5: Install Cert-Manager

```bash
kubectl apply --validate=false \
  -f https://github.com/cert-manager/cert-manager/releases/download/v1.16.1/cert-manager.yaml
```

* `kubectl apply -f <URL>` — downloads and applies the definition file directly from the URL
* `--validate=false` — skips client-side validation (some cert-manager CRDs may not validate against the current kubectl version)

This creates many resources: pods, services, deployments, CRDs, roles, and more in the `cert-manager` namespace. [\[374-argo-cd-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374-argo-cd-setup.txt)

**Wait for cert-manager to be fully ready:**

```bash
kubectl wait --for=condition=available --timeout=180s \
  deployment/cert-manager \
  deployment/cert-manager-cainjector \
  deployment/cert-manager-webhook \
  -n cert-manager
```

This blocks until all three deployments are available (up to 180 seconds). [\[374.ArgoCDSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374.ArgoCDSetup.txt)

**Verify:**

```bash
kubectl get all -n cert-manager
```

Should show pods in `Running` status, services, deployments, and replicasets. [\[374-argo-cd-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374-argo-cd-setup.txt)

***

## Step 6: Install the AWS Load Balancer Controller via Helm

**Add the Helm chart repository:**

```bash
helm repo add eks https://aws.github.io/eks-charts
helm repo update
```

**Get your VPC ID:** Go to **EKS → Clusters → your cluster → Networking** and copy the VPC ID. Alternatively, go to **VPC console** and find the VPC created by Terraform. [\[374-argo-cd-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374-argo-cd-setup.txt)

**Install the controller:**

```bash
helm upgrade --install aws-load-balancer-controller eks/aws-load-balancer-controller \
  -n kube-system \
  --set clusterName=vprofile-eks-cluster \
  --set region=us-east-1 \
  --set vpcId=<YOUR-VPC-ID> \
  --set serviceAccount.create=false \
  --set serviceAccount.name=aws-load-balancer-controller
```

* `helm upgrade --install` — install if not present, upgrade if present (idempotent)
* `-n kube-system` — install in the kube-system namespace
* `--set clusterName` — must match your EKS cluster name
* `--set region` — your AWS region
* `--set vpcId` — **replace with your VPC ID** from the previous step
* `--set serviceAccount.create=false` — don't create a new service account (we already created one in Step 3)
* `--set serviceAccount.name=aws-load-balancer-controller` — use the service account we created

**This takes some time.** [\[374-argo-cd-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374-argo-cd-setup.txt)

**Verify:**

```bash
kubectl get pods -n kube-system | grep aws-load-balancer
```

Should show **two pods** in `Running` status. [\[374-argo-cd-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374-argo-cd-setup.txt)

```bash
kubectl get endpoints aws-load-balancer-webhook-service -n kube-system
```

Should show endpoint IP addresses (confirms the webhook service is functional). [\[374.ArgoCDSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374.ArgoCDSetup.txt)

***

## Step 7: Install ArgoCD via Helm

**Add the Helm chart repository:**

```bash
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update
```

**Install ArgoCD:**

```bash
helm upgrade argocd argo/argo-cd --version 9.5.2 --install --create-namespace -n argocd
```

* `--version 9.5.2` — pin to this specific chart version
* `--create-namespace` — creates the `argocd` namespace if it doesn't exist

**Wait for completion,** then verify: [\[374-argo-cd-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374-argo-cd-setup.txt)

```bash
kubectl get all -n argocd
```

Should show pods (controller, repo-server, argocd-server, etc.), services, deployments, and replicasets. The `argocd-server` pod and its corresponding service are what we'll expose through the Ingress. [\[374-argo-cd-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374-argo-cd-setup.txt)

***

## Step 8: Get Your ACM Certificate ARN

```bash
aws acm list-certificates --region us-east-1 \
  --query "CertificateSummaryList[*].{Domain:DomainName, ARN:CertificateArn}" \
  --output table
```

Copy the **ARN** for your domain's certificate. [\[374.ArgoCDSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374.ArgoCDSetup.txt)

***

## Step 9: Create the ArgoCD Ingress

Create the file `argocd-ingress.yaml` (in VS Code or vim): [\[374-argo-cd-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374-argo-cd-setup.txt), [\[374.ArgoCDSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374.ArgoCDSetup.txt)

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: argocd-ingress
  namespace: argocd
  annotations:
    kubernetes.io/ingress.class: alb
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
    alb.ingress.kubernetes.io/certificate-arn: <YOUR-ACM-CERTIFICATE-ARN>
    alb.ingress.kubernetes.io/listen-ports: '[{"HTTP":80},{"HTTPS":443}]'
    alb.ingress.kubernetes.io/ssl-redirect: '443'
    alb.ingress.kubernetes.io/backend-protocol: HTTPS
spec:
  rules:
    - host: argocd.<YOUR-DOMAIN>
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: argocd-server
                port:
                  number: 443
```

**Replace:** [\[374-argo-cd-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374-argo-cd-setup.txt)

* `<YOUR-ACM-CERTIFICATE-ARN>` — the ARN from Step 8
* `<YOUR-DOMAIN>` — your actual domain (e.g., `hkhinfotek.xyz`)

**Apply:**

```bash
kubectl apply -f argocd-ingress.yaml
```

**Watch the ALB being created:**

```bash
kubectl get ingress argocd-ingress -n argocd -w
```

Wait until the `ADDRESS` column shows an ALB DNS endpoint. Copy this endpoint. [\[374.ArgoCDSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374.ArgoCDSetup.txt)

***

## Step 10: Configure DNS (CNAME Record)

Go to your **domain registrar** (GoDaddy, Route53, etc.) → DNS settings: [\[374-argo-cd-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374-argo-cd-setup.txt)

| Setting | Value                              |
| ------- | ---------------------------------- |
| Type    | CNAME                              |
| Name    | `argocd`                           |
| Value   | `<ALB-DNS-endpoint>` (from Step 9) |

Save and wait a few minutes for DNS propagation. The `argocd` name must **exactly match** the hostname prefix in the Ingress rule. [\[374-argo-cd-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374-argo-cd-setup.txt)

***

## Step 11: Access ArgoCD and Login

Open browser → `https://argocd.<your-domain>`

**Expected:** The ArgoCD login page appears (HTTPS secured with your ACM certificate). [\[374-argo-cd-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374-argo-cd-setup.txt)

**Get the admin password:**

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

* `kubectl get secret` — retrieves the secret object
* `-o jsonpath="{.data.password}"` — extracts only the password field
* `| base64 -d` — decodes from base64 (Kubernetes stores secret values base64-encoded)

**Login:**

* **Username:** `admin`
* **Password:** the decoded output from the command above

**Reset the password:** After login, go to **User Info → Update Password** → enter current password → set new password → save. [\[374-argo-cd-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374-argo-cd-setup.txt)

**Connection to the flow:** ArgoCD is now running and accessible. In the next lecture, it will be configured to watch the `vprofile-helm` Git repository and automatically deploy the Helm charts to the EKS cluster.

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

## Full Installation Sequence

```
0. PREREQ: EKS access mode → "EKS API and ConfigMap" (wait 5 min)
1. Download IAM policy JSON (curl)
2. Create IAM policy (aws iam create-policy)
3. Create IAM service account (eksctl — links K8s SA ↔ IAM role)
4. Fetch kubeconfig (aws eks update-kubeconfig)
5. Install cert-manager (kubectl apply — wait for ready)
6. Install AWS LB Controller (helm — needs VPC ID)
7. Install ArgoCD (helm — creates argocd namespace)
8. Get ACM certificate ARN
9. Create ArgoCD Ingress (kubectl apply — creates ALB)
10. DNS CNAME record: argocd → ALB endpoint
11. Access ArgoCD: https://argocd.domain → admin / decoded-secret
```

## Two Controllers — Two Purposes

```
AWS Load Balancer Controller:
  → manages AWS ALBs from K8s Ingress objects
  → needs IAM permissions (IRSA)
  → needs cert-manager (webhook certs)
  → creates real AWS ALBs

ArgoCD:
  → GitOps CD controller
  → watches Git repo → deploys to cluster
  → replaces manual kubectl/helm commands
  → next lecture: connects to vprofile-helm repo
```

## IAM Permission Chain (IRSA)

```
IAM Policy (JSON) → defines AWS permissions
  ↓
IAM Role (created by eksctl) → assumes the policy
  ↓
K8s Service Account (aws-load-balancer-controller) → linked to role
  ↓
LB Controller Pods (use the service account) → get AWS credentials
  ↓
Pods can create/manage ALBs, target groups, SGs in AWS

Without IRSA: pods have NO AWS permissions → LB creation fails
```

## Dependency Chain

```
IAM policy
  → IAM service account (depends on policy)
    → kubeconfig (independent, but needed for kubectl)
      → cert-manager (independent, but must be ready BEFORE LB controller)
        → AWS LB Controller (depends on cert-manager + service account)
          → ArgoCD (independent of LB controller)
            → ArgoCD Ingress (depends on BOTH LB controller + ArgoCD)
              → DNS CNAME (depends on Ingress ALB endpoint)
                → Browser access (depends on DNS propagation)
```

## ArgoCD Ingress Annotations

```
kubernetes.io/ingress.class: alb              ← select ALB controller
alb.ingress.kubernetes.io/scheme: internet-facing  ← public ALB
alb.ingress.kubernetes.io/target-type: ip     ← route to pod IPs
alb.ingress.kubernetes.io/certificate-arn: ... ← ACM SSL cert
alb.ingress.kubernetes.io/listen-ports: [80,443]  ← both ports
alb.ingress.kubernetes.io/ssl-redirect: '443' ← force HTTPS
alb.ingress.kubernetes.io/backend-protocol: HTTPS ← backend is HTTPS
```

## Traffic Flow (After Setup)

```
Browser: https://argocd.domain.com
  → DNS CNAME → ALB endpoint
    → ALB (created by LB Controller, ACM cert for HTTPS)
      → Ingress rule: host=argocd.domain → service argocd-server:443
        → ArgoCD server pod
```

## Values You MUST Customize

```
<YOUR-ACCOUNT-ID>        → 12-digit AWS account ID (IAM service account)
<CLUSTER-NAME>           → vprofile-eks-cluster (verify yours)
<REGION>                 → us-east-1 (or your region)
<VPC-ID>                 → from EKS networking or VPC console
<ACM-CERTIFICATE-ARN>    → from aws acm list-certificates
<YOUR-DOMAIN>            → in Ingress host field
```

## ArgoCD Credentials

```
Username: admin (always)
Password: kubectl -n argocd get secret argocd-initial-admin-secret \
            -o jsonpath="{.data.password}" | base64 -d

Reset: UI → User Info → Update Password
```

## Helm Pattern (Repeated)

```
helm repo add <name> <url>        ← add chart repository
helm repo update                  ← refresh local cache
helm upgrade <release> <chart> \
  --version X.Y.Z \              ← pin version
  --install \                     ← install if not present
  --create-namespace \            ← create NS if needed
  -n <namespace> \                ← target namespace
  --set key=value                 ← override chart values

Used for: LB Controller, ArgoCD (same pattern, different charts)
```

## Verification Commands

```
cert-manager:   kubectl get all -n cert-manager     → pods Running
LB Controller:  kubectl get pods -n kube-system | grep aws-load-balancer
                                                     → 2 pods Running
ArgoCD:         kubectl get all -n argocd            → server pod Running
Ingress:        kubectl get ingress -n argocd        → ADDRESS shows ALB
Endpoints:      kubectl get endpoints ... -n kube-system → IPs present
```

## Reusable Engineering Patterns

**1. IRSA — Pod-Level AWS Permissions**

```
Problem: pod needs AWS API access
Solution: IAM Policy → IAM Role → K8s Service Account → Pod

More secure than node-level IAM roles:
  Node role: ALL pods on node get permissions
  IRSA: ONLY pods with the specific SA get permissions

Same concept: GCP Workload Identity, Azure Pod Identity
```

**2. Dependency-Ordered Installation**

```
cert-manager BEFORE LB Controller (webhook certs needed)
LB Controller BEFORE Ingress (no controller → Ingress does nothing)
Ingress BEFORE DNS (need ALB endpoint for CNAME)

Pattern: install infrastructure components in dependency order
  Each component is a prerequisite for the next
  kubectl wait → block until dependency is ready
```

**3. Annotations as Controller Configuration**

```
Ingress annotations control ALB behavior:
  scheme, target-type, certificate, ports, SSL redirect

Annotations = controller-specific configuration
  Different controllers read different annotations
  kubernetes.io/ingress.class selects WHICH controller

Same pattern: any K8s resource with controller-specific annotations
  (cert-manager annotations on Ingress for auto-TLS)
  (external-dns annotations for auto DNS records)
```

***

*This completes the full reconstruction. Theory explains the two-controller architecture, the IRSA permission model, and the cert-manager dependency. Practical walks through every command from IAM policy download to ArgoCD login with all customization points highlighted. The Compression Map enables instant recall of the full installation sequence, the dependency chain, the annotation meanings, and the IRSA permission pattern that connects Kubernetes service accounts to AWS IAM roles.* [\[374-argo-cd-setup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374-argo-cd-setup.txt), [\[374.ArgoCDSetup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/374.ArgoCDSetup.txt)
