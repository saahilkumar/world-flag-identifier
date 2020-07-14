from bs4 import BeautifulSoup
import pandas as pd
from PIL import Image
import requests
from io import BytesIO
import numpy as np
import pickle

class FlagUtil:

    def __init__(self):
        self.color_dict = {}

    def pickle_numpy(self, arr, country_filename):
        with open('flags/' + country_filename + '.pkl','wb') as f:
            pickle.dump(arr, f)

    def get_web_safe_colors(self):
        lst = []
        for i in range(0, 256, 51):
            for j in range(0, 256, 51):
                for k in range(0, 256, 51):
                    tup = (i, j, k)
                    lst.append(tup)
                    
        return lst

    def find_nearest_color(self, color):
        if color in self.color_dict:
            return self.color_dict[color]
        
        web_safe = self.get_web_safe_colors()
        
        min_dist = 1000
        nearest_color = (0, 0, 0)
        for cur_col in web_safe:
            dist = sum(tuple(map(lambda i, j: abs(i - j), color, cur_col)))
            if dist < min_dist:
                min_dist = dist
                nearest_color = cur_col
                
        self.color_dict[color] = nearest_color
        return nearest_color

    def fix_image_color(self, img):
        # Get the size of the image
        width, height = img.size

        # Process every pixel
        for x in range(width):
            for y in range(height):
                current_color = img.getpixel( (x,y) )
                new_color = self.find_nearest_color(current_color)
                img.putpixel( (x,y), new_color)

    def process_img(self, url):
        # getting the image from the url
        response = requests.get(url)
        image_bytes = BytesIO(response.content)
        img = Image.open(image_bytes)
        
        # converting it to RGB
        img = img.convert("RGB")
        
        # resizing to 180 x 90
        img = img.resize((180, 90))
        
        # standardizing the colors to 'web safe' colors
        self.fix_image_color(img)
        
        # converting an array of pixels
        img = np.array(img)
        return img

    def makeArray(self, npy_file):
        with open(npy_file,'rb') as npy:
            arr = pickle.load(npy)
            return arr

