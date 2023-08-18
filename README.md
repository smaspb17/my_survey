# My survey
**ОПИСАНИЕ:**

My survey - это простой учебный Pet-проект, в рамках изучения Django REST framework (DRF). В проекте реализован опрос анонимных пользователей - введение ответов на вопросы, их сохранения в БД и получения результатов, с системой аутентификации пользователя по ID. Проект выполнен по техническому заданию (ниже по тексту), найденному мной в сети Интернет. Проект разрабатан с использованием DRF для реализации REST API, включает в себя компоненты, необходимые для предоставления API-сервисов, такие как маршрутизация URL, сериализаторы, модели, представления, аутентификация, управление доступом, обеспечивает поддержку формата передачи данных JSON. Для использования Версия Python должна быть не ниже 3.6.

**СТЕК ТЕХНОЛОГИЙ:**
Python 3, Django Rest Framework 3.14, SQLite3, drf-spectacular, swagger  

**ЛОКАЛЬНАЯ УСТАНОВКА (для Windows):**

1. Клонировать проект на свой компьютер:
```
git clone git@github.com:smaspb17/my_survey.git
```
2. Перейти в директорию my_survey:
```
cd my_survey/
```
3. Создать виртуальное окружение для проекта. Это позволит изолировать проект от системных зависимостей и установленных библиотек. Для создания виртуального окружения используется команда:
```
python -m venv venv
```
4. Активировать виртуальное окружение командой:
```
source venv/Scripts/activate
```

5. Установить необходимые пакеты и зависимости проекта через менеджер пакетов `pip` и `requirements.txt` файл. Он должен содержать в себе список всех зависимостей, необходимых для работы проекта:
```
pip install -r requirements.txt
```
6. При необходимости обновить пакетный менеджер pip:
``` 
python.exe -m pip install --upgrade pip
```
7. Перейти в директорию surveys, там находится файл manage.py:
```
cd my_survey/surveys
```
8. Запустить проект на локальном сервере:
```
python manage.py runserver
```
9. Перейти по ссылке в браузере, для использования swagger:
```
http://127.0.0.1:8000/api/
``` 

**АВТОР:** Шайбаков Марат


**ЛИЦЕНЗИЯ:** Apache License 2.0


**КОНТАКТЫ:** smaspb17@yandex.ru


## ТЕХНИЧЕСКОЕ ЗАДАНИЕ, ПО КОТОРОМУ ВЫПОЛНЕН ПРОЕКТ:

Задание
Тестовое задание – дополнительный способ для нас убедиться в вашей квалификации и понять, какого рода задачи вы выполняете эффективнее всего.

Расчётное время на выполнение тестового задания: 3-4 часа, время засекается нестрого. Приступить к выполнению тестового задания можно в любое удобное для вас время.

У текущего тестового задания есть только общее описание требований, конкретные детали реализации остаются на усмотрение разработчика.

Задача: спроектировать и разработать API для системы опросов пользователей.

### Функционал для администратора системы:

* авторизация в системе (регистрация не нужна)
* добавление/изменение/удаление опросов. Атрибуты опроса: название, дата старта, дата окончания, описание. После создания поле "дата старта" у опроса менять нельзя.
* добавление/изменение/удаление вопросов в опросе. Атрибуты вопросов: текст вопроса, тип вопроса (ответ текстом, ответ с выбором одного варианта, ответ с выбором нескольких вариантов)
### Функционал для пользователей системы:

* получение списка активных опросов
* прохождение опроса: опросы можно проходить анонимно, в качестве идентификатора пользователя в API передаётся числовой ID, по которому сохраняются ответы пользователя на вопросы; один пользователь может участвовать в любом количестве опросов
* получение пройденных пользователем опросов с детализацией по ответам (что выбрано) по ID уникальному пользователя
Использовать следующие технологии: Django, Django REST framework.

Результат выполнения задачи: - исходный код приложения в github (только на github, публичный репозиторий) - инструкция по разворачиванию приложения (в docker или локально) - документация по API
