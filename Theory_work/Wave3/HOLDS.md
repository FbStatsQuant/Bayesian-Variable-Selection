# Wave 3 hold file (PROTOCOL rule 12, fail-closed holds)

Format: `HOLD <claim id | P6> <UTC time> <source> <finding>`; HQ lifts with `LIFT <id> <time> <disposition>`.
Leads read this file (main checkout) before every step.

