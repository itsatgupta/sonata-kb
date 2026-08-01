# Feature-1 Sign-off Demo — searchEmployer SBS pagination (RLSI-6059, Sonata 16.2)

Curated live demo for the phase-0 exit sign-off (SME: Pratigya). Eight questions chosen to show the
breadth of what the assistant handles: direct spec lookup, defaults, explanation, before/after delta,
a negative/out-of-scope case, and Jira lifecycle lookups.

All 27 eval questions graded **Correct (100%)** by the SME; this is a representative subset to watch
live. Run it with `venv/Scripts/python.exe demo/demo_run.py` (from `03-poc/agent`).

| # | Question | Expected citation | Expected answer | Demonstrates |
|---|---|---|---|---|
| 1 | What does the optional `pagingRange` element do in the searchEmployer operation? | Wiki § SFC-04 | Divides results into pages via first row + page size | Direct spec lookup |
| 2 | What is the default number of results per page if `pagingRange` is not supplied? | Wiki § SFC-04 | 20 results per page | Default behavior |
| 3 | Why was pagination added to the searchEmployer operation? | Wiki + Jira | Scalability at high employer volumes; Workplace Pension driver; HMRC alignment | Explanation synthesis |
| 4 | Would a client that calls searchEmployer without `pagingRange` see a change in behaviour? | Wiki § SFC-04 | No — element is optional; default 20/page from index 1 applies | Backward compatibility / delta |
| 5 | Does the searchEmployer pagination change return Employer External References in the response? | Wiki (struck-through) | No — returning external refs was dropped from scope | Negative / out-of-scope |
| 6 | What defect reports 14 failing TDDs for the SaveEmployerTest and GetEmployerTest classes? | Jira: BASE-460256 | BASE-460256 | Jira lifecycle lookup |
| 7 | What exception does BASE-460272 report during the CreateEmployerAccount SBS request? | Jira: BASE-460272 | TechnicalException BRA-190078 in EmployersearchDO#retrieve | Jira defect detail |
| 8 | What is the status of the schema-change ticket BASE-458911? | Jira: BASE-458911 | Closed | Jira status lookup |

Every answer must carry a `Wiki:` or `Jira:` citation — that is the point of the demo.
