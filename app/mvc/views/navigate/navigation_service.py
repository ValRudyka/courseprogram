from PySide6.QtCore import QObject
from PySide6.QtWidgets import QMainWindow

class NavigationService(QObject):
    """Service for managing navigation between application windows"""
    
    def __init__(self):
        super().__init__()
        self.current_view = None
        self.views = {}
        self.window_transitions = {}
        
    def register_view(self, view_name: str, view: QMainWindow) -> None:
        """Register a view with the navigation service"""
        self.views[view_name] = view
        
    def register_transition(self, from_view: str, to_view: str, 
                           condition_func=None, before_show_func=None) -> None:
        """
        Register a transition between views
        
        Args:
            from_view: Name of the source view
            to_view: Name of the destination view
            condition_func: Optional function to call before transition, should return bool
            before_show_func: Optional function to call before showing the destination view
        """
        if from_view not in self.window_transitions:
            self.window_transitions[from_view] = []
            
        self.window_transitions[from_view].append({
            'to_view': to_view,
            'condition': condition_func,
            'before_show': before_show_func
        })
    
    def navigate_to(self, to_view: str, from_view: str = None) -> bool:
        """Navigate from current view (or specified view) to the target view"""
        if from_view is None:
            from_view = self.current_view
            
        if from_view is None or to_view not in self.views:
            return False
            
        if from_view in self.window_transitions:
            for transition in self.window_transitions[from_view]:
                if transition['to_view'] == to_view:
                    if transition['condition'] and not transition['condition']():
                        return False
                    
                    if from_view in self.views:
                        self.views[from_view].hide()
                    
                    if transition['before_show']:
                        transition['before_show']()
                    
                    self.views[to_view].show()
                    self.current_view = to_view
                    return True
        
        if from_view in self.views:
            self.views[from_view].hide()
        
        self.views[to_view].show()
        self.current_view = to_view
        return True
    
    def setup_close_handlers(self, app):
        """Setup close event handlers for all views"""
        if 'main' in self.views:
            main_view = self.views['main']
            main_view.closeEvent = lambda _: app.quit()
            
        for view_name, view in self.views.items():
            if view_name != 'main':
                def create_close_handler(view_name):
                    def handle_close(event):
                        if 'main' in self.views:
                            self.navigate_to('main', view_name)
                            event.ignore()  
                        else:
                            event.accept()
                    return handle_close
                
                view.closeEvent = create_close_handler(view_name)