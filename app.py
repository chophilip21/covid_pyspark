import socket
import requests_oauthlib
import numpy as np
import pandas as pd
import plotly.express as px
from pyspark.sql.types import *
import plotly.graph_objects as go
from pyspark.sql import functions as F
from plotly.subplots import make_subplots
from fbprophet import Prophet
from data import * 


if __name__ == "__main__":

    TCP_IP = "localhost"
    TCP_PORT = 9009
    conn = None
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.listen(1)

    print('Waiting for TCP connection')
    conn, addr = s.accept()
    print('Connected...getting data from API')

    resp = request_data()
    extract_data(resp, conn)