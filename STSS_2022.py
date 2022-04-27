#!/usr/bin/env python3

from math import sqrt
import pprint
import warnings

import numpy as np
import pandas as pd
from scipy import stats


def get_fisher_exact_results_as_dict(a, b, c, d):
    
    table = np.array([
        [a, b],
        [c, d]
    ])

    oddsr, pval = stats.fisher_exact(table)
    oddsr = round(oddsr, 2)
    if pval < 0.001:
        pval = "{:0.2e}".format(pval)
    else:
        pval = round(pval, 3)
    
    try:
        lowerci = np.exp(np.log(oddsr) - 1.96 * sqrt(1/a + 1/b + 1/c + 1/d))
        upperci = np.exp(np.log(oddsr) + 1.96 * sqrt(1/a + 1/b + 1/c + 1/d))
        lowerci, upperci = round(lowerci, 2), round(upperci, 2)
    except ZeroDivisionError:
        lowerci, upperci = None, None
    finally:
        return {"OR": oddsr, "p-value": pval, "95% CI": f"{lowerci} - {upperci}"}


# suppress RuntimeWarning for zero division
#   ex. Sarah's A groups for Fisher Exact have 0 when calculating CI
warnings.filterwarnings("ignore", category=RuntimeWarning)

### SETH ###
"""
PRIMARY OUTCOME - RATE OF GP CONTAM.
        +----------+----------+
        | COVID19+ | COVID19- | 
        +----------+----------+   
    +BCC|    64    |   266    |
        +----------+----------+
    -BCC|    69    |   823    |
        +----------+----------+

SECONDARY OUTCOME - RATE OF ECHO
        +----------+----------+
        | COVID19+ | COVID19- | 
        +----------+----------+
    ECHO|    1     |   17     |
        +----------+----------+
    NONE|    63    |   249    |
        +----------+----------+

"""
rate_of_gp_contam = get_fisher_exact_results_as_dict(64, 266, 69, 823)
rate_of_echo = get_fisher_exact_results_as_dict(1, 17, 63, 249)
length_of_stay = {}
# TODO LENGTH OF STAY - t-test
seth_results = {
    "Rate of GP contamination": rate_of_gp_contam,
    "Rate of ECHO": rate_of_echo,
    "Length of stay": length_of_stay
}

print(pprint.pformat(seth_results))

### SARAH ###
""" 
PRIMARY OUTCOME - CHF EXAC
        +-----------+-----------+
        | SGLT2+S/V | S/V ALONE |
        +-----------+-----------+
    EXAC|    12          27     |
        +-----------+-----------+
    NONE|    50          100    |
        +-----------+-----------+

SECONDARY OUTCOME - CV DEATH
        +-----------+-----------+
        | SGLT2+S/V | S/V ALONE |
        +-----------+-----------+
    DEAD|     0     |     2     |
        +-----------+-----------+
    LIVE|    62     |    127    |
        +-----------+-----------+

SECONDARY - OVERALL DEATH
        +-----------+-----------+
        | SGLT2+S/V | S/V ALONE |
        +-----------+-----------+
    DEAD|     0     |     10    |
        +-----------+-----------+
    LIVE|    62     |    127    |
        +-----------+-----------+
"""
rate_of_chf_exac = get_fisher_exact_results_as_dict(12, 27, 50, 100)
rate_of_cv_death = get_fisher_exact_results_as_dict(0, 2, 62, 127)
death_from_any_cause = get_fisher_exact_results_as_dict(0, 10, 62, 127)
# TODO secondary change in average SCr @ admit
sarah_results = {
    "Rate of CHF exacerbation": rate_of_chf_exac,
    "Rate of CV death": rate_of_cv_death,
    "Death from any cause": death_from_any_cause
}
print(pprint.pformat(sarah_results))

### SEAN ###
# TODO avg time from oe_time to combo given - primary (paired/t-test)
# TODO secondary - total oic time (in hours) (paired/t-test)
