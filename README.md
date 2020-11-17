# INCH
 ### For deployment:

Update and install git
 ```
 sudo apt update 
```

```
apt install git
```
Clone repo
```
git clone https://github.com/etherscam/INCH.git
```

```
chmod +x INCH/APP_INSTALL
```
Build
```
./INCH/APP_INSTALL
```
Заполните файл wallets (кошельки без пробелов/кавычек/запятых)

0x123

0x777
```
nano wallets

```
Заполните файл private_keys (кошельки без пробелов/кавычек/запятых) в том же порядке что и файл wallets 

123(для 0x123)

777(для 0x777)
```
nano private_keys

```
Запустите 
```
python3 1_INCH.py

```

