
<h1>Порядок установки</h1>
0) Создать таблицу в postgres DRF_AUTH_DB 
1) Клонировать репозитрорий 
2)pip install -r requirements.txt 
2.5)cd DRFAuth
4)python manage.py migrate (создает таблицы и наполняет их данными )
5)python manage.py runserver 
<h1>Правила доступа </h1> 


|         | Управление пользователями                      | Товары магазина                                | Заказы                                                                   | Магазины                                       | Управление правилами доступа                   |
|---------|------------------------------------------------|------------------------------------------------|--------------------------------------------------------------------------|------------------------------------------------|------------------------------------------------|
| admin   | read_all<br>create<br>update_all<br>delete_all | read_all<br>create<br>update_all<br>delete_all | read_all<br>create<br>update_all<br>delete_all                           | read_all<br>create<br>update_all<br>delete_all | read_all<br>create<br>update_all<br>delete_all |
| manager | read_all<br>update_all                         | read_all<br>create<br>update_all<br>delete_all | read<br>read_all<br>update_all<br>delete_all (может удалить любой заказ) | read_all<br>create                             | NA                                             |
| user    | read<br>update (свои данные)<br>delete         | read_all                                       | read<br>create(создать заказ)<br>update                                  | read                                           | NA                                             |
| guest   | NA                                             | read_all                                       | NA                                                                       | NA                                             | NA                                             |