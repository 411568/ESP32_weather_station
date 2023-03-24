from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import matplotlib.pyplot as plt
import data_manipulation as dm


class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # window title
        self.setWindowTitle('Weather station')

        # set starting size
        self.setGeometry(100, 100, 1400, 800)

        # set the layout (grid)
        layout = QGridLayout()
        self.setLayout(layout)

        ############################################ FUNCTIONS ############################################
        def update_figures():
            # get new values
            dm.update_data_from_api()

            # clear existing data from plots
            tempx.clear()
            pressx.clear()
            humx.clear()
            windx.clear()
            rainx.clear()
            illx.clear()

            # plot new data
            tempx.plot(dm.date_list, dm.temperature_list)
            pressx.plot(dm.date_list, dm.pressure_list)
            humx.plot(dm.date_list, dm.humidity_list)
            windx.plot(dm.date_list, dm.wind_speed_list)
            rainx.plot(dm.date_list, dm.rain_list)
            illx.plot(dm.date_list, dm.illumination_list)

            # draw figures and show new plots
            self.figureTempCanvas.draw()
            self.figurePressCanvas.draw()
            self.figureHumCanvas.draw()
            self.figureRainCanvas.draw()
            self.figureWindCanvas.draw()
            self.figureIllCanvas.draw()
            self.show()


        ############################################ FIGURES ############################################

        #temperature figure
        self.figureTemp = plt.figure(figsize=(5, 5))
        self.figureTempCanvas = FigureCanvas(self.figureTemp)
        layout.addWidget(self.figureTempCanvas, 1, 0)
        tempx = self.figureTemp.add_subplot(111)
        tempx.plot(dm.date_list, dm.temperature_list)
        tempx.set_title("Temperature")
        # show canvas
        self.figureTempCanvas.show()

        #pressure figure
        self.figurePress = plt.figure(figsize=(5, 5))
        self.figurePressCanvas = FigureCanvas(self.figurePress)
        layout.addWidget(self.figurePressCanvas, 1, 1)
        pressx = self.figurePress.add_subplot(111)
        pressx.plot(dm.date_list, dm.pressure_list)
        pressx.set_title("Pressure")
        # show canvas
        self.figurePressCanvas.show()

        # altitude figure
        self.figureIll = plt.figure(figsize=(5, 5))
        self.figureIllCanvas = FigureCanvas(self.figureIll)
        layout.addWidget(self.figureIllCanvas, 1, 2)
        illx = self.figureIll.add_subplot(111)
        illx.plot(dm.date_list, dm.illumination_list)
        illx.set_title("Illumination")
        # show canvas
        self.figureIllCanvas.show()

        # humidity figure
        self.figureHum = plt.figure(figsize=(5, 5))
        self.figureHumCanvas = FigureCanvas(self.figureHum)
        layout.addWidget(self.figureHumCanvas, 2, 0)
        humx = self.figureHum.add_subplot(111)
        humx.plot(dm.date_list, dm.humidity_list)
        humx.set_title("Humidity")
        # show canvas
        self.figureHumCanvas.show()

        # windspeed figure
        self.figureWind = plt.figure(figsize=(5, 5))
        self.figureWindCanvas = FigureCanvas(self.figureWind)
        layout.addWidget(self.figureWindCanvas, 2, 1)
        windx = self.figureWind.add_subplot(111)
        windx.plot(dm.date_list, dm.wind_speed_list)
        windx.set_title("Wind speed")
        # show canvas
        self.figureWindCanvas.show()

        # rain figure
        self.figureRain = plt.figure(figsize=(5, 5))
        self.figureRainCanvas = FigureCanvas(self.figureRain)
        layout.addWidget(self.figureRainCanvas, 2, 2)
        rainx = self.figureRain.add_subplot(111)
        rainx.plot(dm.date_list, dm.rain_list)
        rainx.set_title("Precipation")
        # show canvas
        self.figureRainCanvas.show()


        ############################################ Bottom row ############################################

        # battery level indicator
        battery_level_label = QLabel("Battery status: " + str(dm.battery_level_value) + "%")
        battery_level_label.setFont(QFont('Times', 20))
        layout.addWidget(battery_level_label, 3, 1, alignment=Qt.AlignCenter)


        # update button
        update_button = QPushButton("Update")
        update_button.setGeometry(0, 0, 200, 10)
        update_button.setFont(QFont('Times', 20))
        update_button.resize(400, 20)
        update_button.clicked.connect(update_figures)
        layout.addWidget(update_button, 3, 0, alignment = Qt.AlignLeft)

        # prediction on/off
        forecast_button = QPushButton("Forecast ON/OFF")
        forecast_button.setFont(QFont('Times', 20))
        update_button.resize(400, 20)
        layout.addWidget(forecast_button, 3, 0, alignment = Qt.AlignRight)

        button_scale = QPushButton("More values")
        button_scale.setGeometry(0, 0, 200, 10)
        button_scale.setFont(QFont('Times', 20))
        button_scale.resize(400, 20)
        layout.addWidget(button_scale, 3, 2, alignment = Qt.AlignRight)

        button_scale_down = QPushButton("Less values")
        button_scale_down.setGeometry(0, 0, 200, 10)
        button_scale_down.setFont(QFont('Times', 20))
        button_scale_down.resize(400, 20)
        layout.addWidget(button_scale_down, 3, 2, alignment=Qt.AlignLeft)

        # show the window
        self.show()



if __name__ == '__main__':
    # update data
    dm.update_data_from_api()

    # start gui
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
