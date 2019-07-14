from PyQt5.QtCore import QDateTime, Qt, QTimer, QRect
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QFileDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget)
from PyQt5.QtGui import QPalette, QColor


class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)

        QApplication.setStyle(QStyleFactory.create('Fusion'))
        QApplication.setPalette(QApplication.style().standardPalette())

        self.createExportGroupBox()
        self.createLogGroupBox()
        self.createSchemaTabWidget()
        self.createRequestsGroupBox()
        self.createProgressBar()

        self.path = ""

        topLayout = QHBoxLayout()
        seasons = ["2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019"]
        seasonsBeginComboBox = QComboBox()
        seasonsBeginComboBox.addItems(seasons)
        seasonsEndComboBox = QComboBox()
        seasonsEndComboBox.addItems(seasons)
        seasonsLabel = QLabel("Seasons:")
        seasonsLabel.setGeometry(QRect(10, 10, 20, 20))
        seasonsLabel.setBuddy(seasonsBeginComboBox)
        toLabel = QLabel("to")
        toLabel.setGeometry(QRect(70, 10, 20, 20))
        toLabel.setBuddy(seasonsEndComboBox)
        topLayout.addWidget(seasonsLabel)
        topLayout.addWidget(seasonsBeginComboBox)
        topLayout.addWidget(toLabel)
        topLayout.addWidget(seasonsEndComboBox)
        topLayout.addStretch(1)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.schemaTabWidget, 1, 0, 2, 1)
        mainLayout.addWidget(self.exportGroupBox, 1, 1, 1, 1)
        mainLayout.addWidget(self.requestsGroupBox, 2, 1, 1, 1)
        mainLayout.addWidget(self.logGroupBox, 3, 0, 1, 2)
        mainLayout.addWidget(self.progressBar, 4, 0, 1, 2)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)

        # Dark mode
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

        self.setLayout(mainLayout)
        self.setWindowTitle("MLB Data Fetch")

    def chooseFilePath(self):
        self.path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.pathLabel.setText(self.path)

    def advanceProgressBar(self):
        curVal = self.progressBar.value()
        maxVal = self.progressBar.maximum()
        self.progressBar.setValue(curVal + (maxVal - curVal) / 100)

    def createExportGroupBox(self):
        self.exportGroupBox = QGroupBox("Export")
        pathButton = QPushButton("Choose file path")
        pathButton.clicked.connect(self.chooseFilePath)
        self.pathLabel = QLabel("")
        layout = QVBoxLayout()
        layout.addWidget(pathButton)
        layout.addWidget(self.pathLabel)
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
        self.schemaTabWidget = QTabWidget()
        self.schemaTabWidget.setMinimumHeight(450)
        self.schemaTabWidget.setMinimumWidth(400)

        # player_tab = QWidget()
        # player_tab_vbox = QVBoxLayout()
        # player_tab_vbox.setContentsMargins(5, 20, 5, 5)
        # player_groupbox = QGroupBox("Player")
        # player_groupbox.setCheckable(True)
        # player_groupbox.setChecked(True)
        # player_groupbox.setContentsMargins(5, 5, 5, 5)
        # player_props = ["PlayerID", "Season", "FullName", "FirstName", "LastName", "BirthDate",
        #                 "Age", "Height", "Weight", "TeamID", "Position", "DebutDate", "BatSide", "PitchHand"]
        # for i in range(len(player_props)):
        #     checkbox = QCheckBox(player_groupbox)
        #     checkbox.setGeometry(QRect(25, 25+(20*i), 100, 17))
        #     checkbox.setObjectName(player_props[i])
        #     checkbox.setText(player_props[i])
        #     checkbox.setChecked(True)
        # player_tab_vbox.addWidget(player_groupbox)
        # player_tab.setLayout(player_tab_vbox)
        
        tabs = ["Player", "Team", "Venue", "Game", "PlayByPlay", "Schedule"]
        props = [
            ["PlayerID", "Season", "FullName", "FirstName", "LastName", "BirthDate", "Age", "Height", "Weight", "TeamID", "Position", "DebutDate", "BatSide", "PitchHand"],
            ["TeamID", "Name", "VenueID", "Abbreviation", "LocationName", "LeagueID", "DivisionID"],
            ["VenueID", "Name"],
            ["GameID", "Season", "GameDate", "Status", "AwayTeamID", "AwayTeamRecordWins", "AwayTeamRecordLosses", "AwayTeamRecordPct", "HomeTeamID", "HomeTeamScore", "HomeTeamRecordWins", "HomeTeamRecordLosses", "HomeTeamRecordPct", "VenueID", "DayNight", "SeriesGameNumber", "SeriesDescription"],
            ["PlayByPlayID", "GameID", "BatterID", "BatSide", "BatterSplit", "PitcherID", "PitchHand", "MenOnBase", "Event", "EventType", "IsScoringPlay", "AwayTeamScore", "HomeTeamScore", "AtBatIndex", "HalfInning", "Inning", "Outs"],
            ["GameID", "GameDate", "AwayTeamID", "HomeTeamID", "VenueID"]
        ]

        for i in range(len(tabs)):
            tab = QWidget()
            tab_vbox = QVBoxLayout()
            tab_vbox.setContentsMargins(5, 5, 5, 5)
            tab_groupbox = QGroupBox(tabs[i])
            tab_groupbox.setCheckable(True)
            tab_groupbox.setChecked(True)
            tab_groupbox.setContentsMargins(5, 5, 5, 5)
            cols = props[i]
            for j in range(len(cols)):
                checkbox = QCheckBox(tab_groupbox)
                checkbox.setGeometry(QRect(20, 35+(20*j), 150, 17))
                checkbox.setObjectName(cols[j])
                checkbox.setText(cols[j])
                checkbox.setChecked(True)
            tab_vbox.addWidget(tab_groupbox)
            tab.setLayout(tab_vbox)
            self.schemaTabWidget.addTab(tab, tabs[i])

    def createRequestsGroupBox(self):
        self.requestsGroupBox = QGroupBox("Make Requests")
        self.requestsGroupBox.setMinimumWidth(400)

        topLayout = QHBoxLayout()

        minSpinBox = QSpinBox()
        #minSpinBox.setGeometry(20, 30, 60, 20)
        minSpinBox.setValue(0)
        maxSpinBox = QSpinBox()
        #maxSpinBox.setGeometry(20, 30, 60, 20)
        maxSpinBox.setValue(30)
        waitTimeLabel = QLabel("Wait")
        waitTimeLabel.setGeometry(QRect(10, 10, 20, 20))
        waitTimeLabel.setBuddy(minSpinBox)
        toLabel = QLabel("to")
        toLabel.setGeometry(QRect(70, 10, 20, 20))
        toLabel.setBuddy(maxSpinBox)
        secondsLabel = QLabel("seconds between requests.")
        secondsLabel.setGeometry(QRect(130, 10, 20, 20))

        goButton = QPushButton("Go")
        goButton.setMinimumHeight(100)
        goButton.setMinimumWidth(380)
        #goButton.setDefault(True)

        topLayout.addWidget(waitTimeLabel)
        topLayout.addWidget(minSpinBox)
        topLayout.addWidget(toLabel)
        topLayout.addWidget(maxSpinBox)
        topLayout.addWidget(secondsLabel)
        topLayout.addStretch(1)

        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(goButton)

        requestsLayout = QGridLayout()
        requestsLayout.addLayout(topLayout, 0, 0, 1, 1)
        requestsLayout.addLayout(bottomLayout, 1, 0, 1, 1)
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