import os
import openpyxl
from openpyxl import Workbook

def update_excel(problem_name, difficulty_level, code_link, explanation, folder_path):
    excel_path = os.path.join(folder_path, "problems.xlsx")
    if not os.path.exists(excel_path):
        wb = Workbook()
    else:
        wb = openpyxl.load_workbook(excel_path)
    sheet = wb.active
    if sheet.title == "Sheet":
        sheet.title = "Problems"
        sheet.append(["Problem Name", "Difficulty Level", "Code Link", "Explanation"])
    sheet.append([problem_name, difficulty_level, code_link, explanation])
    wb.save(excel_path)