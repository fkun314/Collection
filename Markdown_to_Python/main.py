# pip install markdown

# python main.py hoge.md

import sys
import markdown

# 変換するMarkdownファイルを指定
inpuot_file = sys.argv[1]

# Markdownファイルを読み込む
with open(inpuot_file, 'r', encoding='utf8') as f:
    text = f.read()

# MarkdownをHTMLに変換
html = markdown.markdown(text)

# HTMLファイルを出力
output_file = inpuot_file.split('.')[0] + '.html'

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html)
    