from PyQt5.QtCore import QDateTime, Qt, QTimer, QRect
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit, QDial, QDialog, QFileDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy, QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit, QVBoxLayout, QWidget)
from PyQt5.QtGui import QPalette, QColor
from threading import Thread
from time import sleep
from random import randint
import fetch as fetch
import fetch_csv as fetch_csv


class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)

        QApplication.setStyle(QStyleFactory.create('Fusion'))
        QApplication.setPalette(QApplication.style().standardPalette())

        self.tabGroupboxes = []
        self.savePath = ""
        self.logMessages = ""

        self.setDarkMode()
        self.createSeasonsGroupBox()
        self.createExportGroupBox()
        self.createLogGroupBox()
        self.createSchemaTabWidget()
        self.createRequestsGroupBox()
        self.createProgressBar()
        self.initiateLogWatcher()

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

        minSec = self.minSpinBox.value()
        maxSec = self.maxSpinBox.value()


        csv = True
        if csv:
            for table in tables:
                # Team and Venue are not based on season, so just get this data once
                if table["tableName"] == "Team":
                    fetch_csv.export_team_data(table["cols"], self.savePath)
                    self.logMessages += "Team data written to " + self.savePath + "/Team.csv\n"
                    sleep(randint(minSec, maxSec))
                if table["tableName"] == "Venue":
                    fetch_csv.export_venue_data(table["cols"], self.savePath)
                    self.logMessages += "Venue data written to " + self.savePath + "/Venue.csv\n"
                    sleep(randint(minSec, maxSec))

            for season in seasons:
                for table in tables:
                    if table["tableName"] == "Player":
                        fetch_csv.export_player_data(season, table["cols"], self.savePath)
                        self.logMessages += "Player data written to " + self.savePath + "/Player" + str(season) + ".csv\n"
                        sleep(randint(minSec, maxSec))
                    if table["tableName"] == "Schedule":
                        fetch_csv.export_schedule_data(season, table["cols"], self.savePath)
                        self.logMessages += "Schedule data written to " + self.savePath + "/Schedule" + str(season) + ".csv\n"
                        sleep(randint(minSec, maxSec))
                    if table["tableName"] == "Game":
                        fetch_csv.export_game_data(season, table["cols"], self.savePath)
                        self.logMessages += "Game data written to " + self.savePath + "/Game" + str(season) + ".csv\n"
                        sleep(randint(minSec, maxSec))
                    if table["tableName"] == "MlbBoxscoreBatting":
                        fetch_csv.export_boxscore_data(season, table["cols"], minSec, maxSec, self.savePath)
                        self.logMessages += "Boxscore data written to " + self.savePath + "/MlbBoxscoreBatting" + str(season) + ".csv\n"
                        sleep(randint(minSec, maxSec))
                    if table["tableName"] == "MlbBoxscorePitching":
                        fetch_csv.export_boxscore_pitching_data(season, table["cols"], minSec, maxSec, self.savePath)
                        self.logMessages += "Boxscore data written to " + self.savePath + "/MlbBoxscorePitching" + str(season) + ".csv\n"
                        sleep(randint(minSec, maxSec))
                    if table["tableName"] == "PlayByPlay":
                        fetch_csv.export_pbp_data(season, table["cols"], minSec, maxSec, self.savePath)
                        self.logMessages += "PlayByPlay data written to " + self.savePath + "/PlayByPlay" + str(season) + ".csv\n"
                        sleep(randint(minSec, maxSec))
        else:
            for table in tables:
                # Team and Venue are not based on season, so just get this data once
                if table["tableName"] == "Team":
                    fetch.export_team_data(table["cols"], self.savePath)
                    self.logMessages += "Team data written to " + self.savePath + "/Team.xls\n"
                    sleep(randint(minSec, maxSec))
                if table["tableName"] == "Venue":
                    fetch.export_venue_data(table["cols"], self.savePath)
                    self.logMessages += "Venue data written to " + self.savePath + "/Venue.xls\n"
                    sleep(randint(minSec, maxSec))

            for season in seasons:
                for table in tables:
                    if table["tableName"] == "Player":
                        fetch.export_player_data(season, table["cols"], self.savePath)
                        self.logMessages += "Player data written to " + self.savePath + "/Player" + str(season) + ".xls\n"
                        sleep(randint(minSec, maxSec))
                    if table["tableName"] == "Schedule":
                        fetch.export_schedule_data(season, table["cols"], self.savePath)
                        self.logMessages += "Schedule data written to " + self.savePath + "/Schedule" + str(season) + ".xls\n"
                        sleep(randint(minSec, maxSec))
                    if table["tableName"] == "Game":
                        fetch.export_game_data(season, table["cols"], self.savePath)
                        self.logMessages += "Game data written to " + self.savePath + "/Game" + str(season) + ".xls\n"
                        sleep(randint(minSec, maxSec))
                    if table["tableName"] == "MlbBoxscoreBatting":
                        fetch.export_boxscore_data(season, table["cols"], minSec, maxSec, self.savePath)
                        self.logMessages += "MlbBoxscoreBatting data written to " + self.savePath + "/MlbBoxscoreBatting" + str(season) + ".xls\n"
                        sleep(randint(minSec, maxSec))
                    if table["tableName"] == "MlbBoxscorePitching":
                        fetch.export_boxscore_pitching_data(season, table["cols"], minSec, maxSec, self.savePath)
                        self.logMessages += "MlbBoxscorePitching data written to " + self.savePath + "/MlbBoxscoreBatting" + str(season) + ".xls\n"
                        sleep(randint(minSec, maxSec))
                    if table["tableName"] == "PlayByPlay":
                        fetch.export_pbp_data(season, table["cols"], minSec, maxSec, self.savePath)
                        self.logMessages += "PlayByPlay data written to " + self.savePath + "/PlayByPlay" + str(season) + ".xls\n"
                        sleep(randint(minSec, maxSec))


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
        self.logTextbox = QTextEdit()
        #self.logTextbox.setDisabled(True)
        self.logTextbox.setReadOnly(True)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.logTextbox)
        layout.addStretch(1)
        self.logGroupBox.setLayout(layout)

    def createSchemaTabWidget(self):
        self.schemaGroupBox = QGroupBox("Data")
        layout = QVBoxLayout()
        self.schemaTabWidget = QTabWidget()
        self.schemaTabWidget.setMinimumHeight(300)
        self.schemaTabWidget.setMinimumWidth(380)

        self.tabs = ["Team", "Venue", "Player", "Schedule", "Game", "MlbBoxscoreBatting", "MlbBoxscorePitching", "PlayByPlay"]
        self.props = [
            ["MlbTeamID", "TeamName", "MlbVenueID", "TeamAbbrev", "LocationName", "MlbLeagueID", "MlbDivisionID"],
            ["MlbVenueID", "VenueName"],
            ["MlbPlayerID", "Season", "FullName", "FirstName", "LastName", "BirthDate", "PlayerHeight", "PlayerWeight", "MlbTeamID", "Position", "DebutDate", "BatSide", "PitchHand"],
            ["MlbScheduleID", "MlbGameID", "GameDateTime", "GameDate", "GameTime", "AwayTeamID", "HomeTeamID", "MlbVenueID"],
            ["MlbGameID", "Season", "GameDateTime", "GameDate", "GameTime", "Status", "AwayTeamID", "AwayTeamScore", "AwayTeamRecordWins", "AwayTeamRecordLosses", "AwayTeamRecordPct", "HomeTeamID", "HomeTeamScore", "HomeTeamRecordWins", "HomeTeamRecordLosses", "HomeTeamRecordPct", "VenueID", "DayNight", "GamesInSeries", "SeriesGameNumber", "SeriesDescription"],
            ["MlbBoxscoreBattingID", "MlbPlayerID", "MlbGameID", "AwayTeamID", "HomeTeamID", "IsAway", "BattingOrder", "AB", "R", "H", "2B", "3B", "HR", "RBI", "BB", "IBB", "SO", "HBP", "SH", "SF", "GDP", "SB", "CS"],
            ["MlbBoxscorePitchingID", "MlbPlayerID", "MlbGameID", "AwayTeamID", "HomeTeamID", "IsAway", "Start", "Win", "IP", "H", "R", "ER", "ERA", "SO", "HR", "BB", "HBP", "Shutout", "CompleteGame", "PitchCount"],
            ["PlayByPlayID", "GameID", "BatterID", "BatSide", "PitcherID", "PitchHand", "MenOnBase", "Event", "EventType", "IsScoringPlay", "AwayTeamScore", "HomeTeamScore", "AtBatIndex", "HalfInning", "Inning", "Outs"]
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
        self.minSpinBox = QSpinBox()
        self.minSpinBox.setValue(5)
        self.maxSpinBox = QSpinBox()
        self.maxSpinBox.setValue(15)
        waitTimeLabel = QLabel("Wait")
        waitTimeLabel.setGeometry(QRect(10, 10, 20, 20))
        waitTimeLabel.setBuddy(self.minSpinBox)
        toLabel = QLabel("to")
        toLabel.setGeometry(QRect(70, 10, 20, 20))
        toLabel.setBuddy(self.maxSpinBox)
        secondsLabel = QLabel("seconds between requests.")
        secondsLabel.setGeometry(QRect(130, 10, 20, 20))
        topLayout.addWidget(waitTimeLabel)
        topLayout.addWidget(self.minSpinBox)
        topLayout.addWidget(toLabel)
        topLayout.addWidget(self.maxSpinBox)
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

    def lol(self):
        self.logTextbox.setText(self.logMessages)

    def createProgressBar(self):
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 10000)
        self.progressBar.setValue(0)
        timer = QTimer(self)
        timer.timeout.connect(self.advanceProgressBar)
        timer.start(1000)

    def initiateLogWatcher(self):
        logTimer = QTimer(self)
        logTimer.timeout.connect(self.lol)
        logTimer.start(3000)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(app.exec_()) 