from QuanLySinhVien import QuanLySinhVien # Assuming QuanLySinhVien.py is in the same directory

def main_menu():
    """Prints the main menu options."""
    print("\n======== CHUONG TRINH QUAN LY SINH VIEN ========")
    print("********************** MENU **********************")
    print("** 1. Them sinh vien moi.                       **")
    print("** 2. Cap nhat thong tin sinh vien (theo ID).   **")
    print("** 3. Xoa sinh vien (theo ID).                  **")
    print("** 4. Tim kiem sinh vien (theo ten).            **")
    print("** 5. Sap xep sinh vien theo diem trung binh.   **")
    print("** 6. Sap xep sinh vien theo ten.               **") # Changed from "ten chuyen nganh" to "ten" as sortByName is used
    print("** 7. Hien thi danh sach sinh vien.             **")
    print("** 0. Thoat chuong trinh.                       **")
    print("**************************************************")

def get_menu_choice():
    """Gets and validates the user's menu choice."""
    while True:
        try:
            choice = int(input("Nhap tuy chon cua ban: "))
            return choice
        except ValueError:
            print("Lua chon khong hop le. Vui long nhap mot so.")

def get_student_id_input():
    """Gets and validates student ID input."""
    while True:
        try:
            student_id = int(input("Nhap ID sinh vien: "))
            return student_id
        except ValueError:
            print("ID phai la mot so. Vui long nhap lai.")

if __name__ == "__main__":
    qlsv = QuanLySinhVien()

    while True: # Changed from while(11) to standard while True
        main_menu()
        key = get_menu_choice()

        if key == 1:
            print("\n--- 1. Them sinh vien moi ---")
            qlsv.nhapSinhVien()
            # The success message is now part of qlsv.nhapSinhVien() from previous refactoring

        elif key == 2:
            print("\n--- 2. Cap nhat thong tin sinh vien ---")
            if qlsv.soLuongSinhVien() > 0:
                student_id = get_student_id_input()
                qlsv.updateSinhVien(student_id)
            else:
                print("Danh sach sinh vien hien dang trong!")

        elif key == 3:
            print("\n--- 3. Xoa sinh vien ---")
            if qlsv.soLuongSinhVien() > 0:
                student_id = get_student_id_input()
                # The deleteById method in QuanLySinhVien now prints its own status message
                qlsv.deleteById(student_id)
            else:
                print("Danh sach sinh vien hien dang trong!")

        elif key == 4:
            print("\n--- 4. Tim kiem sinh vien theo ten ---")
            if qlsv.soLuongSinhVien() > 0:
                name = input("Nhap ten sinh vien can tim: ")
                search_result = qlsv.findByName(name)
                if search_result:
                    print(f"\n--- Ket qua tim kiem cho '{name}' ---")
                    qlsv.showSinhVien(search_result)
                else:
                    print(f"Khong tim thay sinh vien nao co ten chua '{name}'.")
            else:
                print("Danh sach sinh vien hien dang trong!")

        elif key == 5:
            print("\n--- 5. Sap xep sinh vien theo diem trung binh ---")
            if qlsv.soLuongSinhVien() > 0:
                qlsv.sortByDiemTB()
                # showSinhVien will print the sorted list
                qlsv.showSinhVien(qlsv.getListSinhVien())
            else:
                print("Danh sach sinh vien hien dang trong!")

        elif key == 6:
            print("\n--- 6. Sap xep sinh vien theo ten ---")
            if qlsv.soLuongSinhVien() > 0:
                qlsv.sortByName()
                qlsv.showSinhVien(qlsv.getListSinhVien())
            else:
                print("Danh sach sinh vien hien dang trong!")

        elif key == 7:
            print("\n--- 7. Hien thi danh sach sinh vien ---")
            # showSinhVien handles the case of an empty list internally
            qlsv.showSinhVien(qlsv.getListSinhVien())

        elif key == 0:
            print("\nBan da chon thoat. Tam biet!")
            break

        else:
            print("\nChuc nang khong hop le!")
            print("Vui long chon mot chuc nang co trong menu.")

        input("\nNhan Enter de tiep tuc...") # Pause for user to read output