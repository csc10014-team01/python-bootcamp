def is_palindrome(text: str) -> bool:
    """
    Điểm khác biệt so với C++:
    Trong C++, ta thường dùng vòng lặp để so sánh từng ký tự từ hai đầu chuỗi 
    vào giữa. Trong Python, ta có thể dùng slicing text[::-1] để đảo ngược chuỗi 
    và so sánh trực tiếp bằng == chỉ trong 1 dòng.
    """
    return text == text[::-1]