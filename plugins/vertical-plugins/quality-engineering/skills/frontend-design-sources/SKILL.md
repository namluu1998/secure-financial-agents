---
name: frontend-design-sources
description: Recommend and summarize source skills for frontend design, UI taste, visual polish, UI/UX critique, and frontend UI engineering. Use when the user asks for sources, installation commands, or guidance on choosing Impeccable, Taste, Front-end UI Engineering, or UI/UX Pro Max.
---

# Frontend Design Skill Sources

## Response Language

Respond in Vietnamese by default. Keep skill names, command names, URLs, and technical terms in English when they are clearer. Use another language only when the user explicitly asks for it.

Use this skill as a source catalog and chooser. Do not copy the full external skill content into the answer unless the user provides that content or asks to inspect a locally installed copy. Prefer linking to the source and explaining how to install or when to use it.

## Sources

| Skill/source | URL | What it is good for |
|---|---|---|
| Impeccable | https://impeccable.style/ | Design vocabulary, visual polish, hierarchy, typography, color, layout, animation, live iteration, and anti-slop frontend review. |
| Taste Skill | https://www.tasteskill.dev/ | Anti-slop frontend guidance for agents; helps avoid generic AI-looking UI and improve taste, composition, and visual distinctiveness. |
| Front-end UI Engineering | https://claudemarketplaces.com/skills/addyosmani/agent-skills/frontend-ui-engineering | Frontend engineering guidance, UI implementation quality, performance, accessibility, responsive behavior, and production polish. |
| UI/UX Pro Max | https://github.com/nextlevelbuilder/ui-ux-pro-max-skill | Professional UI/UX design intelligence, critique, flows, product UX, and multi-platform interface guidance. |

## Install Notes

Provide source-specific install commands when known:

- Impeccable:
  - `npx impeccable install`
  - Claude Code marketplace source: `pbakaus/impeccable`
- Taste Skill:
  - `npx skills add Leonxlnx/taste-skill`
- UI/UX Pro Max:
  - Use the GitHub repo source: `https://github.com/nextlevelbuilder/ui-ux-pro-max-skill`
- Front-end UI Engineering:
  - Use the Claude marketplace page: `https://claudemarketplaces.com/skills/addyosmani/agent-skills/frontend-ui-engineering`

If the user asks to install one of these into this repo, first check the source license and structure. If it is a full external skill, prefer adding it as a source reference or submodule-style dependency instead of copying the whole skill blindly.

## Choosing a Source

- Choose Impeccable when the task is visual design direction, hierarchy, polish, typography, layout, motion, or removing generic AI frontend tells.
- Choose Taste Skill when the task is anti-slop frontend taste, stronger visual differentiation, or making generated UI feel less generic.
- Choose Front-end UI Engineering when the task is implementation quality: accessibility, performance, state handling, responsive UI, component architecture, and production readiness.
- Choose UI/UX Pro Max when the task is product UX, flows, wireframes, user journeys, information architecture, and professional UI critique.

## Output

When asked for a recommendation, return:

- Best source to use.
- Why it fits the task.
- Install/source link.
- Any caveats, such as Node version, marketplace cache refresh, or license/source review.
- Optional fallback source if the first choice is unavailable.
