import streamlit.components.v1 as components
import streamlit as st
import pandas as pd
from processor import DataProcess, ColumnProcess, Classifier
import plotly.express as px
import plotly.graph_objs as go
from data_loader import Loader
from data_cleaner import Cleaner
from Filters import DateTimeFilter, CategoricalFilter, NumericFilter


from utils import (
    get_attribute,
    has_numbers,
    portfolio_link,
    load_state,
    measures_methodes
    )


def main():
    load_state()
    portfolio_link()
    st.title("Data Insights")
    df = Loader().uploaded_file()

    if not df.empty:

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

        # ---- column ---- 


        col_list = ["(Count)"] + col_list
        columns = st.multiselect(
            "Select the Columns :",
            options=col_list,
            
        )

        rows = st.multiselect(
            "Select the Rows :",
            options=col_list,
            
        )

        # ---- SIDEBAR ----

        # ---- Filters ----

        st.sidebar.header("Filters :")

        datetime_filter = DateTimeFilter(df, datetime_columns)
        datetime_filter.apply_filters() 
        
        categorical_filter = CategoricalFilter(df, categorical_columns, boolean_columns)
        categorical_filter.apply_filters()

        numeric_filter = NumericFilter(df, numeric_columns)
        numeric_filter.apply_filters()



        # --- DISPLAY groupby ---


        numberic_filter = st.sidebar.multiselect(
            "filter by measurment values: ",
            options=numeric_columns,
            
        )


        measures_options = measures_methodes.keys()
        numberic_filter_dict = {}
        if numberic_filter :
            for col in numberic_filter:
                measure_option = st.sidebar.selectbox(
                f"{col} Measurement",
                options=measures_options,
                )
                numberic_filter_dict[col]=measure_option



        # --- DISPLAY DATAFRAME ---
        def filter_groupby(col):
            if not col in numeric_columns and col != "(Count)" :
                if numberic_filter_dict:
                    df_grouped = df.groupby(col)
                    df_filtered =  df
                    for filter_col, measurs in  numberic_filter_dict.items():
                        ldict = {}
                        df_filtered =  df_filtered.groupby(col)
                        if len(df_grouped) <= 1 :
                            return df
                        grouped = get_attribute(df_grouped, measures_methodes[measurs])()[[filter_col]]
                        mini = int(grouped.min()[0])
                        maxi = int(grouped.max()[0])
                        slider_range = maxi - mini
                        step = None
                        if slider_range > 1000000 :
                            step = int(slider_range / 1000000)
                        values = st.slider(
                            f'Select a range of {filter_col} values for each {col} ',
                            mini, maxi, (mini, maxi),
                            step=step,
                            )
                        df_filtered = df_filtered.filter(lambda x: values[1] >= get_attribute(x[filter_col], measures_methodes[measurs])() >= values[0])
                        df_filtered = ldict["df_filtered"]
                    return df_filtered
            return df

        df_grouped= None
        chart = None
        for col in columns:
            df = filter_groupby(col)
            for row in  rows:
                df = filter_groupby(row)
                count = "Count"
                if col != "(Count)" and row != "(Count)":
                    if col in numeric_columns:
                        if row in numeric_columns:
                            if row == col :
                                df[f"_{row}"] =  df[row]
                                row = f"_{row}"
                            df_grouped = df
                        else:
                            measure_option = st.selectbox(
                            f"Measurement applied on col {col}",
                            options=measures_options,
                            )
                            df_grouped = get_attribute(df.groupby(row), measures_methodes[measure_option])().reset_index()
                    else:
                        if row in numeric_columns:
                            measure_option = st.selectbox(
                            f"Measurement applied on row {row} for column {col}",
                            options=measures_options,
                            )
                            df_grouped = get_attribute(df.groupby(col), measures_methodes[measure_option])().reset_index()
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

                




    else:
        if 'df' in st.session_state:
            del st.session_state["df"]

if __name__ == "__main__":
    main()
