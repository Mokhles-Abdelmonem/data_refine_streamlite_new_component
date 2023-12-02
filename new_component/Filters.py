import streamlit as st
from utils import get_attribute, measures_methodes
from data_loader import Loader

class DateTimeFilter:
    def __init__(self, df, datetime_columns):
        self.df = df
        self.base_df = Loader.base_df()
        self.datetime_columns = datetime_columns

    def filter_by_range(self, col, filter_value):
        dt_col = get_attribute(self.base_df[col].dt, filter_value)
        mini, maxi = int(dt_col.min()), int(dt_col.max())
        slid_range = maxi - mini
        steps = int(slid_range / 1000000) if slid_range > 1000000 else None

        dt_slider_values = st.slider(
            f'Select a range of {col} values',
            mini, maxi, (mini, maxi),
            step=steps,
        )

        self.mask = (get_attribute(self.df[col].dt, filter_value) >= dt_slider_values[0]) & \
                    (get_attribute(self.df[col].dt, filter_value) <= dt_slider_values[1])

        self.df = self.df[self.mask]
        Loader.update_df(self.df)

    def filter_by_values(self, col):
        dt_list = self.base_df[col].dt.year.unique()
        dt_value_list = []

        for dt in dt_list:
            checked = st.checkbox(str(dt), value=True)
            if checked:
                dt_value_list.append(dt)

        if dt_value_list:
            self.mask = (self.df[col].dt.year.isin(dt_value_list))
            self.df = self.df[self.mask]
            Loader.update_df(self.df)

    def apply_filters(self):

        if self.datetime_columns :

            date_time_filter = st.sidebar.multiselect(
                "Date&Time filter:",
                options=self.datetime_columns,
            )

            for col in date_time_filter:
                dt_options = ["year", "month", "day", "hour", "minute", "second"]
                tab1, tab2, tab3 = st.sidebar.tabs(["filter", "filter by", "filter type"])

                dt_filter_value = tab2.selectbox(
                    f"{col} filter",
                    options=dt_options,
                )

                filter_type = tab3.selectbox(
                    f"{col} filter type",
                    options=["range", "values"],
                )

                if filter_type == "range":
                    self.filter_by_range(col, dt_filter_value)
                elif filter_type == 'values':
                    self.filter_by_values(col)


class CategoricalFilter:
    def __init__(self, df, categorical_columns, boolean_columns):
        self.df = df
        self.base_df = Loader.base_df()
        self.categorical_columns = categorical_columns
        self.boolean_columns = boolean_columns

    def apply_filters(self):
        
        categoric_filter = st.sidebar.multiselect(
            "Filter by category and boolean values:",
            options=self.categorical_columns + self.boolean_columns,
        )

        for col in categoric_filter:
            options = self.base_df[col].unique().tolist()
            cat_filter_value = st.sidebar.multiselect(
                f"{col} filter",
                options=options,
            )

            if cat_filter_value:
                self.df = self.df[self.df[col].isin(cat_filter_value)]
                Loader.update_df(self.df)


class NumericFilter:
    def __init__(self, df, numeric_columns):
        self.df = df
        self.base_df = Loader.base_df()
        self.numeric_columns = numeric_columns

    def apply_filters(self):
        
        numeric_filter = st.sidebar.multiselect(
            "Filter by numeric values:",
            options=self.numeric_columns,
        )

        for col in numeric_filter:
            self.filter_by_range(col)

    def filter_by_range(self, col):
        df_col = self.base_df[col]
        mini, maxi = int(df_col.min()), int(df_col.max())
        slid_range = maxi - mini
        steps = int(slid_range / 1000000) if slid_range > 1000000 else None

        dt_slider_values = st.sidebar.slider(
            f'Select a range of {col} values',
            mini, maxi, (mini, maxi),
            step=steps,
        )

        self.mask = (df_col >= dt_slider_values[0]) & \
                    (df_col <= dt_slider_values[1])

        self.df = self.df[self.mask]
        Loader.update_df(self.df)