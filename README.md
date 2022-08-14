# api_test_task

API, реализующее CRUD, содержит две модели - переопределенную модель User и модель Task.


![](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![](https://img.shields.io/badge/django%20rest-ff1709?style=for-the-badge&logo=django&logoColor=white)
![](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=JSON%20web%20tokens&logoColor=white)
![](https://img.shields.io/badge/Swagger-85EA2D?style=for-the-badge&logo=Swagger&logoColor=white)
![](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=Postman&logoColor=white)

## Запуск проекта

> Установите Python (если он не установлен), предпочтительно начиная с версии 3.8 <br>
> [Download Python3](https://www.python.org/downloads/release/python-3910/)

Клонируйте репозиторий:
```
git clone https://github.com/AlexanderZug/api_test_task.git
```
Перейдите в папку с проектом:
```
cd api_test_task
```
Создайте и активируйте виртуальное окружение:
```
python3 -m venv venv
```
```
source venv/bin/activate
```
Установите зависимости:
```
pip3 install -r requirements.txt
```
Выполните миграции:
```
python3 manage.py migrate
```
Запустите проект:
```
python3 manage.py runserver
```

## Документацию по API с эндпоинтами можно найти перейдя по адресу:
```
http://127.0.0.1:8000/redoc/
```
## Подергать API за "ручки" можно при помощи Swagger'a:
```
http://127.0.0.1:8000/swagger/
```

<br>

## Возможности API

Неавторизованный пользователь (доступны только GET запросы):

> GET /api/v1/user/ - возвращает список всех зарегестрированных пользователей

> GET /api/v1/tasks/ - возвращает список всех существующих задач

> GET /api/v1/tasks/{user_id}/detail_info/ - посмотреть список задач конкретного пользователя по id

Регистрация и авторизация осуществялются по JWT-токену (используются технологии Simple JWT и djoser):

> POST /api/auth/users/ - отправляются username и password (email - необязательный параметр)

> POST /api/auth/jwt/create/ - отправляются username и password в ответе приходит access и refresh токены 
(первый необходимо использовать в заголовке каждого запроса (на мой взгляд, наиболее оптимальный способ взаимодействия с API - 
через Postman используя опцию "Authorization"))

Авторизованный пользователь:

> PUT | PATCH /api/v1/user/{user_id}/ - пользователь может обновлять информацию - unsername, name - о самом себе 
(не имеет доступа к изминению информации, относящейся к другим пользователям)

> DELETE /api/v1/user/{user_id}/ - если пользователь поставит перед собой невыполнимые задачи и не сможет их выполнить,
то он имеет возможность сам себя удалить...

> POST /api/v1/tasks/ - создание новой задачи (автоматически привязывается к пользователю ее создавшему)

> PUT | PATCH /api/v1/tasks/{task_id}/ - пользователь имеет возможность редактировать свои собственные задачи 
(не имеет доступа к редактированию чужих задач)

> DELETE /api/v1/tasks/{task_id}/ - пользователь имеет возможность удалить имеющуюся задачу (не имеет полномочий удалять чужие задач)
