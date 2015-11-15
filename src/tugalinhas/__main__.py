import sys
from PyQt5 import QtWidgets
from tugalinhas import Tugalinhas


def main():
    '''Main function entry point for the Tugalinhas executable'''
    
    app = QtWidgets.QApplication(sys.argv)
    window = Tugalinhas()
    window.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()