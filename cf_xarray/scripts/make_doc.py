#!/usr/bin/env python

import argparse
import os

from pandas import DataFrame

from cf_xarray.accessor import _AXIS_NAMES, _COORD_NAMES
from cf_xarray.criteria import coordinate_criteria, regex


def main():
    """
    Generate _build/csv/ with all additional files needed to build cf-xarray documentation.
    """

    make_criteria_csv()
    make_regex_csv()


def make_criteria_csv():
    """
    Make criteria tables:
        _build/csv/{all,axes,coords}_criteria.csv
    """

    csv_dir = "_build/csv"
    os.makedirs(csv_dir, exist_ok=True)

    # Criteria tables
    df = DataFrame.from_dict(coordinate_criteria)
    df = df.dropna(1, how="all")
    df = df.applymap(lambda x: ", ".join(sorted(x)) if isinstance(x, tuple) else x)
    df = df.sort_index(0).sort_index(1)

    # All criteria
    df.to_csv(os.path.join(csv_dir, "all_criteria.csv"))

    # Axes and coordinates
    for keys, name in zip([_AXIS_NAMES, _COORD_NAMES], ["axes", "coords"]):
        subdf = df.loc[sorted(keys)].dropna(1, how="all")
        subdf = subdf.dropna(1, how="all").transpose()
        subdf.to_csv(os.path.join(csv_dir, f"{name}_criteria.csv"))


def make_regex_csv():
    """
    Make regex tables:
        _build/csv/all_regex.csv
    """

    csv_dir = "_build/csv"
    os.makedirs(csv_dir, exist_ok=True)
    df = DataFrame(regex, index=[0])
    df = df.applymap(lambda x: f"``{x}``")
    df = df.sort_index(1).transpose()
    df.to_csv(os.path.join(csv_dir, "all_regex.csv"), header=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Generate _build/csv/ with all additional files"
            " needed to build cf-xarray documentation."
        ),
    )
    parser.parse_args()
    main()
