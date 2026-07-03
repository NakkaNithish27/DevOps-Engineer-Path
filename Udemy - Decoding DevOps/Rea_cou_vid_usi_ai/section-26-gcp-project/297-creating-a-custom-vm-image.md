# 🖼️ GCP — Creating a Custom VM Image (Golden Image) — Deep Learning Material

**Source:** *Creating a Custom VM Image* (Video Lecture Caption File) [\[297-creati...m-vm-image \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/297-creating-a-custom-vm-image.txt)

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

## 1.1 The Golden Image Pipeline — What We Are Building and Why

The goal of this lecture is to create a **custom VM image** (called a "golden image") that contains a fully configured application server — Tomcat with the vprofile application pre-deployed. This image will later be used to create an **instance template** and a **managed instance group** (GCP's equivalent of AWS Auto Scaling Group), enabling automatic scaling of identical, pre-configured application servers. [\[297-creati...m-vm-image \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/297-creating-a-custom-vm-image.txt)

The golden image pipeline has a very specific flow, and understanding this flow is more important than any individual command:

**Launch instance with startup script → Wait for setup → Verify → Stop instance → Snapshot disk → Create image from snapshot → Delete instance → (Next lecture: Instance template → Managed instance group)**

Each step serves a precise purpose. The instance is temporary — it exists only long enough to execute the setup script and be captured as an image. Once the image exists, the instance is disposable. This is **infrastructure as a factory**: you use a temporary machine to produce a reusable artifact (the image), then discard the machine. [\[297-creati...m-vm-image \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/297-creating-a-custom-vm-image.txt)

***

## 1.2 The Startup Script — What It Does

The startup script (`app-golden.sh`) automates the entire application server setup. The instructor notes this is the same script used in the vprofile automated VM project, adapted from CentOS/RPM to **Ubuntu/Debian** (using `apt` instead of `yum`). The script performs these operations in sequence: [\[297-creati...m-vm-image \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/297-creating-a-custom-vm-image.txt)

1. **Creates a user and adds to sudoers** — enables SSH login to the instance
2. **Runs `apt update`** — refreshes package lists
3. **Installs JDK** — Java Development Kit, required to run Tomcat
4. **Downloads Tomcat binary** — from a URL, as a tarball
5. **Extracts the tarball** — unpacks Tomcat files
6. **Creates a Tomcat user** — dedicated system user for running the Tomcat process
7. **Copies Tomcat data to its home directory** — places files in the standard location
8. **Sets ownership to the Tomcat user** — correct file permissions
9. **Creates the systemctl service file** — so Tomcat can be managed via `systemctl start/stop/enable/restart tomcat`
10. **Downloads Maven 3.9.9** — the build tool for the Java project
11. **Extracts and installs Maven** — places it at a system location
12. **Clones the vprofile source code** — from the Git repository
13. **Builds the artifact using Maven** — produces the `.war` file
14. **Removes the default Tomcat application** — clears the default welcome page
15. **Copies the vprofile `.war` to Tomcat's webapps** — deploys the application
16. **Restarts Tomcat** — loads the newly deployed application

This entire sequence runs automatically when the instance boots — it's passed as the startup script during instance creation. The instance needs **approximately 10 minutes** to complete all these steps (downloading packages, cloning code, building with Maven). [\[297-creati...m-vm-image \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/297-creating-a-custom-vm-image.txt)

***

## 1.3 Why the Private Subnet — Two Tests in One

The instructor deliberately launches the instance in the **private subnet** even though the instance is temporary and will be deleted after imaging. The reason is to **test two things simultaneously**: [\[297-creati...m-vm-image \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/297-creating-a-custom-vm-image.txt)

**Test 1: Cloud NAT outbound connectivity.** The startup script downloads packages from the internet (JDK, Tomcat, Maven, Git clone). If the instance is in the private subnet, these downloads must go through the **Cloud NAT** (GCP's equivalent of AWS NAT Gateway). If the script completes successfully, it proves Cloud NAT is working correctly — the private subnet has outbound internet access. [\[297-creati...m-vm-image \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/297-creating-a-custom-vm-image.txt)

**Test 2: Bastion host SSH access.** After the script runs, we need to SSH into the instance to verify Tomcat is running. Since the instance is in the private subnet with no public IP, we must SSH through the bastion host. If this works, it proves the bastion host configuration, the firewall rules, and the public-to-private subnet connectivity are all correct. [\[297-creati...m-vm-image \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/297-creating-a-custom-vm-image.txt)

The instructor could have placed the instance in the public subnet (simpler to access), but chose the private subnet to validate the network infrastructure while also accomplishing the imaging task.

***

## 1.4 Firewall Rules and Tags — How GCP Applies Network Security

GCP uses **network tags** to associate firewall rules with instances. When you create an instance with a specific tag (e.g., `app`), GCP automatically applies all firewall rules that target that tag. [\[297-creati...m-vm-image \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/297-creating-a-custom-vm-image.txt)

The instance is created with tag `app`. Two existing firewall rules match this tag:

**1. `allow-ssh-bastion`** — Tag: `app`. Allows port 22 from the bastion host security group. This enables SSH from the bastion host to any instance tagged `app`.

**2. `allow-load-balancer-to-app`** — Tag: `app`. Allows port 8080 from the GCP load balancer IP range. This will be used later when the managed instance group is behind a load balancer.

This tag-based model is GCP's equivalent of AWS security groups. The difference: in AWS, you assign a security group directly to an instance. In GCP, you assign a **tag** to the instance, and firewall rules **target** that tag. The effect is the same — controlled network access — but the association mechanism is different (tag matching vs. direct assignment). [\[297-creati...m-vm-image \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/297-creating-a-custom-vm-image.txt)

***

## 1.5 The Snapshot → Image Pipeline — Two Distinct Artifacts

GCP separates the imaging process into two steps, and understanding the distinction matters: [\[297-creati...m-vm-image \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/297-creating-a-custom-vm-image.txt)

**Snapshot:** A point-in-time copy of a **disk**. It captures the exact state of the disk — every file, every configuration, every installed package. To take a clean snapshot, the instance should be **stopped** first (to ensure no writes are in progress, preventing data corruption). The instructor stops the instance before taking the snapshot.

**Image:** Created **from a snapshot**. An image is a launchable artifact — it can be used to create new instances. A snapshot is a backup/recovery artifact; an image is a deployment artifact. The relationship is: `disk → snapshot → image → new instances`.

In AWS terms: a snapshot is like an EBS snapshot, and an image is like an AMI. AWS combines these more seamlessly (you can create an AMI directly from an instance), but GCP makes the intermediate snapshot step explicit. [\[297-creati...m-vm-image \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/297-creating-a-custom-vm-image.txt)

The image is stored in a specific **region** (the instructor uses `us-central1`). When you later create instances from this image, the instances should ideally be in the same region for performance (though cross-region usage is possible).

***

## 1.6 Machine Type Selection — Why E2-Micro Won't Work

The instructor selects `e2-small` instead of `e2-micro` for this instance. The reason: the startup script runs Maven (which is memory-intensive — as seen in the Maven hands-on lecture where we had to set `MAVEN_OPTS` for heap space) and Tomcat simultaneously. An `e2-micro` instance doesn't have enough resources — "it's just going to freeze." [\[297-creati...m-vm-image \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/297-creating-a-custom-vm-image.txt)

This is the same resource-awareness demonstrated in the Maven lecture: build processes need sufficient memory. Since this instance is temporary (will be deleted after imaging), the slightly higher cost of `e2-small` is justified by the need for the script to complete successfully.

***

## 1.7 The SSH Key Transfer — A Different Approach Than AWS

Unlike the AWS VPC lecture where the login key was copied to the bastion host using `scp`, GCP uses a different approach here. The instructor copies the **private key content** by displaying it with `cat`, scrolling up to copy the text, then pasting it into a file on the bastion host manually. [\[297-creati...m-vm-image \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/297-creating-a-custom-vm-image.txt)

The instructor creates a file called `gcp-key.pem` on the bastion host, pastes the private key content into it, and sets permissions to `400` (read-only by owner — the same SSH key permission requirement as in AWS). [\[297-creati...m-vm-image \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/297-creating-a-custom-vm-image.txt)

The instructor warns: "Do not copy anything extra character, just from the start till the end." An extra space, newline, or character in the key file will cause SSH authentication to fail — the key must be an exact byte-for-byte copy.

***

## 1.8 The Full Lifecycle — Temporary Instance as a Factory

The complete lifecycle of this temporary instance is: [\[297-creati...m-vm-image \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/297-creating-a-custom-vm-image.txt)

```
Create → Boot → Script runs (10 min) → Verify → Stop → Snapshot → Image → Delete
```

After deletion, the instance is gone. But the **image persists** — it contains the fully configured Tomcat + vprofile application. This image is the input for the next lecture's instance template and managed instance group. Every instance launched from this image will be an exact replica of the golden instance at the moment the snapshot was taken.

This is the **golden image pattern**: build once, capture once, deploy many times. It's the same pattern as AWS AMIs created for Auto Scaling Groups, Docker images built for container orchestration, or Vagrant boxes created for development environments.

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

## What We Are Building

We are launching a temporary EC2 instance in GCP's private subnet, executing a startup script that installs Tomcat and deploys the vprofile application, verifying the setup, then capturing the instance as a custom image (golden image) for future auto-scaling use. After imaging, the temporary instance is deleted. [\[297-creati...m-vm-image \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/297-creating-a-custom-vm-image.txt)

***

## Step 1: Create the Startup Script

In the Google Cloud Shell, create the startup script file:

```bash
cat > app-golden.sh <<EOF
#!/bin/bash
# ... (full script content from lecture resources)
# Creates user, installs JDK, Tomcat, Maven
# Clones source code, builds artifact, deploys to Tomcat
# Last line: systemctl restart tomcat
EOF
```

The `cat > filename <<EOF ... EOF` syntax creates a file by reading input until the `EOF` marker. Copy everything from `cat` until the final `EOF` (uppercase). [\[297-creati...m-vm-image \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/297-creating-a-custom-vm-image.txt)

**Verify the script:**

```bash
cat app-golden.sh
```

* **First line** should be: `#!/bin/bash`
* **Last line** should be: `systemctl restart tomcat`
* If anything is wrong (extra characters, missing content), **delete the file and recreate it**. [\[297-creati...m-vm-image \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/297-creating-a-custom-vm-image.txt)

***

## Step 2: Launch the Instance in the Private Subnet

```bash
gcloud compute instances create vprofile-golden \
  --zone=us-central1-a \
  --machine-type=e2-small \
  --subnet=<private-subnet-name> \
  --no-address \
  --tags=app \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --metadata-from-file=startup-script=app-golden.sh
```

**Breakdown:** [\[297-creati...m-vm-image \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/297-creating-a-custom-vm-image.txt)

* `gcloud compute instances create vprofile-golden` — creates an instance named `vprofile-golden`
* `--zone=us-central1-a` — places the instance in this specific zone
* `--machine-type=e2-small` — uses e2-small (NOT e2-micro — Maven + Tomcat need more resources)
* `--subnet=<private-subnet-name>` — launches in the private subnet (tests Cloud NAT + bastion SSH)
* `--no-address` — no public IP (private subnet instance)
* `--tags=app` — applies the `app` tag, which activates two firewall rules: `allow-ssh-bastion` (SSH from bastion) and `allow-load-balancer-to-app` (port 8080 from LB)
* `--image-family` / `--image-project` — Ubuntu base image (same as bastion host)
* `--metadata-from-file=startup-script=app-golden.sh` — passes the startup script to execute on boot

**After launching: wait approximately 10 minutes.** The script needs time to download packages, clone the repo, build with Maven, and deploy. [\[297-creati...m-vm-image \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/297-creating-a-custom-vm-image.txt)

***

## Step 3: Copy the SSH Key to the Bastion Host

On your **local machine** (or Cloud Shell), navigate to where your SSH keys are stored.

**Display the private key:**

```bash
cat <private-key-filename>
```

Copy the **entire content** — from `-----BEGIN` to the last line `-----END...-----`. No extra characters. [\[297-creati...m-vm-image \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/297-creating-a-custom-vm-image.txt)

**SSH into the bastion host:**

```bash
ssh -i <private-key-path> devops@<bastion-public-ip>
```

* `devops` — the user created on the bastion host
* Use the bastion's **external (public) IP**, not the private IP [\[297-creati...m-vm-image \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/297-creating-a-custom-vm-image.txt)

**Switch to root:**

```bash
sudo -i
```

**Create the key file on the bastion host:**

```bash
vi gcp-key.pem
```

Paste the private key content (`Shift+Insert` to paste in the terminal). Save and quit (`:wq`). [\[297-creati...m-vm-image \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/297-creating-a-custom-vm-image.txt)

**Set correct permissions:**

```bash
chmod 400 gcp-key.pem
```

**Why 400:** SSH refuses to use a private key with permissions that allow other users to read it. `400` = read-only by owner only. Without this: `"WARNING: UNPROTECTED PRIVATE KEY FILE"` error. [\[297-creati...m-vm-image \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/297-creating-a-custom-vm-image.txt)

***

## Step 4: SSH from Bastion Host to the Golden Instance

```bash
ssh -i gcp-key.pem devops@<vprofile-golden-private-ip>
```

* `devops` — the user created by the startup script
* `<vprofile-golden-private-ip>` — get this from the GCP console (Compute Engine → VM instances → vprofile-golden → Internal IP)

**Expected result:** Successful login. This proves: [\[297-creati...m-vm-image \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/297-creating-a-custom-vm-image.txt)

1. The firewall rule `allow-ssh-bastion` is working (port 22 from bastion to instances tagged `app`)
2. The VPC routing from public to private subnet works
3. The `devops` user was created by the startup script

***

## Step 5: Verify Tomcat and the vprofile Application

**Check Tomcat service:**

```bash
systemctl status tomcat
```

**Expected:** `active (running)`. This confirms the entire startup script completed successfully — all downloads worked (Cloud NAT is functional), all installations succeeded, and Tomcat started. [\[297-creati...m-vm-image \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/297-creating-a-custom-vm-image.txt)

Press `q` to quit the status display.

**Check the vprofile application:**

```bash
curl http://localhost:8080
```

**Expected:** HTML output containing `registration` and `login` — the vprofile application's web page. This confirms the `.war` file was deployed correctly to Tomcat's webapps directory. [\[297-creati...m-vm-image \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/297-creating-a-custom-vm-image.txt)

**Connection to the flow:** The instance is verified and ready for imaging. Exit back to the bastion host, then back to Cloud Shell.

***

## Step 6: Stop the Instance

The instance must be stopped before taking a snapshot (ensures disk consistency — no writes in progress).

```bash
gcloud compute instances stop vprofile-golden --zone=us-central1-a
```

* `gcloud compute instances stop` — powers off the instance (doesn't delete it)
* `vprofile-golden` — instance name
* `--zone=us-central1-a` — required zone parameter

**Wait for the command to complete** (the instance transitions to `TERMINATED` state, meaning stopped in GCP terminology). [\[297-creati...m-vm-image \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/297-creating-a-custom-vm-image.txt)

**Note:** If your Cloud Shell session timed out, you'll need to re-authenticate:

```bash
gcloud auth login
gcloud config set project <project-id>
```

Then re-run the stop command. [\[297-creati...m-vm-image \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/297-creating-a-custom-vm-image.txt)

***

## Step 7: Take a Snapshot of the Instance's Disk

```bash
gcloud compute disks snapshot vprofile-golden \
  --snapshot-names=vprofile-snapshot \
  --zone=us-central1-a
```

* `gcloud compute disks snapshot` — takes a snapshot of a disk (the disk is identified by the instance name, since each instance has a boot disk with the same name)
* `vprofile-golden` — the disk name (same as the instance name)
* `--snapshot-names=vprofile-snapshot` — the name to give the snapshot
* `--zone=us-central1-a` — the zone where the disk exists

**Wait for completion.** [\[297-creati...m-vm-image \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/297-creating-a-custom-vm-image.txt)

**Verify in the console:** Go to **Compute Engine → Snapshots**. You should see the snapshot (\~2.17 GB).

***

## Step 8: Create the Custom Image from the Snapshot

```bash
gcloud compute images create vprofile-image \
  --source-snapshot=vprofile-snapshot \
  --storage-location=us-central1
```

* `gcloud compute images create` — creates a custom image
* `vprofile-image` — the name of the image
* `--source-snapshot=vprofile-snapshot` — which snapshot to create the image from
* `--storage-location=us-central1` — the region to store the image (same region as the infrastructure) [\[297-creati...m-vm-image \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/297-creating-a-custom-vm-image.txt)

**Wait for completion** (takes some time).

**Verify in the console:** Go to **Compute Engine → Images**. You should see `vprofile-image` with status ready.

**This is the golden image.** Every instance created from this image will have Tomcat + vprofile pre-installed and configured. [\[297-creati...m-vm-image \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/297-creating-a-custom-vm-image.txt)

***

## Step 9: Delete the Temporary Instance

The instance served its purpose — the image is captured. Delete it.

```bash
gcloud compute instances delete vprofile-golden --zone=us-central1-a
```

When prompted "Do you want to continue?", type `Y` and press Enter. [\[297-creati...m-vm-image \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/297-creating-a-custom-vm-image.txt)

**Connection to the larger flow:** The image is the deliverable of this lecture. The next lecture will create an **instance template** (referencing this image) and a **managed instance group** (auto-scaling group) that automatically launches instances from this image.

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

## Golden Image Pipeline

```
CREATE instance (private subnet, startup script)
  → WAIT ~10 min (script installs Tomcat + deploys vprofile)
    → VERIFY (SSH via bastion → systemctl status + curl)
      → STOP instance (clean disk state)
        → SNAPSHOT disk
          → IMAGE from snapshot
            → DELETE instance

Instance = temporary factory
Image = permanent, reusable artifact
```

## GCP ↔ AWS Mapping

```
GCP Custom Image        ↔  AWS AMI
GCP Snapshot             ↔  AWS EBS Snapshot
GCP Instance Template    ↔  AWS Launch Template
GCP Managed Instance Grp ↔  AWS Auto Scaling Group
GCP Cloud NAT            ↔  AWS NAT Gateway
GCP Firewall Rules+Tags  ↔  AWS Security Groups
GCP Network Tags         ↔  AWS SG assignment (different mechanism)
```

## Disk → Snapshot → Image Relationship

```
Running Instance
  └─ Boot Disk (contains OS + apps + configs)
       │
       ▼ (instance STOPPED first)
     Snapshot (point-in-time disk copy, ~2.17GB)
       │
       ▼
     Custom Image (launchable artifact)
       │
       ▼ (next lecture)
     Instance Template → Managed Instance Group → Auto-scaled instances
```

## Startup Script Summary

```
app-golden.sh:
  1. Create user + sudoers          (SSH access)
  2. apt update + install JDK       (Java runtime)
  3. Download + extract Tomcat      (web server)
  4. Create Tomcat user + ownership (security)
  5. Create systemctl service file  (process management)
  6. Download + install Maven 3.9.9 (build tool)
  7. Clone vprofile source code     (application code)
  8. mvn build                      (produce .war artifact)
  9. Remove default Tomcat app      (clean deployment)
  10. Copy .war to webapps          (deploy vprofile)
  11. systemctl restart tomcat      (start application)

Verify script file:
  First line: #!/bin/bash
  Last line:  systemctl restart tomcat
  Wrong? Delete and recreate.
```

## Instance Launch Command

```
gcloud compute instances create vprofile-golden \
  --zone=us-central1-a \
  --machine-type=e2-small \       ← NOT e2-micro (Maven+Tomcat freeze)
  --subnet=<private-subnet> \
  --no-address \                   ← no public IP (private subnet)
  --tags=app \                     ← activates matching firewall rules
  --metadata-from-file=startup-script=app-golden.sh
```

## Tag-Based Firewall Rules

```
Tag: app
  ├─ allow-ssh-bastion:         port 22 ← bastion SG
  └─ allow-load-balancer-to-app: port 8080 ← LB IP range

Instance created with --tags=app
  → BOTH rules automatically applied
  → No manual SG attachment needed

GCP: tags on instance ← match → targets on firewall rules
AWS: SG directly assigned to instance
```

## Why Private Subnet (Two Tests)

```
Test 1: Cloud NAT works?
  Script downloads packages from internet
  Private subnet → Cloud NAT → Internet
  Script completes ✓ → Cloud NAT works ✓

Test 2: Bastion SSH works?
  SSH from bastion (public) → golden instance (private)
  Login succeeds ✓ → firewall rules + VPC routing ✓
```

## SSH Access Chain (GCP)

```
Cloud Shell / Local → bastion (public IP, devops user)
  → copy private key content manually (cat → copy → vi → paste)
    → chmod 400 gcp-key.pem
      → ssh -i gcp-key.pem devops@<golden-private-ip>

Key transfer method: copy-paste content (not scp)
⚠️ No extra characters in key file → auth fails
```

## Verification Commands

```
systemctl status tomcat      → active (running) ✓
curl http://localhost:8080    → HTML with "registration" and "login" ✓
```

## Snapshot + Image Commands

```
STOP:     gcloud compute instances stop vprofile-golden --zone=us-central1-a
SNAPSHOT: gcloud compute disks snapshot vprofile-golden \
            --snapshot-names=vprofile-snapshot --zone=us-central1-a
IMAGE:    gcloud compute images create vprofile-image \
            --source-snapshot=vprofile-snapshot \
            --storage-location=us-central1
DELETE:   gcloud compute instances delete vprofile-golden --zone=us-central1-a
```

## Cloud Shell Session Timeout

```
Session times out → re-authenticate:
  gcloud auth login
  gcloud config set project <project-id>
Then retry the command.
```

## Machine Type Decision

```
e2-micro:  too small → Maven + Tomcat → instance freezes
e2-small:  sufficient for build + run
Instance is temporary → slight cost increase acceptable
```

## What Persists After This Lecture

```
KEPT:
  ├─ vprofile-snapshot (in Compute Engine → Snapshots)
  ├─ vprofile-image (in Compute Engine → Images)
  ├─ Bastion host (still running)
  ├─ VPC, subnets, firewall rules, Cloud NAT
  └─ All network infrastructure

DELETED:
  └─ vprofile-golden instance (no longer needed)

NEXT LECTURE:
  Instance Template (references vprofile-image)
    → Managed Instance Group (auto-scaling)
```

## Reusable Engineering Patterns

**1. Temporary Factory → Permanent Artifact**

```
Create temporary resource → configure it → capture state → delete resource
Artifact (image) persists → used to create many replicas

Same pattern:
  Docker: build container → commit as image → delete container
  Packer: launch instance → provision → create AMI → terminate
  CI/CD: build server → produce artifact → server is ephemeral
```

**2. Multi-Purpose Testing Through Placement**

```
Choose private subnet for temporary instance
  → tests Cloud NAT (outbound internet)
  → tests bastion SSH (cross-subnet access)
  → accomplishes the primary task (image creation)

Pattern: strategic placement decisions that validate infrastructure
         while accomplishing the immediate task
```

**3. Tag-Based Rule Association**

```
Instance gets tag → rules targeting that tag auto-apply
  → no manual attachment needed
  → add/remove rules later → automatically affect tagged instances

Pattern: declarative association via metadata
Same as: K8s labels + selectors, AWS resource tags + IAM policies
```

***

*This completes the full reconstruction. Theory explains the golden image pipeline, the GCP snapshot-to-image process, and the tag-based firewall model. Practical walks through every command from script creation to instance deletion. The Compression Map enables instant recall of the full pipeline, the GCP-AWS mapping, and the strategic testing pattern of private subnet placement.* [\[297-creati...m-vm-image \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/297-creating-a-custom-vm-image.txt)
