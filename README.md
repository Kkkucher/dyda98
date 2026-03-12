# Flask JSON Loader

Веб-приложение для загрузки JSON файлов с сохранением данных в MySQL и отображением через DataTables.

---

## Требования

- Python 3.10+
- MySQL 8.0+
- pip

---

## Развёртывание

### 1. Клонировать репозиторий

```bash
git clone https://github.com/ВАШ_ЮЗЕР/ВАШ_РЕПО.git
cd ВАШ_РЕПО
```

### 2. Создать и активировать виртуальное окружение

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

### 4. Создать базу данных MySQL

Войти в MySQL:
```bash
mysql -u root -p
```

Выполнить:
```sql
CREATE DATABASE flask_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

### 5. Настроить подключение к БД

В файле `app.py` изменить строку подключения:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ЮЗЕР:ПАРОЛЬ@localhost/flask_db'
```

Заменить `ЮЗЕР` и `ПАРОЛЬ` на свои данные MySQL.

### 6. Запустить приложение

```bash
python app.py
```

### 7. Открыть в браузере

```
http://127.0.0.1:5000
```

---

## Формат JSON файла

```json
[
  {
    "name": "строка менее 50 символов",
    "date": "2024-01-15_14:30"
  }
]
```

- `name` — строка, длина строго меньше 50 символов
- `date` — дата в формате `YYYY-MM-DD_HH:mm`
- Лишние ключи игнорируются
- При ошибке валидации данные не сохраняются, пользователь получает сообщение об ошибке

---

