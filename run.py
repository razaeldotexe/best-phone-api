from flask import Flask
from config import Config
from app.database import init_db
from app.routes.phones import phones_bp
from app.routes.cache import cache_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    init_db(app)
    
    from app.utils.scraper_manager import ScraperManager
    scraper_manager = ScraperManager(app)
    scraper_manager.schedule_auto_refresh()
    
    # Store manager in app for manual trigger
    app.scraper_manager = scraper_manager
    
    app.register_blueprint(phones_bp)
    app.register_blueprint(cache_bp)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
