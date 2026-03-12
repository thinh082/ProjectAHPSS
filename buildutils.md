# Hướng dẫn xây dựng module tính AHP cho dự án FastAPI

## 1. Mục tiêu

Xây dựng các module trong thư mục `utils/` để thực hiện tính toán **AHP (Analytic Hierarchy Process)** cho hệ thống hỗ trợ ra quyết định.

Module phải:

* Tính **trọng số từ ma trận so sánh cặp**
* Kiểm tra **độ nhất quán (CI, CR)**
* Chuẩn hóa ma trận
* Tổng hợp điểm phương án
* Hoạt động độc lập với database
* Có thể được gọi từ `service` hoặc `API layer`

Công thức AHP phải đúng chuẩn theo phương pháp **Saaty**.

---

# 2. Cấu trúc thư mục

AI Agent cần tạo thư mục:

```
app/
 ├─ utils/
 │   ├─ ahp_matrix.py
 │   ├─ ahp_weight.py
 │   ├─ ahp_consistency.py
 │   ├─ ahp_aggregate.py
 │   └─ ahp_utils.py
```

Mỗi file đảm nhiệm một nhiệm vụ riêng.

---

# 3. Nguyên lý AHP cần implement

AHP hoạt động theo quy trình:

1. Tạo **ma trận so sánh cặp**
2. Chuẩn hóa ma trận
3. Tính **vector trọng số (priority vector)**
4. Kiểm tra **Consistency Ratio**
5. Nếu CR < 0.1 → ma trận hợp lệ
6. Tổng hợp điểm phương án

---

# 4. File ahp_matrix.py

Chứa các hàm xử lý ma trận cơ bản.

### Chức năng

* Kiểm tra ma trận hợp lệ
* Tạo ma trận nghịch đảo
* Chuẩn hóa ma trận

### Hàm cần có

```
validate_pairwise_matrix(matrix)

normalize_matrix(matrix)

sum_columns(matrix)
```

### Yêu cầu

* input: `List[List[float]]`
* output: ma trận chuẩn hóa

Chuẩn hóa theo công thức:

```
normalized_value = value / column_sum
```

---

# 5. File ahp_weight.py

Chứa logic tính **trọng số tiêu chí**.

### Phương pháp

Tính **priority vector** bằng cách:

1. Chuẩn hóa ma trận
2. Tính trung bình mỗi dòng

### Hàm cần có

```
calculate_priority_vector(matrix)
```

### Công thức

```
weight_i = average(row_i)
```

---

# 6. File ahp_consistency.py

Chứa logic kiểm tra **độ nhất quán của ma trận**.

### Cần tính

* λmax
* CI
* CR

### Công thức

#### λmax

```
λmax = average( (Aw)i / wi )
```

#### CI

```
CI = (λmax - n) / (n - 1)
```

#### CR

```
CR = CI / RI
```

### Bảng Random Index

```
RI_TABLE = {
    1:0.0,
    2:0.0,
    3:0.58,
    4:0.90,
    5:1.12,
    6:1.24,
    7:1.32,
    8:1.41,
    9:1.45,
    10:1.49
}
```

### Hàm cần có

```
calculate_lambda_max(matrix, weights)

calculate_consistency_index(lambda_max, n)

calculate_consistency_ratio(ci, n)
```

---

# 7. File ahp_aggregate.py

Dùng để **tổng hợp điểm phương án**.

### Input

* ma trận điểm của phương án theo từng tiêu chí
* vector trọng số tiêu chí

### Công thức

```
score = Σ(weight_i * value_i)
```

### Hàm cần có

```
aggregate_scores(criteria_weights, alternative_scores)
```

Output:

```
{
    "alternative": score
}
```

---

# 8. File ahp_utils.py

File orchestration.

Dùng để gọi toàn bộ pipeline AHP.

### Hàm chính

```
run_ahp(pairwise_matrix)
```

Trả về:

```
{
   "weights": [],
   "lambda_max": float,
   "CI": float,
   "CR": float,
   "is_consistent": true/false
}
```

---

# 9. Quy ước code

AI Agent cần tuân thủ:

* Python 3.10+
* type hint đầy đủ
* code tách nhỏ hàm
* không phụ thuộc FastAPI

Ví dụ:

```
def normalize_matrix(matrix: List[List[float]]) -> List[List[float]]:
```

---

# 10. Ví dụ input

```
matrix = [
 [1,3,5],
 [1/3,1,2],
 [1/5,1/2,1]
]
```

---

# 11. Ví dụ output

```
{
 "weights": [0.63,0.26,0.11],
 "lambda_max":3.02,
 "CI":0.01,
 "CR":0.02,
 "is_consistent":true
}
```

---

# 12. Yêu cầu quan trọng

AI Agent phải đảm bảo:

* code dễ đọc
* không hardcode dữ liệu
* có thể reuse cho nhiều tiêu chí
* xử lý lỗi ma trận không vuông
* xử lý chia cho 0

---

# 13. Mục tiêu cuối cùng

Các module trong `utils` phải cho phép hệ thống:

```
DB → AHP → AI → Decision Engine
```

Trong đó:

* **DB chỉ lưu dữ liệu thô**
* **AHP tính trọng số**
* **AI dự đoán**
* **Decision Engine tổng hợp**

Module này chỉ đảm nhiệm **AHP calculation layer**.
