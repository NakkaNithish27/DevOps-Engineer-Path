# 🎓 Deep Learning Material: EC2 Log Management on AWS — Archiving to S3, Streaming to CloudWatch, and ELB Access Logs with Bucket Policies

**Source:** Video lecture on AWS log management (from [276-ec2-logs.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt?EntityRepresentationId=ef9dc6e7-433f-4f88-9ee5-f652b0a8062d) caption file) [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

**Video Context:** This is a comprehensive log management lecture covering three distinct log-handling strategies: **(1)** manually archiving logs from an EC2 instance to S3 (tar → aws s3 cp/sync → clean), **(2)** streaming live logs to CloudWatch using the awslogs agent (with metric filters and alarms), and **(3)** enabling ELB access logs to S3 using S3 bucket policies. The lecture progressively introduces more sophisticated approaches and touches on critical concepts: IAM roles vs. access keys for service-to-service authentication, CloudWatch metrics/alarms from log data, and S3 bucket policies for cross-service access when roles can't be attached. This is one of the most architecturally rich lectures — it connects EC2, S3, IAM, CloudWatch, and ELB in a single operational flow.

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — The Log Problem: Growth, Disk Space, and Operational Need

Every running service generates log files. The instructor demonstrates with the HTTPd web server: even two users accessing the site generates significant log entries. *"Imagine thousands of users or millions of users accessing your web services, how much log it'll generate."* Different services and processes generate different log files, and their combined size **continuously grows**, eventually consuming all available disk space. [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

The fundamental problem has two dimensions: **(1)** logs consume disk space and must be managed, and **(2)** logs contain valuable operational data that must be preserved and made accessible. Simply deleting logs solves the first problem but destroys the second. The lecture presents three progressively more sophisticated solutions that address both dimensions.

***

## 1.2 — Solution 1: Archive → Transfer → Clean (Manual S3 Approach)

The simplest approach is a three-step process: **archive** the log files into a compressed tarball, **transfer** the archive to S3 (durable, cheap storage outside the instance), and **clean** the original log files to reclaim disk space. [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

The instructor performs this manually, but explicitly notes the automation path: *"If you have this method of taking backups, then you better create a script for it. You can use Bash, Python, or Ansible and then you run it in a Cron job."* The manual process is for understanding; the real-world implementation is automated and scheduled. [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

### `aws s3 cp` vs. `aws s3 sync`

The instructor demonstrates both S3 transfer commands and explains the critical difference: [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

**`cp`** — Copies the specified file every time you run it. If you run it again, it copies the same file again (duplicating it). It's a one-shot operation.

**`sync`** — Copies only the **differential data** — files that don't already exist in the destination, or files that have changed. If you add a new file to the source directory and run sync again, only the new file is transferred. Already-synced files are skipped. *"Whatever is not copied, it's just gonna do the sync."* [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

For log archiving workflows, `sync` is generally preferred because it's idempotent — you can run it repeatedly without duplicating data.

***

## 1.3 — Log Cleaning: The `/dev/null` Redirect Technique

To clear a log file **without deleting it** (the service is still writing to it), the instructor uses:

```bash
cat /dev/null > /var/log/httpd/access_log
```

This redirects the "empty content" of `/dev/null` into the log file, effectively truncating it to zero bytes. The file still exists (the service can continue writing to it), but all previous content is removed. This is safer than `rm` because deleting a file that a running service has open can cause issues — the service may continue writing to a deleted file handle, and no new file gets created until the service restarts. [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

***

## 1.4 — IAM Roles vs. Access Keys: The Right Authentication for Services

The instructor initially uses **IAM access keys** (`aws configure` with access key + secret key) for the EC2 instance to access S3. Then he introduces the **better approach**: IAM roles. [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

*"Roles is a way of giving permission to a service, like for example to EC2 service, to access some other service like S3 service. So you can assign role to EC2 instance with privilege of S3 access and there is no chance of exposing access key and secret key, you don't need to rotate the keys."* [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

The instructor proves the role works by **removing the credentials file** and then showing that `aws s3 ls` still works — the instance authenticates through the attached role, not through stored keys. [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

The role created in this lecture (`log-admin-role`) includes **two policies**: S3 Full Access (for log archiving) and CloudWatch Logs Full Access (for the streaming solution that follows). [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

***

## 1.5 — Solution 2: Live Log Streaming to CloudWatch (Agent-Based)

The archiving approach has a limitation: logs are only accessible after they're archived and uploaded. For real-time troubleshooting, you need **live streaming** — logs appearing in a dashboard as they're generated. [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

The instructor presents the real-world scenario: *"Your application is going to generate log. You're not gonna give access to the developers to follow production system. You're going to log into the system, fetch the log from the production system, and give it to the developers... it will be a very good idea if you're able to stream the logs to some dashboard so the developers will have access to the dashboard, they will see the logs live."* [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

**AWS CloudWatch Logs** solves this. You install a **CloudWatch Logs agent** (`awslogs`) on the EC2 instance, configure it to watch specific log files, and it continuously streams new log entries to CloudWatch. [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

### CloudWatch Logs Architecture

The structure in CloudWatch is hierarchical: [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

* **Log Group** — a container that holds related log streams (e.g., `wave-web` for all web server logs)
* **Log Stream** — a specific source of logs within a group (e.g., `web01-httpd-access` for the access log of web01, `web01-sys-logs` for system messages)

You can have multiple streams in one group, and the configuration file (`/etc/awslogs/awslogs.conf`) defines which log files map to which groups and streams. [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

### What CloudWatch Enables Beyond Viewing

Once logs are in CloudWatch, you can: [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

* **View live logs** in the dashboard
* **Export to S3** for archiving
* **Send to Elasticsearch** for advanced search and analysis
* **Trigger Lambda functions** based on log events
* **Create metric filters** — extract numeric metrics from text log data
* **Create alarms** based on those metrics

The instructor demonstrates creating a **metric filter** that watches for a specific IP address (a hypothetical "hacker IP") in the access log. If that IP appears, a metric is generated, and an alarm can notify you. *"If this IP appears to be these many times, you get notification."* This turns unstructured text logs into structured, actionable monitoring. [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

***

## 1.6 — Solution 3: ELB Access Logs to S3 (Bucket Policy Approach)

Load balancers also generate access logs, but they present a unique challenge: **you cannot SSH into a load balancer** (it's a managed service with no operating system access), and **you cannot attach an IAM role** to a load balancer the way you can to an EC2 instance. [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

The solution is **S3 bucket policies**. Instead of the load balancer authenticating to S3, you configure the S3 bucket to **allow writes from the ELB service**. The bucket policy is a JSON document that explicitly permits the ELB service (identified by a region-specific ELB account ID) to write objects to the bucket. [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

### S3 Bucket Policy Structure

The instructor walks through the JSON policy in detail: [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

```json
{
  "Version": "...",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "AWS": "arn:...elb-account-id:root" },
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::bucket-name/prefix/AWSLogs/aws-account-id/*"
    },
    ...
  ]
}
```

* **Version** — always the same standard date string
* **Statement** — a list of rules (three rules in this policy)
* **Effect** — `Allow` or `Deny`
* **Principal** — **who** is accessing (the ELB service, identified by a region-specific account ID)
* **Action** — **what** they can do (`s3:PutObject` for writing logs)
* **Resource** — **where** they can do it (the specific bucket and path)

The **ELB account ID** is **region-specific** — each AWS region has a different ELB account ID. The instructor checks the documentation table: *"Load balancer account ID is region specific... our instance is in us-east-2 Ohio, that's the load balancer account ID."* Using the wrong region's ID causes the policy to fail silently. [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

The instructor also mentions you need your **AWS account ID** in the resource ARN path. [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

### Three Authentication Models for S3 Access

This lecture demonstrates all three S3 authentication models: [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

| Method                 | Used By                                     | How                                          |
| ---------------------- | ------------------------------------------- | -------------------------------------------- |
| **IAM Access Keys**    | Humans, CLI on local machines               | `aws configure` with access key + secret key |
| **IAM Roles**          | EC2 instances, AWS services                 | Attach role to instance; auto-authenticates  |
| **S3 Bucket Policies** | Services that can't use keys or roles (ELB) | Policy on the bucket allows specific service |

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building and Why

We are implementing three log management strategies on AWS: **(1)** manually archiving HTTPd logs to S3, **(2)** streaming live logs to CloudWatch via the awslogs agent, and **(3)** enabling ELB access logs to S3 via bucket policies. The final outcome: logs are preserved in S3, live-viewable in CloudWatch with metric filters, and load balancer access logs flow automatically to S3.

**Prerequisites:** An EC2 instance running Amazon Linux 2 with HTTPd installed and serving a web template from tooplate.com. [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

***

## Part A: Archive Logs to S3

### Step 1: Examine Log Files

```bash
cd /var/log/httpd
ls
```

You'll see `access_log` and `error_log`. Check the access log:

```bash
cat access_log
```

Use `tail -f access_log` to watch live entries as users access the site. [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

### Step 2: Create an S3 Bucket

AWS Console → **S3** → **Create Bucket** → name: `wave-web-logs-<unique-numbers>` → same region as EC2 → **Create Bucket** [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

### Step 3: Archive the Log Files

```bash
tar czvf wave-web01-httpdlogs-19122020.tar.gz *
```

* `tar` — archive utility
* `c` — create archive
* `z` — compress with gzip
* `v` — verbose (show files being archived)
* `f` — filename follows
* `wave-web01-httpdlogs-19122020.tar.gz` — archive name (include date for identification)
* `*` — all files in the current directory [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

```bash
mkdir /tmp/logs-wave
mv wave-web01-httpdlogs-19122020.tar.gz /tmp/logs-wave/
```

### Step 4: Clean the Log Files

```bash
cat /dev/null > access_log
cat /dev/null > error_log
```

Truncates files to zero bytes without deleting them. Verify: `cat access_log` should show nothing (or very recent entries if the service is actively logging). [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

### Step 5: Set Up AWS CLI and IAM User

```bash
yum install awscli
```

Create IAM user: IAM → **Add User** → name: `s3-log-admin` → **Programmatic access** → attach **AmazonS3FullAccess** → create → copy access key + secret key. [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

```bash
aws configure
```

Enter access key, secret key, region, `json` format. [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

**Verify:** `aws s3 ls` — should list all buckets. [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

### Step 6: Transfer Archive to S3

**Using cp:**

```bash
aws s3 cp /tmp/logs-wave/wave-web01-httpdlogs-19122020.tar.gz s3://wave-web-logs-<numbers>/
```

**Using sync (preferred for repeated runs):**

```bash
aws s3 sync /tmp/logs-wave/ s3://wave-web-logs-<numbers>/
```

Sync only copies new/changed files. Test by creating a test file in the source directory and running sync again — only the new file transfers. [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

### Step 7: Switch from Access Keys to IAM Role

**Create role:** IAM → **Roles** → **Create role** → AWS service → **EC2** → attach policies: **AmazonS3FullAccess** + **CloudWatchLogsFullAccess** → name: `log-admin-role` → **Create role** [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

**Remove stored credentials:**

```bash
rm ~/.aws/credentials
aws s3 ls    # → ERROR (no credentials)
```

**Attach role:** EC2 → select instance → **Actions** → **Security** → **Modify IAM role** → select `log-admin-role` → **Save** [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

**Verify:**

```bash
aws s3 ls    # → works (authenticating via role)
```

 [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

***

## Part B: Stream Logs to CloudWatch

### Step 8: Install CloudWatch Logs Agent

```bash
yum install awslogs
```

This installs the `awslogsd` service and creates the configuration file at `/etc/awslogs/awslogs.conf`. [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

### Step 9: Configure Log Streams

```bash
vim /etc/awslogs/awslogs.conf
```

The file has a default section at the end for `/var/log/messages`. Copy that 7-line block and paste it at the end to create a new entry for HTTPd access logs: [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

**Modify the new block:**

| Field             | Value                       |
| ----------------- | --------------------------- |
| `file`            | `/var/log/httpd/access_log` |
| `log_stream_name` | `web01-httpd-access`        |
| `log_group_name`  | `wave-web`                  |

**Also update the original `/var/log/messages` block:**

| Field             | Value            |
| ----------------- | ---------------- |
| `log_stream_name` | `web01-sys-logs` |
| `log_group_name`  | `wave-web`       |

Both streams go into the **same log group** (`wave-web`). [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

**Verify the log file path exists:**

```bash
cat /var/log/httpd/access_log
```

 [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

### Step 10: Start and Enable the Service

```bash
systemctl restart awslogsd
systemctl enable awslogsd
```

 [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

### Step 11: Verify in CloudWatch

AWS Console → **CloudWatch** → **Logs** → **Log groups** → you should see `wave-web` → click → you should see both streams (`web01-httpd-access` and `web01-sys-logs`). [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

Access the web server in a browser to generate new log entries → refresh the CloudWatch stream → new entries appear. [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

### Step 12: Create a Metric Filter (Example)

1. Select a log stream → **Actions** → **Create metric filter** [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)
2. **Filter pattern:** enter a specific IP address (e.g., a "hacker IP")
3. **Test:** preview matching entries
4. **Filter name:** `hacker-ip`
5. **Metric namespace:** `hackers`
6. **Metric value:** `1` (count each occurrence)
7. **Create metric filter** [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

From the metric, you can **create an alarm** that triggers notifications when the IP appears a certain number of times. [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

***

## Part C: ELB Access Logs to S3

### Step 13: Create a Load Balancer

EC2 → **Load Balancers** → **Create** → **Classic Load Balancer** → name: `wave-elb` → create security group `wave-elb-sg` → health check threshold: 2 → add the web server instance → **Create** [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

### Step 14: Create S3 Folder for ELB Logs

Go to your S3 bucket → **Create folder** → name: `elb-wave` [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

### Step 15: Apply S3 Bucket Policy

1. Find the ELB bucket policy in the AWS documentation (Google: "enable access logs for your classic load balancer") [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

2. Copy the JSON policy template

3. **Customize:**
   * Replace `elb-account-id` with the **region-specific ELB account ID** from the documentation table
   * Replace `bucket-name` with your actual bucket name
   * Replace `prefix` with your folder name (`elb-wave`)
   * Replace `aws-account-id` with your AWS account ID [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

4. S3 bucket → **Permissions** → **Bucket policy** → **Edit** → paste the customized policy → **Save changes** [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

### Step 16: Enable ELB Access Logs

Load Balancer → **Attributes** → **Access log** → **Enable** → interval: **5 minutes** → S3 bucket: your bucket name → prefix: `elb-wave` → **Save** [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

**If save fails:** The bucket policy is incorrect — check the ELB account ID (region-specific) and AWS account ID. [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

**If save succeeds:** Check S3 → `elb-wave/AWSLogs/` → a test log file should appear immediately. Full access logs appear after 5 minutes. [\[276-ec2-logs \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/276-ec2-logs.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🔷 Three Log Management Strategies

```
STRATEGY 1: Archive → S3 → Clean (manual/cron)
  tar logs → aws s3 cp/sync → /dev/null > logfile
  Best for: periodic backup, disk space recovery

STRATEGY 2: CloudWatch Logs Agent (live streaming)
  awslogs agent → reads log files → streams to CloudWatch
  Best for: real-time monitoring, developer access, alerting

STRATEGY 3: ELB Access Logs → S3 (bucket policy)
  ELB → writes directly to S3 (no agent possible)
  Best for: managed services without OS access
```

***

## 🔷 Three S3 Authentication Models

```
METHOD              USED BY                 HOW
─────────────       ─────────────────       ────────────────────────────
IAM Access Keys     Humans, local CLI       aws configure (key + secret)
IAM Roles           EC2 instances           Attach to instance, auto-auth
S3 Bucket Policy    ELB, services w/o roles JSON policy on bucket allows writes

SECURITY RANKING: Roles > Bucket Policy > Access Keys
                  (Roles = no stored credentials, auto-rotated)
```

***

## 🔷 Key Commands

```bash
# Archive
tar czvf name-date.tar.gz *
cat /dev/null > logfile              # truncate without deleting

# S3 Transfer
aws s3 cp <file> s3://<bucket>/     # copy (every time)
aws s3 sync <dir> s3://<bucket>/    # sync (differential only)
aws s3 ls                           # list buckets (verify auth)

# CloudWatch Agent
yum install awslogs                 # install agent (Amazon Linux 2)
vim /etc/awslogs/awslogs.conf       # configure log files + streams
systemctl restart awslogsd          # apply config
systemctl enable awslogsd           # persist across reboots
```

***

## 🔷 CloudWatch Logs Configuration Structure

```
/etc/awslogs/awslogs.conf

[section-name]                       ← any label
file = /var/log/httpd/access_log     ← actual log file path (MUST EXIST)
log_group_name = wave-web            ← CloudWatch group (container)
log_stream_name = web01-httpd-access ← CloudWatch stream (specific source)

Multiple sections = multiple log files streamed
Same log_group_name = streams grouped together in CloudWatch
```

***

## 🔷 CloudWatch Hierarchy

```
CloudWatch Logs
  └── Log Group: wave-web
        ├── Stream: web01-sys-logs       ← /var/log/messages
        └── Stream: web01-httpd-access   ← /var/log/httpd/access_log

FROM STREAMS YOU CAN:
  ├── View live logs
  ├── Export → S3
  ├── Send → Elasticsearch
  ├── Trigger → Lambda
  └── Create → Metric Filter → Alarm → Notification
```

***

## 🔷 Metric Filter Flow

```
Log stream (text data)
  │
  ▼
Metric Filter (pattern match, e.g., specific IP)
  │
  ▼
Custom Metric (numeric: count of matches)
  │
  ▼
Alarm (threshold: if count > N → notify)
  │
  ▼
Notification (SNS → email/SMS/etc.)

TRANSFORMS: unstructured text logs → structured numeric metrics → actionable alerts
```

***

## 🔷 ELB Bucket Policy (Key Elements)

```json
{
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "AWS": "arn:...<elb-account-id>:root" },
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::<bucket>/<prefix>/AWSLogs/<account-id>/*"
    }
  ]
}

MUST CUSTOMIZE:
  elb-account-id  → REGION-SPECIFIC (lookup table in docs)
  bucket-name     → your actual S3 bucket
  prefix          → folder name (e.g., elb-wave)
  aws-account-id  → your AWS account ID

WRONG elb-account-id = policy silently fails
```

***

## 🔷 `cp` vs. `sync`

```
aws s3 cp:
  Copies EVERY time you run it
  Same file = duplicated
  Good for: single file transfers

aws s3 sync:
  Copies only DIFFERENTIAL data
  Already-synced files = skipped
  Good for: repeated/scheduled backup workflows
  Idempotent
```

***

## 🔷 Log File Locations (Amazon Linux 2 / CentOS 7)

```
/var/log/httpd/access_log     ← HTTPd access log
/var/log/httpd/error_log      ← HTTPd error log
/var/log/messages             ← system messages (default awslogs target)
```

***

## 🔷 IAM Role Setup (log-admin-role)

```
Service: EC2
Policies:
  ├── AmazonS3FullAccess          (archive logs to S3)
  └── CloudWatchLogsFullAccess    (stream logs to CloudWatch)

Attach: EC2 → Actions → Security → Modify IAM role → select role

PROOF:
  rm ~/.aws/credentials
  aws s3 ls → STILL WORKS (role-based auth, no keys needed)
```

***

## 🔷 Why ELB Can't Use Roles or Keys

```
EC2 Instance:
  ✅ Has OS → can run aws configure (keys)
  ✅ Is AWS service → can attach IAM role

Load Balancer:
  ❌ No OS → can't SSH or run aws configure
  ❌ Can't attach IAM role
  ✅ CAN use S3 bucket policy (bucket allows ELB to write)
```

***

## 🔷 Automation Path (Mentioned)

```
Manual process → AUTOMATE with:
  Bash script + Cron job
  OR Python script + scheduler
  OR Ansible playbook + scheduled run

"If you have this method of taking backups,
 then you better create a script for it."
```

***

## 🔷 Reusable Engineering Pattern: Progressive Log Management Maturity

```
LEVEL 1: Archive & Clean (reactive, scheduled)
  tar → S3 → clean disk
  Simple, batch-oriented, no real-time visibility

LEVEL 2: Live Streaming (proactive, continuous)
  Agent → CloudWatch → dashboard + metrics + alarms
  Real-time, queryable, actionable

LEVEL 3: Service-Level Integration (managed services)
  S3 bucket policy → ELB writes directly
  No agent possible, policy-based access

MATURITY PROGRESSION:
  Manual cleanup → Automated streaming → Service-native logging
  
Each level adds: visibility, automation, and operational capability
without removing the previous level's utility.
```

This lecture demonstrates all three levels in sequence, showing how log management evolves from simple disk cleanup to a full observability pipeline. <cite>turn21search1</cite>
