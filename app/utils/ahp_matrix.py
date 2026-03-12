from typing import List

def validate_pairwise_matrix(matrix: List[List[float]]) -> bool:
    """
    Kiểm tra tính hợp lệ của ma trận so sánh cặp.
    - Phải là ma trận vuông.
    - Các phần tử trên đường chéo chính bằng 1.
    - Các phần tử đối xứng qua đường chéo chính phải là nghịch đảo của nhau (a[i][j] * a[j][i] == 1).
    """
    if not matrix:
        return False
        
    n = len(matrix)
    # Kiểm tra ma trận có vuông hay không
    for row in matrix:
        if len(row) != n:
            return False
            
    # Kiểm tra các tính chất của phân tử
    for i in range(n):
        for j in range(n):
            if i == j:
                # Đường chéo chính phải bằng 1
                if abs(matrix[i][j] - 1.0) > 1e-6:
                    return False
            else:
                # Các phần tử phải dương
                if matrix[i][j] <= 0:
                    return False
                # Tính chất đối xứng nghịch đảo
                if abs(matrix[i][j] * matrix[j][i] - 1.0) > 1e-6:
                    return False
                    
    return True

def sum_columns(matrix: List[List[float]]) -> List[float]:
    """
    Tính tổng các phần tử trên từng cột của ma trận.
    """
    if not matrix:
        return []
        
    n = len(matrix)
    col_sums = [0.0] * n
    
    for j in range(n):
        for i in range(n):
            col_sums[j] += matrix[i][j]
            
    return col_sums

def normalize_matrix(matrix: List[List[float]]) -> List[List[float]]:
    """
    Chuẩn hóa ma trận bằng cách chia mỗi phần tử cho tổng của cột tương ứng.
    """
    col_sums = sum_columns(matrix)
    n = len(matrix)
    
    # Khởi tạo ma trận chuẩn hóa với các giá trị 0
    normalized = [[0.0 for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            if col_sums[j] == 0:
                raise ValueError("Lỗi chia cho 0: Tổng của một cột trong ma trận bằng 0.")
            normalized[i][j] = matrix[i][j] / col_sums[j]
            
    return normalized
