// Original offline probe; upstream source supplied separately. No hardware driver.
#include <cstdio>
#include <cstring>
#include <vector>
#include <deque>
#include <cstdint>
#include "NMEA2000.h"
#include "N2kMessages.h"
static uint32_t clock_ms=0;
extern "C" uint32_t millis(){return clock_ms;}
#if defined(__linux__)
#include <time.h>
// The pinned Linux timer uses clock_gettime, not millis. This standalone fake-CAN
// executable supplies a deterministic process-local clock for its timing assertions.
extern "C" int clock_gettime(clockid_t, struct timespec* value) noexcept {
 value->tv_sec=clock_ms/1000;
 value->tv_nsec=static_cast<long>(clock_ms%1000)*1000000;
 return 0;
}
#endif
struct Frame { unsigned long id; unsigned char len; unsigned char data[8]; };
class FakeCAN: public tNMEA2000 {
 public:
 std::vector<Frame> sent; std::deque<Frame> input;
 bool CANOpen() override {return true;}
 bool CANSendFrame(unsigned long id,unsigned char len,const unsigned char* data,bool=true) override {
  Frame f{};f.id=id;f.len=len;std::memcpy(f.data,data,len);sent.push_back(f);return true;
 }
 bool CANGetFrame(unsigned long &id,unsigned char &len,unsigned char* data) override {
  if(input.empty())return false;Frame f=input.front();input.pop_front();id=f.id;len=f.len;std::memcpy(data,f.data,len);return true;
 }
};
static bool check(const char* name,const tN2kMsg& m,unsigned long pgn,const unsigned char* expected){
 bool ok=m.PGN==pgn&&m.DataLen==8&&std::memcmp(m.Data,expected,8)==0;
 std::printf("%s %s ",name,ok?"PASS":"FAIL");for(int i=0;i<m.DataLen;i++)std::printf("%02X",m.Data[i]);std::puts("");return ok;
}
int main(){
 tN2kMsg m;bool ok=true;
 // Independent scaled integer vectors, not encoder/decoder round trips.
 unsigned char depth[]={1,0xd2,0x04,0,0,0x0c,0xfe,0x0a};
 SetN2kPGN128267(m,1,12.34,-.5,100);ok=check("depth",m,128267,depth)&&ok;
 unsigned char pos[]={0x80,0x96,0x98,0,0,0xd3,0xce,0xfe};
 SetN2kPGN129025(m,1,-2);ok=check("position",m,129025,pos)&&ok;
 unsigned char battery[]={2,0xe2,4,0xe7,0xff,0x83,0x72,3};
 SetN2kPGN127508(m,2,12.5,-2.5,293.15,3);ok=check("battery",m,127508,battery)&&ok;
 unsigned char wind[]={4,0xf4,1,0x10,0x27,2,0xff,0xff};
 SetN2kPGN130306(m,4,5,1,N2kWind_Apparent);ok=check("wind",m,130306,wind)&&ok;
 FakeCAN bus;bus.SetMode(tNMEA2000::N2km_NodeOnly,35);bus.SetForwardStream(nullptr);
 // Start above zero: Linux's 64-bit scheduler uses a strict now > deadline test.
 clock_ms=1;bus.Open();clock_ms=202;bus.ParseMessages();
 bool claimed=false;for(const auto &f:bus.sent)if(((f.id>>16)&0xff)==0xee)claimed=true;
 SetN2kPGN127250(m,7,1,0,0,N2khr_true);
 bool held=!bus.SendMsg(m);clock_ms=453;bus.ParseMessages();bool allowed=bus.SendMsg(m);
 // Lower numeric NAME (all zero, synthetic test only) wins our preferred address.
 Frame conflict{};conflict.id=0x18eeff23;conflict.len=8;bus.input.push_back(conflict);
 bus.ParseMessages();bool moved=bus.GetN2kSource()!=35;
 bool lifecycle=claimed&&held&&allowed&&moved;
 std::printf("address-lifecycle %s claim=%d held=%d allowed=%d moved=%d\n",lifecycle?"PASS":"FAIL",claimed,held,allowed,moved);
 return ok&&lifecycle?0:1;
}
