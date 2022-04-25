Online ayakkabı mağazası olan FLO müşterilerini segmentlere ayırıp bu segmentlere göre pazarlama stratejileri belirlemek istiyor. Buna yönelik olarak
müşterilerin davranışları tanımlanacak ve bu davranışlardaki öbeklenmelere göre gruplar oluşturulacak

# Veri seti Flo’dan son alışverişlerini 2020 - 2021 yıllarında OmniChannel olarak yapan müşterileringeçmiş alışveriş davranışlarından elde edilen bilgilerden oluşmaktadır

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


# Veriye göz attım.
![Ekran görüntüsü 2022-04-25 052038](https://user-images.githubusercontent.com/101973346/165010181-4a30da9d-5005-4ac9-a8cd-8e25bd9b9674.png)
![2](https://user-images.githubusercontent.com/101973346/165010287-c74fb619-77e4-432d-8275-980325c5e3d4.png)
![3](https://user-images.githubusercontent.com/101973346/165010294-f67976b1-c6aa-4208-9830-a29211c33416.png)
![4](https://user-images.githubusercontent.com/101973346/165010297-a6a081ba-e8b5-46fc-9294-3afa4e8b8d05.png)

#Her bir müşterinin toplam alışveriş sayısı ve harcaması bulmak için yeni değişkenler oluşturturdum.
![1](https://user-images.githubusercontent.com/101973346/165010555-9cf6510c-ab84-4f94-aee7-c75d574fe836.png)

#Tarih ifade eden değişkenlerin tipini date'e çevirdim.
![2](https://user-images.githubusercontent.com/101973346/165010662-36ab15c1-a014-45e5-ae55-b71d4ed81491.png)

#Alışveriş kanallarındaki müşteri sayısının, toplam alınan ürün sayısının ve toplam harcamaların dağılımını inceledim.
![5](https://user-images.githubusercontent.com/101973346/165010723-9d08ca30-277c-4d41-9996-ad002a5c9559.png)

# Veri ön hazırlık süreci için bir fonksiyon tanımladım.
#Bu fonksiyon her bir müşterinin toplam alışveriş sayısı ve harcaması için yeni değişkenler oluşturacak ve tarih ifade eden değişkenlerin tipini date'e çevirecek.
![Y](https://user-images.githubusercontent.com/101973346/165010827-e8167e7a-38fd-44b1-9194-a695bb8bd23b.png)

# RFM METRİKLERİNİ HESAPLADIM.
#en son alışveriş tarihinden iki gün sorayı analiz yaptığımızı varsaydım
![NN](https://user-images.githubusercontent.com/101973346/165010978-51793482-ce47-4c92-9777-e3fa6143626e.png)

#customer_id, Recency, Frequency ve Monetary
![1](https://user-images.githubusercontent.com/101973346/165011061-b333531e-69e2-4359-b9cd-734fec000373.png)

#Recency, Frequency ve Monetary metriklerini qcut yardımı ile 1-5 arasında skorlara çevirdim.
![2](https://user-images.githubusercontent.com/101973346/165011183-a441fdb7-8e26-4719-b311-a1643119a53f.png)

#recency_score ve frequency_score’u tek bir değişken olarak ifade ettim ve RF_SCORE olarak kaydettim.
![B](https://user-images.githubusercontent.com/101973346/165011248-0d62b18e-3ee2-4083-8c50-d852f362111a.png)

#RF Skorunun Segment Olarak Tanımladım
![8](https://user-images.githubusercontent.com/101973346/165011364-22109b03-65d4-4b9f-a77f-efd7110276d1.png)
![99](https://user-images.githubusercontent.com/101973346/165011384-e4537919-8399-412f-a08b-c5313c74a253.png)

#Segmentlerin recency, frequnecy ve monetary ortalamalarını inceledim.
![1](https://user-images.githubusercontent.com/101973346/165011442-502ace69-bd13-4e95-95ad-7b3e62f89c94.png)

# RFM analizi yardımıyla aşağıda verilen 2 case için ilgili profildeki müşterileri buldum ve müşteri id'lerini csv olarak kaydettim.

# CASE1
#FLO bünyesine yeni bir kadın ayakkabı markası dahil ediyor.
#Dahil ettiği markanın ürün fiyatları genel müşteri tercihlerinin üstünde.
#Bu nedenle markanın tanıtımı ve ürün satışları için ilgilenecek profildeki müşterilerle özel olarak iletişime geçmek isteniliyor.
#Sadık müşterilerinden(champions, loyal_customers) ve kadın kategorisinden alışveriş yapan kişiler özel olarak iletişim kurulacak müşteriler.
#Bu müşterilerin id numaralarını csv dosyasına kaydediniz
![GG](https://user-images.githubusercontent.com/101973346/165011558-11615c99-7f4f-46bf-aeb7-5be657adb981.png)

# CASE2

#Erkek ve Çocuk ürünlerinde %40'a yakın indirim planlanmaktadır.

#Bu indirimle ilgili kategorilerle ilgilenen geçmişte iyi müşteri olan ama uzun süredir alışveriş yapmayan kaybedilmemesi gereken müşteriler, uykuda olanlar ve yeni gelen müşteriler özel olarak hedef alınmak isteniyor.

#Uygun profildeki müşterilerin id'lerini csv dosyasına kaydediniz

![fd](https://user-images.githubusercontent.com/101973346/165011757-395c98d7-c052-4495-9706-acf229172bb9.png)

# RFM metriklerini hesaplamak için bir fonksiyon tanımladım.












