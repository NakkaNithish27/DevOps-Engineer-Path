DevOps Career Progress Tracker

Session — Environment Setup & Project Foundation

Started the DevOps career journey by setting up the learning environment required for the roadmap. Installed and configured the necessary development tools and established the base environment that will be used throughout the project. Completed the introductory sections of the course and prepared the local machine for hands-on labs.

Created an AWS account and configured the initial cloud environment. To avoid unexpected costs during experimentation, configured AWS Billing Alarms with SNS email notifications. This provides early alerts whenever account charges exceed predefined thresholds.

Configured a DuckDNS domain to make self-hosted services accessible over the internet. After evaluating different cloud options, decided to use Oracle Cloud Free Tier as the primary environment for future practical work because it provides better long-term value for running always-on DevOps projects while keeping AWS focused on learning AWS-specific services.

This session also established several long-term project decisions. The objective of the roadmap is not simply to finish the course but to become employable as a DevOps Engineer by building practical engineering skills and recruiter-worthy portfolio projects. The roadmap, specification, and execution tracker were adopted as the project's operating documents, with execution progress being tracked separately from the long-term roadmap.

At the end of this session, the development environment, AWS account, billing protection, DuckDNS configuration, and primary cloud strategy were all in place, providing a solid foundation for the remaining sections of the roadmap.

---
Session — Virtualization, Linux Foundation & Git

Completed the virtual development environment by installing and configuring VirtualBox and Vagrant. Established a repeatable local lab environment that can be recreated whenever required, providing a reliable foundation for future multi-machine DevOps projects. Built confidence in using Vagrant for managing virtual machines and provisioning development environments.

Completed the Linux section with a strong emphasis on hands-on practice rather than memorizing commands. Covered the Linux file system, navigation, file manipulation, permissions, users and groups, package management, services, processes, archiving, text processing, and common administration tasks. Repeatedly practiced Linux commands until they became comfortable to use from memory. Self-assessed Linux confidence at approximately 95%, indicating a solid foundation for future DevOps technologies.

Moved on to Git and version control. Learned the complete Git workflow, including repository creation, staging, committing, branching, merging, tags, and remote repository management. Established a professional GitHub profile and completed the initial GitHub branding setup to support future portfolio development. Rather than creating multiple technology-specific repositories immediately, decided to focus on building meaningful engineering projects first and publish repositories only when they demonstrate real-world capability. Self-assessed Git confidence at approximately 89%.

By the end of this phase, a stable virtual lab environment, strong Linux administration skills, and a professional version control workflow were established, forming the technical foundation required for the remaining DevOps roadmap.

---
Session — Infrastructure Automation, Multi-VM Environments, Variables, JSON & YAML

Continued building practical DevOps skills by focusing on development environment automation and configuration management concepts. Used Vagrant to move beyond manually created virtual machines and built reproducible Infrastructure as Code (IaC) environments capable of provisioning complete development setups automatically.

Completed several hands-on implementations, including manual website deployment, WordPress deployment, automated Vagrant provisioning, and a multi-VM environment. Created custom "systemd" services to better understand Linux service management and how applications are managed in production environments. These exercises reinforced the idea that infrastructure should be reproducible rather than manually configured.

Studied variables, JSON, and YAML, gaining an understanding of how structured data is represented and exchanged between modern DevOps tools. Explored Python data structures as part of this section to understand how configuration files and automation scripts interact with structured data formats. Self-assessed confidence at approximately 93% for both JSON/YAML and the Python concepts covered in this section.

Throughout this phase, an important portfolio decision was reinforced: learning notes and small practice exercises would not be published as standalone GitHub repositories. Instead, GitHub would be reserved for projects that demonstrate meaningful engineering capability and are valuable to recruiters. This decision keeps the future portfolio focused on quality over quantity.

By the end of this session, development environment automation, Infrastructure as Code fundamentals, multi-VM provisioning, Linux service management, and structured configuration formats had become part of the core technical foundation, preparing the way for larger deployment projects in the next stage of the roadmap.

---
Session — Section 8 Complete: VProfile Multi-Tier Application Deployment

Completed Section 8 — VProfile Project Setup (Manual & Automated), marking the completion of the first major traditional application deployment project in the DevOps roadmap. This concluded all articles in the section, covering both manual deployment and automated provisioning workflows. 

The completed work established a solid understanding of deploying and operating a traditional multi-tier application stack consisting of Nginx, Tomcat, RabbitMQ, Memcached, and MySQL/MariaDB across separate virtual machines. The session reinforced service lifecycle management with systemd, application packaging and deployment using Maven and WAR files, database initialization and remote access configuration, cache and messaging infrastructure, firewall configuration, deployment validation, and end-to-end request flow through the application stack. Special emphasis was placed on understanding the architecture, service interactions, validation techniques, and common troubleshooting patterns rather than memorizing commands.  

The automation portion demonstrated how the manual deployment process is transformed into reproducible infrastructure using Vagrant provisioning with Bash scripts. The key takeaway was the shift from interactive administration to non-interactive provisioning suitable for Infrastructure as Code. Concepts such as one provisioning script per VM, heredoc usage, shell variables, provisioning lifecycle, and automation-friendly configuration patterns were identified as the primary learning objectives because they form the conceptual foundation for later technologies including Ansible, Terraform, cloud-init, CI/CD pipelines, and Kubernetes bootstrapping. 

Track 2 (Projects & GitHub Evolution) was reviewed after completing the technical work. A deliberate portfolio decision was reaffirmed: no GitHub repositories should be created for this section. Although the VProfile deployment and Vagrant automation provide valuable learning, they are intermediate implementations that will later be superseded by stronger cloud-native projects. All repository ideas related to VProfile deployment, provisioning, architecture documentation, deployment guides, and automation documentation remain intentionally deferred until they become part of larger production-grade projects.

Track 3 (Personal Branding & Communication) reached the same conclusion. No LinkedIn posts, technical articles, project walkthroughs, or public-facing communication assets should be published at this stage. Professional communication will remain deferred until complete engineering solutions involving Docker, cloud infrastructure, Infrastructure as Code, Kubernetes, CI/CD, and GitOps can be presented as cohesive portfolio projects.

With Section 8 complete, the roadmap is ready to continue into Section 9 — Networking, followed by Section 10 — Introducing Containers, before performing the Iteration 4 interview readiness assessment and updating the project progress tracker.  

---




















