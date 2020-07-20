from PIL import Image
import requests
from io import BytesIO
import numpy as np
import pickle
import os

class FlagUtil:

    def __init__(self):
        '''
        Initializes a FlagUtil object with a color dictionary to be used for memoization.
        It stores RGB colors as keys and their respective 'web safe' colors as the values.
        This speeds up the process for converting flags to 'web safe' colors. It is also
        initialized with a list of all 216 'web safe' colors.
        '''
        self.color_dict = {}
        self.web_safe_colors = self.get_web_safe_colors()

    def pickle_numpy(self, arr, country_filename):
        '''
        Loads the given numpy array into a file with the given file name.

        Parameters
        ----------
        arr : array
            A 2D array representing an image of a country's flag

        country_filename : str
            The name of the file used to store the image of the country's flag
        '''
        with open('flags/' + country_filename + '.pkl','wb') as f:
            pickle.dump(arr, f)

    def get_web_safe_colors(self):
        '''
        Returns a list of all 216 'web safe' colors.

        Returns
        -------
        list
            A list of all 216 'web safe' colors
        '''
        lst = []
        for i in range(0, 256, 51):
            for j in range(0, 256, 51):
                for k in range(0, 256, 51):
                    tup = (i, j, k)
                    lst.append(tup)
                    
        return lst

    def find_nearest_color(self, color):
        '''
        Returns the 'web safe' color that is closest to the given
        RGB color.

        Parameters
        ----------
        color : tuple
            The color

        Returns
        -------
        tuple
            A tuple of RGB values of the 'web safe' color that is 
            most similar to the given color
        '''
        # if this color's been processed before, get its stored value
        if color in self.color_dict:
            return self.color_dict[color]
                
        min_dist = 1000
        nearest_color = (0, 0, 0)
        for cur_col in self.web_safe_colors:
            # summing up the difference of red, green, and blue values of the two colors
            dist = sum(tuple(map(lambda i, j: abs(i - j), color, cur_col)))
            if dist < min_dist:
                min_dist = dist
                nearest_color = cur_col
                
        # adding the color to the dict for future use
        self.color_dict[color] = nearest_color
        return nearest_color

    def fix_image_color(self, img):
        '''
        Standardizes the given image's colors by changing every 
        pixel's color to its closest 'web safe' color.

        Parameters
        ----------
        img : Image
            The image whose colors are being standardized
        '''
        width, height = img.size

        for x in range(width):
            for y in range(height):
                # get the current color of the pixel
                # and replace it with the 'web safe' version
                current_color = img.getpixel((x, y))
                new_color = self.find_nearest_color(current_color)
                img.putpixel((x, y), new_color)

    def process_img(self, url):
        '''
        Loads in an image from the given url and then converts it to RGB,
        standardizes its colors, and resizes it appropriately.

        Parameters
        ----------
        url : str
            A url linking to an image to be processed

        Returns
        -------
        array
            A numpy array representing the processed image from the
            given url
        '''
        # getting the image from the url
        response = requests.get(url)
        image_bytes = BytesIO(response.content)

        try:
            img = Image.open(image_bytes)
        except:
            raise IOError("Unable to open up image")
        
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
        '''
        Loads in a file of the given file name and returns the numpy array
        that was stored in the file.

        Parameters
        ----------
        npy_file : str 
            The name of the file being read

        Returns
        -------
        array
            A numpy array that was being stored in the given file
        '''
        with open(os.path.join(os.path.dirname(__file__), npy_file), 'rb') as npy:
            arr = pickle.load(npy)
            return arr

