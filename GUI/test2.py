import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit
from pygments import highlight
from pygments.lexers import CLexer
from pygments.formatters import HtmlFormatter


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)

        # 设置窗口标题
        self.setWindowTitle('C Language Syntax Highlighter with Pygments')
        self.resize(800, 600)

        # 示例 C 语言代码
        sample_code = '''#include <stdio.h>

int add(int a, int b) {
    return a + b;
}

int main() {
    int x = 5, y = 10;

    printf("x + y = %d\\n", add(x, y));

    if (x > y) {
        printf("x is greater than y\\n");
    } else {
        printf("x is less than or equal to y\\n");
    }

    for (int i = 0; i < 5; i++) {
        printf("i = %d\\n", i);
    }

    return 0;
}
'''

        # 使用 pygments 高亮 C 语言代码
        self.highlight_code(sample_code)

    def highlight_code(self, code):
        # 使用 pygments 对代码进行高亮
        formatter = HtmlFormatter(style='monokai', full=True, cssclass='pygments')
        highlighted_code = highlight(code, CLexer(), formatter)

        # 提取 pygments 的 CSS 样式
        css_style = formatter.get_style_defs('.pygments')

        # 将 CSS 样式嵌入到 HTML 内容中
        highlighted_code_with_css = f"<style>{css_style}</style>{highlighted_code}"

        # 将高亮后的 HTML 内容插入到 QTextEdit 中
        self.text_edit.setHtml(highlighted_code_with_css)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
