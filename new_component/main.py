import streamlit as st
from data_loader import Loader
from utils import portfolio_link
from data_insights import main as data_insights
from data_profiling import main as data_profiling


def main():
    portfolio_link()
    Loader.load_state()
    st.title("Data Insights")
    df = Loader().uploaded_file()

    if not df.empty:
        tab1, tab2 = st.tabs(["discover", "profiling"])

        with tab1:
            data_insights(df)

        with tab2:
            data_profiling(df)


if __name__ == "__main__":

    main()
