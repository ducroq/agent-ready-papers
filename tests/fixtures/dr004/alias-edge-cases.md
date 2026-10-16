# DR-004 alias edge cases (test fixture)

Parity fixture for the v5 alias path: every row here is one master's tools read
in a particular way, and the branch must give the same exit codes and finding
counts (new behaviour may only add notes). See tests/test_v5_parity.py.

**claims:**

| ID | Statement | Priority | Confidence | Source | Source Tier | Status |
|----|-----------|----------|------------|--------|-------------|--------|
| S9-1 | under a near-miss marker: master drops this table | P0 | EMERGING | x | A | [ ] |

**CLAIMs:**

| ID | Statement | Priority | Confidence | Source | Source Tier | Status |
|----|-----------|----------|------------|--------|-------------|--------|
| S1-1 | a fact | P0 | SUPPORTED | Smith 2020 | A | [x] |
| **S1-2** | a decorated ID | P1 | SUPPORTED | x | A | [x] |
| SN-1 | a letter ID, as in the template | P1 | EMERGING | x | F | [x] |
| S1-3a | a suffixed ID | P1 | EMERGING | x | A | [x] |
| C1 | a DR-027-style ID in a DR-004 table | P1 | EMERGING | x | A | [x] |
| S1-5a |
| C2 |

**ARGUMENTs** (Toulmin):

| ID | Statement | Priority | Confidence | Grounds | Warrant | Rebuttal | Source | Source Tier | Status |
|----|-----------|----------|------------|---------|---------|----------|--------|-------------|--------|
| S1-1 | the same ID in a second sub-table | P0 | SUPPORTED | S1-3a; Smith's model C2 and phase D1 | w | r | Own | F | [x] |
| S2-1 | an argument | P1 | EMERGING | S1-1 | w | r | Own | F | [x] |

**PROVOCATIONs** (Auger):

| ID | Provocation | Tier | Status |
|----|-------------|------|--------|
| PV-1 | a provocation with a non-S ID | GROUNDED | [x] |
| S3-1 | a provocation | EXTRAPOLATED | [ ] |
