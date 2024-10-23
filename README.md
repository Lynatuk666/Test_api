## Данное приложение написано в рамках тестового задания 

### Rest API сервис, отвечающий на:
* get запросы по адресу `/api/v1/wallets/{WALLET_UUID}`
* post запросы по адресу `api/v1/wallets/{WALLET_UUID}/operation` c телом запроса -
```
{
operationType: DEPOSIT or WITHDRAW,
amount: 1000
}
```

<p>Для запуска программы необходимо:
- установить зависимости из requirements.txt
- запустить код в файле main.py
</p>

<p>на эндпоинты написаны тесты, для проверки основных возможных ситуаций
</p>
<p>основные функции асинхронны, для улучшения производительности
</p>



