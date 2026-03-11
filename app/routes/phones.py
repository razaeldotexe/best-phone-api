from flask import Blueprint, request, jsonify
from app.database import DeviceCache, CacheMetadata
from datetime import datetime

phones_bp = Blueprint('phones', __name__, url_prefix='/api/v1/phones')

@phones_bp.route('/ranking', methods=['GET'])
def get_ranking():
    year = request.args.get('year', datetime.now().year)
    limit = min(int(request.args.get('limit', 10)), 50)
    sort_by = request.args.get('sort_by', 'score')
    
    # Ambil semua device dari cache
    devices = DeviceCache.query.all()
    
    data_list = []
    for d in devices:
        device_data = d.data
        # Tambahkan filter tahun jika diperlukan (asumsi data memiliki field 'year')
        if year and str(device_data.get('year')) != str(year) and device_data.get('year') is not None:
             continue
        data_list.append(device_data)

    # Sorting
    if sort_by == 'score':
        data_list.sort(key=lambda x: x.get('aggregate_score', 0), reverse=True)
    elif sort_by == 'price':
        data_list.sort(key=lambda x: x.get('price', 0))
    elif sort_by == 'value':
        # Contoh rumus value: score / price
        data_list.sort(key=lambda x: x.get('aggregate_score', 0) / max(x.get('price', 1), 1), reverse=True)

    # Ambil metadata untuk last_updated
    metadata = CacheMetadata.query.first()
    last_updated = metadata.last_update.isoformat() if metadata else "N/A"

    return jsonify({
        "status": "success",
        "data": data_list[:limit],
        "last_updated": last_updated,
        "message": f"Ranking list fetched successfully ({len(data_list)} devices found)"
    })

@phones_bp.route('/device', methods=['GET'])
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
