// Original synthetic sensor example. Compile default opens no CAN controller.
#include <Arduino.h>
#include <NMEA2000_esp32.h>
#include <N2kMessages.h>
#ifndef MARITIME_ENABLE_BUS
#define MARITIME_ENABLE_BUS 0
#endif
#if MARITIME_ENABLE_BUS
#error "Review pins, transceiver, assigned identity, receiver PGNs and rollback before implementing live mode"
#endif
// Explicit example pins, not a wiring recommendation. Constructor alone does not open CAN.
tNMEA2000_esp32 bus(GPIO_NUM_16, GPIO_NUM_17);
static uint32_t last_sample=0;
void setup(){Serial.begin(115200);}
void loop(){
 const uint32_t now=millis();
 if(static_cast<uint32_t>(now-last_sample)>=1000){
  last_sample=now;
  tN2kMsg sample;
  // Battery-temperature synthetic sample for codec demonstration; no transmission.
  SetN2kPGN127508(sample,0,12.5,-2.5,293.15,0);
  Serial.printf("synthetic PGN=%lu bytes=%d CAN disabled\n",sample.PGN,sample.DataLen);
 }
 delay(1);
}
