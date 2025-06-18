import sys
try:
    from PIL import Image
except ImportError:
    print("Thư viện Pillow chưa được cài đặt.")
    print("Vui lòng cài đặt bằng lệnh: pip install Pillow")
    sys.exit(1)

def decode_image(encoded_image_path):
    """
    Hàm này dùng để trích xuất một thông điệp đã được giấu trong ảnh.
    """
    try:
        img = Image.open(encoded_image_path)
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file ảnh tại đường dẫn '{encoded_image_path}'")
        return None
    except Exception as e:
        print(f"Lỗi khi mở ảnh: {e}")
        return None

    binary_message = ""
    # Duyệt qua từng pixel của ảnh để lấy lại chuỗi nhị phân
    for row in range(img.height):
        for col in range(img.width):
            pixel = img.getpixel((col, row))
            # Duyệt qua từng kênh màu (Red, Green, Blue)
            for color_channel in range(3):
                # Trích xuất bit cuối cùng (LSB) từ mỗi kênh màu
                binary_message += format(pixel[color_channel], '08b')[-1]

    # --- PHẦN ĐƯỢC HIỆU CHỈNH SO VỚI ẢNH GỐC ---
    # Code mã hóa dùng '1111111111111110' để đánh dấu kết thúc thông điệp.
    # Chúng ta cần tìm đúng chuỗi bit này để dừng lại.
    end_marker = '1111111111111110'
    marker_position = binary_message.find(end_marker)

    if marker_position == -1:
        # Nếu không tìm thấy chuỗi bit đánh dấu, có thể ảnh không chứa tin nhắn
        print("Lỗi: Không tìm thấy thông điệp được mã hóa trong ảnh này.")
        return None
    
    # Chỉ lấy phần dữ liệu nhị phân trước chuỗi bit đánh dấu
    data_bits = binary_message[:marker_position]
    
    message = ""
    # Chuyển đổi chuỗi nhị phân trở lại thành văn bản
    # Lặp qua chuỗi bit, mỗi lần lấy 8 bit để tạo thành một ký tự
    for i in range(0, len(data_bits), 8):
        byte = data_bits[i:i+8]
        # Đảm bảo khối bit đủ 8 bit trước khi chuyển đổi
        if len(byte) == 8:
            message += chr(int(byte, 2))
            
    return message

def main():
    """
    Hàm chính để xử lý tham số đầu vào từ dòng lệnh.
    """
    # Script này chỉ cần 1 tham số: đường dẫn đến ảnh đã mã hóa
    if len(sys.argv) != 2:
        print("Cách sử dụng: python decrypt.py <duong_dan_anh_ma_hoa>")
        print("Ví dụ: python decrypt.py encoded_image.png")
        return
    
    encoded_image_path = sys.argv[1]
    decoded_message = decode_image(encoded_image_path)
    
    # Nếu giải mã thành công, in thông điệp ra màn hình
    if decoded_message is not None:
        print("-----------------------------------------")
        print(f"Thông điệp đã giải mã: {decoded_message}")
        print("-----------------------------------------")

# Điểm bắt đầu của chương trình
if __name__ == "__main__":
    main()