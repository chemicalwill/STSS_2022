#!/usr/bin/env python3

import numpy as np
from scipy.stats import fisher_exact


def print_fisher_exact_results(header, table):
    oddsratio, pvalue = fisher_exact(table)
    print(f"{header.title()}: OR = {oddsratio}, p = {pvalue}")
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
print_fisher_exact_results("rate of GPC contamination", np.array([
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
print_fisher_exact_results("CHF exacerbations", np.array([
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
print_fisher_exact_results("cardiovascular death", np.array([
    [0, 2],
    [62, 117]
]))
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
print_fisher_exact_results("death from any cause", np.array([
    [0, 19],
    [62, 127]
]))
### SEAN ###
