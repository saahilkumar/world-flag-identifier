import pandas as pd
from PIL import Image
import numpy as np
from skimage import measure
import imagehash
from .flag_util import FlagUtil
import operator
import os

class FlagIdentifier:

    def __init__(self):
        self.util = FlagUtil()
        
        self.flag_df = pd.read_csv(os.path.join(os.path.dirname(__file__), "flag_df.csv"), index_col = "country")
        self.flag_df["flag"] = self.flag_df["flag"].apply(self.util.makeArray)

    def get_flag_df(self):
        return self.flag_df.copy()

    def get_country_list(self):
        return list(self.get_flag_df().index.values)

    def display(self, country):
        self.get_flag_img(country).show()

    def get_flag_img(self, country):
        return Image.fromarray(self.flag_df["flag"].loc[country.title()])

    def flag_dist(self, countryA, countryB, method = "mse"):
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
        # credit to: https://www.pyimagesearch.com/2014/09/15/python-compare-two-images/
        err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
        err /= float(imageA.shape[0] * imageA.shape[1])

        return err

    def __hash(self, imageA, imageB):
        firsthash = imagehash.average_hash(Image.fromarray(imageA))
        otherhash = imagehash.average_hash(Image.fromarray(imageB))
        return firsthash - otherhash

    def __ssim(self, imageA, imageB):
        return measure.compare_ssim(imageA, imageB, multichannel = True)


    def closest_flag(self, country, method = "mse"):
        if method == "mse" or method == "hash":
            return self.__abstract_compare_flags(country.title(), operator.lt, method)
        elif method == "ssim":
            return self.__abstract_compare_flags(country.title(), operator.gt, method)
        else:
            raise ValueError("method must be one of: mse, ssim, or hash")


    def farthest_flag(self, country, method = "mse"):
        if method == "mse" or method == "hash":
            return self.__abstract_compare_flags(country.title(), operator.gt, method)
        elif method == "ssim":
            return self.__abstract_compare_flags(country.title(), operator.lt, method)
        else:
            raise ValueError("method must be one of: mse, ssim, or hash")

    def __abstract_compare_flags(self, country, op, method):
        # flag = self.flag_df["flag"].loc[country]
        best_dist = -1
        max_country = 0
        for c in self.flag_df.index:
            # cur_flag = self.flag_df["flag"].loc[c]
            dist = self.flag_dist(country, c, method = method)
            if (op(dist, best_dist) or best_dist == -1) and c != country:
                best_dist = dist
                max_country = c
                
        return max_country

    def identify(self, url, method = "mse"):
        if method == "mse":
            return self.__abstract_identify(url, self.__mse, operator.lt)
        elif method == "ssim":
            return self.__abstract_identify(url, self.__ssim, operator.gt)
        elif method == "hash":
            return self.__abstract_identify(url, self.__hash, operator.lt)
        else:
            raise ValueError("method must one of: mse, hash, ssim")

    def __abstract_identify(self, url, dist_func, op):
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