# Study Planner

`shared.study_planner` đọc danh sách công việc từ CSV, sắp xếp theo mức độ ưu
tiên và phân bổ quỹ giờ học thành một kế hoạch dạng văn bản.

## Yêu cầu và chạy nhanh

- Python 3.10 trở lên; module chỉ dùng thư viện chuẩn, không cần cài thêm gói.
- Chạy các lệnh bên dưới từ thư mục gốc `python-bootcamp`.

```bash
python -m shared.study_planner samples/tasks.csv --hours 2
```

Mặc định chương trình dùng ngày hiện tại để tính độ ưu tiên. Để tái hiện kết quả
mẫu, cố định ngày bằng `--today`:

```bash
python -m shared.study_planner samples/tasks.csv --hours 2 --today 2026-10-29
```

Kết quả:

```text
Study plan (2.0 h):
1. DS exam - 2.0 h
```

## Kiến trúc 4 bước

Điểm vào CLI là [`__main__.py`](__main__.py). Luồng xử lý:

```text
CSV → parse_csv → list[Task] → prioritise → list[Task]
    → allocate → list[Block] → render → văn bản kế hoạch
```

| Bước | Hàm và tệp | Vai trò |
| --- | --- | --- |
| 1. Đọc dữ liệu | `parse_csv(path)` trong [parse.py](parse.py) | Đọc CSV UTF-8, bỏ dòng đầu làm tiêu đề, bỏ dòng dữ liệu trắng, chuyển từng dòng thành `Task`. |
| 2. Xếp ưu tiên | `prioritise(tasks, today)` trong [prioritise.py](prioritise.py) | Sắp xếp giảm dần theo `importance / max((deadline - today).days, 1)`. Công việc đến hạn hôm nay hoặc quá hạn dùng mẫu số 1; nếu bằng điểm, giữ thứ tự đầu vào. Trả về danh sách mới. |
| 3. Phân bổ giờ | `allocate(tasks, hours)` trong [allocate.py](allocate.py) | Duyệt theo thứ tự ưu tiên, cấp tối đa `min(task.effort_h, số giờ còn lại)` cho mỗi công việc và dừng khi hết giờ. Có thể chỉ cấp một phần thời gian cho công việc. |
| 4. Xuất kế hoạch | `render(blocks)` trong [render.py](render.py) | Tạo chuỗi có tổng số giờ đã phân bổ và từng công việc, hiển thị giờ với một chữ số thập phân. Danh sách rỗng cho kết quả `No study blocks planned.` |

Hai kiểu dữ liệu dùng chung được định nghĩa trong [contract.py](../contract.py):

- `Task(title, importance, effort_h, deadline)`: một công việc cần học.
- `Block(task, hours)`: số giờ được phân bổ cho một công việc.

Hàm `validate_tasks(tasks, available_h)` trong [validate.py](validate.py) kiểm tra
`importance` trong khoảng 1–5, `effort_h > 0`, quỹ giờ không âm và tổng thời gian
không vượt quỹ giờ; trả về `True` hoặc `False`. CLI hiện chưa gọi hàm này.

### Sử dụng trong Python

Các bước cũng có thể được gọi trực tiếp từ thư mục gốc của dự án:

```python
from datetime import date

from shared.study_planner.allocate import allocate
from shared.study_planner.parse import parse_csv
from shared.study_planner.prioritise import prioritise
from shared.study_planner.render import render

tasks = parse_csv("samples/tasks.csv")
ordered_tasks = prioritise(tasks, today=date(2026, 10, 29))
blocks = allocate(ordered_tasks, hours=2)
print(render(blocks))
```

## Định dạng CSV

Tệp UTF-8, phân cách bằng dấu phẩy, có dòng tiêu đề và bốn cột theo đúng thứ tự:

| Cột | Kiểu dữ liệu | Ý nghĩa và quy ước |
| --- | --- | --- |
| `title` | Chuỗi | Tên công việc; nên có nội dung. |
| `importance` | Số nguyên | Mức độ quan trọng, theo quy ước từ 1 đến 5. |
| `effort_h` | Số thực | Số giờ cần để hoàn thành; theo quy ước lớn hơn 0, dùng dấu chấm thập phân. |
| `deadline` | Ngày ISO | Hạn hoàn thành, viết theo dạng `YYYY-MM-DD`. |

Ví dụ từ [samples/tasks.csv](../../samples/tasks.csv):

```csv
title,importance,effort_h,deadline
DS exam,5,6,2026-10-30
Assignment,4,1.5,2026-10-27
```

Nếu tên chứa dấu phẩy, đặt trong dấu ngoặc kép, ví dụ `"Ôn tập, chương 1"`.
Khoảng trắng ở hai đầu các trường được loại bỏ.

Parser hiện đọc cột theo vị trí, chưa kiểm tra tên tiêu đề; cột thừa bị bỏ qua,
dòng có ít hơn bốn cột gây `ValueError`. Parser kiểm tra khả năng chuyển kiểu
nhưng chưa kiểm tra tên rỗng, khoảng 1–5 của `importance` hay tính dương của
`effort_h`. Khi tạo CSV, hãy tuân thủ các quy ước trong bảng trên.

## Cú pháp CLI

```text
python -m shared.study_planner <file.csv> --hours <float> [--today YYYY-MM-DD]
```

| Tham số | Bắt buộc | Ý nghĩa |
| --- | --- | --- |
| `file` | Có | Đường dẫn CSV; đường dẫn tương đối được tính từ thư mục đang chạy lệnh. Đặt trong dấu ngoặc kép nếu có khoảng trắng. |
| `--hours` | Có | Quỹ giờ học: số hữu hạn, không âm; có thể dùng số thập phân như `1.5`. |
| `--today` | Không | Ngày dùng để xếp ưu tiên; mặc định là ngày hiện tại của máy chạy. |
| `-h`, `--help` | Không | Hiển thị trợ giúp và thoát. |

Ví dụ:

```bash
python -m shared.study_planner --help
python -m shared.study_planner samples/tasks.csv --hours 1.5 --today 2026-10-26
python -m shared.study_planner samples/tasks.csv --hours 0
```

Với `--hours 0`, chương trình xuất `No study blocks planned.` và thoát thành công.
Tổng giờ trên dòng `Study plan (...)` là thời gian thực tế đã cấp; có thể nhỏ hơn
quỹ giờ nếu tất cả công việc đã được cấp đủ thời gian.

## Lỗi và mã thoát

CLI in kết quả thành công ra `stdout`; thông báo lỗi ra `stderr`.

| Mã thoát | Trường hợp | Ngoại lệ / thông báo |
| --- | --- | --- |
| `0` | Thành công, kể cả không có block; hoặc yêu cầu trợ giúp | Kế hoạch, `No study blocks planned.` hoặc nội dung trợ giúp. |
| `1` | Không tìm thấy tệp | `FileNotFoundError`, CLI in `Error: CSV file not found: <path>`. |
| `1` | Lỗi truy cập hoặc đọc tệp | `OSError` hoặc lớp con, CLI in `Error: <chi tiết lỗi>`. |
| `1` | Tệp hoàn toàn rỗng, không có dòng tiêu đề | `ValueError`, CLI in `Error: CSV file is empty.`. |
| `1` | Dòng thiếu cột, số hoặc ngày không hợp lệ | `ValueError`, thông báo có số dòng dữ liệu bị lỗi. |
| `2` | Thiếu tham số bắt buộc, tham số lạ, sai kiểu số/ngày, hoặc `--hours` âm, vô hạn hay `NaN` | Lỗi đối số do `argparse` xử lý; in hướng dẫn cú pháp và chi tiết lỗi. |

Ví dụ kiểm tra lỗi:

```bash
python -m shared.study_planner samples/missing.csv --hours 2
python -m shared.study_planner samples/tasks_bad.csv --hours 2
python -m shared.study_planner samples/tasks.csv --hours -1
```

**CSV chỉ có tiêu đề:** parser hiện trả về `[]`; CLI xuất
`No study blocks planned.` và mã thoát `0`. Trường hợp này khác với tệp hoàn toàn
rỗng, vốn gây `ValueError`.

**`InfeasiblePlan`:** lớp ngoại lệ được định nghĩa trong
[exceptions.py](exceptions.py), nhận `needed_h` và `available_h`, có thông báo
`Plan is infeasible: needs <needed_h> hours, but only <available_h> hours are available.`
Theo yêu cầu Tuần 3, ngoại lệ này dành cho trường hợp tổng thời gian yêu cầu vượt
quỹ giờ. Tuy nhiên, `allocate` hiện chưa phát sinh ngoại lệ này và CLI chưa bắt
nó; vì vậy chưa có mã thoát CLI riêng cho `InfeasiblePlan`. Với dữ liệu mẫu cần
7.5 giờ, `--hours 2` hoặc `--hours 0.1` vẫn tạo kế hoạch một phần thành công.

Để xử lý lỗi: kiểm tra đường dẫn và quyền đọc tệp khi gặp lỗi tệp; bổ sung dữ
liệu hoặc sửa dòng CSV được nêu trong thông báo khi gặp `ValueError`; kiểm tra
lại cú pháp và giá trị tham số khi mã thoát là `2`.

## Kiểm tra module

Nếu đã cài `pytest`, chạy các kiểm thử liên quan từ thư mục gốc:

```bash
python -m pytest -q tests/test_study_planner_parse.py tests/test_study_planner_validate.py tests/test_prioritise.py tests/test_allocate.py tests/test_render.py
```
