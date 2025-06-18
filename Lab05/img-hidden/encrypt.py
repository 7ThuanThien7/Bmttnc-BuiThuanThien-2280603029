import sys
try:
    from PIL import Image
except ImportError:
    print("Thư viện Pillow chưa được cài đặt.")
    print("Vui lòng cài đặt bằng lệnh: pip install Pillow")
    sys.exit(1)

def encode_image(image_path, message):
    """
    Hàm này dùng để giấu một thông điệp vào trong một hình ảnh.
    """
    try:
        img = Image.open(image_path)
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file ảnh tại đường dẫn '{image_path}'")
        return
    except Exception as e:
        print(f"Lỗi khi mở ảnh: {e}")
        return

    # Chuyển đổi thông điệp sang dạng nhị phân
    # Mỗi ký tự sẽ được chuyển thành 8 bit nhị phân
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    
    # Thêm một chuỗi bit đặc biệt để đánh dấu kết thúc thông điệp
    # Điều này giúp chương trình giải mã biết khi nào nên dừng lại
    binary_message += '1111111111111110' 

    # Kiểm tra xem ảnh có đủ lớn để chứa thông điệp không
    if len(binary_message) > img.width * img.height * 3:
        print("Lỗi: Thông điệp quá dài để giấu trong ảnh này.")
        return

    data_index = 0
    # Duyệt qua từng pixel của ảnh
    for row in range(img.height):
        for col in range(img.width):
            # Lấy giá trị màu (R, G, B) của pixel
            pixel = list(img.getpixel((col, row)))

            # Duyệt qua từng kênh màu (Red, Green, Blue)
            for color_channel in range(3):
                # Nếu vẫn còn bit trong thông điệp để giấu
                if data_index < len(binary_message):
                    # Lấy giá trị nhị phân của kênh màu
                    pixel_binary = format(pixel[color_channel], '08b')
                    
                    # Thay thế bit cuối cùng (Least Significant Bit - LSB)
                    # của kênh màu bằng bit của thông điệp
                    new_pixel_binary = pixel_binary[:-1] + binary_message[data_index]
                    
                    # Chuyển giá trị nhị phân mới trở lại dạng số nguyên
                    pixel[color_channel] = int(new_pixel_binary, 2)
                    data_index += 1
            
            # Cập nhật lại pixel trong ảnh với giá trị màu mới
            img.putpixel((col, row), tuple(pixel))

            # Nếu đã giấu xong toàn bộ thông điệp, thoát khỏi vòng lặp
            if data_index >= len(binary_message):
                break
        if data_index >= len(binary_message):
            break
            
    # Lưu ảnh đã được giấu tin
    encoded_image_path = 'encoded_image.png'
    img.save(encoded_image_path)
    print(f"Hoàn tất giấu tin. Ảnh đã mã hóa được lưu tại: {encoded_image_path}")

def main():
    """
    Hàm chính để xử lý các tham số đầu vào từ dòng lệnh.
    """
    # Kiểm tra xem người dùng có nhập đủ 2 tham số không
    # (đường dẫn ảnh và thông điệp)
    if len(sys.argv) != 3:
        print("Cách sử dụng: python encrypt.py <duong_dan_anh> \"<thong_diep>\"")
        print("Ví dụ: python encrypt.py my_image.png \"Hello World\"")
        return
    
    image_path = sys.argv[1]
    message = sys.argv[2]
    encode_image(image_path, message)

# Điểm bắt đầu của chương trình
if __name__ == "__main__":
    main()