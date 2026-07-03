# Manual Virtual Machine Setup with Oracle VirtualBox

### CentOS Stream 9 & Ubuntu 22 Server Installation Guide

*Reconstructed from video lecture captions* [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 — Hardware Virtualization and the BIOS Foundation

A virtual machine is a software-emulated computer that runs inside your physical computer. But this emulation cannot happen purely in software — it needs direct support from your CPU's hardware. This hardware-level support is called **hardware virtualization**, and it is controlled by a setting buried inside your computer's **BIOS** (Basic Input/Output System). The BIOS is firmware that runs *before* your operating system loads — it is the lowest layer of your machine's configuration. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

The setting you need to enable goes by several names depending on your hardware manufacturer: **VTx**, **Intel Virtualization Technology**, **Secure Virtual Machine**, or simply **Virtualization**. All of these refer to the same underlying CPU feature — they instruct the processor to allow a hypervisor (like VirtualBox) to create and manage virtual CPUs. Without this enabled, VirtualBox can only create 32-bit VMs, not 64-bit VMs. This is actually a reliable diagnostic signal: if you only see "32-bit" options when creating a VM in VirtualBox, it means virtualization is not enabled in your BIOS. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

To access the BIOS, you press a specific key during the boot sequence — before the OS loads. The key varies by manufacturer: **F2**, **F12**, **Delete**, or **Escape** are common. You must find the correct key for your specific hardware (HP, Lenovo, Dell, etc.), enable the virtualization setting, then **save and exit** the BIOS. The computer will reboot with virtualization now active at the hardware level. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

> 🔍 **Deep Dive**
> The reason this must be a BIOS setting rather than an OS setting is architectural: virtualization extensions (Intel VT-x or AMD-V) operate at the CPU instruction set level. The hypervisor needs to intercept and manage privileged CPU instructions issued by guest operating systems. This interception must be enabled before any operating system loads, which is why it exists in firmware, not in Windows settings.

***

## 1.2 — Conflicting Windows Hypervisor Features

Even after enabling hardware virtualization in the BIOS, Windows may still interfere. This is because Windows has its own built-in hypervisor technologies that **compete** with VirtualBox for control of the CPU's virtualization extensions. Only one hypervisor can own the CPU's virtualization layer at a time. If Windows' own hypervisor is active, VirtualBox cannot function correctly. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

The features that must be **disabled** through "Turn Windows features on or off" (accessible via the Start menu search) are:

* **Microsoft Hyper-V** / **Windows Hypervisor Platform** — Microsoft's own virtualization platform
* **Windows Subsystem for Linux (WSL)** — uses a lightweight VM internally
* **Virtual Machine Platform** — the underlying platform for WSL2 and other features
* **Docker Desktop** — if installed, it uses Hyper-V or WSL2 backend [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

All of these must be unchecked, then you click OK and **reboot**. The critical insight here is that these are not just "nice to have" disables — if any of them remain active, VirtualBox will encounter errors because the CPU's virtualization extensions are already claimed by the Windows hypervisor stack. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

> ⚠️ **Expert Note**
> This is a Windows-only concern. macOS does not have these competing hypervisor features in the same way. The video explicitly states that macOS users will not find these options. However, macOS has its own Hypervisor.framework, which VirtualBox can coexist with on Intel Macs.

***

## 1.3 — The Virtual Machine as a Hardware Abstraction

When you create a VM in VirtualBox, you are defining a **virtual hardware specification** — not installing an operating system. This is a crucial conceptual distinction. The VM creation step produces an empty virtual computer with allocated resources (CPU cores, RAM, hard disk space), but it has no OS. It is equivalent to assembling a physical computer with a motherboard, CPU, RAM, and hard drive, but never inserting a Windows or Linux installation disc. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

The resources you allocate during creation:

* **RAM (Base Memory):** The amount of physical RAM shared with the VM. The video uses 2048 MB (2 GB), with 1024 MB (1 GB) as a minimum for resource-constrained hosts. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)
* **CPU:** Number of virtual processor cores. The video uses 2 CPUs. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)
* **Hard Disk:** A virtual disk file created on the host. By default, VirtualBox uses **dynamic allocation** — the file grows as data is written, up to the specified maximum (20 GB for CentOS, 25 GB for Ubuntu by default). If you check "Pre-allocate full size," it immediately reserves the full amount on your physical disk. The video explicitly warns to leave this **unchecked**. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

The **Type** and **Subtype** you select (e.g., Linux → Red Hat for CentOS, Linux → Ubuntu for Ubuntu) are metadata hints that tell VirtualBox what defaults to apply. CentOS is a Red Hat-family OS, which is why you select "Red Hat" as the subtype — this doesn't change the VM's behavior, but it pre-configures sensible defaults for that OS family. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

> 🔍 **Deep Dive**
> Dynamic disk allocation is a space-optimization strategy. The virtual disk file (e.g., .vdi format) starts small and grows as the guest OS writes data. This means a 20 GB virtual disk might only consume 3-4 GB on your physical drive initially. Pre-allocation is used in performance-sensitive scenarios where avoiding file-system fragmentation matters, but for learning/lab environments, dynamic allocation is preferred.

***

## 1.4 — ISO Files: The Installation Medium

An ISO file is a digital replica of an optical disc (CD/DVD). In the physical world, you would insert a CentOS installation DVD into a computer's optical drive and boot from it. In the virtual world, you **attach** the ISO file to the VM's virtual CD/DVD drive, and the VM boots from this file as if it were a physical disc. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

Two ISOs are used:

* **CentOS Stream 9 boot.iso** (\~1 GB) — found by searching "CentOS Stream 9 ISO download" and selecting the file ending in `boot.iso` [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)
* **Ubuntu 22 LTS Server ISO** (Jammy Jellyfish) — specifically the **server install image**, not the desktop version [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

The ISO is attached via **Settings → Storage → Controller IDE → Empty → Choose a disc file**. A critical checkbox must be enabled: **"Live CD/DVD"**. This tells VirtualBox to treat the ISO as a bootable medium. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

After installation completes, the ISO **must be removed** from the virtual drive (Settings → Storage → Remove disk from virtual drive). If you leave it attached, the VM will boot from the ISO again on next startup, restarting the installation process instead of booting the installed OS. This mirrors real-world behavior: you remove the installation DVD after installing an OS. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

***

## 1.5 — Network Adapters, IP Addresses, and Bridge Networking

This is the most architecturally significant concept in the video. Understanding it is essential for everything that follows in later courses (Docker networking, Kubernetes networking, cloud networking). [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

### What is a Network Adapter?

A network adapter is the **device** that connects a computer to a network. Physical computers have physical adapters — wireless (WiFi) adapters and ethernet adapters. Each adapter can receive its own **IP address**, which is the unique identifier for that device on the network. The critical insight: **IP addresses are allocated to network adapters, not to computers.** A computer with multiple adapters will have multiple IP addresses. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

### How IP Addresses Are Assigned

Your WiFi router runs a service called **DHCP** (the video says "DSCP," but this is DHCP — Dynamic Host Configuration Protocol). When a network adapter connects to the router, the router assigns it an IP address from its configured range. For example, if the router's own IP is `192.168.1.1` (the **default gateway**), it assigns addresses like `192.168.1.10`, `192.168.1.11`, etc., to connected devices. The first three octets (`192.168.1`) define the **network**, and the last octet identifies the specific device. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

### Virtual Machine Networking: NAT vs. Bridge

VirtualBox provides each VM with up to **four virtual network adapters**. By default, Adapter 1 is configured as **NAT (Network Address Translation)**. NAT creates an isolated private network between the VM and the host — the VM gets a predictable IP like `10.0.2.15`, but it is invisible to other devices on your physical network. NAT is useful for internet access but not for direct communication between machines. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

**Bridged networking** solves this. When you configure Adapter 2 as a **bridged adapter**, you select your computer's physical network adapter (WiFi or Ethernet) as the bridge. The VM's virtual adapter connects *through* the physical adapter directly to the router. The router sees the VM's adapter as just another device and assigns it a real IP address in the same range as your computer. This means the VM becomes a **first-class citizen on the physical network** — other devices can reach it, and it can reach other devices. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

This is why the video instructs you to note your computer's IP (via `ipconfig` on Windows / `ifconfig` on macOS) — when the VM boots with a bridged adapter, it should receive an IP in the same subnet (e.g., `192.168.1.x`). [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

```
Physical Network Architecture:

WiFi Router (192.168.1.1) ─── DHCP ──→ assigns IPs
       │
       ├── Host Computer WiFi Adapter (192.168.1.10)
       │         │
       │         ├── [Bridge] → VM Bridged Adapter (192.168.1.x)  ← Real network IP
       │         │
       │         └── [NAT]   → VM NAT Adapter (10.0.2.15)         ← Isolated IP
       │
       └── Other devices on network...
```

> 🔍 **Deep Dive**
> The reason both NAT and bridged adapters are kept is defense in depth. NAT provides guaranteed internet access regardless of network configuration. Bridged provides network-level reachability. If the bridged adapter fails to get an IP (which the video warns can happen due to router issues), the NAT adapter still provides internet connectivity. The video's precautionary step of rebooting the router before starting addresses a common issue where routers exhaust their DHCP lease pool or have stale ARP tables.

> ⚠️ **Expert Note**
> The video mentions that many students reported VMs not receiving IP addresses, traced to router behavior. This is a real-world DHCP issue — some consumer routers limit the number of DHCP leases, or have MAC address filtering that blocks unknown virtual adapters. The precaution of power-cycling the router before VM setup clears stale leases and refreshes the DHCP state.

***

## 1.6 — Linux Network Interface Naming

Inside the Linux VM, network adapters are not called "Adapter 1" or "WiFi" — they use Linux's predictable naming convention. In the video, the CentOS VM shows:

* **enp0s3** — the NAT adapter (IP: `10.0.2.15`)
* **enp0s8** — the bridged adapter (IP: `192.168.1.x`) [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

The naming scheme `enp0sN` follows a pattern: `en` = ethernet, `p0` = PCI bus 0, `s3`/`s8` = slot number. You identify which is the bridged adapter by its IP range — it will match your host computer's subnet. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

***

## 1.7 — The Root User and Initial User Setup

Linux has a special administrative account called **root**. It has unrestricted access to everything on the system. During CentOS installation, you set the **root password** — this is the master administrative credential. The video notes that a weak password requires clicking "Done" twice (CentOS warns you), while a strong password requires only one click. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

After the first boot of CentOS, a setup wizard prompts you to create a regular user (e.g., `centosuser`). This is the non-administrative account you'll use for daily operations. Ubuntu handles this differently — you create the user during installation itself (e.g., username `devops`), and there is no separate root password step in the installer. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

***

## 1.8 — SSH: Remote Access to Linux Machines

Even though the VM runs on your local computer and you *can* interact with it through VirtualBox's console window, the standard professional practice is to connect to Linux machines **remotely via SSH** (Secure Shell). SSH provides an encrypted terminal connection over the network. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

The connection syntax is: `ssh username@ip_address`. You use **GitBash** (installed during prerequisites) on Windows as the SSH client. The first time you connect, SSH asks you to confirm the server's identity by typing `yes`. Then you enter the user's password. Once connected, you have a full command-line session on the VM. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

A critical difference between CentOS and Ubuntu: **Ubuntu requires you to explicitly select "Install OpenSSH Server" during installation** (using the space bar to check the option). If you skip this, SSH will not be available on the Ubuntu VM, and you will not be able to connect remotely. CentOS includes SSH by default in its server installation. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

***

## 1.9 — USB Tablet Pointing Device Setting

The video instructs changing the VM's pointing device to **USB Tablet** (Settings → System → Motherboard → Pointing Device). This changes how the VM captures and tracks the mouse cursor. Without this, cursor movement inside the VM can be laggy or misaligned because the default PS/2 mouse emulation doesn't support absolute positioning. USB Tablet mode enables absolute cursor positioning, making the mouse behave naturally inside the VM window. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

***

## 1.10 — Disk Partitioning (Deferred Concept)

During both CentOS and Ubuntu installation, the OS asks about disk partitioning — how to divide the virtual hard disk into logical sections. In both cases, the video selects **automatic partitioning**, letting the installer decide. The video explicitly notes that Linux partitioning and file system structure will be covered in a dedicated later section. This is a deferred concept — acknowledged but not explained here. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

***

## 1.11 — VM Lifecycle: Power Management

The video demonstrates two shutdown methods:

* **ACPI Shutdown** — sends a graceful shutdown signal to the guest OS (equivalent to pressing the power button on a real computer). The OS performs a clean shutdown sequence.
* **Power Off** — immediately cuts power to the VM (equivalent to unplugging a real computer). Faster but risks data corruption if the OS was writing to disk. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

The video uses ACPI shutdown as the primary method and mentions power off as an alternative for speed. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are creating two fully functional Linux virtual machines on a local computer using Oracle VirtualBox: one running **CentOS Stream 9** (Red Hat family) and one running **Ubuntu 22 LTS Server**. Both VMs will have bridged network connectivity (real IPs from your router) and SSH access from the host. The final outcome is two Linux servers accessible via SSH from GitBash, behaving as independent networked machines — a foundation for all subsequent DevOps, Docker, Kubernetes, and cloud learning. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

***

## Phase 1: Windows Prerequisites

*(macOS users: skip this phase entirely — these settings do not exist on macOS.)* [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

### Step 1.1 — Enable Virtualization in BIOS

Power off or reboot your computer. During boot, press the appropriate key for your hardware:

| Manufacturer | Common BIOS Key |
| ------------ | --------------- |
| HP           | F10 or Esc      |
| Lenovo       | F2 or Fn+F2     |
| Dell         | F2 or F12       |
| Others       | Delete, F2, Esc |

Navigate to the virtualization setting. It may appear as **VTx**, **Intel Virtualization Technology**, **Secure Virtual Machine**, or simply **Virtualization**. **Enable** it. Save and exit the BIOS. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

**Verification:** You'll confirm this worked later — when creating a VM, if you see "64-bit" options, VT is enabled. If only "32-bit" appears, go back and enable it. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

### Step 1.2 — Disable Conflicting Windows Features

Open the Start menu and search:

```
Turn Windows features on or off
```

In the window that opens, **uncheck** all of the following: [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

* ☐ Microsoft Hyper-V
* ☐ Windows Hypervisor Platform
* ☐ Windows Subsystem for Linux
* ☐ Virtual Machine Platform
* ☐ Docker Desktop (if present)

Click **OK**. Windows will apply changes and prompt you to **reboot**. Reboot your computer. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

**Common Mistake:** Leaving any one of these enabled. Even a single active hypervisor feature will cause VirtualBox errors. Disable *all* of them.

### Step 1.3 — Router Precaution (Prevents IP Issues)

Before proceeding with VM creation: [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

1. **Power off** your computer
2. **Reboot your router** (unplug, wait 30 seconds, plug back in)
3. **Power on** your computer

This is not mandatory but prevents a commonly reported issue where VMs fail to receive IP addresses via the bridged adapter. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

***

## Phase 2: Create Virtual Machines in VirtualBox

### Step 2.1 — Open VirtualBox

Search for and open **Oracle VM VirtualBox**. Verify version: **Help → About VirtualBox** (video uses 7.1.4). [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

### Step 2.2 — Create CentOS VM

Click the **gear icon → New** (or Machine → New).

Configure: [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

| Setting     | Value                       |
| ----------- | --------------------------- |
| **Name**    | `centosvm` (any name works) |
| **Type**    | Linux                       |
| **Subtype** | Red Hat                     |
| **Version** | Red Hat (64-bit)            |

⚠️ If only "32-bit" appears → VT is not enabled in BIOS. Go back to Step 1.1.

Click **Hardware** (or Next):

| Setting               | Value                                   |
| --------------------- | --------------------------------------- |
| **Base Memory (RAM)** | 2048 MB (2 GB). Minimum: 1024 MB (1 GB) |
| **CPUs**              | 2                                       |

Click **Hard Disk**: [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

| Setting                    | Value                                    |
| -------------------------- | ---------------------------------------- |
| **Disk Size**              | 20 GB (default)                          |
| **Pre-allocate full size** | ❌ **Unchecked** (use dynamic allocation) |

Click **Finish**. The VM is created — hardware only, no OS yet. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

### Step 2.3 — Create Ubuntu VM

Click **New** again.

| Setting          | Value                                   |
| ---------------- | --------------------------------------- |
| **Name**         | `ubuntuvm`                              |
| **Type**         | Linux                                   |
| **Subtype**      | Ubuntu                                  |
| **Version**      | Ubuntu (64-bit)                         |
| **RAM**          | 2048 MB                                 |
| **CPUs**         | 2                                       |
| **Hard Disk**    | 25 GB (default for Ubuntu, leave as-is) |
| **Pre-allocate** | ❌ Unchecked                             |

Click **Finish**. You now have two empty VMs. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

***

## Phase 3: Download ISO Files

### Step 3.1 — CentOS Stream 9 ISO

Search Google: `CentOS Stream 9 ISO download`

Navigate to the index page for Stream 9 base OS. Download the file ending in **`boot.iso`** (\~1 GB). Save it to a known location. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

### Step 3.2 — Ubuntu 22 Server ISO

Search Google: `Ubuntu 22 LTS server ISO download`

Look for: **Ubuntu 22.04 LTS (Jammy Jellyfish)** → **Server install image** (NOT desktop). Download and save. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

***

## Phase 4: Configure and Install CentOS VM

### Step 4.1 — Note Your Host IP Address

Open **Command Prompt** (Windows) or **Terminal** (macOS).

```bash
# Windows:
ipconfig

# macOS:
ifconfig
```

Find your **Wireless LAN adapter WiFi** section. Note: [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

* **IPv4 Address** (e.g., `192.168.1.10`) — your computer's IP
* **Default Gateway** (e.g., `192.168.1.1`) — your router's IP
* **First three octets** (e.g., `192.168.1`) — your network range. Your VM will get an IP in this same range.

### Step 4.2 — Attach ISO to CentOS VM

Select `centosvm` → **Right-click → Settings** (or click Settings icon).

1. **Storage** → Switch to **Expert** mode if needed
2. Click **Empty** under Controller: IDE
3. Click the **disc dropdown icon** → **Choose a disc file**
4. Select the downloaded CentOS `boot.iso` → **Open**
5. ✅ Check **"Live CD/DVD"**
6. Click **OK** [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

**What this does:** Attaches the ISO as a bootable virtual DVD. The VM will boot from this file.

### Step 4.3 — Configure Bridged Network Adapter

Select `centosvm` → **Settings → Network** (switch to Expert mode). [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

* **Adapter 1:** Leave as **NAT** (default, do not change)
* **Adapter 2:**
  * ✅ Check **Enable Network Adapter**
  * Attached to: **Bridged Adapter**
  * Name: Select your **WiFi/wireless adapter** from the dropdown

**How to identify the right adapter:** Open **Control Panel → Network and Sharing Center → Change adapter settings**. Find the adapter that shows "Connected" — note its name (e.g., `Intel WiFi 6 AX201`). Select that same name in VirtualBox's dropdown. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

* ✅ Ensure **Cable Connected** is checked
* Click **OK**

### Step 4.4 — Set Pointing Device

Select `centosvm` → **Settings → System → Motherboard**.

Change **Pointing Device** to **USB Tablet**. Click **OK**. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

**Why:** Enables smooth mouse cursor behavior inside the VM window.

### Step 4.5 — Summary of VM Settings Before Boot

Three configurations completed: [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

1. ✅ ISO attached as Live CD/DVD
2. ✅ Bridged adapter enabled on Adapter 2
3. ✅ Pointing device set to USB Tablet

### Step 4.6 — Boot and Install CentOS

Select `centosvm` → click **Start** (or double-click the VM).

A window opens. **Click on the black screen** → VirtualBox captures your mouse cursor (click "Capture" if prompted). Use **arrow keys** to select:

```
Install CentOS Stream 9
```

Press **Enter**. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

🔑 **Mouse release:** Press the **Right Ctrl** key on your keyboard to release the cursor from the VM window.

Wait for the hardware check to complete. The graphical installer loads. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

**Installation Steps:**

1. **Language:** Select **English** → Click **Continue**

2. **Installation Destination:**

   * Click the "Installation Destination" button
   * Select the **20 GB virtual hard disk**
   * Partitioning: **Automatic** (leave default)
   * Click **Done** [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

   ⚠️ If you see "No disk selected," click the disk icon to select it, then click Done.

3. **Network & Hostname:**
   * Click "Network & Host Name"
   * You'll see two adapters:
     * **enp0s3** → IP `10.0.2.15` (NAT — ignore this one)
     * **enp0s8** → IP `192.168.1.x` (Bridged — this is the one you'll use)
   * Set **Hostname:** `centosvm`
   * Click **Apply** → Click **Done** [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

4. **Root Password:**
   * Click "Root Password"
   * Enter a strong password (weak passwords require clicking Done twice)
   * Click **Done** [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

5. **User Creation:** Skip for now (will be created post-install). [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

6. Click **Begin Installation**. Wait **10-15 minutes**. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

### Step 4.7 — Post-Installation: Remove ISO and First Boot

When installation completes and "Reboot System" appears: **Do NOT click Reboot.** [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

1. Go to VirtualBox main window
2. Right-click `centosvm` → **Stop → ACPI Shutdown**
3. Wait for full shutdown
4. **Settings → Storage** → Click the ISO → **Remove disk from virtual drive**
5. Click **OK**
6. Click **Start** to boot the installed OS [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

**Why remove the ISO:** If left attached, the VM boots from the ISO again, restarting the installation process instead of booting the installed CentOS.

### Step 4.8 — CentOS First Boot Setup

After boot, a setup wizard appears:

1. Click **Start Setup** → **Next** (skip through initial screens)
2. **Full Name:** `centosuser` (or any name)
3. Set a **password** for this user
4. Click **Next** → **Start using CentOS Stream** [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

### Step 4.9 — Verify Network in CentOS

Click the **terminal icon** (TV/monitor symbol) to open the command line. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

```bash
ip addr show
```

* `ip` — the networking utility
* `addr` — address subcommand
* `show` — display all addresses

Look for the bridged adapter's IP (in the `192.168.1.x` range, NOT the `10.0.x.x` NAT IP). Note this IP. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

***

## Phase 5: SSH into CentOS VM

### Step 5.1 — Connect via GitBash

Open **GitBash** on your host computer. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

```bash
ssh centosuser@192.168.1.10
```

* `ssh` — the SSH client command
* `centosuser` — the username created during setup
* `@` — separator between user and host
* `192.168.1.10` — the bridged adapter IP of the VM (use YOUR actual IP)

When prompted: type `yes` to accept the host key. Enter the user's password. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

### Step 5.2 — Verify Connection

```bash
ip addr show    # Confirm IP addresses
hostname        # Should show "centosvm"
```

### Step 5.3 — Disconnect

```bash
exit
```

This terminates the SSH session and returns you to the host's GitBash. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

### Step 5.4 — Shut Down CentOS VM

Right-click `centosvm` → **Stop → ACPI Shutdown** (graceful) or **Power Off** (immediate). [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

***

## Phase 6: Configure and Install Ubuntu VM

### Step 6.1 — Attach ISO and Configure Network

Select `ubuntuvm` → **Settings**: [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

1. **Storage** → Click Empty CD → Choose disc file → Select Ubuntu 22 Server ISO → ✅ Check **Live CD/DVD**
2. **Network → Adapter 2** → ✅ Enable → **Bridged Adapter** → Select your WiFi adapter → ✅ Cable Connected
3. Click **OK** [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

*(Pointing device change is not explicitly repeated for Ubuntu in the video but follows the same pattern.)*

### Step 6.2 — Boot and Install Ubuntu

Click **Start**. The Ubuntu installer is text-based (server edition). [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

Installation flow — mostly pressing **Enter/Done** through defaults:

| Screen            | Action                                                                                  |
| ----------------- | --------------------------------------------------------------------------------------- |
| Language          | **English** → Enter                                                                     |
| Installer update  | **Continue without updating** → Enter                                                   |
| Keyboard          | **Done** → Enter                                                                        |
| Network           | Verify both adapters appear. Confirm bridged adapter shows `192.168.1.x` IP. → **Done** |
| Proxy             | **Done**                                                                                |
| Mirror            | **Done**                                                                                |
| Storage/Partition | **Done** (automatic) → Confirm → **Continue**                                           |
| Profile Setup     | See below                                                                               |
| SSH               | **Critical step** — see below                                                           |
| Featured snaps    | **Done** (select nothing)                                                               |

 [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

**Profile Setup:**

| Field       | Value                                |
| ----------- | ------------------------------------ |
| Your name   | Your name (e.g., your real name)     |
| Server name | `ubuntuvm`                           |
| Username    | `devops` (or any preferred username) |
| Password    | Set and remember                     |

**⚠️ CRITICAL — Install OpenSSH Server:**

On the SSH setup screen, you **must** select **"Install OpenSSH Server"**. Use the **space bar** to toggle the checkbox (a cross/X mark should appear). Then Tab to **Done** and press Enter. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

**If you skip this:** SSH will NOT work on the Ubuntu VM. You will not be able to connect remotely. This is the single most important step in the Ubuntu installation that differs from just pressing Enter through everything.

Wait **10-15 minutes** for installation to complete. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

### Step 6.3 — Post-Installation: Remove ISO and First Boot

When "Reboot" option appears: **Do NOT reboot from inside the VM.** [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

1. **Power off** the VM (ACPI Shutdown)
2. **Settings → Storage → Remove disk from virtual drive**
3. Click **OK**
4. Right-click → **Stop → Power Off** (to ensure clean state)
5. Click **Start** [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

### Step 6.4 — Login and Verify

When the VM boots, click on the console and enter: [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

```bash
# Enter username when prompted:
devops

# Enter password when prompted
```

Then verify:

```bash
ip addr show     # Note the bridged adapter IP (e.g., 192.168.1.11)
```

### Step 6.5 — SSH into Ubuntu VM

Open **GitBash**: [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

```bash
ssh devops@192.168.1.11
```

Type `yes` → Enter password → Verify:

```bash
ip addr show
hostname          # Should show "ubuntuvm"
exit              # Disconnect
```

### Step 6.6 — Shut Down Ubuntu VM

Right-click → **Stop → ACPI Shutdown** or **Power Off**. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

***

## Phase 7: Final State

You now have: [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

| VM       | OS                   | Username   | Bridged IP  | SSH Command           |
| -------- | -------------------- | ---------- | ----------- | --------------------- |
| centosvm | CentOS Stream 9      | centosuser | 192.168.1.x | `ssh centosuser@<IP>` |
| ubuntuvm | Ubuntu 22 LTS Server | devops     | 192.168.1.x | `ssh devops@<IP>`     |

Both VMs are network-accessible, SSH-capable, and function as independent Linux servers on your local network. The next lecture covers **automating this entire process**. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    HOST COMPUTER                         │
│                                                         │
│   ┌──────────┐        ┌──────────┐                     │
│   │ centosvm │        │ ubuntuvm │                      │
│   │ CentOS 9 │        │ Ubuntu22 │                      │
│   │ 2CPU/2GB │        │ 2CPU/2GB │                      │
│   │ 20GB dyn │        │ 25GB dyn │                      │
│   ├──────────┤        ├──────────┤                      │
│   │ enp0s3   │        │ Adapter1 │                      │
│   │ NAT      │        │ NAT      │                      │
│   │ 10.0.2.15│        │ 10.0.2.15│                      │
│   ├──────────┤        ├──────────┤                      │
│   │ enp0s8   │        │ Adapter2 │                      │
│   │ BRIDGED ─┼────┐   │ BRIDGED ─┼────┐                │
│   │ 192.168. │    │   │ 192.168. │    │                │
│   │ 1.10     │    │   │ 1.11     │    │                │
│   └──────────┘    │   └──────────┘    │                │
│                   │                   │                 │
│         ┌─────────┴───────────────────┘                 │
│         ▼                                               │
│   ┌──────────────┐                                      │
│   │ Host WiFi    │                                      │
│   │ Adapter      │──── 192.168.1.10                     │
│   └──────┬───────┘                                      │
└──────────┼──────────────────────────────────────────────┘
           ▼
    ┌──────────────┐
    │  WiFi Router │
    │  192.168.1.1 │
    │  DHCP Server │
    └──────────────┘
```

***

## Prerequisite Chain (Windows Only)

```
BIOS: Enable VTx/Virtualization
         ↓
Windows Features: Disable ALL of →  Hyper-V
                                     Hypervisor Platform
                                     WSL
                                     VM Platform
                                     Docker Desktop
         ↓
Reboot
         ↓
(Optional) Power off → Reboot Router → Power on
         ↓
READY for VirtualBox
```

**Diagnostic Signal:** VirtualBox shows only 32-bit → VT not enabled in BIOS

***

## VM Creation Flow

```
New VM → Name + Type (Linux) + Subtype + Version (64-bit)
       → Hardware: RAM (2048MB) + CPU (2)
       → Hard Disk: Size (dynamic, NOT pre-allocated)
       → Finish
       = Empty hardware shell. No OS.
```

***

## ISO Lifecycle

```
Download ISO → Attach to VM (Storage → IDE → Choose disc)
             → ✅ Check "Live CD/DVD"
             → Boot VM → Install OS
             → Power off (do NOT reboot from inside)
             → Remove ISO from virtual drive
             → Boot installed OS

⚠️ ISO not removed → reinstallation loop on next boot
```

***

## Installation Decision Map

```
                CentOS Stream 9              Ubuntu 22 Server
                ───────────────              ────────────────
ISO Source:     boot.iso (~1GB)              Server install image (NOT desktop)
Installer UI:  Graphical                     Text-based (TUI)
Disk:           Select disk → Auto partition Tab to Done → Auto partition
Network:        Check adapters visible       Check adapters visible
Hostname:       Set manually (centosvm)      Set in profile (ubuntuvm)
User:           Root password during install  User created during install
                Regular user post-install     (username: devops)
SSH:            Included by default          ⚠️ MUST SELECT "Install OpenSSH Server"
                                              (Space bar to toggle)
Post-install:   First-boot wizard            Direct login
```

***

## Network Mental Model

```
IP belongs to ADAPTER, not COMPUTER
    ↓
VM has virtual adapters (up to 4)
    ↓
Adapter 1 = NAT (isolated, 10.0.2.15, always works)
Adapter 2 = BRIDGED (real network IP, needs physical adapter selection)
    ↓
Bridge = VM adapter → Host physical adapter → Router → DHCP → real IP
    ↓
Result: VM is first-class network citizen (reachable, routable)
```

***

## SSH Access Pattern

```
Host (GitBash) → ssh user@bridged_IP → yes → password → connected
                                                          ↓
                                              ip addr show (verify)
                                              hostname (verify)
                                              exit (disconnect)
```

***

## Three Settings Before First Boot (Per VM)

```
1. Storage:  ISO attached + Live CD/DVD ✅
2. Network:  Adapter 2 = Bridged → WiFi adapter selected + Cable Connected ✅
3. System:   Pointing Device = USB Tablet (CentOS explicitly, Ubuntu implied)
```

***

## Verification Commands

| Command        | Purpose                          | Platform           |
| -------------- | -------------------------------- | ------------------ |
| `ipconfig`     | Show host network adapters + IPs | Windows            |
| `ifconfig`     | Show host network adapters + IPs | macOS              |
| `ip addr show` | Show VM network adapters + IPs   | Linux (inside VM)  |
| `hostname`     | Show VM hostname                 | Linux (inside VM)  |
| `ssh user@IP`  | Remote connect to VM             | GitBash (host)     |
| `exit`         | End SSH session                  | Inside SSH session |

***

## Key Failure Points & Recovery

```
❌ Only 32-bit in VirtualBox     → Enable VT in BIOS
❌ VirtualBox errors on start    → Disable Hyper-V/WSL/VM Platform
❌ VM gets no bridged IP         → Reboot router, verify adapter selection
❌ Boots into installer again    → Remove ISO from virtual drive
❌ Can't SSH to Ubuntu           → Forgot to select "Install OpenSSH Server"
❌ Mouse stuck in VM             → Press Right Ctrl to release
❌ Weak root password warning    → Click Done twice to force accept
```

***

## Reusable Engineering Patterns

**1. Resource Contention Pattern:** Only one hypervisor can own CPU virtualization extensions → must disable competitors before using VirtualBox. *Transferable to:* any scenario where exclusive resource access is required (port binding, lock contention, device drivers).

**2. Bridge/Adapter Pattern:** A virtual component connects to a physical network through an intermediary physical component, gaining first-class network citizenship. *Transferable to:* Docker bridge networking, container networking, cloud VPC peering.

**3. Boot Media Lifecycle:** Attach → Install → Detach. Installation media must be removed post-install to prevent boot loops. *Transferable to:* PXE boot workflows, cloud instance provisioning with user-data scripts, any ephemeral bootstrap process.

**4. Dual-Adapter Resilience:** NAT (guaranteed internet, isolated) + Bridge (full network, dependent on router). Layered connectivity ensures at least one path always works. *Transferable to:* multi-NIC server configurations, primary/failover network design.

**5. Manual → Automation Preview:** The entire manual process is explicitly framed as a precursor to automation. Understanding the manual steps is prerequisite to understanding what the automation abstracts away. *Transferable to:* IaC philosophy, CI/CD pipeline design, any "understand before you automate" engineering discipline. [\[19-vm-manu...intel-chip \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/19-vm-manually-windows-and-macos-intel-chip.txt)

***

*This completes the full reconstruction of the video lecture. All three sections are designed to be complementary — Theory for understanding, Practical for execution, Mental Compression Map for rapid future recall. The next lecture in the series covers automating this VM setup process.*
