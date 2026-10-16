# Host-side heading encoding experiment

Date: 2026-10-16. Upstream: `ttlappalainen/NMEA2000`, commit
`5b7b9fc3ccc18e30ebfba92da6486cffc6251595`.
Compiler: Apple clang 17.0.0 (clang-1700.3.19.1), C++11.
Harness SHA-256:
`055a18102e6a91a46112a8d0c71e97e97c3f2436fc3f61f5e15d0f46b74cd550`.

## Hypothesis and oracle

The pinned heading setter emits the eight bytes calculated independently from
field widths, little-endian integers and scaling for three inputs: nominal values,
API unavailable sentinels and numeric overflow. Acceptance requires all three exact
vectors and PGN/priority/length checks; any mismatch returns nonzero. The harness
uses explicit conditions, so compiling with `NDEBUG` does not remove its checks.

The expected nominal vector comes from 10000, -1000 and 2000 raw counts. The
unavailable/overflow expectations use the constants inspected in the pinned source;
they are implementation checks, not independent confirmation of a licensed standard.

## Reproduce

Obtain the upstream source separately and check out the exact commit. From this
repository root, set `NMEA_STUDY_SOURCE` to that checkout's absolute path:

```sh
git -C "$NMEA_STUDY_SOURCE" rev-parse HEAD
c++ -std=c++11 -I "$NMEA_STUDY_SOURCE/src" \
  examples/heading_oracle.cpp "$NMEA_STUDY_SOURCE"/src/*.cpp \
  "$NMEA_STUDY_SOURCE/test/millis.cpp" -o /tmp/maritime-heading-oracle
/tmp/maritime-heading-oracle
```

Inspect external source before compiling. The upstream host-test `millis` stub
returns a fixed clock; this experiment does not exercise timing. No hardware CAN
backend is selected and no bus is opened. CI stays dependency-free and does not
fetch or execute this optional external experiment automatically.

## Observed result

Compilation succeeded with three upstream variable-length-array extension warnings:
two in `N2kGroupFunctionDefaultHandlers.cpp` and one in `Seasmart.cpp`.
The executable exited 0 and printed:

```text
nominal PASS 07102718FCD007FC
unavailable PASS 07FFFFFF7FFF7FFC
out-of-range PASS 07FEFFFE7FFE7FFC
```

This verifies these three setter vectors on this host/compiler. It does not verify
fast-packet reception, address claiming, timing, a new standalone stack, all PGNs,
CANboat agreement, hardware interoperability or certification. The source walkthrough
labels those additional findings as inspected behavior and implementation advice.
