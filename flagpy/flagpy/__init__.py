from .flag_identifier import FlagIdentifier

# the identifier
id = FlagIdentifier()

def identify(url, method = "mse"):
    '''
    Uses the given method (either mse, ssim, or hash) to identify the flag that is most similar
    to the image linked to the provided url.

    Parameters
    ----------
    url : str
        The url linking to an image of a flag to be identified

    method : str
        The method (one of mse, ssim, or hash) used to identify the flag that the 
        image is representing

    Returns
    -------
    str
        A string of the country name whose flag is most similar to the given flag image
    '''
    return id.identify(url, method = method)

def closest_flag(country, method = "mse"):
    '''
    Returns the name of the country whose flag is most similar to the given 
    country.

    Parameters
    ----------
    country : str
        The name of the country
    
    method : str
        The method (one of mse, ssim, or hash) used to find the flag that is
        most similar to the one of the given country

    Returns
    -------
    str
        A string of the country name whose flag is most similar to that of the given country
        name
    '''
    return id.closest_flag(country, method = method)

def farthest_flag(country, method = "mse"):
    '''
    Returns the name of the country whose flag is least similar to the given
    country.

    Parameters
    ----------
    country : str
        The name of the country

    method : str
        The method (one of mse, ssim, or hash) used to find the flag that is 
        least similar to the one of the given country

    Returns
    -------
    str
        A string of the country name whose flag is least similar to that of the given country
        name
    '''
    return id.farthest_flag(country, method = method)

def display(country):
    '''
    Displays the flag of the given country.

    Parameters
    ----------
    country : str
        The name of the country whose flag is to be displayed
    '''
    id.display(country)

def get_flag_img(country):
    '''
    Returns an Image object representing the flag of the given country name.

    Parameters
    ----------
    country : str
        The name of the country

    Returns
    -------
    Image
        an image object representing the flag of the given country name.
    '''
    return id.get_flag_img(country)

def get_flag_df():
    '''
    Returns a DataFrame of all the country names and their corresponding flags.

    Returns
    -------
    DataFrame
        A DataFrame of all the country names and their corresponding flags
    '''
    return id.get_flag_df()

def get_country_list():
    '''
    Returns a list of all 195 country names.

    Returns
    -------
    list
        A list of all the country names
    '''
    return id.get_country_list()

def flag_dist(countryA, countryB, method = "mse"):
    '''
    Gets the distance between the flags of the two given countries
    using the given method (one of mse, ssim, or hash).

    Parameters
    ----------
    countryA : str
        The name of the first country

    countryB : str
        The name of the second country

    method : str
        The method (one of mse, ssim, or hash) used to find distance between the
        flags of the two given countries. For both mse and hash, smaller values mean higher 
        similarity and a value of 0 means the two flags are identical. For ssim, higher values mean 
        higher similarity and the value must be between -1 and 1. A value of 1 for ssim
        means the two flags are identical.

    Returns
    -------
    float
        The distance between the two flags of the two given countries
    '''
    return id.flag_dist(countryA, countryB, method)