import csv
import tkinter as tk
from tkinter import simpledialog, messagebox

def extract_content(text_lines):
    extracted_data = []
    current_content = []
    recording = False

    for line in text_lines:
        if '新着レスの表示' in line:
            if len(current_content) > 1:
                current_content.pop()
            break
        if 'それでも動く名無し' in line:
            if recording:
                extracted_data.append("\n".join(current_content).strip())
                current_content = []
            recording = True
        elif recording:
            current_content.append(line)

    if recording and current_content:
        extracted_data.append("\n".join(current_content).strip())

    return extracted_data

def save_to_csv(selected_lines):
    file_path = 'output.csv'
    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for line in selected_lines:
            writer.writerow([line])
    messagebox.showinfo("保存完了", f"CSVファイルが {file_path} に保存されました。")

def main():
    input_text = simpledialog.askstring("テキスト入力", "テキストを入力してください:")
    if not input_text:
        return

    lines = extract_content(input_text.splitlines())

    root = tk.Tk()
    listbox = tk.Listbox(root, selectmode='multiple')
    for line in lines:
        listbox.insert(tk.END, line)
    listbox.pack()

    button = tk.Button(root, text="CSVに保存", command=lambda: save_to_csv([listbox.get(i) for i in listbox.curselection()]))
    button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
