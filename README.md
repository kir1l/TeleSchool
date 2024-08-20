## Cryptan on TON

### Установка бота

1. Установите зависимости:
```cli
pip install -r requirements.txt
```
   

2. Создайте файл `.env` в корне проекта:
```bash
touch .env
```
   

3. Добавьте в файл `.env` следующие переменные окружения:
 ```python
 BOT_TOKEN='YOUR_BOT_TOKEN'
 DB_TOKEN='YOUR_DB_TOKEN'
 REDIS_URL='redis://localhost:6379'
  ```
   * Замените `YOUR_BOT_TOKEN`, `YOUR_DB_TOKEN` на ваши реальные значения.

4. Запустите сервер Redis (на Ubuntu LTS):
```WSL
sudo service redis-server start
```

5. Проверьте, что сервер Redis работает:
```WSL
redis-cli
```


7. Запустите бота:
```bash
python main.py
```

   

### Дополнительные сведения

* Получение BOT_TOKEN: @BotFather в Telegram.
* Получение DB_TOKEN: на сайте mongodb.com

Поздравляем! Теперь Cryptan на TON запущен и готов к работе!
