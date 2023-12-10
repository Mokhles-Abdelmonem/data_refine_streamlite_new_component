import streamlit as st
from processor import Classifier
import plotly.express as px
from data_cleaner import Cleaner
from Filters import DateTimeFilter, CategoricalFilter, NumericFilter
from pandas import DataFrame
from streamlit_pandas_profiling import st_profile_report


from utils import (
    get_attribute,
    measures_methodes
    )


def main(df: DataFrame) -> None:
    
    cleaner = Cleaner(df)
    cleaner.clean_data()
    cleaner.data_editor()

    # ---- Variables ----
    classifier = Classifier(df=df)
    (
        numeric_columns,
        boolean_columns,
        datetime_columns,
        categorical_columns,
        col_list

    ) = classifier.classify()

    # ---- Filters ----

    st.sidebar.header("Filters :")

    datetime_filter = DateTimeFilter(df, datetime_columns)
    df = datetime_filter.apply_filters() 
    
    categorical_filter = CategoricalFilter(df, categorical_columns, boolean_columns)
    df = categorical_filter.apply_filters()

    numeric_filter = NumericFilter(df, numeric_columns)
    df = numeric_filter.apply_filters()


    # --- DISPLAY ---

    col_list = ["(Count)"] + col_list
    columns = st.multiselect(
        "Select the Columns :",
        options=col_list,
        
    )

    rows = st.multiselect(
        "Select the Rows :",
        options=col_list,
        
    )


    df_grouped= None
    chart = None
    for col in columns:
        for row in  rows:
            count = "Count"
            if col != "(Count)" and row != "(Count)":
                if col in numeric_columns:
                    if row in numeric_columns:
                        if row == col :
                            df[f"_{row}"] =  df[row]
                            row = f"_{row}"
                        df_grouped = df
                    else:
                        col_measure_option = st.selectbox(
                        f"Measurement applied on col {col}",
                        options=measures_methodes.keys(),
                        key=f"{row}_measure"
                        )
                        df_grouped = get_attribute(df.groupby(row), measures_methodes[col_measure_option])().reset_index()
                else:
                    if row in numeric_columns:
                        row_measure_option = st.selectbox(
                        f"Measurement applied on row {row} for column {col}",
                        options=measures_methodes.keys(),
                        key=f"{col}_measure"
                        )
                        df_grouped = get_attribute(df.groupby(col), measures_methodes[row_measure_option])().reset_index()
                    else:
                        if row == col :
                            df[f"_{row}"] =  df[row]
                            row = f"_{row}"
                        df_grouped = df.groupby([row, col]).count().reset_index()

            else:
                while count in col_list :
                    count += '_'
                if row != "(Count)":
                    df_grouped = df.groupby(row).size()
                    col = count
                elif col != "(Count)":
                    df_grouped = df.groupby(col).size()
                    row = count
                else:
                    continue 
                df_grouped = df_grouped.reset_index(name=count)

            chart_options = ["bar", "line", "histogram", "area","box", "pie"]
            chart_selected = st.selectbox(
            f"chart for row {row} & column {col}",
            options=chart_options,
            )
            color= {"color_discrete_sequence": ['#F63366']*len(df_grouped)}
            if chart_selected == "line":
                color_cols = categorical_columns+boolean_columns
                color_cols.insert(0, None)
                col_selected = st.selectbox(
                f"Select color columns to row {row} & column {col}",
                options=color_cols,
                )
                if col_selected :
                    color = {"color": col_selected}

            chart = get_attribute(px, chart_selected)(df_grouped, col, row, **color, template='plotly_white')
            st.plotly_chart(chart)
