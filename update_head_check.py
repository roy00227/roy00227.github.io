import tkinter as tk
from tkinter import messagebox, scrolledtext
import os
# import re # 正規表現の利用を停止

# --- 設定 ---
EXCLUDE_FILES = ["header.html", "footer.html", "google224cc59b9c585584.html"]
# --------------------

# ... (GUIの show_results 関数は省略、変更なし) ...

def show_results(root, updated_files, failed_files):
    # (省略：結果表示ウィンドウのコードは以前と同じです)
    result_window = tk.Toplevel(root)
    result_window.title("処理結果")
    
    result_window.grid_columnconfigure(0, weight=1)
    result_window.grid_columnconfigure(1, weight=1)
    result_window.grid_rowconfigure(1, weight=1)

    # --- 成功ファイル枠 ---
    tk.Label(result_window, text=f"✅ 成功ファイル ({len(updated_files)} 件):", font=('Arial', 10, 'bold')).grid(row=0, column=0, padx=10, pady=5, sticky="w")
    success_text = scrolledtext.ScrolledText(result_window, wrap="word", width=40, height=15)
    success_text.grid(row=1, column=0, padx=10, pady=5, sticky="nsew") 
    
    for f in updated_files:
        success_text.insert(tk.END, f"{f}\n")
    success_text.config(state=tk.DISABLED)

    # --- 失敗ファイル枠 ---
    tk.Label(result_window, text=f"⚠️ 失敗ファイル (パターン不一致) ({len(failed_files)} 件):", font=('Arial', 10, 'bold')).grid(row=0, column=1, padx=10, pady=5, sticky="w")
    failed_text = scrolledtext.ScrolledText(result_window, wrap="word", width=40, height=15)
    failed_text.grid(row=1, column=1, padx=10, pady=5, sticky="nsew") 
    
    for f in failed_files:
        failed_text.insert(tk.END, f"{f}\n")
    failed_text.config(state=tk.DISABLED)

    # --- 概要 ---
    tk.Label(result_window, text=f"合計処理ファイル数: {len(updated_files) + len(failed_files)} 件", anchor="w").grid(row=2, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="w")


def replace_in_files():
    """ファイルを検索・置換するメインロジック（プレーンテキスト置換）"""
    # ユーザー入力を取得し、Pythonのreplaceメソッドで処理
    search_text_input = search_text.get("1.0", tk.END).strip()
    replace_text_input = replace_text_area.get("1.0", tk.END).strip()
    target_dir = os.path.dirname(os.path.abspath(__file__)) 

    if not search_text_input:
        messagebox.showerror("エラー", "検索文字列を入力してください。")
        return

    updated_files = []
    failed_files = []
    
    # ディレクトリ内のすべてのファイルとフォルダを走査
    for root_dir, _, files in os.walk(target_dir):
        for filename in files:
            if not filename.endswith(".html"):
                continue
                
            if filename in EXCLUDE_FILES:
                continue

            filepath = os.path.join(root_dir, filename)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception:
                failed_files.append(filepath + " (読み込みエラー)")
                continue
            
            # ★ 修正: str.replace() でプレーンテキスト置換を実行 ★
            new_content = content.replace(search_text_input, replace_text_input)
            
            # 置換されたかどうかの判定 (文字列の長さでチェック)
            if new_content != content:
                # 変更が成功した場合、ファイルに書き込む
                try:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    updated_files.append(filepath)
                except Exception:
                     failed_files.append(filepath + " (書き込みエラー)")
            else:
                # パターンに一致しない場合、失敗（要確認）と見なす
                failed_files.append(filepath)
    
    show_results(root, updated_files, failed_files)


# --- GUIのセットアップ ---
root = tk.Tk()
root.title("HTML一括置換ツール (プレーンモード)")

# ウィンドウの列/行設定 (リサイズ対応)
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1) 
root.grid_rowconfigure(3, weight=1) 

# 検索文字列のラベルと入力欄
tk.Label(root, text="検索文字列 (インデントや改行も含め、完全に一致させる必要があります)", anchor="w").grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
search_text = tk.Text(root, height=5, width=80)
search_text.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

# 置換文字列のラベルと入力欄
tk.Label(root, text="置換文字列 (新しいHTMLコード全体)", anchor="w").grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")
replace_text_area = tk.Text(root, height=10, width=80)
replace_text_area.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")

# 注意事項
tk.Label(root, text=f"⚠️ このツールは、インデント・改行まで完全に一致するプレーン置換です。", fg="red").grid(row=4, column=0, padx=10, pady=(5, 0), sticky="w")
tk.Label(root, text=f"除外ファイル: {', '.join(EXCLUDE_FILES)}", fg="blue").grid(row=5, column=0, padx=10, pady=(5, 0), sticky="w")

# 実行ボタン
tk.Button(root, text="実行 (全HTMLファイルを置換)", command=replace_in_files, bg="red", fg="white").grid(row=6, column=0, padx=10, pady=20)

root.mainloop()