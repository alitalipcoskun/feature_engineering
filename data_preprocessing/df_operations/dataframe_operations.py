import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


"""
Feature scaling her veriye aynı şartlar altında yaklaşabilmeyi amaçlandığı için yaygın olarak kullanılan bir yaklaşımdır.
Aynı zamanda gradient descent temelli makine öğrenmesi algoritmalarının daha hızlı ve efektif çalışmasını da sağlamaktadır.
Büyük değerlere sahip veriler, küçük yapılı değerlere baskın geldiğinde PCA, kNN gibi algoritmalarda bias oluşmasına sebep olmaktadır.

Ağaca bağlı değerler nan değerlerden, aykırı değerlerden ve standartlaştırmalardan etkilenmemektedir. Ağaçlar, tüm olasılıkları göz önünde bulundurduğu için
etkilenmemektedir.


"""
class df_operations:
    def __init__(self, 
                 path:str = "datasets\diabetes.csv") -> None:
        self.__set_path(path)

    def get_path(self) -> str:
        return self.__path

    def __set_path(self,
                   path: str):
        self.__path = path


    def loadCsvDataset(self) -> pd.DataFrame:
        """
        Takes the path of the dataset, which is csv file, returns the dataframe.
            path: Takes a string path argument to return the dataframe.

        Returns:
            df: Returns the dataframe that is located to the path.

        """
        path = self.get_path()
        df = pd.read_csv(path)
        path_list = path.split("\\")
        dataframe_name = path_list[-1]
        print(f"{path} located {dataframe_name} file is succesfully read by your pre-processing environment!")
        return df

    def lowercaseColNames(self,
                         df: pd.DataFrame) -> pd.DataFrame:
        """
        The function takes a dataframe as input and returns the dataframe as same. However, it changes the column names to lowercased version of the original.

        Parameters:
            df -> pd.DataFrame: It is the dataframe that the name of the columns are converted to lowercase.

        Returns: pd.DataFrame
            df -> pd.DataFrame: It is the same dataframe as input value but its column names are converted to the lowercase.

        """
        df.columns = [column.lower() for column in df.columns]
        return df

    def verifyColumn(self,
                    df: pd.DataFrame,
                    column: str):
        """
        The function finds out whether the input string is in the list of dataframe's columns or not

            Parameters:
                df -> pd.DataFrame: The dataframe that must be checked to find out whether the input string is column of its or not.
                column -> str: The string that to gets checked in this function.

            Returns:
                None
        """
        if column not in df.columns:
            path = self.get_path()
            path_list = path.split("\\")
            dataframe_name = path_list[-1] 
            raise Exception(f"{column} is not in the list of {dataframe_name[-1]} columns.")
    def seperateColumns(self,
                        df: pd.DataFrame,
                        categoricTh: int = 8,
                        cardinalTh: int = 20) -> list:
        """
            The function helps you seperate columns as follows: categoric, numeric, ordinal

            Parameters:
                df -> pd.DataFrame: It is the dataframe that the columns must be seperated.
                categoricTh -> int: It is the treshold for categoric variables. It is defined 8 as default.
                cardinalTh -> int: It is the treshold for cardinal variables. It is defined 20 as default.

            Returns: [categoric_cols, numeric_cols, ordinal_cols]
                categoric_cols -> list: It holds the categoric typed columns after the function execution
                numeric_cols -> list: It holds the numeric typed columns after the function execution
                ordinal_cols -> list: It holds the ordinal typed columns after the function execution.
        """
        assert categoricTh >= 8, f"{categoricTh} is not a valid amount to consider"
        assert cardinalTh >= 20 , f"{cardinalTh} is not a valid amount to consider"


        categoric_cols = [column for column in df.columns if df[column].dtypes == 'O']
        numeric_columns = [column for column in df.columns if df[column].dtypes != 'O']
        num_but_cats = [column for column in df.columns if df[column].nunique() < categoricTh and df[column].dtypes != 'O']

        cat_but_cardinals = [column for column in categoric_cols if df[column].nunique() > cardinalTh]

        categoric_cols = categoric_cols + num_but_cats
        categoric_cols = [column for column in categoric_cols if column not in cat_but_cardinals]

        numeric_columns = [column for column in numeric_columns if column not in num_but_cats]

        return [categoric_cols, numeric_columns, cat_but_cardinals]

    def category_convert(self,
                        df: pd.DataFrame,
                        categoric_cols: list[str]) -> pd.DataFrame:
        
        for column in categoric_cols:
            df[column] = df[column].astype(object)

        return df

    def one_hot_encoder(self,
                        df: pd.DataFrame,
                        cat_cols: list[str],
                        num_cols: list[str],
                        drop_first: bool = True) -> pd.DataFrame:
        
        """
            It converts labeled data to different categories that have a natural ordering to them.
            Any categorical data must be mapped to integers in order to use in machine learning.

            args:
                df -> pd.DataFrame: dataframe that wanted to be encoded.
                cat_cols -> the list that includes categorical behaviour columns.
                num_cols -> list[str]:the list that includes numerical behaviour columns.
                drop_first -> bool = True: it improves accuracy of predictions and protects data repetition. It has True value by default.

            returns:
                output_df -> pd.DataFrame: It returns encoded dataframe. 
        """
        output_df = pd.get_dummies(df[cat_cols + num_cols], drop_first= drop_first)

        return output_df

    def rare_analyser(self,
                     df: pd.DataFrame,
                     target_col: str,
                     cat_cols: list[str]) -> pd.DataFrame:
        """
        The function analyzes the columns with respect to the target column.

        args:
            df -> pd.DataFrame: dataframe that wanted to be get analyzed by its target column.
            target_col -> str: the column name that is targeted for prediction.
            cat_cols: -> list[str]: the list that includes categoric typed columns in dataframe

        returns:
            None  
        
        """
        
        for column in cat_cols:
            print(f"{column}: {len(df[column].value_counts())}")
            printed_df = pd.DataFrame({
                "Count": df[column].value_counts(),
                "Ratio": df[column].value_counts() / len(df),
                "Target Mean": df.groupby(column)[target_col].mean()})
            
            print(printed_df, end = "\n\n")
    

    def rare_encoder(self,
                    df: pd.DataFrame,
                    cat_cols: list[str],
                    rare_th: float = 0.1) -> pd.DataFrame:
        
        #Protect the dataframe with copying
        output_df = df.copy()

        #Find out the columns that has rare labels on its rows.
        rare_cols = [column for column in cat_cols if((output_df[column].value_counts() / len(output_df)) < rare_th).any()]

        #Process the columns that has rare labels
        for column in rare_cols:
            temp = output_df[column].value_counts() / len(output_df)
            rare_labels = temp[temp < rare_th].index
            output_df[column] = np.where(output_df[column].isin(rare_labels), 'Rare', output_df[column])
            #Debugging
            print(output_df[column].value_counts())
            print(f"{column}: {len(df[column].value_counts())}")
            printed_df = pd.DataFrame({
                "Count": output_df[column].value_counts(),
                "Ratio": output_df[column].value_counts() / len(df),
                "Target Mean": output_df.groupby(column)['survived'].mean()})
            
            print(printed_df, end = "\n\n")
        #Return the new dataframe
        return output_df




    def scale_with_minmax(self,
                          df: pd.DataFrame) -> pd.DataFrame:
        """
            Minimum of the feature is considered as zero and maximum of feature is
            considered as one. It transforms data by scaling features to a given range.

            args:
                df -> pd.DataFrame: dataframe that wanted to scale with MinMaxScaler.
            
            returns:
                output_df -> pd.DataFrame: It returns scaled dataframe.
        """
        scaler = MinMaxScaler()
        output_df = pd.DataFrame(scaler.fit_transform(df), columns = df.columns)
        return output_df
    
    def inverse_minmax_transform(self,
                          df: pd.DataFrame) -> pd.DataFrame:
        """
        It inverses the transformation with respect to the MinMax scaler
        to observe the changes in dataframe.
        
        args:
            df -> pd.DataFrame: dataframe that wanted to inversed.
        
        returns:
            output_df -> pd.DataFrame: dataframe that inversed transformation
            with respect to the MinMaxScaler.
        """

        scaler = MinMaxScaler()
        output_df = pd.DataFrame(scaler.inverse_transform(df), columns = df.columns)
        return output_df