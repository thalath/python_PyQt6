from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QMessageBox
import sys
from PyQt6.QtGui import QIcon

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Square Compute")
window.setWindowIcon(QIcon("idea.png"))
window.resize(300, 100)

num_input = QLineEdit()
num_input.setPlaceholderText("Enter a number")

get_label = QLabel("")
get_label.setStyleSheet(
    """
        font-family: Times New Roman, Battambang;
        font-size: 14px;
        color: red;
    """
)

def compute_square():
    try:
        num = int(num_input.text())
        get_label.setText(f"Square = {num * num}")
        
    except ValueError:
        QMessageBox.warning(get_label, "អ្នកបញ្ចូលខុសហើយ", "Please input valid integer into the box")

button = QPushButton("Compute_square")
button.setStyleSheet(
    """
        font-family: Times New Roman;
        font-weight: 500;
    """
)
button.clicked.connect(compute_square)

layout = QVBoxLayout()
layout.addWidget(num_input)
layout.addWidget(button)
layout.addWidget(get_label)

window.setLayout(layout)
window.show()
sys.exit(app.exec())
