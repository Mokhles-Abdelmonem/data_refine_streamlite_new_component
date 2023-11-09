

class DataProcess():
    def __init__(self, df):
        self.df = df

    def fill_null(self, value):
        return self.df.fillna(value)

    def drop_duplicates(self):
        return self.df.drop_duplicates()

    def edit_cell(self, changes):
        for key, value in changes.items():
            x , y = key.split(',')
            self.df.iat[int(x), int(y)] = value
        return self.df
    

class ColumnProcess(DataProcess):
    def __init__(self, df, column):
        super().__init__(df)
        self.column = column

    def drop_column(self):
        return self.df.drop(columns=[self.column])

    def drop_null_col(self):
        return self.df.dropna(axis=1)
         
    def drop_null_row(self):
        return self.df.dropna(axis=0)

    def fill_null_col(self, value):
        self.df[self.column] = self.df[self.column].fillna(value)
        return self.df

    def split_col(self, sep):
        splited_columns = self.df[self.column].str.split(sep, expand=True)
        # splited_columns = df.stack().str.split("\t",expand=True).unstack().swaplevel(axis=1)[df.columns]
        self.df[[f'New Column{index+1}' for index in splited_columns ]] = splited_columns
        return self.df

    def rename_col(self, new_name):
        return self.df.rename(columns={self.column:new_name}, inplace=True)

    def join_cols(self, cols):
        for col in cols:
            self.df[self.column] += self.df[col]
        return self.df


    def move_col(self, direction):
        columns = self.df.columns.tolisst()
        index = self.df.columns.get_loc(self.column)
        new_cols = self.move_to(columns, index, direction)
        return self.df[new_cols]

    @classmethod
    def move_to(cls, cols, index, direction):
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
