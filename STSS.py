#!/usr/bin/env python3

import numpy as np
from scipy.stats import fisher_exact


def print_fisher_exact_results(table):
    oddsratio, pvalue = fisher_exact(table)
    if pvalue < 0.05:
        pvalue = "< 0.05"
    else:
        pvalue = round(pvalue, 2)
        pvalue = f"= {pvalue}"
    oddsratio = round(oddsratio, 2)
    print(f"OR = {oddsratio}, p {pvalue}")
    return


### SETH ###
"""
PRIMARY OUTCOME
        +----------+----------+
        | COVID19+ | COVID19- | 
        +----------+----------+
    +BCC|    64    |   266    |
        +----------+----------+
    -BCC|    69    |   823    |
        +----------+----------+
"""
print_fisher_exact_results(np.array([
    [64, 266],
    [69, 823]
]))

### SARAH ###
""" 
PRIMARY OUTCOME
        +-----------+-----------+
        | SGLT2+S/V | S/V ALONE |
        +-----------+-----------+
    CHF |    (A)    |    (B)    |
    EXAC|    12          27     |
        +-----------+-----------+
    NO  |    (C)    |    (D)    |
    EXAC|    50          100    |
        +-----------+-----------+
"""
print_fisher_exact_results(np.array([
    [12, 27],
    [50, 100]
]))

"""
SECONDARY - CV DEATH
        +-----------+-----------+
        | SGLT2+S/V | S/V ALONE |
CV DEATH+-----------+-----------+
    YES |     0     |     2     |
        +-----------+-----------+
    NO  |    62     |    127    |
        +-----------+-----------+
"""

"""
SECONDARY - OVERALL DEATH
        +-----------+-----------+
        | SGLT2+S/V | S/V ALONE |
DEATH   +-----------+-----------+
    YES |     0     |     10    |
        +-----------+-----------+
    NO  |    62     |    127    |
        +-----------+-----------+
"""

### SEAN ###
