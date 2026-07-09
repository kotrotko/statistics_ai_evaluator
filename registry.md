Here's the revised entry, adding the real-data validation without overstating the one variance blip:

---

**Registry Entry — cw13_1, Component 2**

- **Component / file:** Problem Statement, `cw13_1.py`
- **Rubricator (approved):** *Component 2. Problem Statement (4 points total): scored only if formulated in terms of research gap.*
- **Decision:** LLM-alone (no code-level override). Rejected the earlier-gate override proposal after prompt-only tests passed.
- **Test case that justified it:** Mixed gap+aim answer — *"...it is unclear whether spending more time leads to higher final course scores. This study examines whether study hours can predict..."* — scored 4/4, correctly treating the gap as sufficient and the aim as neutral, not disqualifying.
- **Real-answer validation:** 6 real student submissions manually reviewed; Component 2 scoring judged correct across all, including a case with garbled/degraded phrasing (gap clause still recognized).
- **Note:** one single-run scoring inconsistency observed on a synthetic aim-only test case, not reproduced on rerun; treated as model variance, not a rule defect.

---
