# Hướng dẫn viết Python Commands cho Discord Bot

Hệ thống hỗ trợ chạy các file Python (`.py`) như một discord command. Bot sẽ tự động thực thi script và lấy output (`print`) để trả lời user.

## 1. Cấu trúc cơ bản

Mỗi file `.py` trong thư mục `commands/` sẽ được đăng ký là mic slash command.
- **Tên file:** là tên command (ví dụ: `hello.py` -> `/hello`).
- **Nội dung:** Code python chuẩn.
- **Output:** Bất cứ gì bạn `print()` sẽ được gửi lại cho user.

### Ví dụ: `hello.py`
```python
import sys

# Lấy arguments từ dòng lệnh (do bot truyền vào)
# sys.argv[0] là tên file script
# sys.argv[1...] là các tham số user nhập

print("Xin chào từ Python! 🐍")
```

---

## 2. Nhận Tham số (Arguments)

Khi user dùng lệnh kèm tham số (ví dụ: `/calc add 10 20`), các giá trị này sẽ được chuyển thành arguments dòng lệnh.

### Khai báo tham số (trong Manager UI)
Bạn cần cấu hình parameters trong tab **Metadata** của Command Editor:
- Name: `a` (Type: Integer)
- Name: `b` (Type: Integer)

### Đọc tham số (trong Python)
```python
import sys

# sys.argv[1] là tham số đầu tiên, sys.argv[2] là tham số thứ hai...
if len(sys.argv) < 3:
    print("Vui lòng nhập đủ 2 số!")
    sys.exit(1)

a = int(sys.argv[1])
b = int(sys.argv[2])
result = a + b

print(f"Kết quả: {a} + {b} = {result}")
```

---

## 3. Tương tác Database (Supabase)

Hệ thống cung cấp module `db` được cấu hình sẵn. Bạn **KHÔNG** cần cài driver hay setup connection string.

### Import
```python
from db import db
```

### Các hàm hỗ trợ

#### `select(table, where=None, limit=None, order_by=None)`
Lấy dữ liệu từ bảng.
```python
# Lấy 5 logs mới nhất
logs = db.select('logs', limit=5, order_by='created_at.desc')

# Lấy log của worker cụ thể
my_logs = db.select('logs', where={'node_id': 'worker-1'})
```

#### `insert(table, data)`
Thêm dữ liệu mới.
```python
record = db.insert('users', {
    'username': 'nguyenvana',
    'points': 100
})
print(f"Đã thêm user, ID: {record['id']}")
```

#### `update(table, where, data)`
Cập nhật dữ liệu.
```python
db.update('users', where={'id': 1}, data={'points': 200})
```

#### `count(table, where=None)`
Đếm số dòng.
```python
total = db.count('logs')
print(f"Tổng số log: {total}")
```

---

## 4. Lưu ý quan trọng

1.  **UTF-8 Output**: Hệ thống tự động xử lý encoding, bạn có thể print tiếng Việt thoải mái.
2.  **Dependencies**: Worker cần phải có các library bạn dùng (ví dụ `requests`, `numpy`). Nếu worker chưa cài, script sẽ lỗi.
    - *Best Practice:* Chỉ dùng standard library hoặc đảm bảo môi trường Worker đã setup đủ.
3.  **Timeout**: Command cần chạy xong trong vòng 3 giây (mặc định của Discord interaction), nếu xử lý lâu hơn hãy dùng queue background (tính năng nâng cao).
