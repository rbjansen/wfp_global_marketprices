""" Data utilities. """


def latlon_to_gid(lat, lon):
    """ Get gid from lat/lon. """
    lat_component =  ((((90 + (np.floor(lat * 2) / 2)) * 2) + 1) - 1) * 720
    lon_component =  ((180 + (np.floor(lon * 2) / 2)) * 2)
    gid = lat_component + lon_component + 1
    return gid
    

def ym_to_month_id(year, month):
    """ Get month_id from year/month. """
    # Start is 1/1/1980, so compute months since.
    year_component = (year - 1980) * 12
    month_id = year_component + month
    return month_id    
