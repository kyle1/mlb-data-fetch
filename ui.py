import sys
import time

from PyQt5 import QtCore, QtGui, QtWidgets
from fetch import export_player_data

class ui_MainWindow(object):

    def setupUi(self, MainWindow):

        seasons = ["2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019"]

        # Main window
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MLB Data Fetch", "MLB Data Fetch"))

        #QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.lblSeasons = QtWidgets.QLabel(self.centralwidget)
        self.lblSeasons.setGeometry(QtCore.QRect(30, 20, 111, 16))
        self.lblSeasons.setObjectName("lblSeasons")
        self.lblSeasons.setText("Seasons")

        self.cboBeginSeason = QtWidgets.QComboBox(self.centralwidget)
        self.cboBeginSeason.setGeometry(QtCore.QRect(80, 20, 50, 22))
        self.cboBeginSeason.setObjectName("cboBeginSeason")
        self.cboBeginSeason.addItems(seasons)
        self.cboBeginSeason.setMaxVisibleItems(20)

        self.lblTo = QtWidgets.QLabel(self.centralwidget)
        self.lblTo.setGeometry(QtCore.QRect(140, 20, 111, 16))
        self.lblTo.setObjectName("lblTo")
        self.lblTo.setText("to")

        self.cboEndSeason = QtWidgets.QComboBox(self.centralwidget)
        self.cboEndSeason.setGeometry(QtCore.QRect(160, 20, 50, 22))
        self.cboEndSeason.setObjectName("cboEndSeason")
        self.cboEndSeason.addItems(seasons)
        self.cboEndSeason.setMaxVisibleItems(20)

        # PLAYERS
        self.grpPlayers = QtWidgets.QGroupBox(self.centralwidget)
        self.grpPlayers.setGeometry(QtCore.QRect(30, 70, 175, 320))
        self.grpPlayers.setObjectName("grpPlayers")
        self.grpPlayers.setTitle("")
        self.chkPlayers = QtWidgets.QCheckBox(self.grpPlayers)
        self.chkPlayers.setGeometry(QtCore.QRect(5, 5, 70, 17))
        self.chkPlayers.setObjectName("chkPlayers")
        self.chkPlayers.setText("Players")
        self.chkPlayers.setChecked(True)
        self.chkPlayers.stateChanged.connect(lambda: togglePlayers())
        player_props = ["PlayerID", "Season", "FullName", "FirstName", "LastName", "BirthDate", "Age", "Height", "Weight", "TeamID", "Position", "DebutDate", "BatSide", "PitchHand"]
        for i in range(len(player_props)):
            self.checkbox = QtWidgets.QCheckBox(self.grpPlayers)
            self.checkbox.setGeometry(QtCore.QRect(20, 30+(20*i), 100, 17))
            self.checkbox.setObjectName(player_props[i])
            self.checkbox.setText(player_props[i])
            self.checkbox.setChecked(True)

        def togglePlayers():
            if self.chkPlayers.isChecked():
                for prop in player_props:
                    checkbox = self.grpPlayers.findChild(QtWidgets.QCheckBox, prop)
                    checkbox.setEnabled(True)
            else:
                for prop in player_props:
                    checkbox = self.grpPlayers.findChild(QtWidgets.QCheckBox, prop)
                    checkbox.setEnabled(False)

        wait_times = []
        for i in range(31):
            wait_times.append(str(i))

        # GO
        self.grpGo = QtWidgets.QGroupBox(self.centralwidget)
        self.grpGo.setGeometry(QtCore.QRect(500, 500, 218, 108))
        self.grpGo.setObjectName("grpGo")
        self.grpGo.setTitle("")
        self.lblWaitTime = QtWidgets.QLabel(self.grpGo)
        self.lblWaitTime.setGeometry(QtCore.QRect(10, 5, 150, 25))
        self.lblWaitTime.setObjectName("lblWaitTime")
        self.lblWaitTime.setText("Wait time between requests:")
        self.cboRequestMin = QtWidgets.QComboBox(self.grpGo)
        self.cboRequestMin.setGeometry(QtCore.QRect(10, 30, 45, 22))
        self.cboRequestMin.setObjectName("cboRequestMin")
        self.cboRequestMin.addItems(wait_times)
        self.cboRequestMin.setMaxVisibleItems(20)
        self.lblTo = QtWidgets.QLabel(self.grpGo)
        self.lblTo.setGeometry(QtCore.QRect(60, 30, 30, 25))
        self.lblTo.setObjectName("lblTo")
        self.lblTo.setText("to")
        self.cboRequestMax = QtWidgets.QComboBox(self.grpGo)
        self.cboRequestMax.setGeometry(QtCore.QRect(75, 30, 45, 22))
        self.cboRequestMax.setObjectName("cboRequestMax")
        self.cboRequestMax.addItems(wait_times)
        self.cboRequestMax.setMaxVisibleItems(20)
        self.lblSeconds = QtWidgets.QLabel(self.grpGo)
        self.lblSeconds.setGeometry(QtCore.QRect(125, 30, 120, 25))
        self.lblSeconds.setObjectName("lblSeconds")
        self.lblSeconds.setText("seconds (random)")
        self.btnGo = QtWidgets.QPushButton(self.grpGo)
        self.btnGo.setGeometry(QtCore.QRect(150, 75, 60, 22))
        self.btnGo.setObjectName("btnGo")
        self.btnGo.setText("Go")
        self.btnGo.clicked.connect(lambda: getData())

        def getData():
            thread = GetDataThread(self)
            thread.start()
            # requested_seasons = []
            # for i in range(int(self.cboBeginSeason.currentText()), int(self.cboEndSeason.currentText())+1):
            #     requested_seasons.append(i)
            
            # for season in requested_seasons:
            #     if self.chkPlayers.isChecked():
            #         player_cols = []
            #         for prop in player_props:
            #             checkbox = self.grpPlayers.findChild(QtWidgets.QCheckBox, prop)
            #             if checkbox.isChecked():
            #                 player_cols.append(prop)
            #     export_player_data(season)


class GetDataThread(QtCore.QThread):

    def run(self):
        count = 0
        while count < 100:
            count += 1
            print(count)
            sleep(2)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
