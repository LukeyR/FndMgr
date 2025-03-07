# FundMgr

## Assumptions made
* Amount and inception date CANNOT be null (the example csv has invalid test cases that should be rejected)
* We should actually create 3 models for Fund one Fund Management could have many strategies, likewise (more arguable) multiple strategy types could be used by many funds managements
* I use `ignore_conflicts=True` which wouldn't work in a PSQL setting, but works in a sqlite setting
* Duplicates are not allowed (objects reused rather than recreating)
* If 1 row is wrong, it is wrong in isolation. Rest of CSV is still valid and other records are passed as normal (subject to their correctness)



