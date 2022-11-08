import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# !pip install statsmodels
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

df_control = pd.read_excel("datasets/ab_testing.xlsx", sheet_name="Control Group")

df_test = pd.read_excel("datasets/ab_testing.xlsx", sheet_name="Test Group")

#for the control group;
df_control.head()
df_control.describe().T
df_control.isnull().sum()
df_control.shape

#for the test group;
df_test.head()
df_test.describe().T
df_test.isnull().sum()
df_test.shape

df_control["advertisement"]= 0
df_test["advertisement"]= 1

df= pd.concat([df_control, df_test])
df.head()
df.shape

df_control["Purchase"].mean()

df_test["Purchase"].mean()

# Normallik Varsayımı :
# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1: Normal dağılım varsayımı sağlanmamaktadır.
# p < 0.05 H0 RED , p > 0.05 H0 REDDEDİLEMEZ

test_stat, pvalue = shapiro(df.loc[df["advertisement"] == 0, "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
#p-value 0.5891 reddedilemez Normallik varsayımı sağlanmaktadır

test_stat, pvalue = shapiro(df.loc[df["advertisement"] == 1, "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
#p-value = 0.1541 reddedilemez Normallik varsayımı sağlanmaktadır

# VaryansHomojenliği :

test_stat, pvalue = levene(df.loc[df["advertisement"] == 0, "Purchase"],
                           df.loc[df["advertisement"] == 1, "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# p-value = 0.1083 reddedilemez Normallik varsayımı sağlanmaktadır

#Normallik Varsayımı ve Varyans Homojenliği heaplamalarının 0.05'den yüksek değerlere sahip olması
# İki durum için de Normallik varsayımını sağladığından hipotezlerin uygulanması aşamasında parametrik
#yöntem olan t testi kullanılır.

test_stat, pvalue = ttest_ind(df.loc[df["advertisement"] == 1, "Purchase"],
                              df.loc[df["advertisement"] == 0, "Purchase"],
                              equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

#p-value = 0.3493 reddedilemez Normallik varsayımı sağlanmaktadır
#sonuç olarak
# H0= Yeni Tasarımın (AVERAGE BIDDING) Dönüşüm Oranı ile Eski Tasarımın (MAXIMUM BIDDING) Dönüşüm Oranı Arasında İstatistiksel Olarak Anlamlı Farklılık Yoktur.
#Hipotezinin doğruluğu istatistiksel olarak anlamlıdır.
