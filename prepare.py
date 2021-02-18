"""Data prep: extend food price data with mkt lon/lat and exchange rates."""

import time
import pandas as pd
import requests

from hdx.location.country import Country


def get_markets(df, adm_col="adm0_code"):
    """Fetch market features from VAM WFP API."""

    json_arr = {}

    for adm in df[adm_col].unique():
        time.sleep(1)
        print(f"Collecting markets for {adm}...")
        response = requests.get(
            f"https://dataviz.vam.wfp.org/API/GetMarkets?ac={str(int(adm))}"
        )
        output = response.json()
        for region in output:
            if region["text"] != "National Average":  # TODO.
                for mkt in region["items"]:
                    json_arr[int(mkt["id"].replace("mk", ""))] = {
                        "lat": mkt["lat"],
                        "lon": mkt["lon"],
                    }

    out = pd.DataFrame(json_arr).T
    out.index.name = "mkt_id"

    return out


def get_exchange_rates(df, name_col="adm0_name"):
    """Fetch exchange rates from VAM WFP API."""

    out = pd.DataFrame()  # Empty dataframe to concatenate into.

    for adm in df[name_col].unique():
        time.sleep(1)
        print(f"Collecting exchange rates for {adm}...")
        iso3, _ = Country.get_iso3_country_code_fuzzy(adm)  # Slow.
        url = f"https://vam.wfp.org/API/Get.aspx?q=9&iso3={iso3}"  # q9 forex.
        response = requests.get(url)

        try:  # Some are empty.
            df = pd.DataFrame(response.json())
            df = df[df["ind"].str.contains("USD")]  # Limit to USD.

            # Add year, month.
            df["date"] = pd.to_datetime(df["date"], infer_datetime_format=True)
            df["mp_year"] = df["date"].dt.year
            df["mp_month"] = df["date"].dt.month

            # Prepare the median monthly exchange rate. Main dataset is monthly.
            df = pd.DataFrame(
                df.groupby(["mp_year", "mp_month"])["val"].median()
            )

            # Append country to index.
            df["adm0_name"] = adm
            df.set_index("adm0_name", append=True, inplace=True)
            df.index.names = ["mp_year", "mp_month", "adm0_name"]

            # Concatenate.
            out = pd.concat([out, df])
        except Exception:
            print(f"[FAILED] to get exchange rates for {adm}!")

    return out


def extend_wfpfp():
    """Fetch wfpvam from HDX. TODO"""

    df = pd.read_csv("./data/wfp-food-prices.csv")
    df = df.loc[df.mkt_name != "National Average"]

    countries = pd.read_csv("./data/wfp-countries.csv")
    countries.columns = [col.lower() for col in countries]

    # Left merge market locations.
    markets = get_markets(countries)
    print("Merging in market locations...")
    df = df.merge(markets.reset_index(), on="mkt_id", how="left")

    # Left merge in exchange rates.
    exchange = get_exchange_rates(df)
    print("Merging in exchange rates...")
    df = df.merge(
        exchange.reset_index(),
        on=["mp_year", "mp_month", "adm0_name"],
        how="left",
    )

    # Clean up produce labels.
    df["cm_name"].apply(lambda x: x.split(" - ")[0])

    return df


if __name__ == "__main__":
    print()
    extend_wfpfp()
