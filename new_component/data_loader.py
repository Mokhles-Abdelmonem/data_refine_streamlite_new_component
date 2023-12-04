import streamlit as st
import pandas as pd
from pandas import DataFrame
import copy

class Loader:
    def __init__(self):
        self.df = DataFrame()
        self.df_base = DataFrame()

    def uploaded_file(self) -> DataFrame:
        file = st.file_uploader("upload your data here :", type=["csv"])
        if file:
            if not st.session_state.uploaded:
                st.session_state.uploaded = True

            if 'df' not in st.session_state:
                df = pd.read_csv(file, nrows=100)
                self.df = df
                self.df_base = copy.deepcopy(df)
                st.session_state.df = self.df
                st.session_state.base_df = self.df_base
            self.df = st.session_state.df
        return self.df
    
    @staticmethod
    def load_state() -> None:
        if 'uploaded' not in st.session_state:
            st.session_state.uploaded = False

    @staticmethod
    def update_df(df: DataFrame) -> None:
        if not df.equals(st.session_state.df):
            st.session_state.df = df
            st.rerun()

    @staticmethod
    def base_df() -> DataFrame:
        return st.session_state.base_df