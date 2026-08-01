# Feature-1 Sign-off Demo — live transcript

Run date: 2026-08-01 · source: live Wiki + Jira · questions: 8

## Q: What does the optional pagingRange element do in the searchEmployer operation?
*Direct spec lookup · citation present: YES*

## What `pagingRange` does in `searchEmployer`

The `pagingRange` element (of type `dgt:PagingRangeType`) enables pagination of `searchEmployer` results:

- **Purpose**: Allows the request to return a subset of the results matching the search criteria, rather than the full result set.
- **Controls**: Lets the caller specify `firstResult` (index of the first row to return) and `resultsPerPage` (how many results per page).
- **Response info**: The response also echoes back these values plus `totalResults` — the total number of Employers matching the search criteria.
- **Optionality/default**: It's optional (Min: 0, Max: 1) on both request and response. If omitted from the request, the default is 20 results per page starting at index 1.
- **Ordering**: Results are always sorted by Employer Number (`sloc_code`).

Example behavior: with 80 matching Employers and `firstResult=1`, `resultsPerPage=50`, the first 50 are returned and the response includes `firstResult=1`, `resultsPerPage=50`, `totalResults=80`. A follow-up request with `firstResult=51`, `resultsPerPage=50` returns the remaining 30 records.

Citation: Wiki: RLSI-6059 searchEmployer SBS to support pagination § SFC-04 pagingRange added to searchEmployer SBS

---

## Q: What is the default number of results per page if pagingRange is not supplied in a searchEmployer request?
*Default behavior · citation present: YES*

If the `pagingRange` element is not supplied in a `searchEmployer` request, the default is **20 results per page**, beginning with the result at index 1, with results ordered by Employer Number (sloc_code).

Citations:
- Wiki: RLSI-6059 searchEmployer SBS to support pagination § SFC-04 pagingRange added to searchEmployer SBS
- Jira: BASE-460238 — RLSI-6059 searchEmployer SBS to support pagination and return multiple results when searching by External Reference

---

## Q: Why was pagination added to the searchEmployer operation?
*Explanation synthesis · citation present: YES*

Pagination was added to the `searchEmployer` SBS operation to support higher employer search volumes and improve performance, usability, and response management, driven by client Royal London's requirement (RLSI-6059). Specifically, the new optional `pagingRange` element was introduced to:

- **Ensure consistent ordering** – results are returned in a defined, consistent order (sorted by Employer Number), improving data clarity and predictability.
- **Provide result-set visibility** – the response includes the total number of matching records, so users know the full size of the result set.
- **Improve performance** – results are returned in manageable subsets rather than one large payload, optimizing system performance and reducing response time.
- **Offer flexibility** – users can specify the number of records per page (`resultsPerPage`) based on business needs, with a default of 20 records per page.
- **Enable incremental retrieval** – users can define the starting index (`firstResult`) of records so that, combined with page size, the full result set can be retrieved incrementally and in a controlled manner.

This was needed to scale employer search for higher Employer volumes (e.g., for the Workplace Pension product) while keeping the operation aligned with business/regulatory (HMRC) requirements.

Citations:
- Jira: BASE-458911 — Sonata Business Services (SBS) - Operation searchEmployer added with optional element pagingRange (type PagingRangeType) to support pagination for higher Employer volumes, ensuring search flexibility
- Jira: BASE-458836 — Sonata Business Service (SBS) - Operation searchEmployer now supports pagination & indexed sorting via new optional pagingRange element, improving scalability for Workplace Pension product, ensuring alignment with HMRC requirements
- Wiki: RLSI-6059 searchEmployer SBS to support pagination § High Level Solutions
- Wiki: RLSI-6059 searchEmployer SBS to support pagination § SFC-04 pagingRange added to searchEmployer SBS

---

## Q: Would a client that calls searchEmployer without pagingRange see a change in behaviour?
*Backward compatibility / before-after delta · citation present: YES*

Yes — a client that omits `pagingRange` will see a behavior change, not "no change":

- **Default pagination now applies automatically.** If `pagingRange` is not provided, the system now applies a default of **20 results per page, starting at index 1**, and results are **sorted by Employer Number (sloc_code)** — this sorting and paging did not previously apply. *(Wiki: RLSI-6059 searchEmployer SBS to support pagination § SFC-04 pagingRange added to searchEmployer SBS)*

- **Effect depends on result-set size:**
  - If ≤20 employers match the search criteria, all employers are still returned in the response, sorted by Employer Number, with the total count included (AC-4).
  - If **more than 20** employers match, only the **first 20** are returned by default (rather than the full set), still sorted by Employer Number, with the total number of matching employers now included in the response (AC-5).
  *(Wiki: RLSI-6059 searchEmployer SBS to support pagination § SFC-04 pagingRange added to searchEmployer SBS)*

- This was delivered as part of BASE-458911, which added the optional `pagingRange` element to `searchEmployer` "to support pagination for higher Employer volumes, ensuring search flexibility," and the related release note BASE-458836 confirms `searchEmployer` "now supports pagination & indexed sorting via new optional pagingRange element."

So while `pagingRange` remains optional in the request, its absence no longer means "return everything unpaginated" — it now triggers the default page-size/ordering behavior described above, which is a functional change for any caller relying on getting all matching employers back without paging.

---

## Q: Does the searchEmployer pagination change return Employer External References in the response?
*Negative / out-of-scope · citation present: YES*

No — the pagination enhancement itself (RLSI‑6059) does **not** add or expand Employer External References in the `searchEmployer` response. The related work to return (multiple) Employer External References was explicitly scoped out of this change:

- The wiki's **Objectives** section shows "To return the Employer External References in the Employer search API" struck through, leaving only "To be able to divide into pages the results returned by the Employer search API" as the actual objective (Wiki: RLSI-6059 searchEmployer SBS to support pagination § Objectives).
- The **Out of Scope** table explicitly lists "Returning multiple Employer External References in Search Employer API" — noting the current API only returns a single Employer External Reference (type controlled by the Employer Reference Template field), and this was **not** changed by this initiative (Wiki: RLSI-6059 searchEmployer SBS to support pagination § Out of Scope).
- The **High Level Solutions** section confirms only HLS-02 (pagination) was delivered; HLS-01 (returning all/multiple Employer External References) is struck through, i.e., not delivered here — it's tracked separately under RLSI-6149 (Wiki: RLSI-6059 searchEmployer SBS to support pagination § High Level Solutions).
- Regression criteria RC-4/RC-5 (struck through, i.e. unchanged/pre-existing behavior) confirm only a single `employerExternalRef` element is populated per existing Employer Reference Template logic — this behavior is unaffected by the pagination change (Wiki: RLSI-6059 searchEmployer SBS to support pagination § SFC-04 pagingRange added to searchEmployer SBS).

**What the pagination change actually adds:** an optional `pagingRange` element (type `PagingRangeType`) in both the request and response, supporting `firstResult`, `resultsPerPage`, and `totalResults`, defaulting to 20 results per page ordered by Employer Number (Jira: BASE-458911 — SBS Schema Change; Wiki: RLSI-6059 searchEmployer SBS to support pagination § SFC-04 pagingRange added to searchEmployer SBS).

Note: One test-automation Jira ticket (BASE-460238) is titled "...support pagination and return multiple results when searching by External Reference," suggesting a related/linked effort touches multi-result search by external reference — but per the governing design page, the actual External Reference expansion was scoped out of this specific pagination change and belongs to a separate initiative (RLSI-6149).

---

## Q: What defect reports 14 failing TDDs for the SaveEmployerTest and GetEmployerTest classes?
*Jira lifecycle lookup · citation present: YES*

Found it: **BASE-460256** — "TDD Failures for SaveEmployerTest and GetEmployerTest Classes"

This defect explicitly states "14 TDD's are failing for classes 'SaveEmployerTest' and 'GetEmployerTest'", referencing Jenkins job `Sonata_IntegrationSuite/master/8880`, with expected behaviour "Test runs with no exception" vs actual "The above TDD are failing with exception." It was fixed in Sonata 16.2 (status: Closed).

Citation: Jira: BASE-460256 — TDD Failures for SaveEmployerTest and GetEmployerTest Classes

---

## Q: What exception does BASE-460272 report during the CreateEmployerAccount SBS request?
*Jira defect detail · citation present: YES*

During the `CreateEmployerAccount` SBS request, the SOAP call returns an HTTP 500 Internal Server Error with a fault chain culminating in a `java.lang.StackOverflowError`. Specifically, the response reports:

1. `ServiceException: BRA-154165 - Service failed`
2. `TechnicalException: BRA-190078 - Error in bravura.sonata.scheme.setup.EmployersearchDO#retrieve()`
3. `TechnicalException: BRA-190080 - Error invoking: public bravura.sonata.dao.common.search.CMSearchEmployerDTO bravura.sonata.scheme.setup.EmployersearchDO.retrieve(...) throws bravura.commons.LayeredException`
4. `TechnicalException: BRA-001 - A technical error occurred. Please refer to next layer and stacktrace for further details.`
5. `StackOverflowError: BRA-003 - An unexpected error occurred (java.lang.StackOverflowError)`
6. `Exception: BRA-003 - An unexpected error occurred (java.lang.Exception) with message: java.lang.reflect.InvocationTargetException`
7. `UndeclaredThrowableException: BRA-003 - An unexpected error occurred (java.lang.reflect.UndeclaredThrowableException)`

So the root technical exception is a **`java.lang.StackOverflowError`** occurring inside `EmployersearchDO#retrieve()`, which propagates up as a chain of `TechnicalException`/`ServiceException` wrappers (BRA-190078, BRA-190080, BRA-001, BRA-003) before surfacing as a SOAP Fault (`BRA-154165 - Service failed`).

Citation: Jira: BASE-460272 — SBS_SMOKE : Throwing exception 'TechnicalException: BRA-190078 - Error in bravura.sonata.scheme.setup.EmployersearchDO#retrieve()' during run 'CreateEmployerAccount' SBS request

---

## Q: What is the status of the schema-change ticket BASE-458911?
*Jira status lookup · citation present: YES*

**BASE-458911** — Status: **Closed** (fix version: Sonata 16.2)

This SBS schema-change ticket added a new `pagingRange` element (type `PagingRangeType`) to the `searchEmployer` operation, enabling pagination for higher Employer volumes — returning results in consistent order, providing total record counts, and allowing configurable page size/start index for incremental retrieval.

Linked issues: BASE-458834, BASE-458835, BASE-460238.

Citation: Jira: BASE-458911 — Sonata Business Services (SBS) - Operation searchEmployer added with optional element pagingRange (type PagingRangeType) to support pagination for higher Employer volumes, ensuring search flexibility

---

API usage: 17 calls · 82,720 input · 5,272 output · 29,988 cache-read