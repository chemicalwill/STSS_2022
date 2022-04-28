#!/usr/bin/env python3

from math import sqrt
import pprint
import warnings

import numpy as np
import pandas as pd
from scipy import stats


def round_to_3_decimal_or_sci_places(pvalue):
    if pvalue < 0.001:
        return "{:0.2e}".format(pvalue)
    else:
        return round(pvalue, 3)


def get_fisher_exact_results_as_dict(a, b, c, d):
    table = np.array([
        [a, b],
        [c, d]
    ])
    odds_ratio, pvalue = stats.fisher_exact(table)
    odds_ratio = round(odds_ratio, 2)
    pvalue = round_to_3_decimal_or_sci_places(pvalue)
    
    try:
        lowerci = np.exp(np.log(odds_ratio) - 1.96 * sqrt(1/a + 1/b + 1/c + 1/d))
        upperci = np.exp(np.log(odds_ratio) + 1.96 * sqrt(1/a + 1/b + 1/c + 1/d))
        lowerci, upperci = round(lowerci, 2), round(upperci, 2)
    except ZeroDivisionError:
        # lowerci, upperci = None, None
        return {"OR": odds_ratio, "p-value": pvalue}
    else:
        return {"OR": odds_ratio, "p-value": pvalue, "95% CI": f"{lowerci} - {upperci}"}
        

def get_kruskall_wallis_results_as_dict(df, col1, col2):
    statistic, pvalue = stats.kruskal(df[col1], df[col2])
    statistic = round(statistic, 3)
    pvalue = round_to_3_decimal_or_sci_places(pvalue)
    return {"statistic": statistic, "p-value": pvalue}


# suppress RuntimeWarning for zero division
#   ex. Sarah's A groups for Fisher's Exact Test div/0 when calculating 95% CI
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
"""
# TODO
df = pd.read_csv('/path/to/seths/data')
length_of_stay = get_kruskall_wallis_results_as_dict(df, col1, col2)
"""
seths_results = {
    "Rate of GP contamination": rate_of_gp_contam,
    "Rate of ECHO": rate_of_echo,
    "Length of stay": {} # length_of_stay
}

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
sarahs_results = {
    "Rate of CHF exacerbation": rate_of_chf_exac,
    "Rate of CV death": rate_of_cv_death,
    "Death from any cause": death_from_any_cause
}
print(pprint.pformat(sarahs_results))

### SEAN ###
"""
df = pd.read_csv('/path/to/seans/data') # FIXME
premed_time = get_kruskall_wallis_results_as_dict(df, col1, col2)
oic_chair_time = get_kruskall_wallis_results_as_dict(df, col1, col2)
seans_results = {
    "Primary endpoint": premed_time,
    "OIC chair time": oic_chair_time
}
"""