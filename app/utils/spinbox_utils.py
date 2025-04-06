def safe_set_spinbox_value(spinbox, value, default_value=0):
    try:
        if value is None:
            spinbox.setValue(default_value)
            return False
            
        int_value = int(value)
        
        min_value = spinbox.minimum()
        max_value = spinbox.maximum()
        
        if min_value <= int_value <= max_value:
            spinbox.setValue(int_value)
            return True
        else:
            spinbox.setValue(default_value)
            return False
            
    except (ValueError, TypeError):
        spinbox.setValue(default_value)
        return False
    
def safe_get_spinbox_value(spinbox, default_value=None):
    try:
        return spinbox.value()
    except Exception:
        return default_value
    
def set_spinbox_with_data(spinbox, data, key, default_value=0):
    if data and key in data:
        return safe_set_spinbox_value(spinbox, data[key], default_value)
    else:
        spinbox.setValue(default_value)
        return False