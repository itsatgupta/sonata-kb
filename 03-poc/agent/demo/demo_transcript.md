# Feature-1 Sign-off Demo — live transcript

Run date: 2026-08-01 · source: live Wiki + Jira · questions: 8

## Q: What does the optional pagingRange element do in the searchEmployer operation?
*Direct spec lookup · citation present: YES*

## The `pagingRange` element in `searchEmployer`

The optional `pagingRange` element (type `dgt:PagingRangeType`) enables **pagination** of `searchEmployer` results:

- **Purpose**: Allows the request to specify a subset of results to return rather than the whole result set, by passing the **first row index** and the **page size** (results per page).
- **Fields**: In the response, it echoes back `firstResult` and `resultsPerPage`, and additionally returns `totalResults` — the total number of Employers meeting the search criteria.
- **Default behavior**: It's optional (Min: 0, Max: 1). If not provided in the request, the system defaults to **20 results per page starting at index 1**.
- **Ordering**: Results are always sorted by the **Employer Number** (`sloc_code`).
- **Example behavior** (from acceptance criteria):
  - If 80 Employers match and `firstResult=1`, `resultsPerPage=50` → the first 50 Employers are returned, with response showing `firstResult=1`, `resultsPerPage=50`, `totalResults=80`.
  - If `firstResult=51`, `resultsPerPage=50` → the remaining 30 Employers (51st–80th) are returned, with the same paging fields echoed plus `totalResults=80`.

Citation: Wiki: RLSI-6059 searchEmployer SBS to support pagination § SFC-04 pagingRange added to searchEmployer SBS

---

## Q: What is the default number of results per page if pagingRange is not supplied in a searchEmployer request?
*Default behavior · citation present: YES*

The default is **20 results per page**, starting with the result at index 1, when the `pagingRange` element is not supplied in a `searchEmployer` request. Results are ordered by Employer Number (sloc_code).

Citation: Wiki: RLSI-6059 searchEmployer SBS to support pagination § SFC-04 pagingRange added to searchEmployer SBS

---

## Q: Why was pagination added to the searchEmployer operation?
*Explanation synthesis · citation present: YES*

Pagination was added to the **searchEmployer** SBS operation (via the new optional `pagingRange` element) to support higher Employer search volumes and improve performance, usability, and response management. Specifically, the rationale was to:

- **Ensure consistent, ordered results** – results are returned in a defined order (sorted by Employer Number), improving data clarity and predictability.
- **Provide visibility of total matches** – the response includes the total number of records meeting the search criteria.
- **Optimize performance** – results are returned in manageable subsets/pages rather than one large payload, reducing response time and system load.
- **Give requesters flexibility** – users can specify how many records to return per page (`resultsPerPage`) based on business needs.
- **Enable incremental retrieval** – users can define the starting index (`firstResult`) so, combined with page size, the full result set can be retrieved in a controlled, incremental manner.

This was driven by a client requirement (Royal London / RLSI-6059) for `searchEmployer` to scale for higher Employer volumes and support the Workplace Pension product, including alignment with HMRC requirements.

Citations:
- Jira: BASE-458911 — Sonata Business Services (SBS) - Operation searchEmployer added with optional element pagingRange (type PagingRangeType) to support pagination for higher Employer volumes, ensuring search flexibility
- Jira: BASE-458836 — Sonata Business Service (SBS) - Operation searchEmployer now supports pagination & indexed sorting via new optional pagingRange element, improving scalability for Workplace Pension product, ensuring alignment with HMRC requirements
- Wiki: RLSI-6059 searchEmployer SBS to support pagination § High Level Solutions
- Wiki: RLSI-6059 searchEmployer SBS to support pagination § SFC-04 pagingRange added to searchEmployer SBS

---

## Q: Would a client that calls searchEmployer without pagingRange see a change in behaviour?
*Backward compatibility / before-after delta · citation present: YES*

Yes — behaviour would change, even though the client isn't required to pass `pagingRange`.

**What changes for a caller that omits `pagingRange`:**
- The element is optional in the request, but if not provided, the SBS now applies a **default pagination of 20 results per page, starting at index 1**, rather than returning the full unbounded result set (Wiki: RLSI-6059 searchEmployer SBS to support pagination § SFC-04 pagingRange added to searchEmployer SBS).
- Results are now **sorted by Employer Number (sloc_code)** — this ordering is applied regardless of whether `pagingRange` is supplied.
- The response will now always include a **total number of results** matching the search criteria, even when the request didn't specify paging.
- Acceptance criteria confirm this explicitly:
  - AC-4: if ≤20 Employers match, all are still returned, now sorted by Employer Number, plus a total count.
  - AC-5: if >20 Employers match, only the **first 20** are returned by default — previously this cap/sorting/total-count behaviour did not exist (Wiki: RLSI-6059 § SFC-04 pagingRange added to searchEmployer SBS).

So a client with more than 20 matching Employers who does not send `pagingRange` will now receive a truncated (first 20), sorted, and count-annotated result set — a functional change from prior unpaginated behaviour, per Jira: BASE-458911 — "Sonata Business Services (SBS) - Operation searchEmployer added with optional element pagingRange... to support pagination for higher Employer volumes" and Jira: BASE-458836 — "searchEmployer now supports pagination & indexed sorting via new optional pagingRange element."

---

## Q: Does the searchEmployer pagination change return Employer External References in the response?
*Negative / out-of-scope · citation present: YES*

No — the pagination change itself (RLSI‑6059) is scoped **only** to add the `pagingRange` element for paging (page size + starting index) to `searchEmployer`. Returning/searching by Employer External References was explicitly carved out of this ticket:

- The wiki page's **Objectives** section has "To return the Employer External References in the Employer search API" struck through, leaving only "To be able to divide into pages the results returned by the Employer search API" as in-scope (Wiki: RLSI-6059 searchEmployer SBS to support pagination § Objectives).
- The **Out of Scope** table explicitly lists "Returning multiple Employer External References in Search Employer API" as out of scope for this item, noting the current API only returns a single Employer External Reference (type controlled by the Employer Reference Template field on the Scheme) (Wiki: RLSI-6059 searchEmployer SBS to support pagination § Out of Scope).
- The **High Level Solutions** section confirms this work was split out into a separate ticket, RLSI-6149, for "Returning Employer External References in Employer search" (Wiki: RLSI-6059 searchEmployer SBS to support pagination § High Level Solutions).
- Jira RLSI-6059's description confirms: "Requirements related to searching by employer external reference has been moved to RLSI-6149" (Jira: RLSI-6059 — searchEmployer SBS to support pagination).

So the pagination feature adds the `pagingRange` element (page size/starting index, default 20 records from index 1) to `searchEmployer`, but returning Employer External References is handled separately under RLSI-6149, not as part of the pagination change itself (Jira: BASE-460238 — RLSI-6059 searchEmployer SBS to support pagination and return multiple results when searching by External Reference).

---

## Q: What defect reports 14 failing TDDs for the SaveEmployerTest and GetEmployerTest classes?
*Jira lifecycle lookup · citation present: YES*

Found it: **BASE-460256 — "TDD Failures for SaveEmployerTest and GetEmployerTest Classes"**

This defect states: "14 TDD's are failing for classes 'SaveEmployerTest' and 'GetEmployerTest'", with the Jenkins failure reported at `https://jenkins.bravurasolutions.net/job/sonata/job/Sonata_IntegrationSuite/job/master/8880/`. Expected behaviour is that tests run with no exception, but the tests are failing with an exception. It was fixed in **Sonata 16.2** and its status is Closed.

Citation: Jira: BASE-460256 — TDD Failures for SaveEmployerTest and GetEmployerTest Classes

---

## Q: What exception does BASE-460272 report during the CreateEmployerAccount SBS request?
*Jira defect detail · citation present: YES*

**BASE-460272** reports a chain of errors when running the `CreateEmployerAccount` SBS request, resulting in an HTTP 500 SOAP Fault. The faultstring layers are:

1. `ServiceException: BRA-154165 - Service failed`
2. `TechnicalException: BRA-190078 - Error in bravura.sonata.scheme.setup.EmployersearchDO#retrieve()`
3. `TechnicalException: BRA-190080 - Error invoking: ... EmployersearchDO.retrieve(...) throws bravura.commons.LayeredException`
4. `TechnicalException: BRA-001 - A technical error occurred. Please refer to next layer and stacktrace for further details.`
5. `StackOverflowError: BRA-003 - An unexpected error occurred (java.lang.StackOverflowError)`
6. `Exception: BRA-003 - An unexpected error occurred (java.lang.Exception) with message: java.lang.reflect.InvocationTargetException`
7. `UndeclaredThrowableException: BRA-003 - An unexpected error occurred (java.lang.reflect.UndeclaredThrowableException)`

So the root cause exception is a **`java.lang.StackOverflowError`** occurring in `EmployersearchDO#retrieve()`, which propagates up through `InvocationTargetException` and `UndeclaredThrowableException` wrappers before surfacing as the `BRA-190078`/`BRA-154165` service fault — instead of the expected successful account creation response.

Citation: Jira: BASE-460272 — SBS_SMOKE : Throwing exception 'TechnicalException: BRA-190078 - Error in bravura.sonata.scheme.setup.EmployersearchDO#retrieve()' during run 'CreateEmployerAccount' SBS request

---

## Q: What is the status of the schema-change ticket BASE-458911?
*Jira status lookup · citation present: YES*

**BASE-458911 — Status: Closed**

Summary: SBS operation `searchEmployer` was enhanced with a new optional element `pagingRange` (type `PagingRangeType`) to support pagination for higher Employer volumes, improving search flexibility, performance, and result predictability.

- Fix Version: Sonata 16.2
- Linked issues: BASE-458834, BASE-458835, BASE-460238

Citation: Jira: BASE-458911 — Sonata Business Services (SBS) - Operation searchEmployer added with optional element pagingRange (type PagingRangeType) to support pagination for higher Employer volumes, ensuring search flexibility

---

API usage: 17 calls · 107,501 input · 4,539 output · 28,224 cache-read