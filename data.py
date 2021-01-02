import requests
import datetime
import json
import sys


def request_data(type='cumulative', loc='BC'):

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
        url_today = f'https://api.opencovid.ca/summary?stat=cases&date={today}&loc={loc}&version="true"'
        url_yesterday = f'https://api.opencovid.ca/summary?stat=cases&date={yesterday}&loc={loc}&version="true"'

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

        # print(response.json())

    return response

def extract_data(http_resp, tcp_connetion):

    """
    TODO: We should think carefully what data we want to extract
    """

    for line in http_resp.iter_lines():

        try:
            full_data = json.loads(line)
            active_cases = full_data['active_cases']
            # cumulate_cases = full_data['cumulative_cases']
            print(f'Extracted active cases: {active_cases}')

            tcp_connetion.connection.send(active_cases + '\n')
        
        except:
            e = sys.exc_info()[0]
            print(f"Error: {e}")

if __name__ == "__main__":

    print('===' * 40)
    request_data()
    print('===' * 40)