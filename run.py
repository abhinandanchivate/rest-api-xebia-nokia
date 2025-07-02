# app runner
from app.extensions import  db
from app.container import setup_di
from app import create_app
# Create the Flask app instance
app = create_app()

# Set up Dependency Injection (binds services and repositories)
setup_di(app)

# Optional: enable Flask-Migrate if you're using Alembic
# migrate = Migrate(app, db)

# Create all tables (if not using Alembic migrations)
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9800, debug=True)
