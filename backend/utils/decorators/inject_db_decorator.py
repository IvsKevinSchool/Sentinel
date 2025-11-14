from functools import wraps
from fastapi import Depends
from sqlalchemy.orm import Session
from db.session import get_db
import inspect

def inject_db_to_methods(cls):
    """
    Decorador de clase que inyecta automáticamente db: Session = Depends(get_db)
    a todos los métodos que tengan 'db' como parámetro.
    """
    for attr_name in dir(cls):
        if attr_name.startswith('_'):  # Ignorar métodos privados
            continue
            
        attr = getattr(cls, attr_name)
        
        # Solo procesar métodos de instancia
        if callable(attr) and hasattr(attr, '__func__'):
            original_method = attr.__func__
            sig = inspect.signature(original_method)
            
            # Verificar si el método tiene un parámetro 'db'
            if 'db' in sig.parameters:
                @wraps(original_method)
                def make_wrapper(method):
                    def wrapper(self, *args, db: Session = Depends(get_db), **kwargs):
                        return method(self, *args, db=db, **kwargs)
                    wrapper.__signature__ = sig
                    return wrapper
                
                setattr(cls, attr_name, make_wrapper(original_method))
    
    return cls