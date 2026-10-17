// Original host-only experiment: encode synthetic AIS, never open a CAN interface.
#include <N2kMessages.h>
#include <cstdio>
#include <cstdint>
uint32_t millis() { return 0; }
void output(const tN2kMsg &m) {
  std::printf("2026-01-01T00:00:00.000Z,%u,%lu,35,255,%d", m.Priority,m.PGN,m.DataLen);
  for(int i=0;i<m.DataLen;i++) std::printf(",%02x",m.Data[i]);
  std::puts("");
}
int main() {
  tN2kMsg m;
  SetN2kPGN129038(m,1,N2kaisr_Initial,123456789,1,-2,true,false,30,1,5,
    N2kaischannel_A_VDL_reception,.5,0,N2kaisns_Under_Way_Motoring,7); output(m);
  SetN2kPGN129039(m,18,N2kaisr_Initial,123456789,1,-2,true,false,30,1,5,
    N2kaischannel_A_VDL_reception,.5,(tN2kAISUnit)1,false,false,false,false,(tN2kAISMode)0,false,7); output(m);
  SetN2kPGN129809(m,24,N2kaisr_Initial,123456789,"LAB TARGET",N2kaischannel_A_VDL_reception,7); output(m);
  SetN2kPGN129810(m,24,N2kaisr_Initial,123456789,36,"LAB","LAB123",12,4,1,8,0,N2kaischannel_A_VDL_reception,7); output(m);
}
