from PyQt6.QtWidgets import QTableWidget, QHeaderView
from PyQt6.QtCore import Qt

class SortableTableWidget(QTableWidget):
    def __init__(self):
        super().__init__()

        # Connect the header clicked signal to the sorting function
        self.horizontalHeader().sectionClicked.connect(self.sort_column)
        self.last_sorted_column = None
        self.sort_order = Qt.SortOrder.AscendingOrder

        # Set resize mode to allow manual adjustment
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)

    def resizeEvent(self, event):
        # After the widget is resized, trigger automatic resizing
        super().resizeEvent(event)
        self.resize_columns_to_contents()

    def resize_columns_to_contents(self):
        for column in range(self.columnCount()):
            self.resizeColumnToContents(column)

    def sort_column(self, logical_index):
        # If the same column header is clicked, toggle the sort order
        if logical_index == self.last_sorted_column:
            self.sort_order = Qt.SortOrder.DescendingOrder if self.sort_order == Qt.SortOrder.AscendingOrder else Qt.SortOrder.AscendingOrder
        else:
            self.last_sorted_column = logical_index
            self.sort_order = Qt.SortOrder.AscendingOrder

        # Sort the table by the clicked column
        self.sortByColumn(logical_index, self.sort_order)
