
<h1>Порядок установки</h1>
<h2>С Docker:</h2>
 git clone https://github.com/konmaxim/DRF_Auth.git
 <br>
 cd DRF_Auth
 <br>
docker-compose up --build
<br>
Доступен на: <a href="http://localhost:8000">http://localhost:8000 </a>

<h2>Из Python </h2>
0) Создать таблицу в postgres DRF_AUTH_DB 
<br>
1) Клонировать репозитрорий 
<br>
2)pip install -r requirements.txt 
<br>
2.5)cd DRFAuth
<br>
4)python manage.py migrate (создает таблицы и наполняет их данными )
<br>
5)python manage.py runserver 
<br>
<h1>Правила доступа </h1> 


|         | Управление пользователями                      | Товары магазина                                | Заказы                                                                   | Магазины                                       | Управление правилами доступа                   |
|---------|------------------------------------------------|------------------------------------------------|--------------------------------------------------------------------------|------------------------------------------------|------------------------------------------------|
| admin   | read_all<br>create<br>update_all<br>delete_all | read_all<br>create<br>update_all<br>delete_all | read_all<br>create<br>update_all<br>delete_all                           | read_all<br>create<br>update_all<br>delete_all | read_all<br>create<br>update_all<br>delete_all |
| manager | read_all<br>update_all                         | read_all<br>create<br>update_all<br>delete_all | read<br>read_all<br>update_all<br>delete_all (может удалить любой заказ) | read_all<br>create                             | NA                                             |
| user    | read<br>update (свои данные)<br>delete         | read_all                                       | read<br>create(создать заказ)<br>update                                  | read                                           | NA                                             |
| guest   | NA                                             | read_all                                       | NA                                                                       | NA                                             | NA                                             |