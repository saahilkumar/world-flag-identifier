from .flag_identifier import FlagIdentifier

id = FlagIdentifier()

def identify(url, method = "mse"):
    """
    Uses the given method (either mse, ssim, or hash) to find the flag that is most similar
     to the image that the given url links to.
    """
    return id.identify(url, method = method)

def closest_flag(country):
    return id.closest_flag(country)

def farthest_flag(country):
    return id.farthest_flag(country)

def display(country):
    id.display(country)

def get_flag_img(country):
    return id.get_flag_img(country)

def get_flag_df():
    return id.get_flag_df()

def get_country_list():
    return id.get_country_list()

def flag_dist(countryA, countryB, method = "mse"):
    return id.flag_dist(countryA, countryB, method)