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

def save_to_csv(lines, items):
    file_path = 'output.csv'
    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for idx, line in enumerate(lines):
            item = items[idx % len(items)]
            writer.writerow([f"{item}", line])
    messagebox.showinfo("保存完了", f"CSVファイルが {file_path} に保存されました。")

def update_line(listbox, idx, new_text):
    listbox.delete(idx)
    listbox.insert(idx, new_text)

def on_right_click(event, listbox, text_widget):
    try:
        idx = listbox.nearest(event.y)  # クリックされた位置に最も近いアイテムのインデックスを取得
        edit_line(listbox, idx, text_widget)
    except IndexError:
        pass  # クリックされた位置にアイテムがない場合は何もしない

def edit_line(listbox, idx, text_widget):
    original_text = listbox.get(idx)
    text_widget.delete('1.0', tk.END)
    text_widget.insert(tk.END, original_text)
    text_widget.edit_idx = idx  # 現在編集している行のインデックスを保存

def save_edit(listbox, text_widget):
    if hasattr(text_widget, 'edit_idx'):
        new_text = text_widget.get('1.0', tk.END).strip()
        update_line(listbox, text_widget.edit_idx, new_text)

def main():
    items = ["霊夢"]  # 声のリスト

    root = tk.Tk()
    root.withdraw()  # メインウィンドウを非表示にする
    root.geometry('800x600')

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
    list_frame = tk.Frame(root)
    list_frame.pack()

    listbox = tk.Listbox(list_frame, selectmode='multiple', height=20, width=80)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    for line in lines:
        listbox.insert(tk.END, line)

    scrollbar = tk.Scrollbar(list_frame, orient='vertical', command=listbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    listbox.config(yscrollcommand=scrollbar.set)

    text_widget = tk.Text(root, height=4, width=80)
    text_widget.pack()

    save_button = tk.Button(root, text="編集を保存", command=lambda: save_edit(listbox, text_widget))
    save_button.pack()

    listbox.bind("<Button-3>", lambda event: on_right_click(event, listbox, text_widget))  # 右クリックイベントのバインド

    # CSVに保存するボタン
    button = tk.Button(root, text="CSVに保存", command=lambda: save_to_csv([listbox.get(i) for i in listbox.curselection()], items))
    button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
