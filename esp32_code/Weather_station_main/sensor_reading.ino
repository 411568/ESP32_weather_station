#include <Wire.h>
#include <BH1750.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>


//used by BME280 for calculating altitude
#define SEALEVELPRESSURE_HPA (1013.25)

//rain sensor analog pin
#define rain_sensor_pin 4

//rain sensor threshold
#define rain_threshold 2000


// SENSOR objects
BH1750 lightMeter; // light sensor
Adafruit_BME280 bme;  //temperature, pressure, humidity


void sensor_setup()
{
  //start the I2C
  Wire.begin();

  //initialize the light sensor
  lightMeter.begin();

  //initialize the BME280
  bool status = bme.begin(0x76);  
  if (!status) 
  {
    Serial.begin(9600);
    Serial.println("Could not find a valid BME280 sensor, check wiring!");
    while (1);
  }
}

// ---------------- BME280 ---------------- //
float get_temperature_reading()
{
  bme.begin(0x76);
  return bme.readTemperature(); // in *C
}


float get_pressure_reading()
{
  bme.begin(0x76);
  return (bme.readPressure() / 100.0F); // in hPa
}

float get_altitude_reading()
{
  bme.begin(0x76);
  return bme.readAltitude(SEALEVELPRESSURE_HPA); // in m
}


float get_humidity_reading()
{
  bme.begin(0x76);
  return bme.readHumidity(); // in %
}



// ---------------- BH1750 ---------------- //
float get_light_reading()
{
  Wire.begin();
  lightMeter.begin();
  return lightMeter.readLightLevel(); //in lux
}



// ---------------- Rain sensor ---------------- //
int get_rain_adc_reading()
{
  int temp = analogRead(rain_sensor_pin);
  return temp;
}

bool is_it_raining()
{
  if(get_rain_adc_reading() > rain_threshold)
  {
    return false;
  }
  else
  {
    return true;
  }
}



// ---------------- Anemometer ---------------- //
float get_wind_speed_reading()
{
  //TODO
  return 0.0;
}
