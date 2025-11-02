import tkinter as tk
from tkinter import messagebox, scrolledtext
import os
import re

# --- 設定 ---
EXCLUDE_FILES = ["header.html", "footer.html", "google224cc59b9c585584.html"]
# --------------------

def show_results(root, updated_files, failed_files):
    """処理結果を新しいウィンドウに表示する"""
    result_window = tk.Toplevel(root)
    result_window.title("処理結果")
    
    # 横方向（列 0, 1）は自動で広がるように設定
    result_window.grid_columnconfigure(0, weight=1)
    result_window.grid_columnconfigure(1, weight=1)
    
    # ★ 修正: 行 1（ScrolledTextがある行）のみが縦方向に広がるように設定 ★
    result_window.grid_rowconfigure(1, weight=1)
    # 行 0 (ラベル) と 行 2 (概要) は weight=0 (固定サイズ) のまま

    # --- 成功ファイル枠 ---
    tk.Label(result_window, text=f"✅ 成功ファイル ({len(updated_files)} 件):", font=('Arial', 10, 'bold')).grid(row=0, column=0, padx=10, pady=5, sticky="w")
    success_text = scrolledtext.ScrolledText(result_window, wrap="word", width=40, height=15)
    success_text.grid(row=1, column=0, padx=10, pady=5, sticky="nsew") # sticky="nsew" で全方向に拡大
    
    for f in updated_files:
        success_text.insert(tk.END, f"{f}\n")
    success_text.config(state=tk.DISABLED)

    # --- 失敗ファイル枠 ---
    tk.Label(result_window, text=f"⚠️ 失敗ファイル (パターン不一致) ({len(failed_files)} 件):", font=('Arial', 10, 'bold')).grid(row=0, column=1, padx=10, pady=5, sticky="w")
    failed_text = scrolledtext.ScrolledText(result_window, wrap="word", width=40, height=15)
    failed_text.grid(row=1, column=1, padx=10, pady=5, sticky="nsew") # sticky="nsew" で全方向に拡大
    
    for f in failed_files:
        failed_text.insert(tk.END, f"{f}\n")
    failed_text.config(state=tk.DISABLED)

    # --- 概要 ---
    tk.Label(result_window, text=f"合計処理ファイル数: {len(updated_files) + len(failed_files)} 件", anchor="w").grid(row=2, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="w")


def replace_in_files():
    """ファイルを検索・置換するメインロジック"""
    search_pattern = search_text.get("1.0", tk.END).strip()
    replace_text = replace_text_area.get("1.0", tk.END).strip()
    target_dir = os.path.dirname(os.path.abspath(__file__)) 

    if not search_pattern:
        messagebox.showerror("エラー", "検索文字列を入力してください。")
        return

    updated_files = []
    failed_files = []

    try:
        compiled_pattern = re.compile(search_pattern, re.DOTALL | re.IGNORECASE)
    except re.error as e:
        messagebox.showerror("エラー", f"正規表現の形式が正しくありません: {e}")
        return

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
            
            new_content, num_replacements = compiled_pattern.subn(replace_text, content)
            
            if num_replacements > 0:
                try:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    updated_files.append(filepath)
                except Exception:
                     failed_files.append(filepath + " (書き込みエラー)")
            else:
                failed_files.append(filepath)
    
    show_results(root, updated_files, failed_files)


# --- GUIのセットアップ ---
root = tk.Tk()
root.title("HTML一括置換ツール")

# ★ 修正: ウィンドウの列と行の設定 (縦横リサイズ対応) ★
root.grid_columnconfigure(0, weight=1) # 横方向 (Column 0) の拡大を許可
# 以下の行を追加: 検索文字列エリア (Row 1) と 置換文字列エリア (Row 3) の縦方向の拡大を許可
root.grid_rowconfigure(1, weight=1) 
root.grid_rowconfigure(3, weight=1) 

# 検索文字列のラベルと入力欄
tk.Label(root, text="検索文字列 (正規表現使用可能。例: (</head>))", anchor="w").grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
# sticky="ew" から "nsew" に変更し、四方に拡大するように指定
search_text = tk.Text(root, height=5, width=80)
search_text.grid(row=1, column=0, padx=10, pady=5, sticky="nsew") 

# 置換文字列のラベルと入力欄
tk.Label(root, text="置換文字列 (例: 共通部分のHTML\n\\1で元の</head>タグを再挿入)", anchor="w").grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")
# sticky="ew" から "nsew" に変更し、四方に拡大するように指定
replace_text_area = tk.Text(root, height=10, width=80)
replace_text_area.grid(row=3, column=0, padx=10, pady=5, sticky="nsew") 

# 注意事項
tk.Label(root, text=f"除外ファイル: {', '.join(EXCLUDE_FILES)}", fg="blue").grid(row=4, column=0, padx=10, pady=(5, 0), sticky="w")

# 実行ボタン (Row 5は固定サイズでOK)
tk.Button(root, text="実行 (全HTMLファイルを置換)", command=replace_in_files, bg="red", fg="white").grid(row=5, column=0, padx=10, pady=20)

root.mainloop()