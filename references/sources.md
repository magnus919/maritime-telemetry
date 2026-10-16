# Research sources and authority

Research checked 2026-10-16. These are public primary sources (standards-owner,
manufacturer or project-maintainer publications). The licensed NMEA specifications
were **not** acquired or reviewed. This repository contains original integration
guidance, not copied standards or a complete normative PGN/sentence database.

## What each name represents

| Name | Role | Appropriate claim |
|---|---|---|
| NMEA 0183 | Licensed serial interface standard | Implement a declared sentence/electrical profile; verify against target manuals |
| NMEA 2000 | Licensed CAN-based marine network standard | Build a prototype and test interoperability; certification is separate |
| CANboat | Open-source utilities and community protocol definitions | Decode using a pinned interpretation, preserving uncertainty |
| Signal K | Open data model/API specification plus independent implementations | Implement a declared schema/API contract |
| OpenCPN | Open-source chartplotter/navigation application and plugins | Verify named inputs/features on a specific release/platform |
| SensESP | ESP32 sensor integration framework | Publish supported Signal K observations using a tested build |
| OpenPlotter | Integration distribution/tools | Assemble supported hardware/software combinations |

NMEA's public 0183 page identifies version 4.30, and its N2K page identifies version
3.000 with amendments at the research date. Check current errata, licensing,
manufacturer/product codes and certification requirements directly with NMEA when
a conformance or distribution decision depends on them. Open-source library use
does not confer certification or trademark rights. Do not assert a blanket DIY
exemption or copy an assigned commercial identity.

## Source map

| Source | Use | Boundary |
|---|---|---|
| [NMEA 0183](https://www.nmea.org/nmea-0183.html) | Owner's overview, edition and HS distinction | Public overview is not the licensed field specification |
| [NMEA 2000](https://www.nmea.org/nmea-2000.html) | Owner's network and certification overview | Verify formal requirements with NMEA |
| [NMEA OneNet](https://www.nmea.org/nmea-onenet.html) | Ethernet-standard boundary | Not implemented by this skill |
| [Garmin technical reference](https://www8.garmin.com/manuals/webhelp/GUID-1415AAD0-FE63-42A6-8F8D-DB713D616122/EN-US/Technical_Reference_for_Garmin_NMEA_2000_Products_EN-US.pdf) | Physical network construction, power, limits | Apply to the described cable/device system |
| [Actisense 0183 guide](https://actisense.com/wp-content/uploads/2021/01/Everything-you-need-to-know-about-NMEA-0183-1.pdf) | Wiring/interface explanations | Exact device manual governs terminal connections |
| [GPSD NMEA reference](https://gpsd.gitlab.io/gpsd/NMEA.html) | Maintainer's sentence interoperability knowledge | Community interpretation, not normative NMEA text |
| [NMEA2000 library](https://github.com/ttlappalainen/NMEA2000) | Embedded implementation starting point | Pin core and controller backend together |
| [NMEA2000 identity guide](https://ttlappalainen.github.io/NMEA2000/md_7_glossary.html) | NAME, address/instance and developer responsibilities | Some author recommendations are not adopted here, including vendor identity substitution |
| [NMEA2000 message API](https://ttlappalainen.github.io/NMEA2000/_n2k_messages_8h.html) | Physical-unit setter/parser interfaces | Consult pinned source signatures before coding |
| [CANboat](https://github.com/canboat/canboat) | Capture tools and database provenance | Software project, not standards authority |
| [CANboat PGN reference](https://canboat.github.io/canboat/canboat.html) | Header/transport and field interpretations | Incomplete/proprietary definitions need independent evidence |
| [Signal K spec entry](https://signalk.org/specification/latest/) | Discover the current specification | Redirect/version can change; freeze actual version |
| [Signal K data model](https://signalk.org/specification/1.7.0/doc/data_model.html) | Versioned full/delta behavior | Historical versioned reference, not a claim of newest release |
| [Signal K sources](https://signalk.org/specification/1.7.0/doc/sources.html) | Provenance representation | Preserve identity through conversion |
| [Signal K REST](https://signalk.org/specification/1.7.0/doc/rest_api.html) | Endpoint discovery and reads | Discover deployed server support |
| [Signal K streaming](https://signalk.org/specification/1.7.0/doc/streaming_api.html) | Hello, subscriptions and cached values | Test reconnect/freshness policy separately |
| [Signal K PUT](https://signalk.org/specification/1.7.0/doc/put.html) | Command request contract | Handler acceptance is not physical feedback |
| [Signal K Server docs](https://demo.signalk.org/documentation/) | Provider/plugin architecture | Public demo is not a destination for private captures |
| [Signal K Server source](https://github.com/SignalK/signalk-server) | Installed-version configuration/source | Spec and server release numbers differ |
| [SensESP](https://signalk.org/SensESP/) | ESP32-to-Signal-K path | Does not automatically publish N2K PGNs |
| [OpenCPN N2K guide](https://opencpn.org/wiki/dokuwiki/doku.php?id=opencpn%3Amanual_basic%3Aquick_start_guide%3Aconnect_to%3Anmea2000) | Direct adapter support | Verify platform/version; descriptive unit typos are not wire-rate authority |
| [OpenCPN plugins](https://opencpn.org/OpenCPN/info/downloadplugins.html) | Supported installation route | Plugin-specific compatibility still applies |
| [Radar PI](https://github.com/opencpn-radar-pi/radar_pi) | Radar model and transport support | No generic radar interoperability promise |
| [OpenCPN radar targets](https://opencpn.org/wiki/dokuwiki/doku.php?id=opencpn%3Amanual_advanced%3Aais%3Aradar_targets) | Target data versus imagery | Older feature documentation; verify current consumer |
| [Linux SocketCAN](https://docs.kernel.org/networking/can.html) | Controller state and CAN socket behavior | Generic CAN plumbing, not an N2K application stack |
| [Espressif TWAI v5.1](https://docs.espressif.com/projects/esp-idf/en/v5.1/esp32/api-reference/peripherals/twai.html) | External transceiver and true listen-only semantics | Version/SoC-specific; select actual target docs |
| [OpenPlotter CAN 2.x](https://openplotter.readthedocs.io/2.x.x/can/can_app.html) | Historical integration orientation | Not current board/OS installation authority |

## Resolve conflicts rather than hide them

Prefer licensed requirements for conformance, exact manufacturer manuals for a
physical device, and pinned source for the software actually running. A public
page's “latest” link is not a reproducibility pin. During research, Signal K search
metadata and the live `latest` redirect disagreed; the reference links above use
an accessible explicit 1.7.0 snapshot without declaring it the newest version.

CANboat's current README describes both C tools and a newer Rust CLI; older guides
may assume only the C pipeline. Consult the selected release. Live interface/server
commands can claim addresses or modify gateway settings; offline conversion does
not have the same behavior. Inspect configuration and defaults before attaching.

When sources conflict, record the claim, version, authority and missing evidence.
Offer the smallest resolving test or document request. Never turn a plausible
community decoding into an unqualified standard requirement.

## Source-code study

The NMEA2000 walkthrough is pinned to commit
`5b7b9fc3ccc18e30ebfba92da6486cffc6251595` (inspected 2026-10-16).
It covers headers, typed codecs, transport, node management and service-loop behavior.
Three heading encoding vectors were also compiled and executed against that source;
see the walkthrough and experiment record linked from SKILL.md for exact scope.
