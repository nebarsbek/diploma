# Pizza Delivery Service 🍕

A full-fledged web application for a pizza delivery service. The project includes a client side (website), an admin panel, and a powerful backend API.

## ✨ Key Features

### 👤 For Users:
*   **Registration and Authorization:**
    *   Registration with email confirmation (bot protection).
    *   Login (JWT authorization).
    *   Password recovery via email.
    *   Change password in the profile.
*   **Menu and Orders:**
    *   View menu with filtering by categories (Pizza, Drinks, Desserts).
    *   Add items to the cart.
    *   Checkout with delivery address.
*   **Profile:**
    *   View order history.
    *   Track current order status.

### 🛡️ For Admins and Employees:
*   **Product Management:** Add, edit, and delete menu items (photo, description, price).
*   **Order Management:** View all orders and change their status (Pending -> Processing -> Delivered -> Cancelled).
*   **Staff Management:** Ability to create accounts for new employees.

---

## 🛠️ Tech Stack

*   **Backend:** Python 3.12, FastAPI, SQLAlchemy (Async), PostgreSQL, Pydantic, Docker.
*   **Frontend:** React, TypeScript, Vite, Tailwind CSS, Axios.
*   **Infrastructure:** Docker Compose, Nginx.

---

## 🚀 How to Run the Project (Step-by-Step Guide)

Even if you have never run projects from GitHub, follow these instructions and you will succeed.

### Step 1: Install Necessary Software

Before starting, make sure you have installed:
1.  **Git** — to download the project. [Download Git](https://git-scm.com/downloads).
2.  **Docker Desktop** — to run the project in isolated containers (this is the easiest way). [Download Docker](https://www.docker.com/products/docker-desktop/).
    *   *After installing Docker Desktop, make sure to launch it.*

### Step 2: Download the Project

1.  Open a terminal (PowerShell, Command Prompt, or Terminal).
2.  Navigate to the folder where you want to save the project and run the command:
    ```bash
    git clone <link-to-your-repository>
    cd diploma
    ```

### Step 3: Configure Environment Variables (.env)

The project needs secret settings (database passwords, email settings).

1.  Go to the `backend` folder.
2.  Create a file named `.env` there (no name, just `.env`).
3.  Open it in any text editor (Notepad, VS Code) and paste the following content:

```env
# Database settings (can be left as is for Docker)
POSTGRES_USER=admin
POSTGRES_PASSWORD=password
POSTGRES_DB=project_db
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Secret key for tokens (come up with any complex random string)
JWT_SECRET_KEY=super_secret_random_string_change_me
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60

# Email settings (Gmail)
# IMPORTANT: For Gmail, you need to use an "App Password", not your regular password.
# Instruction: Google Account -> Security -> 2-Step Verification -> App passwords.
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_16_digit_app_password
MAIL_FROM=no-reply@pizza-delivery.com
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com
MAIL_STARTTLS=True
MAIL_SSL_TLS=False
```

> **Важно:** Без настройки `MAIL_USERNAME` и `MAIL_PASSWORD` регистрация работать не будет, так как система не сможет отправить письмо с подтверждением.

### Шаг 4: Запуск

1.  Вернитесь в корневую папку проекта (`diploma2026`), где лежит файл `docker-compose.yml`.
2.  В терминале выполните команду:
    ```bash
    docker-compose up --build
    ```
3.  Дождитесь окончания сборки. В первый раз это может занять несколько минут.
4.  Когда в консоли перестанут бежать строки и появится сообщение `Application started`, проект готов!

---

## 🌐 Доступ к приложению

После запуска откройте браузер:

*   **Сайт (Frontend):** http://localhost:5173
*   **Документация API (Swagger):** http://localhost:8000/docs
    *   Здесь можно тестировать бэкенд напрямую.

---

## 💡 Полезные команды

*   **Остановить проект:** Нажмите `Ctrl + C` в терминале, где запущен Docker.
*   **Удалить контейнеры (очистить все):**
    ```bash
    docker-compose down
    ```
*   **Пересобрать проект (если изменили код):**
    ```bash
    docker-compose up --build
    ```

---

## 🔑 Учетные записи

При первом запуске база данных пуста.

1.  **Создание Админа:**
    *   Первый зарегистрированный пользователь автоматически получает роль **Admin**.
    *   Зарегистрируйтесь на сайте через форму регистрации.
    *   Подтвердите почту (перейдите по ссылке из письма).
2.  **Создание Клиентов:**
    *   Все последующие регистрации будут создавать пользователей с ролью **Customer**.
3.  **Создание Сотрудников:**
    *   Администратор может создавать сотрудников (Employee) через Админ-панель.