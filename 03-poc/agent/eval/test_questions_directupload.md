# POC Test Question Set — Direct Uploads: saveExternalCorrespondence size allowance (FEAT-10148 / LIBSON-3635, Sonata 16.6)

Pilot feature per `03-poc/poc-candidate-selection.md`:
- Feature: Direct Uploads — increase document size allowance for saveExternalCorrespondence SBS (LIBSON-3635)
- Wiki: LIBSON-3635: Direct Uploads - Increase document size allowance for saveExternalCorrespondence sbs (space CliStl, page 1001573493)
- Jira: FEAT-10148 (work package), FEAT-10149 (IA), FEAT-10150 (design), BASE-464868 (story), BASE-464872 (release note)
- SME: Sanjay Joshi

Note: the wiki consistently misspells the operation as "saveExternalCorespondence"; both spellings appear in source.

Format parsed by eval/run_eval.py: `question | expected_citation_contains | expected_answer_gist`.
run_eval only parses lines starting with What/Why/Does/Would.

## Direct fact lookup
What is the purpose of the saveExternalCorrespondence SBS operation? | Wiki: Problem | Lets advisers save client documents onto the client correspondence tab in Sonata
What is the current hardcoded file size limit of the saveExternalCorrespondence SBS? | Wiki: | 2MB
What is the new maximum document upload size after the LIBSON-3635 enhancement? | Wiki: | 10MB
What type of client document was too large to upload before this change? | Wiki: Problem | bank statements
What Sonata release introduced the increased document size allowance? | Jira: BASE-464872 | Sonata 16.6
What is the objective of the LIBSON-3635 direct uploads enhancement? | Wiki: Objectives | allow documents larger than 2MB through the saveExternalCorrespondence SBS request

## Explanation
Why was the document size allowance increased for saveExternalCorrespondence? | Wiki: Problem | advisers could not upload documents larger than 2MB (e.g. bank statements); improve adviser and client experience on the client web platform
Why is the RDA upload functionality out of scope for this change? | Wiki: Out of Scope | it already allows a 10MB limit, so no change is required
What must be maintained when the new upload size limit is reached? | Wiki: High Level Solutions | the existing error message shown when the limit is reached

## Before/after (delta)
What changed about the saveExternalCorrespondence SBS in Sonata 16.6? | Jira: BASE-464872 | maximum document upload size increased from 2MB to 10MB
Would a 5MB client document upload successfully after this enhancement? | Wiki: | Yes - documents up to 10MB are now allowed
What does the LIBSON-3635 change assume about existing saveExternalCorrespondence functionality? | Wiki: Assumptions | Existing functionality remains unchanged (CA-01)
What does the HLS-01 solution description say about the size limit change? | Wiki: High Level Solutions | increase the allowed file size limit from 2MB to 10MB

## Negative / edge case (correct answer is "no" or "not found")
Does this enhancement change the RDA upload functionality? | Wiki: Out of Scope | No - RDA already allows 10MB and is explicitly out of scope
Does the change apply to the saveScheme or getMemberList operations? | | No evidence in indexed content - only saveExternalCorrespondence is mentioned
Does the enhancement remove the file size limit on saveExternalCorrespondence? | Wiki: | No - the limit is raised to 10MB, not removed
Does the LIBSON-3635 change affect the searchEmployer operation? | | No evidence - unrelated operation from a separate feature

## Jira lifecycle
What Jira story tracks the direct uploads document size enhancement? | Jira: BASE-464868 | BASE-464868
What is the status of the release-note ticket BASE-464872? | Jira: BASE-464872 | Closed
What work package does the direct uploads enhancement belong to? | Jira: | FEAT-10148
What is the fixVersion of the direct uploads story BASE-464868? | Jira: BASE-464868 | Sonata 16.6
