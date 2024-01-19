import csv
import tkinter as tk
from tkinter import simpledialog, messagebox

def extract_content(text_lines, start_keyword, end_keyword):
    extracted_data = []
    current_content = []
    recording = False

    for line in text_lines:
        if end_keyword in line:
            if len(current_content) > 1:
                current_content.pop()
            break
        if start_keyword in line:
            if recording:
                extracted_data.append("\n".join(current_content).strip())
                current_content = []
            recording = True
        elif recording:
            current_content.append(line)

    if recording and current_content:
        extracted_data.append("\n".join(current_content).strip())

    return extracted_data

def save_to_csv(selected_lines, items):
    file_path = 'output.csv'
    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for idx, line in enumerate(selected_lines):
            item = items[idx % len(items)]
            writer.writerow([f"{item}", line])
    messagebox.showinfo("保存完了", f"CSVファイルが {file_path} に保存されました。")

def main():
    items = ["霊夢"]  # 声のリスト

    root = tk.Tk()
    root.withdraw()  # メインウィンドウを非表示にする

    # 行抽出キーワードと終了キーワードの入力
    start_keyword = simpledialog.askstring("キーワード入力", "抽出する行のキーワードを入力してください:")
    end_keyword = simpledialog.askstring("キーワード入力", "終了する行のキーワードを入力してください:")

    # テキスト入力
    input_text = simpledialog.askstring("テキスト入力", "テキストを入力してください:")
    if not input_text:
        return

    # 文字抽出
    lines = extract_content(input_text.splitlines(), start_keyword, end_keyword)

    # 抽出結果をリストボックスに表示
    root.deiconify()  # メインウィンドウを表示する
    listbox = tk.Listbox(root, selectmode='multiple')
    for line in lines:
        listbox.insert(tk.END, line)
    listbox.pack()

    # CSVに保存するボタン
    button = tk.Button(root, text="CSVに保存", command=lambda: save_to_csv([listbox.get(i) for i in listbox.curselection()], items))
    button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
