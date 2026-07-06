# Prompts Library

## 1. Start the Chat GPT Session

```markdown
## Session Initialization

Read the attached **Project Specification**, **DevOps Career Roadmap**, and **Project Progress Tracker**, and use them as the context for this session.

Understand:

* The overall project goals and learning strategy.
* The DevOps Career Roadmap and planned iteration deliverables.
* My current progress from the Project Progress Tracker.

Do not begin any work yet. Wait for my next instruction.

```

## 2. Current Iteration Review

```markdown
## Current Iteration Review

Based on the attached **Project Specification**, **DevOps Career Roadmap**, and **Project Progress Tracker**, tell me where we currently are in the project.

Provide a concise overview including:

* My current phase, iteration, curriculum position, article, and current track.
* The objective of the current iteration.
* The topics and articles planned for the current iteration.
* The planned deliverables for all four tracks:

  * Core Technical Building
  * Projects & GitHub Evolution
  * Personal Branding & Communication
  * Interview & Job Conversion
* What has already been completed according to the Project Progress Tracker.
* What remains to be completed in the current iteration.
* The recommended order for completing the remaining work.
* Any deferred work that should be revisited before moving to the next iteration.
* Current interview readiness for the technologies covered so far.
* Any technologies currently in the Technical Revision Queue.
* The recommended technical focus for today's learning session.

Do not begin teaching.

Wait for my next instruction.


```
## 3. Section Context Initialization
~~~markdown
## Section Context Initialization

The uploaded articles represent the complete learning material for the **current section** of the DevOps roadmap.

Before we begin Track 1:

- Read every uploaded article.
- Understand the section as a whole rather than as individual articles.
- Identify the overall objective of this section.
- Understand how the articles relate to one another.
- Identify the practical skills that will be developed throughout this section.
- Use this understanding as the context for the remainder of this chat.

During this session:

- Treat all uploaded articles as the authoritative source for this section.
- Maintain awareness of the entire section while we work through each article in Track 1.
- As we complete each article, keep track of the cumulative knowledge and practical work completed.

Do not begin teaching or summarizing yet.

Wait for my next instruction.
~~~

## 4. Track 1 – Core Technical Building

```markdown
## Track 1 – Core Technical Building

Use the attached **Project Specification**, **DevOps Career Roadmap**, and **Project Progress Tracker** as the project context.

Then use this article to complete the **Core Technical Building** track for today's learning session.

Before starting, classify this topic into one of these categories:

* 🟢 **Follow (20%)** — Mindset: *"If I forget this in six months, I can confidently follow the documentation again."*

* 🟡 **Understand (60%)** — Mindset: *"If someone asks me how this works, I should be able to explain the flow without looking at notes."*

* 🔴 **Troubleshoot (100%)** — Mindset: *"If this breaks in production at 2 AM, I should know where to start investigating."*

Briefly explain why you chose that category and tell me where I should spend my mental effort during this learning session.

Then:

* Give me a quick theory refresher (2–3 minutes) based on the **Theory** section.
* Dump the entire **Practical** section as-is in a clean, reader-friendly format (split it into multiple parts if it's too long).
* After the Practical section, dump the entire **Mental Compression Map** section as-is in a clean, reader-friendly format.
* Keep production tips and troubleshooting minimal, and only include them when absolutely necessary.
* Do not omit, summarize, or skip any practical steps or Mental Compression Map content.

```

## 5. Track 2 – Projects & GitHub Evolution

```markdown
## Track 2 – Projects & GitHub Evolution

Use the attached **Project Specification**, **DevOps Career Roadmap**, and **Project Progress Tracker** as the project context.

Based on everything completed in **Track 1 during this session** and the current project context, help me complete the **Projects & GitHub Evolution** track.

* Review the GitHub deliverables planned for the current iteration.
* Consider everything completed throughout this section, not just the final article.
* Recommend only recruiter-worthy portfolio assets that demonstrate meaningful engineering work or technical capability.
* Ignore personal notes, summaries, study material, and anything intended only for personal learning.
* If a deliverable should be deferred because it belongs to a larger future project, clearly explain why and tell me to wait.
* If there are GitHub tasks to complete now, guide me through them in the recommended order.
* If there is nothing to do at this stage of the section, simply say:

  **"There are no Projects & GitHub deliverables to complete at this stage of the section."**
```

## 6. Track 3 – Personal Branding & Communication

```markdown
## Track 3 – Personal Branding & Communication

Use the attached **Project Specification**, **DevOps Career Roadmap**, and **Project Progress Tracker** as the project context.

Based on everything completed in **Track 1 during this session** and the current project context, help me complete the **Personal Branding & Communication** track.

* Review the communication deliverables planned for the current iteration.
* Consider everything completed throughout this section, not just the final article.
* Recommend only meaningful public-facing content that demonstrates real engineering work, technical understanding, or professional growth.
* Ignore trivial setup tasks, routine course progress, personal study notes, and content that would not add value to my professional profile.
* If there are communication tasks to complete now, guide me through them in the recommended order (e.g., LinkedIn profile updates, technical posts, project walkthroughs, architecture explanations, portfolio descriptions, etc.).
* If a communication deliverable should be deferred because it depends on a larger project or milestone, clearly explain why and tell me to wait.
* If there is nothing to do at this stage of the section, simply say:

  **"There are no Personal Branding & Communication deliverables to complete at this stage of the section."**
```

## 7. Track 4 – Interview & Job Conversion

```markdown
## Track 4 – Interview & Job Conversion
## Track 4 – Interview & Job Conversion

Use the attached **Project Specification**, **DevOps Career Roadmap**, and **Project Progress Tracker** as the project context.

Based on everything completed in **Track 1 during this session** and the current project context, help me complete the **Interview & Job Conversion** track.

* Review the interview deliverables planned for the current iteration.
* Consider everything completed throughout the current section, not just the final article.
* Recommend only interview preparation that adds value at my current stage of the roadmap.
* Keep all recommendations aligned with my current technical level and completed technical work.
* Match the depth of interview preparation to the current roadmap phase:

  * **Phase 1:** Quick Interview Readiness Check (Recognition & Recall only)
  * **Phase 2:** Add Application assessment when appropriate.
  * **Phase 3–4:** Add Troubleshooting assessment when appropriate.
  * **Phase 5:** Conduct comprehensive interview preparation, mock interviews, and job conversion activities.
* If there are interview tasks to complete now, guide me through them in the recommended order (e.g., concept revision, interview questions, hands-on reasoning, troubleshooting scenarios, mock interviews, resume preparation, etc.).
* At the end of the session, assign confidence scores for the technology covered today:

  * Recognition
  * Recall
  * Application (if applicable)
  * Troubleshooting (if applicable)
  * Overall Confidence
* Recommend revision only when the confidence score indicates it is necessary.
* If a deliverable should be deferred because it will be more valuable after completing future topics, projects, or iterations, clearly explain why and tell me to wait.
* If there is nothing to do at this stage of the section, simply say:

  **"There are no Interview & Job Conversion deliverables to complete at this stage of the section."**

```

## 8. End of Session Review

### Progress Tracker Edit Script:

~~~markdown
## Progress Tracker Edit Script

Use the attached **Project Specification**, **DevOps Career Roadmap**, and **Project Progress Tracker** as the project context.

Compare the current tracker with the project's current state.

Output only the minimal edit script required to update the tracker.

### Format

Each edit must follow this format:

PATCH <number>

Anchor: <unique heading path>

Operation:
Replace
OR
Replace Block
OR
Insert Before
OR
Insert After
OR
Delete

Find: <existing text within the Anchor>

With: <replacement text>

### Requirements

* Generate only the edits that are required.

* Every PATCH must have a unique **Anchor**.

* Use heading paths as anchors instead of line numbers.

  Example:

  Anchor:

  # Current Focus > ### Current Work

* The **Find** text must exactly match the current tracker.

* The **Find** text must be unique within the specified **Anchor**.

* Keep the **Find** block as small as possible while still uniquely identifying the target.

* If necessary, expand the **Find** block with additional surrounding context until it is unique within the Anchor.

* Preserve every unchanged line exactly.

* Update only the sections affected by the completed learning session.

* Update the **Technical Confidence Dashboard** only when a confidence assessment was completed during **Track 4 – Interview & Job Conversion**.

* Update the **Technical Revision Queue** only when confidence scores indicate that a technology should be added, updated, reprioritized, or removed.

* Do not mark roadmap items as completed unless their roadmap completion criteria have been satisfied.

* Do not modify the roadmap structure or static project information.

* Do not explain the edits.

* Do not summarize the project.

* If no edits are required, output exactly:

No changes.

Do not generate the updated tracker.

Wait for my confirmation before applying the edit script.

~~~

## 9. Apply Progress Tracker Patch
~~~markdown
## Apply Progress Tracker Edit Script

Use:

* The uploaded **Project Progress Tracker** as the base document.
* The approved **Progress Tracker Edit Script**, which may be either:

  * included in the user's message, or
  * the immediately preceding approved assistant response.

Apply the edit script by executing a deterministic interpreter.

Treat the approved edit script as the **only source of truth** for all permitted document modifications.

Do **not** manually edit, rewrite, improve, reorganize, or optimize the tracker.

### Execution

* Parse the approved edit script into PATCH objects.
* Execute every PATCH directly from the parsed PATCH data.
* The interpreter must be generic and data-driven.
* The generated code must not contain any document-specific text outside the parsed PATCH objects.

For each PATCH:

* Locate the specified **Anchor**.
* Search only within that Anchor.
* Verify the **Find** text exists exactly once.
* Execute the specified **Operation** (`Replace`, `Replace Block`, `Insert Before`, `Insert After`, or `Delete`).
* Verify the PATCH was applied successfully before continuing.

If any PATCH cannot be applied unambiguously, stop immediately and report the PATCH number and reason.

### Validation

Verify that:

* Every PATCH was parsed.
* Every PATCH was applied exactly once.
* No PATCH was skipped.
* No PATCH modified the wrong location.
* Every modification in the generated tracker is explained by exactly one PATCH.
* No additional edits were introduced.

### Output

Generate the updated **Project Progress Tracker** as a Markdown (`.md`) file.

Return only the downloadable file.

~~~

## 10. Updated Project Progress Tracker Validation

~~~markdown
## Validate Progress Tracker Edit Script

Use:

- The original **Project Progress Tracker**
- The updated **Project Progress Tracker**
- The approved **Progress Tracker Edit Script**, which may be either:
  - included in the user's message, or
  - the immediately preceding approved assistant response.

Validate that the updated tracker is exactly the result of applying the approved edit script to the original tracker.

The edit script completely defines every permitted modification.

### Validation

For each PATCH:

- Verify it was applied exactly once.
- Verify it was applied to the correct **Section** and **Anchor**.
- Verify the specified **Operation** was performed correctly.
- Verify the **Find** text was replaced, inserted, or deleted exactly as specified.

Then verify that:

- Every difference between the original and updated tracker is explained by the approved edit script.
- No PATCH was skipped.
- No PATCH modified the wrong location.
- No additional edits were introduced.
- No unrelated content was modified or removed.
- Formatting, Markdown, headings, spacing, ordering, and document structure remain unchanged except where explicitly modified by the approved edit script.

### Output

If everything is correct, respond exactly:

```text
✅ PASS – The approved edit script was applied successfully.
```

Otherwise respond with:

```text
❌ FAIL
```

Then list only the validation failures under the relevant headings (omit any heading with no issues):

- Missing PATCHES
- Incorrectly Applied PATCHES
- Unexpected Changes
- Removed Content
- Duplicate Content
- Formatting or Structural Issues
- Other Inconsistencies

Do not suggest improvements or rewrite the tracker.
Only validate whether the approved edit script was applied correctly.
~~~

