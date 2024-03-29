import pandas as pd
import sys
#It is for importing the dfOps class.
sys.path.append(r"C:\Users\ali_t\data_science\data_science_practices\feature_engineering\data_preprocessing")
from df_operations import dfOps
from outliers._single_outliers import singleColOutliers as singleCol
from sklearn.neighbors import LocalOutlierFactor


"""
Local Outlier Factor değeri, çok değişkenli bir aykırı değer belirleme yöntemidir.
Gözlemleri yoğunluk tabanlı skorlayarak, buna göre aykırı değer tanımı yapabilmeyi sağlar.
LOF'un verdiği skor 1'e ne kadar yakınsa o kadar iyidir.
1'den uzaklaştıkça, ilgili değer outlier olmaya yakınlaşır.
Verileri iki boyutlu olarak görselleştirebilmek dimentional reduction. (PCA)
Principle Component Analysisle yapılabilir.
"""

"""
Local Outlier Factor is used to determine outliers with respect to the multi-variable(multiple columns).

When the score is close to 1, it means that it is good, which means not outlier, for the row.

"""


class outlier_handler(singleCol):
    
    def __init__(self,
                path: str,
                q1: int = 0.1,
                q3: int = 0.9,
                n_neighbors: int = 20):
        
        super().__init__(q1= q1, q3= q3, path= path)
        self.__set_lof(LocalOutlierFactor, n_neighbors= n_neighbors)
    
    def getTresholds(self):
        return [self.__cardinalTh, self.__categoryTh]

    def setTresholds(self,
                     cardinalTh: int = 20,
                     categoryTh: int = 8) -> None:
        self.__cardinalTh = cardinalTh
        self.__categoryTh = categoryTh
    def __get_lof(self) -> LocalOutlierFactor:
        return self.__lof

    def __set_lof(self, 
                local_outlier: LocalOutlierFactor,
                n_neighbors: int = 20) -> None:
        
        self.__lof = local_outlier(n_neighbors= n_neighbors)

    def findLocalOutlierFactor(self,
                               df: pd.DataFrame):
        lof_calculator = self.__get_lof()
        lof_calculator.fit_predict(df)
        df_scores = lof_calculator.negative_outlier_factor_
        print(df_scores)

