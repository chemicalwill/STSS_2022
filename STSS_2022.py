#!/usr/bin/env python3

import os
from pathlib import Path
import warnings

os.chdir(Path(__file__).parent)
from resident import Resident


def write_out_results(fp, results_dict):
    with open(fp, "w") as f:
        f.write()
        for endpoint, result in results_dict.items():
            pass

"""
def write_out_results(fp, residents): # FIXME
    with open(fp, "w") as f:
        for resident in residents:
            for name, results in resident.items():
                f.write(name.title())
                for endpoint, result in results.items():
                    f.write(f"\n - {endpoint}:")
                    for stat, value in result.items():
                        f.write(f" {stat} {value},")
                f.write("\n\n")
    return
"""


def main():
    os.chdir(Path(__file__).parent)
    """
    # suppress RuntimeWarning for zero division
    #   ex. groups for Fisher's Exact Test div/0 when calculating 95% CI
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    # TODO see if this is necessary now that FET += 0.5 if 0
    """ 

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
    Sarah.get_fisher_exact_results_as_dict(50, 12, 100, 27)
    Sarah.get_barnard_exact_results_as_dict(62, 0, 125, 2)
    Sarah.get_barnard_exact_results_as_dict(62, 0, 117, 10)

    Sean = Resident("sean", "sean_data_cleaned.csv")
    # all data pulled from spreasheet, no tables to draw
    Sean.check_for_normalcy(0.05, "combo_time_delta")
    Sean.get_kruskall_wallis_results_as_dict("combo_batched_yn", "combo_time_delta")
    Sean.check_for_normalcy(0.05, "total_oic_visit_time")
    Sean.get_kruskall_wallis_results_as_dict("combo_batched_yn", "total_oic_visit_time")

    return


if __name__ == "__main__":
    main()
