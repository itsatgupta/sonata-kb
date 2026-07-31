# POC Test Question Set — searchEmployer SBS pagination (RLSI-6059, Sonata 16.2)

Pilot feature per `03-poc/poc-candidate-selection.md`:
- Feature: searchEmployer SBS pagination (RLSI-6059)
- Wiki: RLSI-6059 searchEmployer SBS to support pagination (space CliRln, page 973706490)
- Jira: BASE-458832 (story), FEAT-9707 (work package), BASE-458836 (release note),
  BASE-458911 (schema change), BASE-460256 / BASE-460272 (defects)
- SME: Pratigya

Format parsed by eval/run_eval.py: `question | expected_citation_contains | expected_answer_gist`.
Note: run_eval.py only parses lines starting with What/Why/Does/Would.

## Direct fact lookup
What does the optional pagingRange element do in the searchEmployer operation? | Wiki: SFC-04 | Divides searchEmployer results into pages by passing first row and page size
What is the default number of results per page if pagingRange is not supplied in a searchEmployer request? | Wiki: SFC-04 | 20 results per page
What is the default index of the first result returned if pagingRange is not supplied? | Wiki: SFC-04 | result index 1
What is the data type of the pagingRange element added to the searchEmployer operation? | Wiki: SFC-04 | PagingRangeType
What is the cardinality of the pagingRange element in the searchEmployer request? | Wiki: SFC-04 | optional, min 0 max 1
What order are paged searchEmployer results returned in? | Wiki: SFC-04 | sorted by Employer Number (sloc_code)
What does the searchEmployer response return alongside the paged employer results? | Wiki: SFC-04 | pagingRange with firstResult, resultsPerPage, and totalResults
What Sonata release introduced the searchEmployer pagination enhancement? | Jira: BASE-458836 | Sonata 16.2
What product is the main driver for adding pagination to searchEmployer? | Wiki: | Workplace Pension product
What is the purpose of the pagingRange element as stated in the SFC-04 specification? | Wiki: SFC-04 | request paging by passing first row and page size

## Explanation
Why was pagination added to the searchEmployer operation? | Wiki: | many employers in Sonata; improve scalability for the Workplace Pension product and align with HMRC requirements
Why is the pagingRange element optional rather than mandatory in the searchEmployer request? | Wiki: SFC-04 | so requests without it keep working; the default of 20 results per page from result index 1 applies when omitted
What did the searchEmployer operation return before the pagination enhancement? | Wiki: | all matching employers in a single response without paging, which caused scalability concerns at high employer volumes

## Before/after (delta)
What changed in the searchEmployer request schema in Sonata 16.2? | Jira: BASE-458911 | an optional pagingRange element of type PagingRangeType was added
Would a client that calls searchEmployer without pagingRange see a change in behaviour? | Wiki: SFC-04 | No - the element is optional; the default of 20 results per page from result index 1 applies
What originally-planned objectives were dropped from the searchEmployer enhancement scope? | Wiki: | returning employer external references and searching by employer external reference were struck-through / out of scope
What does the searchEmployer response echo when a client requests a page starting at result 51 with 50 results per page and 80 employers match? | Wiki: SFC-04 | pagingRange with firstResult 51, resultsPerPage 50, totalResults 80

## Negative / edge case (correct answer is "no" or "not found")
Does the searchEmployer enhancement support searching by Employer External Reference? | Wiki: | No - explicitly out of scope / struck-through in the IA
Does the searchEmployer pagination change return Employer External References in the response? | Wiki: | No - returning external references was dropped from scope
Does the pagingRange element apply to the createEmployerAccount operation? | | No evidence in indexed content - pagination applies to searchEmployer only
Does the searchEmployer pagination feature affect the getEmployer operation? | | No evidence in indexed content - should not assert a relationship

## Jira lifecycle / defects
What Jira release-note ticket documents the searchEmployer pagination change? | Jira: BASE-458836 | BASE-458836
What Jira ticket tracks the SBS schema change that added the pagingRange element? | Jira: BASE-458911 | BASE-458911
What defect reports 14 failing TDDs for the SaveEmployerTest and GetEmployerTest classes? | Jira: BASE-460256 | BASE-460256
What exception does BASE-460272 report during the CreateEmployerAccount SBS request? | Jira: BASE-460272 | TechnicalException BRA-190078 in bravura.sonata.scheme.setup.EmployersearchDO#retrieve
What is the fixVersion of the searchEmployer pagination release-note ticket? | Jira: BASE-458836 | Sonata 16.2
What is the status of the schema-change ticket BASE-458911? | Jira: BASE-458911 | Closed
