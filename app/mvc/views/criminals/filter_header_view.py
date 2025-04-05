from PySide6.QtWidgets import (QHeaderView, QLineEdit, QWidget, 
                             QHBoxLayout, QVBoxLayout, QApplication)
from PySide6.QtCore import Qt, Signal, QSize, QRect, QPoint, QEvent
from PySide6.QtGui import QPainter, QFontMetrics

class FilterHeaderView(QHeaderView):
    """
    A custom header view that places filter widgets in the header.
    """
    filterChanged = Signal(int, str)
    
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        
        self.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.setSectionsClickable(True)
        
        self.filter_widgets = []
        self.filter_containers = []
        
        # Configure section resize behaviors
        self.setSectionsMovable(True)
        self.setStretchLastSection(True)
        
        # Set up initial state
        self.filter_visible = True
        
        # Track when the mouse is over the header section (for hover effects)
        self.hover_section = -1
        self.setMouseTracking(True)
        
    def setFilterVisible(self, visible):
        """Show or hide the filter row."""
        self.filter_visible = visible
        
        # Show/hide all filter widgets
        for container in self.filter_containers:
            container.setVisible(visible)
            
        # Update section sizes
        self.updateGeometries()
    
    def setModel(self, model):
        """Override to create filter widgets when model is set."""
        super().setModel(model)
        
        # Clear existing filters
        for widget in self.filter_widgets:
            widget.deleteLater()
        
        for container in self.filter_containers:
            container.deleteLater()
            
        self.filter_widgets = []
        self.filter_containers = []
        
        # Create filter widgets for each column
        if model:
            for col in range(model.columnCount()):
                # Create container widget
                container = QWidget(self.parent())
                layout = QHBoxLayout(container)
                layout.setContentsMargins(0, 0, 0, 0)
                
                # Create line edit for filtering
                filter_widget = QLineEdit(container)
                filter_widget.setPlaceholderText("Фільтр...")
                
                # Connect signal
                filter_widget.textChanged.connect(lambda text, col=col: self.filterChanged.emit(col, text))
                
                # Add to layout
                layout.addWidget(filter_widget)
                
                # Store references
                self.filter_widgets.append(filter_widget)
                self.filter_containers.append(container)
                
                # Position the container
                self._updateFilterPosition(col)
    
    def sectionResized(self, logicalIndex, oldSize, newSize):
        """Handle section resize events."""
        super().sectionResized(logicalIndex, oldSize, newSize)
        
        # Update positions of filter widgets
        for col in range(len(self.filter_widgets)):
            self._updateFilterPosition(col)
    
    def _updateFilterPosition(self, col):
        """Update the position of a filter widget."""
        if col >= len(self.filter_widgets) or not self.filter_visible:
            return
            
        # Get the section geometry
        section_rect = self.sectionViewportPosition(col)
        
        # Calculate position and size for filter
        x = self.sectionViewportPosition(col)
        width = self.sectionSize(col)
        
        # Adjust for last section stretch
        if col == len(self.filter_widgets) - 1 and self.stretchLastSection():
            width = max(width, self.width() - x)
        
        # Set geometry - important: the filter should be positioned below the header
        header_height = self.height() // 2 if self.filter_visible else self.height()
        
        self.filter_containers[col].setGeometry(
            x, header_height, 
            width, header_height
        )
        
        # Show the filter widget
        self.filter_containers[col].setVisible(self.filter_visible)
    
    def updateGeometries(self):
        """Update the header geometry including filter positions."""
        super().updateGeometries()
        
        # Update positions of all filter widgets
        for col in range(len(self.filter_widgets)):
            self._updateFilterPosition(col)
    
    def sectionSizeFromContents(self, logicalIndex):
        """Override to account for filter widgets in size calculation."""
        size = super().sectionSizeFromContents(logicalIndex)
        
        # If filters are visible, make header taller
        if self.filter_visible:
            size.setHeight(size.height() * 2)
            
        return size
    
    def sizeHint(self):
        """Override to provide a proper size hint for the header."""
        size = super().sizeHint()
        
        # If filters are visible, make header taller
        if self.filter_visible:
            size.setHeight(size.height() * 2)
            
        return size
    
    def filterText(self, column):
        """Get the filter text for a specific column."""
        if 0 <= column < len(self.filter_widgets):
            return self.filter_widgets[column].text()
        return ""
    
    def clearFilters(self):
        """Clear all filter inputs."""
        for widget in self.filter_widgets:
            widget.clear()
    
    def eventFilter(self, obj, event):
        """Filter events for child widgets."""
        if event.type() == QEvent.Resize:
            self.updateGeometries()
        return super().eventFilter(obj, event)