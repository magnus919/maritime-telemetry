// Original offline harness. Link against a separately obtained, pinned NMEA2000 tree.
// No CAN backend, bus opening, sockets, address claiming or live transmission.
#include <cstdio>
#include <cstring>
#include "N2kMessages.h"

static bool check(const char *label, double heading, double deviation,
                  double variation, const unsigned char expected[8]) {
  tN2kMsg message;
  SetN2kPGN127250(message, 7, heading, deviation, variation, N2khr_true);
  const bool ok = message.PGN == 127250 && message.Priority == 2 &&
                 message.DataLen == 8 && std::memcmp(message.Data, expected, 8) == 0;
  std::printf("%s %s ", label, ok ? "PASS" : "FAIL");
  for (int i = 0; i < message.DataLen; ++i) std::printf("%02X", message.Data[i]);
  std::puts("");
  return ok;
}

int main() {
  // Expected bytes independently calculated from integer scaling and byte order.
  const unsigned char nominal[] = {7, 0x10, 0x27, 0x18, 0xfc, 0xd0, 7, 0xfc};
  const unsigned char missing[] = {7, 0xff, 0xff, 0xff, 0x7f, 0xff, 0x7f, 0xfc};
  const unsigned char overflow[] = {7, 0xfe, 0xff, 0xfe, 0x7f, 0xfe, 0x7f, 0xfc};
  bool ok = check("nominal", 1.0, -0.1, 0.2, nominal);
  ok = check("unavailable", N2kDoubleNA, N2kDoubleNA, N2kDoubleNA, missing) && ok;
  ok = check("out-of-range", 7.0, 4.0, -4.0, overflow) && ok;
  return ok ? 0 : 1;
}
