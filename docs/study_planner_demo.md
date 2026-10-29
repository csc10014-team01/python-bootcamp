# Study Planner CLI Execution Demo

Tài liệu lưu trữ kết quả chạy mẫu của công cụ dòng lệnh `shared.study_planner`.

---

## 1. Trường hợp chạy với 2.0 giờ khả dụng (Happy Path)

**Lệnh thực thi:**
```bash
python -m shared.study_planner samples/tasks.csv --hours 2
```

**Kết quả đầu ra (Output):**
```text
Study plan (2.0 h):
1. DS exam - 2.0 h
```

---

## 2. Trường hợp chạy với 0.1 giờ khả dụng

**Lệnh thực thi:**
```bash
python -m shared.study_planner samples/tasks.csv --hours 0.1
```

**Kết quả đầu ra (Output):**
```text
Study plan (0.1 h):
1. DS exam - 0.1 h
```

---

## 3. Trường hợp tệp không tồn tại (FileNotFoundError)

**Lệnh thực thi:**
```bash
python -m shared.study_planner samples/missing.csv --hours 2
```

**Kết quả đầu ra (Output):**
```text
Lỗi: Không tìm thấy tệp 'samples/missing.csv'
```