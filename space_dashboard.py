import dash
import dash_core_components
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import sqlite3
import ipdb
from datetime import datetime as dt

external_stylesheets = ['https://codepen.io/chiddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

conn = sqlite3.connect("space.db", isolation_level=None)
cur = conn.cursor()

