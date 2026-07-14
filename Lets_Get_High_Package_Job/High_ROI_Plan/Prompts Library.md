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

## Prompt — Engineering Debrief (End of Section)
~~~markdown
# Prompt — Engineering Debrief (End of Section)

Use the attached **Project Specification**, **DevOps Career Roadmap**, **Project Progress Tracker**, and **all articles from the completed section** as the context.

Assume I have successfully completed every practical in this section. During the section, my priority was execution and producing a working implementation. This debrief exists to convert that completed work into a compact engineering mental model before moving to the next section.

Produce an **Engineering Debrief** that maximizes **engineering understanding per minute invested**.

The output should contain the following sections.

---

## 1. Big Picture

Present the completed section as one coherent system rather than a collection of articles.

Explain:

* What was built.
* Why it exists.
* The problem it solves.
* How the major components interact.
* The end-to-end system flow.
* The single mental model that best represents the section.

The goal is that I can explain and sketch the architecture from memory.

---

## 2. Engineering Thinking

Develop engineering intuition using a small set of representative real-world scenarios from this section.

For each scenario, explain:

* The observed symptom.
* How an experienced engineer would reason about it.
* How the problem space is narrowed before investigating specific commands or tools.

Focus on reasoning rather than procedures.

---

## 3. Engineering Invariants

Extract the highest-value engineering principles from this section.

Include only concepts that remain useful even if the specific technology changes.

Prefer transferable architecture, infrastructure, deployment, networking, automation, and operational principles over technology-specific details.

---

## 4. Interview Compression

Provide explanations suitable for interviews in three formats:

* 30-second explanation
* 2-minute explanation
* 5-minute explanation

The explanations should demonstrate genuine engineering understanding rather than course memorization.

---

## Success Criteria

The debrief should:

* Maximize engineering understanding while minimizing review time.
* Merge overlapping concepts instead of following the article structure.
* Avoid repeating Track 1 content, installation procedures, commands, or configuration syntax unless essential for understanding.
* Focus on mental models, engineering reasoning, and transferable principles.
* Leave me confident explaining, reasoning about, and discussing the completed section in an engineering interview.
* Prepare me to continue to the next section without needing to revisit the completed articles.


~~~
## Upload all the articles again, tell those are completed (tell track 2 and track 3 also if nothing is there)
## Paste the track 2 suggesstion and complete it if any
## Paste the track 3 sugesstion and complete it if any

## 7. Track 4 – Interview & Job Conversion Assessment

```markdown
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
### Progress Tracker Edit Script for Json tracker:
~~~markdown
# Generate Progress Tracker JSON Patch

Use the attached:

* Project Specification
* DevOps Career Roadmap
* Progress Tracker V2 JSON

Compare the current tracker with the current project state.

Output only the minimal patch required to synchronize the tracker with the current project state.

---

## Tracker Philosophy

The Progress Tracker is the project's **live execution state**, not a historical record.

Its purpose is to represent the project's **current actionable state**. After applying the generated patch, the tracker should answer:

> **"If I open this tracker tomorrow, what should I work on next?"**

rather than:

> **"What was the last thing I completed?"**

Whenever a roadmap milestone (such as an article, section, iteration, or phase) has satisfied its completion criteria, the tracker must:

* Mark the milestone as completed.
* Advance the current working position to the next logical roadmap item, if one exists.
* Update every dependent field required to keep the tracker internally consistent.

Do not leave the tracker pointing at a completed milestone unless there is intentionally no next milestone.

---

## Roadmap Hierarchy Requirement

The **DevOps Career Roadmap** is the authoritative source for the project hierarchy:

**Phase → Iteration → Section → Article**

When determining the current project state or generating updates, use this hierarchy to determine the correct roadmap position.

If completing a roadmap milestone advances the project to the next milestone, update every affected level of the roadmap hierarchy so the tracker remains synchronized with the roadmap.

Never leave different levels of the roadmap hierarchy referring to different logical positions (for example, a completed iteration with a current section that belongs to the next iteration).

If the **Progress Tracker** and the **DevOps Career Roadmap** disagree about the current roadmap position, treat the **DevOps Career Roadmap** as the authoritative source for roadmap progression and generate the patch required to reconcile the tracker.

---

## Format

Each change must follow this format:

```text
PATCH <number>

Path:
<JSON path>

Operation:
SET
OR
ADD
OR
REMOVE

Old Value:
<existing value>

New Value:
<replacement value>
```

---

## Requirements

* Generate only the changes required to produce a fully synchronized and internally consistent tracker.
* Every PATCH must reference exactly one JSON path.
* The JSON path must uniquely identify the value being modified.
* The Old Value must exactly match the current tracker.
* The New Value must contain the complete replacement value.
* Preserve every unchanged value exactly.
* Update only the `state` object. Never modify the `schema`.
* Update only the fields affected by the completed work and any dependent fields required to keep the tracker synchronized.
* Do not mark roadmap progress as completed unless its documented completion criteria have been satisfied.
* Respect deferred deliverables. A deliverable intentionally deferred by the roadmap counts as satisfied when the roadmap explicitly specifies that it should remain deferred at the current stage.
* Update technical confidence only when Track 4 completed a confidence assessment.
* Update only the technologies assessed during this session.
* Update the Technical Revision Queue only when the confidence assessment changes its required state.
* Generate the smallest possible set of PATCH operations that leaves the tracker fully synchronized and internally consistent.
* Do not modify unrelated state.
* Do not generate redundant patches.

---

## Consistency Requirement

The generated patch must leave the tracker in a **fully synchronized and internally consistent state**.

Whenever a roadmap milestone changes state, update every dependent field that must also change so that:

* the tracker remains internally consistent,
* every level of the roadmap hierarchy matches the current project state,
* no part of the tracker references an outdated or completed roadmap item when a logical next item exists,
* and no two parts of the tracker contradict each other.

---

## Output Rules

* Do not explain the changes.
* Do not generate the updated tracker.

If no changes are required, output exactly:

```text
No changes.
```

Wait for my confirmation before applying the patch.

~~~

## 9. Apply Progress Tracker Patch for Json Tracker
~~~markdown
## Apply Progress Tracker JSON Patch

Use:

- The uploaded Progress Tracker V2 JSON as the base document.
- The approved Progress Tracker JSON Patch, which may be either:
  - included in the user's message, or
  - the immediately preceding approved assistant response.

Apply the approved patch to the tracker.

The approved patch is the complete specification of the permitted changes.

If any PATCH cannot be applied exactly, stop immediately and report the PATCH number and reason.

Validate that:

- Every PATCH was applied exactly once.
- No PATCH was skipped.
- No changes were made beyond the approved patch.

Generate the updated Progress Tracker V2 as a JSON (".json") file.

Return only the downloadable file.
~~~

## 10. Updated Project Json Progress Tracker Validation
~~~markdown
## Validate Progress Tracker JSON Patch

Use:

- The original Progress Tracker V2 JSON.
- The updated Progress Tracker V2 JSON.
- The approved Progress Tracker JSON Patch, which may be either:
  - included in the user's message, or
  - the immediately preceding approved assistant response.

Validate that the updated tracker is exactly the result of applying the approved patch to the original tracker.

The approved patch completely defines every permitted modification.

### Verify

For each PATCH:

- It was applied exactly once.
- It was applied to the specified JSON path.
- The specified operation was performed correctly.
- The Old Value was replaced, added, or removed exactly as defined.

Then verify that:

- Every difference between the original and updated tracker is explained by the approved patch.
- No additional changes were introduced.
- No unrelated values were modified or removed.
- The schema object is unchanged.
- The updated tracker remains valid JSON.

### Output

If everything is correct, respond exactly:

```text
✅ PASS – The approved JSON patch was applied successfully.
```

Otherwise respond:

```text
❌ FAIL
```

Then list only the validation failures under the relevant headings (omit any heading with no issues):

- Missing PATCHES
- Incorrectly Applied PATCHES
- Unexpected Changes
- Removed Content
- Invalid JSON
- Modified Schema
- Other Inconsistencies

Do not suggest improvements.

Do not rewrite the tracker.

Only validate whether the approved JSON patch was applied correctly.
~~~
