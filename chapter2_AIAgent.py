import sys
from PyQt6.QtWidgets import (
    QApplication, QLabel, QTextEdit, QSlider, QGroupBox, QHBoxLayout, QVBoxLayout,
    QWidget, QPushButton
)
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt

class SimpleAgent:
    """A very basic rule-based Agent AI"""
    def decision(self, environment):
        price = environment["price"]
        if price > 70:
            return "sell"
        elif price < 30:
            return "Buy"
        else:
            return "Wait"

class SimulatorAgent(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Agent Simulator")
        self.setWindowIcon(QIcon("idea.png"))
        self.setGeometry(500, 200, 400, 450)
        
        self.setStyleSheet(
        """
            QPushButton{
                color: black;
                font-family: Times New Roman;
                background-color: powderblue;
                width: 70px;
                height: 20px;
            }
            QPushButton:hover{
                background-color: darkblue;
            }
        """
        )
        
        self.agent = SimpleAgent()
        self.environment = {"price": 50}
        
        self.create_widgets()
        self.create_layouts()

        
    def create_widgets(self):
        self.price_label = QLabel(f"Price: {self.environment['price']}")
        self.price_label.setStyleSheet(
        """
            font-family: Times New Roman;
            font-weight: 700;
            
        """
        )
        self.price_slider = QSlider(Qt.Orientation.Horizontal)
        self.price_slider.setRange(0, 100)
        self.price_slider.setValue(self.environment['price'])
        self.price_slider.valueChanged.connect(self.update_price)
        
        self.buy_btn = QPushButton("Buy")
        self.sell_btn = QPushButton("Sell")
        self.wait_btn = QPushButton("Wait")
        self.sell_btn.clicked.connect(lambda: self.manual_action("Sell"))
        self.buy_btn.clicked.connect(lambda: self.manual_action("Buy"))
        self.wait_btn.clicked.connect(lambda: self.manual_action("Wait"))
        
        self.auto_decided = QPushButton("Auto Decision")
        self.auto_decided.clicked.connect(self.agent_decision)

        self.group_box = QGroupBox("Trigger Agent")
        self.group_box.setStyleSheet(
        """
            font-family: Times New Roman;
            border: 1px solid green;
            border-radius: 10px;
            padding: 10px;
        """
        )
        
        self.result = QTextEdit()
        self.result.setStyleSheet(
        """
            font-family: Times New Roman;
            font-weight: 500;
            color: blue;
        """
        )
        self.result.setReadOnly(True)

        


    def create_layouts(self):
        layout = QVBoxLayout()
        M_layout = QHBoxLayout()
        
        header_text = QLabel("Environment Controls")
        header_text.setFont(QFont("Times New Roman", 11, QFont.Weight.Medium))
        
        layout.addWidget(header_text)
        layout.addWidget(self.price_label)
        layout.addWidget(self.price_slider)
        
        M_layout.addWidget(self.sell_btn)
        M_layout.addWidget(self.buy_btn)
        M_layout.addWidget(self.wait_btn)
        
        self.group_box.setLayout(M_layout)
        layout.addWidget(self.group_box)
        layout.addWidget(self.auto_decided)
        layout.addWidget(self.result)
        self.setLayout(layout)
    
    def update_price(self, value):
        self.environment['price'] = value
        self.price_label.setText(f"Price: {value}")
    
    def manual_action(self, action):
        self.result.append(f"👸🏽 Manual Decision Triggered: {self.environment['price']}: {action}")
        
    def agent_decision(self):
        decision = self.agent.decision(self.environment)
        self.result.append(f"👽 Agent decision depended on price: {self.environment['price']}: {decision}")
    
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimulatorAgent()
    window.show()
    sys.exit(app.exec())
        