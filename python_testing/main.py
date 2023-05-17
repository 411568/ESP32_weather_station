from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import matplotlib.pyplot as plt
import data_manipulation as dm


class MainWindow(QWidget):

    update_from_server = True
    predictions = False
    current_range = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # window title
        self.setWindowTitle('Weather station')

        # set starting size
        self.setGeometry(100, 100, 1400, 800)

        # set the layout (grid)
        layout = QGridLayout()
        self.setLayout(layout)

        # get data from server
        dm.temperature, dm.humidity, dm.pressure, dm.illumination, dm.wind_speed, dm.rain = dm.update_data_from_api()

        ############################################ FIGURES ############################################

        #temperature figure
        self.figureTemp = plt.figure(figsize=(5, 5))
        self.figureTempCanvas = FigureCanvas(self.figureTemp)
        layout.addWidget(self.figureTempCanvas, 1, 0)
        self.tempx = self.figureTemp.add_subplot(111)
        self.tempx.plot(dm.date_list, dm.temperature_list)
        self.tempx.xaxis.set_major_locator(plt.MaxNLocator(6))
        self.tempx.set_title("Temperature")
        # show canvas
        self.figureTempCanvas.show()

        #pressure figure
        self.figurePress = plt.figure(figsize=(5, 5))
        self.figurePressCanvas = FigureCanvas(self.figurePress)
        layout.addWidget(self.figurePressCanvas, 1, 1)
        self.pressx = self.figurePress.add_subplot(111)
        self.pressx.plot(dm.date_list, dm.pressure_list)
        self.pressx.xaxis.set_major_locator(plt.MaxNLocator(6))
        self.pressx.set_title("Pressure")
        # show canvas
        self.figurePressCanvas.show()

        # altitude figure
        self.figureIll = plt.figure(figsize=(5, 5))
        self.figureIllCanvas = FigureCanvas(self.figureIll)
        layout.addWidget(self.figureIllCanvas, 1, 2)
        self.illx = self.figureIll.add_subplot(111)
        self.illx.plot(dm.date_list, dm.illumination_list)
        self.illx.xaxis.set_major_locator(plt.MaxNLocator(6))
        self.illx.set_title("Illumination")
        # show canvas
        self.figureIllCanvas.show()

        # humidity figure
        self.figureHum = plt.figure(figsize=(5, 5))
        self.figureHumCanvas = FigureCanvas(self.figureHum)
        layout.addWidget(self.figureHumCanvas, 2, 0)
        self.humx = self.figureHum.add_subplot(111)
        self.humx.plot(dm.date_list, dm.humidity_list)
        self.humx.xaxis.set_major_locator(plt.MaxNLocator(6))
        self.humx.set_title("Humidity")
        # show canvas
        self.figureHumCanvas.show()

        # windspeed figure
        self.figureWind = plt.figure(figsize=(5, 5))
        self.figureWindCanvas = FigureCanvas(self.figureWind)
        layout.addWidget(self.figureWindCanvas, 2, 1)
        self.windx = self.figureWind.add_subplot(111)
        self.windx.plot(dm.date_list, dm.wind_speed_list)
        self.windx.xaxis.set_major_locator(plt.MaxNLocator(6))
        self.windx.set_title("Wind speed")
        # show canvas
        self.figureWindCanvas.show()

        # rain figure
        self.figureRain = plt.figure(figsize=(5, 5))
        self.figureRainCanvas = FigureCanvas(self.figureRain)
        layout.addWidget(self.figureRainCanvas, 2, 2)
        self.rainx = self.figureRain.add_subplot(111)
        self.rainx.plot(dm.date_list, dm.rain_list)
        self.rainx.xaxis.set_major_locator(plt.MaxNLocator(6))
        self.rainx.set_title("Precipation")
        # show canvas
        self.figureRainCanvas.show()


        ############################################ Bottom row ############################################

        # battery level indicator
        label_text = "Battery voltage: " + str(dm.battery_level_value).strip() + "V"
        battery_level_label = QLabel(label_text)
        battery_level_label.setFont(QFont('Times', 20))
        layout.addWidget(battery_level_label, 3, 1, alignment=Qt.AlignCenter)


        # update button
        update_button = QPushButton("Update")
        update_button.setGeometry(0, 0, 200, 10)
        update_button.setFont(QFont('Times', 20))
        update_button.resize(400, 20)
        update_button.clicked.connect(self.update_figures)
        layout.addWidget(update_button, 3, 0, alignment = Qt.AlignLeft)

        # prediction on/off
        forecast_button = QPushButton("Forecast ON/OFF")
        forecast_button.setFont(QFont('Times', 20))
        forecast_button.resize(400, 20)
        forecast_button.clicked.connect(self.prediction_change)
        layout.addWidget(forecast_button, 3, 0, alignment = Qt.AlignRight)


        date_label = QLabel("Date range: ")
        date_label.setFont(QFont('Times', 20))
        layout.addWidget(date_label, 3, 2, alignment = Qt.AlignLeft)

        self.date_frame_widget = QComboBox()
        self.date_frame_widget.setFont(QFont('Times', 20))
        self.date_frame_widget.addItems(["Last day", "Last week", "Last month", "All"])
        self.date_frame_widget.currentIndexChanged.connect(self.change_date_range)
        layout.addWidget(self.date_frame_widget, 3, 2, alignment = Qt.AlignRight)


        # show the window
        self.show()

    ############################################ FUNCTIONS ############################################
    def update_figures(self):
        # get new values if button pressed
        if(self.update_from_server == True):
            dm.temperature, dm.humidity, dm.pressure, dm.illumination, dm.wind_speed, dm.rain = dm.update_data_from_api()

        # clear existing data from plots
        self.tempx.clear()
        self.pressx.clear()
        self.humx.clear()
        self.windx.clear()
        self.rainx.clear()
        self.illx.clear()

        # plot new data
        self.tempx.plot(dm.date_list, dm.temperature_list)
        self.pressx.plot(dm.date_list, dm.pressure_list)
        self.humx.plot(dm.date_list, dm.humidity_list)
        self.windx.plot(dm.date_list, dm.wind_speed_list)
        self.rainx.plot(dm.date_list, dm.rain_list)
        self.illx.plot(dm.date_list, dm.illumination_list)

        # set ticks
        self.tempx.xaxis.set_major_locator(plt.MaxNLocator(6))
        self.pressx.xaxis.set_major_locator(plt.MaxNLocator(6))
        self.humx.xaxis.set_major_locator(plt.MaxNLocator(6))
        self.windx.xaxis.set_major_locator(plt.MaxNLocator(6))
        self.rainx.xaxis.set_major_locator(plt.MaxNLocator(6))
        self.illx.xaxis.set_major_locator(plt.MaxNLocator(6))

        # add titles
        self.tempx.set_title("Temperature")
        self.pressx.set_title("Pressure")
        self.illx.set_title("Illumination")
        self.humx.set_title("Humidity")
        self.windx.set_title("Wind speed")
        self.rainx.set_title("Precipation")


        # draw figures and show new plots
        self.figureTempCanvas.draw()
        self.figurePressCanvas.draw()
        self.figureHumCanvas.draw()
        self.figureRainCanvas.draw()
        self.figureWindCanvas.draw()
        self.figureIllCanvas.draw()
        self.show()

        self.update_from_server = True

    # change the data range on plots
    def change_date_range(self, i):
        # change the data lists (dm.date_list etc)
        self.current_range = i
        if(self.predictions == False):
            dm.change_date_range(self.current_range, False, dm.temperature, dm.humidity, dm.pressure, dm.illumination, dm.wind_speed, dm.rain)
        else:
            #with predictions on
            dm.change_date_range(self.current_range, True, dm.temperature, dm.humidity, dm.pressure, dm.illumination, dm.wind_speed, dm.rain)

        # update figures without getting data from the server again
        self.update_from_server = False
        self.update_figures()

    # prediction on/off button
    def prediction_change(self):
        if(self.predictions == False):
            self.predictions = True
        else:
            self.predictions = False
        # update the figures
        self.change_date_range(self.current_range)


if __name__ == '__main__':
    # start gui
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())