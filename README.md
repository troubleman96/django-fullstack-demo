# Django Full-Stack Learning Project

This project is a full-stack web application built with the Django framework. It serves as a practical example for learning and understanding the core concepts of Django and full-stack development.

## Features

*   **User Authentication:** Complete user authentication system including sign up, login, and logout functionality.
*   **User Profiles:** Each user has a profile page with their information.
*   **Project Management:** Authenticated users can create, view, update, and delete their projects.
*   **Task Management:** Within each project, users can create and manage tasks.
*   **Settings Page:** Users can manage their account settings.
*   **Static Files:** Demonstrates how to serve static files like CSS and JavaScript.
*   **Database:** Uses SQLite for the database, managed by Django's ORM.
*   **Templates:** Utilizes Django's template engine with inheritance to create reusable page layouts.
*   **Forms:** Implements Django forms for user input and validation.
*   **AJAX:** Uses AJAX for asynchronous task status updates.

## Technologies Used

*   Python
*   Django
*   SQLite
*   HTML
*   CSS
*   JavaScript

## Setup and Installation

To get this project up and running on your local machine, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd django-fullstack
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the database migrations:**
    ```bash
    python manage.py migrate
    ```

## Running the Application

To run the development server, use the following command:

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`.

## Project Structure

```
├── db.sqlite3
├── manage.py
├── requirements.txt
├── demo/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── main/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── models.py
    ├── tests.py
    ├── urls.py
    ├── views.py
    ├── migrations/
    ├── static/
    │   ├── css/
    │   └── js/
    └── templates/
        ├── about.html
        ├── base.html
        ├── home.html
        ├── login.html
        ├── profile.html
        ├── projects.html
        ├── settings.html
        └── signup.html
```

*   `demo/`: The main Django project directory.
    *   `settings.py`: Contains the project settings.
    *   `urls.py`: The main URL configuration for the project.
*   `main/`: A Django app that contains the core functionality of the application.
    *   `models.py`: Defines the database models.
    *   `views.py`: Contains the view functions and classes.
    *   `urls.py`: URL configuration for the `main` app.
    *   `forms.py`: Defines the forms used in the application.
    *   `templates/`: Contains the HTML templates.
    *   `static/`: Contains the static files (CSS and JavaScript).
*   `db.sqlite3`: The SQLite database file.
*   `manage.py`: A command-line utility for interacting with the Django project.
*   `requirements.txt`: A list of the Python dependencies.

## Learning Objectives

By studying and working with this project, you can learn about:

*   **Django Project Structure:** How to organize a Django project with multiple apps.
*   **MVT Architecture:** The Model-View-Template pattern as implemented in Django.
*   **Database Modeling:** Creating and managing database models with Django's ORM.
*   **User Authentication:** Implementing a complete user authentication system.
*   **CRUD Operations:** Building Create, Read, Update, and Delete functionality.
*   **Template Inheritance:** Creating reusable templates to avoid code duplication.
*   **Static File Management:** Serving CSS, JavaScript, and other static files.
*   **Form Handling:** Creating and validating forms for user input.
*   **URL Routing:** Configuring URLs for different pages and views.
