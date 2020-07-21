import pandas as pd
from PIL import Image
import numpy as np
from skimage import metrics
import imagehash
from .flag_util import FlagUtil
import operator
import os

class FlagIdentifier:

    def __init__(self):
        '''
        Initializes a FlagIdentifier object that has a FlagUtil object and DataFrame of 
        countries and their flags.
        '''
        self.util = FlagUtil()
        
        # reading in a df of file names which store numpy arrays
        self.flag_df = pd.read_csv(os.path.join(os.path.dirname(__file__), "flag_df.csv"), index_col = "country")

        # converting the files to numpy arrays
        self.flag_df["flag"] = self.flag_df["flag"].apply(self.util.makeArray)

    def get_flag_df(self):
        '''
        Returns a copy of this FlagIdentifier's flag DataFrame.

        Returns
        -------
        DataFrame
            A copy of this FlagIdentifier's flag DataFrame
        '''
        return self.flag_df.copy()

    def get_country_list(self):
        '''
        Returns a list of all 195 current countries stored in this FlagIdentifier's DataFrame

        Return
        ------
        list
            A list of all the countries in this FlagIdentifier's DataFrame
        '''
        return list(self.get_flag_df().index.values)

    def display(self, country):
        '''
        Displays the flag of the given country.

        Parameters
        ----------
        country : str
            The country whose flag is to be displayed
        '''
        self.get_flag_img(country).show()

    def get_flag_img(self, country):
        '''
        Returns an Image object of the flag of the given country.

        Parameters
        ----------
        country : str
            The country whose flag is returned

        Returns
        -------
        Image
            An Image object of the flag of the given country
        '''
        return Image.fromarray(self.flag_df["flag"].loc[country.title()])

    def flag_dist(self, countryA, countryB, method = "mse"):
        '''
        Uses the given method (one of mse, ssim, or hash) to find the distance
        between the two flags of the two given countries.

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
        flagA = self.flag_df["flag"].loc[countryA.title()]
        flagB = self.flag_df["flag"].loc[countryB.title()]
        if method == "mse":
            return self.__mse(flagA, flagB)
        elif method == "ssim":
            return self.__ssim(flagA, flagB)
        elif method == "hash":
            return self.__hash(flagA, flagB)
        else:
            raise ValueError("method must be one of: mse, ssim, hash")

    def __mse(self, imageA, imageB):
        '''
        Returns the mean-squared error between the two given images. Lower values mean
        a higher similarity between the two images (0 is perfect similarity).

        Parameters
        ----------
        imageA : array
            A numpy array representing the first image

        imageB : array
            A numpy array representing the second image

        Returns
        -------
        float
            The mean-squared error between the two given images
        '''
        # credit to: https://www.pyimagesearch.com/2014/09/15/python-compare-two-images/
        err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
        err /= float(imageA.shape[0] * imageA.shape[1])

        return err

    def __hash(self, imageA, imageB):
        '''
        Returns the hash distance between the two given images. Lower values mean
        a higher similarity between the two images (0 is perfect similarity).

        Parameters
        ----------
        imageA : array
            A numpy array representing the first image

        imageB : array
            A numpy array representing the second image

        Returns
        -------
        int
            The hash distance between the two given images
        '''
        firsthash = imagehash.average_hash(Image.fromarray(imageA))
        otherhash = imagehash.average_hash(Image.fromarray(imageB))
        return firsthash - otherhash

    def __ssim(self, imageA, imageB):
        '''
        Returns the structural similarity index measure (ssim) 
        between the two given images. Higher values mean
        a higher similarity between the two images (1 is perfect similarity).

        Parameters
        ----------
        imageA : array
            A numpy array representing the first image

        imageB : array
            A numpy array representing the second image

        Returns
        -------
        float
            The structural similarity index measure (ssim) between the two given images
        '''
        return metrics.structural_similarity(imageA, imageB, multichannel=True)


    def closest_flag(self, country, method = "mse"):
        '''
        Returns the name of the country whose flag is most similar to the flag
        of the given country. Uses the given method to find the closest flag.

        Parameters
        ----------
        country : str
            The name of the country

        method : str
            The method (one of mse, ssim, or hash) used to find the flag that is
            most similar to that of the given country

        Returns
        -------
        str
            The name of the country whose flag is most similar to that of the given
            country
        '''
        if method == "mse" or method == "hash":
            return self.__abstract_compare_flags(country.title(), operator.lt, method)
        elif method == "ssim":
            return self.__abstract_compare_flags(country.title(), operator.gt, method)
        else:
            raise ValueError("method must be one of: mse, ssim, or hash")


    def farthest_flag(self, country, method = "mse"):
        '''
        Returns the name of the country whose flag is least similar to the flag
        of the given country. Uses the given method to find the farthest flag.

        Parameters
        ----------
        country : str
            The name of the country

        method : str
            The method (one of mse, ssim, or hash) used to find the flag that is
            least similar to that of the given country

        Returns
        -------
        str
            The name of the country whose flag is least similar to that of the given
            country
        '''
        if method == "mse" or method == "hash":
            return self.__abstract_compare_flags(country.title(), operator.gt, method)
        elif method == "ssim":
            return self.__abstract_compare_flags(country.title(), operator.lt, method)
        else:
            raise ValueError("method must be one of: mse, ssim, or hash")

    def __abstract_compare_flags(self, country, op, method):
        '''
        Finds the country whose flag is "closest" (according to the given operation)
        to the flag of the given country. Uses the given method to calculate the distance
        between flags.

        Parameters
        ----------
        country : str
            The name of the country

        op : operator
            The operator used to find the "closest" flag

        method : str
            The method (one of mse, ssim, or hash) used to find the distance between
            flags

        Returns
        -------
        str
            The name of the country whose flag is "closest" to the flag of the given
            country
        '''
        best_dist = -1
        max_country = 0
        for c in self.flag_df.index:
            dist = self.flag_dist(country, c, method = method)
            if (op(dist, best_dist) or best_dist == -1) and c != country:
                best_dist = dist
                max_country = c
                
        return max_country

    def identify(self, url, method = "mse"):
        '''
        Returns the name of the country whose flag is most similar to the flag 
        in the image represented by the given url.

        Parameters
        ----------
        url : str
            The url that links to an image of a flag to be identified

        method : str
            The method (one of mse, ssim, or hash) used to find the flag that 
            is most similar to the one in the image of the given url

        Returns
        -------
        str
            The name of the country whose flag is most similar to the one 
            represented by the url
        '''
        if method == "mse":
            return self.__abstract_identify(url, self.__mse, operator.lt)
        elif method == "ssim":
            return self.__abstract_identify(url, self.__ssim, operator.gt)
        elif method == "hash":
            return self.__abstract_identify(url, self.__hash, operator.lt)
        else:
            raise ValueError("method must one of: mse, hash, ssim")

    def __abstract_identify(self, url, dist_func, op):
        '''
        Returns the name of the country whose flag is most similar to the
        image represented by the url. Uses the given dist_func and operator to find the 
        closest flag.

        Parameters
        ----------
        url : str
            The url that links to an image of a flag to be identified

        dist_func : function
            A distance function (either mse, ssim, or hash) to find the closest
            flag to the one in the url

        op : operator
            The operator used to find the flag closest to the one represented
            by the url
        
        Returns
        -------
        str
            The name of the country whose flag is most similar to the one in the 
            image of the url
        '''
        flag = self.util.process_img(url)
        
        best_dist = -1
        closest_index = 0
        for c in self.flag_df.index:
            cur_flag = self.flag_df["flag"].loc[c]
            dist = dist_func(flag, cur_flag)

            if op(dist, best_dist) or best_dist == -1:
                best_dist = dist
                closest_index = c
                
        return closest_index