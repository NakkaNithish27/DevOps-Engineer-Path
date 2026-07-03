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

```markdown
## Progress Tracker Review

Before updating the Project Progress Tracker, review everything completed since the last update and provide a concise overview of the changes you plan to make.

Include:
- Current position updates (phase, iteration, article, track)
- Newly completed work across all four tracks
- New deliverables, assets, and milestones
- Deferred items (if any)
- Changes to Current Focus, Next Actions, and Overall Status

Do **not** generate the updated tracker yet. Wait for my confirmation.
```

## Progress Tracker Update

```markdown
## End of Iteration – Project Progress Tracker Update

Based on the approved **Progress Tracker Review**, everything completed during this iteration, the attached **Project Specification**, and the **DevOps Career Roadmap**, generate the **entire updated Project Progress Tracker** as a complete replacement document.

The tracker is a **dynamic current-state dashboard**, not a historical log. Its purpose is to answer:

> **"Where am I right now in the DevOps Career Project?"**

Only include information that is relevant to the project's current state.

### Update Requirements

Update the tracker to accurately reflect the current project state by:

* Updating the current position:
  * Phase
  * Iteration
  * Section (if applicable)
  * Article
  * Current Track
* Updating the Overall Status and Progress Dashboard.
* Updating the current status of all four tracks.
* Updating only the currently relevant deliverables, assets, milestones, deferred work, current focus, and next actions.
* Removing completed historical details that are no longer useful for understanding the current project state.
* Ensuring every section remains internally consistent.
* Keeping the tracker fully aligned with the attached **Project Specification** and **DevOps Career Roadmap**.

### Tracker Design Principles

The tracker should remain approximately the same size throughout the entire project.

Do **not** allow the document to grow indefinitely.

Treat it as a living dashboard rather than a project history.

Prioritize:

* Current State
* Current Focus
* Current Objectives
* Current Assets
* Current Milestones
* Next Actions

Avoid:

* Long historical summaries
* Repeating previously completed work
* Maintaining chronological logs
* Duplicating information already contained in the Project Specification or Roadmap

### Large Document Handling

If the complete tracker cannot fit in a single response:

1. Determine how many parts are required.
2. Tell me upfront how many parts the tracker will be split into.
3. Generate the tracker sequentially as:
   * Part 1 of N
   * Part 2 of N
   * ...
   * Part N of N
4. Do not omit or reformat content because of the split.
5. Ensure the combined parts form a single complete replacement document that can directly replace the existing Project Progress Tracker.
```
