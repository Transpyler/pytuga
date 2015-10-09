import sys
from tugalinhas2 import QtWidgets, Tugalinhas


def main():
    '''Main function entry point for the Tugalinhas executable'''
    
    app = QtWidgets.QApplication(sys.argv)
    window = Tugalinhas()
    window.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()