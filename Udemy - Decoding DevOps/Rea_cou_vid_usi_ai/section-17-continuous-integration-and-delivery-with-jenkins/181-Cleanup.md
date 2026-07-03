# 🎓 Post-Project Cleanup — Tearing Down AWS & CI/CD Infrastructure

*Reconstructed from video lecture #181 caption file*

***

## 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

### 1. Why Cleanup Matters

Cleanup is the final and often overlooked step in any DevOps project lifecycle. After you've built your CI/CD pipeline, deployed your application, and verified everything works, the infrastructure you spun up continues to **run and accumulate costs** on AWS — even if you're not actively using it. EC2 instances, ECS services, load balancers, and target groups are all **billable resources**. Leaving them running when they're no longer needed is wasted money. [\[181.-Cleanup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/181.-Cleanup.txt)

In a learning environment, this is especially important. You created these resources to practice and learn, not to run them indefinitely. The video is positioned at the end of a section — the CI/CD pipeline with Docker, ECR, and ECS has been completed, and the upcoming lectures will take a different direction. So this is the natural point to clean up resources that won't be reused. [\[181.-Cleanup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/181.-Cleanup.txt)

The underlying principle is simple: **if you're not using it, shut it down or delete it.** But the *how* of cleanup requires understanding **which resources to delete, which to merely stop, and in what order** — because some resources depend on others, and deleting them in the wrong order can leave orphaned components still incurring charges. [\[181.-Cleanup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/181.-Cleanup.txt)

***

### 2. Stop vs. Terminate vs. Delete — Choosing the Right Action

The video makes deliberate, different decisions for each resource, and the reasoning behind each choice is important to understand: [\[181.-Cleanup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/181.-Cleanup.txt)

**Terminate (Delete permanently):** Used for **Nexus** and **Sonar** EC2 instances. Terminating an instance destroys it completely — the instance, its root volume (unless configured otherwise), and its state are all gone. The instructor chooses termination because these services are **not needed for the upcoming lectures**. And critically, he explains that even if they're deleted, they can be **relaunched easily using user data scripts**. This is a key DevOps concept — if your infrastructure is defined as code (user data scripts, CloudFormation, Terraform, etc.), you don't need to preserve running instances. You can recreate them on demand. The instance is disposable; the script is the real asset. [\[181.-Cleanup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/181.-Cleanup.txt)

**Stop (Preserve but don't run):** Used for **Jenkins**. Stopping an instance halts it — it stops incurring compute charges, but the instance and its attached EBS volumes are preserved. You can start it again later and pick up where you left off. The instructor recommends stopping (not terminating) Jenkins because **a few more lectures will need it**. However, he also notes that even if you accidentally delete Jenkins, you already know the entire setup process — installing plugins, configuring tools, storing credentials — so you could rebuild it. The stop is a convenience choice, not a necessity. [\[181.-Cleanup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/181.-Cleanup.txt)

**Delete (Service-level removal):** Used for **ECS services**, **ECS clusters**, **load balancers**, and **target groups**. These are AWS-managed services, not EC2 instances, so the terminology is "delete" rather than "terminate." Each has its own deletion process and dependencies. [\[181.-Cleanup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/181.-Cleanup.txt)

**Keep (Optional):** The **ECR repository** is called out as something you *can* delete but don't *have* to. The instructor explicitly states there are **no charges** for the ECR repository itself (charges apply to storage of images, which is minimal). He recommends cleaning it up as good practice, but it's not a cost concern. [\[181.-Cleanup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/181.-Cleanup.txt)

> 🔍 **Deep Dive (Optional)**
>
> The distinction between "stop" and "terminate" is fundamental in AWS EC2. A **stopped** instance retains its instance ID, attached EBS volumes, Elastic IP associations (if any), and security group assignments. You only pay for the EBS storage, not for the compute. A **terminated** instance is destroyed — AWS reclaims the compute resources, and the root EBS volume is deleted by default (unless `DeleteOnTermination` is set to `false`). Understanding this difference prevents accidental data loss and unexpected charges. [\[181.-Cleanup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/181.-Cleanup.txt)

***

### 3. Infrastructure as Code — The Safety Net for Deletion

A recurring theme in this video is the instructor's confidence in deleting resources: *"Even if you delete it, you know the whole steps"* and *"You can just use the user data script and launch them."* This reflects a core DevOps philosophy — **infrastructure should be reproducible, not precious**. [\[181.-Cleanup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/181.-Cleanup.txt)

When your setup process is documented (or better, scripted), every resource becomes disposable. You don't need to keep a Nexus server running "just in case" if you can spin up an identical one in minutes using a user data script. This mindset is what separates traditional IT (where servers are carefully maintained and never deleted) from modern DevOps (where servers are cattle, not pets). [\[181.-Cleanup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/181.-Cleanup.txt)

***

### 4. Deletion Order and Dependencies

The video demonstrates a specific order for cleanup, and this order is not arbitrary. AWS resources often have **dependencies** — you cannot delete a resource that is still being referenced by another. [\[181.-Cleanup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/181.-Cleanup.txt)

The order shown is:

1.  **ECS Service** → must be deleted **before** the cluster (a cluster cannot be deleted if it still has active services)
2.  **ECS Cluster** → can only be deleted after all services within it are removed
3.  **Load Balancer** → the one created by ECS must be deleted separately (ECS creates it but does not always clean it up automatically)
4.  **Target Group** → associated with the load balancer; must also be removed
5.  **EC2 Instances** → independent, can be stopped/terminated in any order
6.  **ECR Repository** → independent, can be deleted at any time [\[181.-Cleanup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/181.-Cleanup.txt)

> ⚠️ **Expert Note (Optional)**
>
> A common real-world mistake is deleting the ECS cluster first and assuming everything else is cleaned up. The load balancer and target group created by ECS are **separate AWS resources** — they persist even after the service and cluster are deleted. If you don't explicitly remove them, the load balancer continues to incur hourly charges. Always check the EC2 → Load Balancers and EC2 → Target Groups sections after deleting ECS resources. The video specifically warns about this: *"Make sure you delete this load balancer"* and *"Make sure to remove this as well."* [\[181.-Cleanup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/181.-Cleanup.txt)

***

### 5. Force Delete — When Normal Deletion Isn't Enough

When deleting the ECS service, the video mentions checking **"Force Delete"**. Normal deletion of an ECS service attempts a graceful shutdown — it stops running tasks, deregisters targets from the load balancer, and waits for everything to drain. This can take time and can sometimes get stuck if tasks fail to stop cleanly. [\[181.-Cleanup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/181.-Cleanup.txt)

**Force Delete** bypasses the graceful process and immediately removes the service regardless of the state of its tasks. In a cleanup scenario (where you don't care about graceful shutdown because you're tearing everything down), force delete is the appropriate choice. It's faster and avoids potential hang-ups. [\[181.-Cleanup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/181.-Cleanup.txt)

***

## ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

### What We Are Doing

We are tearing down all the AWS infrastructure that was created during the CI/CD pipeline project — EC2 instances (Nexus, Sonar, Jenkins), ECS services and clusters, ECR repositories, load balancers, and target groups. The goal is to **stop incurring charges** for resources no longer needed and leave the AWS account clean for the next set of lectures. [\[181.-Cleanup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/181.-Cleanup.txt)

The final outcome: only the Jenkins instance remains (in a stopped state) for use in upcoming lectures. Everything else is deleted.

***

### Step 1: Terminate Nexus and Sonar EC2 Instances

Navigate to the **AWS Console → EC2 → Instances**. Locate the **Nexus** and **Sonar** instances. [\[181.-Cleanup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/181.-Cleanup.txt)

Select each instance → **Instance State → Terminate Instance**.

**Why terminate (not stop)?** These two services are not needed for the upcoming lectures. And since you have the **user data scripts** that were used to launch and configure them originally, you can recreate them at any time. There's no value in keeping them in a stopped state and paying for their EBS storage. [\[181.-Cleanup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/181.-Cleanup.txt)

**What happens internally:** AWS shuts down the instance, releases the compute resources, and (by default) deletes the root EBS volume. The instance will briefly show a "shutting down" state, then transition to "terminated," and eventually disappear from the console.

**Connection to overall cleanup:** These were supporting services for the CI pipeline (artifact storage and code quality analysis). With the CI pipeline section complete, they serve no purpose.

***

### Step 2: Stop the Jenkins EC2 Instance

Locate the **Jenkins** instance in the EC2 console. Select it → **Instance State → Stop**. [\[181.-Cleanup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/181.-Cleanup.txt)

**Why stop (not terminate)?** Jenkins will be needed for **a few more lectures** in the course. Stopping it preserves the instance and all its configuration (installed plugins, stored credentials, pipeline jobs, tool configurations) while halting compute charges. When you need Jenkins again, simply start the instance. [\[181.-Cleanup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/181.-Cleanup.txt)

The instructor adds reassurance: even if you accidentally delete Jenkins, you already know the complete setup process — installing Java, installing Jenkins, configuring Maven, JDK, SonarQube scanner, Docker, plugins, credentials — all of it. So there's no catastrophic loss either way. [\[181.-Cleanup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/181.-Cleanup.txt)

**What happens internally:** The instance enters the "stopping" state, then "stopped." The EBS volume remains attached and you continue to pay for its storage (typically a few cents per GB per month), but compute billing stops entirely.

> 🔍 **Deep Dive (Optional)**
>
> Be aware that when you stop and restart an EC2 instance, its **public IP address changes** (unless you have an Elastic IP attached). This means any configurations that reference the Jenkins public IP (like SonarQube webhooks, or bookmarked URLs) will need to be updated after restart. The private IP also may change depending on your VPC configuration. Keep this in mind when resuming work. [\[181.-Cleanup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/181.-Cleanup.txt)

***

### Step 3: Delete the ECS Service

Navigate to **AWS Console → ECS (Elastic Container Service)**. Go to your **service**. Click on the **service name** to open its details. Click **Delete Service**. [\[181.-Cleanup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/181.-Cleanup.txt)

Check the **"Force Delete"** option. Type `delete` in the confirmation field. Click **Delete**. [\[181.-Cleanup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/181.-Cleanup.txt)

**Why force delete?** In a cleanup scenario, there's no need for graceful draining or task shutdown. Force delete removes the service immediately regardless of the current state of its running tasks.

**Why delete the service before the cluster?** The ECS cluster cannot be deleted while it still contains active services. The service is a child resource of the cluster — it must go first. [\[181.-Cleanup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/181.-Cleanup.txt)

**What happens internally:** ECS stops all running tasks associated with the service, deregisters container instances from target groups, and removes the service definition. This may take a moment.

***

### Step 4: Delete the ECS Cluster

Once the service deletion is complete, go to your **ECS Cluster**. Select the cluster (in this case, the **vprofile** cluster). [\[181.-Cleanup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/181.-Cleanup.txt)

Go to **Actions → Delete Cluster**. Type `delete` followed by the cluster name (e.g., `vprofile`) in the confirmation field. Click **Delete**. [\[181.-Cleanup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/181.-Cleanup.txt)

**What happens internally:** ECS removes the cluster definition, deregisters any remaining container instances, and cleans up the cluster's internal networking configuration. This process takes some time — the video notes *"It's gonna take some time."* [\[181.-Cleanup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/181.-Cleanup.txt)

**Connection to cleanup flow:** With the service and cluster deleted, ECS is fully cleaned up. But there are still **associated resources** that ECS created but doesn't automatically clean up — specifically the load balancer and target group.

***

### Step 5: Delete the Load Balancer

Navigate to **AWS Console → EC2 → Load Balancers** (in the left sidebar, under "Load Balancing"). [\[181.-Cleanup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/181.-Cleanup.txt)

Look for the load balancer that **was created by ECS**. Select it and **delete** it. [\[181.-Cleanup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/181.-Cleanup.txt)

**Why is this a separate step?** When ECS creates a service with a load balancer, the load balancer is created as an independent EC2 resource. Deleting the ECS service and cluster does **not** automatically delete the load balancer. If you forget this step, the load balancer continues to run and **incur hourly charges** (Application Load Balancers cost approximately $0.0225/hour plus data processing charges). [\[181.-Cleanup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/181.-Cleanup.txt)

The video specifically warns: *"Make sure you delete this load balancer."* This is one of the most commonly missed cleanup steps. [\[181.-Cleanup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/181.-Cleanup.txt)

***

### Step 6: Delete the Target Group

Navigate to **AWS Console → EC2 → Target Groups** (also under "Load Balancing" in the sidebar). [\[181.-Cleanup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/181.-Cleanup.txt)

Locate the target group that was associated with the load balancer / ECS service. Select it and **delete** (deregister/remove) it. [\[181.-Cleanup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/181.-Cleanup.txt)

**Why?** Similar to the load balancer, the target group is an independent resource. While target groups themselves don't incur direct charges, leaving orphaned target groups clutters your account and can cause confusion in future projects. The video says: *"Make sure to remove this as well."* [\[181.-Cleanup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/181.-Cleanup.txt)

***

### Step 7: (Optional) Delete the ECR Repository

Navigate to **AWS Console → ECR (Elastic Container Registry)**. Locate your ECR repository (the one created for storing the vprofile Docker images). [\[181.-Cleanup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/181.-Cleanup.txt)

You can delete it if you wish. The instructor notes: **"Even if you keep it, there's no problem. There's no charges for this one."** ECR repositories themselves don't incur charges — only the **stored images** consume storage (and the cost is negligible for a few images). However, the instructor recommends deleting it as good practice: *"I just recommend cleaning it up if you're not going to use it."* [\[181.-Cleanup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/181.-Cleanup.txt)

***

### Cleanup Summary — Final State

After completing all steps, here is what your AWS account should look like:

| Resource                    | Action             | Status            | Reason                                        |
| --------------------------- | ------------------ | ----------------- | --------------------------------------------- |
| Nexus EC2 Instance          | Terminated         | ❌ Gone            | Not needed; reproducible via user data script |
| Sonar EC2 Instance          | Terminated         | ❌ Gone            | Not needed; reproducible via user data script |
| Jenkins EC2 Instance        | Stopped            | ⏸️ Preserved      | Needed for upcoming lectures                  |
| ECS Service                 | Deleted (Force)    | ❌ Gone            | Pipeline section complete                     |
| ECS Cluster (vprofile)      | Deleted            | ❌ Gone            | No services remain                            |
| Load Balancer (ECS-created) | Deleted            | ❌ Gone            | Prevents ongoing charges                      |
| Target Group                | Deleted            | ❌ Gone            | Prevents orphaned resources                   |
| ECR Repository              | Deleted (optional) | ❌ / ✅ Your choice | No charges either way                         |

 [\[181.-Cleanup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/181.-Cleanup.txt)

***

### The DevOps Mindset Takeaway

The key lesson embedded in this cleanup lecture isn't just "delete your stuff." It's the confidence that comes from **knowing your infrastructure is reproducible**. The instructor casually says to terminate Nexus and Sonar because you can just relaunch them with user data scripts. He says even if you delete Jenkins, you know the whole setup. This is the DevOps engineer's relationship with infrastructure — **it's disposable because the knowledge and the code to recreate it are the real assets**. Servers come and go. Scripts and pipelines endure. [\[181.-Cleanup \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/181.-Cleanup.txt)

***

Want me to save this as a downloadable Markdown file? 📄
