from pandas import DataFrame
import pandas as pd
from utils import has_numbers

class DataProcess():
    def __init__(self, df):
        self.df = df

    def fill_null(self, value):
        return self.df.fillna(value)

    def drop_null_col(self):
        return self.df.dropna(axis=1)
         
    def drop_null_row(self):
        return self.df.dropna(axis=0)

    def drop_duplicates(self):
        return self.df.drop_duplicates()

    def edit_cell(self, changes):
        for key, value in changes.items():
            x , y = key.split(',')
            self.df.iat[int(x), int(y)] = value
        return self.df
    

class ColumnProcess(DataProcess):
    def __init__(self, df:DataFrame, column:str) -> None:
        super().__init__(df)
        self.column = column

    def drop_column(self) -> DataFrame:
        return self.df.drop(columns=[self.column])

    def fill_null_col(self, value:str) -> DataFrame:
        self.df[self.column] = self.df[self.column].fillna(value)
        return self.df

    def split_col(self, sep:str) -> DataFrame:
        splited_columns = self.df[self.column].str.split(sep, expand=True)
        # splited_columns = df.stack().str.split("\t",expand=True).unstack().swaplevel(axis=1)[df.columns]
        self.df[[f'New Column{index+1}' for index in splited_columns ]] = splited_columns
        return self.df

    def rename_col(self, new_name:str) -> DataFrame:
        return self.df.rename(columns={self.column:new_name}, inplace=True)

    def join_cols(self, cols:list[str]) -> DataFrame:
        for col in cols:
            self.df[self.column] += self.df[col]
        return self.df


    def move_col(self, direction:str) -> DataFrame:
        columns = self.df.columns.tolisst()
        index = self.df.columns.get_loc(self.column)
        new_cols = self.move_to(columns, index, direction)
        return self.df[new_cols]

    @classmethod
    def move_to(cls, cols:list[str], index:int, direction:str) -> DataFrame:
        if direction == "right":
            if index+1 < len(cols):
                cols = cols[0:index]  + [cols[index+1], cols[index]] + cols[index+2:]
            return cols
        if direction == "left":
            if index > 0 :
                cols = cols[0:index-1]  + [cols[index],cols[index-1]] + cols[index+1:]
            return cols
        if direction == "first":
            return cols[index:index+1] + cols[0:index] + cols[index+1:]
        if direction == "last":
            return cols[0:index] + cols[index+1:] + cols[index:index+1]


class Classifier():
    def __init__(self, df:DataFrame) -> None:
        self.df = df
        self.numeric_columns =[]
        self.boolean_columns =[]
        self.datetime_columns =[]
        self.categorical_columns =[]
        self.columns_list = self.df.columns.to_list()

    def classify(self) -> tuple[list[str]]:
        self.numeric_columns  = self.list_numeric_columns()
        self.boolean_columns = self.list_boolean_columns()
        self.datetime_columns = self.list_datetime_columns()
        self.categorical_columns = self.list_categorical_columns()

        return (self.numeric_columns, self.boolean_columns, self.datetime_columns, self.categorical_columns, self.columns_list)

    def list_numeric_columns(self) -> list[str]:
        numerics = ["int16", "int32", "int64","float16", "float32", "float64"]
        return self.filter_columns(include=numerics)
    
    def list_boolean_columns(self) -> list[str]:
        return self.filter_columns(include=[bool])
    
    def list_datetime_columns(self) -> list[str]:

        other_dtypes_columns = list((
                set(self.columns_list) - 
                set(self.numeric_columns) - 
                set(self.boolean_columns)
                ))
                
        for col in  self.df[other_dtypes_columns]:
            sample = self.df[col].sample(10).to_list()
            if len(col) > 6 and has_numbers(sample) :
                try:
                    self.df[col] = pd.to_datetime(self.df[col])
                    self.datetime_columns.append(col)
                    other_dtypes_columns.remove(col)
                except:
                    pass 
        return self.datetime_columns

    def list_categorical_columns(self) -> list[str]:
        return list((
            set(self.columns_list) - 
            set(self.numeric_columns) - 
            set(self.boolean_columns) -
            set(self.datetime_columns)
        ))

    def filter_columns(self, include:list[str]) -> list[str]:
        columns = self.df.select_dtypes(include=include).columns
        return columns.to_list()

