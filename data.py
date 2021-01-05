import requests
import datetime
import json
import sys
from pyspark.sql.types import StructField, StringType, DoubleType, StructType, DateType

def request_data(type='cumulative'):

    """
    Specify the type of API calls to make
    TODO: provide sophisticated control for the type of API calls one can make
    """

    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    yesterday = yesterday.strftime("%d-%m-%Y")
    today = today.strftime("%d-%m-%Y")

    if type == 'time_series':
        pass

    elif type == 'cumulative':
        url_today = f'https://api.opencovid.ca/summary?stat=cases&date={today}&version="true"'
        url_yesterday = f'https://api.opencovid.ca/summary?stat=cases&date={yesterday}&version="true"'

    response = requests.get(url_today)

    # Just making sure nothing is crashing
    if response.status_code != 200:

        if response.status_code == 404:
            print('Data not found')
            return None
        else:
            raise Exception("API failed - {}".format(response.text))
    
    if len(response.json()) <= 1:
        print(f"Picking up results from {yesterday} as results of {today} are not updated yet.")
        response = requests.get(url_yesterday)  

    return response

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

    
def data_to_df(data_type, session):

    response = request_data(data_type)
    province_total = response.json()

    province_total_data = []

    # select only the relevant information (TODO: Maybe add )
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



if __name__ == "__main__":

    test = ['test', 'your', 'code']
    code = ','.join(test)
    print(code)

