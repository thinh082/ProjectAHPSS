from typing import List, Dict

def aggregate_scores(criteria_weights: List[float], alternative_scores: Dict[str, List[float]]) -> Dict[str, float]:
    """
    Tổng hợp điểm của các phương án (alternatives) dựa trên vector trọng số của từng tiêu chí.
    
    - criteria_weights: Vector trọng số của các tiêu chí [w1, w2, ..., wn].
    - alternative_scores: Một dictionary lưu danh sách điểm của từng phương án đối với mỗi tiêu chí
                          (Ví dụ: { "PhuongAnA": [v1, v2, ..., vn] }).
                          
    Trả về: Dictionary chứa tổng điểm cho mỗi phương án ({ "PhuongAnA": tong_diem }).
    """
    final_scores = {}
    
    for alt_name, scores in alternative_scores.items():
        if len(scores) != len(criteria_weights):
            raise ValueError(f"Số lượng điểm tiêu chí của phương án '{alt_name}' không khớp với số lượng trọng số.")
            
        # Tính tổng điểm bằng cách nhân có trọng số
        total_score = sum(w * s for w, s in zip(criteria_weights, scores))
        final_scores[alt_name] = total_score
        
    return final_scores
