# 🎓 AWS Lambda: Serverless Computing & Security Group Compliance Automation — Deep Learning Material

**Source:** Video caption file — *AWS Lambda Serverless Computing* + accompanying IAM Policy and Python Lambda Code [\[277-aws-lambda \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277-aws-lambda.txt), [\[277.SGCompPolicy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277.SGCompPolicy.txt), [\[277.PyLambCodeSGComp \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277.PyLambCodeSGComp.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — The Problem: Why Run a Server If You Just Need to Run Code?

With EC2, you launch an instance, select instance type (CPU/memory), select EBS volume (storage), log in, install your application, and run it. The server runs continuously — you pay for it continuously — whether your code is executing or sitting idle. But many workloads don't need a permanent server. What if you just need to **run some code, get a result, and be done with it**? Setting up an entire EC2 instance for a task that runs for two minutes every hour is massive over-provisioning. You're paying for 58 minutes of idle time per hour. [\[277-aws-lambda \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277-aws-lambda.txt)

This is the problem **AWS Lambda** solves. Lambda lets you **run code without provisioning or managing any EC2 instances** — without managing any servers at all. You upload your code, define when it should run, and AWS handles everything else: the compute resources, the scaling, the availability, the operating system. You pay **only for the compute time you actually use**. If your code runs for two minutes, you pay for two minutes. When it's not running, you pay nothing. [\[277-aws-lambda \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277-aws-lambda.txt)

***

## 1.2 — What Lambda Is: The Core Model

Lambda is a **serverless compute service**. "Serverless" doesn't mean there are no servers — it means **you don't see, manage, or think about servers**. AWS runs your code on infrastructure that's completely abstracted away from you.

The working model is straightforward: [\[277-aws-lambda \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277-aws-lambda.txt)

1. **Upload your code as a function** — Lambda supports **Python, Node.js, Java, .NET**, and also provides a temporary **Amazon Linux OS** environment to run arbitrary commands.
2. **Define a trigger** — How and when should the function execute? Options include: AWS events (S3 upload, security group change), API Gateway calls, EventBridge schedules (cron jobs), direct invocation from code or shell.
3. **When the trigger fires → Lambda executes the code** — AWS automatically provisions the compute resources, runs the function, and tears down the resources.
4. **After execution, you handle the output** — Upload results to S3, send notifications via SNS, write to a database, return an API response — whatever your code does.

You don't worry about compute resources, scaling, or availability. Lambda **scales automatically** to handle your requests — whether it's 1 invocation per hour or 1,000 concurrent invocations. [\[277-aws-lambda \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277-aws-lambda.txt)

***

## 1.3 — Lambda as Event-Driven Architecture

Lambda is fundamentally an **event-driven execution model**. AWS is full of events: you create a security group (event), upload a file to S3 (event), power on an instance (event), reboot it (event). Lambda lets you attach code to these events — "when X happens, run this code." [\[277-aws-lambda \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277-aws-lambda.txt)

The trigger types include:

* **S3 events** — Object uploaded/deleted → run function (e.g., check compliance, resize image)
* **EventBridge schedule** — Cron-style scheduling → run function periodically (e.g., every hour)
* **EventBridge rules** — React to specific AWS events
* **API Gateway** — HTTP request → run function (backend API)
* **Direct invocation** — Call function from code or CLI [\[277-aws-lambda \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277-aws-lambda.txt)

> 🔍 **Deep Dive:** The event-driven model is a fundamental architectural paradigm. Instead of a server continuously polling for work ("is there something to do?"), the system **reacts** to events ("something happened, run this code"). This is inherently efficient — compute is consumed only when there's actual work. This pattern extends far beyond Lambda: message queues (SQS), pub/sub systems (SNS), Kubernetes event controllers, and webhook-based integrations all follow the same trigger → action model.

***

## 1.4 — Lambda Execution Environment and Constraints

Lambda provides a **temporary execution environment** — an Amazon Linux container that exists only for the duration of the function execution. The key operational constraint is the **timeout**. By default, Lambda functions have a **3-second timeout** — if the code doesn't complete in 3 seconds, it's killed. For longer-running tasks (like scanning security groups across all regions), you must **increase the timeout** in the function configuration. The video sets it to **5 minutes** for the compliance scanner. [\[277-aws-lambda \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277-aws-lambda.txt)

The maximum timeout for Lambda is 15 minutes. If your code needs longer, Lambda isn't the right service — you'd use EC2, ECS, or Step Functions instead.

***

## 1.5 — The Exercise Architecture: Security Group Compliance Scanner

The lecture builds a complete, real-world automation system — not a toy example. The instructor explicitly states: "This is not just some example, it is actually used. I have used it personally to make sure nobody opens port 22 from anywhere." [\[277-aws-lambda \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277-aws-lambda.txt)

### What the System Does

A **Python function** scans **all security groups** in **all AWS regions** and finds any inbound rule that allows traffic from **`0.0.0.0/0`** (anywhere). This detects overly permissive firewall rules — a critical security compliance concern. The function then:

* **Uploads the findings** as a JSON report to an **S3 bucket**
* **Sends an email notification** via **SNS** with the findings
* Runs **automatically every hour** via an **EventBridge schedule** [\[277-aws-lambda \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277-aws-lambda.txt)

### The Five Components

| Component                | Role                                          |
| ------------------------ | --------------------------------------------- |
| **S3 Bucket**            | Stores compliance reports (JSON files)        |
| **SNS Topic**            | Sends email notifications with findings       |
| **IAM Role + Policy**    | Grants Lambda permission to access EC2/S3/SNS |
| **Lambda Function**      | Executes the Python compliance-checking code  |
| **EventBridge Schedule** | Triggers the Lambda function every hour       |

 [\[277-aws-lambda \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277-aws-lambda.txt)

***

## 1.6 — The IAM Policy: Defining Exact Permissions

Lambda functions run with an **IAM role** that defines exactly what AWS services and resources the function can access. This follows the **principle of least privilege** — the function gets only the permissions it needs, nothing more.

The policy for this exercise grants three groups of permissions: [\[277.SGCompPolicy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277.SGCompPolicy.txt)

**EC2 permissions** (for scanning security groups):

* `ec2:DescribeRegions` — List all AWS regions
* `ec2:DescribeInstances` — List instances (contextual)
* `ec2:DescribeSecurityGroups` — Read security group rules
* `ec2:RevokeSecurityGroupIngress` — Remove inbound rules (for future remediation capability)
* Resource: `*` (all EC2 resources, since security groups exist across all regions)

**SNS permissions** (for sending notifications):

* `sns:Publish` — Send a message to an SNS topic
* Resource: Specific SNS topic ARN (only the compliance notification topic, not all topics)

**S3 permissions** (for storing reports):

* `s3:PutObject` — Upload files
* `s3:GetBucketLocation` — Check bucket location
* `s3:ListBucket` — List bucket contents
* Resource: Specific S3 bucket ARN + all objects within it (`bucket/*`) [\[277.SGCompPolicy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277.SGCompPolicy.txt)

> 🔍 **Deep Dive:** Notice the resource scoping difference. EC2 permissions use `*` (all resources) because security groups are distributed across all regions and accounts. But SNS and S3 permissions are **scoped to specific ARNs** — only the compliance-specific topic and bucket. This is least-privilege in action: broad where necessary (scanning everything), narrow where possible (writing only to designated outputs). [\[277.SGCompPolicy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277.SGCompPolicy.txt)

***

## 1.7 — The Python Code: How the Compliance Scanner Works

The Lambda function code follows a clear algorithmic flow: [\[277.PyLambCodeSGComp \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277.PyLambCodeSGComp.txt)

1. **Initialize AWS clients** — Create `boto3` clients for EC2, SNS, and S3. (`boto3` is the AWS SDK for Python — the library that lets Python code interact with AWS services.)
2. **Collect all AWS regions** — `ec2.describe_regions()` returns every region. The region names are extracted into a list.
3. **Nested loop: regions → security groups → rules** — For each region, create a region-specific EC2 client, fetch all security groups in that region, and iterate through each security group's inbound permissions (`IpPermissions`).
4. **Check for `0.0.0.0/0`** — For each rule, check if any `IpRanges` entry has `CidrIp` equal to `0.0.0.0/0`. This means the rule allows traffic from **anywhere on the Internet** — a compliance violation.
5. **Record findings** — Each violation is recorded with: region, security group ID, port number, and protocol.
6. **Send SNS notification** — Publish the findings (or "no findings" message) to the SNS topic.
7. **Upload report to S3** — Create a timestamped JSON file (e.g., `security-audit-2026-06-12-10-30-00.json`) and upload it to the S3 bucket.
8. **Return result** — Return a response with the findings. [\[277.PyLambCodeSGComp \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277.PyLambCodeSGComp.txt)

The instructor is transparent: "I have not written this Python code. I understand this very well, but I have asked ChatGPT to generate this code for me. I have just given the requirement." This reflects a realistic modern workflow — AI generates the code, the engineer understands, validates, and deploys it. [\[277-aws-lambda \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277-aws-lambda.txt)

> ⚠️ **Expert Note:** The code creates a **new EC2 client for each region** (`boto3.client('ec2', region_name=region)`) inside the loop. This is necessary because AWS API calls are region-scoped — a single EC2 client can only query one region. To scan all regions, you must iterate and create region-specific clients. This is a common pattern in any multi-region AWS automation. [\[277.PyLambCodeSGComp \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277.PyLambCodeSGComp.txt)

***

## 1.8 — EventBridge Schedule: The Cron-Based Trigger

The final component is an **EventBridge schedule** that triggers the Lambda function automatically. The schedule uses **cron format** — the same format as Linux cron jobs: [\[277-aws-lambda \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277-aws-lambda.txt)

```
0 * * * ? *
```

* `0` — Minute: at the 0th minute (start of the hour)
* `*` — Hour: every hour
* `*` — Day of month: every day
* `*` — Month: every month
* `?` — Day of week: any (the `?` means "no specific value")
* `*` — Year: every year

This runs the function at the **start of every hour**, every day, indefinitely. The console shows the **next trigger dates** so you can verify the schedule is correct.

EventBridge needs its own **IAM role** to invoke Lambda — separate from the Lambda function's execution role. The Lambda role defines what the function can do; the EventBridge role defines EventBridge's permission to trigger the function. [\[277-aws-lambda \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277-aws-lambda.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We're Building

A fully automated **security group compliance monitoring system**: a Lambda function that scans every security group in every AWS region every hour, detects any rule allowing traffic from `0.0.0.0/0` (anywhere), emails the findings via SNS, and stores a JSON report in S3. Five AWS services wired together into one automated security pipeline. [\[277-aws-lambda \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277-aws-lambda.txt)

***

## Step 1: Create the S3 Bucket

### The Action

AWS Console → Search **S3** → **Create bucket.**

| Setting | Value                                                            |
| ------- | ---------------------------------------------------------------- |
| Name    | `sg-compliance921` (must be globally unique — change the number) |
| Type    | General purpose                                                  |

 [\[277-aws-lambda \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277-aws-lambda.txt)

Click **Create bucket.** All other settings can remain default.

### Common Mistakes

* **Uppercase characters in bucket name** — S3 bucket names cannot contain uppercase. The video shows this error live.
* **Non-unique name** — S3 bucket names are globally unique across ALL AWS accounts. If the name is taken, you must choose a different one.

***

## Step 2: Create the SNS Topic and Subscription

### Step 2a: Create the Topic

AWS Console → Search **SNS** → **Create topic:**

| Setting      | Value                                              |
| ------------ | -------------------------------------------------- |
| Type         | **Standard**                                       |
| Name         | `SGCompliaceNotification` (or your preferred name) |
| Display name | Same as name                                       |

 [\[277-aws-lambda \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277-aws-lambda.txt)

Click **Create topic.**

### Step 2b: Create an Email Subscription

Go to **Subscriptions → Create subscription:**

| Setting   | Value                             |
| --------- | --------------------------------- |
| Topic ARN | Select the topic you just created |
| Protocol  | **Email**                         |
| Endpoint  | Your email address                |

 [\[277-aws-lambda \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277-aws-lambda.txt)

Click **Create subscription.**

### Step 2c: Confirm the Subscription

Go to your **email inbox** (check spam/junk folder). Find the SNS confirmation email and click **Confirm subscription**. Return to the SNS console and refresh — status should show **"Confirmed."** [\[277-aws-lambda \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277-aws-lambda.txt)

### Critical Warning

If you don't confirm, SNS cannot send emails. The Lambda function will execute successfully but no email arrives. Always verify "Confirmed" status.

***

## Step 3: Create the IAM Policy

### The Action

AWS Console → **IAM → Policies → Create policy → JSON tab.**

### The Policy Document

Download from lecture resources, or use: [\[277.SGCompPolicy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277.SGCompPolicy.txt)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeRegions",
        "ec2:DescribeInstances",
        "ec2:DescribeSecurityGroups",
        "ec2:RevokeSecurityGroupIngress"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": "sns:Publish",
      "Resource": "arn:aws:sns:us-east-1:<YOUR_ACCOUNT_ID>:<YOUR_SNS_TOPIC_NAME>"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetBucketLocation",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::<YOUR_BUCKET_NAME>",
        "arn:aws:s3:::<YOUR_BUCKET_NAME>/*"
      ]
    }
  ]
}
```

### Values You MUST Replace

| Placeholder             | Where to Find                      | Example                   |
| ----------------------- | ---------------------------------- | ------------------------- |
| `<YOUR_ACCOUNT_ID>`     | AWS Console top-right → Account ID | `983794312705`            |
| `<YOUR_SNS_TOPIC_NAME>` | SNS Console → Topics → Name        | `SGCompliaceNotification` |
| `<YOUR_BUCKET_NAME>`    | S3 Console → Buckets               | `sg-compliance921`        |

 [\[277-aws-lambda \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277-aws-lambda.txt), [\[277.SGCompPolicy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277.SGCompPolicy.txt)

### Name the Policy

Give it a name like `SGCompliancePolicy`. Click **Create policy.**

### How to Verify

After creation, scroll down to see the three services listed: EC2, S3, SNS — with their access levels and resource scopes. [\[277-aws-lambda \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277-aws-lambda.txt)

### Common Mistakes

* **Wrong account ID** — The SNS ARN won't match. The function will fail with an authorization error when trying to publish.
* **Wrong bucket name** — S3 operations will fail with access denied.
* **Missing the `/*` on the second S3 resource** — `PutObject` needs access to objects *inside* the bucket, not just the bucket itself.

***

## Step 4: Create the IAM Role

### The Action

IAM → **Roles → Create role:**

| Setting        | Value                                                            |
| -------------- | ---------------------------------------------------------------- |
| Trusted entity | **AWS service**                                                  |
| Use case       | **Lambda**                                                       |
| Permissions    | Search and select `SGCompliancePolicy` (the policy just created) |
| Role name      | `SGComplianceRole`                                               |

 [\[277-aws-lambda \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277-aws-lambda.txt)

Click **Create role.**

### Why "Use case: Lambda"

This tells AWS that the Lambda service is allowed to **assume** this role. Without this trust relationship, Lambda can't use the role's permissions.

***

## Step 5: Prepare the Python Code

### The Action

Download the Python code from the lecture resources or use a text editor. [\[277.PyLambCodeSGComp \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277.PyLambCodeSGComp.txt)

### Values You MUST Update in the Code

```python
sns_topic_arn = "arn:aws:sns:us-east-1:<YOUR_ACCOUNT_ID>:<YOUR_SNS_TOPIC_NAME>"
s3_bucket_name = "<YOUR_BUCKET_NAME>"
```

 [\[277.PyLambCodeSGComp \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277.PyLambCodeSGComp.txt)

Replace with your actual account ID, topic name, and bucket name — same values used in the IAM policy.

***

## Step 6: Create the Lambda Function

### The Action

AWS Console → Search **Lambda** → **Create function:**

| Setting        | Value                                                |
| -------------- | ---------------------------------------------------- |
| Option         | **Author from scratch**                              |
| Function name  | `SecurityGroupComplianceChecker`                     |
| Runtime        | **Python 3.13**                                      |
| Execution role | **Use an existing role** → select `SGComplianceRole` |

 [\[277-aws-lambda \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277-aws-lambda.txt)

Click **Create function.**

***

## Step 7: Configure the Timeout

### What We're Doing

Increasing the timeout from the default 3 seconds to 5 minutes, because scanning security groups across all regions takes over a minute.

### The Action

Lambda function page → **Configuration** tab → **General configuration** → **Edit:**

| Setting | Value                                  |
| ------- | -------------------------------------- |
| Timeout | **5 minutes** (or 2–3 minutes minimum) |

 [\[277-aws-lambda \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277-aws-lambda.txt)

Click **Save.**

### Why This Is Critical

With the default 3-second timeout, the function will be **killed mid-execution** before it finishes scanning all regions. The scan completes in roughly one minute, so 5 minutes provides comfortable headroom.

***

## Step 8: Deploy the Code

### The Action

Go to the **Code** tab → Select all existing code → **Delete it** → **Paste your Python code** → Click **Deploy.** [\[277-aws-lambda \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277-aws-lambda.txt)

Wait a few seconds for deployment confirmation.

***

## Step 9: Test the Function

### Step 9a: Create a Test Event

Click **Test** → **Create new test event:**

| Setting    | Value                                          |
| ---------- | ---------------------------------------------- |
| Event name | `TestLambda`                                   |
| Event JSON | Leave default (empty `{}` or default template) |

 [\[277-aws-lambda \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277-aws-lambda.txt)

Click **Save.**

### Step 9b: Execute the Test

Click **Test** again. The function begins executing. Watch the output area.

### Expected Behavior

* Execution takes about **1 minute** (scanning all regions).
* Status: **"Execution completed successfully."**
* Output shows findings: region, security group ID, port number, protocol for any rule allowing `0.0.0.0/0`. [\[277-aws-lambda \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277-aws-lambda.txt)

### How to Verify End-to-End

1. **S3 Bucket:** Go to your bucket → refresh → a timestamped JSON file should appear (e.g., `security-audit-2026-06-12-10-30-00.json`). Open it to see the findings. [\[277-aws-lambda \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277-aws-lambda.txt)
2. **Email:** Check your inbox for the SNS notification email with the compliance report.
3. **Create a test security group** with port 22 or 80 allowed from `0.0.0.0/0` (anywhere) to ensure it appears in findings.

### Troubleshooting

| Symptom             | Cause                               | Fix                                     |
| ------------------- | ----------------------------------- | --------------------------------------- |
| Timeout error       | Function timeout too low            | Increase to 5 minutes                   |
| Access denied (EC2) | IAM policy missing EC2 permissions  | Check policy has DescribeSecurityGroups |
| Access denied (S3)  | Wrong bucket name in policy or code | Verify bucket name matches in both      |
| Access denied (SNS) | Wrong ARN in policy or code         | Verify account ID and topic name        |
| No email received   | SNS subscription not confirmed      | Check email/spam, confirm subscription  |

***

## Step 10: Create the EventBridge Schedule

### The Action

AWS Console → Search **EventBridge** → **Schedules** → **Create schedule:**

| Setting                 | Value                                                                   |
| ----------------------- | ----------------------------------------------------------------------- |
| Name                    | `SecurityGroupComplianceSchedule`                                       |
| Description             | `Runs Lambda periodically to check open security groups`                |
| Schedule type           | **Schedule**                                                            |
| Schedule pattern        | **Recurring schedule**                                                  |
| Schedule type           | **Cron-based schedule**                                                 |
| Cron expression         | `0 * * * ? *`                                                           |
| Flexible time window    | **Off**                                                                 |
| Target                  | **AWS Lambda** → select `SecurityGroupComplianceChecker`                |
| Action after completion | **None**                                                                |
| Role                    | **Create a new role** (auto-generated name, add numbers for uniqueness) |

 [\[277-aws-lambda \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277-aws-lambda.txt)

Click **Create schedule.**

### Cron Expression Breakdown

```
0 * * * ? *
│ │ │ │ │ │
│ │ │ │ │ └── Year: every year
│ │ │ │ └──── Day of week: any
│ │ │ └────── Month: every month
│ │ └──────── Day of month: every day
│ └────────── Hour: every hour
└──────────── Minute: 0 (start of hour)
```

### How to Verify

The console shows **"Next trigger dates"** — confirm they show hourly intervals. Wait a few hours and check:

* Email notifications arriving every hour
* New JSON files appearing in S3 every hour [\[277-aws-lambda \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277-aws-lambda.txt)

***

## Step 11: Cleanup

### What to Remove

| Resource                 | Action                       | Notes                         |
| ------------------------ | ---------------------------- | ----------------------------- |
| **EventBridge Schedule** | Delete schedule              | Stop hourly invocations first |
| **Lambda Function**      | Delete function              |                               |
| **IAM Role**             | Delete role                  |                               |
| **IAM Policy**           | Delete policy                |                               |
| **SNS Subscription**     | Delete subscription          |                               |
| **SNS Topic**            | Delete topic                 |                               |
| **S3 Bucket**            | Empty bucket → Delete bucket | Must empty before deleting    |

 [\[277-aws-lambda \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277-aws-lambda.txt)

### Instructor's Advice

"Let it run for a few hours. Get the notification so you know that it worked." The exercise is **free** — no cost concerns. Only delete EventBridge schedule when you're tired of hourly emails. [\[277-aws-lambda \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277-aws-lambda.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## 🏗️ Lambda Core Identity

```
LAMBDA = Run code WITHOUT servers
  ├── Upload code as a FUNCTION
  ├── Define a TRIGGER (event, schedule, API, manual)
  ├── AWS handles: compute, scaling, availability, OS
  ├── Pay ONLY for execution time (idle = free)
  ├── Runtimes: Python, Node.js, Java, .NET, Amazon Linux
  └── Max timeout: 15 minutes

EC2 = permanent server (you manage everything, pay always)
Lambda = temporary execution (AWS manages everything, pay per use)
```

 [\[277-aws-lambda \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277-aws-lambda.txt)

***

## 📐 Exercise Architecture: 5-Component Pipeline

```
EventBridge Schedule (cron: 0 * * * ? *)
       │
       │ triggers every hour
       ▼
Lambda Function (Python 3.13)
  ├── IAM Role → SGCompliancePolicy
  │     ├── ec2: DescribeRegions, DescribeSecurityGroups (Resource: *)
  │     ├── sns: Publish (Resource: specific topic ARN)
  │     └── s3: PutObject, ListBucket (Resource: specific bucket ARN)
  │
  ├── SCANS: All regions → All SGs → All rules → CidrIp == 0.0.0.0/0?
  │
  ├── OUTPUT 1: SNS → Email notification (findings or "no findings")
  │
  └── OUTPUT 2: S3 → JSON report (security-audit-YYYY-MM-DD-HH-MM-SS.json)
```

 [\[277-aws-lambda \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277-aws-lambda.txt), [\[277.PyLambCodeSGComp \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277.PyLambCodeSGComp.txt), [\[277.SGCompPolicy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277.SGCompPolicy.txt)

***

## 🔄 Python Code Execution Flow

```
lambda_handler(event, context)
  │
  ├── Initialize: boto3 clients (ec2, sns, s3)
  │
  ├── regions = ec2.describe_regions()          ← Get ALL AWS regions
  │
  ├── FOR each region:
  │     ├── ec2_region = boto3.client('ec2', region_name=region)  ← Region-specific client
  │     ├── sgs = ec2_region.describe_security_groups()
  │     │
  │     └── FOR each sg:
  │           └── FOR each IpPermission:
  │                 └── FOR each IpRange:
  │                       └── IF CidrIp == '0.0.0.0/0':
  │                             └── findings.append({Region, SG_ID, Port, Protocol})
  │
  ├── sns.publish(TopicArn, Subject, Message=findings)    ← Email alert
  │
  ├── s3.put_object(Bucket, Key=timestamped.json, Body=findings)  ← Store report
  │
  └── return {statusCode: 200, body: findings}
```

 [\[277.PyLambCodeSGComp \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277.PyLambCodeSGComp.txt)

***

## 🛡️ IAM Permission Structure

```
SGCompliancePolicy:
  ├── EC2 (Resource: *)
  │     ├── DescribeRegions      ← List all regions
  │     ├── DescribeInstances    ← Instance context
  │     ├── DescribeSecurityGroups ← Read SG rules
  │     └── RevokeSecurityGroupIngress ← Future: auto-remediation
  │
  ├── SNS (Resource: specific topic ARN)
  │     └── Publish              ← Send notification
  │
  └── S3 (Resource: specific bucket + bucket/*)
        ├── PutObject            ← Upload report
        ├── GetBucketLocation    ← Check bucket region
        └── ListBucket           ← List contents

SGComplianceRole:
  ├── Trusted entity: Lambda service
  └── Attached policy: SGCompliancePolicy

EventBridge Role (auto-created):
  └── Permission: Invoke Lambda function
```

 [\[277.SGCompPolicy \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277.SGCompPolicy.txt)

***

## ⚡ Complete Build Sequence

```
 1. S3 → Create bucket (sg-compliance921, globally unique name)
 2. SNS → Create topic (SGCompliaceNotification, standard)
 3. SNS → Create subscription (email, confirm from inbox)
 4. IAM → Create policy (JSON: EC2/SNS/S3 permissions, update ARNs)
 5. IAM → Create role (Lambda use case, attach policy)
 6. Update Python code (sns_topic_arn, s3_bucket_name)
 7. Lambda → Create function (Python 3.13, existing role)
 8. Lambda → Configuration → Timeout: 5 minutes (default 3s too short!)
 9. Lambda → Code → Paste Python → Deploy
10. Lambda → Test → Create test event → Run → Verify findings ✅
11. Verify: S3 bucket has JSON file ✅, email received ✅
12. EventBridge → Create schedule (cron: 0 * * * ? *, target: Lambda)
13. Wait hours → verify hourly notifications + S3 reports
14. Cleanup: EventBridge schedule → Lambda → IAM role/policy → SNS → S3
```

 [\[277-aws-lambda \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277-aws-lambda.txt)

***

## ⚠️ Critical Configuration Points

```
TIMEOUT: Default 3 seconds → MUST increase to 5 minutes (multi-region scan ~1 min)
ARNs: Account ID + Topic name + Bucket name must match in BOTH policy AND code
SNS: Subscription MUST be confirmed from email (check spam)
S3: Bucket name globally unique, no uppercase
ROLE: Use case MUST be "Lambda" (trust relationship)
EVENTBRIDGE: Needs its OWN role (separate from Lambda's role)
COST: Exercise is FREE (Lambda free tier + S3/SNS minimal usage)
```

***

## 🔗 Two Separate IAM Roles

```
ROLE 1: SGComplianceRole (FOR Lambda)
  └── "What can the Lambda function DO?"
  └── Access: EC2 (read SGs), SNS (publish), S3 (write reports)

ROLE 2: EventBridge Role (FOR EventBridge, auto-created)
  └── "Can EventBridge INVOKE the Lambda function?"
  └── Access: Lambda (invoke function)

RULE: The trigger's role ≠ the function's role
      Trigger role = permission to START the function
      Function role = permission to ACCESS services during execution
```

***

## 🧩 Reusable Engineering Patterns

```
PATTERN 1: EVENT-DRIVEN AUTOMATION (Trigger → Function → Output)
  Event/Schedule → Serverless code → Results/Notifications
  → Same as: CI/CD pipeline triggers, webhook handlers,
    Kubernetes controllers, message queue consumers,
    any reactive automation system

PATTERN 2: MULTI-REGION ITERATION
  Get all regions → loop → create region-specific client → query
  → Required for ANY global AWS compliance/audit/inventory task
  → Single client = single region; multi-region = loop + new client per region

PATTERN 3: LEAST-PRIVILEGE IAM (Scoped Permissions)
  Broad where necessary (EC2: * for all regions)
  Narrow where possible (SNS: specific topic, S3: specific bucket)
  → Same as: K8s RBAC, database user permissions, API scopes

PATTERN 4: DUAL OUTPUT CHANNEL (Notification + Persistent Record)
  SNS = real-time alert (email, ephemeral)
  S3 = persistent audit trail (JSON file, durable)
  → Same as: Alerting + logging, PagerDuty + Splunk,
    Slack notification + database record

PATTERN 5: AI-GENERATED CODE + HUMAN VALIDATION
  "I asked ChatGPT to generate this code... I understand this very well"
  → Modern workflow: AI generates, engineer validates + deploys
  → Same as: Copilot-assisted coding from earlier lecture
```

 [\[277-aws-lambda \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/277-aws-lambda.txt)

***

## 🧭 Course Flow Context

```
PREVIOUS  → EC2, EBS, EFS, RDS (infrastructure services — you manage servers)
THIS      → Lambda (SERVERLESS — no servers to manage)
            + Integration: S3 + SNS + IAM + EventBridge + EC2 API
            = First fully automated, multi-service, event-driven pipeline

SERVICES USED IN THIS LECTURE:
  Lambda (compute) + S3 (storage) + SNS (notification) + 
  IAM (security) + EventBridge (scheduling) + EC2 API (data source)
  = 6 services wired into one automated compliance system

EVOLUTION:
  EC2 (manual server)
  → User Data (automated server setup)
  → Lambda (no server at all — just code)
```

***

Your AWS Lambda + Security Group Compliance automation deep learning material is fully reconstructed — covering the serverless compute model, the 5-component architecture, the Python scanning logic, the IAM permission design, and the EventBridge scheduling system. Want me to generate **AnkiDroid flashcards (.csv)** from this lecture or across the full lecture series? 🃏
