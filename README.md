# Library Management System

LMS - бекенд онлайн-системи для керування бібліотекою.

## Можливості

- Реєстрація в системі для подальшого користування її функціоналом
- Перегляд каталогу книжок
- Редагування каталогу книжок (тільки для адміністратора)
- Внесення інформації про взяття книжки та її повернення

## Технічний стек
- Python
- Flask
- Postgresql
- MongoDB
- Redis
- RabbitMQ
- Docker-compose
- GitHub Actions (в якості демонстрації роботи CI. Реалізована одна job "Build", з окремим step-oм для білду кожного сервісу)

## Локальний запуск
Запустити всі сервіси можна разом
```sh
docker-compose up --build
```
Або кожен окремо
```sh
docker-compose up api_gateway --build
docker-compose up users --build
docker-compose up books --build
docker-compose up rental --build
```

## Архітектура системи
Проект складаеться з чотирьох мікросервісів, що виконують такі функції:
* api_gateway - RESTful API для фронтенду
* users - авторизація (видача токену) та зберігання даних користувачів
* books - перегляд та редагування каталогу книжок
* rental - контроль прокату книжок (внесення відомостей про взяття та поверненя книг)
<img width="648" alt="image" src="https://github.com/vyaroshchuk/lms/assets/3406545/7d67bfbc-3e02-43da-82e1-05b11c687d40">

Мікросервіси rental i users працюють з Postgres базами даних.
Books працює з MongoDB replica set із трьох нод.

Всі мікросервіси взаємодіють між собою за допомогою http-запитів, але в проекті представлені і інші способи взаємодії між мікросервісами:
* Redis: використовуєтсья для зберігання авторизаційних токенів користувачів.
* RabbitMQ: використовується для створення запитів на взяття та повернення книг.

## Приклади використання
### Приклад №1
Реєстрація користувача
```sh
$ curl -w '\n' -X POST http://0.0.0.0:8000/sign_up/test_user/test_pwd 

Successfully signed up user: test_user
```
Авторизація
```sh
$ curl -w '\n' -X POST http://0.0.0.0:8000/sign_in/test_user/test_pwd

e6a07ad7-6995-498c-a108-8b9d3eed3a3b
```
Перегляд каталогу книжок
```sh
$ curl -w '\n' -X GET http://0.0.0.0:8000/books --header 'Authorization: e6a07ad7-6995-498c-a108-8b9d3eed3a3b' 
[
  {
    "genre": "Fiction",
    "id": "664a356e72fa16f965cac8f6",
    "title": "To Kill a Mockingbird"
  },
  {
    "genre": "Dystopian",
    "id": "664a356e72fa16f965cac8f7",
    "title": "1984"
  },
  {
    "genre": "Romance",
    "id": "664a356e72fa16f965cac8f8",
    "title": "Pride and Prejudice"
  },
  {
    "genre": "Fiction",
    "id": "664a356e72fa16f965cac8f9",
    "title": "The Great Gatsby"
  },
  {
    "genre": "Adventure",
    "id": "664a356e72fa16f965cac8fa",
    "title": "Moby-Dick"
  },
  {
    "genre": "Historical",
    "id": "664a356e72fa16f965cac8fb",
    "title": "War and Peace"
  },
  {
    "genre": "Fiction",
    "id": "664a356e72fa16f965cac8fc",
    "title": "The Catcher in the Rye"
  },
  {
    "genre": "Fantasy",
    "id": "664a356e72fa16f965cac8fd",
    "title": "The Hobbit"
  },
  {
    "genre": "Dystopian",
    "id": "664a356e72fa16f965cac8fe",
    "title": "Brave New World"
  },
  {
    "genre": "Epic",
    "id": "664a356e72fa16f965cac8ff",
    "title": "The Odyssey"
  }
]
```

Перегляд детальної інформації про книгу
```sh
$ curl -w '\n' -X GET http://0.0.0.0:8000/book/664a356e72fa16f965cac8ff --header 'Authorization: e6a07ad7-6995-498c-a108-8b9d3eed3a3b' 

{
  "author": "Homer",
  "genre": "Epic",
  "id": "664a356e72fa16f965cac8ff",
  "title": "The Odyssey",
  "year": -800
}
```

Перевірка прокатного статусу книги
```sh
$ curl -w '\n' -X GET http://0.0.0.0:8000/rental/status/664a356e72fa16f965cac8ff --header 'Authorization: e6a07ad7-6995-498c-a108-8b9d3eed3a3b' 

{
  "available": true,
  "retrieved_date": "Mon, 20 May 2024 19:22:53 GMT"
}
```
Книга доступна

Взяття книги в прокат
```sh
$ curl -w '\n' -X POST http://0.0.0.0:8000/rental/borrow/664a356e72fa16f965cac8ff --header 'Authorization: e6a07ad7-6995-498c-a108-8b9d3eed3a3b'

Borrow request created
```
Перевірімо чи змінився прокатний статус книги
```sh
$ curl -w '\n' -X GET http://0.0.0.0:8000/rental/status/664a356e72fa16f965cac8ff --header 'Authorization: e6a07ad7-6995-498c-a108-8b9d3eed3a3b'
{
  "available": false,
  "borrowed_date": "Mon, 20 May 2024 21:04:41 GMT"
}
```
Бачиимо, що тепер книга недоступна

Повернення книги
```sh
$ curl -w '\n' -X POST http://0.0.0.0:8000/rental/retrieve/664a356e72fa16f965cac8ff --header 'Authorization: e6a07ad7-6995-498c-a108-8b9d3eed3a3b'     

Retrieve request created
```
Знову перевіряємо статус
```sh
$ curl -w '\n' -X GET http://0.0.0.0:8000/rental/status/664a356e72fa16f965cac8ff --header 'Authorization: e6a07ad7-6995-498c-a108-8b9d3eed3a3b'        
{
  "available": true,
  "retrieved_date": "Mon, 20 May 2024 21:08:19 GMT"
}
```
Книга знову доступна

Знищення токену
```sh
$ curl -w '\n' -X POST http://0.0.0.0:8000/sign_out/e6a07ad7-6995-498c-a108-8b9d3eed3a3b

Success
```
Якщо робити запити без токену, або з не дійсним токеном - API буде повертати 401
```sh
$ curl -I -w '\n' -X GET http://0.0.0.0:8000/books                                                               
HTTP/1.1 401 UNAUTHORIZED

$ curl -I -w '\n' -X GET http://0.0.0.0:8000/books --header 'Authorization: e6a07ad7-6995-498c-a108-8b9d3eed3a3b'                      
HTTP/1.1 401 UNAUTHORIZED
```

### Приклад №2
Авторизація адміністратора
```sh
$ curl -w '\n' -X POST http://0.0.0.0:8000/sign_in/admin/admin                                                                        

dee1e752-4650-4136-90f6-8e2ffa6a42f5
```
Додавання книги до каталогу
```sh
$ curl -w '\n' -X POST http://0.0.0.0:8000/book/add -d '{"title":"1","genre":"2","author":"3"}' --header "Content-Type: application/json" --header "Authorization: dee1e752-4650-4136-90f6-8e2ffa6a42f5" 

664bbd94a3abf01a2d8e8230
```

Перевіримо наявність такої книги в каталозі
```sh
$ curl -w '\n' -X GET http://0.0.0.0:8000/book/664bbd94a3abf01a2d8e8230 --header 'Authorization: dee1e752-4650-4136-90f6-8e2ffa6a42f5' 
{
  "author": "3",
  "genre": "2",
  "id": "664bbd94a3abf01a2d8e8230",
  "title": "1"
}
```

Видалення книги
```sh
$ curl -w '\n' -X POST http://0.0.0.0:8000/book/delete/664bbd94a3abf01a2d8e8230 --header "Authorization: dee1e752-4650-4136-90f6-8e2ffa6a42f5"
Book deleted
```

Спробуємо знову переглянути інформацію про видалену книгу
```sh
$ curl -w '\n' -X GET http://0.0.0.0:8000/book/664bbd94a3abf01a2d8e8230 --header 'Authorization: dee1e752-4650-4136-90f6-8e2ffa6a42f5'
Book not found
```
