# Chat GPT Session Prompt

## Start the Chat GPT Session

```markdown
## Session Initialization

Read the attached **Project Specification**, **DevOps Career Roadmap**, and **Project Progress Tracker**, and use them as the context for this session.

Understand:

* The overall project goals and learning strategy.
* The DevOps Career Roadmap and planned iteration deliverables.
* My current progress from the Project Progress Tracker.

Do not begin any work yet. Wait for my next instruction.

```

## Current Iteration Review

```markdown
## Current Iteration Review

Based on the attached **Project Specification**, **DevOps Career Roadmap**, and **Project Progress Tracker**, tell me where we currently are in the project.

Provide a concise overview including:

* My current phase, iteration, article, and current track.
* The objective of the current iteration.
* The topics and articles planned for this iteration.
* The planned deliverables for all four tracks:

  * Core Technical Building
  * Projects & GitHub Evolution
  * Personal Branding & Communication
  * Interview & Job Conversion
* What has already been completed according to the Project Progress Tracker.
* What remains to be completed in the current iteration.
* The recommended order for completing the remaining work.
* Any deferred work that should be revisited before moving to the next iteration.

Then wait for my input before we begin.

```

## Track 1 – Core Technical Building

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

## Track 2 – Projects & GitHub Evolution

```markdown
## Track 2 – Projects & GitHub Evolution

Use the attached **Project Specification**, **DevOps Career Roadmap**, and **Project Progress Tracker** as the project context.

Based on the practicals I have completed so far in this iteration, help me complete the **Projects & GitHub Evolution** track.

* Review the GitHub deliverables planned for the current iteration.
* Recommend only recruiter-worthy portfolio assets.
* Ignore personal notes, summaries, study material, and anything intended only for personal learning.
* If a deliverable should be deferred because it belongs to a larger future project, clearly explain why and tell me to wait.
* If there are GitHub tasks to complete now, guide me through them in the recommended order.
* If there is nothing to do at this stage of the iteration, simply say:

  **"There are no Projects & GitHub deliverables to complete at this stage of the iteration."**

```

## Track 3 – Personal Branding & Communication

```markdown
## Track 3 – Personal Branding & Communication

Use the attached **Project Specification**, **DevOps Career Roadmap**, and **Project Progress Tracker** as the project context.

Based on everything I have completed so far in this iteration, help me complete the **Personal Branding & Communication** track.

* Review the communication deliverables planned for the current iteration.
* Recommend only meaningful public-facing content that demonstrates real engineering work, technical understanding, or professional growth.
* Ignore trivial setup tasks, routine course progress, personal study notes, and content that would not add value to my professional profile.
* If there are communication tasks to complete now, guide me through them in the recommended order (e.g., LinkedIn profile updates, technical posts, project walkthroughs, architecture explanations, portfolio descriptions, etc.).
* If a communication deliverable should be deferred because it depends on a larger project or milestone, clearly explain why and tell me to wait.
* If there is nothing to do at this stage of the iteration, simply say:

  **"There are no Personal Branding & Communication deliverables to complete at this stage of the iteration."**

```

## Track 4 – Interview & Job Conversion

```markdown
## Track 4 – Interview & Job Conversion

Use the attached **Project Specification**, **DevOps Career Roadmap**, and **Project Progress Tracker** as the project context.

Based on everything I have completed so far in this iteration, help me complete the **Interview & Job Conversion** track.

* Review the interview deliverables planned for the current iteration.
* Recommend only interview preparation that adds value at my current stage of the roadmap.
* Keep all recommendations aligned with my current technical level and completed practicals.
* If there are interview tasks to complete now, guide me through them in the recommended order (e.g., concept revision, troubleshooting scenarios, common interview questions, hands-on exercises, mock interviews, resume preparation, etc.).
* If a deliverable should be deferred because it will be more valuable after completing future topics, projects, or iterations, clearly explain why and tell me to wait.
* If there is nothing to do at this stage of the iteration, simply say:

  **"There are no Interview & Job Conversion deliverables to complete at this stage of the iteration."**

```

## End of Session Review

### Unified diff Output:

~~~markdown
## Progress Tracker Patch

Use the attached **Project Specification**, **DevOps Career Roadmap**, and **Project Progress Tracker** as the project context.

Review everything completed since the last update and compare it against the current **Project Progress Tracker**.

Produce **only the minimal changes** required to transform the current tracker into the correct updated tracker.

### Output Format

Output **only a unified diff (git patch format)**.

Example:

```diff
--- Project Progress Tracker.md
+++ Project Progress Tracker.md

@@ -31,3 +31,3 @@
-**Iteration 1 — Environment Foundation**
+**Iteration 2 — Linux Foundation**
```

### Requirements

- Compare the current tracker with the project's current state.
- Include **only** sections that actually change.
- Do **not** include unchanged sections.
- Preserve the existing wording unless it must change.
- Preserve formatting exactly.
- Use unified diff hunks (`@@ ... @@`) for every change.
- Include the corresponding line numbers from the current tracker in each hunk.
- Group nearby edits into the same hunk whenever appropriate.
- Do not rewrite entire sections when only a few lines changed.
- Do not explain the changes.
- Do not summarize the project.
- Do not suggest improvements.
- Do not restructure the tracker.
- Do not output markdown outside the diff.
- If there are no changes, output exactly:

```text
No changes.
```

Do **not** generate the updated tracker.

Wait for my confirmation before applying the patch.
~~~

### Unstructured Output
```markdown
## Progress Tracker Review

Review everything completed since the last Project Progress Tracker update and identify the exact changes that should be reflected in the tracker.

Only identify changes that require edits to the tracker. Do not summarize the overall project state or include unchanged areas.

Include:

- Current position updates (Phase, Iteration, Section, Article, Track)
- Changes across all four tracks
- Newly created assets, deliverables, and milestones
- Deferred items (if any)
- Changes to Current Focus, Next Actions, Overall Progress, and Overall Status

Requirements:
- Report only differences between the current tracker and the updated tracker.
- Do not suggest improvements, restructuring, or cleanup.
- Do not rewrite tracker content.
- If an area has no changes, explicitly state **No changes**.

Do **not** generate the updated tracker yet.

Wait for my confirmation.
```

## Apply Progress Tracker Patch
~~~markdown
## Apply Progress Tracker Patch

I will upload:

- The current **Project Progress Tracker**
- The approved **Progress Tracker Patch** (unified diff)
- (If needed) the **Project Specification**
- (If needed) the **DevOps Career Roadmap**

Apply the approved patch to the uploaded **Project Progress Tracker**.

Treat the unified diff as the **single source of truth** for every modification.

This is a **patch application task**, not a document rewrite.

### Requirements

- Use the uploaded Project Progress Tracker as the base document.
- Apply the unified diff exactly as provided.
- Modify only the lines specified by the patch.
- Preserve every unchanged line exactly as it appears.
- Preserve all headings, spacing, Markdown, formatting, ordering, and document structure.
- Do not infer additional edits.
- Do not fix, improve, normalize, reorganize, or rewrite any content.
- Do not change wording unless required by the patch.
- Do not modify any section that is not referenced by the patch.
- If a patch hunk affects multiple matching locations, apply it only where the unified diff indicates.
- If any hunk cannot be applied with certainty, stop and explain the conflict instead of guessing.

### Validation

Before generating the updated file, verify that:

- Every patch hunk has been applied successfully.
- No patch hunk has been skipped.
- No additional modifications have been made.
- No duplicate content has been introduced.
- The updated tracker differs from the original only where specified by the patch.
- The final document remains internally consistent.

### Output

Generate the updated **Project Progress Tracker** as a Markdown (`.md`) file.

Return only the updated downloadable file.
~~~

## Progress Tracker Update - Manually copy paste

```markdown
## End of Iteration – Project Progress Tracker Update

Based on the approved Progress Tracker Review, generate the **entire updated Project Progress Tracker** as a complete replacement document.

The tracker is a **dynamic current-state dashboard**, not a historical log.

Update only what is necessary to accurately reflect the current project state while keeping the document concise, internally consistent, and aligned with the Project Specification and DevOps Career Roadmap.

If the tracker is too large for one response:

1. Tell me how many parts are required.
2. Generate it sequentially as:
   - Part 1 of N
   - Part 2 of N
   - ...
   - Part N of N

Ensure the combined parts form one complete replacement document.
```

## Progress Tracker Update - No Manual Editing - Just Download The Updated Progress Tracker - Error Prone

```markdown
## End of Iteration – Project Progress Tracker Update

I will upload the current **Project Progress Tracker**, **Project Specification**, and **DevOps Career Roadmap**.

Based on the approved Progress Tracker Review, update the tracker by making only the changes necessary to reflect the project's current state.

Treat this as a surgical edit operation, not a document rewrite.

Requirements:
- Use the uploaded tracker as the source of truth.
- Treat the approved Progress Tracker Review as the complete and authoritative patch list.
- Apply only the approved changes.
- Do not infer, improve, reorganize, normalize, or clean up the tracker.
- If a change was not explicitly approved in the Progress Tracker Review, leave it unchanged.
- Modify existing content in place whenever possible.
- Every approved change must be mapped to an existing location in the tracker before editing. Do not guess edit locations.
- Do not append new versions of existing content or create duplicate sections, headings, or lists.
- If an approved change replaces existing content, replace it instead of adding another copy.
- If an approved change affects multiple related sections, update every affected occurrence while preserving the document structure.
- If the correct edit location cannot be determined with certainty, stop and ask instead of guessing.
- Preserve all formatting, structure, headings, spacing, Markdown, wording, ordering, and document layout unless a change is required.
- Do not rewrite, rephrase, move, merge, split, or reorder unchanged content.
- Leave every unrelated line untouched.

Before generating the updated file, verify that:
- Every approved change has been applied everywhere it is required.
- No approved changes have been missed.
- Every modification corresponds to an approved change.
- No duplicate sections, headings, or content have been introduced.
- No formatting or structural inconsistencies have been introduced.
- No unrelated content has been modified or removed.
- The updated tracker differs from the original only where approved changes were required.
- The document remains internally consistent after the edits.

Output:
- Generate the updated Markdown (.md) file.
- Return it as a downloadable file.
```

## Updated Project Progress Tracker Validation

```markdown
## Project Progress Tracker Validation

I will upload:

1. The original Project Progress Tracker.
2. The updated Project Progress Tracker.

Based on the approved Progress Tracker Review in this conversation, compare the original and updated trackers.

Treat the approved Progress Tracker Review as the authoritative list of expected differences.

Verify that:
- All approved changes were applied.
- No approved changes were missed.
- Every difference between the original and updated trackers corresponds to an approved change.
- No unintended changes were introduced.
- No important content was removed.
- The updated tracker is identical to the original except for the approved changes.

If everything is correct, respond with:

✅ PASS – Only the approved changes were made.

Otherwise, respond with:

❌ FAIL

List:
- Missing changes
- Unexpected changes
- Removed content
- Any inconsistencies
```
