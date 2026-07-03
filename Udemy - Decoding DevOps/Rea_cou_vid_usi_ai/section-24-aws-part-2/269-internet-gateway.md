# 🎓 Deep Learning Material: AWS Internet Gateway — Creation & VPC Attachment

**Source:** [269-internet-gateway.txt](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/269-internet-gateway.txt?EntityRepresentationId=fbcae690-9905-4af2-a194-5937697b39f3) — Video lecture covering the creation of an AWS Internet Gateway (IGW), its initial "detached" state, attaching it to a custom VPC, and its relationship to the default VPC's existing internet gateway. [\[269-internet-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/269-internet-gateway.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1.1 What an Internet Gateway Is

An Internet Gateway (IGW) is an AWS VPC component that enables communication between resources inside a VPC and the public internet. Without an internet gateway, instances in a VPC have no path to or from the internet — they are completely isolated. The internet gateway is the **doorway** between the private VPC network and the outside world. [\[269-internet-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/269-internet-gateway.txt)

Every AWS account comes with a **default VPC**, and that default VPC already has an internet gateway attached to it. The video confirms this: when you navigate to the Internet Gateways section in the AWS console, you see an existing gateway belonging to the default VPC. The instructor renames it to "default internet gateway IGW" for clarity. When you create a **custom VPC** (like "vprofile-VPC" in this project), it does **not** come with an internet gateway. You must create and attach one yourself. [\[269-internet-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/269-internet-gateway.txt)

***

## 1.2 The Detached State — Creation vs Attachment Are Separate Steps

This is the key conceptual point of the lecture. When you create an internet gateway, it is born in a **detached** state. It exists as an AWS resource, but it is not connected to any VPC. The console shows `State: detached` immediately after creation. A detached internet gateway does nothing — it is an unlinked component floating in your account. [\[269-internet-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/269-internet-gateway.txt)

You must explicitly **attach** the internet gateway to a VPC. This is a separate action: `Actions → Attach to VPC → select the VPC`. After attachment, the state changes to `attached`, and the gateway becomes the VPC's internet-facing exit point. [\[269-internet-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/269-internet-gateway.txt)

The video also mentions that this same attach operation can be performed via the **AWS CLI** using the `attach-internet-gateway` command — the console even shows the CLI equivalent when you perform the action through the UI. [\[269-internet-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/269-internet-gateway.txt)

🔍 **Deep Dive**
The two-step process (create → attach) reflects AWS's design philosophy of **decoupled resource creation**. Resources are created independently and then associated. This allows for flexibility — you could create an internet gateway, configure other components, and attach it later. It also means that simply creating the gateway is not enough; if you forget to attach it, your VPC remains internet-isolated. [\[269-internet-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/269-internet-gateway.txt)

***

## 1.3 Internet Gateway Alone Is Not Enough — The Route Table Connection

The instructor explicitly states: "In the next lecture, we are going to associate that internet gateway with the public subnet through the route table." Creating and attaching the internet gateway gives the VPC the *capability* to reach the internet, but no traffic will actually flow until a **route table** directs traffic to the gateway. Specifically, the route table associated with the public subnets must have a route entry like `0.0.0.0/0 → IGW` that says: "For any destination not in the VPC's local network, send the traffic to the internet gateway." [\[269-internet-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/269-internet-gateway.txt)

This means the internet gateway is one piece of a **three-part chain**: Internet Gateway (exists and is attached) → Route Table (has a route pointing to the IGW) → Subnet (is associated with that route table). Only subnets whose route table points to the IGW become truly "public." Other subnets in the same VPC remain private even though the VPC has an IGW attached. [\[269-internet-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/269-internet-gateway.txt)

***

## 1.4 One IGW per VPC

After creation, the account now has **two** internet gateways: one for the default VPC and one for the custom vprofile VPC. Each VPC gets its own dedicated internet gateway. An internet gateway is a one-to-one relationship with a VPC — you cannot share a single IGW across multiple VPCs, and a VPC cannot have more than one IGW. [\[269-internet-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/269-internet-gateway.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We Are Building

We are creating an Internet Gateway and attaching it to the custom vprofile VPC. This is a prerequisite for making any subnet in this VPC internet-accessible. The final outcome: the VPC has an attached IGW, ready to be linked to public subnets via a route table in the next lecture. [\[269-internet-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/269-internet-gateway.txt)

***

## Step 1: Identify the Existing Default Internet Gateway

Navigate to **VPC → Internet Gateways** in the AWS console.

You will see one internet gateway already present — this belongs to the **default VPC**. Rename it for clarity:

* Click on the Name field → enter `default internet gateway IGW`.

This is just organizational housekeeping — it helps distinguish the default from the custom one you're about to create. [\[269-internet-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/269-internet-gateway.txt)

***

## Step 2: Create a New Internet Gateway

Click **Create internet gateway**.

| Setting | Value          |
| ------- | -------------- |
| Name    | `vprofile-IGW` |

Click **Create Internet Gateway**. [\[269-internet-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/269-internet-gateway.txt)

**Immediately after creation:** The console shows `State: detached`. This is expected — the gateway exists but is not connected to any VPC yet. If you stop here, the gateway does nothing.

***

## Step 3: Attach the Internet Gateway to the VPC

While still on the newly created IGW's detail page:

1. Click **Actions** → **Attach to VPC**.
2. In the VPC dropdown, select **vprofile-VPC** (your custom VPC).
3. Click **Attach internet gateway**.

 [\[269-internet-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/269-internet-gateway.txt)

**Expected result:** The state changes from `detached` to `attached`. The IGW is now linked to the vprofile VPC.

**Verification:** Navigate back to the Internet Gateways list. You should now see **two** gateways:

| Gateway Name                   | Attached VPC |
| ------------------------------ | ------------ |
| `default internet gateway IGW` | Default VPC  |
| `vprofile-IGW`                 | vprofile-VPC |

 [\[269-internet-gateway \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/269-internet-gateway.txt)

**Common mistake:** Creating the IGW and forgetting to attach it. The VPC will remain without internet access, and instances in public subnets won't be reachable — a confusing failure that is easy to overlook.

**Connection to larger flow:** The IGW is now attached, but no traffic routes to it yet. The next lecture creates a **route table** entry (`0.0.0.0/0 → vprofile-IGW`) and associates it with the public subnets, completing the internet connectivity chain.

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## Internet Gateway — Core Concept

```
IGW = doorway between VPC and public internet
No IGW → VPC is completely internet-isolated
```

***

## Two-Step Process

```
Step 1: Create IGW              → State: DETACHED (exists, does nothing)
Step 2: Attach IGW to VPC       → State: ATTACHED (linked, ready for routing)

⚠️ Create without attach = VPC still has no internet access
```

***

## Internet Connectivity Chain (Three Parts)

```
IGW (attached to VPC)
  ↑
Route Table (0.0.0.0/0 → IGW)     ← NEXT LECTURE
  ↑
Public Subnet (associated with that route table)

ALL THREE must be in place for internet access.
Missing any one = no connectivity.
```

***

## VPC-to-IGW Relationship

```
Default VPC  ←→  default internet gateway IGW     (pre-existing)
vprofile-VPC ←→  vprofile-IGW                      (just created)

Rule: 1 VPC ↔ 1 IGW (one-to-one, not shared)
```

***

## Operational Sequence

```
1. VPC → Internet Gateways → see default IGW → rename for clarity
2. Create Internet Gateway → name: vprofile-IGW → state: detached
3. Actions → Attach to VPC → select vprofile-VPC → state: attached
4. Verify: two IGWs listed, each attached to its VPC

Alternative: AWS CLI → attach-internet-gateway command
```

***

## Key Engineering Pattern

| Pattern                          | Manifestation                                                                                                                  |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| **Decoupled create-then-attach** | Resource exists independently before being linked — allows flexible assembly order; but forgetting attachment = silent failure |
| **Layered connectivity**         | Internet access requires IGW + route table + subnet association — no single component is sufficient alone                      |
| **Default vs Custom**            | Default VPC comes with IGW pre-attached; custom VPCs require explicit creation and attachment                                  |

***

## Project Continuity

```
BEFORE: VPC created, subnets defined (public + private)
THIS:   Internet Gateway created and attached to VPC
NEXT:   Route table with 0.0.0.0/0 → IGW, associated with public subnets
```

***

This completes the full reconstruction. It's a short lecture with one core action, but the **conceptual weight** lies in understanding the detached-vs-attached state and the three-part connectivity chain (IGW → route table → subnet) — which the Theory section covers thoroughly. The Compression Map gives you the chain diagram for instant recall. Let me know if you'd like Anki flashcards or any section expanded! 🚀
