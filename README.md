# Ninova Arşivci v3 BETA

Ninova Arşivci, [Ninova](https://ninova.itu.edu.tr/)'daki dosyaları topluca indirmek için yazılmış bir Python programıdır.  
(Ninova: İstanbul Teknik Üniversitesinin e-öğrenim merkezi)

## v3 Yeni Özellikler
* İndirilen yeni dosyalar, program sonunda ekrana yazdırılıyor.
* Artık dosya kayıtları bir veri tabanında tutuluyor. Bu sayede aynı dosyaların tekrar indirilmesinin önüne geçildi.
* Çoklu süreç sistemi, hıza katkısı olmadığı için kaldırıldı. Kod tabanı, tek çekirdekte çalışmak üzere optimize edildi.
* "-core" komut satırı parametresi kaldırıldı. Program tek çekirdek üzerinde çalışıyor.
* v3 sürümü v2 ile indirilmiş klasörlerde uyumlu çalışır. İndirme klasörünü v3'e yükseltmek için yeni sürümü indirin ve klasör üzerinde indirme işlemi yapın.
* Hatalı şifre girildiğinde programı kapatmak yerine tekrar soruyor.
* Klasör seçme penceresi, son seçilen klasörü hatırlıyor.

## Kurulum
Bu program [Python yorumlayıcısı (interpreter)](https://www.python.org/downloads/) gerektirir.
1. Üst sağ köşedeki yeşil "Code" butonuna tıklayın ve zip olarak indirin
2. NinovaArsivci-Nightly klasörünü zipten çıkarın.
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

Komutların bir arada kullanımına örnek:
```bash
python main.py -u Bee20 passwd -debug -verbose
```

## S.S.S.
1. "HATA! src klasörü bulunamadı veya yeri değiştirilmiş. Programı yeniden indirin." diye bir hata alıyorum.  
  Programı arşivden çıkarırken src klasörünü de çıkarmalısın. "main.py" dosyası src klasörü içindeki dosyalarla birlikte çalışır.  
  Eğer hata devam ediyorsa, issues kısmından bana bildir.

2. "No such file or directory" hatası alıyorum.  
  Terminalin açıldığı klasör, main.py ile aynı klasör olmalı.

3. Şifreleri topluyor musun? Şifrem güvende mi?  
  Şifreler tamamen yerelde kalıyor ve Ninova'ya giriş yaptıktan sonra siliniyor.

4. İndirme klasörünü "-d" komutu ile komut satırı üzerinden verdiğim halde klasör seçme penceresi açılıyor.  
  Parametre olarak verdiğin yolu kontrol et. Eğer yol geçerli değilse, kullanıcıya sorar
  
5. İndirme klasörünü "-d" komutu ile komut satırı üzerinden verdiğim halde klasör seçme penceresi açılıyor.  
  Parametre olarak verdiğin yolu kontrol et. Eğer yol geçerli değilse, kullanıcıya sorar
  
6. "Veri tabanına manuel müdahele tespit edildi!" hatası alıyorum. Ama ben veri tabanını değiştirmedim  
  Eğer önceki indirme yarıda kesilmişse, veri tabanı bozulabilir. Bu hata önemli değildir ve program akışını etkilemez. Dosyalar indirilir.
  
7. Klasörler oluşturuluyor ama dosyalar indirilmiyor.  
  Daha önce indirdiğin bir dosyayı silersen, tekrar indirilmez. Bu sorunu tüm dosyaları tekrardan indirerek çözebilirsin. Bunun için komut satırında çalıştırırken -f komutunu da ekle:  
  ```bash
  python main.py -f
  ```



## Notlar
* Eğer indirme klasöründe indirilen dosya ile aynı isimde farklı içerikte bir dosya varsa sonuna "_new" eklenerek kaydedilir.
* İndirdiğiniz dosyaları değiştirseniz de programı çalıştırdığınızda Ninova'daki halleri indirilir ve üstüne yazılır.
* Program çalıştırdığınızda yalnızca varolmayan dosyalar indirilir.
* Programın tamamlanması süresi 2-3 dakika sürebilir.
* Detaylı bilgileri görmek için programı çalıştırırken "-debug" ve "-verbose" parametrelerini ekleyin

## Hata bildirimi
Programın github sayfasındaki "issues" sekmesi altından, aldığınız hataları veya önerilerinizi yazabilirsiniz.
