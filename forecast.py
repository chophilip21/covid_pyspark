from fbprophet import Prophet

def prophet_forecast(df):

    """
    Forecasting using Facebook model.
    The results do not seem to be so promising though. 
    """

    df.rename(columns={"cases": "y", "date_report":"ds"}, inplace=True)
    df.drop(['province', 'cumulative_cases'], axis=1, inplace=True)

    alberta_df['floor'] = 0
    alberta_df['cap'] = 100000

    print(alberta_df.tail(50))

    model = Prophet(
        interval_width=0.95,
        growth='linear',
        daily_seasonality=False,
        weekly_seasonality= False,
        yearly_seasonality=True,
        seasonality_mode='multiplicative'
    )

    model.fit(alberta_df)   

    future_pd = model.make_future_dataframe(
    periods=90,
    include_history=True,
    )

    future_pd['floor'] = 0
    future_pd['cap'] = 100000

    print('Training complete...')
    forecast_pd = model.predict(future_pd)

    print(forecast_pd[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(90))

    return forecast_pd

   