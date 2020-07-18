from bs4 import BeautifulSoup
import requests
from string import ascii_lowercase
from flag_identifier import FlagIdentifier

class FlagTester:

    def __init__(self):
        self.identifier = FlagIdentifier()

    def test(self, test_website = "cia", method = "mse"):
        if test_website == "cia":
            return self.__test_with_cia(method)
        elif test_website == "flagpedia":
            return self.__test_with_flagpedia(method)
        else:
            raise ValueError("The test website must be one of: flagpedia, cia")

    def __test_with_cia(self, identify_type):
        html = requests.get("https://www.cia.gov/library/publications/the-world-factbook/docs/flagsoftheworld.html").text
        soup = BeautifulSoup(html, "lxml")
        
        num_correct = 0
        num_total = 0
        
        for letter in ascii_lowercase:
            test_flags = soup.find_all("li", class_ = "flag appendix-entry ln-" + letter)
            
            for flag in test_flags:
                
                flag_country = flag.find("span").get_text().title()
                if "," in flag_country:
                    split = flag_country.split(", ")
                    flag_country = split[1] + " " + split[0]
                    
    #             print(flag_country, flag_country in flag_df.index)
                flag_img = flag.find("img").get("src").replace("..", "https://www.cia.gov/library/publications/the-world-factbook")
                if flag_country in self.identifier.flag_df.index or "The " + flag_country in self.identifier.flag_df.index:
                    num_total += 1
                    identified_flag = self.identifier.identify(flag_img, method = identify_type)
                    if identified_flag == flag_country or identified_flag == "The " + flag_country:
                        num_correct+=1

                    if num_total % 25 == 0:
                        print("tested", num_total, "flags so far")

        return num_correct / num_total

    def __test_with_flagpedia(self, identify_type):
        html = requests.get("https://flagpedia.net/index").text
        soup = BeautifulSoup(html, "lxml")
        
        num_correct = 0
        num_total = 0

        test_flags = soup.find("ul", class_ = "flag-grid").find_all("li")

        for flag in test_flags:

            flag_country = flag.find("span").get_text().title()

            if "," in flag_country:
                split = flag_country.split(", ")
                flag_country = split[1] + " " + split[0]

            flag_img = "https://flagpedia.net/" + flag.find("img").get("src")
            if flag_country in self.identifier.flag_df.index or "The " + flag_country in self.identifier.flag_df.index:
                num_total += 1
                identified_flag = self.identifier.identify(flag_img, method = identify_type)
                if identified_flag == flag_country or identified_flag == "The " + flag_country:
                    num_correct+=1

                if num_total % 25 == 0:
                    print("tested", num_total, "flags so far")

        return num_correct / num_total