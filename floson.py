import pandas as pd
import datetime as dt
from sklearn.preprocessing import MinMaxScaler
pd.set_option("display.max_columns", None)
pd.set_option("display.float_format", lambda x: "%.2f" % x)

df_kopya = pd.read_csv("flo_data_20k.csv")
df = df_kopya.copy()
df.head(10)

#Veri seti Flo’dan son alışverişlerini 2020 - 2021 yıllarında OmniChannel olarak yapan müşterilerin
#geçmiş alışveriş davranışlarından elde edilen bilgilerden oluşmaktadır

#master_id = Eşsiz müşteri numarası
#order_channel = Alışveriş yapılan platforma ait hangi kanalın kullanıldığı (Android, ios, Desktop, Mobile)
#last_order_channel = En son alışverişin yapıldığı kanal
#first_order_date = Müşterinin yaptığı ilk alışveriş tarihi
#last_order_date = Müşterinin yaptığı son alışveriş tarihi
#last_order_date_online = Müşterinin online platformda yaptığı son alışveriş tarihi
#last_order_date_offline = Müşterinin offline platformda yaptığı son alışveriş tarihi
#order_num_total_ever_online = Müşterinin online platformda yaptığı toplam alışveriş sayısı
#order_num_total_ever_offline = Müşterinin offline'da yaptığı toplam alışveriş sayısı
#customer_value_total_ever_offline = Müşterinin offline alışverişlerinde ödediği toplam ücret
#customer_value_total_ever_online = Müşterinin online alışverişlerinde ödediği toplam ücret
#interested_in_categories_12 = Müşterinin son 12 ayda alışveriş yaptığı kategorilerin liste

#Veriye göz attım.
df.columns
df.shape
df.describe().T
df.isnull().sum()
df.info()

#Her bir müşterinin toplam alışveriş sayısı ve harcaması bulmak için yeni değişkenler oluşturturdum.
df["order_num_total"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
df["customer_value_total"] = df["customer_value_total_ever_offline"] + df["customer_value_total_ever_online"]

#Tarih ifade eden değişkenlerin tipini date'e çevirdim.
date_columns = df.columns[df.columns.str.contains("date")]
df[date_columns] = df[date_columns].apply(pd.to_datetime)
df.info()

#Alışveriş kanallarındaki müşteri sayısının, toplam alınan ürün sayısının ve toplam harcamaların dağılımını inceledim.
df.groupby("order_channel").agg({"master_id": "count",
                                 "order_num_total": "sum",
                                 "customer_value_total": "sum"})


#Veri ön hazırlık süreci için bir fonksiyon tanımladım.
#Bu fonksiyon her bir müşterinin toplam alışveriş sayısı ve harcaması için yeni değişkenler oluşturacak ve tarih ifade eden değişkenlerin tipini date'e çevirecek.
def data_prep(dataframe):
    dataframe["order_num_total"] = dataframe["order_num_total_ever_online"] + dataframe["order_num_total_ever_offline"]
    dataframe["customer_value_total"] = dataframe["customer_value_total_ever_offline"] + dataframe["customer_value_total_ever_online"]
    date_columns = dataframe.columns[dataframe.columns.str.contains("date")]
    dataframe[date_columns] =dataframe[date_columns].apply(pd.to_datetime)
    return df

data_prep(df)

#RFM METRİKLERİNİ HESAPLADIM.
#en son alışveriş tarihinden iki gün sorayı analiz yaptığımızı varsaydım

df["last_order_date"].max() #'2021-05-30'

analysis_date = dt.datetime(2021,6,1)
type(analysis_date)

#customer_id, Recency, Frequency ve Monetary

rfm = pd.DataFrame()
df["last_order_date"]
rfm["customer_id"] = df["master_id"]
rfm["recency"] = (analysis_date - df["last_order_date"]).astype('timedelta64[D]')
rfm["frequency"] = df["order_num_total"]
rfm["monetary"] = df["customer_value_total"]

rfm.head()

# Recency, Frequency ve Monetary metriklerini qcut yardımı ile 1-5 arasında skorlara çevirdim.
rfm["recency_score"] = pd.qcut(rfm["recency"], 5, labels=[5, 4, 3, 2, 1])
rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]) #frekanslarda oluşabilecek sorun için rank metodunu kullandım.
rfm["monetary_score"] = pd.qcut(rfm["monetary"], 5, labels=[1, 2, 3, 4, 5])

rfm.head()

# recency_score ve frequency_score’u tek bir değişken olarak ifade ettim ve RF_SCORE olarak kaydettim.
rfm["RF_SCORE"] = (rfm["recency_score"].astype(str) + rfm["frequency_score"].astype(str))

# RF Skorunun Segment Olarak Tanımladım
seg_map = {
    r"[1-2][1-2]": "hibernating",
    r"[1-2][3-4]": "at_Risk",
    r"[1-2]5": "cant_loose",
    r"3[1-2]": "about_to_sleep",
    r"33": "need_attention",
    r"[3-4][4-5]": "loyal_customers",
    r"41": "promising",
    r"51": "new_customers",
    r"[4-5][2-3]": "potential_loyalists",
    r"5[4-5]": "champions",
}

rfm["segment"] = rfm["RF_SCORE"].replace(seg_map, regex=True)
rfm.head()

#Segmentlerin recency, frequnecy ve monetary ortalamalarını inceledim.
rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean", "count"])

#RFM analizi yardımıyla aşağıda verilen 2 case için ilgili profildeki müşterileri buldum ve müşteri id'lerini csv olarak kaydettim.

#CASE1
#FLO bünyesine yeni bir kadın ayakkabı markası dahil ediyor.
#Dahil ettiği markanın ürün fiyatları genel müşteri tercihlerinin üstünde.
#Bu nedenle markanın tanıtımı ve ürün satışları için ilgilenecek profildeki müşterilerle özel olarak iletişime geçmek isteniliyor.
#Sadık müşterilerinden(champions, loyal_customers) ve kadın kategorisinden alışveriş yapan kişiler özel olarak iletişim kurulacak müşteriler.
#Bu müşterilerin id numaralarını csv dosyasına kaydediniz

#rfm segmenti champions ve loyal customers olanların idlerini tuttum.
target_segments_customer_ids = rfm[rfm["segment"].isin(["champions","loyal_customers"])]["customer_id"]
#master idsi target segment customer id içinde olanları ve kadın olanları cust_id içerisinde tuttum.
cust_ids = df[(df["master_id"].isin(target_segments_customer_ids)) & (df["interested_in_categories_12"].str.contains("KADIN"))]["master_id"]
#cust_ids bir pandas serisiydi. Bunu yeni_marka_hedef_müşteri_id.csv olarak kaydettim.
cust_ids.to_csv("yeni_marka_hedef_müşteri_id.csv", index=False)

cust_ids.shape
rfm.head()

#CASE2
#Erkek ve Çocuk ürünlerinde %40'a yakın indirim planlanmaktadır.
#Bu indirimle ilgili kategorilerle ilgilenen geçmişte iyi müşteri olan ama uzun süredir alışveriş yapmayan kaybedilmemesi gereken müşteriler,
#uykuda olanlar ve yeni gelen müşteriler özel olarak hedef alınmak isteniyor.
#Uygun profildeki müşterilerin id'lerini csv dosyasına kaydediniz

target_segments_customer_ids2 = rfm[rfm["segment"].isin(["cant_loose","at_Risk", "new_customers"])]["customer_id"]
cust_ids2 = df[(df["master_id"].isin(target_segments_customer_ids2)) & ((df["interested_in_categories_12"].str.contains("ERKEK"))|(df["interested_in_categories_12"].str.contains("ÇOCUK")))]["master_id"]
cust_ids2.to_csv("indirim_hedef_müşteri_id.csv", index=False)

#RFM metriklerini hesaplamak için bir fonksiyon tanımladım.
def create_rfm(dataframe):
    #veriyi hazırlama
    dataframe["order_num_total"] = dataframe["order_num_total_ever_online"] + dataframe["order_num_total_ever_offline"]
    dataframe["customer_value_total"] = dataframe["customer_value_total_ever_offline"] + dataframe["customer_value_total_ever_online"]
    date_columns = dataframe.columns[dataframe.columns.str.contains("date")]
    dataframe[date_columns] = dataframe[date_columns].apply(pd.to_datetime)

    #RFM metriklerinin hesaplanması
    dataframe["last_order_date"].max() #2021-05-30
    analysis_date = dt.datetime(2021, 6, 1)
    rfm = pd.DataFrame()
    rfm["customer_id"] = dataframe["master_id"]

    rfm["recency"] = (analysis_date - dataframe["last_order_date"]).astype('timedelta64[D]')

    rfm["frequency"] = dataframe["order_num_total"]

    rfm["monetary"] = dataframe["customer_value_total"]

    #RF VE RFM SKORLANININ HESAPLANMASI
    rfm["recency_score"] = pd.qcut(rfm["recency"], 5, labels=[5, 4, 3, 2, 1])
    rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
    rfm["monetary_score"] = pd.qcut(rfm["monetary"], 5, labels=[1, 2, 3, 4, 5])
    rfm["RF_SCORE"] = (rfm["recency_score"].astype(str) + rfm["frequency_score"].astype(str))
    rfm["RFM_SCORE"] = (rfm["recency_score"].astype(str) + rfm["frequency_score"].astype(str) + rfm["monetary_score"].astype(str))


    #SEGMENTLERİN İSİMLENDİRİLMESİ
    seg_map = {
        r"[1-2][1-2]": "hibernating",
        r"[1-2][3-4]": "at_Risk",
        r"[1-2]5": "cant_loose",
        r"3[1-2]": "about_to_sleep",
        r"33": "need_attention",
        r"[3-4][4-5]": "loyal_customers",
        r"41": "promising",
        r"51": "new_customers",
        r"[4-5][2-3]": "potential_loyalists",
        r"5[4-5]": "champions",
    }

    rfm["segment"] = rfm["RF_SCORE"].replace(seg_map, regex=True)

    return rfm[["customer_id", "recency", "frequency", "monetary", "RF_SCORE", "RFM_SCORE", "segment"]]


create_rfm(df)







