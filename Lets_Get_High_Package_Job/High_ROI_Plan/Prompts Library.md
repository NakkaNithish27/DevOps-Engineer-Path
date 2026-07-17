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

## 7.2 Prompt — Interview Answer Reviewer
~~~markdown
## Prompt — Interview Answer Reviewer

Use the attached **Project Specification**, **DevOps Career Roadmap**, and **Project Progress Tracker** as the project context.

My answers are responses to interview questions based on the technologies and topics completed so far in the roadmap.

Assume I answered **without looking at notes**.

The objective of this prompt is **not** to generate interview questions.

Its only responsibility is to review and improve my interview answers.

For **every answer I provide**, perform the following:

---

## 1. My Answer

Show **my original answer exactly as I wrote it**.

* Do **not** rewrite it.
* Do **not** correct it.
* Do **not** improve it.
* Preserve my wording so I can compare it with the improved version.

---

## 2. Interview Quality Improvement

Internally evaluate my answer for:

* Missing technical concepts.
* Incorrect understanding.
* Weak or imprecise wording.
* Missing interview points.
* Incomplete explanations.

Do **not** show this internal evaluation.

Instead, provide a rewritten answer that:

* Preserves my current level of technical knowledge.
* Fills only the important knowledge gaps appropriate for my current roadmap stage.
* Uses accurate technical terminology naturally.
* Sounds like an engineer with approximately **3–5 years of DevOps experience** answering in a technical interview.
* Remains completely aligned with the technologies and concepts I have already completed.
* Does **not** introduce advanced topics from future roadmap sections simply to make the answer sound more senior.
* Produces an answer that I could realistically explain during a real interview.

---

## 3. Why This Answer Is Better

Briefly explain why the improved answer is stronger.

Focus on improvements such as:

* Better technical terminology.
* More complete explanation.
* Better logical structure.
* More professional interview wording.
* Important concepts that were added.
* Improved clarity.

Do **not** critique my original answer line by line.

The objective is to teach me how experienced engineers communicate the same technical knowledge professionally.

---

# General Rules

* Review every answer independently.
* Preserve the intent of my original answer whenever possible.
* Correct factual mistakes.
* Fill important knowledge gaps appropriate to my current roadmap stage.
* Keep answers concise but interview-ready.
* Optimize for real technical interviews rather than textbook definitions.
* Show my original answer before the improved answer so I can easily compare the two.
* Do not ask follow-up questions unless my answer is too ambiguous to improve accurately.
* Do not introduce technologies, production practices, or concepts that belong to future sections of the roadmap.
* The goal is to help me progressively improve both my **technical understanding** and my **professional interview communication**, not simply to provide model answers.

---

# Output Size Management

Before generating the review, **estimate whether the complete interview review can fit within a single response**.

* If the complete review fits within one response, generate it normally.

* If the complete review is too large to fit within a single response, **do not begin the review immediately**.

Instead, first provide **only** an execution plan using the following format:

```text
The complete interview review is too large to fit in a single response.

It will be delivered in X parts.

Part 1
- Questions X–Y

Part 2
- Questions X–Y

...

Reply with:

"Part 1"

to begin.
```

After that:

* Generate **only** the requested part when I ask for it (e.g., "Part 1", "Part 2", etc.).
* Continue exactly where the previous part ended.
* Do **not** repeat content from previous parts.
* Do **not** skip any interview questions.
* Maintain the same output structure for every question throughout all parts.
* Continue until the complete interview review has been delivered.

~~~

##  8.0 Tell ai about all tracks result

## 8.1 End of Session Review
### Progress Tracker Edit Script for Json tracker:
~~~markdown
Generate Execution Tracker JSON Patch

Use the attached:

- Project Specification
- Project Roadmap
- Execution Tracker JSON

Compare the current Execution Tracker with the current project state.

Output only the minimal JSON patch required to synchronize the Execution Tracker with the current project state.

---

Execution Tracker Philosophy

The Execution Tracker is the project's persistent execution memory.

It stores only the smallest set of execution facts that cannot be reconstructed from the static project documents.

The Execution Tracker is not:

- a dashboard
- a progress report
- a roadmap
- a summary
- a historical log

Instead, it is the project's single source of execution truth.

Every change must preserve this philosophy.

---

Design Principles

For every potential change, apply the following rules.

Rule 1 � Store only execution state

Store only facts that represent something that actually happened.

Examples include:

- completed work
- execution notes
- assessments
- decisions
- deferred work
- created references
- execution artifacts

---

Rule 2 � Never store derived information

If information can be reconstructed from:

- the Project Specification
- the Project Roadmap
- other execution state already stored

do not store it.

Examples of derived information include:

- current phase
- current iteration
- current section
- current article
- dashboards
- progress percentages
- summaries
- health
- recommendations
- next actions
- generated reports

These must always be derived dynamically.

---

Rule 3 � Preserve single ownership

Every execution fact must have exactly one owner.

Never duplicate execution state.

If information naturally belongs to a section, deferment, assessment, reference, or another execution unit, update only that owner.

---

Rule 4 � Keep the tracker minimal

Only modify execution state that actually changed.

Never reorganize the tracker.

Never rewrite existing data unless it is necessary to keep the execution state correct.

---

Rule 5 � Respect the roadmap

The Project Roadmap is the authoritative definition of project structure and completion criteria.

Only record execution state that satisfies the roadmap's documented completion requirements.

If the tracker and roadmap disagree, generate the minimal patch necessary to reconcile the tracker with the roadmap.

---

Patch Format

Each change must follow this format:

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

---

Requirements

- Generate only the minimal set of PATCH operations required.
- Every PATCH must reference exactly one JSON path.
- The JSON path must uniquely identify the value being modified.
- The Old Value must exactly match the current tracker.
- The New Value must contain the complete replacement value.
- Preserve every unchanged value exactly.
- Do not restructure the tracker.
- Do not introduce new schema elements unless explicitly required by the project.
- Do not duplicate execution state.
- Do not store derived information.
- Modify only execution state that changed during this iteration.
- Respect deferred work recorded in the roadmap.
- Update assessments only when a new assessment has actually been completed.
- Update references only when a new project reference has been created or an existing reference has changed.
- Generate the smallest possible patch.
- Do not generate redundant PATCH operations.

---

Consistency Requirement

After applying the generated patch:

- every stored execution fact must remain correct,
- no execution fact may contradict another,
- no duplicate execution state may exist,
- every execution fact must have a single owner,
- and every stored value must represent persistent execution state rather than derived information.

---

Output Rules

- Do not explain the changes.
- Do not generate the updated tracker.

If no changes are required, output exactly:

No changes.

Wait for my confirmation before applying the patch.
~~~

## 9. Apply Progress Tracker Patch for Json Tracker
~~~markdown
Apply Execution Tracker JSON Patch

Use:

- The uploaded Execution Tracker JSON as the base document.
- The approved Execution Tracker JSON Patch, provided either:
  - in the user's message, or
  - in the immediately preceding approved assistant response.

Apply the approved patch to the Execution Tracker.

The updated tracker must satisfy all of the following:

- Every PATCH has been applied exactly once.
- No PATCH has been skipped.
- No changes have been made beyond those specified by the approved patch.
- The resulting JSON is valid.
- The tracker structure is unchanged unless the approved patch explicitly modifies it.

If any PATCH cannot be applied exactly, stop immediately and report the PATCH number and the reason.

Output the updated Execution Tracker as a ".json" file.

Return only the downloadable file.
~~~

## 10. Updated Project Json Progress Tracker Validation
~~~markdown
Validate Execution Tracker JSON Patch

Use:

- The original Execution Tracker JSON.
- The updated Execution Tracker JSON.
- The approved Execution Tracker JSON Patch, provided either:
  - in the user's message, or
  - in the immediately preceding approved assistant response.

Validate whether the updated Execution Tracker is exactly the result of applying the approved patch to the original Execution Tracker.

The approved patch is the complete specification of all permitted changes.

Validation Criteria

Confirm that:

- Every approved PATCH has been applied correctly.
- No approved PATCH has been omitted.
- No approved PATCH has been applied incorrectly.
- Every difference between the original and updated tracker is explained by the approved patch.
- No additional modifications have been introduced.
- The tracker structure is unchanged unless explicitly modified by the approved patch.
- The updated tracker is valid JSON.

Output

If the validation succeeds, respond exactly:

 PASS � The approved JSON patch was applied successfully.

Otherwise respond exactly:

 FAIL

Then list only the validation failures under the relevant headings (omit any heading with no issues):

- Missing PATCHES
- Incorrectly Applied PATCHES
- Unexpected Changes
- Removed Content
- Invalid JSON
- Modified Structure
- Other Inconsistencies

Do not suggest improvements.

Do not rewrite the tracker.

Only determine whether the approved JSON patch was applied correctly.
~~~
