# Monitoring and Observability — The Foundation of Reliability (Introduction)

**Source:** Video caption file — *"Introduction to Monitoring and Observability"*, with supplementary presentation slides and restaurant analogy reference table [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt), [\[250.Intro_...ervability \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250.Intro_to_Monitoring_and_Observability.pdf), [\[250.Monito...nt+Analogy \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7BFA1783BE-732E-4551-BF6A-CAB9468D2DFB%7D&file=250.Monitoring%2BLayers%2BExplained%2Bwith%2Ba%2BRestaurant%2BAnalogy.xlsx&action=default&mobileredirect=true)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — Why Monitoring Exists

The instructor begins with a personal experience: "When I started my career we used to monitor systems to see the future. Actually the future problems." This is the foundational purpose of monitoring — not just observing the present state of systems, but **detecting problems before they impact users**. [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

The concrete example: a server receives a heavy load of computing requests. Without monitoring, it keeps running until it crashes — users experience downtime, the team scrambles reactively. With monitoring, you get a notification **before** the CPU even reaches 80%. You see the trend, you recognize the trajectory, and you **scale out before the problem materializes**. The problem is prevented, not fixed after the fact. [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

The business impact is stated bluntly: "User is happy, client is happy, and bank account is also happy." Monitoring ensures **reliability and uptime** — the core operational promise of any production system. [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

But the video immediately expands beyond this traditional view: "In today's time, monitoring is not just limited to this much." Modern monitoring is also about **collecting the right amount of data, performing proper data analysis, understanding market trends, and making business decisions** based on that data. Monitoring has evolved from a purely technical, operations-focused activity into a strategic tool that informs business decisions. [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

***

## 1.2 — Core Concepts: Metrics, Time Series, Exporters, and Monitoring Models

Before diving into the types of monitoring, the video establishes four foundational concepts using a medical analogy that makes each concept immediately tangible. [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

### Metrics (also called Checks)

A metric is a **measurement of a specific property** of a system. The analogy: a thermometer is a metric for temperature. It measures one specific thing and gives you a reading. In software systems, metrics are measurements like CPU utilization percentage, page load time in milliseconds, number of requests per second, error rate, disk usage. Each metric measures one specific aspect of system health. The video notes that metrics are "sometimes also called checks" — the same concept, different terminology. [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

### Time Series

When you record a metric at regular intervals over time, you create a **time series** — a sequence of data points indexed by time. The analogy: recording a patient's temperature every two hours creates a time series table. You can see when the temperature spikes, when it drops, and correlate those changes with events (medication administered, activity changes). [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

In systems monitoring, time series data is the foundation of everything. CPU usage recorded every 15 seconds, request latency recorded every minute, error count recorded every 5 minutes — these are all time series. The power of time series is that it reveals **trends** — you don't just see the current value, you see how it's changing over time, which lets you predict future behavior (the "seeing the future" the instructor mentioned). [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

### Exporters (also called Agents)

An exporter is the component that **makes metrics available** for collection. The analogy: a display window outside a patient's room that shows their temperature readings. The temperature reading is "exported" out of the room so it can be watched continuously from outside. [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

In software systems, an exporter is a piece of software that runs on or alongside the monitored system, collects metrics from it, and makes those metrics available for the monitoring server to consume. The video notes the alternate name: "Exporters are also called as agents." Both terms refer to the same concept — the component that bridges the monitored system and the monitoring infrastructure. [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

### Pull Model vs. Push Model

There are two fundamentally different approaches to how metrics get from the monitored system to the monitoring server. [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

**Push model:** The monitored system actively **sends** its metrics to the monitoring server. Analogy: the patient calling the doctor or going to the doctor. The initiative comes from the monitored side.

**Pull model:** The monitoring server actively **connects to** the monitored system and **fetches** the metrics. Analogy: the doctor visiting the patient. The initiative comes from the monitoring side. [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

This distinction matters because different monitoring tools use different models. Prometheus (which will be used in the hands-on section) uses the **pull model** — it connects to exporters on target systems and scrapes their metrics at regular intervals. Other tools use push models. The architectural implications are significant: pull models require the monitoring server to know where all targets are and be able to reach them; push models require the monitored systems to know where the monitoring server is and be able to send data to it. [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

***

## 1.3 — The Seven Layers of Monitoring

Monitoring is not a single activity — it's organized into **seven distinct layers**, each focusing on a different aspect of the system. Understanding these layers is essential because each answers a different question, uses different metrics, and often requires different tools. [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt), [\[250.Intro_...ervability \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250.Intro_to_Monitoring_and_Observability.pdf)

The video uses a **restaurant analogy** throughout to make each layer intuitive. A downloadable reference table maps each layer to its restaurant equivalent, software equivalent, key metrics, and common tools. [\[250.Monito...nt+Analogy \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7BFA1783BE-732E-4551-BF6A-CAB9468D2DFB%7D&file=250.Monitoring%2BLayers%2BExplained%2Bwith%2Ba%2BRestaurant%2BAnalogy.xlsx&action=default&mobileredirect=true)

***

### Layer 1: Browser / Frontend Monitoring

**What it monitors:** The **actual user's experience** — what happens on the user's side when they interact with your application. How fast the page loads, how quickly the UI responds to clicks, whether JavaScript errors occur, how navigation feels. [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

**Restaurant analogy:** The customer experience at the table — how quickly they get the menu, how responsive the waiter is. This is the **first impression**, the direct user-facing experience. [\[250.Monito...nt+Analogy \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7BFA1783BE-732E-4551-BF6A-CAB9468D2DFB%7D&file=250.Monitoring%2BLayers%2BExplained%2Bwith%2Ba%2BRestaurant%2BAnalogy.xlsx&action=default&mobileredirect=true)

**Key metrics:** Page Load Time, Time to First Byte (TTFB), First Contentful Paint (FCP), Core Web Vitals (LCP, FID, CLS), JavaScript Errors, User Navigation & Clicks, Click Response Time. [\[250.Intro_...ervability \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250.Intro_to_Monitoring_and_Observability.pdf), [\[250.Monito...nt+Analogy \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7BFA1783BE-732E-4551-BF6A-CAB9468D2DFB%7D&file=250.Monitoring%2BLayers%2BExplained%2Bwith%2Ba%2BRestaurant%2BAnalogy.xlsx&action=default&mobileredirect=true)

**Example from the slides:** "Track checkout page load time for users in India" — measuring real user experience from a specific geographic region. [\[250.Intro_...ervability \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250.Intro_to_Monitoring_and_Observability.pdf)

**Common tools:** Datadog RUM (Real User Monitoring), New Relic Browser, Sentry, Pingdom RUM, Google Lighthouse, Grafana Faro. [\[250.Monito...nt+Analogy \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7BFA1783BE-732E-4551-BF6A-CAB9468D2DFB%7D&file=250.Monitoring%2BLayers%2BExplained%2Bwith%2Ba%2BRestaurant%2BAnalogy.xlsx&action=default&mobileredirect=true), [\[250.Intro_...ervability \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250.Intro_to_Monitoring_and_Observability.pdf)

The video clarifies the boundary: "Front end or browser is the user experience — where the user clicks, login, whatever the user sees on the browser or on the app. But what happens behind the scene" is the next layer (APM). [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

***

### Layer 2: Application Performance Monitoring (APM)

**What it monitors:** What happens **behind the scenes** — the backend code, APIs, database queries, service-to-service communication. When a user clicks a button, the frontend sends an API request. That request hits the backend, queries a database, possibly calls other services. APM monitors **all of that internal processing**. [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

**Restaurant analogy:** Kitchen operations — how fast the chefs cook, any delays between steps, and who's causing bottlenecks. The customer doesn't see the kitchen, but kitchen performance directly determines their experience. [\[250.Monito...nt+Analogy \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7BFA1783BE-732E-4551-BF6A-CAB9468D2DFB%7D&file=250.Monitoring%2BLayers%2BExplained%2Bwith%2Ba%2BRestaurant%2BAnalogy.xlsx&action=default&mobileredirect=true)

**The video specifies what "application" means here:** "Application here means the services like MySQL, Node.js, Tomcat, Apache, etc." It's not the user-facing application — it's the backend services that power it. [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

**Key metrics:** Response Time, Throughput (Requests Per Second), Error Rate, Database Query Performance, External API Latency, End-to-End Tracing (following a request through multiple services), Apdex Score, Trace Duration. [\[250.Intro_...ervability \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250.Intro_to_Monitoring_and_Observability.pdf), [\[250.Monito...nt+Analogy \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7BFA1783BE-732E-4551-BF6A-CAB9468D2DFB%7D&file=250.Monitoring%2BLayers%2BExplained%2Bwith%2Ba%2BRestaurant%2BAnalogy.xlsx&action=default&mobileredirect=true)

**Example from the slides:** "Trace API latency from NGINX → Java → MySQL" — following a single request through the entire backend stack to find where delays occur. [\[250.Intro_...ervability \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250.Intro_to_Monitoring_and_Observability.pdf)

**Common tools:** New Relic, Datadog APM, AppDynamics ("I've seen this a lot"), Dynatrace ("in today's time is the best monitoring and observability tool, I would say. Again, it's debatable, but that is enterprise. Dynatrace is not free. We get a 15-day trial"), Elastic APM. [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt), [\[250.Intro_...ervability \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250.Intro_to_Monitoring_and_Observability.pdf)

**The relationship to frontend monitoring:** "If these things are measured, the user experience can be improved drastically in real time. You will know how your application is performing and what is the problem. Once you find that through monitoring you can fix that and user will be happy." APM is the diagnostic layer that explains **why** the frontend experience is good or bad. [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

***

### Layer 3: Infrastructure Monitoring

**What it monitors:** The **compute resources** — servers, containers, cloud resources. CPU, memory, disk, network throughput, system uptime, pod/container status in Kubernetes. This is the most traditional and foundational layer of monitoring. [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

**Restaurant analogy:** Kitchen equipment and staff health — how hot the stove is, how much gas is left, whether fridges are overloaded. The infrastructure that everything runs on. [\[250.Monito...nt+Analogy \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7BFA1783BE-732E-4551-BF6A-CAB9468D2DFB%7D&file=250.Monitoring%2BLayers%2BExplained%2Bwith%2Ba%2BRestaurant%2BAnalogy.xlsx&action=default&mobileredirect=true)

**The video calls this "the most common one, the first one that we should set up."** Before you monitor application performance or user experience, you need to know if the underlying infrastructure is healthy. [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

**Key metrics:** CPU / Memory Usage, Disk I/O, Network Latency, Node Uptime, Pod/Container Status (Kubernetes). [\[250.Monito...nt+Analogy \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7BFA1783BE-732E-4551-BF6A-CAB9468D2DFB%7D&file=250.Monitoring%2BLayers%2BExplained%2Bwith%2Ba%2BRestaurant%2BAnalogy.xlsx&action=default&mobileredirect=true)

**Example from the slides:** "Alert when EC2 CPU > 90% for 5 minutes." [\[250.Intro_...ervability \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250.Intro_to_Monitoring_and_Observability.pdf)

**Common tools:** The video provides a historical perspective: "I started from Nagios. After that we used many different tools, but Nagios and Zabbix are the ones that stayed for a very long time." Then: Datadog Infra, CloudWatch (already seen in the course), and **Prometheus and Grafana** — "that we will be seeing in this section." [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

The video makes an important statement about Prometheus and Grafana: "Prometheus and Grafana can monitor almost anything. Everything that we are seeing in this lecture, except few things, but that can be also monitored with Prometheus and Grafana." This positions them as the Swiss-army-knife tools of the monitoring ecosystem. [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

***

### Layer 4: Synthetic Monitoring

**What it monitors:** **Simulated user actions** to test uptime and performance proactively — even when no real users are active. [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

**Restaurant analogy:** Mystery diners or test customers — people who periodically visit the restaurant to check service quality even when no real customers are there. The video adds a cultural reference: "If you have seen the movie Ratatouille... a periodic check to the restaurant to check the service quality." [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt), [\[250.Monito...nt+Analogy \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7BFA1783BE-732E-4551-BF6A-CAB9468D2DFB%7D&file=250.Monitoring%2BLayers%2BExplained%2Bwith%2Ba%2BRestaurant%2BAnalogy.xlsx&action=default&mobileredirect=true)

**What makes it different from frontend monitoring:** Frontend/RUM monitoring measures **real** users. Synthetic monitoring uses **simulated/fake** users. Synthetic monitoring runs continuously on a schedule, whether real users are active or not. This means you can detect problems at 3 AM when no real users are on the system — before the morning traffic spike hits a broken system. [\[250.Intro_...ervability \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250.Intro_to_Monitoring_and_Observability.pdf)

**Types:** Availability Checks (HTTP 200 responses), Transaction Flows (simulating Login → Checkout), API Endpoint Testing. [\[250.Intro_...ervability \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250.Intro_to_Monitoring_and_Observability.pdf)

**Example from the slides:** "Simulate user login from Mumbai and London every 10 minutes." [\[250.Intro_...ervability \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250.Intro_to_Monitoring_and_Observability.pdf)

**Key metrics:** Uptime, Response Time, Transaction Success Rate. [\[250.Monito...nt+Analogy \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7BFA1783BE-732E-4551-BF6A-CAB9468D2DFB%7D&file=250.Monitoring%2BLayers%2BExplained%2Bwith%2Ba%2BRestaurant%2BAnalogy.xlsx&action=default&mobileredirect=true)

**Common tools:** Pingdom, Checkly, Datadog Synthetics, CloudWatch Canaries, UptimeRobot, Grafana Synthetic Monitoring. [\[250.Monito...nt+Analogy \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7BFA1783BE-732E-4551-BF6A-CAB9468D2DFB%7D&file=250.Monitoring%2BLayers%2BExplained%2Bwith%2Ba%2BRestaurant%2BAnalogy.xlsx&action=default&mobileredirect=true), [\[250.Intro_...ervability \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250.Intro_to_Monitoring_and_Observability.pdf)

***

### Layer 5: Business / KPI Monitoring

**What it monitors:** **Business performance metrics** — not technical health, but business outcomes. How many signups per minute, conversion rates, revenue, failed payments, daily active users, customer satisfaction. [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

**Restaurant analogy:** The restaurant manager's dashboard — total orders, revenue, repeat customers, customer satisfaction. The manager doesn't care about stove temperature; they care about how many dishes were sold and whether customers are coming back. [\[250.Monito...nt+Analogy \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7BFA1783BE-732E-4551-BF6A-CAB9468D2DFB%7D&file=250.Monitoring%2BLayers%2BExplained%2Bwith%2Ba%2BRestaurant%2BAnalogy.xlsx&action=default&mobileredirect=true)

The instructor adds a personal note: "I use this for my own business — conversion rate, like how many people visit and how many actually sign up." This grounds the concept in real usage. [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

**Key metrics:** Signups per minute, Conversion Rate, Failed Payments, Daily Active Users, Revenue per hour, Average order value. [\[250.Intro_...ervability \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250.Intro_to_Monitoring_and_Observability.pdf), [\[250.Monito...nt+Analogy \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7BFA1783BE-732E-4551-BF6A-CAB9468D2DFB%7D&file=250.Monitoring%2BLayers%2BExplained%2Bwith%2Ba%2BRestaurant%2BAnalogy.xlsx&action=default&mobileredirect=true)

**Example from the slides:** "Alert when checkout success < 95%." [\[250.Intro_...ervability \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250.Intro_to_Monitoring_and_Observability.pdf)

**Common tools:** Mixpanel, Amplitude, Google Analytics, Datadog Custom Metrics, Power BI, Looker. Some organizations build custom tools for their specific KPI needs. [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt), [\[250.Monito...nt+Analogy \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7BFA1783BE-732E-4551-BF6A-CAB9468D2DFB%7D&file=250.Monitoring%2BLayers%2BExplained%2Bwith%2Ba%2BRestaurant%2BAnalogy.xlsx&action=default&mobileredirect=true)

***

### Layer 6: Log Monitoring

**What it monitors:** The **event logs** generated by systems, services, and applications. User access logs, API query logs, MySQL query logs, application events, error messages — all the textual records of what happened and when. [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

**Restaurant analogy:** The restaurant logbook — notes of issues, complaints, and actions taken ("table 4 complained", "oven restarted"). [\[250.Monito...nt+Analogy \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7BFA1783BE-732E-4551-BF6A-CAB9468D2DFB%7D&file=250.Monitoring%2BLayers%2BExplained%2Bwith%2Ba%2BRestaurant%2BAnalogy.xlsx&action=default&mobileredirect=true)

The video makes a critical distinction: **"Logging will be just keeping the log. Monitoring those logs or looking at those logs and understanding stuff will be log monitoring."** Logging and log monitoring are not the same thing. Logging is the act of writing events to files. Log monitoring is the act of systematically analyzing those files to detect errors, debug issues, and identify trends. [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

**Key metrics:** Error Frequency, Request Logs (status codes), Authentication Failures, Audit Trails, System Events. [\[250.Intro_...ervability \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250.Intro_to_Monitoring_and_Observability.pdf), [\[250.Monito...nt+Analogy \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7BFA1783BE-732E-4551-BF6A-CAB9468D2DFB%7D&file=250.Monitoring%2BLayers%2BExplained%2Bwith%2Ba%2BRestaurant%2BAnalogy.xlsx&action=default&mobileredirect=true)

**Example from the slides:** "Detect spike in TimeoutException logs after deployment." [\[250.Intro_...ervability \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250.Intro_to_Monitoring_and_Observability.pdf)

**Common tools:** ELK Stack (Elasticsearch, Logstash, Kibana), Loki + Grafana ("that we will be seeing in this section"), Splunk ("very famous name in this category"), CloudWatch Logs. [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt), [\[250.Monito...nt+Analogy \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7BFA1783BE-732E-4551-BF6A-CAB9468D2DFB%7D&file=250.Monitoring%2BLayers%2BExplained%2Bwith%2Ba%2BRestaurant%2BAnalogy.xlsx&action=default&mobileredirect=true)

***

### Layer 7: Security Monitoring

**What it monitors:** **Threats, unauthorized access, and security vulnerabilities**. Suspicious IPs, privilege escalation events, intrusion detection, vulnerability scanning. [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

**Restaurant analogy:** The security guard and CCTV — watching for suspicious behavior, theft, or break-ins. [\[250.Monito...nt+Analogy \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7BFA1783BE-732E-4551-BF6A-CAB9468D2DFB%7D&file=250.Monitoring%2BLayers%2BExplained%2Bwith%2Ba%2BRestaurant%2BAnalogy.xlsx&action=default&mobileredirect=true)

The video notes that this is typically handled by a **dedicated team**: "This will be done mostly by a separate security team, or there will be a SOC team, NOC team that will be dedicatedly working on this one." The cybersecurity team often has their own specialized tools, including penetration testing tools. [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

**Key metrics:** Unauthorized Access Attempts, IAM Anomalies, Intrusion Detection, Failed Logins, Firewall Breaches, Vulnerability Alerts. [\[250.Intro_...ervability \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250.Intro_to_Monitoring_and_Observability.pdf), [\[250.Monito...nt+Analogy \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7BFA1783BE-732E-4551-BF6A-CAB9468D2DFB%7D&file=250.Monitoring%2BLayers%2BExplained%2Bwith%2Ba%2BRestaurant%2BAnalogy.xlsx&action=default&mobileredirect=true)

**Common tools:** AWS GuardDuty, Datadog Security, Splunk Security, Wazuh, CrowdStrike, Falco, Grafana Alloy. [\[250.Monito...nt+Analogy \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7BFA1783BE-732E-4551-BF6A-CAB9468D2DFB%7D&file=250.Monitoring%2BLayers%2BExplained%2Bwith%2Ba%2BRestaurant%2BAnalogy.xlsx&action=default&mobileredirect=true), [\[250.Intro_...ervability \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250.Intro_to_Monitoring_and_Observability.pdf)

***

## 1.4 — A Note on Tools and Metrics

The video delivers an important framing about tools and metrics that prevents the wrong learning approach: **"You don't need to memorize these things. This is just information so you understand different kinds of monitoring."** [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

The instructor elaborates from experience: "I have worked on several projects and I have seen many different monitoring and observability tools, different requirements, different use cases, different monitoring tool. Some use open source, some use enterprise versions. It's all based on requirement and also of course the budget." [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

The takeaway: understand the **categories** and what each layer monitors. The specific tools and metrics are project-dependent. Don't memorize tool lists — understand the monitoring landscape. [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

***

## 1.5 — The Four Pillars of Observability

After covering the seven monitoring layers, the video introduces **observability** — a concept that goes beyond monitoring. The distinction: monitoring tells you **what** is happening (or what went wrong). Observability tells you **why** it happened. [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt), [\[250.Intro_...ervability \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250.Intro_to_Monitoring_and_Observability.pdf)

Observability rests on four pillars (originally three, with a fourth added recently). These are attributed to Google: [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

### Pillar 1: Metrics

Metrics tell you **if** anything is wrong. CPU spikes, disk filling up, error rate increasing, user experience degrading — metrics are the first signal that something is off. They answer the question: "Is there a problem?" [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

### Pillar 2: Logs

Logs tell you **why** something went wrong. A user request failed, a query timed out, a service threw an exception — the log entry contains the details of what happened. A metric might show an error rate spike; the corresponding logs show the specific errors causing the spike. [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

### Pillar 3: Traces

Traces tell you **where** it went wrong. When a user clicks something, the request may travel through multiple services — load balancer → web server → application server → database → cache → back. A trace follows the entire journey of a single request across all these components and shows exactly where the delay or failure occurred. [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

### Pillar 4: Events (Recently Added)

Events tell you **what changed**. An application code deployment, an infrastructure configuration change, a scaling event — if you're monitoring changes/events, you can correlate them with problems. "Due to that, all these things happened." This is the newest pillar and connects operational changes to their consequences. [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

The formula from the slides: **Observability = Metrics + Logs + Traces + Events**. [\[250.Intro_...ervability \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250.Intro_to_Monitoring_and_Observability.pdf)

🔍 **Deep Dive:**
The relationship between the four pillars forms a diagnostic workflow: Metrics **detect** that something is wrong → Logs **explain** why it went wrong → Traces **locate** where in the request chain it went wrong → Events **identify** what change caused it to go wrong. Together, they provide complete diagnostic coverage. Individually, each pillar gives partial information. This is why modern observability tools (OpenTelemetry, Grafana Stack, Datadog, New Relic) aim to integrate all four into a unified platform. [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt), [\[250.Intro_...ervability \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250.Intro_to_Monitoring_and_Observability.pdf)

***

## 1.6 — The Four Golden Signals (Google SRE)

The video introduces four specific metrics — called the **Four Golden Signals** — given by Google's SRE (Site Reliability Engineering) practice. These are the four key metrics considered most critical for monitoring the health of any system: [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

**Latency** — How long it takes for a user to get served. "User trying to make a payment — how long it is taking or how quickly it is happening, if there is any failure." Latency measures the responsiveness of the system from the user's perspective.

**Traffic** — How many users or requests are hitting the system. "A system under pressure or not under pressure." Traffic measures the demand on the system.

**Errors** — Whether anything is failing. "Either it could be something that the user is experiencing or some internal failures that you see in the logs." Errors measure the correctness of the system's responses.

**Saturation** — How full or busy the system is. "You can find out the limit of the system — like disk capacity, CPU utilizations." Saturation measures how close the system is to its capacity limits. [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

These four signals provide a **minimum viable monitoring** framework: if you monitor nothing else, monitor these four, and you'll have a basic understanding of your system's health. [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Learning

This is a **conceptual introduction lecture** — hands-on tool setup (Prometheus, Grafana, Loki) begins in subsequent lectures. The practical value of this lecture is building the mental framework that makes tool usage purposeful rather than mechanical. However, the video establishes several practically actionable items and references. [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

***

## Practical Reference Materials

### Downloadable Restaurant Analogy Table

The video explicitly instructs: "I have created this table. You can download it from this lecture resource." The table maps all seven monitoring layers to their restaurant analogy, software equivalent, key metrics, and example tools. [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt), [\[250.Monito...nt+Analogy \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7BFA1783BE-732E-4551-BF6A-CAB9468D2DFB%7D&file=250.Monitoring%2BLayers%2BExplained%2Bwith%2Ba%2BRestaurant%2BAnalogy.xlsx&action=default&mobileredirect=true)

**How to use it:** This table is a **quick reference** for understanding which monitoring layer addresses which concern. When you encounter a monitoring question in a real project ("we need to track API latency" → that's APM; "we need to know if the site is up at 3 AM" → that's Synthetic Monitoring), the table maps you to the right category instantly.

***

## Practical Decision Framework: Which Layer Comes First?

The video provides a clear prioritization: **Infrastructure monitoring is "the most common one, the first one that we should set up."** Before monitoring application performance, user experience, or business KPIs, ensure the underlying compute resources (CPU, memory, disk, network) are monitored. You can't diagnose application problems if you don't know whether the server itself is healthy. [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

***

## Tool Selection Guidance

The video provides practical guidance on how monitoring tools are chosen in real projects: [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

**It depends on:**

* Project requirements — different projects have different monitoring needs.
* Use case — what specifically you need to monitor determines the tool.
* Budget — enterprise tools (Dynatrace, Datadog, Splunk) cost money; open-source tools (Prometheus, Grafana, Loki, ELK) are free but require operational effort to run.

**What's coming next in the course:** Prometheus (infrastructure metrics), Grafana (visualization/dashboards), and Loki (log monitoring). The video confirms: "Prometheus and Grafana can monitor almost anything." [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

**Dynatrace note:** The instructor calls Dynatrace "the best monitoring and observability tool" (enterprise, not free, 15-day trial available). This is positioned as a "debatable" opinion but grounded in experience. [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

**Historical context:** The instructor's tool journey — started with Nagios, then Zabbix ("stayed for a very long time"), then CloudWatch (already covered in the course), now Prometheus + Grafana. This gives a practical timeline of how the monitoring tool landscape has evolved. [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

***

## What to Expect Next

The video sets up the learning path: [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

1. **Next lecture:** "Why DevOps should learn monitoring and observability" — the role-specific justification.
2. **Following lectures:** Hands-on with Prometheus, Grafana, Loki — actual tool setup and configuration.
3. **Recommended revisit:** "You can again watch or revisit this lecture after you complete this section" — the theory will make more sense after hands-on experience.

⚠️ **Expert Note:**
The video's practical advice on not memorizing tool names and metrics is critical for career longevity. The monitoring landscape changes every few years — Nagios → Zabbix → Prometheus is just one evolution path. Understanding the **categories** (what to monitor and why) is permanent knowledge; tool-specific skills are temporary and must be updated regularly. [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## System Identity

```
TOPIC:    Monitoring and Observability — Introduction
PURPOSE:  Understand WHAT to monitor, WHY, and the conceptual framework
CONTEXT:  Theory lecture before hands-on with Prometheus, Grafana, Loki
SCOPE:    Concepts, layers, pillars, golden signals — NO tool setup yet
```

 [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

***

## Core Concepts (Foundation)

```
CONCEPT         ANALOGY                    IN SOFTWARE
──────────      ───────                    ───────────
Metric/Check    Thermometer reading        CPU %, page load time, error rate
Time Series     Temperature log over time  Metric values recorded at intervals
Exporter/Agent  Display outside room       Software that exposes metrics for collection
Pull Model      Doctor visits patient      Monitoring server fetches from targets (Prometheus)
Push Model      Patient calls doctor       Targets send metrics to monitoring server
```

 [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

***

## Seven Layers of Monitoring

```
LAYER                RESTAURANT ANALOGY              MONITORS                   FIRST SETUP?
─────                ──────────────────              ────────                   ────────────
1. Browser/Frontend  Customer at table               User experience (RUM)      -
2. APM               Kitchen operations              Backend code, APIs, DB     -
3. Infrastructure    Kitchen equipment & staff        CPU, memory, disk, network ✅ FIRST
4. Synthetic         Mystery diner (test customer)    Simulated uptime checks    -
5. Business/KPI      Manager dashboard               Revenue, signups, trends   -
6. Log               Restaurant logbook               Error logs, events, audit  -
7. Security          Security guard & CCTV            Threats, unauthorized access -

PRIORITY: Infrastructure first → then expand outward
```

 [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt), [\[250.Monito...nt+Analogy \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7BFA1783BE-732E-4551-BF6A-CAB9468D2DFB%7D&file=250.Monitoring%2BLayers%2BExplained%2Bwith%2Ba%2BRestaurant%2BAnalogy.xlsx&action=default&mobileredirect=true)

***

## Layer Relationship Map

```
USER SIDE:
  Layer 1 (Browser)    → What the USER sees/feels
  Layer 4 (Synthetic)  → What a SIMULATED user sees/feels

BACKEND SIDE:
  Layer 2 (APM)        → What the APPLICATION does internally
  Layer 3 (Infra)      → What the HARDWARE/OS does underneath

DATA SIDE:
  Layer 6 (Logs)       → What EVENTS were recorded
  Layer 7 (Security)   → What THREATS were detected

BUSINESS SIDE:
  Layer 5 (KPI)        → What the BUSINESS outcome is

DIAGNOSTIC FLOW:
  User reports slowness (Layer 1)
    → Check backend (Layer 2) → API latency found
      → Check infra (Layer 3) → CPU at 95%
        → Check logs (Layer 6) → memory leak detected
          → Check events → deployment 2hrs ago caused it
```

 [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

***

## Four Pillars of Observability

```
PILLAR       ANSWERS            ANALOGY
──────       ───────            ───────
Metrics      IS something wrong?    Thermometer shows fever
Logs         WHY is it wrong?       Doctor's notes explain cause
Traces       WHERE did it go wrong? X-ray shows exact location
Events       WHAT CHANGED?          "Patient ate something new"

FORMULA: Observability = Metrics + Logs + Traces + Events

MONITORING vs. OBSERVABILITY:
  Monitoring → WHAT happened
  Observability → WHY it happened
```

 [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt), [\[250.Intro_...ervability \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250.Intro_to_Monitoring_and_Observability.pdf)

***

## Four Golden Signals (Google SRE)

```
SIGNAL       QUESTION                           EXAMPLE
──────       ────────                           ───────
Latency      How LONG does it take?             Payment takes 5s vs 200ms
Traffic      How MUCH demand is there?          1000 RPS vs 100 RPS
Errors       Is anything FAILING?               5xx errors, failed queries
Saturation   How FULL/BUSY is the system?       CPU 95%, disk 90%

MINIMUM VIABLE MONITORING: Monitor these 4 → basic system health covered
```

 [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

***

## Tool Landscape (Reference, Don't Memorize)

```
LAYER              OPEN SOURCE                    ENTERPRISE
─────              ───────────                    ──────────
Browser/Frontend   Grafana Faro, Sentry           Datadog RUM, New Relic
APM                Grafana Tempo, Jaeger           Datadog APM, Dynatrace, AppDynamics
Infrastructure     Prometheus + Grafana, Zabbix    CloudWatch, Datadog Infra
Synthetic          Grafana Synthetic               Pingdom, Checkly, Datadog
Business/KPI       Grafana                         Mixpanel, Google Analytics
Logs               Loki + Grafana, ELK Stack       Splunk, CloudWatch Logs
Security           Wazuh, Falco                    GuardDuty, CrowdStrike

SWISS-ARMY KNIFE: Prometheus + Grafana = "can monitor almost anything"
BEST ENTERPRISE (per instructor): Dynatrace (not free, 15-day trial)
HISTORICAL: Nagios → Zabbix → CloudWatch → Prometheus+Grafana

COURSE TOOLS: Prometheus, Grafana, Loki (hands-on in next lectures)
```

 [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt), [\[250.Monito...nt+Analogy \| Excel\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/_layouts/15/Doc.aspx?sourcedoc=%7BFA1783BE-732E-4551-BF6A-CAB9468D2DFB%7D&file=250.Monitoring%2BLayers%2BExplained%2Bwith%2Ba%2BRestaurant%2BAnalogy.xlsx&action=default&mobileredirect=true)

***

## Logging vs. Log Monitoring

```
LOGGING:        Writing events to text files (the ACT of recording)
LOG MONITORING: Analyzing those files for errors, trends, debugging (the ACT of watching)

"Logging will be just keeping the log.
 Monitoring those logs will be log monitoring."
```

 [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

***

## Pull vs. Push Model

```
PULL MODEL:                              PUSH MODEL:
  Monitoring server → connects to target   Target → sends data to monitoring server
  Doctor visits patient                    Patient goes to doctor
  Prometheus uses this model               Other tools use this

ARCHITECTURAL IMPLICATION:
  Pull: Server must know all targets + reach them
  Push: Targets must know server address + send to it
```

 [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

***

## Tool Selection Decision Framework

```
CHOOSE BASED ON:
  ├── Project requirements (what to monitor)
  ├── Use case (specific monitoring need)
  ├── Budget (open source vs. enterprise)
  └── Team (security team has own tools)

DON'T: Memorize tool lists
DO:    Understand categories → pick tools per project
```

 [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

***

## Reusable Engineering Patterns

| Pattern                                        | Manifestation                                                                        |
| ---------------------------------------------- | ------------------------------------------------------------------------------------ |
| **Layered Monitoring Architecture**            | Seven distinct layers, each monitoring a different system aspect                     |
| **Predictive Detection**                       | Monitor trends to see future problems before they impact users                       |
| **Pull vs. Push Collection**                   | Two architectural models for metric collection, each with tradeoffs                  |
| **Diagnostic Cascade**                         | Metrics → Logs → Traces → Events = complete root cause analysis                      |
| **Minimum Viable Monitoring (Golden Signals)** | Latency + Traffic + Errors + Saturation = baseline health                            |
| **Separation of Concerns**                     | Each monitoring layer has distinct ownership (DevOps vs. Security team vs. Business) |
| **Category Over Tool**                         | Understand monitoring categories permanently; tools change per project/era           |
| **Infrastructure First**                       | Monitor compute resources before anything else — foundation of all layers            |

 [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt)

***

## One-Line System Reconstruction

> **Monitoring uses metrics (checks) collected as time series via exporters (agents) in pull or push models across seven layers (Browser → APM → Infrastructure → Synthetic → Business/KPI → Logs → Security), with observability adding the "why" through four pillars (Metrics + Logs + Traces + Events), measured by Google SRE's four golden signals (Latency, Traffic, Errors, Saturation) — where infrastructure monitoring comes first, Prometheus + Grafana can cover almost everything, and tool selection is always project/budget-dependent.** [\[250-introd...monitoring \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250-introduction-to-monitoring.txt), [\[250.Intro_...ervability \| PDF\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/250.Intro_to_Monitoring_and_Observability.pdf)

***

This completes the full reconstruction of the Monitoring and Observability Introduction lecture. It establishes the conceptual framework that all subsequent hands-on lectures (Prometheus, Grafana, Loki) will build upon — each tool maps to specific layers and pillars covered here. The next lecture covers why DevOps specifically should learn monitoring and observability. Let me know if you'd like any section expanded or adjusted! 🚀
