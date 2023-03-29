#include <ESP32Time.h>
#include <WiFi.h>

// ESP32 internal RTC
ESP32Time rtc(3600);

void rtc_setup()
{
  //TODO 
  //get time from internet
  int second = 0;
  int minute = 0;
  int hour = 0;
  int day = 1;
  int month = 1;
  int year = 2023;

  rtc.setTime(second, minute, hour, day, month, year);
}