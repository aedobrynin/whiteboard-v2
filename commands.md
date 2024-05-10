Удаляем папочку с данными mongo
```bash
rm -r server/mongo_data; mkdir server/mongo_data
```
Подключаем сервер mongo
```bash
mongod --dbpath server/mongo_data
```
Подключаем сервер
```bash
cd server/src
```
```bash
python main.py
```
Потом запускаем клиента дважды
```bash
cd ../../src
```
```bash
python main.py
```