from bs4 import BeautifulSoup
import pandas as pd
import requests
from flagpy.flag_util import FlagUtil

class FlagScraper:

    def __init__(self):
        '''
        Initializes this scraper with a list of states that are not countries but still
        appear on Wikipedia's list of sovereign state flags. This prevents them from getting
        mixed in with the official countries in the DataFrame.
        '''
        self.util = FlagUtil()

        # a list of non-countries that are still on the Wikipedia page for some reason
        self.states = ["Abkhazia", "The Republic Of Artsakh", "The Republic Of China", "The Cook Islands", 
        "Kosovo", "Niue", "Northern Cyprus", "Western Sahara", "Somaliland", "Ossetia", "Transnistria"]

    def get_flags(self):
        '''
        Scrapes the name of each country and its corresponding flag image. Instead of storing the
        image directly into a DataFrame, it stores the image in a .pkl file and stores the name 
        of the file in the DataFrame instead.
        '''
        html = requests.get("https://en.wikipedia.org/wiki/Gallery_of_sovereign_state_flags").text
        soup = BeautifulSoup(html, "lxml")
        
        flags = soup.find_all("li", class_ = "gallerybox")
        flag_df = pd.DataFrame(columns = ["country", "flag"])
        
        i = 1
        
        for flag in flags:
            # getting the name of the country
            country = flag.find("div", class_ = "gallerytext").find("a").get("title")
            country = country.split("Flag of ")[1].title()

            # replacing the spaces with underscores to be used in file names
            country_filename = country.replace(" ", "_")

            # fixing an edge case with the country of Georgia
            if "Georgia" in country:
                country = "Georgia"

            # getting the url of the flag and converting to a 180 x 90 RGB image (as a numpy array)
            img_url = "https:" + flag.find("img").get("src")
            img = self.util.process_img(img_url)
            
            # if the country is actually a country, add it to the df
            if country not in self.states:
                self.util.pickle_numpy(img, country_filename)

                flag_df = flag_df.append({"country": country, "flag": 'flags/' + country_filename + '.pkl'}, ignore_index = True)
                i += 1

            if i % 25 == 0:
                print("finished", i, "flags")
            
            
        print("finished all 195 flags!")
        flag_df = flag_df.set_index("country")
        flag_df.to_csv("flag_df.csv")