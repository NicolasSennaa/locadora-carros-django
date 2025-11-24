#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import atexit

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'locadora_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    try:
        from carros.utils.logout_all import logout_all_sessions
    except ImportError:
        def logout_all_sessions():
            pass 
    
    if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
        atexit.register(logout_all_sessions)

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()