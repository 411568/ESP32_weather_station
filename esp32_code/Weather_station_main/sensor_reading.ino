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

// hall sensor pin
#define hall_pin 25

// battery level adc pin
#define battery_pin 2

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
    //while (1);
  }

  
  pinMode(hall_pin, INPUT_PULLUP); //hall sensor input


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
float get_rain_adc_reading()
{
  int temp = analogRead(rain_sensor_pin);
  float perc_temp = (4096.0 - float(temp)) / 40.96; 
  return perc_temp;
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


// ---------------- Battery level ---------------- ///
int get_battery_level()
{
  int battery_adc = analogRead(battery_pin);
  int battery_level = (battery_adc - 2321) / 5.46; //estimate battery percentage level 
  //the calculations above assume the max batt voltage to be 4.2V and lowest 3.4V
  return battery_level;
}


// ---------------- Anemometer ---------------- //
float get_wind_speed_reading()
{
  float hall_thresh = 10.0;
  float hall_count = 0.0;
  float start = micros(); // start the time count
  bool on_state = false;

  // counting number of times the hall sensor is tripped
  // but without double counting during the same trip
  while(true)
  {
    if (digitalRead(hall_pin) == 0)
    {      
      if (on_state==false)
      {
        on_state = true;
        hall_count += 1.0;
      }
    } 
    else
    {
      on_state = false;
    }
    
    //if threshold reached -> break
    if (hall_count >= hall_thresh)
    {
      break;
    }

    //if taking too long to reach th
    if(((micros()-start)/1000000.0) > 5)
    {
      break;
    }    
  }
  
  //calculate rpm
  float end_time = micros();
  float time_passed = ((end_time-start)/1000000.0);
  float rpm_val = (hall_count/time_passed)*60.0;
  //calculate wind speed in m/s
  float wind_speed = 2 * 3.14 * 0.045 * rpm_val / 60; // 0.045 is the arm length (R)
  return wind_speed;
  delay(10);
}

float get_wind_speed_average()
{
  float sum = 0.0;
 
  for(int i = 0; i < 5; i++)
  {
    sum += get_wind_speed_reading();
  }
  
  return sum/5;
}
