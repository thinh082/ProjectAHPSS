# SPEC API AHP – FastAPI (Dành cho AI Agent)

## 1. Mục tiêu

Xây dựng các **API endpoint trong dự án FastAPI** để thực hiện tính toán **AHP (Analytic Hierarchy Process)** và **trực quan hóa từng bước tính toán** trên website.

Yêu cầu từ giảng viên:

Người dùng phải có thể **bấm từng bước** để xem quá trình tính toán:

1. Nhập ma trận so sánh cặp
2. Tính **tổng cột**
3. Chuẩn hóa ma trận
4. Tính **trọng số (priority vector)**
5. Tính **λmax, CI, CR**
6. Xếp hạng phương án

Frontend sẽ gọi API **từng bước một** để hiển thị kết quả trung gian.

---

# 2. Tổng số endpoint cần xây dựng

Sau khi gộp bước **validate ma trận** vào bước **tính tổng cột**, hệ thống cần **5 endpoint**.

```
POST /ahp/step/column-sum
POST /ahp/step/normalize
POST /ahp/step/weights
POST /ahp/step/consistency
POST /ahp/rank
```

---

# 3. Cấu trúc project FastAPI

AI Agent cần tổ chức project như sau:

```
app/
 ├─ main.py
 ├─ routers/
 │   └─ ahp_router.py
 │
 ├─ schemas/
 │   └─ ahp_schema.py
 │
 ├─ services/
 │   └─ ahp_service.py
 │
 └─ utils/
     ├─ ahp_matrix.py
     ├─ ahp_weight.py
     ├─ ahp_consistency.py
     ├─ ahp_aggregate.py
     └─ ahp_utils.py
```

Quy tắc:

* `router` → định nghĩa endpoint
* `service` → business logic
* `utils` → thuật toán AHP

---

# 4. Endpoint 1 — Tính tổng cột + Validate ma trận

```
POST /ahp/step/column-sum
```

### Chức năng

* Validate ma trận
* Kiểm tra ma trận vuông
* Kiểm tra giá trị > 0
* Tính tổng các cột

### Input

```json
{
 "matrix":[
  [1,3,5],
  [0.333,1,2],
  [0.2,0.5,1]
 ]
}
```

### Output

```json
{
 "column_sums":[1.533,4.5,8]
}
```

### Validate rules

* Ma trận phải vuông `n x n`
* Giá trị > 0
* `matrix[i][j] ≈ 1 / matrix[j][i]`

---

# 5. Endpoint 2 — Chuẩn hóa ma trận

```
POST /ahp/step/normalize
```

### Input

```json
{
 "matrix":[...],
 "column_sums":[...]
}
```

### Công thức

```
normalized_value = value / column_sum
```

### Output

```json
{
 "normalized_matrix":[
   [0.65,0.66,0.62],
   [0.21,0.22,0.25],
   [0.14,0.11,0.13]
 ]
}
```

Frontend sẽ hiển thị **bảng normalized matrix**.

---

# 6. Endpoint 3 — Tính trọng số

```
POST /ahp/step/weights
```

### Mục tiêu

Tính **priority vector**.

### Công thức

```
weight_i = average(row_i)
```

### Input

```json
{
 "normalized_matrix":[...]
}
```

### Output

```json
{
 "weights":[0.63,0.26,0.11]
}
```

---

# 7. Endpoint 4 — Kiểm tra Consistency

```
POST /ahp/step/consistency
```

### Cần tính

* λmax
* CI
* CR

### Công thức

#### λmax

```
λmax = average((Aw)i / wi)
```

#### CI

```
CI = (λmax - n) / (n - 1)
```

#### CR

```
CR = CI / RI
```

### Random Index

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

### Input

```json
{
 "matrix":[...],
 "weights":[...]
}
```

### Output

```json
{
 "lambda_max":3.02,
 "CI":0.01,
 "CR":0.02,
 "is_consistent":true
}
```

---

# 8. Endpoint 5 — Xếp hạng phương án

```
POST /ahp/rank
```

### Input

```json
{
 "criteria_weights":[...],
 "alternative_scores":[
   [0.7,0.2,0.1],
   [0.5,0.3,0.2],
   [0.2,0.3,0.5]
 ]
}
```

### Công thức

```
score = Σ(weight_i * value_i)
```

### Output

```json
{
 "ranking":[
  {"name":"A","score":0.42},
  {"name":"B","score":0.33},
  {"name":"C","score":0.25}
 ]
}
```

Kết quả phải **sort giảm dần theo score**.

---

# 9. Quy tắc code cho AI Agent

Bắt buộc:

* Python 3.10+
* type hint đầy đủ
* tách logic vào `services`
* thuật toán đặt trong `utils`

Ví dụ:

```
def normalize_matrix(matrix: List[List[float]], column_sums: List[float]) -> List[List[float]]:
```

---

# 10. Xử lý lỗi

Hệ thống phải xử lý các lỗi sau:

* ma trận không vuông
* chia cho 0
* column sum = 0
* CR > 0.1 (ma trận không nhất quán)

Trả về:

```
HTTP 400
```

---

# 11. Flow hoạt động frontend

Website sẽ hoạt động theo thứ tự:

```
Nhập ma trận
    ↓
[ Bấm tính tổng cột ]
    ↓
[ Bấm chuẩn hóa ]
    ↓
[ Bấm tính trọng số ]
    ↓
[ Bấm kiểm tra CR ]
    ↓
[ Bấm xếp hạng ]
```

Mỗi bước gọi **1 endpoint riêng**.

---

# 12. Mục tiêu hệ thống

Module này là **AHP Calculation Layer** trong kiến trúc:

```
Database → AHP Engine → AI Prediction → Decision Engine → Visualization
```

Trong đó:

* Database lưu dữ liệu thô
* AHP tính trọng số
* AI dự đoán
* Decision Engine tổng hợp kết quả
* Frontend hiển thị từng bước tính toán
