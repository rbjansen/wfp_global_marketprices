"""Plot a selection of maps."""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

MARKETS = pd.read_csv("./data/markets.csv")


def map_market_locations(markets, path):
    """Map WFP market locations."""
    world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
    gdf = gpd.GeoDataFrame(
        markets, geometry=gpd.points_from_xy(markets.lon, markets.lat)
    )

    _, ax = plt.subplots(figsize=(25, 20))
    world.plot(ax=ax, color="white", edgecolor="black")
    gdf.plot(ax=ax, color="red", markersize=1)
    plt.savefig(path, dpi=200, bbox_inches="tight")


if __name__ == "__main__":
    map_market_locations(MARKETS, "./markets.png")
