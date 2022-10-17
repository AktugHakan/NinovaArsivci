## TEST AŞAMASINDAKİ ÖZELLİKLER
* İndirme işlemi paralel hale getirildi. Aynı anda bir dosya indirmek yerine birkaç dosya indiriliyor bu sayede programın çalışma süresi yarı yarıya azalmalıdır.

*Eğer hata alırsanız, programı düzeltebilmem için "issues" bölümünden bildirin.*

# Ninova Arşivci v2 TEST

Ninova Arşivci, [Ninova](https://ninova.itu.edu.tr/)'daki dosyaları topluca indirmek için yazılmış bir Python programıdır.
(Ninova: İstanbul Teknik Üniversitesinin e-öğrenim merkezi)

## Kurulum
Bu program [Python yorumlayıcısı (interpreter)](https://www.python.org/downloads/) gerektirir.
1. Üst sağ köşedeki yeşil "Code" butonuna tıklayın ve zip olarak indirin
2. NinovaArsivci-main klasörünü zipten çıkarın.
3. Çıkarttığınız klasöre girin ve aşağıdaki komutu yazın. Bu komut gerekli kütüphaneleri yükleyecektir.
```bash
pip install -r requirements.txt
```


## Kullanım
1. Daha önceden zipten çıkartmış olduğunuz klasöre girin
2. Buradan bir uçbirim (terminal) başlatın (Sağ tık > Uçbirimde aç)
3. Aşağıdaki komut ile programı başlatın:
```bash
python main.py
```

## S.S.S.
1. "HATA! src klasörü bulunamadı veya yeri değiştirilmiş. Programı yeniden indirin." diye bir hata alıyorum.  

Programı arşivden çıkarırken src klasörünü de çıkarmalısın. "main.py" dosyası src klasörü içindeki dosyalarla birlikte çalışır.

2. "No such file or directory" hatası alıyorum.  

Terminalin açıldığı klasör, main.py ile klasör olmalı.

3. Şifremi giriyorum ama çalar mısın?  

Hayır.


## Notlar
* Eğer indirme klasöründe indirilen dosya ile aynı isimde bir dosya varsa üstüne yazılır.
* İndirdiğiniz dosyaları değiştirseniz de programı çalıştırdığınızda Ninova'daki halleri indirilir ve üstüne yazılır.
* Program her çalıştırıldığında tüm dosyalar tekrar indirilir.
* Programın tamamlanması süresi 3-4 dakika sürebilir.
* Detaylı bilgileri görmek için src/logger.py dosyasındaki "DEBUG = False" satırını "DEBUG = True" ile değiştirin.

## Deneysel Özellikleri Test Edin
Eğer yeni özellikleri önceden keşfetmek ve programı geliştirmeme yardımcı olmak isterseniz sol üst köşede, üstünde "main" yazan butona tıklayın ve mevcut dalı Nightly ile değiştirin. Daha sonra normal kurulum adımlarını takip edin.

## Hata bildirimi
Programın github sayfasındaki "issues" sekmesi altından, aldığınız hataları veya önerilerinizi yazabilirsiniz.
