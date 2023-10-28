# This class is not for object instantiation

import pathlib
import time

import pandas as pd
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_auto_update import check_driver

import assist


class WebpageHandler:
    @classmethod
    def get_region_ticker_list(cls, region: str, tickerfile_location: str):
        # Required packages

        def get_most_updated_selenium_driver() -> webdriver:
            check_driver(str(pathlib.Path.cwd()))
            path = r".\chromedriver.exe"
            driver = webdriver.Chrome(executable_path=path)
            return driver

        driver = get_most_updated_selenium_driver()
        target_url = f"https://www.tradingview.com/markets/stocks-{region}/market-movers-all-stocks/"
        driver.get(target_url)

        # Part 1 -- roll over to the end of the page.
        assist.printlog(
            "Start browsing the website {target_url} for scraping the tickerID"
        )
        count = 0

        def scrolling_webpage_to_end(driver: webdriver) -> None:
            while True:
                try:
                    time.sleep(0.5)
                    # Row the page to the end of the page
                    driver.execute_script(
                        "window.scrollTo(0, document.body.scrollHeight);"
                    )
                    loadMoreButton = driver.find_element_by_xpath(
                        "//span[@class='tv-load-more__btn']"
                    )
                    print("Attemp click the button....")
                    loadMoreButton.click()
                    print(f"Click:{count} completed")
                    count += 1
                except:
                    print("Selenium Process Terminated")
                    break

        scrolling_webpage_to_end(driver)

        soup = bs(driver.page_source, "html.parser")
        ticker_id_list = []
        css_l_tickerid = "div.tv-screener-table__symbol-container-description > a.tv-screener__symbol"
        
        # split out different region cases, so that each cases could be tested independently.
        def get_hongkong_tickerlist():
            # for hong kong tickers, stock ID are alphabets
            print("Starting the loop.....")
            print(len(soup.select(css_l_tickerid)))
            for item in soup.select(css_l_tickerid):
                ticker_id_list.append(f"{item.get_text():0>4}.HK")
        
        def get_other_region_tickerlist():
            # for other region tickers, stock ID are numbers
            print(len(soup.select(css_l_tickerid)))
            for item in soup.select(css_l_tickerid):
                ticker_id_list.append(item.get_text())
        
        if region == "hong-kong":
            get_hongkong_tickerlist()
        else:
            get_other_region_tickerlist()
        
        assist.printlog(f"TickerID collection complete. TickerID collected: {ticker_id_list}. Total number of TickerID collected: {len(ticker_id_list)}")

        def output_the_list(_list):
            dict = {"tickerID": _list}
            df = pd.DataFrame(dict)
            df.to_csv(f".\id_feeder_folder\{tickerfile_location}")
            assist.printlog(f"csv file '{tickerfile_location}' created or updated.")

        output_the_list(ticker_id_list)

        return ticker_id_list
