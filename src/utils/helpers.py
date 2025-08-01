import pandas as pd

def is_file_open(file_path: str):
    try:
        file = open(file_path, "a")
        file.close()
        return False
    except:
        return True
    
def is_sheet_existed(file_path, sheet_name):
    try:
        # Mở file Excel
        excel_file = pd.ExcelFile(file_path)
        
        # Lấy danh sách các sheet
        sheets = excel_file.sheet_names
        
        # Kiểm tra sheet_name có trong danh sách không
        if sheet_name in sheets:
            return True
        else:
            return False
    except FileNotFoundError: # file không tồn tại
        return False