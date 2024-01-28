import tkinter as tk
from tkinter import filedialog
import json

def load_and_modify_file(root):
    # ファイル選択ダイアログを表示
    filepath = filedialog.askopenfilename(
        title="ymmpファイルを選択してください",
        filetypes=(("ymmp Files", "*.ymmp"), ("All Files", "*.*"))
    )

    if not filepath:
        root.destroy()  # ファイルが選択されなかった場合、プログラムを終了
        return

    try:
        # ファイルを読み込む
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()

        # "Hatsuon": " の後に 、、 を追加
        modified_content = content.replace('"Hatsuon": "', '"Hatsuon": "、、')

        # 変更をファイルに保存
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(modified_content)

        print("ファイルが更新されました。")

    except Exception as e:
        print("エラーが発生しました:", e)

    root.destroy()  # 処理が完了したらプログラムを終了

def main():
    root = tk.Tk()
    root.withdraw()  # メインウィンドウを表示しない
    load_and_modify_file(root)

if __name__ == "__main__":
    main()
