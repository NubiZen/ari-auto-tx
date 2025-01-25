# AriChain Wallet Auto Transfer Script  
Script untuk melakukan auto-transfer pada wallet AriChain dengan opsi penggunaan proxy.  

## Tools dan Komponen yang Dibutuhkan  
1. **Ari Chain Account**  
   - Download: [iOS](https://apps.apple.com/kr/app/ari-wallet/id6504207160) / [Android](https://play.google.com/store/apps/details?id=arichain.app.ari.wallet)  
   - Registrasi dan masukkan referral code: `678e6a1b1c1b1`  

2. **Proxy (Opsional)**  
   - Proxy mendukung format `http` dan `https`  

3. **VPS atau RDP (Opsional)**  
4. **Python Versi 3.10 atau Lebih Baru**  

### Proxy (Opsional)  

## Instalasi  
### Windows  
1. Unduh Python: [Python 3.13 (64-bit)](https://www.python.org/ftp/python/3.13.0/python-3.13.0-amd64.exe)  
2. Pastikan Python ditambahkan ke PATH saat instalasi.  

### Unix/Linux  
```bash  
apt install python3 python3-pip git -y  
```  

### Termux  
```bash  
pkg install python python-pip git -y  
```  

### Unduh Script  
- Unduh manual: [Download](https://github.com/NubiZen/ari-auto-tx/archive/refs/heads/main.zip)  
- Atau gunakan git:  
```bash  
git clone https://github.com/NubiZen/ari-auto-tx
```  

## Instalasi Dependensi  
- Masuk ke folder bot:  
```bash  
cd ari-auto-tx
```  

## Menjalankan Bot  
1. Ganti file `accounts.txt` dengan format:  
   ```
   email1|password1|address1|private_key1  
   email2|password2|address2|private_key2  
   ```  

2. (Opsional) Tambahkan proxy pada file `proxy.txt` dengan format:  
   ```
   http://127.0.0.1:8080  
   http://user:pass@127.0.0.1:8080  
   ```  

3. Jalankan script:  
   - Windows/Termux:  
     ```bash  
     python main.py  
     ```  
   - Unix/Linux:  
     ```bash  
     python3 main.py  
     ```  

## Catatan  
- Bot ini memiliki jeda waktu 50 detik per transaksi dengan jumlah transfer sebesar 1 ARI.
- Bot auto loop setiap 24 Jam apabila semua transaksi sudah berhasil.  
- Penggunaan proxy bersifat opsional. Jika tidak ada proxy, bot akan berjalan tanpa proxy.  
- Harap gunakan script ini dengan tanggung jawab. Saya tidak bertanggung jawab atas kerugian atau kerusakan akibat penggunaan bot ini.  
- Bot ini hanya untuk tujuan edukasi.  
