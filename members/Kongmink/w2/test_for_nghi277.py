from members.nghi277.w1.text_tools import top_k, word_count

# ==========================================
# Tests for word_count
# ==========================================

def test_word_count_basic_and_case_insensitive():
    """Kiểm tra đếm từ cơ bản và không phân biệt chữ hoa/thường."""
    text = "Hello world hello"
    expected = {"hello": 2, "world": 1}
    assert word_count(text) == expected


def test_word_count_punctuations():
    """Kiểm tra việc loại bỏ dấu câu (., !, ?, ;, :) và thay thế bằng khoảng trắng."""
    text = "apple,banana. apple! banana? orange; grape:"
    expected = {"apple": 2, "banana": 2, "orange": 1, "grape": 1}
    assert word_count(text) == expected


def test_word_count_empty_and_whitespace():
    """Kiểm tra chuỗi rỗng hoặc chỉ toàn khoảng trắng / dấu câu."""
    assert word_count("") == {}
    assert word_count("   \n\t  ") == {}
    assert word_count("... !!! ??? ,,, ;;; :::") == {}


# ==========================================
# Tests for top_k
# ==========================================

def test_top_k_basic_and_tie_breaking():
    """
    Kiểm tra top k từ xuất hiện nhiều nhất.
    Edge case: Khi tần suất bằng nhau (-x[1]), phải sắp xếp theo thứ tự bảng chữ cái (x[0]).
    """
    text = "banana apple orange banana apple grape"
    # Tần suất: banana: 2, apple: 2, orange: 1, grape: 1
    # Với k=2: 'apple' và 'banana' cùng có 2 lần, 'apple' đứng trước 'banana' theo bảng chữ cái.
    result = top_k(text, k=2)
    assert result == [("apple", 2), ("banana", 2)]


def test_top_k_greater_than_unique_words():
    """Kiểm tra khi k lớn hơn tổng số từ phân biệt trong văn bản."""
    text = "one two one"
    result = top_k(text, k=10)
    assert result == [("one", 2), ("two", 1)]


def test_top_k_zero_or_negative():
    """Kiểm tra khi k <= 0."""
    text = "python is fun"
    assert top_k(text, k=0) == []
    result = top_k(text, k=10)
    assert len(result) == 3


# ==========================================
# Edge case nâng cao (W2-4: Instructor test might not cover)
# ==========================================

def test_word_count_unhandled_punctuations_and_special_chars():
    """
    Edge case: Kiểm tra các dấu câu khác chưa được xử lý trong hàm như gạch nối '-', ngoặc kép '"'.
    Lưu ý: Test này phản ánh hành vi hiện tại của code.
    Ví dụ: 'state-of-the-art' hiện bị tính là 1 từ thay vì tách rời.
    """
    text = 'Say "hello" to state-of-the-art!'
    result = word_count(text)
    # Hiện tại dấu '"' và '-' không nằm trong danh sách thay thế nên dính liền vào từ
    assert '"hello"' in result
    assert "state-of-the-art" in result