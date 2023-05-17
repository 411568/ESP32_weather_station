// SLEEP TIME
#define uS_TO_S_FACTOR 1000000 /* Conversion factor for micro seconds to seconds */ 
#define TIME_TO_SLEEP 600 /* Time ESP32 will go to sleep (in seconds) */

void setup() 
{
  //setup sensors
  sensor_setup();

  //get sensor readings
  float temp = get_temperature_reading();
  float humidity = get_humidity_reading();
  float pressure= get_pressure_reading();
  float altitude = get_altitude_reading();
  float light = get_light_reading();
  float rain = get_rain_adc_reading();
  float wind = get_wind_speed_average();
  int battery_level = get_battery_level();

  //setup wifi (data logging)
  wifi_setup();
  delay(5000);

  //send data to thingspeak
  send_data(temp, humidity, pressure, altitude, light, rain, wind, battery_level);
  delay(5000);

  Serial.println("Data sent");
  Serial.flush(); 

  //go to sleep
  esp_sleep_enable_timer_wakeup(TIME_TO_SLEEP * uS_TO_S_FACTOR); //sleep for x minutes
  esp_deep_sleep_start();
}

void loop() 
{
  //does nothing in the main loop
}
