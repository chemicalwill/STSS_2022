#!/usr/bin/env python3

from math import sqrt 
import warnings

import numpy as np
from scipy.stats import fisher_exact


def fisher_exact_results_dict(a, b, c, d):
    
    table = np.array([
        [a, b],
        [c, d]
    ])

    oddsr, pval = fisher_exact(table)
    oddsr = round(oddsr, 2)
    pval = "{:0.2e}".format(pval)
    
    try:
        lowerci = np.exp(np.log(oddsr) - 1.96 * sqrt(1/a + 1/b + 1/c + 1/d))
        upperci = np.exp(np.log(oddsr) + 1.96 * sqrt(1/a + 1/b + 1/c + 1/d))
        lowerci, upperci = round(lowerci, 2), round(upperci, 2)
    except ZeroDivisionError:
        lowerci, upperci = None, None
    finally:
        return {"OR": oddsr, "p-value": pval, "95% CI": f"{lowerci} - {upperci}"}


# suppress RuntimeWarning for zero division
#   Sarah's A groups for Fisher Exact have 0 when calculating CI
warnings.filterwarnings("ignore", category=RuntimeWarning)

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
rate_of_gpc_contam = fisher_exact_results_dict(64, 266, 69, 823)

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
rate_of_chf_exac = fisher_exact_results_dict(12, 27, 50, 100)

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
rate_of_cv_death = fisher_exact_results_dict(0, 2, 62, 127)

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
death_from_any_cause = fisher_exact_results_dict(0, 10, 62, 127)

### SEAN ###

