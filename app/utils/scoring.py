def normalize_score(score, max_score=100):
    """Normalize score to 0-100 scale."""
    if score is None: return 0
    return (float(score) / max_score) * 100

def calculate_aggregate_score(scores):
    """
    Calculate weighted aggregate score.
    Weights: 
    AnTuTu 25%, Geekbench 20%, DXOMARK 20%, 3DMark 15%, Nanoreview 10%, Kimovil 10%
    """
    weights = {
        'antutu': 0.25,
        'geekbench': 0.20,
        'dxomark': 0.20,
        'd3dmark': 0.15,
        'nanoreview': 0.10,
        'kimovil': 0.10
    }
    
    total_score = 0
    total_weight = 0
    
    for key, weight in weights.items():
        score = scores.get(key)
        if score is not None:
            # Assuming incoming scores are already normalized to 100 or specific scales
            # For simplicity, we assume they are already normalized here or handled per source
            total_score += float(score) * weight
            total_weight += weight
            
    if total_weight == 0: return 0
    return round(total_score / total_weight, 2)
