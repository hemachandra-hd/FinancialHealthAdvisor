# utils/file_handler.py

import os
import shutil

def handle_file(uploaded_file, save_directory="uploads"):
    # Ensure the directory exists
    os.makedirs(save_directory, exist_ok=True)
    
    # Define the save path
    save_path = os.path.join(save_directory, uploaded_file.name)
    
    # Save the file
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return save_path







# import os
# from parsers.csv_parser import parse_csv
# from parsers.pdf_parser import parse_pdf
# from parsers.text_parser import parse_txt

# def handle_file(file_path):
#     ext = os.path.splitext(file_path)[-1].lower()
#     if ext == ".csv":
#         return parse_csv(file_path)
#     elif ext == ".pdf":
#         return parse_pdf(file_path)
#     elif ext == ".txt":
#         return parse_txt(file_path)
#     else:
#         return f"Unsupported file type: {ext}"
