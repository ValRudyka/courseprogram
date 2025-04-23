from PySide6.QtCore import QObject
from PySide6.QtWidgets import QMainWindow

class NavigationService(QObject):
    def __init__(self):
        super().__init__()
        self.current_view = None
        self.views = {}
        self.window_transitions = {}
        
    def register_view(self, view_name: str, view: QMainWindow) -> None:
        self.views[view_name] = view
        
    def register_transition(self, from_view: str, to_view: str, 
                           condition_func=None, before_show_func=None) -> None:
        if from_view not in self.window_transitions:
            self.window_transitions[from_view] = []
            
        self.window_transitions[from_view].append({
            'to_view': to_view,
            'condition': condition_func,
            'before_show': before_show_func
        })
    
    def navigate_to(self, to_view: str, from_view: str = None) -> bool:
        if from_view is None:
            from_view = self.current_view
            
        if from_view is None:
            if to_view in self.views:
                self.views[to_view].show()
                self.current_view = to_view
                return True
            return False
            
        if to_view not in self.views:
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
        if 'main' in self.views:
            main_view = self.views['main']
            main_view.closeEvent = lambda _: app.quit()
            
        for view_name, view in self.views.items():
            if view_name != 'main':
                def create_close_handler(view_name):
                    def handle_close(event):
                        if view_name == 'login':
                            app.quit()
                            event.accept()
                        elif view_name == 'register' and 'users' in self.views:
                            # Special case for register ->users transition
                            self.navigate_to('users', 'register')
                            event.ignore()
                        elif 'main' in self.views:
                            self.navigate_to('main', view_name)
                            event.ignore()  
                        else:
                            event.accept()
                    return handle_close
                
                view.closeEvent = create_close_handler(view_name)