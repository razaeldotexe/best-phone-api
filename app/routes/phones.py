from flask import Blueprint, request, jsonify
from app.auth import require_api_key
from app.database import DeviceCache, CacheMetadata
from datetime import datetime

phones_bp = Blueprint('phones', __name__, url_prefix='/api/v1/phones')

@phones_bp.route('/ranking', methods=['GET'])
@require_api_key
def get_ranking():
    year = request.args.get('year', datetime.now().year)
    limit = min(int(request.args.get('limit', 10)), 50)
    sort_by = request.args.get('sort_by', 'score')
    
    # Logic to fetch from DeviceCache and sort
    # For now, return empty or mock
    return jsonify({
        "status": "success",
        "data": [],
        "message": "Ranking list fetched successfully"
    })

@phones_bp.route('/device', methods=['GET'])
@require_api_key
def get_device():
    name = request.args.get('name')
    if not name:
        return jsonify({"status": "error", "message": "Query param 'name' is required"}), 400
        
    device = DeviceCache.query.filter_by(name=name).first()
    if not device:
        return jsonify({"status": "error", "message": "Device not found in cache"}), 404
        
    return jsonify({
        "status": "success",
        "data": device.data,
        "message": "Device details fetched successfully"
    })
