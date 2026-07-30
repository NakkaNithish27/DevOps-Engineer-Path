# Section 01 – introduction

The instructor opens the course by stating goals and the practical projects that will be built during the path. (01-Introduction.md)  
The instructor scopes the engineering focus to CI/CD, automation, infrastructure, containers, and cloud rather than theory. (02-What-is-DevOps.md)  
The instructor outlines the continuous integration steps and what a working CI pipeline must produce. (04-Continuous-Integration.md)  
The instructor specifies continuous delivery expectations and how deployments will be automated and validated. (05-Continuous-Delivery.md)  
The section closes by positioning the repository and projects used across the course as the running engineering examples. (Section Summary)

# Section 02 – prerequisites info and setup

The instructor lists required local tools and accounts to reproduce course exercises and captures exact package names and versions. (01-prerequisites.md)  
The instructor demonstrates Windows tooling automation using Chocolatey to install development dependencies. (02-chocolatey.md)  
The instructor provides platform-specific software installation steps and verifies runtimes for later labs. (03-software-installation.md)  
The instructor collects cloud and third‑party signups and configures initial account-level settings used throughout the course. (06-signups.md)  
The instructor provides a consolidated checklist for environment validation so later automation assumes a reproducible base. (Section Summary)

# Section 03 – vm setup

The instructor introduces virtualization concepts and why VMs are used for reproducible labs. (16-virtualization-overview.md)  
The instructor contrasts host virtualization models and selects the VM tooling used in hands-on examples. (17-what-is-virtualization.md)  
The instructor provides step-by-step VM provisioning and manual VM configuration commands to prepare lab hosts. (18-introduction.md, 19-vm-manual.md)  
The instructor documents images, networking and storage choices for the lab VMs to ensure consistent environments. (19-vm-manual.md)  
The instructor finishes by describing how the VM setup supports later container, orchestration, and CI experiments. (Section Summary)

# Section 04 – linux

The instructor establishes the Linux baseline by installing and validating a supported distribution for labs. (23-linux-intro.md)  
The instructor configures filesystem layout and demonstrates the exact commands used to create, mount, and manage filesystems. (24-commands-filesystem.md)  
The instructor applies common admin commands and user workflows that will be reused in automation tasks. (25-basic-commands.md)  
The instructor configures and uses the vim editor for in-place file editing of automation and configuration files. (26-vim.md)  
The instructor enumerates file types, ACLs, and text-processing filters used during configuration tasks. (27-file-types.md, 28-filters.md)  
The instructor automates redirection, user/group, permission, sudo, and package management tasks to prepare systems for services. (29-redirection.md, 30-users-groups.md, 31-permissions.md, 32-sudo.md, 33-package-management.md)  
The instructor validates service and process management workflows used later by CI and orchestration examples. (34-services.md, 35-processes.md)  
The section ends with archiving and cleanup procedures for lab reproducibility. (36-archiving.md, Section Summary)

# Section 05 – git

The instructor introduces Git and configures a working repository used across course projects. (40-introduction.md)  
The instructor documents versioning strategies and shows how commits map to CI runs used later. (41-versioning.md)  
The instructor demonstrates branching workflows and the branch operations that will trigger pipelines. (42-branches.md)  
The instructor demonstrates rollback techniques and recovery steps for deployment failures. (43-rollback.md)  
The instructor sets up SSH-based Git access and key management for automation agents. (44-git-ssh.md)  
The instructor enforces SemVer tagging and explains how tags are used as build artifacts in pipelines. (45-tags-semver.md)  
The instructor shows how AI tools (Copilot) integrate into developer workflows and how that affects repository edits. (46-github-copilot.md)  
The instructor consolidates Git policies and the repository layout that downstream automation assumes. (Section Summary)

# Section 06 – vagrant and linux servers

The instructor uses Vagrant to define VM resource profiles (IP, RAM, CPU) for lab hosts and captures the Vagrantfile parameters. (49-Vagrant-IP-RAM-CPU.md)  
The instructor configures host directories to sync source code into VMs for iterative development and pipeline testing. (50-Vagrant-Sync-Dirs.md)  
The instructor creates provisioning steps that install web stacks and dependencies inside VMs for deterministic builds. (51-Provisioning.md)  
The instructor sets up a reference website and then a WordPress instance on provisioned VMs to exercise deployment and automation. (52-Website-Setup.md, 53-WordPress-Setup.md)  
The instructor automates website and WordPress provisioning with repeatable scripts and documents the commands used. (54-Automate-Website.md, 55-Automate-WordPress.md)  
The instructor demonstrates AI-assisted automation examples using Copilot to accelerate repetitive tasks in the Vagrant environment. (56-Copilot-AI.md)  
The instructor expands to multi-VM Vagrant configurations to model small distributed systems used later for orchestration and testing. (57-Multi-VM-Vagrant.md)  
The section concludes with validated, provisioned Vagrant VM templates used as lab infrastructure. (Section Summary)

# Section 07 – vars json yaml

The instructor presents variable handling across languages and tools and demonstrates practical variable usage in Python data structures. (60-Variables-Python-DS.md)  
The instructor documents JSON and YAML file formats, exact serializer/deserializer commands, and common pitfalls when used as configuration for automation. (61-JSON-YAML.md)  
The instructor provides reproducible examples of storing and consuming variables in deployment manifests and automation scripts. (Section Summary)

# Section 08 – vprofile setup

The instructor introduces the "vprofile" sample project and its repository layout used throughout the course. (62-Project-Welcome.md, 63-Intro.md)  
The instructor provisions a VM environment required to run the vprofile project and captures the setup commands. (64-VM-Setup.md)  
The instructor installs and configures MySQL for the project and documents schema and credential initialization steps. (65-MySQL-Setup.md, 145-DB-Initialization.md)  
The instructor sets up Memcached and RabbitMQ services required by the application and records service configuration files. (66-Memcache-Setup.md, 67-RabbitMQ-Setup.md)  
The instructor deploys application components onto the prepared VMs and validates service connectivity and health checks. (68-App-Setup.md, 69-Nginx-Setup.md, 70-Validate.md)  
The instructor automates the vprofile environment with scripted code and captures the repository automation entry points used later in CI. (71-Automated-Intro.md, 72-Automated-Code.md)  
The section leaves a reproducible application stack for use in containerization, CI, and GitOps exercises later in the course. (Section Summary)

# Section 09 – networking

The instructor explains ISO and layered network concepts only as they apply to designing lab networks for the projects. (74-ISO.md)  
The instructor documents IP addressing, subnetting, and the exact address plans used in lab topologies. (75-Networks-IP.md)  
The instructor enumerates protocols and ports required by services used throughout the course and configures firewall rules accordingly. (76-Protocols-Ports.md)  
The instructor records and demonstrates networking commands (ping, traceroute, netstat, iptables) used during troubleshooting across labs. (77-Networking-Commands.md)  
The instructor concludes with a validated network configuration that supports VM, container, and cloud lab scenarios. (Section Summary)

# Section 10 – containers

The instructor describes container fundamentals and prepares the environment for Docker-based work. (78-Containers.md)  
The instructor installs Docker, demonstrates core Docker commands, and validates the engine and runtime behavior. (79-Docker.md, 80-Docker-Hands-On.md)  
The instructor adapts the vprofile project to run inside containers and demonstrates containerized service interactions. (81-VProfile-Containers.md, 82-Microservices.md)  
The instructor breaks the application into microservices, builds images for each component, and demonstrates running them locally. (82-Microservices.md, 83-Microservice*.md)  
The instructor finalizes the container examples used later by CI and orchestration sections. (Section Summary)

# Section 11 – bash scripting

The instructor prepares a shell scripting environment on lab VMs and demonstrates first-party script editing and execution. (85-Intro.md, 86-VM-Setup.md)  
The instructor writes and runs simple shell scripts and then progressively adds CLI argument parsing and system variable usage. (87-First-Script.md, 91-CLI-Arguments.md, 92-System-Variables.md)  
The instructor adds input handling, variables export, quoting and substitution techniques to make scripts robust for automation. (90-Variables.md, 93-Quotes.md, 94-Command-Substitution.md, 95-Export-Variables.md, 96-User-Input.md)  
The instructor demonstrates remote execution, SSH key exchange, and running scripts across multiple hosts. (102-Remote-Execution.md, 103-SSH-Key-Exchange.md)  
The instructor automates typical admin workflows using loops, conditionals, and control flow and shows complete examples used later in provisioning. (100-For-Loops.md, 101-While-Loops.md, 104-Finale-1.md, 105-Finale-2.md)  
The section closes with scripts packaged as repeatable automation artifacts for provisioning and CI jobs. (Section Summary)

# Section 12 – ai scripting

The instructor demonstrates using AI tools to assist command and code generation for ops tasks. (106-Autocomplete.md, 108-AI-Suggestions.md)  
The instructor captures AI best practices for prompt engineering and validation of generated scripts to avoid unsafe commands. (107-Best-Practices.md)  
The instructor shows AI-assisted code generation examples and integrates them into the automation workflow used in labs. (109-AI-Code-Generation.md)  
The section ends with validated AI-produced artifacts and guidance on verifying them in CI pipelines. (Section Summary)

# Section 13 – aws part 1

The instructor introduces cloud concepts and maps them to the AWS services used in the course projects. (110-Cloud-Computing.md, 111-Intro.md)  
The instructor walks through EC2 instance creation, the exact console/CLI steps, and AMI selection used for lab instances. (112-EC2-Intro.md, 113-EC2-Quick-Start.md, 114-EC2-Part1.md, 115-EC2-Part2.md)  
The instructor configures the AWS CLI, demonstrates CloudShell and SSM for remote management, and records commands for automation. (116-AWS-CLI.md, 117-SSM-CloudShell.md)  
The instructor provisions EBS volumes, snapshots, and documents mounting and backup procedures used by the application. (118-EBS.md, 119-EBS-Snapshots.md)  
The instructor introduces ELB/ALB and demonstrates hands-on load balancer creation and configuration used to front app instances. (120-ELB-Intro.md, 121-ELB-HandsOn-1.md, 122-ELB-HandsOn-2.md)  
The instructor integrates CloudWatch metrics and alarms and shows the exact metrics used to drive scaling and alerts. (123-CloudWatch-Intro.md, 124-CloudWatch-HandsOn.md)  
The instructor provisions EFS for shared storage and sets up autoscaling patterns used later in production-like architectures. (125-EFS.md, 126-AutoScaling-Intro.md, 127-AutoScaling-HandsOn.md)  
The instructor demonstrates S3 usage for static assets and artifacts required by CI/CD flows. (128-S3-Intro.md)  
The section leaves a reproducible AWS baseline for subsequent re-architecting and CI/CD projects. (Section Summary)

# Section 14 – aws cloud

The instructor creates AWS security groups and keypairs and records the exact rule sets used for service access. (133-Security-Groups-Keypairs.md)  
The instructor launches EC2 instances and captures AMI, instance types, user-data, and connectivity validation steps. (134-EC2-Instances.md)  
The instructor provisions Route53 DNS records to map services and validates DNS propagation for load balanced endpoints. (135-Route53-DNS.md)  
The instructor demonstrates build/deploy artifact storage and retrieval patterns for continuous delivery. (136-Build-Deploy-Artifacts.md)  
The instructor configures ELB and DNS integration and then uses Auto Scaling Groups to achieve scale-out behavior under load. (137-LoadBalancer-DNS.md, 138-AutoScaling-Group.md)  
The instructor validates the full deployed architecture end-to-end and records the verification checks used in automation. (139-Validate*.md)  
This section establishes the cloud infrastructure that the later AWS CI/CD project and GitOps pipeline will extend. (Section Summary)

# Section 15 – re-architecting

The instructor introduces application re-architecture goals and migrates vprofile services from VM to managed cloud services. (140-Intro.md)  
The instructor updates security groups and keypairs for the re-architected topology to maintain least-privilege access. (141-Security-Groups-Keypairs.md)  
The instructor migrates the database to RDS and documents instance sizing, parameter groups, and maintenance practices. (142-RDS.md)  
The instructor provisions ElastiCache for caching and configures Amazon MQ or managed message brokers to replace self-hosted RabbitMQ. (143-ElasticCache.md, 144-Amazon-MQ.md)  
The instructor initializes the database with migration scripts and integrates initialization into the deployment pipeline. (145-DB-Initialization.md)  
The instructor deploys the application to Elastic Beanstalk as a managed runtime and records build, environment, and deployment steps. (146-Beanstalk.md)  
The instructor updates security groups and load balancer settings to the re-architected design and demonstrates artifact deployment flows. (147-SG-ELB-Update.md, 148-Build-Deploy-Artifact.md)  
The instructor documents CDN usage (CloudFront) for static content and finalizes the cloud-optimized architecture. (149_CloudFront_Complete_Explanation.md)  
This section transitions the sample app from VM-centric hosting to managed cloud services used in the CI/CD projects. (Section Summary)

# Section 16 – build tools

The instructor introduces build tooling and installs Maven and Node.js toolchains used for building sample services. (151_Introduction.md, 153. Maven, NodeJS & AI.md)  
The instructor walks through a Maven hands-on build lifecycle and documents POM structure, packaging, and artifact outputs used by pipelines. (152_Maven_Hands_on.md)  
The instructor records the commands used to produce build artifacts and how they are integrated into Nexus or other artifact repositories. (152_Maven_Hands_on.md, 153. Maven, NodeJS & AI.md)  
The section delivers concrete build steps that CI pipelines run to produce deployable artifacts. (Section Summary)

# Section 17 – continuous integration and delivery with jenkins

The instructor installs Jenkins and validates the server and plugin prerequisites for CI in the lab environment. (154.-Introduction.md, 155.-Installation.md)  
The instructor contrasts freestyle jobs and pipeline-as-code and decides to use Pipeline-as-Code for reproducible automation. (156.-Freestyle-Vs-Pipeline-As-A-Code.md)  
The instructor creates and runs the first jobs and captures the job definitions and console outputs used for troubleshooting. (158.-First-Job.md, 159.-First-Build-Job.md)  
The instructor configures build agents, documents agent registration, and shows how agents execute pipeline stages. (160.-Agents.md)  
The instructor installs and manages plugins, demonstrates common disk-space issues, and provides remediation steps for long-running CI servers. (161-Plugins-Versioning- &-more.md, 162-Disk-Space-Issue.md)  
The instructor outlines the CI pipeline flow, enumerates step-by-step stages, and shows how code analysis, unit tests, and artifact publication fit together. (163-Flow-of-Continuous-Integration-Pipeline.md, 164-Steps-for-Continuous-Integration-Pipeline.md)  
The instructor integrates SonarQube and Nexus, runs code analysis, demonstrates quality gates, and stores artifacts for consumption by CD. (165-Jenkins-Nexus-&-Sonarqube-Setup.md, 168-Code-Analysis.md, 170-Quality-Gates.md, 171-Software-Repositories-Intro-(Nexus).md)  
The instructor demonstrates Docker CI patterns, builds and pushes images from Jenkins, and shows a working Docker CI/CD demo. (174-CI-for-Docker---Intro.md, 176-Docker-PAAC-Demo.md, 178-Docker-CICD-Code.md, 180-Docker-CICD-Demonstration.md)  
The section concludes with a Jenkins-driven pipeline that builds, analyzes, and publishes artifacts and images for delivery. (Section Summary)

# Section 18 – github actions

The instructor introduces GitHub Actions and sets up the initial workflow scaffolding in the repository. (185-introduction.md)  
The instructor walks through a quickstart and creates the first action that runs on push, capturing the exact workflow YAML used. (186-quickstart-part1.md, 187-quickstart-part2.md)  
The instructor defines triggers and workflow inputs and connects them to repository events that will drive CI runs. (188-triggers-and-inputs.md)  
The instructor demonstrates artifact handling, conditional jobs, and repository permissions required for secure automation. (189-artifacts-conditions-and-repo-permissions.md)  
The instructor runs security scanning jobs and shows how to surface findings in the workflow and fail builds when needed. (190-security-scan.md)  
The instructor demonstrates handling secrets and building/publishing Docker images from Actions, including secrets usage and runner configuration. (191-secrets-and-docker.md, 192-build-and-publish-job.md)  
The instructor delivers a GitHub Actions pipeline that replaces or complements Jenkins pipelines for building and publishing artifacts. (Section Summary)

# Section 19 – gitlab

The instructor introduces GitLab CI and performs an initial GitLab project setup used for parallel CI examples. (193-introduction.md, 194-initial-setup.md)  
The instructor creates the first GitLab pipeline with a .gitlab-ci.yml example and documents runner registration. (195-first-pipeline.md)  
The instructor demonstrates variable management, pipeline rules, triggers, and staged job execution specific to GitLab. (196-variables-and-more.md, 197-triggers-and-rules.md)  
The instructor applies security controls and artifact handling in GitLab and integrates builds with artifact repositories. (198-security-and-artifacts.md)  
The instructor finishes by showing GitLab-specific build and deploy patterns that map to the same artifacts produced by other CI systems. (199-build-and*.md, Section Summary)

# Section 20 – python

The instructor sets up the Python development environment and explains version/indentation constraints on lab hosts. (200-introduction.md, 201-python-on-linux-versions-and-indentation.md)  
The instructor covers Python syntax essentials used by ops scripts, including quoting, variables, print formatting, slicing, and operators. (202-quotes-and-comments.md, 203-variables.md, 204-print-format.md, 205-slicing.md, 206-operators.md)  
The instructor demonstrates control flow—conditions, loops, break/continue—and builds reusable functions and modules used in automation. (207-conditions.md, 208-loops.md, 209-break-and-continue.md, 211-functions-part-1.md, 212-functions-part-2.md, 213-modules.md)  
The instructor runs OS-level tasks from Python, uses Fabric for remote execution, and integrates exception handling for robust scripts. (214-os-tasks.md, 215-python-fabric.md, 216-exception-handling.md)  
The instructor demonstrates cloud interactions by using boto3 to automate AWS resources from Python code and records the sample scripts. (217-cloud-interaction-with-boto3.md)  
The section delivers production-ready Python automation examples that are invoked from CI and provisioning workflows. (Section Summary)

# Section 21 – terraform

The instructor introduces Terraform and sets up the local toolchain and provider configuration used for cloud infrastructure automation. (221-introduction.md, 222-basics-of-terraform.md)  
The instructor lays out repository code structure and modular organization for reusable infrastructure definitions. (223-code-structure.md, 224-code-structure-part-2.md)  
The instructor demonstrates plan, apply, update, and destroy workflows including the commands and state handling used in labs. (225-plan-apply-update-and-destroy.md)  
The instructor documents variable usage, input conventions, and how provisioners are invoked during resource creation. (226-variables.md, 227-provisioners.md)  
The instructor records outputs, backends, and remote state storage patterns required to collaborate in team settings. (228-outputs.md, 229-backend.md)  
The instructor completes by showing a Terraform-driven infrastructure deployment that underpins the cloud projects used later. (230-what-next.md, Section Summary)

# Section 22 – ansible

The instructor introduces Ansible, installs control node tooling, and prepares inventory and SSH access for managed hosts. (231-introduction.md, 232-setup-ansible-and-infra.md)  
The instructor builds inventories and demonstrates the ping module to validate connectivity and agentless management. (233-inventory-and-ping-module.md, 234-inventory-part-2.md)  
The instructor covers YAML/JSON data structures and shows how playbooks and ad-hoc commands operate against inventory groups. (235-yaml-and-json.md, 236-ad-hoc-commands.md, 237-playbook-and-modules.md)  
The instructor iteratively finds, uses, and troubleshoots modules while demonstrating copy/template modules, handlers, and idempotent patterns. (238-modules---find-use-troubleshoot-and-repeat.md, 245-file-copy-and-template-modules.md, 246-handlers.md)  
The instructor configures Ansible settings, variables, and debug patterns and demonstrates group/host/fact variables for dynamic playbooks. (239-ansible-configuration.md, 240-variables-and-debug.md, 241-group-and-host-variables.md, 242-fact-variables.md)  
The instructor demonstrates decision-making, loops, and control structures inside playbooks and shows how to integrate Ansible into CI pipelines. (243-decision-making.md, 244-loops.md)  
The section finishes with a set of Ansible playbooks that automate the vprofile and infrastructure setup used downstream. (Section Summary)

# Section 23 – monitoring and observability

The instructor establishes monitoring requirements and selects toolchains for logs and metrics. (250-introduction-to-monitoring.md, 251-why-monitoring-is-essential-for-devops.md)  
The instructor provisions a monitoring environment and installs Prometheus, Grafana, and Loki components used for metrics and logs. (252-monitoring-and-observability-tools.md, 253-setting-up-the-monitoring-environment.md)  
The instructor deploys Loki and a web server to capture logs and configures Promtail/agents to forward logs into Loki. (254-loki-and-web-server-setup.md)  
The instructor adds node exporters and configures Prometheus scrape jobs to collect host and application metrics. (255-adding-a-node-to-prometheus.md)  
The instructor introduces PromQL, creates queries, and builds Grafana dashboards from those queries to visualize service health. (256-understanding-promql-.md, 259-promql-for-grafana-dashboards.md, 260-building-grafana-panels-and-dashboards.md)  
The instructor connects Grafana to Prometheus, demonstrates alert rules, and integrates Slack for notifications on critical conditions. (257-connecting-grafana-and-prometheus.md, 258-integrating-slack-for-notifications.md)  
The section closes with a validated observability stack used to monitor the application and infrastructure deployed in the course. (Section Summary)

# Section 24 – aws part 2

The instructor introduces VPC design and components required for production-like networking in AWS. (263-vpc-introduction.md, 264-vpc-design-and-components.md)  
The instructor documents VPC creation steps, subnets, internet gateway, route tables, and NAT gateways used to isolate and secure workloads. (265-vpc-setup-details.md, 266-default-vpc.md, 267-create-vpc.md, 268-subnets.md, 269-internet-gateway.md, 270-route-tables.md, 271-nat-gateway.md)  
The instructor provisions a bastion host pattern and validates SSH access workflows for private subnets. (272-bastion-host.md)  
The instructor deploys websites and application stacks into the VPC and demonstrates peering patterns used for cross-account or cross-VPC connectivity. (273-website-in-vpc.md, 274-peering.md)  
The instructor captures Terraform examples that automate the VPC and networking setup and provides reproducible IaC code. (275-terraform-for-vpc-setup.md)  
This section establishes secure network foundations that other AWS modules and the CI/CD project build on. (Section Summary)

# Section 25 – aws ci cd project

The instructor introduces a complete AWS CI/CD project that integrates CodeCommit, CodeBuild, ECR, CodeDeploy/Beanstalk and other services. (282-introduction.md)  
The instructor sets up Elastic Beanstalk environments, RDS instances, and application wiring used for the CI/CD delivery target. (283-beanstalk.md, 284-rds-and-app-setup-on-beanstalk.md)  
The instructor configures source control integration and demonstrates committing code into CodeCommit and triggering builds. (285-code-commit.md)  
The instructor configures CodeBuild projects that produce artifacts, builds Docker images, and pushes them to ECR. (286-code-build.md)  
The instructor demonstrates deploy pipelines that take artifacts from build, run tests, and promote successful builds into Beanstalk environments. (286-code-build.md, 283-beanstalk.md)  
The section culminates in a runnable AWS-native CI/CD pipeline that builds, tests, and deploys the vprofile application. (Section Summary)

# Section 26 – gcp project

The instructor introduces a GCP vprofile project and documents architecture choices mapped to GCP services. (288-introduction-to-the-gcp-vprofile-project.md, 289-project-architecture-overview.md)  
The instructor sets up GCP account, project, and credentials required for IaC and CLI automation. (290-setting-up-your-gcp-account-and-project.md)  
The instructor records commands embedded in source code and shows how to configure project variables used by automation. (291-commands-in-the-source-code.md, 292-configuring-project-variables.md)  
The instructor provisions VPCs, subnets, firewall rules, and VM deployments using reproducible commands and IaC patterns. (293-vpc-subnets-and-network-setup.md, 294-firewall-rules-and-vm-deployment.md)  
The instructor configures Cloud SQL, Memorystore, Cloud DNS, custom VM images, managed instance groups, and the global HTTP/HTTPS load balancer used for production-like deployments. (295-configuring-cloud-sql-and-memorystore.md, 296-setting-up-cloud-dns.md, 297-creating-a-custom-vm-image.md, 298-building-a-managed-instance-group.md, 299-configuring-the-global-http-https-load-balancer.md)  
This section produces a complete GCP-hosted variant of the vprofile architecture suitable for GitOps and CI pipelines. (Section Summary)

# Section 27 – docker

The instructor introduces Docker-specific topics and prepares the environment for image builds. (302-introduction.md)  
The instructor walks through Docker installation and local setup used in all container exercises. (303-docker-setup.md)  
The instructor documents core Docker commands and concepts used to build, run, inspect, and troubleshoot containers. (304-docker-commands-and-concepts.md)  
The instructor demonstrates log collection, container storage with volumes, and common runtime troubleshooting steps. (305-docker-logs.md, 306-docker-volumes.md)  
The instructor builds images, explains ENTRYPOINT vs CMD, and creates multi-stage Dockerfiles to produce lean build artifacts. (307-building-images.md, 308-entrypoint-and-cmd.md, 310-multi-stage*.md)  
The instructor shows how docker-compose defines multi-container applications and runs the sample stacks used in later labs. (309-docker-compose.md)  
The section provides a reproducible Docker image build and run process used throughout CI and orchestration examples. (Section Summary)

# Section 28 – containerization

The instructor explains base image selection and Docker Hub integration for the vprofile images. (311-introduction.md, 312-overview-of-base-image.md, 313-dockerhub-setup.md)  
The instructor installs and configures Docker Engine for the lab environment and maps Dockerfile references to application source. (314-setup-docker-engine.md, 315-dockerhub-and-dockerfile-references.md)  
The instructor writes Dockerfiles for app, DB, and web components and records the exact instructions and build contexts. (316-app-image-dockerfile.md, 317-db-image-dockerfile.md, 318-web-image-dockerfile.md)  
The instructor composes multi-container stacks with docker-compose, builds images, and runs the application end-to-end locally. (319-docker-compose.md, 320-build-and-run.md)  
The instructor summarizes containerization steps and then containerizes the microservice project for CI and Kubernetes deployment. (321-summarize.md, 322-containerizing-microservice-project.md)  
This section hands off containerized artifacts and compose files that feed the CI/CD pipelines and GitOps flows. (Section Summary)

# Section 29 – kubernetes

The instructor introduces Kubernetes and presents multiple cluster setup options (minikube, kops) for local and cloud clusters. (324-introduction.md, 325-minikube-for-k8s-setup.md, 326-kops-for-k8s-setup.md)  
The instructor documents Kubernetes objects and how to author resource YAML for reproducible deployments. (327-objects-and-documentation.md)  
The instructor configures kubeconfig contexts and CLI usage patterns used throughout the labs. (328-kube-config.md, 340-kubectl-cli-and-cheatsheet.md)  
The instructor creates Pods, Services, ReplicaSets, Deployments, and demonstrates rolling updates and health checks. (329-pods.md, 332-service.md, 333-replica-set.md, 334-deployment.md)  
The instructor covers volumes, ConfigMaps, Secrets, commands/args, and shows logging levels and diagnostics used in production troubleshooting. (335-command-and-arguments.md, 336-volumes.md, 337-config-map.md, 338-secret.md, 331-different-levels-of-logging.md)  
The instructor introduces Ingress, Helm charts, runs Helm hands‑on exercises, and documents Helm chart patterns used later in GitOps. (339-ingress.md, 342-helm-introduction.md, 343-helm-hands-on.md, 344-helm-with-ai.md)  
The section produces a working Kubernetes application deployment pattern and Helm charts that become inputs to the GitOps project. (Section Summary)

# Section 30 – app dep on kub clu

The instructor introduces the application deployment architecture for Kubernetes-based clusters. (347-introduction.md)  
The instructor diagrams the deployment architecture and maps application services to Kubernetes primitives used in manifests. (348-architecture.md)  
The instructor inspects the source code and extracts container images, ports, and runtime configuration that the manifests will require. (349-source-code-overview.md)  
The instructor secures sensitive values as Kubernetes Secrets and documents the secret creation steps used in CI. (350-secret.md)  
The instructor provisions a PersistentVolume for the MySQL component and records the exact storage class and claim definitions. (351-persistent-volume-for-db-.md)  
The instructor creates and deploys MySQL, Memcache, RabbitMQ, and Tomcat application manifests, validates Service connectivity, and exposes the app via Ingress. (352-mysql-app.md, 353-mysql-service.md, 354-memcache-app-and-service.md, 355-rabbitmq-app-and-service.md, 356-tomcat-app-and-service.md, 357-ingress.md)  
The instructor documents cluster setup and source code mapping so that the same manifests are deployable via GitOps and CI pipelines. (358-k8s-cluster-setup-and-source-code.md, Section Summary)

# Section 31 – gitops project

The instructor introduces the GitOps project and its repository layout dedicated to cluster state and helm charts. (361-Intro.md, 362-Architecture.md)  
The instructor sets up Git repositories, branching, and secrets used to store cluster manifests and Helm charts. (363-Git-Repo-Setup.md, 369-GitHub-Secrets-Variables.md)  
The instructor authors Helm charts for application components, iterates chart values, and prepares chart repositories consumed by ArgoCD. (364-Helm-Charts-1.md, 365-Helm-Charts-2.md)  
The instructor documents the CI pipeline that builds container images, runs code analysis, and pushes images to ECR for GitOps consumption. (366-CI-Pipeline-Overview.md, 370-CICD-Pipeline-1.md, 371-CICD-Pipeline-2.md)  
The instructor installs SonarQube for code quality checks and demonstrates the end-to-end pipeline with quality gates before promotion. (367-SonarQube-Server.md, 168-Code-Analysis.md)  
The instructor configures ECR, IAM roles, and GitHub repository variables that tie CI outputs to GitOps deployments. (368-ECR-IAM.md, 369-GitHub-Secrets-Variables.md)  
The instructor deploys ArgoCD, configures app sync, and demonstrates automatic synchronization of Git changes into the cluster. (372-EKS-Prereqs.md, 374-ArgoCD-Setup.md, 375-Argo-App-Sync.md)  
This section completes a full GitOps workflow where code commits produce images and Git-hosted manifests drive cluster state via ArgoCD. (Section Summary)

# Section 32 – conclusion

The instructor compiles final resume and career guidance materials and provides artifact references for reproducing course projects. (378-resumes.md)  
The instructor summarizes the end-to-end engineering outcomes achieved across the course: reproducible dev VMs, container images, CI pipelines, cloud infrastructure, configuration automation, monitoring stacks, and GitOps deployments. (Section Summary)
