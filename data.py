import requests
import datetime
import json
import sys
from pyspark.sql.types import StructField, StringType, DoubleType, StructType, DateType
from pyspark.sql import SparkSession
import time


def clean_data(data):

    if data == "NULL":
        data = 0
    
    #no data should be less than 0. 
    elif data < 0:
        data = 0

    return float(data)

def string_to_date(date):
    date_time_obj = datetime.datetime.strptime(date, '%d-%m-%Y')

    return date_time_obj.date()

def request_data(type = 'cumulative'):

    today = datetime.date.today()
    year_before_today = today - datetime.timedelta(days=365)
    year_before_today = year_before_today.strftime("%d-%m-%Y")

    yesterday = today - datetime.timedelta(days=1)
    year_before_yesterday = yesterday - datetime.timedelta(days=365)
    year_before_yesterday = year_before_yesterday.strftime(("%d-%m-%Y"))

    yesterday = yesterday.strftime("%d-%m-%Y")

    today = today.strftime("%d-%m-%Y")

    if type == 'cumulative':
        url_today = f'https://api.opencovid.ca/summary?stat=cases&date={today}&version="true"'
        url_yesterday = f'https://api.opencovid.ca/summary?stat=cases&date={yesterday}&version="true"'

    elif type == 'time_series':
        url_today = f'https://api.opencovid.ca/timeseries?stat=cases&loc=prov&after={year_before_today}&before={today}'
        url_yesterday = f'https://api.opencovid.ca/timeseries?stat=cases&loc=prov&after={year_before_yesterday}&before={yesterday}'

    response = requests.get(url_today)

    # Make sure nothing is crashing
    if response.status_code != 200:

        if response.status_code == 404:
            print('Data not found')
            return None
        else:
            raise Exception("API failed - {}".format(response.text))
    
    # Check if today's record has already been updated
    if len(response.json()) <= 1:
        print(f"Picking up results from {yesterday} as results of {today} are not updated yet.")
        response = requests.get(url_yesterday)
        
    return response


def data_to_df(data_type = 'cumulative', session=None):

    response = request_data(data_type)
    province_total = response.json()

    province_total_data = []

    if data_type == 'cumulative':

        for record in province_total['summary']:
            province_data = {}
            province_data['province'] = record['province']
            province_data['active_cases'] = clean_data(record['active_cases'])
            province_data['cumulative_cases'] = clean_data(record['cumulative_cases'])
            province_data['cumulative_tested'] = clean_data(record['cumulative_testing'])
            province_data['cumulative_deaths'] = clean_data(record['cumulative_deaths'])
            province_data['vaccine_administration'] = clean_data(record['cumulative_avaccine'])
            province_data['cumulative_recovered'] = clean_data(record['cumulative_recovered'])
            province_data['date'] = string_to_date(record['date'])

            province_total_data.append(province_data)

        data_schema = [
            StructField("province", StringType(), True),
            StructField("active_cases", DoubleType(), True),
            StructField("cumulative_cases", DoubleType(), True),
            StructField("cumulative_tested", DoubleType(), True),
            StructField("cumulative_deaths", DoubleType(), True),
            StructField("vaccine_administration", DoubleType(), True),
            StructField("cumulative_recovered", DoubleType(), True),
            StructField('date', DateType(), True)
        ]
        
        final_struct = StructType(fields=data_schema)

        df = session.createDataFrame(province_total_data,final_struct)

        final_df = df.where((df.province != "Repatriated"))

        return final_df

    elif data_type == 'time_series':
                
        for record in province_total['cases']:
        
            province_data = {}
            province_data['province'] = record['province']
            province_data['cases'] = clean_data(record['cases'])
            province_data['cumulative_cases'] = clean_data(record['cumulative_cases'])
            province_data['date_report'] = string_to_date(record['date_report'])

            province_total_data.append(province_data)

        data_schema = [
            StructField("province", StringType(), True),
            StructField("cases", DoubleType(), True),
            StructField("cumulative_cases", DoubleType(), True),
            StructField('date_report', DateType(), True)
        ]

        final_struct = StructType(fields=data_schema)

        df = session.createDataFrame(province_total_data,final_struct)

        ## Lets only consider Alberta, BC, Quebec, Ontario
        alberta_df = df.where((df.province == "Alberta"))
        bc_df = df.where((df.province == 'BC'))
        quebec_df = df.where((df.province == 'Quebec'))
        ontario_df = df.where((df.province == 'Ontario'))

        return alberta_df, bc_df, quebec_df, ontario_df


if __name__ == "__main__":

    spark = SparkSession.builder.appName('test_session').getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")

    alberta_df, bc_df, quebec_df, ontario_df  = data_to_df('time_series', spark)

    print('The length of Alberta df is : {}'.format(len(alberta_df.toPandas())))
    print('The length of BC df is : {}'.format(len(bc_df.toPandas())))
    print('The length of Quebec df is : {}'.format(len(quebec_df.toPandas())))
    print('The length of Ontario df is : {}'.format(len(ontario_df.toPandas())))
    
    # alberta_cumulatve = alberta_df.cumulative_cases
    # alberta_population = 4371000
    # for i, v in alberta_cumulatve.iteritems():
    #     print((v/alberta_population) * 100000)