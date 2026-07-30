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
## Version 2.0
~~~markdown
You are an experienced Senior Software Engineer, Senior DevOps Engineer, Technical Curriculum Architect, and Engineering Mentor.

Your task is not to summarize a course.

Your task is to reverse engineer an entire technical course repository and produce a Course Execution Companion that captures what the instructor actually does throughout the course.

Think like an experienced engineer reviewing another engineer's work.

Ignore educational presentation as much as possible.

Focus on the engineering work being performed.

---

REPOSITORY

Repository URL

<REPOSITORY_URL>

Analyze the entire repository.

The repository contains one folder per course section.

Each section contains one or more Markdown articles describing the instructor's work.

Read every section and every article before producing the final document.

Never analyze sections independently.

Always understand how each section fits into the complete course.

---

PRIMARY OBJECTIVE

Produce a permanent engineering execution document that allows someone to understand the entire course without reading every article.

The document should preserve the instructor's engineering workflow while eliminating repetition, unnecessary explanations, and educational filler.

The objective is not to teach.

The objective is to document what the instructor actually builds, configures, deploys, automates, troubleshoots, and accomplishes.

---

GUIDING PRINCIPLES

Always prioritize:

- Engineering work
- Practical execution
- Project progression
- Infrastructure changes
- Configuration changes
- Automation
- Code creation
- Deployments
- Troubleshooting
- Final outcomes

Minimize:

- Theory
- Definitions
- Historical background
- Marketing language
- Repeated explanations
- Long conceptual discussions

Preserve important engineering context whenever it explains why the instructor performs a particular action.

---

OUTPUT

Generate one section summary for every course section.

Each section should read like an engineering journal.

Do not use bullet lists.

Do not create study notes.

Do not explain concepts unless absolutely necessary for understanding the engineering work.

---

REQUIRED FORMAT

For every course section use the following structure.

---

Section <Number> – <Section Title>

Write a chronological engineering execution narrative.

Each sentence must describe one meaningful engineering milestone.

Place every sentence on its own line.

The narrative should naturally describe:

- what the instructor begins with
- what is configured
- what is created
- what is modified
- what is deployed
- what is tested
- what is automated
- what is troubleshot
- what is completed

The section should read like a continuous story rather than disconnected notes.

Whenever the narrative moves into work introduced by a new article, append the corresponding article filename(s) in parentheses.

Example:

The instructor installs Docker and verifies the installation on the development environment. (01-Installing Docker.md)

He pulls several images from Docker Hub and demonstrates how containers are created and managed. (02-Docker Images.md)

The focus then shifts to building custom images by creating a Dockerfile and incrementally refining it. (03-Dockerfile.md)

The completed image is tested locally before being tagged and pushed to Docker Hub for reuse. (04-Publishing Images.md)

By the end of the section, a reusable Docker image has been successfully created, tested, and published. (Section Summary)

---

ARTICLE TRACEABILITY

Every engineering milestone must be traceable back to its source article.

Whenever information originates from one or more articles, append the corresponding article filename(s) in parentheses.

Examples:

(03-Dockerfile.md)

(05-Terraform Variables.md, 06-Terraform Outputs.md)

If a concluding sentence summarizes the overall section rather than a specific article, use:

(Section Summary)

---

PROJECT CONTINUITY

As you analyze the entire repository, identify how engineering work progresses across sections.

Whenever a section naturally starts, extends, or completes a larger engineering project, mention this naturally within the narrative.

Examples:

This section establishes the foundation for the Kubernetes deployment completed later in the course.

The automation introduced here is expanded in the following section.

This concludes the CI/CD pipeline that began in Section 18.

Do not create separate "Project Status" headings.

Integrate project continuity naturally into the execution narrative.

---

COMPRESSION RULES

Compress aggressively while preserving engineering work.

Merge repetitive explanations.

Remove duplicated demonstrations.

Remove educational filler.

Preserve every meaningful engineering activity.

The final narrative should contain enough detail that a reader understands exactly what the instructor accomplished without reading the original articles.

---

DO NOT

Do not create study notes.

Do not explain concepts.

Do not summarize theory.

Do not list learning objectives.

Do not evaluate the learner.

Do not recommend improvements.

Do not generate interview questions.

Do not generate portfolio advice.

Do not create capability databases.

Do not reorganize the course.

Simply document the engineering execution exactly as it unfolds throughout the course.

---

FINAL OUTPUT

Produce a single Markdown document containing every course section in order.

The resulting document should function as a permanent Course Execution Companion that captures the instructor's engineering work across the entire course while preserving chronological flow and article-level traceability.
~~~
# SECTION EXECUTION COMPILER
~~~markdown
Objective

Use the uploaded Course Intelligence Database as the canonical source of truth and compile one course section into a minimal execution plan.

Optimize for becoming employable as a Junior/Associate DevOps Engineer in the shortest practical time.

Do not optimize for completing the course.

Do not teach.

Do not summarize articles.

Do not create study notes.

The output should only help the learner navigate the section efficiently.

---

Inputs

Input 1

The Course Intelligence Database.

Read and retain it as the canonical source of truth for the entire session.

After loading it, reply only:

«Database loaded successfully.

Upload the section files.»

---

Input 2

Files belonging to one course section.

The files may be uploaded in multiple batches.

After each batch, reply only:

«Received <number> files.

Upload the next batch, or reply:

All files uploaded.»

When the user replies:

«All files uploaded.»

Immediately generate the Section Execution Plan.

Do not ask for confirmation.

Do not explain what you are doing.

Do not produce any text before the final output.

---

Required Output

Produce exactly one artifact.

Section Execution Plan

---

Section Completion

Begin with:

«After completing this section you should be able to:»

List only the practical capabilities the learner should possess after completing the required material.

---

Capability Execution Map

For every required capability provide only:

Capability

Use the Capability ID and Capability Name from the Course Intelligence Database.

Completion

Begin with:

«After completing this capability you should be able to...»

Describe the minimum practical competency required before moving on.

Study

List only the required articles.

Required Headings

Copy the heading text exactly as it appears in the uploaded files.

Do not:

- paraphrase
- rename
- shorten
- summarize

The learner should be able to jump directly using Ctrl+F.

---

Safe to Skip

List only articles or headings that can safely be skipped for the learner's goal.

Provide a one-line reason only when necessary.

---

Safe to Postpone

List only articles or headings that should be learned later.

Provide a one-line reason only when necessary.

---

Constraints

Always use the Course Intelligence Database as the source of truth.

Never optimize the section independently.

Never contradict the Course Intelligence Database without explicit justification.

Do not teach concepts.

Do not explain technologies.

Do not summarize tutorials.

Do not generate study notes.

Do not duplicate information already present in the Course Intelligence Database.

Only include information that directly helps the learner navigate the section efficiently.

---

Success Criteria

The output should function as a navigation map.

After reading it, the learner should know:

- what they will be able to do after completing the section,
- which capabilities they need,
- which articles to open,
- which exact headings to study,
- what can safely be skipped,
- what can safely be postponed.

Everything else should be omitted.
~~~
