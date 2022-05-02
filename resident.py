#!/usr/bin/env python3

from math import sqrt

import numpy as np
import pandas as pd
from scipy import stats


def round_to_3_decimal_or_sci_places(pvalue):
    if pvalue < 0.001:
        return "{:0.2e}".format(pvalue)
    else:
        return round(pvalue, 3)


def extract_2_groups_from_df(df, group_col, outcome_value):
    a, b = sorted(df[group_col].unique())
    a_rows = df.loc[[group_col] == a, outcome_value]
    b_rows = df.loc[df[group_col] == b, outcome_value]
    return (a_rows, b_rows)


class Resident:
    def __init__(self, residents_name, fp=None):
        self.name = residents_name.title()
        self.df = pd.read_csv(fp)
        self.results = {}

    def check_for_normalcy(self, alpha, col):
        k2, p = stats.normaltest(self.df[col])
        if p < alpha:
            p = round_to_3_decimal_or_sci_places(p)
            print(f"{col} is normally distributed, p = {p}")
        else:
            p = round_to_3_decimal_or_sci_places(p)
            print(f"Warning: {col} is NOT normally distributed, p = {p}")

    def get_fisher_exact_results_as_dict(self, endpoint, a, b, c, d):
        table = np.array([[a, b], [c, d]])
        if any([a == 0, b == 0, c == 0, d == 0]):
            a += 0.5
            b += 0.5
            c += 0.5
            d += 0.5
        odds_ratio, pvalue = stats.fisher_exact(table)
        odds_ratio = round(odds_ratio, 2)
        pvalue = round_to_3_decimal_or_sci_places(pvalue)
        lowerci = np.exp(
            np.log(odds_ratio) - 1.96 * sqrt(1 / a + 1 / b + 1 / c + 1 / d)
        )
        upperci = np.exp(
            np.log(odds_ratio) + 1.96 * sqrt(1 / a + 1 / b + 1 / c + 1 / d)
        )
        lowerci, upperci = round(lowerci, 2), round(upperci, 2)
        self.results[endpoint.title()] = {
            "OR (Fisher Exact Test)": odds_ratio,
            "p-value": pvalue,
            "95% CI": f"{lowerci} - {upperci}",
        }

    def get_ag_results_as_dict(self, endpoint, group_col, outcome_value):
        group1, group2 = extract_2_groups_from_df(self.df, group_col, outcome_value)
        res = stats.alexandergovern(group1, group2)
        self.results[endpoint.title()] = {
            "Alexander Govern statistic": res.statistic,
            "p-value": res.pvalue,
        }

    def get_barnard_exact_results_as_dict(self, endpoint, a, b, c, d):
        table = np.array([[a, b], [c, d]])
        ber = stats.barnard_exact(table)
        stat = round(ber.statistic, 3)
        p = round_to_3_decimal_or_sci_places(ber.pvalue)
        self.results[endpoint.title()] = {"Barnard Exact statistic": stat, "p-value": p}

    def get_kruskall_wallis_results_as_dict(self, endpoint, group_col, outcome_value):
        group1, group2 = extract_2_groups_from_df(self.df, group_col, outcome_value)
        kw_h_statistic, pvalue = stats.kruskal(group1, group2)
        kw_h_statistic = round(kw_h_statistic, 3)
        pvalue = round_to_3_decimal_or_sci_places(pvalue)
        self.results[endpoint.title()] = {
            "Kruskall-Wallis H statistic": kw_h_statistic,
            "p-value": pvalue,
        }

    def get_one_way_anova_results_as_dict(self, endpoint, group_col, outcome_value):
        group1, group2 = extract_2_groups_from_df(self.df, group_col, outcome_value)
        anova_stat, pvalue = stats.f_oneway(group1, group2)
        anova_stat = round(anova_stat, 3)
        pvalue = round_to_3_decimal_or_sci_places(pvalue)
        self.results[endpoint.title()] = {"One-Way ANOVA": anova_stat, "p-value": pvalue}

    def get_t_test_results_as_dict(self, group_col, outcome_value):
        # TODO
        group1, group2 = extract_2_groups_from_df(self.df, group_col, outcome_value)
        pass


# TODO move normalcy check into paramentric tests, and only throw message if not a normal distribution?
