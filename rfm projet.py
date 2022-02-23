import pandas as pd
import datetime as dt

#Load Data
df_= pd.read_excel(r"C:\Users\hp\PycharmProjects\pythonProject\online_retail_II.xlsx", sheet_name ="Year 2010-2011")
df=df_.copy()
df.describe()

#Missing Values
df.isnull().sum()
df.dropna(inplace=True)

#Preparing Data
df["Description"].nunique()
df.groupby("Description").agg({"Quantity": "count"})
df.groupby("Description").agg({"Quantity": "count"}).sort_values("Quantity", ascending=False).head(5)
df= df[~df["Invoice"].str.contains("C", na=False)]
df["TotalPrice"]= df["Price"] * df["Quantity"]

#RFM

today_date = dt.datetime(2011,12,11)
rfm= df.groupby('Customer ID').agg({'InvoiceDate': lambda date :(today_date- date.max()).days,
'Invoice': lambda num: num.nunique() ,
'TotalPrice': lambda TotalPrice: TotalPrice.sum()})

rfm.columns= ["recency", "frequency" , "monetary"]
rfm=rfm[rfm["monetary"]>0]

#RFM Scores
rfm["recency_score"]= pd.qcut( rfm["recency"],5, labels=[5,4,3,2,1] )
rfm["frequency_score"]=pd.qcut(rfm["frequency"].rank(method="first"),5, labels=[1,2,3,4,5])
rfm["RFM_SCORE"]=rfm["recency_score"].astype(str)+ rfm["frequency_score"].astype(str)

#Customer Segmentation

seg_map = {
         r'[1-2][1-2]': 'hibernating',
         r'[1-2][3-4]': 'at_risk',
         r'[1-2]5': 'cant_loose',
         r'3[1-2]': 'about_to_sleep',
         r'33': 'need_attention',
         r'[3-4][4-5]': 'loyal_customers',
         r'41': 'promising',
         r'51': 'new_customers',
         r'[4-5][2-3]': 'potential_loyalists',
         r'5[4-5]': 'champions'
     }
rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map, regex=True)

#Review Loyal Customers
lyl_cstmrs =rfm[rfm['segment']== 'loyal_customers']
lyl_cstmrs= lyl_cstmrs.reset_index()
lyl_cstmrs["Customer ID"].to_excel("lyl_cstmr_output.xlsx")

