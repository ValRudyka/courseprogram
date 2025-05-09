import os
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize

class IconManager:
    def __init__(self) -> None:
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.icons_dir = os.path.join(self.base_dir, "icons")
        self._icon_cache = {}
        
        if not os.path.isdir(self.icons_dir):
            print(f"Warning: Icons directory not found at {self.icons_dir}")
    
    def get_icon(self, icon_name: str) -> QIcon:
        if icon_name in self._icon_cache:
            return self._icon_cache[icon_name]
        
        for ext in ['.png', '.jpg', '.svg']:
            icon_path = os.path.join(self.icons_dir, f"{icon_name}{ext}")
            if os.path.exists(icon_path):
                icon = QIcon(icon_path)
                self._icon_cache[icon_name] = icon
                return icon
        
        icon_path = os.path.join(self.icons_dir, icon_name)
        if os.path.exists(icon_path):
            icon = QIcon(icon_path)
            self._icon_cache[icon_name] = icon
            return icon
        
        print(f"Warning: Icon '{icon_name}' not found in {self.icons_dir}")
        return QIcon()
    
    def set_button_icon(self, button, icon_name: str, size: tuple[int, int] = (30, 30)) -> bool:
        icon = self.get_icon(icon_name)
        if not icon.isNull():
            button.setIcon(icon)
            button.setIconSize(QSize(*size))
            return True

icon_manager = IconManager()