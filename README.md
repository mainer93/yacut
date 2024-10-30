Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:mainer93/yacut.git
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Заполните файл .env:

```
FLASK_APP=yacut
FLASK_DEBUG=1
DATABASE_URI=sqlite:///db.sqlite3
SECRET_KEY=YOUR_SECRET_KEY
```

Создайте базу данных с таблицами. Для этого импортируйте созданный в приложении экземпляр базы данных db и запустите его метод create_all():

```
flask shell
>>> from opinions_app import db
>>> db.create_all()
```

Запустите проект:

```
flask run
```