Section: section-01-introduction
- The instructor lays out the project scope, goals, and the end-to-end systems to be built and integrated across the course. (01-Introduction.md)
- The instructor describes DevOps as an engineering practice that combines CI/CD pipelines, infrastructure automation, monitoring, and feedback loops to deliver software reliably. (02-What-is-DevOps.md)
- The instructor defines Continuous Integration practices and explains the engineering need to verify change quickly via automated builds and tests, establishing CI as the first automation layer. (04-Continuous-Integration.md)
- The instructor defines Continuous Delivery and positions automated artifact production and deployment pipelines as the engineering outcome to be implemented across later sections. (05-Continuous-Delivery.md)
- By the end of this section, the course-wide engineering objectives and a target architecture for CI/CD, automation, and cloud deployment are defined and available as the project blueprint. (Section Summary)

Section: section-02-prerequisites-info-and-setup
- The instructor enumerates hardware and software prerequisites, ensuring reproducible lab execution environments and version constraints for all tools used later. (01-prerequisites.md)
- The instructor documents Windows package management using Chocolatey to standardize developer workstation provisioning for the course. (02-chocolatey.md)
- The instructor records step-by-step software installation commands and versions (editors, Git, Docker, Vagrant, Terraform, AWS/GCP CLIs) to produce repeatable developer setups. (03-software-installation.md)
- The instructor provides account signup flows and required cloud/third-party services to ensure every student can access required cloud resources for hands-on labs. (06-signups.md)
- By the end of this section, a standardized, reproducible developer workstation and account inventory exists that enables the remainder of the engineering work. (Section Summary)

Section: section-03-vm-setup
- The instructor explains virtualization fundamentals and why VM-based isolation is chosen for initial labs to mirror on-prem/VM workflows. (16-virtualization-overview.md)
- The instructor clarifies virtualization terminology and the engineering trade-offs between hypervisors, images, and resource allocation for lab VMs. (17-what-is-virtualization.md)
- The instructor outlines the VM-based lab architecture and the baseline images chosen for subsequent provisioning. (18-introduction.md)
- The instructor documents manual VM creation steps and hands-on validation, producing a working VM image and operational checklist for automated provisioning later. (19-vm-manual.md)
- By the end of this section, a validated manual VM baseline exists and is ready to be converted into automated provisioning artifacts in later sections. (Section Summary)

Section: section-04-linux
- The instructor establishes the Linux server baseline used across labs and documents the core OS concepts required for operations and automation. (23-linux-intro.md)
- The instructor records filesystem commands and layout conventions necessary for installing and managing application artifacts on lab hosts. (24-commands-filesystem.md)
- The instructor documents a set of essential shell commands and workflows used repeatedly in provisioning, debugging, and CI agents. (25-basic-commands.md)
- The instructor introduces vi/vim configuration and usage to support editing configuration files on headless lab VMs. (26-vim.md)
- The instructor catalogs Linux file types and their operational meaning for packaging and deployment pipelines. (27-file-types.md)
- The instructor demonstrates data filtering tools used for troubleshooting and logs analysis during later CI/CD and monitoring tasks. (28-filters.md)
- The instructor explains I/O redirection patterns used by service startup and automation scripts for deterministic logs and process orchestration. (29-redirection.md)
- The instructor codifies user and group management practices that will be referenced by provisioning/Ansible scripts. (30-users-groups.md)
- The instructor records file permission and sudo practices required to securely run CI/CD agents and automation tasks. (31-permissions.md)
- The instructor documents package management strategies and how they will be used to install build/runtime dependencies across environments. (33-package-management.md)
- The instructor documents service management patterns (systemd) used later to run build agents, web servers, and monitoring agents. (34-services.md)
- The instructor captures process inspection and lifecycle commands used when diagnosing services in CI, VMs, and containers. (35-processes.md)
- By the end of this section, a reproducible set of Linux operational practices and command sequences exists and is referenced by later automation code. (Section Summary)

Section: section-05-git
- The instructor establishes version control as the single source of truth and documents repository strategies required for CI/CD and GitOps. (40-introduction.md)
- The instructor describes versioning strategies and how releases and artifacts will be tied to tags/semver for later automation. (41-versioning.md)
- The instructor documents branching models, branch protections, and workflows that will govern feature development, CI triggers, and merge flows. (42-branches.md)
- The instructor documents rollback procedures and Git commands to recover application state during deployment failures. (43-rollback.md)
- The instructor documents SSH key setup and secure Git access required by CI agents and automated deployments. (44-git-ssh.md)
- The instructor documents tagging and semantic versioning practices that will later drive artifact promotion in CI pipelines. (45-tags-semver.md)
- The instructor records how GitHub Copilot will be used as a coding aid in automation tasks (policy, not required for execution). (46-github-copilot.md)
- By the end of this section, repository governance, branching, tagging, and secure remote access practices exist and are ready to drive CI/CD triggers and GitOps flows. (Section Summary)

Section: section-06-vagrant-and-linux-servers
- The instructor configures Vagrant environments with explicit control over IPs, RAM, and CPU to reproduce multi-VM lab topologies. (49-Vagrant-IP-RAM-CPU.md)
- The instructor explains folder-sync patterns between host and guest so source code and automation artifacts remain editable and testable during local development. (50-Vagrant-Sync-Dirs.md)
- The instructor demonstrates provisioning sequences (shell/Ansible) that install and configure services on Vagrant VMs, producing reproducible server state. (51-Provisioning.md)
- The instructor sets up a sample website and documents how the site is deployed onto provisioned VMs to validate full-stack provisioning flows. (52-Website-Setup.md)
- The instructor automates a WordPress deployment on Vagrant to produce a multi-component application environment (web, DB) for integration testing. (53-WordPress-Setup.md)
- The instructor converts manual site installs into idempotent automation scripts to ensure repeatable rebuilds of the lab environment. (54-Automate-Website.md)
- The instructor automates WordPress-specific tasks (plugins, DB migrations) to validate application-level automation integration. (55-Automate-WordPress.md)
- The instructor documents AI-assisted automation considerations relevant to Vagrant workflows. (56-Copilot-AI.md)
- The instructor expands multi-VM Vagrant orchestration patterns to model real multi-service deployments in later container and orchestration sections. (57-Multi-VM-Vagrant.md)
- By the end of this section, Vagrant-based, reproducible multi-VM environments and idempotent provisioning scripts exist and are used to prototype application infrastructure. (Section Summary)

Section: section-07-vars-json-yaml
- The instructor introduces structured variables and demonstrates how typed/structured data (JSON/YAML) will be used by Terraform/Ansible/Helm pipelines. (60-Variables-Python-DS.md)
- The instructor documents JSON vs YAML formats and parsing patterns used by automation tools for templates and config injection. (61-JSON-YAML.md)
- By the end of this section, a consistent approach for variable representation and templating across automation tools exists and is used by subsequent provisioning and CI code. (Section Summary)

Section: section-08-vprofile-setup
- The instructor introduces the application project (“vprofile”) and its component breakdown, establishing the target application to be automated and deployed. (62-Project-Welcome.md)
- The instructor describes the project onboarding and initial architecture for the vprofile application used throughout the course. (63-Intro.md)
- The instructor provisions VM hosts used to run the multi-component vprofile app for integration testing and local demos. (64-VM-Setup.md)
- The instructor installs and configures MySQL as the relational datastore for the vprofile app, documenting schema and connection details required by deployment automation. (65-MySQL-Setup.md)
- The instructor deploys memcached (or memcache) as a caching tier and records its configuration to accelerate the app during load tests. (66-Memcache-Setup.md)
- The instructor installs RabbitMQ as the message broker component and configures durable queues used by asynchronous app components. (67-RabbitMQ-Setup.md)
- The instructor installs the vprofile application on the provisioned VMs and documents the runtime configuration, ports, and operational checks. (68-App-Setup.md)
- The instructor installs and configures Nginx as a reverse proxy and static asset server fronting the application components. (69-Nginx-Setup.md)
- The instructor validates the entire vprofile stack end-to-end and captures verification steps for later CI and monitoring integration. (70-Validate.md)
- The instructor introduces automated provisioning for the vprofile stack and provides the automation code or commands that will be reused by CI/CD and Terraform/Ansible workflows. (71-Automated-Intro.md)
- The instructor supplies the automated provisioning code and demonstrates its execution to produce reproducible application environments. (72-Automated-Code.md)
- By the end of this section, a working multi-component vprofile application stack (MySQL, Memcache, RabbitMQ, App, Nginx) exists on reproducible VMs and is codified into automated provisioning artifacts. (Section Summary)

Section: section-09-networking
- The instructor records ISO/networking fundamentals to ensure learners understand networking primitives used in cloud and container deployments. (74-ISO.md)
- The instructor documents IP addressing and subnetting concepts used later when designing VPC/subnet layouts. (75-Networks-IP.md)
- The instructor documents transport and application-layer protocols and port mapping patterns required for exposing services in VMs, containers, and cloud load balancers. (76-Protocols-Ports.md)
- The instructor provides a toolkit of networking commands used for troubleshooting routing, firewall, and connectivity issues during deployments. (77-Networking-Commands.md)
- By the end of this section, a network troubleshooting workflow and an understanding of networking components required by subsequent VPC/container orchestration tasks exist. (Section Summary)

Section: section-10-containers
- The instructor clarifies container fundamentals and why containers are used as the next step beyond VMs for packaging services. (78-Containers.md)
- The instructor introduces Docker as the chosen container runtime and documents the environment used for building and running containers in labs. (79-Docker.md)
- The instructor performs hands-on Docker experiments to validate container lifecycle, image layering, and runtime behavior relevant to later CI pipelines. (80-Docker-Hands-On.md)
- The instructor demonstrates how the vprofile project maps to containerized components, establishing container artifacts for the application. (81-VProfile-Containers.md)
- The instructor explains how the microservices model informs container design and inter-service networking used in Kubernetes and orchestrations. (82-Microservices.md)
- By the end of this section, container images and a repeatable local container-based development workflow for vprofile exist and will be used as input artifacts for CI and orchestration steps. (Section Summary)

Section: section-11-bash-scripting
- The instructor introduces shell scripting essentials used throughout automation and build agents. (85-Intro.md)
- The instructor records VM preparation steps used to run shell scripts across remote hosts. (86-VM-Setup.md)
- The instructor authors and validates initial shell scripts that automate common tasks and system checks in the lab environment. (87-First-Script.md)
- The instructor provides sample scripts demonstrating idempotent operations and reusable utilities for automation chains. (88-Sample-Script.md)
- The instructor documents how to use ChatGPT/AI to accelerate script writing while noting validation and security considerations. (89-ChatGPT.md)
- The instructor captures variable patterns, CLI argument parsing, and system variable usage to make scripts reusable in CI. (90-Variables.md; 91-CLI-Arguments.md; 92-System-Variables.md)
- The instructor demonstrates loops, conditional logic, and control-flow constructs required to orchestrate multi-step deployments and error handling within scripts. (100-For-Loops.md; 101-While-Loops.md; 207-conditions.md; 208-loops.md)
- The instructor documents SSH key exchange and remote execution patterns used to run scripts on fleet hosts and by CI agents. (102-Remote-Execution.md; 103-SSH-Key-Exchange.md)
- The instructor demonstrates final combined scripts that will be invoked by CI pipelines to orchestrate build, test, and deployment steps. (104-Finale-1.md; 105-Finale-2.md)
- By the end of this section, a library of production-ready shell scripts and conventions exists and is integrated into later CI/CD and provisioning workflows. (Section Summary)

Section: section-12-ai-scripting
- The instructor explores how AI-assisted code completion and generation can accelerate routine automation tasks like templating and script generation for DevOps. (106-Autocomplete.md)
- The instructor defines best practices to safely incorporate AI-generated suggestions into automation code while maintaining reproducibility and security. (107-Best-Practices.md)
- The instructor documents how AI suggestions can be integrated into CI workflows as developer aids but not as automation authoritative sources. (108-AI-Suggestions.md)
- The instructor demonstrates AI-based code generation examples specifically targeted at DevOps automation (scripts, CI templates, config). (109-AI-Code-Generation.md)
- By the end of this section, guidelines and examples for safe AI-assisted automation exist and can be used to speed up engineering tasks without replacing validation workflows. (Section Summary)

Section: section-13-aws-part-1
- The instructor frames cloud computing fundamentals and why AWS is used for scaling the vprofile project. (110-Cloud-Computing.md)
- The instructor introduces core AWS services that will be used (EC2, EBS, ELB, CloudWatch, S3) and maps them to vprofile architecture components. (111-Intro.md)
- The instructor gives an EC2 quick-start and provisions initial EC2 instances to run application components and CI/CD agents. (112-EC2-Intro.md; 113-EC2-Quick-Start.md)
- The instructor details EC2 instance types and demonstrates hands-on provisioning and instance lifecycle management. (114-EC2-Part1.md; 115-EC2-Part2.md)
- The instructor demonstrates AWS CLI usage and CloudShell/SSM patterns for remote management of EC2 hosts used in automation. (116-AWS-CLI.md; 117-SSM-CloudShell.md)
- The instructor explains EBS volumes and snapshot strategies for durable storage and backup of instance data used by the application. (118-EBS.md; 119-EBS-Snapshots.md)
- The instructor introduces Elastic Load Balancers and configures them to front EC2 application tiers. (120-ELB-Intro.md; 121-ELB-HandsOn-1.md; 122-ELB-HandsOn-2.md)
- The instructor demonstrates CloudWatch metrics, logging, and alarm creation to instrument the deployed EC2 fleet for observability. (123-CloudWatch-Intro.md; 124-CloudWatch-HandsOn.md)
- The instructor shows EFS usage for shared file storage patterns across autoscaled instances. (125-EFS.md)
- The instructor introduces and implements Auto Scaling Groups to scale EC2 fleets in response to load and metrics. (126-AutoScaling-Intro.md; 127-AutoScaling-HandsOn.md)
- The instructor configures S3 as an object store for artifacts and static assets used by deployments and build pipelines. (128-S3-Intro.md)
- By the end of this section, foundational AWS infrastructure primitives (EC2, EBS, ELB, ASG, CloudWatch, S3) are provisioned manually and instrumented, establishing the cloud execution layer for the application. (Section Summary)

Section: section-14-aws-cloud
- The instructor provides a structured AWS lab introduction and defines security group and keypair policies used for secure EC2 access. (132-Intro.md; 133-Security-Groups-Keypairs.md)
- The instructor provisions EC2 instances with secure network controls and documents instance provisioning and AMI usage patterns used later for autoscaling and image baking. (134-EC2-Instances.md)
- The instructor configures Route53 DNS records to map domain names to application endpoints and load balancers. (135-Route53-DNS.md)
- The instructor documents build and deployment artifacts (JAR/WAR/images) and how they are staged to S3, ECR, or deployment targets for automated pipelines. (136-Build-Deploy-Artifacts.md)
- The instructor configures Load Balancer DNS and integrates Route53 and ELB for resilient routing of external traffic. (137-LoadBalancer-DNS.md)
- The instructor implements Auto Scaling groups with launch templates and lifecycle hooks to achieve horizontal scaling of application tiers. (138-AutoScaling-Group.md)
- By the end of this section, an AWS environment with secure networking, instances, load balancing, DNS, artifact staging patterns, and autoscaling capability exists and is prepared for infrastructure-as-code automation. (Section Summary)

Section: section-15-re-architecting
- The instructor introduces re-architecting patterns to move the monolithic vprofile stack toward managed cloud services. (140-Intro.md)
- The instructor documents security group updates and keypair handling in the re-architected design to maintain secure access controls. (141-Security-Groups-Keypairs.md)
- The instructor migrates the database layer to managed RDS instances and documents configuration for connections, backups, and parameter groups. (142-RDS.md)
- The instructor migrates caching to Elasticache and documents clustering and parameterization for production readiness. (143-ElasticCache.md)
- The instructor explores managed messaging with Amazon MQ and documents migration changes needed for RabbitMQ replacement. (144-Amazon-MQ.md)
- The instructor documents database initialization and schema migration steps to move from local MySQL to RDS while preserving data. (145-DB-Initialization.md)
- The instructor demonstrates deploying the app on Elastic Beanstalk as a managed platform option and outlines the continuous deployment flow to it. (146-Beanstalk.md)
- The instructor records required security group and ELB updates for the re-architected platform and tests traffic flows. (147-SG-ELB-Update.md)
- The instructor records artifact packaging and how build artifacts are promoted to managed platform deployments. (148-Build-Deploy-Artifact.md)
- The instructor explains CloudFront usage and CDN fronting strategies for static assets in a re-architected design. (149_CloudFront_Complete_Explanation.md)
- By the end of this section, a re-architected cloud deployment strategy exists where managed services (RDS, Elasticache, Amazon MQ, Beanstalk, CloudFront) replace self-managed components and define a path for operational scalability. (Section Summary)

Section: section-16-build-tools
- The instructor introduces build tools and demonstrates how Maven is used to produce deployable Java artifacts for the vprofile project. (151_Introduction.md; 152_Maven_Hands_on.md)
- The instructor records mixed-tool build workflows (Maven plus NodeJS artifacts) and how these artifacts are integrated into CI pipelines. (153. Maven, NodeJS & AI.md)
- The instructor creates a small README that links build tool usage into the CI lifecycle for repeatability. (README.md)
- By the end of this section, local build tool configurations and artifact outputs are defined and will be consumed by CI pipelines for image creation and deployment. (Section Summary)

Section: section-17-continuous-integration-and-delivery-with-jenkins
- The instructor installs and validates Jenkins as a CI orchestrator and records installation steps for reproducible CI host provisioning. (154.-Introduction.md; 155.-Installation.md)
- The instructor explains the difference between Freestyle jobs and Pipeline-as-Code and selects pipelines-as-code for reproducible automation. (156.-Freestyle-Vs-Pipeline-As-A-Code.md)
- The instructor creates the first Jenkins job and demonstrates an automated first-build flow to validate SCM integration and build agents. (158.-First-Job.md; 159.-First-Build-Job.md)
- The instructor sets up and configures Jenkins agents, documenting agent registration, labels, and resource allocation used by pipelines. (160.-Agents.md)
- The instructor inventories necessary Jenkins plugins, documents versioning, and records plugin choices required for Docker, Git, and artifact management. (161-Plugins-Versioning-&-more.md)
- The instructor troubleshoots disk-space issues and documents cleanup and retention policies to maintain CI host health. (162-Disk-Space-Issue.md)
- The instructor maps the CI pipeline flow (checkout, build, test, artifact publish) into a reproducible pipeline and records steps for later conversion into GitHub Actions/GitLab CI equivalents. (163-Flow-of-Continuous-Integration-Pipeline.md; 164-Steps-for-Continuous-Integration-Pipeline.md)
- The instructor provisions and integrates Jenkins with Nexus and SonarQube to perform artifact publishing and static code analysis as part of CI. (165-Jenkins-Nexus-&-Sonarqube-Setup.md)
- The instructor defines notification integrations (Slack) to surface CI results to teams. (173-Notification-Slack.md)
- The instructor integrates Docker build & publish steps into Jenkins pipelines to produce container images from build artifacts. (174-CI-for-Docker---Intro.md; 175-Docker-PAAC-Prereqs-info.md; 176-Docker-PAAC-Demo.md)
- The instructor captures pipeline-as-code examples and shows how Jenkinsfiles orchestrate build, test, image build, and artifact publish steps for the vprofile app. (167-Pipeline-As-A-Code-Introduction.md; 178-Docker-CICD-Code.md)
- By the end of this section, an operational Jenkins CI environment exists that builds code, runs static analysis, produces artifacts, builds container images, and integrates with Nexus/SonarQube/Slack for full pipeline automation. (Section Summary)

Section: section-18-github-actions
- The instructor introduces GitHub Actions as a cloud-native CI platform and records the Quickstart setup to run workflows in the repository. (185-introduction.md; 186-quickstart-part1.md; 187-quickstart-part2.md)
- The instructor demonstrates workflow triggers (push, pull_request, scheduled), inputs, and event semantics used to run CI pipelines automatically. (188-triggers-and-inputs.md)
- The instructor documents artifact handling, conditional steps, and repository permissions required for secure and maintainable Actions workflows. (189-artifacts-conditions-and-repo-permissions.md)
- The instructor integrates security scans and SAST into GitHub Actions to fail builds on critical vulnerabilities. (190-security-scan.md)
- The instructor demonstrates using GitHub Secrets for Docker registry authentication and configures build-and-publish jobs that build container images and publish to registries. (191-secrets-and-docker.md; 192-build-and-publish-job.md)
- By the end of this section, fully-specified GitHub Actions workflows exist that build, test, scan, and publish artifacts and container images, providing a cloud-hosted CI path for the project. (Section Summary)

Section: section-19-gitlab
- The instructor introduces GitLab CI and documents initial setup patterns and the first pipeline used to exercise the platform. (193-introduction.md; 194-initial-setup.md; 195-first-pipeline.md)
- The instructor demonstrates variables, pipeline configuration, triggers, and rules specific to GitLab CI and how they map to previous CI platforms. (196-variables-and-more.md; 197-triggers-and-rules.md)
- The instructor documents security and artifact handling within GitLab and how to configure CI for secure artifact storage and access. (198-security-and-artifacts.md)
- By the end of this section, equivalent CI pipelines exist in GitLab demonstrating multi-platform CI options and providing alternative CI paths for the project artifacts. (Section Summary)

Section: section-20-python
- The instructor introduces Python as an automation language for DevOps tasks and documents cross-platform considerations for running Python on Linux. (200-introduction.md; 201-python-on-linux-versions-and-indentation.md)
- The instructor builds a library of Python examples demonstrating variables, control flow, functions, modules, and exception handling used later for small automation tasks and orchestration. (203-variables.md; 208-loops.md; 211-functions-part-1.md; 216-exception-handling.md)
- The instructor demonstrates OS-level interactions with Python (os module, subprocess), and how Python scripts will invoke cloud CLIs and manage artifacts in CI. (214-os-tasks.md; 217-cloud-interaction-with-boto3.md)
- The instructor shows Fabric usage to orchestrate remote tasks from Python as an alternative to shell scripting or Ansible for certain automation jobs. (215-python-fabric.md)
- By the end of this section, a suite of Python-based automation utilities and examples exists and is available as an alternative scripting layer for CI tasks and cloud interactions. (Section Summary)

Section: section-21-terraform
- The instructor introduces Terraform as the infrastructure-as-code tool for provisioning cloud resources and documents supported cloud providers. (221-introduction.md)
- The instructor records Terraform basics, workflow (init/plan/apply), and state handling that will be used to automate AWS/GCP infrastructures introduced earlier. (222-basics-of-terraform.md; 225-plan-apply-update-and-destroy.md)
- The instructor outlines a code structure for maintaining modules and environments to support multi-environment deployments. (223-code-structure.md; 224-code-structure-part-2.md)
- The instructor defines variables, provisioners, outputs, and backends, including remote state configuration used for team deployments, and documents example module implementations for VPC and compute. (226-variables.md; 227-provisioners.md; 228-outputs.md; 229-backend.md)
- By the end of this section, Terraform configuration and module scaffolding exist that can reproducibly provision VPCs, compute instances, and managed cloud services used by the vprofile project. (Section Summary)

Section: section-22-ansible
- The instructor introduces Ansible as the configuration-management system to provision and configure OS-level services and application stacks. (231-introduction.md)
- The instructor documents Ansible environment setup and example infrastructure used for playbook development and testing. (232-setup-ansible-and-infra.md)
- The instructor defines inventory patterns, group/host variables, and idempotent playbooks for roles used to install app components (MySQL, RabbitMQ, Nginx) across host groups. (233-inventory-and-ping-module.md; 234-inventory-part-2.md; 241-group-and-host-variables.md)
- The instructor demonstrates module usage, ad-hoc commands, templates, handlers, and complex playbook constructs (loops, conditionals, decision-making) used to build robust, repeatable automation. (235-yaml-and-json.md; 236-ad-hoc-commands.md; 237-playbook-and-modules.md; 238-modules---find-use-troubleshoot-and-repeat.md; 243-decision-making.md; 244-loops.md; 245-file-copy-and-template-modules.md; 246-handlers.md)
- The instructor documents debugging, variable scoping, and facts usage so Ansible runs reliably in diverse lab environments. (239-ansible-configuration.md; 240-variables-and-debug.md; 242-fact-variables.md)
- By the end of this section, a complete Ansible codebase and playbook library exist to configure OS and application state for both Vagrant/VM and cloud-hosted systems, ready to be invoked by CI/CD. (Section Summary)

Section: section-23-monitoring-and-observability
- The instructor introduces monitoring and observability goals and maps required telemetry to components in the vprofile architecture. (250-introduction-to-monitoring.md)
- The instructor explains why monitoring is essential to DevOps and defines alerting and SLO/SLI expectations for the application. (251-why-monitoring-is-essential-for-devops.md)
- The instructor catalogs monitoring and observability tools (Prometheus, Grafana, Loki) and selects a stack for collection, storage, and visualization. (252-monitoring-and-observability-tools.md)
- The instructor provisions a monitoring environment and demonstrates installing Prometheus, Grafana, and Loki to collect metrics and logs from lab services. (253-setting-up-the-monitoring-environment.md; 254-loki-and-web-server-setup.md)
- The instructor adds node exporters and configures Prometheus to scrape targets, explaining metrics instrumentation required by the application. (255-adding-a-node-to-prometheus.md)
- The instructor teaches PromQL queries for alerting and dashboards and demonstrates how to author queries for operational dashboards. (256-understanding-promql-.md)
- The instructor connects Grafana to Prometheus and builds dashboards to visualize app and infra metrics. (257-connecting-grafana-and-prometheus.md; 260-building-grafana-panels-and-dashboards.md)
- The instructor integrates Slack for alert notifications and documents alert routing and runbook creation for incident response. (258-integrating-slack-for-notifications.md)
- The instructor composes PromQL tailored to Grafana panels and demonstrates creating production-grade dashboards for the vprofile stack. (259-promql-for-grafana-dashboards.md)
- By the end of this section, a monitoring stack (Prometheus, Grafana, Loki) with configured exporters, dashboards, and alerting channels exists and is ready to monitor deployed infrastructure and applications. (Section Summary)

Section: section-24-aws-part-2
- The instructor introduces VPC architecture and describes desired isolation and connectivity patterns for production-like cloud networks. (263-vpc-introduction.md)
- The instructor documents VPC design components (subnets, IGWs, route tables, NAT, peering) used to build multi-tier network segmentation. (264-vpc-design-and-components.md)
- The instructor records step-by-step VPC setup details and demonstrates creating VPCs for lab and production environments. (265-vpc-setup-details.md; 267-create-vpc.md)
- The instructor explains default VPC behavior and considerations when replacing it with custom VPCs for security and compliance. (266-default-vpc.md)
- The instructor implements subnets, internet gateways, route tables, NAT gateway patterns, and bastion host architecture to enable secure management and outbound access for private subnets. (268-subnets.md; 269-internet-gateway.md; 270-route-tables.md; 271-nat-gateway.md; 272-bastion-host.md)
- The instructor deploys a website within the VPC, validates connectivity, and demonstrates peering configurations for cross-VPC connectivity. (273-website-in-vpc.md; 274-peering.md)
- The instructor demonstrates Terraform automation for VPC setup and provides the Terraform modules used to codify network infrastructure. (275-terraform-for-vpc-setup.md)
- By the end of this section, a reproducible VPC network architecture (public/private subnets, IGW/NAT, route tables, bastion, peering) exists and is codified for Terraform automation used across environments. (Section Summary)

Section: section-25-aws-ci-cd-project
- The instructor introduces a cloud-native CI/CD project on AWS and maps service responsibilities (CodeCommit, CodeBuild, Beanstalk) for the vprofile app. (282-introduction.md)
- The instructor provisions Elastic Beanstalk environments and documents using Beanstalk for application deployments and autoscaling. (283-beanstalk.md)
- The instructor configures RDS and connects it to Beanstalk-hosted application tiers, documenting environment configuration for app-to-RDS connectivity. (284-rds-and-app-setup-on-beanstalk.md)
- The instructor configures source control with CodeCommit and demonstrates how commits trigger CodeBuild jobs that produce deployment artifacts. (285-code-commit.md; 286-code-build.md)
- The instructor integrates CodeBuild with artifact stores and deployment targets to produce an automated AWS-native pipeline. (286-code-build.md)
- By the end of this section, an AWS-native CI/CD pipeline exists that uses CodeCommit/CodeBuild/Beanstalk (and RDS) to automatically build and deploy the application to AWS managed platforms. (Section Summary)

Section: section-26-gcp-project
- The instructor introduces a GCP project variant for vprofile and documents architecture differences compared to AWS. (288-introduction-to-the-gcp-vprofile-project.md; 289-project-architecture-overview.md)
- The instructor configures the GCP accounts, projects, and IAM prerequisites required to provision GCP resources. (290-setting-up-your-gcp-account-and-project.md)
- The instructor documents CLI commands present in the source code that will be used for GCP automation and infrastructure setup. (291-commands-in-the-source-code.md)
- The instructor configures project variables and parametrization for reproducible GCP deployments. (292-configuring-project-variables.md)
- The instructor provisions VPCs, subnets, firewall rules, and VM deployments on GCP to mirror the cloud architecture used in AWS labs. (293-vpc-subnets-and-network-setup.md; 294-firewall-rules-and-vm-deployment.md)
- The instructor configures managed services on GCP (Cloud SQL, Memorystore) and documents connection/configuration steps for the app. (295-configuring-cloud-sql-and-memorystore.md)
- The instructor configures Cloud DNS, creates custom VM images, and builds managed instance groups and a global HTTP(S) load balancer to serve traffic. (296-setting-up-cloud-dns.md; 297-creating-a-custom-vm-image.md; 298-building-a-managed-instance-group.md; 299-configuring-the-global-http-https-load-balancer.md)
- By the end of this section, a fully-documented GCP variant of the vprofile environment exists—VPC, managed DB/cache, instance groups, global load balancing—ready for Terraform and CI automation. (Section Summary)

Section: section-27-docker
- The instructor provides a comprehensive Docker introduction and establishes the runtime environment used for container builds in CI. (302-introduction.md)
- The instructor documents Docker engine setup, daemon validation, and host-level configuration required for subsequent image builds. (303-docker-setup.md)
- The instructor enumerates core Docker commands, lifecycle operations, and image layering details used when building application images. (304-docker-commands-and-concepts.md)
- The instructor documents Docker logging and troubleshooting techniques that will be used when CI builds or containers fail. (305-docker-logs.md)
- The instructor demonstrates Docker volumes and persistent storage patterns for database and stateful services. (306-docker-volumes.md)
- The instructor documents building images from Dockerfiles, multi-stage builds, and build-time optimizations to produce small, reproducible images. (307-building-images.md)
- The instructor explains entrypoint and CMD semantics to ensure containerized apps start correctly when orchestrated. (308-entrypoint-and-cmd.md)
- The instructor documents docker-compose usage as a local orchestration tool for multi-container application testing before moving to Kubernetes. (309-docker-compose.md)
- By the end of this section, repeatable Dockerfile patterns, images, and local compose-based orchestration exist and serve as the canonical container artifacts for later orchestration and CI pipelines. (Section Summary)

Section: section-28-containerization
- The instructor introduces containerization strategy and base image selection and records choices for language-specific base images. (311-introduction.md; 312-overview-of-base-image.md)
- The instructor documents Docker Hub usage, repository naming, and how images are referenced and pulled during deployments. (313-dockerhub-setup.md; 315-dockerhub-and-dockerfile-references.md)
- The instructor shows how to set up the Docker engine on hosts used by CI and build agents to produce images reproducibly. (314-setup-docker-engine.md)
- The instructor provides Dockerfile examples for application, database, and web service images and explains build-time and runtime configuration for each component. (316-app-image-dockerfile.md; 317-db-image-dockerfile.md; 318-web-image-dockerfile.md)
- The instructor demonstrates composing multi-image setups with docker-compose and running full integration tests to validate containerized app stacks. (319-docker-compose.md; 320-build-and-run.md; 322-containerizing-microservice-project.md)
- The instructor summarizes containerization outcomes and how these images become inputs to CI/CD pipelines and Kubernetes deployments. (321-summarize.md)
- By the end of this section, production-grade container images for all app components exist, are hosted on a registry, and are validated by local compose-based integration tests to become CI inputs. (Section Summary)

Section: section-29-kubernetes
- The instructor introduces Kubernetes concepts and captures the cluster-level architecture that will host the vprofile container workloads. (324-introduction.md)
- The instructor documents cluster setup options (minikube, kops) and provides the exact commands and prerequisites used to bootstrap development and production clusters. (325-minikube-for-k8s-setup.md; 326-kops-for-k8s-setup.md)
- The instructor explains API objects, resource definitions, and documentation patterns used to manage workload manifests and operator integrations. (327-objects-and-documentation.md)
- The instructor records kubeconfig usage and context management for connecting CI agents and developer machines to clusters. (328-kube-config.md)
- The instructor details pods, services, replica sets, deployments, and how each will be applied to host application components. (329-pods.md; 332-service.md; 333-replica-set.md; 334-deployment.md)
- The instructor documents namespaces for multi-tenant separation and log-level strategies and logging options. (330-namespace.md; 331-different-levels-of-logging.md)
- The instructor covers command/args semantics, volumes, ConfigMaps, Secrets, and best practices for injecting configuration into containers at runtime. (335-command-and-arguments.md; 336-volumes.md; 337-config-map.md; 338-secret.md)
- The instructor configures Ingress objects and Ingress controllers for external HTTP(S) routing and documents ingress annotations and TLS handling. (339-ingress.md)
- The instructor provides a kubectl CLI cheatsheet and extras to speed operational tasks for cluster and app management. (340-kubectl-cli-and-cheatsheet.md; 341-extras.md)
- The instructor introduces Helm for templated Kubernetes releases and demonstrates hands-on Helm chart creation and packaging to manage application lifecycle. (342-helm-introduction.md; 343-helm-hands-on.md)
- By the end of this section, Kubernetes manifests, ConfigMaps, Secrets, Services, Deployments, PersistentVolumes, and Helm charts exist and are validated; these artifacts are ready for GitOps-driven deployment. (Section Summary)

Section: section-30-app-dep-on-kub-clu
- The instructor introduces application deployment targets and maps the vprofile microservices to Kubernetes objects for cluster deployment. (347-introduction.md)
- The instructor documents the application architecture in the Kubernetes context, indicating which components become deployments, services, and stateful sets. (348-architecture.md)
- The instructor reviews source code organization and how container images are produced from repository artifacts for Kubernetes deployment. (349-source-code-overview.md)
- The instructor captures Kubernetes Secret management patterns for application credentials and DB connections. (350-secret.md)
- The instructor configures PersistentVolume claims for the MySQL DB and documents storage class and access mode choices. (351-persistent-volume-for-db-.md)
- The instructor creates Kubernetes manifests for MySQL, Memcache, RabbitMQ, and Tomcat app services and verifies in-cluster networking and service discovery. (352-mysql-app.md; 353-mysql-service.md; 354-memcache-app-and-service.md; 355-rabbitmq-app-and-service.md; 356-tomcat-app-and-service.md)
- The instructor configures Ingress and validates external routing to the in-cluster application. (357-ingress.md)
- The instructor demonstrates cluster setup and deployment of the full vprofile source code, creating a complete application environment running on Kubernetes. (358-k8s-cluster-setup-and-source-code.md)
- By the end of this section, the vprofile application is fully deployed on Kubernetes using manifests/Helm charts, with persistent storage, secrets, services, and ingress configured for production-like operation. (Section Summary)

Section: section-31-gitops-project
- The instructor introduces GitOps principles and maps them onto the vprofile deployment lifecycle to achieve declarative cluster state management. (361-Intro.md)
- The instructor documents the GitOps architecture: Git repositories hold manifests/Helm charts and an operator (ArgoCD) performs continuous reconciliation. (362-Architecture.md)
- The instructor sets up dedicated Git repositories and branches to store application manifests and infrastructure definitions used by the GitOps operator. (363-Git-Repo-Setup.md)
- The instructor converts Helm charts and Kubernetes manifests to GitOps-ready artifacts and documents chart parameterization for environments. (364-Helm-Charts-1.md; 365-Helm-Charts-2.md)
- The instructor designs CI pipeline responsibilities (build, lint, push images, update manifest refs) and documents the CI-to-GitOps handoff. (366-CI-Pipeline-Overview.md)
- The instructor provisions SonarQube server for code quality gating and documents integration points into the GitOps flow to prevent bad code from being deployed. (367-SonarQube-Server.md)
- The instructor configures ECR and IAM roles for private image registry access used by ArgoCD and CI pipelines; documents role policies and IAM bindings. (368-ECR-IAM.md)
- The instructor sets up GitHub secrets and variables used by CI pipelines and GitOps automation for secure credential storage and templating. (369-GitHub-Secrets-Variables.md)
- The instructor builds a multi-step CI/CD pipeline that builds images, runs tests, pushes artifacts to ECR, and updates manifests stored in Git to trigger GitOps sync. (370-CICD-Pipeline-1.md; 371-CICD-Pipeline-2.md)
- The instructor documents EKS prerequisites and provisions a cluster compatible with ArgoCD and the GitOps model. (372-EKS-Prereqs.md)
- The instructor installs and configures ArgoCD, registers the Git repos, and configures applications to continuously reconcile Git state into the Kubernetes cluster. (374-ArgoCD-Setup.md; 375-Argo-App-Sync.md)
- By the end of this section, a GitOps pipeline exists where CI pipelines build and publish artifacts and ArgoCD continuously reconciles application manifests from Git to the Kubernetes cluster for automated deployments. (Section Summary)

Section: section-32-conclusion
- The instructor collects resume and career guidance artifacts and provides a structured wrap-up of technical deliverables students have built during the course. (378-resumes.md)
- By the end of this section, the course artifacts are summarized and the student has a checklist linking all infrastructure, CI/CD, container, Kubernetes, GitOps, and monitoring deliverables as tangible outcomes of the engineering journey. (Section Summary)

Final note on project continuity and state:
- Across the course, the instructor starts with manual VM and OS-level workflows, converts them into idempotent provisioning using Vagrant and Ansible (Sections 03, 04, 06, 22), then moves to container packaging (Sections 10, 27, 28), produces container images with build tools (Section 16), and wires CI pipelines (Jenkins, GitHub Actions, GitLab) to build/test/publish artifacts (Sections 17, 18, 19). (multiple articles)
- Infrastructure is progressively automated: manual EC2/VPC work becomes Terraform modules (Sections 13, 14, 24, 21), and cloud-native managed services are introduced as part of re-architecting (Section 15) and cloud CI/CD projects (Section 25). (multiple articles)
- Container images produced in containerization sections are the canonical deployment artifacts for Kubernetes, and Helm charts/manifests are prepared and then managed via a GitOps model using ArgoCD (Sections 28, 29, 31). (multiple articles)
- Observability and SRE practices are integrated by instrumenting cloud and cluster workloads with Prometheus/Grafana/Loki and alerting; dashboards and runbooks complete the operational loop. (Section 23)
- By the end of the full course, the instructor has produced: (a) reproducible developer workstation and Vagrant lab environments, (b) Ansible playbooks and Terraform modules to provision cloud/VM infrastructure, (c) build tool configurations that produce artifacts, (d) Dockerfiles and container images stored in registries, (e) CI pipelines across Jenkins/GitHub Actions/GitLab to build, scan, and publish artifacts, (f) Kubernetes manifests and Helm charts, and (g) a GitOps deployment pipeline (ArgoCD) plus monitoring and alerting—forming a complete, automated, observable deployment lifecycle for the vprofile application. (Section Summary)

