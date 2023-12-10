from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
from pandas import DataFrame

def main(df: DataFrame) -> None:
    pr = ProfileReport(df, title="Report")
    st_profile_report(pr)

