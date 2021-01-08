from fbprophet import Prophet
from data import *
import pandas as pd
from pyspark.sql.types import *
from pyspark.sql import functions as F
from pyspark.sql import SparkSession
import numpy as np

def prophet_forecast(df, forecast_period=30):

    """
    Forecasting using Facebook model.
    The results do not seem to be so promising though. 
    """

    df.rename(columns={"cases": "y", "date_report":"ds"}, inplace=True)
    df.drop(['province', 'cumulative_cases'], axis=1, inplace=True)

    model = Prophet(
        interval_width=0.95,
        growth='linear',
        daily_seasonality=False,
        weekly_seasonality= False,
        yearly_seasonality=True,
        seasonality_mode='multiplicative',
        changepoints=['2020-11-01']
    )

    model.fit(df)   

    future_pd = model.make_future_dataframe(
    periods=forecast_period,
    include_history=False,
    )

    future_pd['floor'] = 0
    future_pd['cap'] = 100000
    forecast_pd = model.predict(future_pd)

    new_time = forecast_pd['ds'].dt.strftime('%Y-%m-%d')

    # give some randomness to the values
    random_number = np.random.uniform(low=0, high=0.1)

    forecast_pd['yhat'] = np.where((forecast_pd.yhat < 0), 0, forecast_pd.yhat)

    new_value = round(forecast_pd['yhat'])

    forecasted_values = df['y'].append(new_value, ignore_index=True)
    forecasted_dates = df['ds'].append(new_time, ignore_index=True)

    return forecasted_values, forecasted_dates


if __name__ =="__main__":


    random_number = np.random.uniform(low=0, high=0.1)

    print(random_number)

    # spark = SparkSession.builder.appName('covid-19_test').getOrCreate()
    # spark.sparkContext.setLogLevel("ERROR")
 
    # alberta_df, bc_df, quebec_df, ontario_df  = data_to_df('time_series', spark)

    # alberta_df = alberta_df.toPandas()
    # bc_df =  bc_df.toPandas()
    # quebec_df = quebec_df.toPandas()
    # ontario_df = ontario_df.toPandas()
    
    # print('The length of Alberta df is : {}'.format(len(alberta_df.toPandas())))
    # print('The length of BC df is : {}'.format(len(bc_df.toPandas())))
    # print('The length of Quebec df is : {}'.format(len(quebec_df.toPandas())))
    # print('The length of Ontario df is : {}'.format(len(ontario_df.toPandas())))

    # print(alberta_df.head())

    # test = prophet_forecast(alberta_df)
   
    # print(test)