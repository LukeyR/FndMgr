# FundMgr

## Assumptions made
* Amount and inception date CANNOT be null (the example csv has invalid test cases that should be rejected)
* We should actually create 3 models for Fund one Fund Management could have many strategies, likewise (more arguable) multiple strategy types could be used by many funds managements
* I use `ignore_conflicts=True` which wouldn't work in a PSQL setting, but works in a sqlite setting



