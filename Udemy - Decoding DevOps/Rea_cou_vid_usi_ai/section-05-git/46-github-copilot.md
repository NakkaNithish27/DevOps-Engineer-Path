# 🎓 Setting Up GitHub Copilot with VS Code — Deep Learning Material

*Reconstructed from the video lecture on GitHub Copilot introduction and VS Code integration setup* [\[46-setup-g...ub-copilot \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/46-setup-github-copilot.txt)

***

***

# 🧠 SECTION 1: THEORY (Deep Learning Mode)

***

## 1. What GitHub Copilot Is — An AI Coding Assistant

**GitHub Copilot** is an AI tool created by GitHub that functions as a **coding assistant**. It is not a standalone application — it works by **integrating into your code editor** (specifically VS Code in this course). Once integrated, it sits alongside you as you write code, actively participating in the development process rather than waiting for you to ask questions separately. [\[46-setup-g...ub-copilot \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/46-setup-github-copilot.txt)

Its intelligence comes from being **trained on billions of lines of public code**. This massive training base is what allows it to understand coding patterns, language syntax, common idioms, and best practices across many programming languages and frameworks. It doesn't just pattern-match — it derives contextual understanding from the code you're currently writing and suggests what should come next. [\[46-setup-g...ub-copilot \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/46-setup-github-copilot.txt)

***

## 2. What Copilot Actually Does — Four Core Capabilities

Copilot provides four distinct types of assistance during day-to-day coding work: [\[46-setup-g...ub-copilot \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/46-setup-github-copilot.txt)

**Code suggestions** — As you type, Copilot suggests entire blocks of code that logically follow from what you've written. These aren't random snippets — they're contextually aware predictions based on your current file, function signatures, comments, and variable names.

**Code completions** — Beyond full suggestions, Copilot completes partial lines, function calls, parameter lists, and expressions as you type. This is finer-grained than suggestions — it fills in the details of what you're actively writing.

**Writing inline documentation** — Copilot can generate comments and documentation strings within your code, explaining what functions do, what parameters expect, and what values are returned. This reduces the manual effort of documenting code.

**Fixing mistakes** — Copilot can identify errors in your code and suggest corrections. This overlaps with traditional linting but goes further by understanding intent and suggesting fixes that align with what you're trying to accomplish.

The combined effect of these four capabilities is threefold: you **write code faster**, you write code that's **more accurate**, and — importantly — you **learn from Copilot's suggestions**. When Copilot suggests a way to write something, you see how code can be written better than you might have written it yourself. This learning dimension makes it not just a productivity tool but also a teaching tool. [\[46-setup-g...ub-copilot \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/46-setup-github-copilot.txt)

***

## 3. Copilot Chat — Conversational AI Interface

Beyond the inline code assistance, Copilot includes a **Chat** feature. This is a conversational interface where you can ask questions, request explanations, or ask Copilot to generate code through natural language dialogue — similar to chatting with an AI assistant, but within your code editor and aware of your project context. [\[46-setup-g...ub-copilot \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/46-setup-github-copilot.txt)

When you install the **GitHub Copilot** extension, the **GitHub Copilot Chat** extension is installed alongside it automatically — they are bundled together. [\[46-setup-g...ub-copilot \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/46-setup-github-copilot.txt)

***

## 4. VS Code — The Host Environment

**Visual Studio Code (VS Code)** is a code editor from Microsoft, described as **"the most famous code editor used by developers and DevOps around the world."** It serves as the host environment where Copilot operates. [\[46-setup-g...ub-copilot \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/46-setup-github-copilot.txt)

VS Code has two important architectural characteristics relevant to this lecture:

**Repository integration** — VS Code integrates directly with code repositories like GitHub. You can **clone** a repository from GitHub directly into VS Code, make commits from within the editor, or open an existing local repository folder and start editing. This means your version control workflow (covered in the previous lecture) and your coding workflow happen in the same tool.

**Extension architecture** — VS Code ships with core features, but its real power comes from its **extension system**. Extensions add new capabilities — language support (Python, C/C++, Jupyter), tooling integration, and AI assistance like Copilot. You install extensions from within VS Code's Extensions panel. This modular design means VS Code adapts to whatever technology stack you're working with. [\[46-setup-g...ub-copilot \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/46-setup-github-copilot.txt)

> 🔍 **Deep Dive**
> The extension architecture is what makes Copilot possible as a VS Code integration rather than a separate tool. Copilot runs as an extension — it hooks into VS Code's editor APIs to receive your keystrokes, understand your cursor position and file context, communicate with GitHub's AI servers, and render suggestions inline. You don't need to switch between tools; the AI assistance appears naturally within your editing experience. This is the "integrated assistant" model — the tool comes to where you work, rather than you going to the tool.

***

## 5. Pricing Model — Free Trial with Subscription

GitHub Copilot is **not completely free**. GitHub provides a **free trial** period, after which a **paid subscription** is required for continued use. The instructor explicitly notes that the course will operate within the free trial tier and advises learners not to worry about subscription costs for the duration of the course. However, the instructor recommends checking subscription fees if you plan to use Copilot beyond the course. [\[46-setup-g...ub-copilot \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/46-setup-github-copilot.txt)

The free trial has **usage limits**. The instructor shows the usage tracking interface within VS Code, which displays percentage consumption across two dimensions: **code completions** (88.6% used in the instructor's trial) and **chat messages** (37% used). These are independent quotas — you can exhaust one while still having capacity in the other. The instructor advises to "use it wisely" before the course demonstrations begin. [\[46-setup-g...ub-copilot \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/46-setup-github-copilot.txt)

When you start a paid subscription, the first **30 days are free** — providing an additional buffer beyond the initial trial. [\[46-setup-g...ub-copilot \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/46-setup-github-copilot.txt)

***

## 6. Authentication Model — GitHub Account as Identity

Copilot authenticates through your **GitHub account**. You must be logged into GitHub from your **default browser** before signing into Copilot from VS Code. When you click "Sign in to use Copilot" in VS Code, it redirects to your default browser, uses your existing GitHub session for authentication, and then returns control to VS Code. This is the same GitHub identity used for repository operations (push, pull, clone) — a single identity serves both version control and AI assistance. [\[46-setup-g...ub-copilot \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/46-setup-github-copilot.txt)

***

## 7. Course Integration — Learning by Using

The instructor positions Copilot as a tool that will be used **across several sections of the course**, not just in this lecture. The setup happens now; the usage begins in upcoming lectures and continues throughout. The learning approach is experiential: "you will be using it and learning it at the same time." [\[46-setup-g...ub-copilot \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/46-setup-github-copilot.txt)

***

***

# ⚙️ SECTION 2: PRACTICAL (Guided Execution Mode)

***

## What We're Building

We are **installing the GitHub Copilot extension in VS Code** and **authenticating it with our GitHub account**. The final outcome: Copilot is active in VS Code, ready to provide code suggestions, completions, documentation, and chat capabilities in upcoming lectures. This is a one-time setup. [\[46-setup-g...ub-copilot \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/46-setup-github-copilot.txt)

***

## Prerequisites

Before starting, ensure:

1. **VS Code** is installed on your machine
2. **A GitHub account** exists (created during the Git/versioning lecture)
3. You are **logged into your GitHub account** from your **default browser** (the browser your OS opens by default — the instructor uses Brave) [\[46-setup-g...ub-copilot \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/46-setup-github-copilot.txt)

***

## Step 1: Open VS Code

Launch Visual Studio Code. You should see the standard editor interface with the sidebar on the left containing icons for Explorer, Search, Source Control, and Extensions. [\[46-setup-g...ub-copilot \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/46-setup-github-copilot.txt)

***

## Step 2: Open the Extensions Panel

**What we're doing:** Accessing VS Code's extension marketplace to find and install Copilot.

Click the **Extensions icon** in the left sidebar (it looks like four squares with one detached). [\[46-setup-g...ub-copilot \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/46-setup-github-copilot.txt)

**What you see:** A list of popular extensions appears — you may see Python, Jupyter, C/C++, and others depending on your setup. These are language/tool-specific extensions that add support for various programming environments. [\[46-setup-g...ub-copilot \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/46-setup-github-copilot.txt)

***

## Step 3: Search for and Install GitHub Copilot

**What we're doing:** Finding the Copilot extension and installing it.

In the Extensions search bar, type:

```
Copilot
```

**What you see:** Two relevant results appear: [\[46-setup-g...ub-copilot \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/46-setup-github-copilot.txt)

* **GitHub Copilot** — the core extension (inline code suggestions, completions, documentation, fixes)
* **GitHub Copilot Chat** — the conversational interface

**Click Install on GitHub Copilot.** When you install GitHub Copilot, the Chat extension is **automatically installed alongside it** — you don't need to install them separately. [\[46-setup-g...ub-copilot \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/46-setup-github-copilot.txt)

**How to verify:** After installation, a **Copilot icon** (the Copilot symbol) appears in VS Code's interface. [\[46-setup-g...ub-copilot \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/46-setup-github-copilot.txt)

***

## Step 4: Authenticate with Your GitHub Account

**What we're doing:** Linking VS Code's Copilot extension to your GitHub account for authorization.

Click on the **Copilot icon** that appeared after installation, then click **"Sign in to use Copilot"**. [\[46-setup-g...ub-copilot \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/46-setup-github-copilot.txt)

**What happens internally:**

1. VS Code opens your **default browser**
2. The browser shows your GitHub session (you must already be logged in)
3. GitHub asks you to **"Continue"** — confirming you authorize Copilot to use your account
4. GitHub prompts you to **"Open Visual Studio Code"** — this redirects back to VS Code
5. VS Code confirms the connection is established [\[46-setup-g...ub-copilot \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/46-setup-github-copilot.txt)

**Common failure scenario:** If you are not logged into GitHub in your default browser, the authentication flow will fail or ask you to log in first. Ensure your default browser has an active GitHub session before starting this step.

**How to verify:** After authentication, Copilot is active. You should be able to click the Copilot icon and access its features. [\[46-setup-g...ub-copilot \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/46-setup-github-copilot.txt)

***

## Step 5: Access the Chat Feature

**What we're doing:** Verifying the chat interface is available.

Click the Copilot icon, then click **"Open chat"**. A chat panel opens where you can type natural language questions and receive AI-generated responses within VS Code. [\[46-setup-g...ub-copilot \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/46-setup-github-copilot.txt)

***

## Step 6: Check Free Trial Usage

**What we're doing:** Understanding how much of the free trial quota remains.

Click the **Copilot symbol** in the status area. A panel shows your usage: [\[46-setup-g...ub-copilot \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/46-setup-github-copilot.txt)

* **Code completion usage** — percentage of code completion quota consumed (instructor: 88.6%)
* **Chat message usage** — percentage of chat message quota consumed (instructor: 37%) [\[46-setup-g...ub-copilot \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/46-setup-github-copilot.txt)

**Operational advice from the instructor:** Use the free trial wisely — conserve quota for the upcoming course demonstrations where Copilot will be actively used. [\[46-setup-g...ub-copilot \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/46-setup-github-copilot.txt)

> ⚠️ **Expert Note**
> If you exhaust the free trial before the course completes, you can start a paid subscription — the first 30 days are free, providing an additional buffer. But the instructor emphasizes this is not necessary for the course; almost everything will work within the free trial limits.

***

## Setup Complete

Copilot is now installed, authenticated, and ready. No further configuration is needed. The instructor will demonstrate actual usage (code suggestions, completions, chat interactions) in upcoming lectures across multiple course sections. [\[46-setup-g...ub-copilot \| Txt\]](https://myoffice.accenture.com/personal/nakka_nithish_accenture_com/Documents/Microsoft%20Copilot%20Chat%20Files/46-setup-github-copilot.txt)

***

***

# 🧠 SECTION 3: MENTAL COMPRESSION MAP

***

## What GitHub Copilot Is

```
GitHub Copilot = AI coding assistant
  Trained on: billions of lines of public code
  Runs as: VS Code extension (not standalone)
  Provides: code suggestions, completions, inline docs, error fixes, chat
  Result: faster coding + better accuracy + learning from suggestions
```

***

## Architecture

```
┌─────────────────────────────────────────┐
│              VS Code                    │
│  ┌───────────────────────────────────┐  │
│  │         Your Code Editor          │  │
│  │  (write code, edit files, etc.)   │  │
│  └──────────────┬────────────────────┘  │
│                 │ hooks into             │
│  ┌──────────────▼────────────────────┐  │
│  │   GitHub Copilot Extension        │  │
│  │   ├── Inline: suggestions,        │  │
│  │   │   completions, docs, fixes    │  │
│  │   └── Chat: conversational AI     │  │
│  └──────────────┬────────────────────┘  │
│                 │ authenticates via      │
└─────────────────┼───────────────────────┘
                  │
                  ▼
        GitHub Account (browser)
```

***

## Setup Sequence

```
1. Open VS Code
2. Extensions panel → search "Copilot"
3. Install "GitHub Copilot" → auto-installs Chat too
4. Click Copilot icon → "Sign in to use Copilot"
5. Browser redirect → GitHub auth → "Continue" → "Open VS Code"
6. Done — Copilot active

Prerequisite: logged into GitHub in default browser
```

***

## Copilot Capabilities (4)

```
Code suggestions     → full block predictions from context
Code completions     → partial line/expression fill-in
Inline documentation → auto-generated comments/docstrings
Error fixing         → identifies mistakes + suggests corrections

Bonus: Chat interface → natural language Q&A within editor
```

***

## Pricing Model

```
Free trial → limited quota (code completions + chat messages tracked separately)
Subscription → paid, first 30 days free
Course plan → stay on free trial, use wisely
```

***

## Usage Tracking

```
Click Copilot symbol → shows:
  Code completion: X% used
  Chat messages:   Y% used
  (independent quotas)
```

***

## Authentication Flow

```
VS Code "Sign in" 
    → opens default browser
    → GitHub session validates
    → "Continue" → authorize
    → "Open VS Code" → redirects back
    → Copilot active

Identity: same GitHub account used for git push/pull/clone
Credential: saved after first auth
```

***

## VS Code Extension Architecture

```
VS Code (core editor)
  └── Extensions (modular add-ons)
       ├── Language support: Python, C/C++, Jupyter...
       ├── Tool integration: Git, Docker, etc.
       └── AI: GitHub Copilot + Copilot Chat

Install Copilot → Chat auto-bundled
Extensions panel → search → install → activate
```

***

## Key Relationships

```
GitHub account ─── authenticates ──→ Copilot extension
GitHub account ─── authenticates ──→ git push/pull (same identity)
VS Code ─── hosts ──→ Copilot (via extension system)
VS Code ─── integrates ──→ GitHub repos (clone, commit from editor)
Copilot ─── trained on ──→ billions of public code lines
```

***

## Reusable Patterns

```
PATTERN 1: Extension/Plugin Architecture
  Core system (VS Code) + pluggable modules (extensions)
  Base stays lean; capabilities added on demand
  → Same pattern: browser extensions, Jenkins plugins, IDE plugins

PATTERN 2: Unified Identity Across Services
  One GitHub account → version control (push/pull) + AI assistance (Copilot)
  Single auth identity serves multiple integrated tools
  → Same pattern: Google account across services, AWS IAM across services

PATTERN 3: Browser-Delegated Authentication
  App (VS Code) delegates auth to browser → browser holds session → redirects back
  App never handles credentials directly
  → Same pattern: OAuth flows, SSO redirects, "Sign in with Google"
```

***

This is a lightweight setup lecture — the real Copilot learning happens experientially across upcoming sections. The key takeaway is that Copilot is now an active part of your development environment, integrated into the same VS Code + GitHub ecosystem you've been building throughout the course. Ready for the next one! 🚀
