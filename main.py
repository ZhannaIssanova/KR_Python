import requests
from bs4 import BeautifulSoup
from PyQt5 import QtCore, QtWidgets, uic
import sys
from pyqt5_plugins.examplebuttonplugin import QtGui

theme = ""
answer = ['']
link = ''


class Form1(QtWidgets.QMainWindow):
    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        super(Form1, self).__init__()
        uic.loadUi('UI/mainactivity.ui', self)
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.Next.clicked.connect(self.next)
        self.listWidget.clicked.connect(self.find_task)
        parsing(self)

    def next(self):
        self.switch_window.emit('1>2')



    def find_task(self):
        theme = self.listWidget.currentItem().text()
        if theme == "":
            self.label.setText("Выберите тему")
        else:
            try:

                link = "https://100task.ru/subject/sample_vm.aspx"
                responce = requests.get(link)
                src = responce.text


                with open("math.html", "w", encoding="utf-8") as file:
                    file.write(src)
                answer[0] = theme


            except:
                print("Ошибка подключения")




class Form2(QtWidgets.QMainWindow):
    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        super(Form2, self).__init__()
        uic.loadUi('UI/secondform.ui', self)
        self.setWindowTitle(answer[0])
        #self.Back.clicked.connect(self.back)
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        parsing2(self)


def parsing(self):
    link = "https://100task.ru/subject/sample_vm.aspx"
    responce = requests.get(link)
    src = responce.text
    soup = BeautifulSoup(src, "lxml")

    theme = soup.find("span", string = "Линейная алгебра")
    ptheme = theme.find_parent("liv",id=True)
    tema = ptheme.find_all("a")

    ptema=[]
    for word in tema:
        ptema.append(word.get('title'))

    for i in range(len(ptema)):
        self.listWidget.addItem(ptema[i])

def parsing2(self):
    link = "https://100task.ru/subject/sample_vm.aspx"
    responce = requests.get(link)
    src = responce.text
    soup = BeautifulSoup(src, "lxml")

    theme = soup.find('a', string = answer[0])

    url = 'https://100task.ru'+theme['href'][2:]
    responce = requests.get(url)
    src = responce.text
    root = BeautifulSoup(src, "lxml")

    theme = root.find('div', class_="linetheory")

    for x in theme.find_all('p'):
        print(x.get_text())
        self.textBrowser.append(x.get_text())

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Form1()
    window.show()
    sys.exit(app.exec_())


class Controller:
    def __init__(self):
        pass

    def select_forms(self, text):
        if text == '1':
            self.form1 = Form1()
            self.form1.switch_window.connect(self.select_forms)
            self.form1.show()
        if text == '1>2':
            self.form2 = Form2()
            self.form2.switch_window.connect(self.select_forms)
            self.form2.show()
            self.form1.close()





def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.select_forms("1")
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
