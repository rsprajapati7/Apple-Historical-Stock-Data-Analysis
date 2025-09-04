import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Apple Historical Stock Data Analysis
stock_data = pd.read_csv("Apple Dataset.csv", parse_dates=['Date'],  index_col='Date')

stock_data['Moving_Avg_20'] = stock_data['Close'].rolling(window=20).mean()
stock_data['Moving_Avg_50'] = stock_data['Close'].rolling(window=50).mean()
#stock_data['Moving_Avg_100'] = stock_data['Close'].rolling(window=100).mean()
stock_data['Daily_Returns'] = stock_data['Adj Close'].pct_change()
stock_data['Risk_Volatility'] = (stock_data['Daily_Returns'].rolling(window=30).std())*np.sqrt(252)


yearly_price = stock_data['Close'].resample('YE').agg(['first','last'])
yearly_price['Yearly_Returns'] = (yearly_price['last'] - yearly_price['first']) / yearly_price['first'] * 100


daily_returns_desc = stock_data['Daily_Returns'].describe().to_frame(name='Daily Return Stats')
yearly_returns_desc = yearly_price['Yearly_Returns'].describe().to_frame(name='Yearly Return Stats')
print(daily_returns_desc)
print(yearly_returns_desc)


fig, ((ax1,ax2),(ax3,ax4)) = plt.subplots(nrows=2,ncols=2,figsize=(15,10))
ax1.plot(stock_data.index, stock_data['Close'], label='Closing Price',color='red')
ax1.set_title('Closing Price Over Time')
ax1.set_xlabel('Year')
ax1.set_ylabel('Price (in $USD)')
ax1.legend()
ax1.grid(True)

ax2.plot(stock_data.index,stock_data['Close'],label='Closing Price',color='red')
ax2.plot(stock_data.index,stock_data['Moving_Avg_20'],label='Moving Averages Of 20 Days',color='green')
ax2.plot(stock_data.index,stock_data['Moving_Avg_50'],label='Moving Averages Of 50 Days',color='blue')
#ax2.plot(stock_data.index, stock_data['Moving_Avg_100'], label='Moving Averages OF 100 Days', color='black')
ax2.set_title('Closing Prices With MA')
ax2.set_xlabel('Year')
ax2.set_ylabel('Price (in $USD)')
ax2.legend()
ax2.grid(True)

ax3.bar(yearly_price.index.year, yearly_price['Yearly_Returns'], label='Yearly Returns', color=['green' if val >=0 else 'red' for val in yearly_price['Yearly_Returns']])
ax3.set_title('Yearly Returns')
ax3.set_xlabel("Year")
ax3.set_ylabel("Frequency")
ax3.grid(True)

ax4.plot(stock_data.index, stock_data['Risk_Volatility'], label='Risk Volatility', color='tan')
ax4.set_title('Risk Volatility')
ax4.set_xlabel("Year")
ax4.set_ylabel("Std. Dev Of Returns")
ax4.grid(True)

stock_data.describe()

fig.savefig('./apple_stock_data_graph')
plt.show()