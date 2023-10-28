import interface


list_of_region = ["korea", "singapore", "united-kingdom", "hong-kong", "us", "japan"]  # could use for-loop to do mass-actions

# Function 1: get ID list
interface.StockInfo("hong-kong").get_id_list()

# Function 2: get detailed company information
interface.StockInfo("hong-kong").info_query()
