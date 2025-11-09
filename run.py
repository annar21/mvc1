from app.init import create_app
from app.db import init_db

if __name__ == "__main__":
    app = create_app()
    init_db()

    app.run(debug=True)