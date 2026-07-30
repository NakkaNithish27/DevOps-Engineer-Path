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
### Get as image
~~~markdown
/handwritten + /visualizelearning: convert the attached document into image, preserve everything in a one image, you can avoid duplicate information.
~~~
~~~markdown
/handwritten + /visualizelearning

Transform the attached document into a single handwritten visual learning sheet.

## Objective

Create a **high-density visual learning companion** for the document. The image should maximise understanding, recall, revision speed, and practical execution while complementing the original document rather than replacing it.

## Requirements

- Preserve all important concepts, workflows, relationships, dependencies, practical procedures, and key technical details from the source. Remove duplicated, redundant, and low-value explanatory content where appropriate.
- Preserve the original document hierarchy, pedagogical flow, dependencies, relationships, workflows, execution order, and meaning. Do not reorder or redesign the document structure.
- Ignore the document's **Mental Map**, **Mental Compression Map**, **Summary**, or equivalent revision section. Do not include it in the image.
- Prioritise **practical content** over theory while preserving the original document hierarchy. Allocate more visual space and emphasis to practical procedures, workflows, commands, verification steps, troubleshooting, warnings, and decision points.
- Include the theory required to understand the practical work, presenting it as concisely as possible without losing the core concepts.
- Preserve all essential technical details accurately, including commands, code snippets, configuration, syntax, filenames, shortcuts, examples, warnings, verification steps, decision points, and practical procedures.
- Optimise the image for **rapid visual scanning and memory recall**. Prefer concise notes, workflows, diagrams, arrows, comparisons, grouping, and visual cues over long paragraphs wherever possible.
- Present the content as a cohesive handwritten engineering notebook or whiteboard, using natural handwritten layouts, annotations, callouts, sketches, icons, colour, and visual hierarchy to improve understanding and retention.
- Maximise information density while maintaining readability.
- Produce exactly one high-resolution image representing the entire document.

## Success Criteria

The generated image should function as a **visual learning companion** to the original document.

After studying the original document once, a learner should be able to use only the image to:

- Quickly reconstruct the complete topic.
- Recall the important concepts, relationships, and workflows.
- Revise the topic efficiently.
- Perform the practical workflows with confidence.
- Remember the important commands, procedures, warnings, verification steps, and decision points.
- Know when to return to the original document for deeper explanations or implementation details.

The image should minimise rereading of the document while significantly accelerating understanding, recall, revision, and practical execution.
~~~

### Or just give it context:
~~~markdown
I am working on the attached article. I'll reach out to you if I need any help.
~~~
### Get in Chat

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

## Get ai narration friendly interview question and answers:
~~~markdown
I am attaching the entire conversation for you. From all the parts interview review, read the interview questions along with their final interview-quality answers and convert them into a clean Interview Preparation Handbook.

Instructions

For each question, output only:

The question.

The interview-quality answer immediately below it.

Do not include:

"Answer:"

"Interview Quality Answer"

"My Answer"

"Why This Answer Is Better"

"Recall Mapping"

Scores

Feedback

Notes

Tips

Any headings or commentary.

Preserve the original question numbering and order.

Do not modify, rewrite, improve, shorten, expand, or paraphrase the interview-quality answers. Copy them exactly as provided.

Output Format

1. <Question>          

<Interview-quality answer>          2. <Question>          

<Interview-quality answer>          3. <Question>          

<Interview-quality answer>          ...

The final output should read like a clean interview handbook containing only questions and their corresponding interview-quality answers.

Note:

If the output exceeds the response limit, split it into multiple parts while preserving the numbering. Tell me how many parts you can give me the output.
~~~

## Listen using gemini voice agent 
~~~markdown
Narrate me the attached document as it is.
~~~
##  8.0 Tell ai about all tracks result

## 8.1 Progress Tracker Log
~~~markdown
Go through the attached PDF containing this entire chat conversation and the attached Progress_Tracker document containing previous session logs.

Generate a concise Markdown session log that records the highest-value permanent outcomes of this session.

The log should function as an append-only execution history for the project, documenting only information that will remain useful in future sessions.

Include, where applicable:

Completed work and milestones reached.

Important decisions or changes in direction.

Significant problems encountered and their resolutions.

Files, documents, or major artifacts created or modified.

Important insights or conclusions that affect future work.

The logical next starting point for the project.


Do not include:

Unfinished discussions.

Abandoned ideas.

Brainstorming or conversational filler.

Step-by-step learning notes or explanations unless they produced a lasting project decision.

Minor implementation details that can be recovered from project files or documentation.


Prioritize recording what changed rather than everything that was discussed. If several related tasks were completed, summarize them together instead of listing every individual activity.

Write naturally without following a fixed template or mandatory headings. Organize the information in whatever structure best reflects the completed work.

Assume someone will read this log months later to understand the project's evolution. Include enough context for continuity, but avoid repeating information already captured in previous session logs unless it changed during this session.

Target approximately 150–300 words. If very little was accomplished, write less. If an unusually large amount was accomplished, remain concise by recording only the most important outcomes.

Return only the Markdown content, enclosed in a fenced Markdown code block, ready to append to the end of Progress_Tracker.md.

End the output with a horizontal rule (---) to serve as the session separator.
~~~
# GLOBAL COURSE INTELLIGENCE GENERATION PROMPT
## Version 1.0
~~~markdown
You are an expert Technical Curriculum Architect, Senior Software/DevOps Engineer, Technical Hiring Manager, Learning Scientist, and Career Coach.

Your task is NOT to summarize this course.

Your task is to reverse engineer the entire course repository and build a permanent **Course Intelligence Document**.

This document will become the strategic foundation for all future learning prompts.

Think like an experienced engineering mentor redesigning the course into the shortest possible path to professional employability.

---

# PRIMARY OBJECTIVE

Optimize the course for one goal:

> Become employable as quickly as possible with strong real-world engineering capability while minimizing unnecessary study time.

The objective is NOT maximum knowledge.

The objective is maximum employability.

---

# GUIDING PRINCIPLES

Always optimize for:

• Practical engineering capability
• Real-world DevOps work
• Industry relevance
• Portfolio value
• Interview readiness
• Long-term career growth
• Learning efficiency

Never optimize for:

• Academic completeness
• Historical completeness
• Vendor-specific trivia
• Low-value repetition
• Knowledge that is quickly replaced later in the course

Whenever trade-offs exist, always preserve at least **90% of the employability value while minimizing total study time**.

---

# REPOSITORY SCOPE

Analyze the ENTIRE repository.

Read every section, article, chapter, and supporting document necessary to understand:

• Every capability taught
• Concept evolution
• Knowledge dependencies
• Reinforcement
• Redundancy
• Technology evolution
• Industry relevance
• Practical exercises
• Portfolio opportunities

Never optimize a section independently.

Always evaluate every section relative to the ENTIRE course.

A later section may reinforce, replace, or supersede an earlier section.

Use the complete repository before making recommendations.

---

# LEARNER PROFILE

Assume the learner:

• Has general computer literacy
• Wants a Junior / Associate DevOps Engineer role
• Prefers learning by building
• Wants practical capability over theory
• Wants strong interview preparation
• Wants portfolio-ready projects
• Is willing to revisit topics later
• Wants the shortest path to employability

---

# DECISION FRAMEWORK

Whenever making recommendations prioritize in this order:

1. Daily engineering work
2. Core engineering principles
3. Interview frequency
4. Portfolio value
5. Industry relevance
6. Career growth
7. Learning efficiency
8. Historical completeness

If two options provide similar employability value, always recommend the option requiring less study time.

---

# REQUIRED ANALYSIS

Produce the following permanent Course Intelligence.

---

## PART 1 — Capability Inventory

Identify every major engineering capability taught by the course.

For each capability include:

• Purpose
• Professional relevance
• Industry importance
• Recommended Learning Depth

Learning Depth must be one of:

• Master
• Working Knowledge
• Read Once
• Reference Only
• Safe to Skip

---

## PART 2 — Capability Evolution

For every capability identify:

• First Introduction
• Reinforcement
• Mastery Location
• Advanced Evolution

Show how knowledge evolves.

Example

Infrastructure as Code

↓

Vagrant

↓

Terraform

↓

Production Infrastructure

The purpose is to avoid over-investing in introductory technologies.

---

## PART 3 — Mastery Location

For every capability identify:

• Introduction Sections
• Reinforcement Sections
• Mastery Sections

Explicitly identify when later sections supersede earlier learning.

---

## PART 4 — Capability Importance

Rate every capability.

★★★★★
★★★★☆
★★★☆☆
★★☆☆☆
★☆☆☆☆

Provide a short justification.

Capability Importance and Learning Depth are independent.

---

## PART 5 — Section Classification

Classify every section as exactly one:

• Foundation
• Primary Learning
• Reinforcement
• Application
• Reference
• Optional
• Legacy

Explain the reasoning.

---

## PART 6 — Knowledge Dependency Graph

Identify prerequisite relationships.

Example

Linux

↓

Networking

↓

Virtualization

↓

Vagrant

↓

Provisioning

↓

Docker

↓

Kubernetes

This graph defines the optimal learning sequence.

---

## PART 7 — Redundancy Analysis

Identify:

• Repeated concepts
• Repeated explanations
• Strongest explanation
• Weaker explanations
• Safe opportunities to skim

Only recommend skipping when later material fully replaces earlier material.

---

## PART 8 — Industry Evolution

Identify technologies that are:

• Foundational
• Transitional
• Legacy
• Modern Industry Standard

Examples

Vagrant → Terraform

Jenkins Freestyle → Jenkins Pipeline

Docker Compose → Kubernetes

Recommend the appropriate investment level for each.

---

## PART 9 — Employability ROI

For every capability score:

Interview Value

★★★★★

Daily Job Value

★★★★★

Portfolio Value

★★★★★

Career Growth Value

★★★★★

Provide a concise justification.

---

## PART 10 — Global Learning Depth

Determine the minimum learning depth required for every capability.

Use ONLY:

• Master
• Working Knowledge
• Read Once
• Reference Only
• Safe to Skip

Justify every recommendation.

---

## PART 11 — Global Skip Strategy

Across the ENTIRE course identify:

• Safe to Skip Immediately
• Safe to Postpone
• Reference Only
• Read Once
• Master

This is a GLOBAL optimization.

Never evaluate sections independently.

---

## PART 12 — Portfolio Opportunities

For every capability identify:

• Should it produce a portfolio project?
• Portfolio Priority
• Recommended Project
• Minimum Implementation
• Optional Advanced Implementation

Highlight the projects with the highest hiring value.

---

## PART 13 — Interview Intelligence

Identify:

• Highest-frequency interview topics
• Practical interview exercises
• Troubleshooting scenarios
• Whiteboard/system explanation topics
• Concepts expected to be explained confidently

Prioritize real interview relevance over theoretical trivia.

---

## PART 14 — Common Learning Mistakes

Identify where learners commonly:

• Over-study
• Under-study
• Memorize instead of practice
• Spend time on obsolete knowledge
• Ignore high-value concepts

Recommend how to avoid these mistakes.

---

## PART 15 — Capability-Based Learning Roadmap

Create the final optimized roadmap.

Organize by CAPABILITIES rather than sections.

For every capability include:

• Learning Depth
• Capability Importance
• Primary Sections
• Supporting Sections
• Mastery Section
• Portfolio Recommendation
• Completion Outcome

This roadmap should represent the shortest path to employability.

---

# CONFIDENCE REPORTING

If a recommendation is uncertain because the course material does not provide enough evidence:

• State the uncertainty explicitly.
• Explain why.
• Do not guess.

---

# CONSTRAINTS

Do NOT:

• Summarize articles
• Rewrite tutorials
• Explain concepts in detail
• Produce study notes
• List every heading
• Optimize sections independently

Focus exclusively on strategic curriculum optimization.

---

# OUTPUT QUALITY STANDARDS

The Course Intelligence document must be:

• Strategic rather than descriptive
• Capability-oriented rather than section-oriented
• Concise rather than verbose
• Actionable rather than explanatory
• Stable enough to remain useful throughout the entire course

Every recommendation should be justified by employability value.

---

# FUTURE PROMPT COMPATIBILITY

Design this document to become the permanent input for future prompts including:

• Section Planner
• Learning Sessions
• Reinforcement Sessions
• Revision Planner
• Portfolio Planner
• Interview Planner

The document should act as the single source of truth for all downstream learning workflows.

---

# FINAL OUTPUT

Produce a structured Markdown document titled:

# Course Intelligence

This document should serve as the permanent strategic intelligence layer for this course and should not require regeneration unless the course content itself changes.
~~~
