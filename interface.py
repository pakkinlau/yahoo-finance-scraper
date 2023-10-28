import concurrent.futures
import logging
import os
import pathlib
from contextlib import contextmanager
from datetime import date

import assist
import webpage_handler
import yfin_handler
import external_file

class StockInfo:

    def __init__(self, region: str):

        self.region: str = region
        self.logfilename: str = f"logfile-yfin-info-{date.today()}-{self.region}.log"
        self.tickerfilename: str = f"tickerfile-yfin-{self.region}.csv"
        self.resultfilename: str = f"resultfile-yfin-info-{date.today()}.csv"

    def get_id_list(self):
        return webpage_handler.WebpageHandler.get_region_ticker_list(self.region,self.tickerfilename)

    def info_query(self):
        def check_and_report_import_properly() -> None:
            if len(tickerID_list) != 0:
                print("tickerlist csv successfully loaded")
                print(tickerID_list)
                print(f"Length of tickerList:{len(tickerID_list)}")
                logging.info(f"'.info' Query Looping for {self.region} started. ")
            else:
                print("tickerlist csv loading")

        tickerID_list = external_file.import_id_list(self.tickerfilename)
        check_and_report_import_properly()

        info_result_list: list[dict] = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
            future_to_tickerID: dict[dict:str] = {
                executor.submit(
                    yfin_handler.YfinHandler.query_1ticker_as_1row, ticker
                ): ticker
                for ticker in tickerID_list
            }
            count = 0
            for futures in concurrent.futures.as_completed(future_to_tickerID):
                info_result_list.append(futures.result())
                count += 1
                print(f"progress: ({count}/{len(tickerID_list)}).")
        assist.printlog("Loop ended=========================")

        external_file.export_result_list_of_dist(info_result_list, self.resultfilename)

class Havent_used:
    # Haven't used it
    @contextmanager
    @staticmethod
    def in_dir(path):
        """This method is for open a directory in the context manager and do something and then return to original dir right the way."""
        old_dir = pathlib.Path.cwd()  # save current working directory
        os.chdir(path)  # switch to new working directory
        yield
        # change back to pervious working directory
        os.chdir(old_dir)

    # Haven't used it
    def get_region_ticker_list(self):
        return webpage_handler.WebpageHandler.get_region_ticker_list(
            self.region, self.tickerfilename
        )
