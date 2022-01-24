import sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile, QIODevice, Qt

sets_data = []
config_data = []

class GDATA:
    currentFuncID = 0
    GL_CN = 0

GDT = GDATA()

def FuncMinus():
    window.listWidget.takeItem(window.listWidget.count()-1)
    sets_data.pop()

def FuncPlus():
    window.listWidget.addItem("New Function")
    item = window.listWidget.item(window.listWidget.count()-1)
    item.setFlags(item.flags() | Qt.ItemIsEditable)
    sets_data.append([])

def get_selected(widget):
    selected = widget.selectedItems()
    if not selected:
        return None
    return selected[0]

def OnFunctionChange():
    if len(sets_data) <= 1:
        return

    if GDT.currentFuncID >= 0:
        for i in range(len(sets_data[GDT.currentFuncID])):
            sets_data[GDT.currentFuncID][i].setHidden(True)

    selected = get_selected(window.listWidget)
    if selected is not None:
        GDT.currentFuncID = window.listWidget.row(selected)
        for itm in sets_data[GDT.currentFuncID]:
            itm.setHidden(False)
    else:
        GDT.currentFuncID = window.listWidget.count()-1
        for itm in sets_data[GDT.currentFuncID]:
            itm.setHidden(False)

def OnDataSetSelect():
    selected = get_selected(window.listWidget_2)
    ID = None
    if selected is not None:
        ID = int(selected.text().split(" ")[1])
    else:
        ID = window.listWidget_2.count() - 1


    window.lineEdit.setText(config_data[ID][0])
    window.lineEdit_2.setText(config_data[ID][1])
    window.lineEdit_3.setText(config_data[ID][2])
    window.lineEdit_4.setText(config_data[ID][3])


def DataMinus():
    selected = get_selected(window.listWidget)
    if selected is not None:
        accessID = window.listWidget.row(selected)
        accessList = sets_data[accessID]
        if accessList:
            deleted = accessList.pop()
            window.listWidget_2.takeItem(window.listWidget_2.row(deleted))
    else:
        accessID = window.listWidget.count()-1
        accessList = sets_data[accessID]
        if accessList:
            deleted = accessList.pop()
            window.listWidget_2.takeItem(window.listWidget_2.row(deleted))


def DataPlus():
    window.listWidget_2.addItem("Donnée "+str(GDT.GL_CN))
    item = window.listWidget_2.item(window.listWidget_2.count()-1)
    selected = get_selected(window.listWidget)
    if selected is not None:
        sets_data[window.listWidget.row(selected)].append(item)
        config_data.append(["" for _ in range(4)])
    else:
        sets_data[window.listWidget.count()-1].append(item)
        config_data.append(["" for _ in range(4)])
    GDT.GL_CN += 1

def SaveButton():
    selected = get_selected(window.listWidget_2)
    ID = None
    if selected is not None:
        ID = int(selected.text().split(" ")[1])
    else:
        ID = window.listWidget_2.count() - 1

    config_data[ID] = [window.lineEdit.text(),window.lineEdit_2.text(),window.lineEdit_3.text(),window.lineEdit_4.text()]

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
    window.listWidget_2.itemSelectionChanged.connect(OnDataSetSelect)

    #
    window.show()

    sys.exit(app.exec())
