import sys
import requests # Thư viện để gửi HTTP requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.rsa import Ui_MainWindow # Import class UI từ file rsa_ui.py

API_BASE_URL = "http://localhost:5000/api/rsa" # Địa chỉ API Flask

class RSAApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self) # Thiết lập UI từ Ui_MainWindow
        self.setWindowTitle("Ứng dụng Mã hóa RSA") # Đặt tiêu đề cửa sổ
        self._connect_signals()

    def _connect_signals(self):
        # Kết nối các nút bấm với hàm xử lý tương ứng
        self.btnGenerateKeys.clicked.connect(self.generate_keys)
        self.btnEncrypt.clicked.connect(self.encrypt_message)
        self.btnDecrypt.clicked.connect(self.decrypt_message)
        self.btnSign.clicked.connect(self.sign_message)
        self.btnVerify.clicked.connect(self.verify_signature)

    def _show_message(self, title, message, detail_info="", icon=QMessageBox.Information):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        if detail_info: # Hiển thị thông tin chi tiết nếu có
            msg_box.setInformativeText(detail_info)
        msg_box.setIcon(icon)
        msg_box.exec_()
        
    def generate_keys(self):
        try:
            self.txtInformation.setPlainText("Đang tạo khóa...")
            response = requests.post(f"{API_BASE_URL}/generate_keys")
            response.raise_for_status() 
            
            data = response.json()
            message = data.get("message", "Tạo khóa thành công!")
            self.txtInformation.setPlainText(message)
            self._show_message("Tạo Khóa", message)
            
            # Tùy chọn: Tải và hiển thị public key trong txtInformation hoặc một widget khác nếu muốn
            try:
                pk_response = requests.get(f"{API_BASE_URL}/public_key")
                pk_response.raise_for_status()
                public_key_content = pk_response.text
                self.txtInformation.appendPlainText("\n\nPublic Key:\n" + public_key_content)
            except Exception as pk_e:
                self.txtInformation.appendPlainText(f"\nKhông thể tải Public Key: {pk_e}")

        except requests.exceptions.RequestException as e:
            error_msg = f"Lỗi API khi tạo khóa: {e}"
            self.txtInformation.setPlainText(error_msg)
            self._show_message("Lỗi API", error_msg, icon=QMessageBox.Critical)
        except Exception as e:
            error_msg = f"Lỗi không xác định: {e}"
            self.txtInformation.setPlainText(error_msg)
            self._show_message("Lỗi", error_msg, icon=QMessageBox.Critical)

    def encrypt_message(self):
        message = self.txtPlainText.toPlainText()
        if not message:
            self._show_message("Lỗi Đầu Vào", "Tin nhắn cần mã hóa không được để trống.", icon=QMessageBox.Warning)
            return

        try:
            self.txtInformation.setPlainText(f"Đang mã hóa tin nhắn: \"{message[:30]}...\"")
            payload = {'message': message}
            response = requests.post(f"{API_BASE_URL}/encrypt", json=payload)
            response.raise_for_status()
            
            data = response.json()
            if 'encrypted_message' in data:
                encrypted_text = data['encrypted_message']
                self.txtCipherText.setPlainText(encrypted_text) # Hiển thị ciphertext
                self.txtInformation.setPlainText("Mã hóa tin nhắn thành công.")
                self._show_message("Mã Hóa", "Tin nhắn đã được mã hóa thành công.")
            else:
                error_msg = data.get('error', 'Lỗi mã hóa không xác định.')
                self.txtInformation.setPlainText(error_msg)
                self._show_message("Lỗi Mã Hóa", error_msg, icon=QMessageBox.Critical)
        except requests.exceptions.RequestException as e:
            error_msg = f"Lỗi API khi mã hóa: {e}"
            self.txtInformation.setPlainText(error_msg)
            self._show_message("Lỗi API", error_msg, icon=QMessageBox.Critical)
        except Exception as e:
            error_msg = f"Lỗi không xác định: {e}"
            self.txtInformation.setPlainText(error_msg)
            self._show_message("Lỗi", error_msg, icon=QMessageBox.Critical)

    def decrypt_message(self):
        encrypted_message_b64 = self.txtCipherText.toPlainText()
        if not encrypted_message_b64:
            self._show_message("Lỗi Đầu Vào", "Tin nhắn đã mã hóa không được để trống.", icon=QMessageBox.Warning)
            return

        try:
            self.txtInformation.setPlainText("Đang giải mã tin nhắn...")
            payload = {'encrypted_message': encrypted_message_b64}
            response = requests.post(f"{API_BASE_URL}/decrypt", json=payload)
            response.raise_for_status()
            
            data = response.json()
            if 'decrypted_message' in data:
                decrypted_text = data['decrypted_message']
                self.txtPlainText.setPlainText(decrypted_text) # Hiển thị plaintext
                self.txtInformation.setPlainText("Giải mã tin nhắn thành công.")
                self._show_message("Giải Mã", "Tin nhắn đã được giải mã thành công.")
            else:
                error_msg = data.get('error', 'Lỗi giải mã không xác định.')
                self.txtInformation.setPlainText(error_msg)
                self._show_message("Lỗi Giải Mã", error_msg, icon=QMessageBox.Critical)
        except requests.exceptions.RequestException as e:
            error_detail = "Lỗi API không xác định"
            try: error_detail = e.response.json().get('error', error_detail)
            except: pass
            self.txtInformation.setPlainText(f"Lỗi API khi giải mã: {error_detail}")
            self._show_message("Lỗi API", f"Lỗi API khi giải mã: {error_detail}", icon=QMessageBox.Critical)
        except Exception as e:
            error_msg = f"Lỗi không xác định: {e}"
            self.txtInformation.setPlainText(error_msg)
            self._show_message("Lỗi", error_msg, icon=QMessageBox.Critical)

    def sign_message(self):
        message = self.txtPlainText.toPlainText()
        if not message:
            self._show_message("Lỗi Đầu Vào", "Tin nhắn cần ký không được để trống.", icon=QMessageBox.Warning)
            return
        
        try:
            self.txtInformation.setPlainText(f"Đang ký tin nhắn: \"{message[:30]}...\"")
            payload = {'message': message}
            response = requests.post(f"{API_BASE_URL}/sign", json=payload)
            response.raise_for_status()
            
            data = response.json()
            if 'signature' in data:
                signature_text = data['signature']
                self.txtSignature.setPlainText(signature_text) # Hiển thị chữ ký
                self.txtInformation.setPlainText("Ký tin nhắn thành công.")
                self._show_message("Ký Tin Nhắn", "Tin nhắn đã được ký thành công.")
            else:
                error_msg = data.get('error', 'Lỗi ký không xác định.')
                self.txtInformation.setPlainText(error_msg)
                self._show_message("Lỗi Ký", error_msg, icon=QMessageBox.Critical)
        except requests.exceptions.RequestException as e:
            error_msg = f"Lỗi API khi ký: {e}"
            self.txtInformation.setPlainText(error_msg)
            self._show_message("Lỗi API", error_msg, icon=QMessageBox.Critical)
        except Exception as e:
            error_msg = f"Lỗi không xác định: {e}"
            self.txtInformation.setPlainText(error_msg)
            self._show_message("Lỗi", error_msg, icon=QMessageBox.Critical)

    def verify_signature(self):
        message = self.txtPlainText.toPlainText() # Tin nhắn gốc để xác thực
        signature_b64 = self.txtSignature.toPlainText()

        if not message or not signature_b64:
            self._show_message("Lỗi Đầu Vào", "Tin nhắn và chữ ký không được để trống để xác thực.", icon=QMessageBox.Warning)
            return

        try:
            self.txtInformation.setPlainText("Đang xác thực chữ ký...")
            payload = {'message': message, 'signature': signature_b64}
            response = requests.post(f"{API_BASE_URL}/verify", json=payload)
            response.raise_for_status()
            
            data = response.json()
            result_message = data.get('message', 'Không rõ kết quả xác thực.')
            self.txtInformation.setPlainText(result_message)
            if data.get('is_valid'):
                self._show_message("Xác Thực Chữ Ký", result_message, icon=QMessageBox.Information)
            else:
                self._show_message("Xác Thực Chữ Ký", result_message, icon=QMessageBox.Warning)
        except requests.exceptions.RequestException as e:
            error_msg = f"Lỗi API khi xác thực: {e}"
            self.txtInformation.setPlainText(error_msg)
            self._show_message("Lỗi API", error_msg, icon=QMessageBox.Critical)
        except Exception as e:
            error_msg = f"Lỗi không xác định: {e}"
            self.txtInformation.setPlainText(error_msg)
            self._show_message("Lỗi", error_msg, icon=QMessageBox.Critical)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = RSAApp()
    main_window.show()
    sys.exit(app.exec_())