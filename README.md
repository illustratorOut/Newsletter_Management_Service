<H1 style="text-align: center"> 
Сервис рассылок <span style='color: red;'>New-Maling</span>
</H1>

---
<br>

В приложеннии точкой входа является [Страница авторизации](http://127.0.0.1:8000/users/login).

  <div class="wrapper">
    <div class="block">

| Описание                    | Команды                             |
|-----------------------------|-------------------------------------|
| Приминить миграции          | ```python manage.py migrate```      |
| Добавить пользователей      | ```python manage.py ccsu```         |
| Заполнить список рассылок   | ```python manage.py fill```         |
| Заполнить контент для блога | ```python manage.py content_blog``` |

</div>


<div class="img_" align="center">
  <img src="https://media.giphy.com/media/M9gbBd9nbDrOTu1Mqx/giphy.gif" width="100"/>
</div>

  </div>

---
<H3 style="text-align: center; color:#A7FC00;"> .env </H3>

 <div class="wrapper">
    <div class="block">

| Шаблон |
|--------|

```text 
CACHE_ENABLED=True
REDIS=redis://127.0.0.1:6379

POSTGRES_NAME=
POSTGRES_PASSWORD=
POSTGRES_USER= postgres
POSTGRES_HOST= localhost

YANDEX_MAIL=
MAIL_PASSWORD=
 ```

</div>
  </div>


<style>
.wrapper {
  display: flex;
  align-items: center;
}

.block {

  display: inline-block;
  margin: 2px;
}

.img_{
    padding-left : 10%
}
</style>
