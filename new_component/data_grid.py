import streamlit.components.v1 as components
import streamlit as st
import pandas as pd
import json
from processor import DataProcess, ColumnProcess

st.set_page_config(layout="wide")


_custom_dataframe = components.declare_component(
    "DataGrid",
    url="http://localhost:3000"
)


def custom_dataframe(columns, rows, key=None):
    return _custom_dataframe(columns=columns, rows=rows, key=key, default={})


def load_df(df):
    df_json = df.to_json(orient="index")
    return df.columns.to_list(), df_json

if 'uploaded' not in st.session_state:
    st.session_state.uploaded = False

def main():
    st.title("File Upload Example")
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    st.sidebar.write("File view!")

    if uploaded_file :
        if not st.session_state.uploaded:
            st.session_state.uploaded = True

        if 'df' not in st.session_state:
            df = pd.read_csv(uploaded_file, nrows=100)
            st.session_state.df = df
            print("read_csv only one time >>>> ", df.columns)
            
        df = st.session_state.df
        columns, rows = load_df(df)
        event = custom_dataframe(columns, rows)

        event, col = event.get("event", None), event.get("colName", None)
        if event:
            print("event >>>> ", event)
            Processor = ColumnProcess(df, col)
            callable_method = getattr(Processor, event)
            df = callable_method()
            res = st.session_state.df.equals(df)           
            print("______________ res ________________")
            print(res)
            if st.session_state.df.equals(df):
                print("______________ nothing to do here ________________")
                return
            
            st.session_state.df = df
            print("df.columns >>>> ", df.columns)
            st.rerun()
    else:
        if 'df' in st.session_state:
            del st.session_state["df"]

if __name__ == "__main__":
    main()
