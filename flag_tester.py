from bs4 import BeautifulSoup
import requests
from string import ascii_lowercase
import flagpy as fp

class FlagTester:

    def test(self, test_website = "cia", method = "mse"):
        '''
        Tests the given method on the given website of flags.

        Parameters
        ----------
        test_website : str
            Either "cia" or "flagpedia", represents the website used to test the 
            flagpy identifier

        method : str
            The method being tested (one of mse, ssim, or hash)

        Returns
        -------
        float
            The accuracy of the identifier, out of 1.0
        '''
        if test_website == "cia":
            return self.__test_with_cia(method)
        elif test_website == "flagpedia":
            return self.__test_with_flagpedia(method)
        else:
            raise ValueError("The test website must be one of: flagpedia, cia")

    def __test_with_cia(self, identify_type):
        '''
        Tests the given method on the CIA website of country flags.

        Parameters
        ----------
        method : str
            The method being tested (one of mse, ssim, or hash)

        Returns
        -------
        float
            The accuracy of the identifier, out of 1.0
        '''
        html = requests.get("https://www.cia.gov/library/publications/the-world-factbook/docs/flagsoftheworld.html").text
        soup = BeautifulSoup(html, "lxml")
        
        num_correct = 0
        num_total = 0
        
        for letter in ascii_lowercase:

            # all of the flags on the website
            test_flags = soup.find_all("li", class_ = "flag appendix-entry ln-" + letter)
            
            for flag in test_flags:
                
                flag_country = flag.find("span").get_text().title()

                # reformatting country names (ie. Korea, South -> South Korea)
                if "," in flag_country:
                    split = flag_country.split(", ")
                    flag_country = split[1] + " " + split[0]
                    
                
                flag_img = flag.find("img").get("src").replace("..", "https://www.cia.gov/library/publications/the-world-factbook")

                # Checking if adding "The " to the front of the country name helps 
                # with reformatting
                if flag_country in fp.get_country_list() or "The " + flag_country in fp.get_country_list():
                    num_total += 1
                    identified_flag = fp.identify(flag_img, method = identify_type)
                    if identified_flag == flag_country or identified_flag == "The " + flag_country:
                        num_correct+=1

                    if num_total % 25 == 0:
                        print("tested", num_total, "flags so far")

        return num_correct / num_total

    def __test_with_flagpedia(self, identify_type):
        '''
        Tests the given method on the flagpedia website of country flags.

        Parameters
        ----------
        method : str
            The method being tested (one of mse, ssim, or hash)

        Returns
        -------
        float
            The accuracy of the identifier, out of 1.0
        '''
        html = requests.get("https://flagpedia.net/index").text
        soup = BeautifulSoup(html, "lxml")
        
        num_correct = 0
        num_total = 0

        # all of the flags on the website
        test_flags = soup.find("ul", class_ = "flag-grid").find_all("li")

        for flag in test_flags:

            flag_country = flag.find("span").get_text().title()

            # reformatting country names (ie. Korea, South -> South Korea)
            if "," in flag_country:
                split = flag_country.split(", ")
                flag_country = split[1] + " " + split[0]

            flag_img = "https://flagpedia.net/" + flag.find("img").get("src")

            # Checking if adding "The " to the front of the country name helps 
            # with reformatting
            if flag_country in fp.get_country_list() or "The " + flag_country in fp.get_country_list():
                num_total += 1
                identified_flag = fp.identify(flag_img, method = identify_type)
                if identified_flag == flag_country or identified_flag == "The " + flag_country:
                    num_correct+=1

                if num_total % 25 == 0:
                    print("tested", num_total, "flags so far")

        return num_correct / num_total