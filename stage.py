"""Stage VAM WFP to cm and pgm."""

import pandas as pd

from utilities import latlon_to_gid, ym_to_month_id


# TODO: cm.
def stage_pgm_wfpfp():
    """Stage market food price data to pgm."""
    # Get month_id and pg_id in.
    df = df.dropna(subset=["lat", "lon"])  # Drop rows with no coords.
    df["pg_id"] = latlon_to_gid(df["lat"], df["lon"])
    df["month_id"] = ym_to_month_id(df["mp_year"], df["mp_month"])

    # Pivot to priogrid-month.
    df = pd.pivot_table(
        df,
        index=["month_id", "pg_id"],
        columns=["cm_name"],
        values="mp_price",
        dropna=True,
        aggfunc="mean",
    )

    return df


if __name__ == "__main__":
    df = stage_pgm_wfpfp()
    df.to_csv("./wfp-food-prices-pgm.csv")
    print("Finished staging food price data.")
