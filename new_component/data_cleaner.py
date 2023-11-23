import streamlit as st
import pandas as pd
from processor import DataProcess
from pandas import DataFrame


class Cleaner:
    def __init__(self, df:DataFrame) -> None:
        self.df = df
        self.nulls_num = self.df.isnull().values.sum().sum()
        self.duplicates_num = self.df.duplicated().any().sum()
        self.is_clean = not(self.nulls_num and self.duplicates_num)

    def clean_data(self) -> DataFrame:
        self.clean_header()

        if self.nulls_num:
            self.handle_nulls()

        if self.duplicates_num:
            self.handle_duplicates()

        return self.df

    def clean_header(self) -> None:
        st.sidebar.header("Cleaning :")
        if self.is_clean:
            st.sidebar.info("your data is clean", icon="🔍")
        else:
            not_clean_msg = f"your data is not clean"
            st.sidebar.error(not_clean_msg, icon="⚠️")

    def handle_nulls(self) -> None:

        null_msg = f"{self.nulls_num} null values found"
        st.sidebar.warning(null_msg, icon="⚠️")
        
        handle_nulls_options = [
            "Egnore",
            "Drop columns with nulls",
            "Drop rows with nulls"
        ]
        dt_null_value = st.sidebar.selectbox("Handle Nulls", options=handle_nulls_options)

        if handle_nulls_options.index(dt_null_value) == 1 :
            self.df = DataProcess(self.df).drop_null_col()
            st.session_state.df = self.df
            st.rerun()
        if handle_nulls_options.index(dt_null_value) == 2 :
            self.df = DataProcess(self.df).drop_null_row()
            st.session_state.df = self.df
            st.rerun()

    def handle_duplicates(self) -> None:
        alert_msg = f"you have {self.duplicates_num} duplicated on your data"
        st.sidebar.warning(alert_msg, icon="⚠️")
        
        handle_duplicates_options = [
            "Egnore",
            "Drop duplicates"
        ]
        dt_duplicates_value = st.sidebar.selectbox("Handle Duplicates", options=handle_duplicates_options)

        if handle_duplicates_options.index(dt_duplicates_value) == 1 :
            self.df = DataProcess(self.df).drop_null_col()
            st.session_state.df = self.df
            st.rerun()

    def data_editor(self) -> None:
        st.data_editor(self.df)