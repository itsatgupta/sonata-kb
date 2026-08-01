# Feature-1 Sign-off Demo — live transcript

Run date: 2026-08-01 · source: live Wiki + Jira · questions: 8

## Q: What does the optional pagingRange element do in the searchEmployer operation?
*Direct spec lookup · citation present: YES*

## Optional `pagingRange` element in `searchEmployer`

The `pagingRange` element (type `dgt:PagingRangeType`) is an **optional** element (Min: 0, Max: 1) that can appear in both the `SearchEmployerRequestType` and `SearchEmployerResponseType`. It enables **pagination** of employer search results:

- **In the request**: It lets the caller specify how many results to return per page (`resultsPerPage`) and the index of the first row to return (`firstResult`), effectively requesting a specific "page" of results that meet the search criteria.
- **Default behavior**: If `pagingRange` is not provided in the request, the default is **20 results per page**, starting at index 1.
- **Ordering**: Results are always sorted by the **Employer Number** (`sloc_code`).
- **In the response**: It echoes back `firstResult` and `resultsPerPage`, and also returns `totalResults` — the total number of results matching the search criteria (regardless of how many are returned in that page).

### Example behavior (from acceptance criteria)
- If 80 employers match the search criteria and the request specifies `firstResult = 1`, `resultsPerPage = 50`, the response returns the first 50 employers (sorted by Employer Number) along with `firstResult = 1`, `resultsPerPage = 50`, `totalResults = 80`.
- A follow-up request with `firstResult = 51`, `resultsPerPage = 50` would return the remaining 30 employers, with `totalResults` still showing 80.

This allows the SBS user to page incrementally through large result sets rather than retrieving everything at once.

**Citation:** Wiki: RLSI-6059 searchEmployer SBS to support pagination § SFC-04 pagingRange added to searchEmployer SBS

---

## Q: What is the default number of results per page if pagingRange is not supplied in a searchEmployer request?
*Default behavior · citation present: YES*

The default is **20 results per page**, starting from the result with index 1, when the `pagingRange` element is not provided in a `searchEmployer` request. Results are ordered by Employer Number (sloc_code).

Citation: Wiki: RLSI-6059 searchEmployer SBS to support pagination § SFC-04 pagingRange added to searchEmployer SBS

---

## Q: Why was pagination added to the searchEmployer operation?
*Explanation synthesis · citation present: YES*

Pagination was added to the `searchEmployer` SBS operation to support higher Employer volumes and improve search flexibility, performance, usability, and response management. Specifically, the goal was to:

- **Ensure consistent ordering** — search results are returned in a defined, consistent order (sorted by Employer Number/sloc_code), improving data clarity and predictability.
- **Provide result-set visibility** — give users visibility of the total number of matching records so they understand the complete result set.
- **Optimize performance** — return results in manageable subsets rather than one large payload, reducing response time and improving system performance for higher Employer volumes.
- **Offer flexibility** — allow users to specify the number of records per page in the request based on business needs.
- **Enable incremental retrieval** — let users define the starting index of records so that, combined with page size, the full result set can be retrieved incrementally and in a controlled manner.

This was implemented via a new optional `pagingRange` element (type `PagingRangeType`) in the request/response, defaulting to 20 records per page starting at index 1 if not specified.

Citations:
- Jira: BASE-458911 — Sonata Business Services (SBS) - Operation searchEmployer added with optional element pagingRange (type PagingRangeType) to support pagination for higher Employer volumes, ensuring search flexibility
- Jira: BASE-458836 — Sonata Business Service (SBS) - Operation searchEmployer now supports pagination & indexed sorting via new optional pagingRange element, improving scalability for Workplace Pension product, ensuring alignment with HMRC requirements
- Wiki: RLSI-6059 searchEmployer SBS to support pagination § High Level Solutions
- Wiki: RLSI-6059 searchEmployer SBS to support pagination § SFC-04 pagingRange added to searchEmployer SBS

---

## Q: Would a client that calls searchEmployer without pagingRange see a change in behaviour?
*Backward compatibility / before-after delta · citation present: YES*

Yes — behaviour changes, but it's a change in *result size/ordering*, not a breaking change to the call itself.

**What happens if `pagingRange` is omitted:**
- `pagingRange` is optional in both the request and response (Min: 0, Max: 1), so existing clients don't need to change their request payload.
- If **≤20 employers** match the search criteria, all of them are still returned (no visible change) — the response now additionally includes the total result count.
- If **more than 20 employers** match, the client will now only receive the **first 20 results by default** (sorted by Employer Number/`sloc_code`), instead of the full, unbounded result set previously returned. The response will also include the total number of matching results, even though `pagingRange` wasn't supplied in the request.

So a client omitting `pagingRange` will see identical behaviour for small result sets, but for larger result sets it will now get a truncated first page (default 20 results per page starting at index 1) rather than the complete list, plus a new total-results indicator in the response.

**Citations:**
- Wiki: RLSI-6059 searchEmployer SBS to support pagination § SFC-04 pagingRange added to searchEmployer SBS
- Jira: BASE-458911 — Sonata Business Services (SBS) - Operation searchEmployer added with optional element pagingRange (type PagingRangeType) to support pagination for higher Employer volumes, ensuring search flexibility
- Jira: BASE-460238 — RLSI-6059 searchEmployer SBS to support pagination and return multiple results when searching by External Reference

---

## Q: Does the searchEmployer pagination change return Employer External References in the response?
*Negative / out-of-scope · citation present: YES*

No — the pagination change in RLSI-6059/FEAT-9707 is scoped strictly to pagination (introducing the `pagingRange` element for page size and starting index). Returning/searching by Employer External References was explicitly split out and moved to a separate ticket, **RLSI-6149**, and is marked as **Out of Scope** for the pagination work:

- "Returning multiple Employer External References in Search Employer API ... only supports providing a single External Reference in a request" — listed as out of scope for this change (Wiki: RLSI-6059 searchEmployer SBS to support pagination § Out of Scope).
- The Objectives section strikes through "To return the Employer External References in the Employer search API," leaving only "To be able to divide into pages the results returned by the Employer search API" as the actual objective (Wiki: RLSI-6059 searchEmployer SBS to support pagination § Objectives).
- The original ticket description also notes: "Requirements related to searching by employer external reference has been moved to RLSI-6149" (Jira: RLSI-6059 — searchEmployer SBS to support pagination).

So the searchEmployer pagination change itself only adds the `pagingRange` element (page size + start index); it does not add Employer External References to the response — that's handled by the separate RLSI-6149 work.

---

## Q: What defect reports 14 failing TDDs for the SaveEmployerTest and GetEmployerTest classes?
*Jira lifecycle lookup · citation present: YES*

Found it: **BASE-460256 — "TDD Failures for SaveEmployerTest and GetEmployerTest Classes"**

- **Overview**: "14 TDD's are failing for classes 'SaveEmployerTest' and 'GetEmployerTest'"
- Jenkins reference: `Sonata_IntegrationSuite/job/master/8880`
- Expected behaviour: Test runs with no exception
- Actual behaviour: The TDDs are failing with exception
- Fix version: Sonata 16.2
- Status: Closed

Citation: Jira: BASE-460256 — TDD Failures for SaveEmployerTest and GetEmployerTest Classes

---

## Q: What exception does BASE-460272 report during the CreateEmployerAccount SBS request?
*Jira defect detail · citation present: YES*

## BASE-460272 Exception Details

During the `CreateEmployerAccount` SBS request, the SOAP call returns an **HTTP 500 Internal Server Error** with a fault chain (7 layers) rooted in a `StackOverflowError`:

1. `ServiceException: BRA-154165` - Service failed
2. `TechnicalException: BRA-190078` - Error in `bravura.sonata.scheme.setup.EmployersearchDO#retrieve()`
3. `TechnicalException: BRA-190080` - Error invoking the reflective method `EmployersearchDO.retrieve(...)` (throws `bravura.commons.LayeredException`)
4. `TechnicalException: BRA-001` - A technical error occurred; refer to next layer/stacktrace
5. `StackOverflowError: BRA-003` - `java.lang.StackOverflowError`
6. `Exception: BRA-003` - `java.lang.Exception: java.lang.reflect.InvocationTargetException`
7. `UndeclaredThrowableException: BRA-003` - `java.lang.reflect.UndeclaredThrowableException`

So the root cause propagating up through the layered exception is a **`java.lang.StackOverflowError`** occurring inside `EmployersearchDO#retrieve()`, which is wrapped by reflection-related exceptions (`InvocationTargetException`, `UndeclaredThrowableException`) before surfacing as a generic `ServiceException (BRA-154165 - Service failed)` at the SOAP fault level, instead of the expected successful account creation response.

Citation: Jira: BASE-460272 — SBS_SMOKE : Throwing exception 'TechnicalException: BRA-190078 - Error in bravura.sonata.scheme.setup.EmployersearchDO#retrieve()' during run 'CreateEmployerAccount' SBS request

---

## Q: What is the status of the schema-change ticket BASE-458911?
*Jira status lookup · citation present: YES*

**BASE-458911** — Status: **Closed** (fix version: Sonata 16.2)

This SBS Schema Change ticket adds a new optional element `pagingRange` (type `PagingRangeType`) to the `searchEmployer` operation, supporting pagination for higher Employer volumes. It's linked to issues BASE-458834, BASE-458835, and BASE-460238.

Citation: Jira: BASE-458911 — Sonata Business Services (SBS) - Operation searchEmployer added with optional element pagingRange (type PagingRangeType) to support pagination for higher Employer volumes, ensuring search flexibility

---

API usage: 17 calls · 87,933 input · 4,357 output · 29,988 cache-read