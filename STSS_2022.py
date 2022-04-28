#!/usr/bin/env python3

from math import sqrt
import os
from pathlib import Path
import warnings

import numpy as np
import pandas as pd
from scipy import stats


def round_to_3_decimal_or_sci_places(pvalue):
    if pvalue < 0.001:
        return "{:0.2e}".format(pvalue)
    else:
        return round(pvalue, 3)


def check_for_normalcy(df, alpha, col):
    k2, p = stats.normaltest(df[col])
    if p < alpha:
        p = round_to_3_decimal_or_sci_places(p)
        print(f"{col} is normally distributed, p = {p}")
    else:
        p = round_to_3_decimal_or_sci_places(p)
        print(f"Warning: {col} is NOT normally distributed, p = {p}")
    return


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
        # TODO make these 2 lines build a dict rather than make 2 different ones
        return {"OR": odds_ratio, "p-value": pvalue}
    else:
        return {"OR": odds_ratio, "p-value": pvalue, "95% CI": f"{lowerci} - {upperci}"}
        

def extract_2_groups_from_df(df, group_col, value):
    a, b = sorted(df[group_col].unique())
    a = df.loc[df[group_col] == a, value]
    b = df.loc[df[group_col] == b, value]
    return (a, b)


def get_ag_results_as_dict(df, group_col, value):
    group1, group2 = extract_2_groups_from_df(df, group_col, value)
    # FIXME would like to figure out how to split up results
    return {"Alexander Govern results": stats.alexandergovern(group1, group2)}


def get_kruskall_wallis_results_as_dict(df, group_col, value):
    group1, group2 = extract_2_groups_from_df(df, group_col, value)
    kw_h_statistic, pvalue = stats.kruskal(group1, group2)
    kw_h_statistic = round(kw_h_statistic, 3)
    pvalue = round_to_3_decimal_or_sci_places(pvalue)   
    return {"Kruskall-Wallis H statistic": kw_h_statistic, "p-value": pvalue}


def get_one_way_anova_results_as_dict(df, group_col, value):
    group1, group2 = extract_2_groups_from_df(df, group_col, value)
    anova_stat, pvalue = stats.f_oneway(group1, group2)
    anova_stat = round(anova_stat, 3)
    pvalue = round_to_3_decimal_or_sci_places(pvalue)
    return {"One-Way ANOVA": anova_stat, "p-value": pvalue} 


def get_t_test_results_as_dict(df, group_col, value):
    # TODO
    group1, group2 = extract_2_groups_from_df(df, group_col, value)
    pass

def write_out_results(fp, residents):
    with open(fp, 'w') as f:
        for resident in residents:
            for name, results in resident.items():
                f.write(name.title())
                for endpoint, result in results.items():
                    f.write(f"\n - {endpoint}: ")
                    for stat, value in result.items():
                        f.write(f" {stat}: {value}, ")
                f.write("\n\n")
        
        # TODO remove the trailing commas...
    return


def seth():
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
    df = pd.read_csv('seth_data_cleaned.csv')
    check_for_normalcy(df, 0.05, "length_ofstay")
    length_of_stay = get_kruskall_wallis_results_as_dict(df, "covid_positive", "length_ofstay")
    return {
        "Seth": {
            "Rate of GP contamination": rate_of_gp_contam,
            "Rate of ECHO": rate_of_echo,
            "Length of stay": length_of_stay
        }
    }


def sarah():
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
    return {
        "Sarah": {
            "Rate of CHF exacerbation": rate_of_chf_exac,
            "Rate of CV death": rate_of_cv_death,
            "Death from any cause": death_from_any_cause
        }
    }


def sean():
    df = pd.read_csv('sean_data_cleaned.csv')
    check_for_normalcy(df, 0.05, "combo_time_delta")
    check_for_normalcy(df, 0.05, "total_oic_visit_time")
    premed_time = get_kruskall_wallis_results_as_dict(df, "combo_batched_yn", "combo_time_delta")
    oic_chair_time = get_kruskall_wallis_results_as_dict(df, "combo_batched_yn", "total_oic_visit_time")
    return {
        "Sean": {
            "Premed time": premed_time,
            "OIC chair time": oic_chair_time
        }
    }

def main():
    # suppress RuntimeWarning for zero division + move into project dir
    #   ex. Sarah's A groups for Fisher's Exact Test div/0 when calculating 95% CI
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    os.chdir(Path(__file__).parent)

    write_out_results('results.txt', [seth(), sarah(), sean()])
    return
    

if __name__ == "__main__":
    main()
