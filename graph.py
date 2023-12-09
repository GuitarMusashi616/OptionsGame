from matplotlib import pyplot as plt


def graph_prices(series):
    plt.figure(figsize=(12, 9))
    plt.plot(series.index, series)
    plt.title('Recent Prices')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.grid(True)
    plt.show()