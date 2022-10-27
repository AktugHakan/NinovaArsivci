# Ninova Arşivci v2.1

Ninova Arşivci, [Ninova](https://ninova.itu.edu.tr/)'daki dosyaları topluca indirmek için yazılmış bir Python programıdır.
(Ninova: İstanbul Teknik Üniversitesinin e-öğrenim merkezi)

## v2 Yeni Özellikler
* Birden fazla iş parçacığı ve süreç ile paralelleştirilmiş indirme işlemi, önceki sürüme göre **3 kat** daha hızlı.

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
### Komut satırı komutları
Kullanımı kolaylaştırmak ve otomasyonlara kolaylık sağlamak adına komut satırı parametreleri getirildi. Komutlar bir arada kullanılabilir ve sıralamaları önemli değildir.

1. "-u username password"
Bu komutu kullanarak kullanıcı adı ve şifrenizi komut satırı üzerinden verebilirsiniz. Bu komut kullanıldığı taktirde program çalışırken kullanıcı adı ve şifre sorulmaz.
Örnek kullanım:
```bash
python main.py -u bee20 psswd
```
2. "-d klasör"
Bu komut ile hangi klasöre indirileceğini komut satırından seçebilirsiniz. Bu komut kullanıldığı taktirde program çalışırken indirme için klasör seçme penceresi açılmaz.
Örnek kullanım:
```bash
python main.py -d "C:\Users\Bee\Desktop\Ninova"
```

3. "-debug" ve "-verbose"
Debug ve verbose bilgisini etkinleştirir. Verbose hangi işlemin kaç saniye sürdüğü bilgisini, debug ise daha detaylı bilgiler içerir. Debug modu seçildiği taktirde verbose komutları da görünecektir.
```bash
python main.py -verbose
```

4. "-core cekirdek_sayisi"
Bilgisayarınızda aynı anda kaç çekirdek ile işlem yapılacağını belirtir. Varsayılan değeri 2'dir. Çok fazla seçildiği taktirde program, otomatik olarak çekirdek sayısını düşürür.
```bash
python main.py -core 4
```

Komutların bir arada kullanımına örnek:
```bash
python main.py -u Bee20 passwd -debug -core 5
```

## S.S.S.
1. "HATA! src klasörü bulunamadı veya yeri değiştirilmiş. Programı yeniden indirin." diye bir hata alıyorum.  
  Programı arşivden çıkarırken src klasörünü de çıkarmalısın. "main.py" dosyası src klasörü içindeki dosyalarla birlikte çalışır.

2. "No such file or directory" hatası alıyorum.  
  Terminalin açıldığı klasör, main.py ile klasör olmalı.

3. Şifremi giriyorum ama çalar mısın?  
  Hayır.

4. İndirme klasörünü "-d" komutu ile komut satırı üzerinden verdiğim halde klasör seçme penceresi açılıyor.  
  Parametre olarak verdiğin yolu kontrol et.



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
