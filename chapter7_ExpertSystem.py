import sys
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QTextEdit,
    QLabel, QTabWidget, QDialog, QFormLayout, QComboBox, QMessageBox,
    QHeaderView, QCheckBox, QSpinBox, QGroupBox, QScrollArea
)

from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


class TroubleshootingRule:
    """Represents a troubleshooting rule with symptoms and solutions"""
    def __init__(self, rule_id: str, title: str, description: str, 
                 symptoms: List[str], solution: str, category: str, 
                 priority: int = 1, confidence: float = 0.8):
        self.rule_id = rule_id
        self.title = title
        self.description = description
        self.symptoms = symptoms # List of required symptoms
        self.solution = solution
        self.category = category
        self.priority = priority
        self.confidence = confidence
        self.create_date = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'rule_id': self.rule_id,
            'title': self.title,
            'description': self.description,
            'symptoms': self.symptoms,
            'solution': self.solution,
            'category': self.category,
            'priority': self.priority,
            'confidence': self.confidence,
            'create_date': self.create_date
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TroubleshootingRule':
        rule = cls(
            data['rule_id'], data['title'], data['description'],
            data['symptoms'], data['solution'], data['category'],
            data.get('priority', 1), data.get('confidence', 0.8)
        )
        rule.create_date = data.get('create_date', datetime.now().isoformat())
        return rule
    
    
class TroubleshootingCase:
    """Represents a troubleshooting case/section"""
    def __init__(self, case_id: str, symptoms: List[str],
                 diagnosis: str = "", solutions: List[str] = None):
        self.case_id = case_id
        self.symptoms = symptoms
        self.diagnosis = diagnosis
        self.solutions = solutions or []
        self.create_date = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'case_id': self.case_id,
            'symptoms': self.symptoms,
            'diagnosis': self.diagnosis,
            'solutions': self.solutions,
            'create_date': self.create_date
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TroubleshootingCase':
        case = cls(
            data['case_id'], data['symptoms'], data.get('diagnosis', ''), data.get('solutions', [])
        )
        case.create_date = data.get('create_date', datetime.now().isoformat())
        return case
    

class DataManager:
    """Handles all CRUD operations and JSON persistence"""
    def __init__(self, filename: str = "expert_system_data.json"):
        self.filename = filename
        self.rules: Dict[TroubleshootingRule] = {}
        self.cases: Dict[TroubleshootingCase] = {}
        self.symptoms_list = set()
        self.load_data()
    
    def load_data(self):
        """Load dat from JSON file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Load rules
                for rule_data in data.get('rules', []):
                    rule = TroubleshootingRule.from_dict(rule_data)
                    self.rules[rule.rule_id] = rule
                    self.symptoms_list.update(rule.symptoms)

                # Load cases
                for case_data in data.get('cases', []):
                    case = TroubleshootingCase.from_dict(case_data)
                    self.cases[case.case_id] = case
            except Exception as e:
                print(f"Error Loading data: {e}")
                self.create_sample_data()
        else:
            self.create_sample_data()
    
    def save_data(self):
        """Save data to JSON file"""
        data = {
            'rules': [rule.to_dict() for rule in self.rules.values()],
            'cases': [case.to_dict() for case in self.cases.values()],
            'symptoms': list(self.symptoms_list)
        }
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving data{e}")
    
    def create_sample_data(self):
        """Create sample troubleshooting rules and data"""
        sample_rules = [
            TroubleshootingRule(
                "RULE001", "Computer Won't Start",
                "Computer doesn't power on at all",
                ["No power light", "No fan noise", "Screen blank"],
                "1. Check power cable connection\n2. Verify power outlet works\n3. Check power supply switch\n4. Test with different power cable",
                "Hardware", 1, 0.9
            ),
            TroubleshootingRule(
                "RULE002", "Blue screen of death",
                "Computer crashes woth blue screen error",
                ["Blue screen", "Automatic restart", "error code"],
                "1. Note error code\n2. Check recent software/hardware changes\n3. Run memory diagnostic\n4. Update drivers\n5. Check for overheating",
                "Software", 2, 0.85
            ),
            TroubleshootingRule(
                "RULE003", "Slow Performance",
                "Computer runs very slowly ",
                ["Slow boot time", "Programs lag", "High CPU usage"],
                "1. Run Antivirus scan\n2. Check startuo programs\n3. Clean temperary files\n4. Add more RAM if needed\n5. Defragment haed drive",
                "Performance", 1, 0.8
            ),
            TroubleshootingRule(
                "RULE004", "Internet Connection issues",
                "Cannot connect to internet",
                ["No Internet access", "Connection timeout", "DNS errors"],
                "1. Check cable connections\n2. Restart router/modern\n3. Run network troubleshooter\n4. Update network drivers\n5. Restart network settings",
                "Network", 1, 0.85
            ),
            TroubleshootingRule(
                "RULE005", "Overheating issues",
                "Computer gets too hot and shuts down",
                ["Computer hot to touch", "Automatic shutdown", "Fan noise loud"],
                "1. Clean dust from vents and fans\n2. Check therminal paste\n3. Ensure proper ventilation\n4. Check fan functionality\n5. Reduce CPU load",
                "Hardware", 2, 0.9
            )
        ]
        
        for rule in sample_rules:
            self.rules[rule.rule_id] = rule
            self.symptoms_list.update(rule.symptoms)

        self.save_data()
    
    # CRUD Operations for rules
    def create_rule(self, rule: TroubleshootingRule) -> bool:
        if rule.rule_id not in self.rules:
            self.rules[rule.rule_id] = rule
            self.symptoms_list.update(rule.symptoms)
            self.save_data()
            return True
        return False
    
    def read_rule(self, rule_id: str) -> Optional[TroubleshootingRule]:
        return self.rules.get(rule_id)
    
    def read_all_rules(self) -> List[TroubleshootingRule]:
        return list(self.rules.values())
    
    def update_rule(self, rule: TroubleshootingRule) -> bool:
        if rule.rule_id in self.rules:
            old_symptoms = self.rules[rule.rule_id].symptoms
            self.rules[rule.rule_id] = rule
            # Update symptoms
            for symptom in old_symptoms:
                if not any(symptom in r.symptoms for r in self.rules.values() if r.rule_id != rule.rule_id):
                    self.symptoms_list.discard(symptom)
            self.symptoms_list.update(rule.symptoms)
            self.save_data()
            return True
        return False
    
    def delete_rule(self, rule_id: str) -> bool:
        if rule_id in self.rules:
            old_symptoms = self.rules[rule_id].symptoms
            del self.rules[rule_id]
            # Clean up symptoms that are no longer used
            for symptom in old_symptoms:
                if not any(symptom in rule.symptoms for rule in self.rules.values()):
                    self.symptoms_list.discard(symptom)
                self.save_data()
                return True
            return False
    
    # CRUD Operaions for Cases
    def create_case(self, case: TroubleshootingCase) -> bool:
        if case.case_id not in self.cases:
            self.cases[case.case_id] = case
            self.save_data()
            return True
        return False
    
    def read_case(self, case_id: str) -> Optional[TroubleshootingCase]:
        return self.cases.get(case_id)

    def read_all_cases(self) -> List[TroubleshootingCase]:
        return list(self.cases.values())
    
    def update_case(self, case: TroubleshootingCase) -> bool:
        if case.case_id in self.cases:
            self.cases[case.case_id] = case
            self.save_data()
            return True
        return False
    
    def delete_case(self, case_id: str) -> bool:
        if case_id in self.cases:
            del self.cases[case_id]
            self.save_data()
            return True
        return False
    
    def get_all_symptoms(self) -> List[str]:
        return sorted(list(self.symptoms_list))


class InferenceEngine:
    """Simple forward-chaining inference engine"""
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
    
    def diagnose(self, selected_symptoms: List[str]) -> List[tuple]:
        """Returns kust of (rulem confidence_score) tules"""
        matches = []
        rules = self.data_manager.read_all_rules()

        for rule in rules:
            matched_symptoms = 0
            for symptom in rule.symptoms:
                if any(s.lower() in symptom.lower() or symptom.lower() in s.lower() for s in selected_symptoms):
                    matched_symptoms += 1
            
            if matched_symptoms > 0:
                # Calculate confidence based on symptom match ratio
                match_ratio = matched_symptoms / len(rule.symptoms)
                confidence = rule.confidence * match_ratio
                matches.append((rule, confidence))

        # Sort by confidence and priority
        matches.sort(key=lambda x: (x[1], x[0].priority), reverse=True)
        return matches[:5] # Return to[ 5 matches]
    
    
class RuleDialog(QDialog):
    """Dialog for creating/editting rules"""
    def __init__(self, parent=None, rule: TroubleshootingRule = None, symptoms_list: List[str] = None):
        super().__init__(parent)
        self.rule = rule
        self.symptoms_list = symptoms_list or []
        self.setWindowTitle("Add/Edit Rule")
        self.setModal(True)
        self.resize(500, 600)
        self.setup_ui()
        if rule:
            self.populate_fields()
    
    def setup_ui(self):
        layout =QVBoxLayout()

        # Form fields
        form_layout = QFormLayout()

        self.rule_id_edit = QLineEdit()
        self.title_edit = QLineEdit()
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(80)

        self.category_combo = QComboBox()
        self.category_combo.addItems(["Hardware", "Sotfware", "Network", "Performance", "Security"])

        self.priority_spin = QSpinBox()
        self.priority_spin.setRange(1, 5)
        self.priority_spin.setValue(1)
        
        self.confidence_spin = QSpinBox()
        self.confidence_spin.setRange(1, 100)
        self.confidence_spin.setValue(80)
        self.confidence_spin.setSuffix("%")

        form_layout.addRow("Rule ID:", self.rule_id_edit)
        form_layout.addRow("Title", self.title_edit)
        form_layout.addRow("Description:", self.description_edit)
        form_layout.addRow("Category:", self.category_combo)
        form_layout.addRow("Priority:", self.priority_spin)
        form_layout.addRow("Confidence:", self.confidence_spin)

        layout.addLayout(form_layout)
        
        # Symptoms section
        symptoms_group = QGroupBox("Symptoms (check all that apply)")
        symptoms_layout = QVBoxLayout()

        # Add new Symptoms
        add_symptom_layout = QHBoxLayout()
        self.new_symptom_edit = QLineEdit()
        self.new_symptom_edit.setPlaceholderText("Enter new symptoms...")
        add_symptom_btn = QPushButton("Add Symptom")
        add_symptom_btn.clicked.connect(self.add_new_symptoms)
        add_symptom_layout.addWidget(self.new_symptom_edit)
        add_symptom_layout.addWidget(add_symptom_btn)
        symptoms_layout.addLayout(add_symptom_layout)

        # Symptoms checkboxes
        self.symptoms_area = QScrollArea()
        self.symptoms_widget = QWidget()
        self.symptoms_checkboxes_layout = QVBoxLayout(self.symptoms_widget)
        self.symptoms_area.setWidget(self.symptoms_widget)
        self.symptoms_area.setWidgetResizable(True)
        self.symptoms_area.setMaximumHeight(200)

        self.symptom_checkboxes = {}
        self.update_symptoms_checkboxes()

        symptoms_layout.addWidget(self.symptoms_area)
        symptoms_group.setLayout(symptoms_layout)
        layout.addWidget(symptoms_group)

        # Solution
        layout.addWidget(QLabel("Solution:"))
        self.solution_edit = QTextEdit()
        self.solution_edit.setMaximumHeight(100)
        layout.addWidget(self.solution_edit)

        # Buttons
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")
        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)
    
    def add_new_symptoms(self):
        new_symptom = self.new_symptom_edit.text().strip()
        if new_symptom and new_symptom not in self.symptoms_list:
            self.symptoms_list.append(new_symptom)
            self.update_symptoms_checkboxes()
            self.new_symptom_edit.clear()
    
    def update_symptoms_checkboxes(self):
        # Clear existing checkboxes
        for checkbox in self.symptom_checkboxes.values():
            checkbox.setParent(None)
        self.symptom_checkboxes.clear()

        # Create new checkboxes
        for symptom in sorted(self.symptoms_list):
            checkbox = QCheckBox(symptom)
            self.symptom_checkboxes[symptom] = checkbox
            self.symptoms_checkboxes_layout.addWidget(checkbox)
    
    def populate_fields(self):
        self.rule_id_edit.setText(self.rule.rule_id)
        self.rule_id_edit.setReadOnly(True)
        self.title_edit.setText(self.rule.title)
        self.description_edit.setPlainText(self.rule.description)
        self.category_combo.setCurrentText(self.rule.category)
        self.priority_spin.setValue(self.rule.priority)
        self.confidence_spin.setValue(int(self.rule.confidence * 100))
        self.solution_edit.setPlainText(self.rule.solution)

        # Check relecant symptoms
        for symptom in self.rule.symptoms:
            if symptom in self.symptom_checkboxes:
                self.symptom_checkboxes[symptom].setChecked(True)
    
    def get_rule_data(self) -> TroubleshootingRule:
        selected_symptoms = [symptom for symptom, checkbox in self.symptom_checkboxes.items() if checkbox.isChecked()]


        return TroubleshootingRule(
            self.rule_id_edit.text(),
            self.title_edit.text(),
            self.description_edit.toPlainText(),
            selected_symptoms,
            self.solution_edit.toPlainText(),
            self.category_combo.currentText(),
            self.priority_spin.value(),
            self.confidence_spin.value() / 100.0
        )
    
class ExpertSystemApp(QMainWindow):
    """Main application window"""
    def __init__(self):
        super().__init__()
        self.data_manager = DataManager()
        self.inference_engine = InferenceEngine(self.data_manager)

        self.setWindowTitle("Computer Troubleshooting Expert System")
        self.setGeometry(100, 100, 1000, 700)
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Title
        title = QLabel("Computer Troubleshooting Expert System")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setBold(True)
        font.setPointSize(16)
        title.setFont(font)
        layout.addWidget(title)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        #Create tabs
        self.create_diagnosis_tab()
        self.create_rules_tab()
        self.create_cases_tab()
    
    def create_diagnosis_tab(self):
        """Create the main diagnosis interface"""
        tab = QWidget()
        layout = QVBoxLayout()

        
        # Instructions
        instructions = QLabel("Select symptoms you're experiencing:")
        instructions.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        layout.addWidget(instructions)

        # Symptoms selection
        self.symptoms_area = QScrollArea()
        self.symptoms_widget = QWidget()
        self.symptoms_layout = QVBoxLayout(self.symptoms_widget)
        self.symptoms_area.setWidget(self.symptoms_widget)
        self.symptoms_area.setWidgetResizable(True)
        self.symptoms_area.setMaximumHeight(200)
        layout.addWidget(self.symptoms_area)

        # Diagnosis button
        diagnose_btn = QPushButton("Diagnose Problem")
        diagnose_btn.clicked.connect(self.run_diagnosis)
        layout.addWidget(diagnose_btn)
        
        # Results area
        layout.addWidget(QLabel("Diagnosis Results:"))
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        layout.addWidget(self.results_text)

        tab.setLayout(layout)
        self.tab_widget.addTab(tab, "Diagnosis")
    
    def create_rules_tab(self):
        """Create rules managerment interface"""
        tab = QWidget()
        layout = QVBoxLayout()

        # Controls
        controls_layout = QHBoxLayout()
        add_btn = QPushButton("Add Rule")
        edit_btn = QPushButton("Edit Rule")
        delete_btn = QPushButton("Delete Rule")
        refresh_btn = QPushButton("Refresh")

        add_btn.clicked.connect(self.add_rule)
        edit_btn.clicked.connect(self.edit_rule)
        delete_btn.clicked.connect(self.delete_rule)
        refresh_btn.clicked.connect(self.load_rules_table)

        controls_layout.addWidget(add_btn)
        controls_layout.addWidget(edit_btn)
        controls_layout.addWidget(delete_btn)
        controls_layout.addWidget(refresh_btn)
        controls_layout.addStretch()
        layout.addLayout(controls_layout)

        # Rules table
        self.rules_table = QTableWidget()
        self.rules_table.setColumnCount(6)
        self.rules_table.setHorizontalHeaderLabels([
            "Rule ID", "Tilte", "Category", "Priority", "Confidence", "Symptoms Count"
        ])
        header = self.rules_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.rules_table)

        tab.setLayout(layout)
        self.tab_widget.addTab(tab, "Rules Management")
    
    def create_cases_tab(self):
        """Create cases managerment interface"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Controls
        controls_layout = QHBoxLayout()
        save_case_btn = QPushButton("Save Current Diagnosis as Case")
        delete_case_btn = QPushButton("Delete Case")
        refresh_cases_btn = QPushButton("Refress")

        save_case_btn.clicked.connect(self.save_current_case)
        delete_case_btn.clicked.connect(self.delete_case)
        refresh_cases_btn.clicked.connect(self.load_cases_table)

        controls_layout.addWidget(save_case_btn)
        controls_layout.addWidget(delete_case_btn)
        controls_layout.addWidget(refresh_cases_btn)
        controls_layout.addStretch()
        layout.addLayout(controls_layout)

        # Case table
        self.cases_table = QTableWidget()
        self.cases_table.setColumnCount(4)
        self.cases_table.setHorizontalHeaderLabels([
            "Case ID", "Symptoms Count", "Diagnosis", "Date"
        ])
        header = self.cases_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.cases_table)
        
        tab.setLayout(layout)   
        self.tab_widget.addTab(tab, "Cases History")
    
    def load_data(self):
        """Load all data into interfance"""
        self.load_symptoms_checkboxes()
        self.load_rules_table()
        self.load_cases_table()
    
    def load_symptoms_checkboxes(self):
        """Load symptoms as checkboxes"""
        # Clear existing
        for i in reversed(range(self.symptoms_layout.count())):
            self.symptoms_layout.itemAt(i).widget().setParent(None)

        # Add checkboxes for each symptom
        symptoms = self.data_manager.get_all_symptoms()
        self.symptom_checkboxes = {}

        for symptom in symptoms:
            checkbox = QCheckBox(symptom)
            self.symptom_checkboxes[symptom] = checkbox
            self.symptoms_layout.addWidget(checkbox)
        
    def load_rules_table(self):
        """Load rules into the table"""
        rules = self.data_manager.read_all_rules()
        self.rules_table.setRowCount(len(rules))

        for row, rule in enumerate(rules):
            self.rules_table.setItem(row, 0, QTableWidgetItem(rule.rule_id))
            self.rules_table.setItem(row, 1, QTableWidgetItem(rule.title))
            self.rules_table.setItem(row, 2, QTableWidgetItem(rule.category))
            self.rules_table.setItem(row, 3, QTableWidgetItem(str(rule.priority)))
            self.rules_table.setItem(row, 4, QTableWidgetItem(f"{rule.confidence:.0%}"))
            self.rules_table.setItem(row, 5, QTableWidgetItem(str(len(rule.symptoms))))
        
    def load_cases_table(self):
        """Load cases into the table"""
        cases = self.data_manager.read_all_cases()
        self.cases_table.setRowCount(len(cases))

        for row, case in enumerate(cases):
            self.cases_table.setItem(row, 0, QTableWidgetItem(case.case_id))
            self.cases_table.setItem(row, 1, QTableWidgetItem(str(len(case.symptoms))))
            self.cases_table.setItem(row, 2, QTableWidgetItem(case.diagnosis[:50] + "..." if len(case.diagnosis) > 50 else case.diagnosis))
            self.cases_table.setItem(row, 3, QTableWidgetItem(case.create_date[:10]))

    def run_diagnosis(self):
        """Run the expert system diagnosis"""
        selected_symptoms = [symptom for symptom, checkbox in self.symptom_checkboxes.items() if checkbox.isChecked()]


        if not selected_symptoms:
            QMessageBox.warning(self, "Warning", "Please select at least one symptom.")
            return

        matches = self.inference_engine.diagnose(selected_symptoms)

        if matches:
            result_text = "Based on the symptoms, here are the most likely problem\n\n"
            for i, (rule, confidence) in enumerate(matches, 1):
                result_text += f"{i}. {rule.title} (Confidence: {confidence:.0%})\n"
                result_text += f"   Category: {rule.category}\n"
                result_text += f"   Solution:\n{rule.solution}\n\n"
        else:
            result_text = "No matching problems found. Please check if you've selected the correct symptoms or contact technical support."

        self.results_text.setPlainText(result_text)
        self.current_diagnosis = result_text
        self.current_symptoms = selected_symptoms

    def add_rule(self):
        """Add a new rule"""
        dialog = RuleDialog(self, symptoms_list=self.data_manager.get_all_symptoms())
        if dialog.exec() == QDialog.DialogCode.Accepted:
            rule = dialog.get_rule_data()
            if self.data_manager.create_rule(rule):
                self.load_data()
                QMessageBox.information(self, "Success", "Rule added successfully!")
            else:
                QMessageBox.warning(self, "Error", "Rule ID already exist exist!")

    def edit_rule(self):
        """Edit selected rule"""
        current_row = self.rules_table.currentRow()
        if current_row >= 0:
            rule_id = self.rules_table.item(current_row, 0).text()
            rule = self.data_manager.read_rule(rule_id)
            if rule:
                dialog = RuleDialog(self, rule, self.data_manager.get_all_symptoms())
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    update_rule = dialog.get_rule_data()
                    self.data_manager.update_rule(update_rule)
                    self.load_data()
                    QMessageBox.information(self, "Success", "Rule updated successfully!")

    def delete_rule(self):
        """Delete selected rule"""
        current_row = self.rules_table.currentRow()
        if current_row >= 0:
            rule_id = self.rules_table.item(current_row, 0).text()
            reply = QMessageBox.question(self, "Confirm", f"Delete rule {rule_id}?")
            if reply == QMessageBox.StandardButton.Yes:
                self.data_manager.delete_rule(rule_id)
                self.load_data()
                QMessageBox.information(self, "Success", "Rule deleted successfully!")
        
    def save_current_case(self):
        """Save current diagnosis as a case"""
        if hasattr(self, 'current_symptoms') and hasattr(self, 'current_diagnosis'):
            case_id = f"CASE_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            case = TroubleshootingCase(case_id, self.current_symptoms, self.current_diagnosis)
            self.data_manager.create_case(case)
            self.load_cases_table()
            QMessageBox.information(self, "Success", f"Case saved as {case_id}?")
        else:
            QMessageBox.warning(self, "Warning", "No diagnosis to save. Please run a diagnosis first.")

    def delete_case(self):
        """Delete selected case"""
        current_row = self.cases_table.currentRow()
        if current_row >= 0:
            case_id = self.cases_table.item(current_row, 0).text()
            reply = QMessageBox.question(self, "Confirm", f"Delete case {case_id}?")
            if reply == QMessageBox.StandardButton.Yes:
                self.data_manager.delete_case(case_id)
                self.load_cases_table()
                QMessageBox.information(self, "Success", "Case deleted successfully!")

        
def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Computer troubleshooting Expert System")

    window = ExpertSystemApp()
    window.show()
    
    sys.exit(app.exec())
    
if __name__ == "__main__":
    main()
