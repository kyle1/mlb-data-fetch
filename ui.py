from PyQt5.QtCore import QDateTime, Qt, QTimer, QRect
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit, QDial, QDialog, QFileDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QMessageBox,
    QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy, QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit, QVBoxLayout, QWidget)
from PyQt5.QtGui import QPalette, QColor
from threading import Thread
from time import sleep
import fetch as fetch


class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)

        QApplication.setStyle(QStyleFactory.create('Fusion'))
        QApplication.setPalette(QApplication.style().standardPalette())

        self.tabGroupboxes = []
        self.savePath = ""

        self.setDarkMode()
        self.createSeasonsGroupBox()
        self.createExportGroupBox()
        self.createLogGroupBox()
        self.createSchemaTabWidget()
        self.createRequestsGroupBox()
        self.createProgressBar()

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.schemaGroupBox, 0, 0, 3, 1)
        mainLayout.addWidget(self.seasonsGroupBox, 0, 1, 1, 1)
        mainLayout.addWidget(self.exportGroupBox, 1, 1, 1, 1)
        mainLayout.addWidget(self.requestsGroupBox, 2, 1, 1, 1)
        mainLayout.addWidget(self.logGroupBox, 3, 0, 1, 2)
        mainLayout.addWidget(self.progressBar, 4, 0, 1, 2)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)
        self.setWindowTitle("MLB Data Fetch")

    def setDarkMode(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        app.setPalette(palette)

    def chooseFilePath(self):
        self.savePath = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.savePathLabel.setText(self.savePath)

    def validateSettings(self):
        error = ""
        if int(self.seasonsBeginComboBox.currentText()) > int(self.seasonsEndComboBox.currentText()):
            error += "Invalid seasons range.\n"
        if self.savePath == "":
            error += "No save directory chosen.\n"

        if error != "":
            msgbox = QMessageBox()
            msgbox.setFixedWidth(800)
            msgbox.setWindowTitle("Error")
            msgbox.setIcon(QMessageBox.Critical)
            msgbox.setText(error)
            msgbox.exec_()
            return False
        else:
            return True

    def fetchData(self):
        tables = []
        for groupbox in self.tabGroupboxes:
            if groupbox.isChecked():
                table = groupbox.objectName()
                cols = []
                checkboxes = groupbox.findChildren(QWidget)
                for checkbox in checkboxes:
                    if checkbox.isChecked():
                        cols.append(checkbox.objectName())
                tables.append({"tableName": table, "cols": cols})

        seasons = []
        for i in range(int(self.seasonsBeginComboBox.currentText()), int(self.seasonsEndComboBox.currentText())+1):
            seasons.append(i)

        for season in seasons:
            for table in tables:
                if table["tableName"] == "Player":
                    fetch.export_player_data(season, table["cols"])
                    #sleep(10)
                # if table["tableName"] == "Team":
                #     fetch.export_team_data(season, table["cols"])
                #     sleep(10)
                # if table["tableName"] == "Venue":
                #     fetch.export_venue_data(season, table["cols"])
                #     sleep(10)
                # if table["tableName"] == "Game":
                #     fetch.export_game_data(season, table["cols"])
                #     sleep(10)
                # if table["PlayByPlay"] == "PlayByPlay":
                #     fetch.export_game_data(season, table["cols"])
                #     sleep(10)
                # if table["Schedule"] == "Schedule":
                #     fetch.export_game_data(season, table["cols"])
                #     sleep(10)


    def goButtonClicked(self):
        validSettings = self.validateSettings()
        if validSettings:
            thread = Thread(target=self.fetchData, daemon=True)
            thread.start()

    def advanceProgressBar(self):
        curVal = self.progressBar.value()
        maxVal = self.progressBar.maximum()
        self.progressBar.setValue(curVal + (maxVal - curVal) / 100)

    def createSeasonsGroupBox(self):
        self.seasonsGroupBox = QGroupBox("Seasons")
        topLayout = QHBoxLayout()
        seasons = ["2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019"]
        self.seasonsBeginComboBox = QComboBox()
        self.seasonsBeginComboBox.addItems(seasons)
        self.seasonsEndComboBox = QComboBox()
        self.seasonsEndComboBox.addItems(seasons)
        seasonsLabel = QLabel("Range:")
        seasonsLabel.setGeometry(QRect(10, 10, 20, 20))
        seasonsLabel.setBuddy(self.seasonsBeginComboBox)
        toLabel = QLabel("to")
        toLabel.setGeometry(QRect(70, 10, 20, 20))
        toLabel.setBuddy(self.seasonsEndComboBox)
        topLayout.addWidget(seasonsLabel)
        topLayout.addWidget(self.seasonsBeginComboBox)
        topLayout.addWidget(toLabel)
        topLayout.addWidget(self.seasonsEndComboBox)
        topLayout.addStretch(1)
        seasonsLayout = QGridLayout()
        seasonsLayout.addLayout(topLayout, 0, 0, 1, 1)
        self.seasonsGroupBox.setLayout(seasonsLayout)   

    def createExportGroupBox(self):
        self.exportGroupBox = QGroupBox("Export")
        pathButton = QPushButton("Choose file path")
        pathButton.clicked.connect(self.chooseFilePath)
        self.savePathLabel = QLabel("")
        radioButton1 = QRadioButton(".xls")
        radioButton2 = QRadioButton(".csv")
        radioButton1.setChecked(True)
        layout = QVBoxLayout()
        layout.addWidget(pathButton)
        layout.addWidget(self.savePathLabel)
        layout.addWidget(radioButton1)
        layout.addWidget(radioButton2)
        layout.addStretch(1)
        self.exportGroupBox.setLayout(layout)    

    def createLogGroupBox(self):
        self.logGroupBox = QGroupBox("Log")
        textEdit = QTextEdit()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(textEdit)
        layout.addStretch(1)
        self.logGroupBox.setLayout(layout)

    def createSchemaTabWidget(self):
        self.schemaGroupBox = QGroupBox("Data")
        layout = QVBoxLayout()
        self.schemaTabWidget = QTabWidget()
        self.schemaTabWidget.setMinimumHeight(300)
        self.schemaTabWidget.setMinimumWidth(380)
        
        self.tabs = ["Player", "Team", "Venue", "Game", "PlayByPlay", "Schedule"]
        self.props = [
            ["PlayerID", "Season", "FullName", "FirstName", "LastName", "BirthDate", "Age", "Height", "Weight", "TeamID", "Position", "DebutDate", "BatSide", "PitchHand"],
            ["TeamID", "Name", "VenueID", "Abbreviation", "LocationName", "LeagueID", "DivisionID"],
            ["VenueID", "Name"],
            ["GameID", "Season", "GameDate", "Status", "AwayTeamID", "AwayTeamRecordWins", "AwayTeamRecordLosses", "AwayTeamRecordPct", "HomeTeamID", "HomeTeamScore", "HomeTeamRecordWins", "HomeTeamRecordLosses", "HomeTeamRecordPct", "VenueID", "DayNight", "SeriesGameNumber", "SeriesDescription"],
            ["PlayByPlayID", "GameID", "BatterID", "BatSide", "BatterSplit", "PitcherID", "PitchHand", "MenOnBase", "Event", "EventType", "IsScoringPlay", "AwayTeamScore", "HomeTeamScore", "AtBatIndex", "HalfInning", "Inning", "Outs"],
            ["GameID", "GameDate", "AwayTeamID", "HomeTeamID", "VenueID"]
        ]

        for i in range(len(self.tabs)):
            tab = QWidget()
            tabVbox = QVBoxLayout()
            tabVbox.setContentsMargins(5, 5, 5, 5)
            tabGroupbox = QGroupBox(self.tabs[i])
            tabGroupbox.setObjectName(self.tabs[i])
            tabGroupbox.setCheckable(True)
            tabGroupbox.setChecked(True)
            tabGroupbox.setContentsMargins(5, 5, 5, 5)
            self.tabGroupboxes.append(tabGroupbox)
            cols = self.props[i]
            x_offset = 0
            y_multiplier = 0

            for j in range(len(cols)):
                if j == 10:
                    x_offset = 175
                    y_multiplier = 0
                checkbox = QCheckBox(tabGroupbox)
                checkbox.setGeometry(QRect(20+x_offset, 35+(20*y_multiplier), 150, 17))
                checkbox.setObjectName(cols[j])
                checkbox.setText(cols[j])
                checkbox.setChecked(True)
                y_multiplier += 1

            tabVbox.addWidget(tabGroupbox)
            tab.setLayout(tabVbox)
            self.schemaTabWidget.addTab(tab, self.tabs[i])

        layout.addWidget(self.schemaTabWidget)
        self.schemaGroupBox.setLayout(layout)

    def createRequestsGroupBox(self):
        self.requestsGroupBox = QGroupBox("Make Requests")
        self.requestsGroupBox.setMinimumWidth(380)

        topLayout = QHBoxLayout()
        minSpinBox = QSpinBox()
        minSpinBox.setValue(0)
        maxSpinBox = QSpinBox()
        maxSpinBox.setValue(30)
        waitTimeLabel = QLabel("Wait")
        waitTimeLabel.setGeometry(QRect(10, 10, 20, 20))
        waitTimeLabel.setBuddy(minSpinBox)
        toLabel = QLabel("to")
        toLabel.setGeometry(QRect(70, 10, 20, 20))
        toLabel.setBuddy(maxSpinBox)
        secondsLabel = QLabel("seconds between requests.")
        secondsLabel.setGeometry(QRect(130, 10, 20, 20))
        topLayout.addWidget(waitTimeLabel)
        topLayout.addWidget(minSpinBox)
        topLayout.addWidget(toLabel)
        topLayout.addWidget(maxSpinBox)
        topLayout.addWidget(secondsLabel)
        topLayout.addStretch(1)

        middleLayout = QHBoxLayout()
        estimatedTimeLabel = QLabel("Estimated run time:")
        middleLayout.addWidget(estimatedTimeLabel)
        middleLayout.addStretch(1)

        bottomLayout = QHBoxLayout()
        goButton = QPushButton("Go")
        goButton.setMinimumHeight(30)
        goButton.setMinimumWidth(300)
        goButton.clicked.connect(lambda: self.goButtonClicked())
        bottomLayout.addWidget(goButton)

        requestsLayout = QGridLayout()
        requestsLayout.addLayout(topLayout, 0, 0, 1, 1)
        requestsLayout.addLayout(middleLayout, 1, 0, 1, 1)
        requestsLayout.addLayout(bottomLayout, 2, 0, 1, 1)
        self.requestsGroupBox.setLayout(requestsLayout)

    def createProgressBar(self):
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 10000)
        self.progressBar.setValue(0)
        timer = QTimer(self)
        timer.timeout.connect(self.advanceProgressBar)
        timer.start(1000)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(app.exec_()) 