import sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile, QIODevice, Qt

data = []

def FuncMinus():
    window.listWidget.takeItem(window.listWidget.count()-1)
    data.pop()

def FuncPlus():
    window.listWidget.addItem("New Function")
    item = window.listWidget.item(window.listWidget.count()-1)
    item.setFlags(item.flags() | Qt.ItemIsEditable)
    data.append([])

def get_selected():
    selected = window.listWidget.selectedItems()
    if not selected:
        return None
    return selected[0]

def OnFunctionChange():
    pass


def DataMinus():
    window.listWidget_2.takeItem(window.listWidget_2.count()-1)
    item = window.listWidget_2.item(window.listWidget_2.count()-1)
    selected = get_selected()
    if selected is not None:
        data[window.listWidget.row(selected)].pop()
    else:
        data[window.listWidget.count()-1].pop()
def DataPlus():
    window.listWidget_2.addItem("Donnée "+str(window.listWidget_2.count()))
    item = window.listWidget_2.item(window.listWidget_2.count()-1)
    selected = get_selected()
    if selected is not None:
        data[window.listWidget.row(selected)].append(item)
    else:
        data[window.listWidget.count()-1].append(item)

def SaveButton():
    print("Save")

def GenConfigButton():
    print("GenConfigButton")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    ui_file_name = "GuiDesign.ui"
    ui_file = QFile(ui_file_name)
    if not ui_file.open(QIODevice.ReadOnly):
        print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
        sys.exit(-1)
    loader = QUiLoader()
    window = loader.load(ui_file)
    ui_file.close()
    if not window:
        print(loader.errorString())
        sys.exit(-1)

    # Signals test

    window.pushButton.clicked.connect(FuncMinus)
    window.pushButton_2.clicked.connect(FuncPlus)
    window.pushButton_3.clicked.connect(DataMinus)
    window.pushButton_4.clicked.connect(DataPlus)
    window.pushButton_5.clicked.connect(SaveButton)
    window.pushButton_6.clicked.connect(GenConfigButton)

    window.listWidget.itemSelectionChanged.connect(OnFunctionChange)

    #
    window.show()

    sys.exit(app.exec())
