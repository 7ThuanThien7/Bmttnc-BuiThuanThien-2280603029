from SinhVien import SinhVien

class QuanLySinhVien:
    def __init__(self):
        self.listSinhVien = []

    def generateID(self):
        maxId = 0  # Start with 0, so the first ID will be 1
        if self.soLuongSinhVien() > 0:
            # Consider using a set for faster max finding if performance is critical for very large lists
            maxId = max(sv._id for sv in self.listSinhVien)
        return maxId + 1

    def soLuongSinhVien(self):
        return len(self.listSinhVien) # Use Python's built-in len()

    def nhapSinhVien(self):
        svId = self.generateID()
        name = input("Nhap ten sinh vien: ")
        sex = input("Nhap gioi tinh sinh vien: ")
        major = input("Nhap chuyen nganh cua sinh vien: ")
        # Add input validation for diemTB
        while True:
            try:
                diemTB = float(input("Nhap diem cua sinh vien: "))
                if 0 <= diemTB <= 10: # Assuming a 0-10 scale
                    break
                else:
                    print("Diem TB phai nam trong khoang tu 0 den 10. Vui long nhap lai.")
            except ValueError:
                print("Diem TB phai la mot so. Vui long nhap lai.")

        sv = SinhVien(svId, name, sex, major, diemTB)
        self.xepLoaiHocLuc(sv)
        self.listSinhVien.append(sv)
        print("Them sinh vien thanh cong!")

    def updateSinhVien(self, ID):
        sv: SinhVien = self.findByID(ID)
        if sv: # More Pythonic way to check if sv is not None
            print(f"--- Cap nhat thong tin cho sinh vien co ID: {ID} ---")
            print(f"Ten cu: {sv._name}")
            name_input = input("Nhap ten sinh vien moi (nhan Enter de bo qua): ")
            if name_input: # Only update if user provided input
                sv._name = name_input

            print(f"Gioi tinh cu: {sv._sex}")
            sex_input = input("Nhap gioi tinh sinh vien moi (nhan Enter de bo qua): ")
            if sex_input:
                sv._sex = sex_input

            print(f"Chuyen nganh cu: {sv._major}")
            major_input = input("Nhap chuyen nganh moi cua sinh vien (nhan Enter de bo qua): ")
            if major_input:
                sv._major = major_input # Assuming major is a string, removed int() conversion

            print(f"Diem TB cu: {sv._diemTB}")
            diemTB_input = input("Nhap diem moi cua sinh vien (nhan Enter de bo qua): ")
            if diemTB_input:
                while True:
                    try:
                        new_diemTB = float(diemTB_input)
                        if 0 <= new_diemTB <= 10:
                            sv._diemTB = new_diemTB
                            break
                        else:
                            print("Diem TB phai nam trong khoang tu 0 den 10.")
                            diemTB_input = input("Nhap lai diem moi cua sinh vien (nhan Enter de bo qua): ")
                            if not diemTB_input: break # Allow skipping if user enters blank again
                    except ValueError:
                        print("Diem TB phai la mot so.")
                        diemTB_input = input("Nhap lai diem moi cua sinh vien (nhan Enter de bo qua): ")
                        if not diemTB_input: break # Allow skipping

            self.xepLoaiHocLuc(sv)
            print(f"Cap nhat sinh vien co ID {ID} thanh cong.")
        else:
            print(f"Sinh vien co ID {ID} khong ton tai.")

    def sortByID(self):
        self.listSinhVien.sort(key=lambda x: x._id, reverse=False) # Corrected 'key-lambda' and 'reverse-False'
        print("Da sap xep danh sach sinh vien theo ID.")

    def sortByName(self):
        self.listSinhVien.sort(key=lambda x: x._name.lower(), reverse=False) # Sort case-insensitively
        print("Da sap xep danh sach sinh vien theo Ten.")

    def sortByDiemTB(self):
        self.listSinhVien.sort(key=lambda x: x._diemTB, reverse=False)
        print("Da sap xep danh sach sinh vien theo Diem TB.")

    def findByID(self, ID):
        # Consider using a dictionary for ID lookups if performance is critical for very large lists
        for sv in self.listSinhVien:
            if sv._id == ID: # Corrected 'sv. id ID'
                return sv
        return None # Return None if not found, consistent with updateSinhVien

    def findByName(self, keyword):
        listSV = []
        if self.soLuongSinhVien() > 0:
            for sv in self.listSinhVien:
                if keyword.upper() in sv._name.upper():
                    listSV.append(sv)
        return listSV

    def deleteById(self, ID):
        sv = self.findByID(ID)
        if sv:
            self.listSinhVien.remove(sv)
            print(f"Da xoa sinh vien co ID {ID}.")
            return True
        print(f"Sinh vien co ID {ID} khong tim thay de xoa.")
        return False

    def xepLoaiHocLuc(self, sv: SinhVien):
        # Ensure sv._diemTB is float
        try:
            diem = float(sv._diemTB)
            if diem >= 8:
                sv._hocLuc = "Gioi"
            elif diem >= 6.5:
                sv._hocLuc = "Kha" # Removed duplicate "Kha"
            elif diem >= 5:
                sv._hocLuc = "Trung binh"
            else:
                sv._hocLuc = "Yeu"
        except (ValueError, TypeError):
             sv._hocLuc = "N/A" # Handle cases where diemTB might not be a valid number
             print(f"Warning: Khong the xep loai cho sinh vien {sv._name} do diem khong hop le.")


    def showSinhVien(self, listSV_to_show=None): # Allow showing a specific list or the main list
        if listSV_to_show is None:
            listSV_to_show = self.listSinhVien

        # Header updated for clarity
        print("\n--- DANH SACH SINH VIEN ---")
        print(f"{'ID':<5} {'Ten Sinh Vien':<25} {'Gioi Tinh':<12} {'Chuyen Nganh':<20} {'Diem TB':<10} {'Hoc Luc':<10}")
        print("-" * 82) # Separator line

        if len(listSV_to_show) > 0: # Use Python's built-in len()
            for sv in listSV_to_show:
                # Ensure all attributes exist before trying to format
                sv_id = getattr(sv, '_id', 'N/A')
                sv_name = getattr(sv, '_name', 'N/A')
                sv_sex = getattr(sv, '_sex', 'N/A')
                sv_major = getattr(sv, '_major', 'N/A')
                sv_diemTB = getattr(sv, '_diemTB', 'N/A')
                sv_hocLuc = getattr(sv, '_hocLuc', 'N/A')

                # Format diemTB as float with 2 decimal places if it's a number
                try:
                    diemTB_formatted = f"{float(sv_diemTB):.2f}"
                except (ValueError, TypeError):
                    diemTB_formatted = sv_diemTB

                print(f"{str(sv_id):<5} {str(sv_name):<25} {str(sv_sex):<12} {str(sv_major):<20} {str(diemTB_formatted):<10} {str(sv_hocLuc):<10}")
        else:
            print("Danh sach sinh vien trong.")
        print("-" * 82) # Separator line
        print("\n")

    def getListSinhVien(self):
        return self.listSinhVien