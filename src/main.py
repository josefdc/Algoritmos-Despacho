from PyQt5 import QtWidgets
from gui import SchedulerApp
import sys

def main():
    # Initialize the application
    app = QtWidgets.QApplication(sys.argv)
    
    # Create and show the main window (SchedulerApp)
    scheduler = SchedulerApp()
    scheduler.show()
    
    # Start the application event loop
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
