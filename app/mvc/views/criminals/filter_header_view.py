from PySide6.QtWidgets import (QHeaderView, QLineEdit, QWidget, 
                             QHBoxLayout, QVBoxLayout, QApplication)
from PySide6.QtCore import Qt, Signal, QSize, QRect, QPoint, QEvent
from PySide6.QtGui import QPainter, QFontMetrics

class FilterHeaderView(QHeaderView):
    filterChanged = Signal(int, str)
    
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        
        self.filter_widgets = []
        self.filter_containers = []
        
        self.filter_visible = True
        
        self.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.setSectionsClickable(True)
        self.setSectionsMovable(True)
        self.setStretchLastSection(True)
        
        self.hover_section = -1
        self.setMouseTracking(True)
        
    def setFilterVisible(self, visible):
        self.filter_visible = visible
        
        for container in self.filter_containers:
            container.setVisible(visible)
            
        self.updateGeometries()
    
    def setModel(self, model):
        super().setModel(model)
        
        for widget in self.filter_widgets:
            widget.deleteLater()
        
        for container in self.filter_containers:
            container.deleteLater()
            
        self.filter_widgets = []
        self.filter_containers = []
        
        if model:
            for col in range(model.columnCount()):
                container = QWidget(self.parent())
                layout = QHBoxLayout(container)
                layout.setContentsMargins(0, 0, 0, 0)

                header_text = model.headerData(col, Qt.Horizontal)
                
                filter_widget = QLineEdit(container)
                filter_widget.setPlaceholderText("Фільтр...")
                
                filter_widget.textChanged.connect(lambda text, col=col: self.filterChanged.emit(col, text))
                
                layout.addWidget(filter_widget)
                
                self.filter_widgets.append(filter_widget)
                self.filter_containers.append(container)

                tooltip_text = "Фільтрувати за частковим збігом\n"
            
                # Date columns
                if "дата" in header_text.lower():
                    tooltip_text += "Діапазон (вводити роки): РРРР-ММ-ДД - РРРР-ММ-ДД\n"
                    tooltip_text += "Більше ніж: >РРРР-ММ-ДД\n"
                    tooltip_text += "Менше ніж: <РРРР-ММ-ДД"
                # Numeric columns
                elif any(word in header_text.lower() for word in ["зріст", "вага", "кількість"]):
                    tooltip_text += "Діапазон: число1 - число2\n"
                    tooltip_text += "Більше ніж: >число\n"
                    tooltip_text += "Менше ніж: <число"
                # Text columns
                else:
                    tooltip_text += "Діапазон (алфавітний): текст1 - текст2"
                    
                filter_widget.setToolTip(tooltip_text)
                
                self._updateFilterPosition(col)

                
    def sectionResized(self, logicalIndex, oldSize, newSize):
        """Handle section resize events."""
        super().sectionResized(logicalIndex, oldSize, newSize)
        
        for col in range(len(self.filter_widgets)):
            self._updateFilterPosition(col)
    
    def _updateFilterPosition(self, col):
        """Update the position of a filter widget."""
        if not self.filter_widgets or col >= len(self.filter_widgets) or not self.filter_visible:
            return
            
        section_rect = self.sectionViewportPosition(col)
        
        x = self.sectionViewportPosition(col)
        width = self.sectionSize(col)
        
        if col == len(self.filter_widgets) - 1 and self.stretchLastSection():
            width = max(width, self.width() - x)
        
        header_height = self.height() // 2 if self.filter_visible else self.height()
        
        self.filter_containers[col].setGeometry(
            x, header_height, 
            width, header_height
        )
        
        self.filter_containers[col].setVisible(self.filter_visible)
    
    def updateGeometries(self):
        """Update the header geometry including filter positions."""
        super().updateGeometries()
        
        if self.filter_widgets:
            for col in range(len(self.filter_widgets)):
                self._updateFilterPosition(col)
    
    def sectionSizeFromContents(self, logicalIndex):
        """Override to account for filter widgets in size calculation."""
        size = super().sectionSizeFromContents(logicalIndex)
        
        if self.filter_visible:
            size.setHeight(size.height() * 2)
            
        return size
    
    def sizeHint(self):
        """Override to provide a proper size hint for the header."""
        size = super().sizeHint()
        
        if self.filter_visible:
            size.setHeight(size.height() * 2)
            
        return size
    
    def filterText(self, column):
        """Get the filter text for a specific column."""
        if self.filter_widgets and 0 <= column < len(self.filter_widgets):
            return self.filter_widgets[column].text()
        return ""
    
    def clearFilters(self):
        """Clear all filter inputs."""
        if self.filter_widgets:
            for widget in self.filter_widgets:
                widget.clear()
    
    def eventFilter(self, obj, event):
        """Filter events for child widgets."""
        if event.type() == QEvent.Resize:
            self.updateGeometries()
        return super().eventFilter(obj, event)