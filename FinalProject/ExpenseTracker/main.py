# Add dependencies
import datetime
import sys
import sqlite3
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QAction, QPainter
from PySide6.QtWidgets import (QApplication, QHeaderView, QHBoxLayout, QLabel, QLineEdit,
                               QMainWindow, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout,
                               QWidget, QCalendarWidget)
from PySide6.QtCharts import QChartView, QPieSeries, QChart


class Widget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.items = 0
        # Dummy Data
        self._data = {1: ["Water", 'Food', "20/02/2024", 20], 2: ["Rent", "Rent", '01/02/2024', 1000],
                      3: ["Coffee", "Food", '10/02/2024', 30]}

        # Left Widget
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Description", "Category", "Date", "Price"])
        # noinspection PyUnresolvedReferences
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Chart
        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        # Right Widget
        self.description = QLineEdit()
        self.category = QLineEdit()
        self.date = QCalendarWidget()
        self.price = QLineEdit()
        self.add = QPushButton("Add")
        self.clear = QPushButton("Clear")
        self.quit = QPushButton("Quit")
        self.plot = QPushButton("Plot")

        # Disabling 'Add' button
        self.add.setEnabled(False)

        self.right = QVBoxLayout()
        self.right.addWidget(QLabel("Description"))
        self.right.addWidget(self.description)
        self.right.addWidget(QLabel("Category"))
        self.right.addWidget(self.category)
        self.right.addWidget(QLabel("Date"))
        self.right.addWidget(self.date)
        self.right.addWidget(QLabel("Price"))
        self.right.addWidget(self.price)
        self.right.addWidget(self.add)
        self.right.addWidget(self.plot)
        self.right.addWidget(self.chart_view)
        self.right.addWidget(self.clear)
        self.right.addWidget(self.quit)

        # QWidget Layout
        self.layout = QHBoxLayout()

        # self.table_view.setSizePolicy(size)
        self.layout.addWidget(self.table)
        self.layout.addLayout(self.right)

        # Set the layout to the QWidget
        self.setLayout(self.layout)

        # Signals and Slots
        self.add.clicked.connect(self.add_element)
        self.quit.clicked.connect(self.quit_application)
        self.plot.clicked.connect(self.plot_data)
        self.clear.clicked.connect(self.clear_table)
        self.description.textChanged[str].connect(self.check_disable)
        self.category.textChanged[str].connect(self.check_disable)
        self.price.textChanged[str].connect(self.check_disable)

        # Fill example data
        self.fill_table()

    @Slot()
    def add_element(self):
        des = self.description.text()
        cat = self.category.text()
        date = self.date.selectedDate().getDate()
        date_str = datetime.date(date[0],date[1],date[2]).strftime("%x")
        price = self.price.text()

        try:
            price_item = QTableWidgetItem(f"{float(price):.2f}")
            price_item.setTextAlignment(Qt.AlignRight)

            self.table.insertRow(self.items)
            description_item = QTableWidgetItem(des)
            category_item = QTableWidgetItem(cat)
            date_item = QTableWidgetItem(date_str)

            self.table.setItem(self.items, 0, description_item)
            self.table.setItem(self.items, 1, category_item)
            self.table.setItem(self.items, 2, date_item)
            self.table.setItem(self.items, 3, price_item)

            self.description.setText("")
            self.category.setText("")
            self.price.setText("")

            self.items += 1
        except ValueError:
            print("That is an invalid input:", price, "Make sure to enter a price!")

    @Slot()
    def check_disable(self, x):
        if not self.description.text() or not self.price.text():
            self.add.setEnabled(False)
        else:
            self.add.setEnabled(True)

    @Slot()
    def plot_data(self):
        # Get table information
        series = QPieSeries()
        for i in range(self.table.rowCount()):
            text = self.table.item(i, 0).text()
            number = float(self.table.item(i, 3).text())
            series.append(text, number)

        chart = QChart()
        chart.addSeries(series)
        chart.legend().setAlignment(Qt.AlignLeft)
        self.chart_view.setChart(chart)

    @Slot()
    def quit_application(self):
        QApplication.quit()

    def fill_table(self, data=None):
        data = self._data if not data else data
        for no, item in data.items():
            description_item = QTableWidgetItem(item[0])
            cat_item = QTableWidgetItem(item[1])
            date_item = QTableWidgetItem(item[2])
            price_item = QTableWidgetItem(f"{item[3]:.2f}")
            price_item.setTextAlignment(Qt.AlignRight)
            self.table.insertRow(self.items)
            self.table.setItem(self.items, 0, description_item)
            self.table.setItem(self.items, 1, cat_item)
            self.table.setItem(self.items, 2, date_item)
            self.table.setItem(self.items, 3, price_item)
            self.items += 1

    @Slot()
    def clear_table(self):
        self.table.setRowCount(0)
        self.items = 0
        self.print_history()

    def print_history(self, data):
        date_from = datetime.date(2023, 12, 1)
        print("Date from:", date_from)
        date_to = datetime.date(2024, 3, 1)
        print("Date to: ", date_to)
        for no, item in data.items():
            date = item[2].split('/')
            date_item = datetime.date(int(date[2]), int(date[1]), int(date[0]))
            print(date_item)
            if date_from < date_item < date_to:
                print(item)


class MainWindow(QMainWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setWindowTitle("Expense Tracker")

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        # Exit QAction
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.exit_app)

        self.file_menu.addAction(exit_action)
        self.setCentralWidget(widget)

    @Slot()
    def exit_app(self):
        QApplication.quit()


if __name__ == "__main__":
    # Qt Application
    app = QApplication(sys.argv)
    # QWidget
    widget = Widget()
    # QMainWindow using QWidget as central widget
    window = MainWindow(widget)
    window.resize(800, 600)
    window.show()

    # Execute application
    sys.exit(app.exec())
