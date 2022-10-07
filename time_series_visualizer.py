import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

df = pd.read_csv('./fcc-forum-pageviews.csv', index_col='date', parse_dates=True)

df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
  fig, ax = plt.subplots(figsize=(10,5))
  ax.plot(df.index, df['value'], 'r', linewidth=1)
  ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
  ax.set_xlabel('Date')
  ax.set_ylabel('Page Views')

  fig.savefig('line_plot.png')
  return fig

def draw_bar_plot():
  df_bar = df.copy()  
  df_bar['Month'] = df_bar.index.month  
  df_bar['Year'] = df_bar.index.year
  df_bar = df_bar.groupby(['Year', 'Month'])['value'].mean()
  df_bar = df_bar.unstack()
  
  fig = df_bar.plot.bar(legend=True, figsize=(10,5), ylabel="Average Page Views", xlabel='Years').figure
  plt.legend(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
  
  fig.savefig('bar_plot.png')
  return fig

def draw_box_plot():
  df_box = df.copy()
  df_box.reset_index(inplace=True)
  df_box['year'] = [d.year for d in df_box.date]
  df_box['month'] = [d.strftime('%b') for d in df_box.date]

  fig, ax = plt.subplots(1, 2, figsize=(32, 10), dpi=100)

  sns.boxplot(data=df_box, x="year", y="value", ax=ax[0])
  ax[0].set_title("Year-wise Box Plot (Trend)")
  ax[0].set_xlabel("Year")
  ax[0].set_ylabel("Page Views")
  
  month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
  sns.boxplot(data=df_box, x="month", y="value", order=month_order, ax=ax[1])
  ax[1].set_title("Month-wise Box Plot (Seasonality)")
  ax[1].set_xlabel("Month")
  ax[1].set_ylabel("Page Views")

  fig.savefig('box_plot.png')
  return fig
