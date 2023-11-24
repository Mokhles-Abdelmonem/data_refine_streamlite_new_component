import streamlit as st
import pandas as pd



class Loader:
    def __init__(self):
        self.df = pd.DataFrame()

    def uploaded_file(self) -> pd.DataFrame:
        file = st.file_uploader("upload your data here :", type=["csv"])
        if file:
            if not st.session_state.uploaded:
                st.session_state.uploaded = True

            if 'df' not in st.session_state:
                self.df = pd.read_csv(file, nrows=100)
                st.session_state.df = self.df
                
            self.df = st.session_state.df
        return self.df
    
