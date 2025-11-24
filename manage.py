# manage.py

from app import create_app

app = create_app()  # 👈 acá van los paréntesis

if __name__ == "__main__":
    app.run()
