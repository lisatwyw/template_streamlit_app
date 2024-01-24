!/usr/bin/python

# admin
import numpy as np
rng = np.random.default_rng( 12345 )

import sys, os, copy, json
from pathlib import Path
from glob import glob
from datetime import datetime, timedelta
from time import sleep
import requests 

import pandas as pd

from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

# getting EOD  
#import climateservaccess as ca

# plotting
import plotly.express as px
import matplotlib.pyplot as plt

# mapping
import geopandas
from branca.element import Figure
import folium, geopy; from folium import plugins; import geopandas as gpd

# streamlit 
import streamlit.components.v1 as components
import streamlit as st
from streamlit_folium import st_folium, folium_static


# Get the parent directory
path_root = Path( os.path.dirname(os.path.realpath(__file__)) )
print( 'Root path: ' + path_root )



def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')


def filter_dataframe(df, name_of_chkbox,  ) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns
    Args:
        df (pd.DataFrame): Original dataframe
    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox( name_of_chkbox )

    if not modify:
        return df
    df = df.copy()
    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        try:
           if is_object_dtype(df[col]):            
              df[col] = pd.to_datetime(df[col])
           if is_datetime64_any_dtype(df[col]):
              df[col] = df[col].dt.tz_localize(None)
        except Exception:
           pass

    modification_container = st.container()
    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns )
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            left.write("↳")
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 200:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    _min,
                    _max,
                    (_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].str.contains(user_text_input)]
    return df

def print_footer():
    st.markdown('''
    Related materials:
    https://www.ubc.ca | https://www.sfu.ca
    ''')
