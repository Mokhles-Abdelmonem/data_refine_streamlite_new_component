import streamlit as st
import pandas as pd
from processor import DataProcess



class Cleaner:
    def __init__(self, df):
        self.df = df
        self.nulls_num = self.df.isnull().values.sum().sum()
        self.duplicates_num = self.df.duplicated().any().sum()
        self.is_clean = self.nulls_num and self.duplicates_num


    def clean_data(self) -> pd.DataFrame:
        st.sidebar.header("Cleaning :")

        if self.nulls_num:

            not_clean_msg = f"your data is not clean"
            null_msg = f"{self.nulls_num} null values found"

            st.sidebar.error(not_clean_msg, icon="⚠️")

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
                st.rerun()
        elif self.duplicates_num:
            alert_msg = f"you have {self.duplicates_num} duplicated on your data"
            st.warning(alert_msg, icon="⚠️")

        else:
            st.sidebar.info("your data is clean", icon="🔍")

        return self.df
    
    def data_editor(self):
        st.data_editor(self.df)