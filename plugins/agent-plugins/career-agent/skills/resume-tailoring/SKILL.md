---
name: resume-tailoring
description: Generate a job-specific, ATS-optimized resume and cover letter from a Career DNA record and a job's match analysis. Versions each output — do not overwrite prior versions. Use after job-matching confirms at least a stretch recommendation.
---

# Tailor the resume and cover letter

Inputs: Career DNA record, job requirements (from job-matching), and any existing resume versions for this candidate.

## Step 1: ATS keyword alignment

From the job requirements, identify:
- Keywords appearing in the JD title, responsibilities, and requirements sections
- Required skills not yet prominent in the candidate's existing resume
- Seniority and domain language the hiring company uses

## Step 2: Rewrite for this role

Produce a tailored resume that:
1. Opens with a summary targeting this specific role and company
2. Reorders work history bullets to surface the most relevant achievements first
3. Integrates JD keywords naturally — never keyword-stuffed
4. Quantifies achievements where possible (%, $, time saved)
5. Passes a standard ATS scan: clean formatting, no tables/columns, standard section headers

Sections: Summary · Experience · Skills · Education · Certifications

## Step 3: Write the cover letter

Three paragraphs:
1. Why this role and this company (specific, not generic)
2. Two or three achievements most relevant to the JD requirements
3. Call to action

## Step 4: Version and output

```json
{
  "candidate_id": "...",
  "job_id": "...",
  "version": "v1",
  "generated_at": "YYYY-MM-DD",
  "ats_keywords_integrated": ["..."],
  "missing_skills_addressed": ["..."],
  "resume_file": "./out/resume-<candidate>-<job>-v1.md",
  "cover_letter_file": "./out/cover-<candidate>-<job>-v1.md",
  "ats_score_estimate": 0
}
```

Never overwrite an existing version — increment the version number.
