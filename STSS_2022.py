#!/usr/bin/env python3

import os
from pathlib import Path

os.chdir(Path(__file__).parent)
from resident import Resident


### SETH ###
"""
PRIMARY OUTCOME - RATE OF GP CONTAM.
        +------+------+
        | BCC- | BCC+ |
        +------+------+
COVID19+|  69  |  64  |
        +------+------+
COVID19-| 823  | 266  |
        +------+------+

SECONDARY OUTCOME - RATE OF ECHO
        +-------+-------+
        | ECHO- | ECHO+ |
        +-------+-------+
COVID19+|   63  |   1   |
        +-------+-------+
COVID19-|  249  |  17   |
        +-------+-------+
"""
Seth = Resident("seth", "seth_data_cleaned.csv")
Seth.get_fisher_exact_results_as_dict("rate of GP contam.", 69, 64, 823, 266)
Seth.get_fisher_exact_results_as_dict("rate of ECHO", 63, 1, 249, 17)
Seth.check_for_normalcy(0.05, "length_ofstay")
Seth.get_kruskall_wallis_results_as_dict(
    "length of stay", "covid_positive", "length_ofstay"
)


### SARAH ###
"""
PRIMARY OUTCOME - CHF EXAC
        +---------+---------+
        | NO EXAC |  EXACS  |
        +---------+---------+
COMBO TX|    50   |    12   |
        +---------+---------+
SGLT2 TX|   100   |    27   |
        +---------+---------+

SECONDARY OUTCOME - CV DEATH
        +-------+------+
        | ALIVE | DEAD |
        +-------+------+
COMBO TX|   62  |   0  |
        +-------+------+
S/V MONO|  125  |   2  |
        +-------+------+

SECONDARY - OVERALL DEATH
        +-------+------+
        | ALIVE | DEAD |
        +-------+------+
COMBO TX|   62  |   0  |
        +-------+------+
S/V MONO|  117  |  10  |
        +-------+------+
"""
Sarah = Resident("sarah")
Sarah.get_fisher_exact_results_as_dict("chf exacerbations", 50, 12, 100, 27)
Sarah.get_barnard_exact_results_as_dict("cv death", 62, 0, 125, 2)
Sarah.get_barnard_exact_results_as_dict("death from any cause", 62, 0, 117, 10)


### SEAN ###
Sean = Resident("sean", "sean_data_cleaned.csv")
# all data pulled from spreadsheet, no tables to draw
Sean.check_for_normalcy(0.05, "combo_time_delta")
Sean.get_kruskall_wallis_results_as_dict("premed admin time", "combo_batched_yn", "combo_time_delta")
Sean.check_for_normalcy(0.05, "total_oic_visit_time")
Sean.get_kruskall_wallis_results_as_dict("total oic visit time", "combo_batched_yn", "total_oic_visit_time")
