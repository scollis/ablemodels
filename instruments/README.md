# Instruments

One file per instrument; link the `INST_*` (or `CSAPR2`) collection. Root at the origin.

`INST_BALLOON` is the radiosonde launch at M1: balloon, sonde, the line (a stretch-to constraint from sonde to balloon) and the two-person launch crew (`BALLOON_Crew`). It carries the release animation over frames 1–480; the *_Hold/*_Release crew poses swap visibility at release.

ECOR and SEBS share one tower, as deployed for DERECHOS. `INST_SEBS` has no mast of its own: instance it at the same transform as `INST_ECOR` (and `INST_SEBS_4m` with `INST_ECOR_4m`). It adds the Kipp & Zonen CNR4 radiometer in a CNF4 ventilator on a crossarm off the ECOR boom, the Vaisala DRD11A rain detector on the boom, the SEBS logger box on the tower, and three buried soil sets under the radiometer (Hukseflux HFP01 heat-flux plate at 5 cm, Stevens HydraProbe at 2.5 cm). The ECOR carries a Gill WindMaster Pro 3 sonic and a LI-COR LI-7500DS open-path gas analyser. The farm-workspace build script is `tools/build_farm_sebs.py`; `tools/port_farm_instrument.py` copies its output here.

| Preview | Collection | File |
|---|---|---|
| <img src="preview/AERI.jpg" width="260"> | `INST_AERI` | [`AERI/AERI.blend`](AERI/AERI.blend) (0.2 MB) |
| <img src="preview/AOSMET.jpg" width="260"> | `INST_AOSMET` | [`AOSMET/AOSMET.blend`](AOSMET/AOSMET.blend) (0.1 MB) |
| <img src="preview/ASI.jpg" width="260"> | `INST_ASI` | [`ASI/ASI.blend`](ASI/ASI.blend) (0.2 MB) |
| <img src="preview/AWOS.jpg" width="260"> | `INST_AWOS` | [`AWOS/AWOS.blend`](AWOS/AWOS.blend) (0.3 MB) |
| <img src="preview/BALLOON.jpg" width="260"> | `INST_BALLOON` | [`BALLOON/BALLOON.blend`](BALLOON/BALLOON.blend) (1.9 MB) |
| <img src="preview/CEIL.jpg" width="260"> | `INST_CEIL` | [`CEIL/CEIL.blend`](CEIL/CEIL.blend) (0.1 MB) |
| <img src="preview/CSAPR2.jpg" width="260"> | `CSAPR2` | [`CSAPR2/CSAPR2.blend`](CSAPR2/CSAPR2.blend) (1.2 MB) |
| <img src="preview/CSPHOT.jpg" width="260"> | `INST_CSPHOT` | [`CSPHOT/CSPHOT.blend`](CSPHOT/CSPHOT.blend) (0.2 MB) |
| <img src="preview/DL.jpg" width="260"> | `INST_DL` | [`DL/DL.blend`](DL/DL.blend) (0.2 MB) |
| <img src="preview/ECOR.jpg" width="260"> | `INST_ECOR` | [`ECOR/ECOR.blend`](ECOR/ECOR.blend) (0.3 MB) |
| <img src="preview/ECOR_4m.jpg" width="260"> | `INST_ECOR_4m` | [`ECOR/ECOR.blend`](ECOR/ECOR.blend) (0.3 MB) |
| <img src="preview/IRT.jpg" width="260"> | `INST_IRT` | [`IRT/IRT.blend`](IRT/IRT.blend) (0.1 MB) |
| <img src="preview/KAZR.jpg" width="260"> | `INST_KAZR` | [`KAZR/KAZR.blend`](KAZR/KAZR.blend) (0.2 MB) |
| <img src="preview/LDIS.jpg" width="260"> | `INST_LDIS` | [`LDIS/LDIS.blend`](LDIS/LDIS.blend) (0.1 MB) |
| <img src="preview/MAWS.jpg" width="260"> | `INST_MAWS` | [`MAWS/MAWS.blend`](MAWS/MAWS.blend) (0.2 MB) |
| <img src="preview/MET.jpg" width="260"> | `INST_MET` | [`MET/MET.blend`](MET/MET.blend) (0.3 MB) |
| <img src="preview/MFR.jpg" width="260"> | `INST_MFR` | [`MFR/MFR.blend`](MFR/MFR.blend) (0.1 MB) |
| <img src="preview/MFRSR.jpg" width="260"> | `INST_MFRSR` | [`MFRSR/MFRSR.blend`](MFRSR/MFRSR.blend) (0.1 MB) |
| <img src="preview/MPL.jpg" width="260"> | `INST_MPL` | [`MPL/MPL.blend`](MPL/MPL.blend) (0.1 MB) |
| <img src="preview/MWR3C.jpg" width="260"> | `INST_MWR3C` | [`MWR3C/MWR3C.blend`](MWR3C/MWR3C.blend) (0.2 MB) |
| <img src="preview/RWP.jpg" width="260"> | `INST_RWP` | [`RWP/RWP.blend`](RWP/RWP.blend) (0.3 MB) |
| <img src="preview/SEBS.jpg" width="260"> | `INST_SEBS` | [`SEBS/SEBS.blend`](SEBS/SEBS.blend) (0.2 MB) |
| <img src="preview/SEBS.jpg" width="260"> | `INST_SEBS_4m` | [`SEBS/SEBS.blend`](SEBS/SEBS.blend) (0.2 MB) |
| <img src="preview/SIRS.jpg" width="260"> | `INST_SIRS` | [`SIRS/SIRS.blend`](SIRS/SIRS.blend) (0.3 MB) |
| <img src="preview/SONDE.jpg" width="260"> | `INST_SONDE` | [`SONDE/SONDE.blend`](SONDE/SONDE.blend) (0.2 MB) |
| <img src="preview/VDIS.jpg" width="260"> | `INST_VDIS` | [`VDIS/VDIS.blend`](VDIS/VDIS.blend) (0.1 MB) |
| <img src="preview/WB.jpg" width="260"> | `INST_WB` | [`WB/WB.blend`](WB/WB.blend) (0.2 MB) |
