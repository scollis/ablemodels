"""ECOR sensor heads: Gill WindMaster 3-axis sonic + LI-COR LI-7500DS open-path IRGA.

Shared by build_ecor.py (farm asset) and patch_ecor_heads.py (ablemodels repo blend).
Geometry from the Gill WindMaster Pro datasheet 1561-0012 iss 8 (2022) dimension drawing:
  overall 750 mm; base flange 100 mm dia; body 57 mm dia; 254 mm from body top to the lower
  transducer hub; 233 mm from the lower hub to the top; three rectangular support frames
  reaching a 240 mm diameter; three lower transducers on arms rising from the lower hub and
  three upper transducers on arms hanging from the upper hub, each pair facing across the axis.
Scott (2026-11-16): ARM uses the Gill WindMaster Pro 3 - all stainless body, stem, frames and
hub caps, with black transducer arms, transducers and hub collars (Gill product photo). `pro=False`
gives the aluminium/carbon WindMaster for other sites.
LI-7500DS: white sensor head, 65 mm housings, 125 mm open path, three struts.

All coordinates are in the instrument root's local frame (Z up, +Y = north = along the boom
toward the tower). `sb` is the sonic base (bottom of the flange); `hb` the IRGA head bottom.
The helper functions (cyl, lathe, cable, rod) come from inst_common and parent to the root.
"""
import math
from mathutils import Vector

# heights above the flange bottom (m)
WM_BODY_TOP = 0.263          # 750 - 233 - 254
WM_LOWER_HUB = 0.517         # body top + 254 mm
WM_UPPER_HUB = 0.739         # top hub centre (cap reaches 0.750)
WM_FRAME_R = 0.118           # frames reach a 240 mm circle (rod centreline)
WM_TIP_R = 0.068             # transducer face radius from the axis
WM_TIP_DZ = 0.052            # transducer face height above lower hub / below upper hub
WM_CENTRE = 0.5 * ((WM_LOWER_HUB + WM_TIP_DZ) + (WM_UPPER_HUB - WM_TIP_DZ))   # ~0.628


def _hdir(az):
    a = math.radians(az)
    return Vector((math.sin(a), math.cos(a), 0.0))


def _orient(ob, d):
    ob.rotation_mode = 'QUATERNION'
    ob.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(Vector(d).normalized())
    return ob


def windmaster(H, M, sb, pro=True):
    """H: dict of inst_common helpers (cyl, lathe, cable, rod, box, text). Returns measurement centre."""
    cyl, lathe, cable, rod, box, text = (H[k] for k in ('cyl', 'lathe', 'cable', 'rod', 'box', 'text'))
    sb = Vector(sb)
    body_m = M['stainless'] if pro else M['aluminum']
    stem_m = M['stainless'] if pro else M.get('carbon', M['black_anod'])
    frame_m = M['stainless'] if pro else M['aluminum']
    # base flange (3 bolts on an 85 mm pcd) + body tube with tapered top collar
    cyl('sonic_flange', 0.050, 0.008, loc=sb + Vector((0, 0, 0.004)), mat=body_m, verts=48)
    for k in range(3):
        h = _hdir(120 * k + 60)
        cyl(f'sonic_flange_bolt_{k}', 0.0055, 0.006, loc=sb + Vector((0, 0, 0.011)) + h * 0.0425, mat=M['stainless'], verts=6)
    lathe('sonic_body', [(0.0, 0.008), (0.0285, 0.008), (0.0285, 0.240), (0.0270, 0.248), (0.020, 0.256),
                         (0.016, WM_BODY_TOP), (0.0, WM_BODY_TOP)], loc=sb, mat=body_m, steps=48)
    # north alignment mark + notch on the flange (points along the boom to the tower = +Y)
    box('sonic_north_mark', (0.006, 0.003, 0.04), loc=sb + Vector((0, 0.0292, 0.05)), mat=M['black_plastic'], bevel=0)
    text('sonic_N', 'N', 0.014, loc=sb + Vector((0, 0.0300, 0.085)), rot=(90, 0, 180), mat=M['black_plastic'])
    cyl('sonic_connector', 0.012, 0.03, loc=sb + Vector((0.0, -0.035, 0.03)), rot=(90, 0, 0), mat=M['black_plastic'], verts=16)
    # slim stem up to the lower hub
    lathe('sonic_stem', [(0.0, WM_BODY_TOP - 0.004), (0.0105, WM_BODY_TOP - 0.004), (0.0105, WM_LOWER_HUB - 0.012),
                         (0.0, WM_LOWER_HUB - 0.012)], loc=sb, mat=stem_m, steps=24)
    # hubs (named sonic_head_hub = lower hub, used as an anchor by scene scripts)
    lathe('sonic_head_hub', [(0, WM_LOWER_HUB - 0.013), (0.016, WM_LOWER_HUB - 0.013), (0.022, WM_LOWER_HUB - 0.006),
                             (0.022, WM_LOWER_HUB + 0.008), (0.015, WM_LOWER_HUB + 0.013), (0, WM_LOWER_HUB + 0.013)],
          loc=sb, mat=body_m, steps=32)
    lathe('sonic_top_hub', [(0, WM_UPPER_HUB - 0.013), (0.015, WM_UPPER_HUB - 0.013), (0.022, WM_UPPER_HUB - 0.008),
                            (0.022, WM_UPPER_HUB + 0.006), (0.014, WM_UPPER_HUB + 0.011), (0, WM_UPPER_HUB + 0.0115)],
          loc=sb, mat=body_m, steps=32)
    # black transducer-mount collars: above the lower hub, below the top hub
    lathe('sonic_lower_collar', [(0, WM_LOWER_HUB + 0.010), (0.026, WM_LOWER_HUB + 0.010), (0.028, WM_LOWER_HUB + 0.016),
                                 (0.024, WM_LOWER_HUB + 0.024), (0, WM_LOWER_HUB + 0.024)], loc=sb, mat=M['black_plastic'], steps=32)
    lathe('sonic_upper_collar', [(0, WM_UPPER_HUB - 0.024), (0.024, WM_UPPER_HUB - 0.024), (0.028, WM_UPPER_HUB - 0.016),
                                 (0.026, WM_UPPER_HUB - 0.010), (0, WM_UPPER_HUB - 0.010)], loc=sb, mat=M['black_plastic'], steps=32)
    # three rectangular support frames (hub -> out -> up -> back in), at az 90/210/330
    zl, zu, R, rc = WM_LOWER_HUB, WM_UPPER_HUB, WM_FRAME_R, 0.012
    for i, az in enumerate((90, 210, 330)):
        h = _hdir(az)
        P = lambda r, z: sb + h * r + Vector((0, 0, z))
        pts = [P(0.018, zl), P(0.050, zl), P(R - rc - 0.03, zl), P(R - rc, zl), P(R - rc * 0.3, zl + rc * 0.3), P(R, zl + rc),
               P(R, zl + rc + 0.04), P(R, zu - rc - 0.04), P(R, zu - rc), P(R - rc * 0.3, zu - rc * 0.3), P(R - rc, zu),
               P(R - rc - 0.03, zu), P(0.050, zu), P(0.018, zu)]
        cable(f'sonic_frame_{i}', pts, r=0.0045, mat=frame_m)
    # transducers: lower at az 0/120/240 look up across the axis at upper ones at az 180/300/60
    for i, az in enumerate((0, 120, 240)):
        lo = sb + _hdir(az) * WM_TIP_R + Vector((0, 0, WM_LOWER_HUB + WM_TIP_DZ))
        hi = sb + _hdir(az + 180) * WM_TIP_R + Vector((0, 0, WM_UPPER_HUB - WM_TIP_DZ))
        path = (hi - lo).normalized()
        for kind, face, d_out, hub_z, haz in (('lo', lo, -path, WM_LOWER_HUB, az), ('hi', hi, path, WM_UPPER_HUB, az + 180)):
            body = cyl(f'sonic_xdcr_{kind}_{i}', 0.0085, 0.032, loc=face + d_out * 0.018, mat=M['black_plastic'], verts=20, bevel=0.0015)
            _orient(body, d_out)
            ring = cyl(f'sonic_xdcr_collar_{kind}_{i}', 0.0095, 0.008, loc=face + d_out * 0.032, mat=M['black_plastic'], verts=20, bevel=0.001)
            _orient(ring, d_out)
            back = face + d_out * 0.036
            root = sb + _hdir(haz) * 0.022 + Vector((0, 0, hub_z + (0.017 if kind == 'lo' else -0.017)))
            rod(f'sonic_arm_{kind}_{i}', root, back, 0.0048, M['black_plastic'], verts=12)
    return sb + Vector((0, 0, WM_CENTRE))


def li7500ds(H, M, ib):
    """LI-7500DS open-path IRGA: white upper and lower housings, dark windows, three struts.
    ib = foot of the IRGA post on the crossbar. Returns the head bottom point hb."""
    cyl, lathe, rod, box = (H[k] for k in ('cyl', 'lathe', 'rod', 'box'))
    ib = Vector(ib)
    rod('irga_post', ib, ib + Vector((0, 0, 0.36)), 0.0125, M['aluminum'], verts=16)
    tilt = math.radians(15)     # tilted ~15 deg (top leaning north) to shed water
    ax = Vector((0, math.sin(tilt), math.cos(tilt)))
    hb = ib + Vector((0, -0.04, 0.42))
    box('irga_clamp', (0.04, 0.06, 0.05), loc=ib + Vector((0, -0.02, 0.38)), mat=M['black_anod'], bevel=0.003)
    along = lambda d: hb + ax * d
    put = lambda ob: _orient(ob, ax)
    white = M['white_plastic']
    put(lathe('irga_lower', [(0, 0), (0.024, 0), (0.0325, 0.012), (0.0325, 0.105), (0.030, 0.118), (0.020, 0.122), (0, 0.122)],
              loc=hb, mat=white, steps=40))
    put(cyl('irga_lower_window', 0.019, 0.003, loc=along(0.1225), mat=M['lens_dark'], verts=32))
    put(cyl('irga_lower_band', 0.0329, 0.006, loc=along(0.016), mat=M['black_plastic'], verts=40))
    put(lathe('irga_upper', [(0, 0.247), (0.020, 0.247), (0.030, 0.252), (0.0325, 0.262), (0.0325, 0.285), (0.022, 0.30), (0, 0.302)],
              loc=hb, mat=white, steps=40))
    put(cyl('irga_upper_window', 0.019, 0.003, loc=along(0.2465), mat=M['lens_dark'], verts=32))
    perp1 = ax.cross(Vector((1, 0, 0))).normalized(); perp2 = ax.cross(perp1).normalized()
    for k in range(3):
        a = math.tau * k / 3 + 0.5
        off = (perp1 * math.cos(a) + perp2 * math.sin(a)) * 0.028
        rod(f'irga_spar_{k}', along(0.118) + off, along(0.252) + off, 0.0042, M['grey_plastic'], verts=10)
    put(cyl('irga_connector', 0.011, 0.03, loc=along(-0.012), mat=M['stainless'], verts=16))
    return hb
