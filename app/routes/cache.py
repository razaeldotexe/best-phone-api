from flask import Blueprint, jsonify
from app.auth import require_api_key
from app.database import CacheMetadata, db
from datetime import datetime, timedelta
from config import Config

cache_bp = Blueprint('cache', __name__, url_prefix='/api/v1/cache')

@cache_bp.route('/status', methods=['GET'])
@require_api_key
def get_cache_status():
    metadata = CacheMetadata.query.first()
    if not metadata:
        return jsonify({
            "status": "success",
            "data": {
                "device_count": 0,
                "last_update": None,
                "expires_at": None,
                "is_expired": True
            }
        })
    
    expires_at = metadata.last_update + timedelta(hours=Config.CACHE_EXPIRY_HOURS)
    is_expired = datetime.utcnow() > expires_at
    
    return jsonify({
        "status": "success",
        "data": {
            "device_count": metadata.device_count,
            "last_update": metadata.last_update.isoformat(),
            "expires_at": expires_at.isoformat(),
            "is_expired": is_expired
        }
    })

@cache_bp.route('/refresh', methods=['POST'])
@require_api_key
def refresh_cache():
    from flask import current_app
    import threading
    
    # Run in background to not block response
    thread = threading.Thread(target=current_app.scraper_manager.run_refresh)
    thread.start()
    
    return jsonify({
        "status": "success",
        "data": None,
        "message": "Cache refresh triggered"
    }), 202
