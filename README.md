## APIwork

- Установить и активировать виртуальное окружение

```bash
source /venv/Scripts/activated
```

- Установить зависимости из файла requirements.txt

```bash
python -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```

- Выполнить миграции:

```bash
python manage.py migrate
```

- В папке с файлом manage.py выполнить команду:
```bash
python manage.py runserver
```

### Примеры запросов к API:

Регистрация (POST)
```
http://127.0.0.1:8000/api/users/

 {
    "email": "",
    "username": "",
    "first_name": "",
    "last_name": "",
    "password": ""
}
```
Далее на почту прийдет письмо с подтверждением , необходимо будет перейти по ссылке в письме, после чего получить токен

Получение токена (POST)
```
http://127.0.0.1:8000/api/users/

 {
    "email": "",
    "password": ""
}
```
После чего токен нужно всегда передавать токен в заголовках 

Получение списка всех компонентов (POST)  
```
http://127.0.0.1:8000/api/v1/component/

 {
    {
        "title_categories": "",
        "category": "",
        "parametrs": {
            "сontent": ,
            "humidity": ,
            "contentmass": ,
            "heatmass": 
        }
    }
}
```
Для получение списка всех компонентов по полю title_categories необходимо делать запрос на http://127.0.0.1:8000/api/v1/component/?search=test , будет происходить поиск по всех компонентам и искать у них в title_categories нахождение подстроки "test"

Чтобы выйти необходимо сделать POST запрос на http://127.0.0.1:8000/api/token/logout/ 

