# 📘 Jenkins Security — Authentication & Authorization — Deep Learning Material

*Reconstructed from video lecture: [184.-Authentication-&-Authorization.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt?EntityRepresentationId=580c8ff9-7caa-4bf3-b384-0002cfe91243)* [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

***

## 🧠 SECTION 1: THEORY (Deep Learning Mode)

### The Core Problem: Why Jenkins Needs Security

Up to this point in the course, everything in Jenkins has been done using a single **admin user** with full privileges. This works fine for learning, but in a real organization, Jenkins is a shared tool. Once you create a pipeline, you may hand it over to **developers**, **testers**, **ops teams**, or **non-ops teams**. The fundamental question becomes: **how much privilege do you want each of them to have?** [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

If Jenkins is used at an organization level — with multiple projects and CI/CD pipelines running from the same Jenkins instance — you absolutely do not want a non-admin user to have full admin access. A developer from Project A should not be able to access, modify, or even see the content of Project B. A tester should not be able to reconfigure pipeline settings. An ops team member might only need the ability to trigger builds, not install plugins or manage credentials. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

Jenkins addresses this through two distinct security mechanisms: **authentication** (who can log in) and **authorization** (what they can do after logging in). The lecture makes the distinction crisp and memorable: **authentication is login, authorization is privilege.** [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

The lecture's overarching advice is clear: **don't share login details, don't give full access to other people.** Instead, create individual accounts, fine-tune what each user or group of users can do, and apply the principle of least privilege throughout. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

***

### Authentication: Who Can Log In

Authentication controls **who is allowed to access Jenkins at all**. Jenkins offers several authentication mechanisms, each suited to different environments. The lecture walks through all of them from the **Configure Global Security** page under **Manage Jenkins → Security**: [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

***

#### Option 1: Delegate to Servlet Container

This option delegates authentication to the application server (servlet container) running Jenkins, such as Tomcat or Jetty. The lecture explicitly dismisses this option — "we don't want to do that." It is rarely used in modern Jenkins setups because it ties authentication to the web server layer rather than managing it within Jenkins itself. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

***

#### Option 2: Jenkins' Own User Database

This is the option the lecture uses and recommends for smaller or project-level setups. With this option, Jenkins maintains its own internal database of users. Users can **sign up themselves** — when someone accesses the Jenkins URL, they see a **Create an Account** button, fill in a username, name, email, and password, and their credentials are stored in Jenkins' own database. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

The key setting here is the **"Allow users to sign up"** checkbox. When enabled, anyone who can reach the Jenkins URL can create an account. This is convenient but must be paired with proper authorization — otherwise, a self-registered user could potentially have excessive access. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

Additionally, admins can create users directly from the **Manage Users** page in Jenkins (introduced later in the lecture). This means users don't *have* to self-register — an admin can pre-create accounts with usernames, passwords, and email addresses. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

***

#### Option 3: LDAP

LDAP (Lightweight Directory Access Protocol) integration is the recommended approach for **organization-level Jenkins deployments**. In most companies, employees already exist in an **Active Directory** or similar centralized authentication system. Rather than having every employee create a separate Jenkins account, you integrate Jenkins with the LDAP server, and all users in the directory can log in to Jenkins with their existing corporate credentials. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

The lecture notes that to set this up, you need server details (LDAP server address, search base, etc.) from your **IT team**. You fill in these details in the LDAP configuration section and save. After that, any user in the directory can authenticate against Jenkins. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

The lecture does not demonstrate LDAP configuration in practice — it only explains the concept and when to use it. The focus remains on Jenkins' own user database.

***

#### Option 4: Unix User/Group Database

This option uses the operating system's user and group database for authentication. The lecture **explicitly does not recommend this** — "that should be separate." Tying Jenkins authentication to the OS user database creates a tight coupling between the Jenkins application and the underlying server, which is problematic for portability, security, and separation of concerns. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

***

### Authorization: What Logged-In Users Can Do

Once a user is authenticated (logged in), **authorization** determines what they are allowed to do. Jenkins offers multiple authorization strategies, ranging from completely open to extremely granular. The lecture walks through all of them, clearly identifying which are usable and which are dangerous: [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

***

#### "Anyone Can Do Anything"

This is literally **no security**. Any user — or even anonymous users — can do anything: configure Jenkins, delete pipelines, access credentials, install plugins. The lecture calls this out as "really no security." It exists as an option, but should never be used in any real environment. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

***

#### "Legacy Mode"

This enables **anonymous access**, meaning users don't even need to log in to interact with Jenkins. This is a holdover from older Jenkins versions and is equally dangerous. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

***

#### "Logged-in Users Can Do Anything"

At first glance, this seems reasonable — at least users have to log in. But the lecture explains why it's a trap: if you combine this with **"Allow users to sign up"** in the authentication section, then *anybody* can sign up and then do *anything*. This provides zero meaningful security. The lecture is emphatic: "not a good option, not at all." [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

***

#### Matrix-Based Security (Jenkins-Level Fine-Tuning)

This is the first **genuinely useful** authorization strategy. Matrix-based security lets you define **per-user permissions** across the entire Jenkins instance. When you select this option, you get a matrix (grid) where rows are users and columns are permission categories. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

The permission categories include:

*   **Overall** — General Jenkins permissions (e.g., Read, Administer)
*   **Credentials** — Access to stored credentials
*   **Agent** — Permissions related to Jenkins build agents
*   **Job** — Permissions on jobs/pipelines (Build, Cancel, Configure, Create, Delete, Read, Workspace)
*   **View** — Permissions on Jenkins views/dashboards

For each user, you check or uncheck individual permissions. For example, you can give a user the ability to **Build** and **Cancel** jobs, but not **Configure** or **Delete** them. You can grant read access to credentials but not create/update/delete access. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

The **limitation** of matrix-based security is that it applies to the **entire Jenkins instance**. If you give a user Build permission on jobs, that user can build **all** jobs in Jenkins. The lecture highlights this directly: "the user has access to all the jobs and that is the problem with this." If your Jenkins instance serves only one project and all users belong to that project, matrix-based security is sufficient. But if multiple projects share the same Jenkins, users from one project will see and potentially interact with jobs from other projects. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

> 🔍 **Deep Dive (Optional)**
>
> The matrix-based security screen validates usernames in real-time. If you type a username that exists in the Jenkins database, it shows a confirmation (the user is recognized). If you type a username that does **not** exist, you see a cross mark. The lecture demonstrates this: typing an existing user shows it's valid, typing "DevOps" (a non-existent user) shows a cross. You *can* add a non-existent user and pre-assign permissions before they sign up — but the lecture notes this "goes against the ethics." The proper flow is: have the user sign up first, then assign permissions. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

***

#### Project-Based Matrix Authorization Strategy (Job-Level Fine-Tuning)

This is the **tightest security** option available in core Jenkins. It extends the matrix-based approach by allowing you to define permissions **per job**, not just per Jenkins instance. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

When you select "Project-based Matrix Authorization Strategy" in global security, you still define global permissions (like minimum read access). But then, on **each individual job**, you get a new option: **"Enable project-based security."** Within that job's configuration, you can add specific users and define what they can do *on that job only*. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

This means a user can have Build access on Job A but no access at all to Job B. A developer from Project A sees only Project A's jobs; a developer from Project B sees only Project B's jobs. The lecture demonstrates this: after enabling project-based security, the test user can see only the specific job they were granted access to — nothing else. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

The trade-off is that this approach requires **more configuration effort**. You must go to each job individually and set up its security. The lecture acknowledges this: "sure it may take more time but it is the tightest security that you can do." [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

> ⚠️ **Expert Note**
>
> In project-based authorization, the global-level permissions serve as a **baseline**. At minimum, a user typically needs **Overall → Read** at the global level to even access the Jenkins UI. Without it, the user sees a "permission missing" error. The job-level permissions then layer on top of this baseline. If a user has no job-level permissions for a particular job, that job is invisible to them — they don't even know it exists. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

***

#### Role-Based Strategy (Plugin: Role-Based Authorization Strategy)

Managing per-user permissions becomes tedious when you have many users. The **Role-Based Authorization Strategy** plugin solves this by introducing the concept of **roles**. A role is a named collection of permissions (e.g., "DevOps role" with Build, Cancel, Configure, Create permissions on jobs, read on credentials, full on agents, etc.). Instead of assigning permissions to each user individually, you create roles once and then assign users to roles. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

This plugin must be installed from **Manage Plugins** — it is not built into Jenkins. The plugin name is **"Role-Based Authorization Strategy"** and can be found by searching for "role" in the available plugins. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

Once installed, a new authorization option appears in Configure Global Security: **"Role-Based Strategy."** Selecting it and saving reveals a new management section under **Manage Jenkins → Security**: **"Manage and Assign Roles."** This section has two sub-pages: [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

**Manage Roles** — where you create roles and define their permissions. You enter a role name (e.g., "DevOps"), click Add, and then check/uncheck permissions across the same categories (Overall, Credentials, Agent, Job, View, etc.). [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

**Assign Roles** — where you map users to roles. You enter a username, and then check which role(s) the user belongs to. If you have many roles, they all appear as columns, and you simply check the appropriate one(s) for each user. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

The lecture emphasizes the management benefit: "it's pretty easy to manage from this dashboard." Whenever a new user signs up, you simply go to Assign Roles, find the user, and add them to the appropriate role. You don't need to set individual permissions each time. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

***

### Managing Users Directly in Jenkins

The lecture introduces one more capability near the end: the **Manage Users** page (available under Manage Jenkins). From here, an admin can **create users directly** without requiring the user to self-register. You click "Create User," provide a username, password, full name, and email address, and Jenkins creates the account in its own database. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

After creating the user, authorization must still be configured separately — user creation and permission assignment are independent actions. You go to Configure Global Security (or Manage and Assign Roles, depending on your authorization strategy) to grant the new user appropriate access. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

The Manage Users page also allows you to **reset user passwords** and **upload public keys** for key-based logins — an alternative authentication method where users log in with SSH keys rather than passwords. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

***

## ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

### What We Are Building

In this practical section, we are configuring **authentication and authorization** on a Jenkins instance. We will set up user sign-up, create a test user, and then progressively apply three authorization strategies — **matrix-based security**, **project-based matrix authorization**, and **role-based strategy** — testing each one to observe how permissions affect what the user can see and do. We will also create a user directly from the admin interface. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

By the end, you will understand how to control who accesses your Jenkins instance, what they can do at the Jenkins level, what they can do at the individual job level, and how to manage this at scale using roles.

The lecture uses **two browsers simultaneously** to test: **Edge** (logged in as the admin user) for making configuration changes, and **Firefox** (logged in as a test user) for verifying the effect of those changes. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

***

### Step 1: Configure Authentication — Enable Jenkins' Own User Database with Sign-Up

Navigate to **Manage Jenkins → Security → Configure Global Security**. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

Under the **Authentication** section (labeled "Security Realm"), you see several options. Select **"Jenkins' own user database"** and enable the checkbox **"Allow users to sign up."** [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

This configures Jenkins to maintain its own internal user store. The "Allow users to sign up" option means anyone who accesses the Jenkins URL will see a **"Create an account"** button on the login page. They can register themselves with a username, name, email, and password. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

**Why this matters:** In a real team, this is the simplest way to onboard users without requiring external infrastructure like LDAP. Users self-register, and then an admin grants them appropriate permissions.

**Connection to overall system:** Authentication is the first gate. Without it, authorization is meaningless — you need to know *who* the user is before you can decide *what* they're allowed to do.

***

### Step 2: Set Up Matrix-Based Security (First Authorization Strategy)

Still in **Configure Global Security**, scroll down to the **Authorization** section. Select **"Matrix-based security."** [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

A permission matrix appears. Click **"Add user"** and type `admin` (or whatever your admin username is). Check the **Administrator** checkbox to give this user full access. This is critical — if you save without giving your admin user full permissions, you can lock yourself out of Jenkins. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

Click **Save**. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

> ⚠️ **Expert Note**
>
> Always ensure your admin user has full Administrator privileges before saving matrix-based security settings. If you accidentally save without granting admin permissions, you will be locked out. The recovery involves manually editing Jenkins' `config.xml` file on the server's filesystem and restarting Jenkins — a stressful experience you want to avoid. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

***

### Step 3: Test User Sign-Up (Firefox Browser)

Open **Firefox** (or any second browser where you are not logged in). Navigate to the Jenkins URL. You should see a login page with a **"Create an account"** button. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

Click **"Create an account"** and fill in:

*   **Username** — e.g., `imran`
*   **Full name** — your name
*   **Email** — any email address
*   **Password** — set a password [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

Click **Create account**. Jenkins confirms: "Success. The account is created." The user details are stored in Jenkins' internal database. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

Now click **"Go back to the top page"** and try to access Jenkins. You will see an error: **"Overall or read permission is missing."** This is expected — the new user exists (authentication passed) but has **zero permissions** (authorization blocks everything). [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

**What this demonstrates:** Authentication and authorization are truly independent. A user can successfully log in but still be completely blocked from doing anything if no permissions are assigned.

***

### Step 4: Grant Permissions in the Matrix

Switch back to **Edge** (admin browser). Navigate to **Manage Jenkins → Configure Global Security**. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

In the matrix-based security section, click **"Add user"** and type the test user's username (e.g., `imran`). If the user exists in the database, Jenkins shows a confirmation indicator. If you type a username that doesn't exist, you'll see a **cross mark** — the user is not recognized. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

**First test — Overall Read only:** Check only the **Overall → Read** permission for this user. Save. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

Switch to Firefox, refresh. The user can now access Jenkins but sees essentially nothing useful. The lecture describes this as "pointless" — read access alone shows the Jenkins dashboard but with no meaningful content or actionable capabilities. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

**Second test — Add Job permissions:** Back in Edge, go to Configure Global Security. For the test user, add Job-level permissions: **Build**, **Cancel**, **Configure**, **Create** — but leave out **Delete**. Also add **Read** and **Workspace** permissions on jobs. Save. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

Switch to Firefox, refresh. Now the user can see **all jobs** in Jenkins and can build, cancel, configure, and create jobs — but cannot delete them. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

**The problem revealed:** The user has access to **all jobs** across the entire Jenkins instance. If there are jobs from other projects, this user can see and interact with those too. The lecture explicitly identifies this: "the user has access to all the jobs and that is the problem with this." Matrix-based security controls *what* a user can do, but not *which jobs* they can do it on. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

***

### Step 5: Switch to Project-Based Matrix Authorization Strategy

To solve the "access to all jobs" problem, switch to a more granular strategy. In **Configure Global Security → Authorization**, select **"Project-based Matrix Authorization Strategy."** [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

Add the test user and give them only **Overall → Read** permission. This is the **minimum** required for the user to access the Jenkins UI at all. Save. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

Switch to Firefox, refresh. The user can log in and see the Jenkins dashboard, but sees **no jobs** — because no job-level permissions have been granted yet. The Overall Read permission at the global level is just enough to enter Jenkins; everything else must be granted per-job. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

***

### Step 6: Configure Per-Job Security

Back in Edge (admin), navigate to a specific job — for example, the **"build test"** job. Go to **Configure**. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

You'll see a new option: **"Enable project-based security."** Check this box. A permission matrix appears, specific to *this job only*. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

Add the test user (e.g., `imran`). Assign permissions:

*   **Credentials** — select all (or as needed)
*   **Job permissions** — grant Build, Cancel, Read, Workspace — but remove **Delete** and **Configure** [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

This means the user can build and view this specific job, but cannot delete it or change its configuration. Save. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

Switch to Firefox, refresh. Now the user sees **only that one job** — nothing else. They can build it, view its output, but cannot reconfigure or delete it. Other jobs are completely invisible. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

**What this achieves:** True project-level isolation. A developer from Project A sees only Project A's jobs. A developer from Project B sees only Project B's jobs. No cross-project visibility or access. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

The lecture acknowledges the trade-off: "sure it may take more time but it is the tightest security that you can do." You must configure security on each job individually. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

***

### Step 7: Install and Configure Role-Based Authorization Strategy

To manage permissions at scale (many users, many jobs), install the **Role-Based Authorization Strategy** plugin. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

Navigate to **Manage Jenkins → Manage Plugins → Available Plugins**. Search for **"role"**. Find **"Role-Based Authorization Strategy"** and install it. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

After installation, go to **Manage Jenkins → Configure Global Security → Authorization**. You now see a new option: **"Role-Based Strategy."** Select it and **Save**. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

***

### Step 8: Create a Role

After saving with Role-Based Strategy selected, navigate to **Manage Jenkins → Security**. You'll find a new option: **"Manage and Assign Roles."** Click it. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

Go to **"Manage Roles."** In the role name field, type a role name — e.g., `DevOps` — and click **Add**. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

A permission matrix appears for this role. Assign permissions based on what this role should be able to do. The lecture demonstrates: [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

*   **Job** — Build, Cancel, Configure, Create, Discover, Workspace (but **not** Delete)
*   **Run** — permissions as needed
*   **View** — as needed
*   **Agent** — full permission
*   **Credentials** — view only (read access, not create/update/delete)
*   **Overall** — Read access

Click **Save**. The role is now created with its defined set of permissions. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

***

### Step 9: Assign a User to the Role

Navigate to **Manage and Assign Roles → Assign Roles**. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

Enter the test user's username (e.g., `imran`). You'll see all available roles displayed as columns. Check the **DevOps** role for this user. Save. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

Switch to Firefox, refresh. The user now has all the permissions defined in the DevOps role — they can build, cancel, configure, and create jobs, view credentials, and work with agents, but cannot delete jobs. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

**The management benefit:** When a new user joins the team, you don't need to individually configure dozens of permissions. You simply go to Assign Roles, enter the username, and check the appropriate role. The role carries all the pre-defined permissions with it. If the role's permissions need to change (e.g., adding delete access for DevOps), you change it once in Manage Roles and it applies to all users in that role. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

***

### Step 10: Create a User Directly from Admin Interface

Navigate to **Manage Jenkins → Manage Users → Create User**. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

Fill in the user details:

*   **Username** — e.g., `Sheldon`
*   **Password** — set a password
*   **Full name** — e.g., `Sheldon` (the lecture references "from Big Bang Theory")
*   **E-mail** — e.g., `sheldon@don.com` [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

Click **Create User**. The account is created in Jenkins' internal database. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

**Important:** Creating the user here does **not** assign any permissions. You must separately go to your authorization configuration (Configure Global Security, or Manage and Assign Roles) and grant this user appropriate access. User creation and authorization are independent operations. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

The Manage Users page also provides options to **reset passwords** and **upload public keys** for key-based authentication — an alternative where users log in using SSH keys instead of passwords. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

***

### Summary of Authorization Strategies — Quick Reference

| Strategy                               | Scope                             | Best For                                    | Trade-off                    |
| -------------------------------------- | --------------------------------- | ------------------------------------------- | ---------------------------- |
| **Anyone can do anything**             | No security                       | Never use                                   | Dangerous                    |
| **Legacy mode**                        | Anonymous access                  | Never use                                   | Dangerous                    |
| **Logged-in users can do anything**    | All logged-in users = full access | Never use (especially with sign-up enabled) | Dangerous                    |
| **Matrix-based security**              | Per-user, Jenkins-wide            | Single-project Jenkins instances            | Users see all jobs           |
| **Project-based matrix authorization** | Per-user, per-job                 | Multi-project Jenkins instances             | More configuration effort    |
| **Role-based strategy** (plugin)       | Per-role, assignable to users     | Large teams, many users                     | Requires plugin installation |

 [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)

***

### Connection to the Overall System

Jenkins security is not a one-time setup — it is an ongoing concern that affects every pipeline, every job, and every user interaction. Authentication ensures only authorized people can access Jenkins. Authorization ensures each person can only do what their role requires. The progression from matrix-based → project-based → role-based represents increasing sophistication for increasingly complex organizational needs. In a production environment, you will almost always use either **project-based matrix authorization** (for tight per-job control) or **role-based strategy** (for scalable user management), often combined with **LDAP authentication** for enterprise-grade identity management. [\[184.-Authe...horization \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/184.-Authentication-%26-Authorization.txt)
