from app.database.manage import get_paneles
from app.ssh.ssh_client import ComunicationSSH
from app.icmp.icmp_client import is_device_online
from app.gui.main_windows import QApplication,MainWindow
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    
    useCustomTheme = True
    themeFile ="C:\\Users\\PC\Documents\\repositorio\\PanelesPyside6\\dark_theme.qss"
    
    window = MainWindow(useCustomTheme, themeFile)
    
    window.show()
    
    sys.exit(app.exec())
