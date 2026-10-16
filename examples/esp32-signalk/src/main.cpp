// Original synthetic producer, compile-only validation. No GPIO sensor or actuator.
#include <memory>
#include "sensesp.h"
#include "sensesp/sensors/sensor.h"
#include "sensesp/signalk/signalk_output.h"
#include "sensesp_app_builder.h"
using namespace sensesp;
void loop(){event_loop()->tick();}
void setup(){
 SetupLogging(ESP_LOG_INFO);
 SensESPAppBuilder builder;
 sensesp_app=builder.set_hostname("maritime-synthetic-lab")->get_app();
 auto sensor=std::make_shared<RepeatSensor<float>>(1000, [](){return 293.15f;});
 auto meta=std::make_shared<SKMetadata>("K","Synthetic water temperature - not a real sensor");
 auto output=std::make_shared<SKOutput<float>>("environment.water.temperature","/lab/water",meta);
 sensor->connect_to(output);
 while(true){loop();}
}
