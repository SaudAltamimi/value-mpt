def saudi_fetch_stock_tickers():

    list_saudi=[]
    with open('Saudi_Stock_Active_Tickers.csv','r') as file:
        content = file.read()
        list_saudi = content.split('\n')

    return list_saudi