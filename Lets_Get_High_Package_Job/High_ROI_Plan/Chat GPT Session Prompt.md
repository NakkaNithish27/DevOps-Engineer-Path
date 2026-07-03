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

## End of Iteration – Progress Review & Tracker Update

```markdown
Yes, and I think that's an excellent addition. It solves a problem we've already encountered several times when updating your tracker.

I would add it to **Phase 2**, just before the generation step.

Here's the final version of the prompt with that addition:

---

# End of Iteration – Project Progress Tracker Update

Use the attached **Project Specification**, **DevOps Career Roadmap**, and **Project Progress Tracker** as the project context.

---

# Phase 1 — Progress Review

Before updating the tracker, review everything completed since the last tracker update and provide a concise overview of the planned changes.

Include:

## Current Position

* Phase
* Iteration
* Article
* Current Track

## Newly Completed Work

Review progress across all four tracks:

* Track 1 — Core Technical Building
* Track 2 — Projects & GitHub Evolution
* Track 3 — Personal Branding & Communication
* Track 4 — Interview & Job Conversion

## New Deliverables

List any newly completed:

* Technical deliverables
* GitHub assets
* LinkedIn assets
* Career assets
* Infrastructure assets

## Deferred Work

List anything intentionally deferred and briefly explain why.

## Planned Tracker Updates

Summarize what will change in:

* Current Focus
* Next Actions
* Milestones
* Overall Status

**Do not generate the updated tracker yet.**

Wait for my confirmation.

---

# Phase 2 — Generate Updated Tracker

After I confirm, generate the **entire Project Progress Tracker** as a complete replacement document.

Update:

* Current position (phase, iteration, article, current track)
* Completed work across all four tracks
* Completed phases, iterations, and article count
* Deliverables, assets, and milestones
* Deferred work
* Current Focus
* Next Actions
* Milestones
* Overall Status

Keep the tracker fully consistent with the:

* Project Specification
* DevOps Career Roadmap

Generate the **entire tracker** so I can directly replace the existing document.

### Large Document Handling

If the complete tracker is too large to generate in a single response:

1. **Determine how many parts** are required.
2. **Tell me upfront** how many parts the tracker will be split into.
3. Generate the tracker sequentially as:

   * Part 1 of N
   * Part 2 of N
   * ...
   * Part N of N
4. Ensure that **no content is omitted, summarized, or reformatted differently** because of the split.
5. The combined parts must form a **single, complete replacement document** when copied together.

```