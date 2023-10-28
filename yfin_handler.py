# This class is not for object instantiation. 
import yfinance as yf

# test_function completed
class YfinHandler():
    @classmethod
    def query_1ticker_as_1row(cls, ticker: str) -> dict:
        # Query by yfin package
        print("Worker(s) take new task!")
        
        obj:dict = yf.Ticker(str(ticker)).info 
        """
        Example printout: 
        {'zip': '518054', 'sector': 'Communication Services', 'fullTimeEmployees': 112771,
        'longBusinessSummary': "Tencent Holdings Limited, an investment holding company, prov......
        """
        
        # Collecting and sorting information here
        collector_dict = {"tickerID": ticker}

        # List of attributes for the collector dict
        company_info_keys = [
            "longName",
            "sector",
            "industry",
            "fullTimeEmployees",
            "city",
            "country",
            "companyOfficers",
            "maxAge",
            "isEsgPopulated",
            "fundFamily",
        ]  # 4
        analyst_keys = [
            "forwardPE",
            "targetLowPrice",
            "targetHighPrice",
            "targetMedianPrice",
            "targetMeanPrice",
            "numberOfAnalystOpinions",
            "recommendationMean",
            "recommendationKey",
        ]  # 5
        other_ratings_keys = [
            "morningStarRiskRating",
            "forwardEps",
            "revenueQuarterlyGrowth",
            "trailingEps",
        ]  # 3
        financial_related_keys = ["financialCurrency", "sharesOutstanding"]  # 2
        important_dates_keys = [
            "lastFiscalYearEnd",
            "nextFiscalYearEnd",
            "mostRecentQuarter",
            "lastDividendDate",
            "exDividendDate",
            "fundInceptionDate",
        ]  # 5
        insider_keys = ["heldPercentInsiders"]  # 1
        performance_keys = [
            "ebitdaMargins",
            "profitMargins",
            "grossMargins",
            "operatingMargins",
            "revenueGrowth",
            "earningsGrowth",
            "threeYearAverageReturn",
        ]
        ratio_keys = [
            "dividendYield",
            "dividendRate",
            "payoutRatio",
            "lastCapGain",
            "currentRatio",
            "debtToEquity",
            "returnOnEquity",
            "totalCashPerShare",
            "revenuePerShare",
            "quickRatio",
            "enterpriseToRevenue",
            "enterpriseToEbitda",
            "52WeekChange",
            "annualReportExpenseRatio",
            "bookValue",
            "sharesShort",
            "priceToBook",
            "yield",
            "shortRatio",
            "beta",
            "pegRatio",
        ]
        financial_figures_keys = [
            "enterpriseValue",
            "marketCap",
            "operatingCashflow",
            "ebitda",
            "grossProfits",
            "freeCashflow",
            "totalCash",
            "totalDebt",
            "totalRevenue",
        ]
        other_keys = ["algorithm", "averageVolume"]
        
        total_list = (
            company_info_keys
            + analyst_keys
            + other_ratings_keys
            + financial_related_keys
            + important_dates_keys
            + insider_keys
            + performance_keys
            + ratio_keys
            + financial_figures_keys
            + other_keys
        )

        # This for-loop loop over the response object dictionary and get data one-by-one.
        for item in total_list:
            collector_dict.update({item: obj.get(item)})
        # handling the resultant dictionary text.

        return collector_dict

def test_query_1ticker_as_1row():
    empty_dict = {}
    A = YfinHandler.query_1ticker_as_1row("0700.HK")
    if bool(A == empty_dict):
        print("Nothing returned")
    else:
        print("It is not an empty dict.")
        abc = A["sharesOutstanding"]
        print(f"sharesOutstanding:{abc}")
    
test_query_1ticker_as_1row()