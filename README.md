# DayFlow

**A simple and intuitive task management web application built with Django.**

DayFlow is a web application designed to help users organize their daily activities and manage tasks in one place. The project focuses on providing a straightforward experience for managing personal tasks, with user authentication and a PostgreSQL database.

🌐 **Live Demo:** [DayFlow](https://day-flow-eta-dusky.vercel.app/)

📂 **Repository:** [GitHub – Adil-Bikiev/DayFlow](https://github.com/Adil-Bikiev/DayFlow)

---

## Features

- **User Authentication** — User registration, login, and logout.
- **Task Management** — A dedicated interface for viewing and managing tasks.
- **Personalized Access** — Authentication-based access to the application.
- **Database Integration** — PostgreSQL database for persistent data storage.
- **Cloud Deployment** — Hosted on Vercel with Neon PostgreSQL.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| Django 6.1 | Web framework |
| PostgreSQL | Relational database |
| Neon | Cloud PostgreSQL hosting |
| HTML / CSS | Frontend development |
| JavaScript | Frontend functionality |
| Vercel | Application deployment |
| Git & GitHub | Version control |

## Project Structure

```text
DayFlow/
│
├── DayFlow/
│   ├── DayFlow/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   │
│   ├── DayFlowApp/
│   │   ├── migrations/
│   │   ├── templates/
│   │   ├── static/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── forms.py
│   │   └── urls.py
│   │
│   └── manage.py
│
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

*The structure above illustrates the main Django components; individual files may differ in the repository.*

## Getting Started

Follow these instructions to run DayFlow locally.

### 1. Clone the Repository

```bash
git clone https://github.com/Adil-Bikiev/DayFlow.git

cd DayFlow
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it:

**macOS / Linux**
```bash
source venv/bin/activate
```

**Windows**
```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the directory containing `manage.py`.

Add the following variables:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True

DATABASE_URL=postgresql://USER:PASSWORD@HOST/DATABASE?sslmode=require
```

Replace the database connection string with your own PostgreSQL connection URL.

For local development, you can use a local PostgreSQL instance or a Neon database.

**Important:** Never commit your `.env` file or expose your database credentials.

### 5. Apply Database Migrations

```bash
python manage.py migrate
```

### 6. Create an Administrator Account (Optional)

```bash
python manage.py createsuperuser
```

### 7. Run the Development Server

```bash
python manage.py runserver
```

Open your browser:

```text
http://127.0.0.1:8000/
```

## Database Configuration

DayFlow uses PostgreSQL for persistent data storage.

The project supports cloud database hosting through [Neon](https://neon.com/).

To configure Neon:

1. Create a PostgreSQL project in Neon.
2. Open the Neon dashboard.
3. Copy your PostgreSQL connection string.
4. Add it to the `DATABASE_URL` environment variable.
5. Apply Django migrations.

```bash
python manage.py migrate
```

## Deployment

DayFlow is configured for deployment on [Vercel](https://vercel.com/).

The production environment requires the following environment variables:

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | Set to `False` |
| `DATABASE_URL` | Neon PostgreSQL connection string |

Make sure to configure these variables in your Vercel project settings before deploying.

## Future Improvements

Potential improvements for future versions:

- Task deadlines and priority levels.
- Task categories and filtering.
- Improved dashboard and user experience.
- Task completion statistics.
- Responsive design improvements.

## Author

**Adil Bikiev**

Computer Science Student | Software Developer

- GitHub: [@Adil-Bikiev](https://github.com/Adil-Bikiev)

---

*Built with Python and Django.*