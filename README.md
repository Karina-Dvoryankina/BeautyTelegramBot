# 💄 EmberBeauty Telegram Bot

**EmberBeauty** — интеллектуальный Telegram-бот для автоматизации работы салона красоты.  
Он позволяет клиентам легко записываться на процедуры, узнавать информацию об услугах и мастерах, а также связываться с администрацией через удобный интерфейс Telegram.

---

## Возможности

- Просмотр списка доступных услуг
- Получение информации о мастерах
- Онлайн-запись на процедуры
- Обратная связь с администратором
- Интерактивное меню, удобная навигация
- Использование базы данных SQLite для хранения данных

---

## Технологии

- **Язык:** Python 3.x  
- **Telegram API:** [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)  
- **База данных:** SQLite (`date.db`)

---

## Использование базы данных

Бот работает с базой данных **SQLite** (📂`date.db`), которая используется для хранения информации о:

- Пользователях
- Записях на процедуры
- Выбранных услугах
- Дате и времени обращений

---

## Структура проекта

```
EmberBeauty_bot/
│
├── EmberBeauty_bot.py       # Основной код бота
├── date.db                  # SQLite база данных
└── README.md                # Документация
```
## Демонстрация работы 

### Главное меню
<img width="281" height="179" alt="image" src="https://github.com/user-attachments/assets/a94ae342-2310-4f0b-aed3-8eb3b81a0cd6" />

### Контактная информация
<img width="239" height="301" alt="image" src="https://github.com/user-attachments/assets/54232cc5-0a2a-4dd8-bb62-bb36651dce29" />

### Выбор ближайшей записи
<img width="709" height="266" alt="image" src="https://github.com/user-attachments/assets/0379574d-42fc-430c-8fb2-8bb0d9b01c3e" />

### Успешная запись на услугу
<img width="974" height="1088" alt="image" src="https://github.com/user-attachments/assets/af44214f-c477-4e21-b5b4-2b7437b1f856" />


