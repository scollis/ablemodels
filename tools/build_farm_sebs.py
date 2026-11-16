"""SEBS - Surface Energy Balance System, DERECHOS configuration: shares the ECOR tower.

Instrument mentor (2026-11-16): one shared tripod/tower for ECOR and SEBS; Kipp & Zonen CNR4 net
radiometer in a CNF4 ventilation unit; LI-7500DS IRGA (in the ECOR asset); Vaisala rain detector
(DRD11A) as the wetness sensor; soil sensors for DERECHOS = Hukseflux HFP01 heat-flux plates and
Stevens HydraProbe soil moisture/temperature probes.

This asset therefore has no mast of its own. Its origin is the ECOR tower centre and it overlays the
ECOR asset (instance both at the same transform). INST_SEBS fits INST_ECOR (boom at 2.75 m);
INST_SEBS_4m fits INST_ECOR_4m (everything above ground raised 0.60 m).

  * CNR4 + CNF4: on a 0.45 m south-pointing rod at the east end of a 0.9 m crossarm clamped on top
    of the ECOR boom 1.2 m out, so the radiometer sits ~1.6 m south / 0.85 m east of the tower,
    clear of the sonic and IRGA, upward sensors level, downward sensors over the soil plot.
  * DRD11A: on the top of the boom 1.6 m out, plate tilted 30 deg to drain south (Vaisala manual).
  * Three soil sets under the radiometer footprint (E-W line, 0.4 m apart): HFP01 plate (80 mm dia,
    5 mm) flat at 5 cm depth, HydraProbe (42 mm x 124 mm body, four 58 mm tines) horizontal with the
    tines at 2.5 cm in undisturbed soil; leads in shallow trenches to a conduit up the tower.
  * SEBS logger enclosure (CR1000X) on the tower's north side below the ECOR enclosure.
Refs: ARM SEBS handbook DOE/SC-ARM-TR-092; Kipp & Zonen CNR4/CNF4 manual; Vaisala DRD11A datasheet;
Hukseflux HFP01 manual (80 mm x 5 mm); Stevens HydraProbe manual (body 4.2 x 12.4 cm, tines 5.8 cm).
"""
import sys, math, os
sys.path.insert(0, '/Users/scollis/Documents/Blender/farm_amf2/scripts/instr')
from inst_common import *
from inst_common import _STATE
import bpy
from mathutils import Vector, Matrix

# ECOR tower frame (must match build_ecor.py)
BOOM_Z = 2.75
BOOM_Y0 = -0.09
RR = 0.30 / math.sqrt(3)
ECOR_ENC_Z = 1.25
BR = 0.024                   # boom radius

ID = 'SEBS'
root = reset(ID)
M = lib()
soil = pbr('soil_disturbed', 'Ground037', tint=(0.17, 0.12, 0.08), tint_mix=0.85, scale=1.5, metallic=0.0, normal_strength=0.8)
conduit = pbr('pvc_grey', None, base_color=(0.42, 0.43, 0.44), metallic=0.0, roughness=0.5)
fglass = pbr('fibreglass_white', 'Plastic013A', tint=(0.86, 0.86, 0.83), tint_mix=0.85, scale=3.0, metallic=0.0)
kz_white = pbr('kz_white', None, base_color=(0.9, 0.9, 0.9), metallic=0.0, roughness=0.35)
drd_plate_m = pbr('drd_plate', None, base_color=(0.15, 0.17, 0.2), metallic=0.3, roughness=0.15)
hfp_m = pbr('hfp01_black', None, base_color=(0.03, 0.03, 0.03), metallic=0.0, roughness=0.35)
hydra_m = pbr('hydraprobe_body', None, base_color=(0.78, 0.78, 0.74), metallic=0.0, roughness=0.45)


def orient(ob, d):
    ob.rotation_mode = 'QUATERNION'
    ob.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(Vector(d).normalized())
    return ob


def build(dz):
    Z = BOOM_Z + dz
    # ------------------------------------------------ radiometer crossarm on top of the boom
    CY, CX1 = -1.20, 0.90
    AZ = Z + BR + 0.018                      # crossarm centreline, sitting on the boom
    box('rad_crossarm', (CX1 + 0.08, 0.032, 0.032), loc=((CX1 - 0.08) / 2, CY, AZ), mat=M['aluminum'], bevel=0.003)
    box('rad_crossover_plate', (0.10, 0.10, 0.008), loc=(0, CY, Z + BR + 0.002), mat=M['aluminum'], bevel=0.002)
    for dx in (-0.035, 0.035):
        tube(f'rad_crossover_ubolt_{dx}', BR + 0.007, BR + 0.002, 0.012, loc=(dx, CY, Z), rot=(90, 0, 0), mat=M['stainless'], verts=24)
    cyl('rad_crossarm_cap', 0.018, 0.008, loc=(CX1 + 0.004, CY, AZ), rot=(0, 90, 0), mat=M['black_plastic'], verts=16)
    # ------------------------------------------------ CNR4 + CNF4 on a south-pointing rod
    RX = CX1 - 0.05
    TIPY = CY - 0.45
    rod('cnr4_rod', (RX, CY, AZ), (RX, TIPY + 0.08, AZ), 0.009, M['anodized_al'], verts=16)
    box('cnr4_rod_clamp', (0.05, 0.06, 0.05), loc=(RX, CY, AZ), mat=M['aluminum'], bevel=0.004)
    for dx in (-0.016, 0.016):
        cyl(f'cnr4_clamp_bolt_{dx}', 0.004, 0.06, loc=(RX + dx, CY, AZ), mat=M['stainless'], verts=8)
    cn = group('cnr4', loc=(RX, TIPY, AZ))
    # CNF4 ventilation unit: white housing round the rod end with intake grille
    box('cnf4_body', (0.11, 0.12, 0.085), loc=(0, 0.11, -0.005), mat=kz_white, bevel=0.012, parent=cn)
    for k in range(5):
        box(f'cnf4_grille_{k}', (0.09, 0.004, 0.006), loc=(0, 0.11 - 0.061, -0.03 + 0.012 * k), mat=M['black_plastic'], bevel=0, parent=cn)
    cyl('cnf4_conn', 0.009, 0.02, loc=(0.05, 0.15, -0.045), mat=M['stainless'], verts=12, parent=cn)
    box('cnr4_body', (0.06, 0.07, 0.05), loc=(0, 0.02, 0), mat=M['anodized_al'], bevel=0.006, parent=cn)
    SX = 0.062
    for sx, kind in ((-1, 'cmp3'), (1, 'cgr3')):
        x = sx * SX
        cyl(f'{kind}_housing', 0.034, 0.05, loc=(x, 0, 0), mat=M['anodized_al'], bevel=0.004, parent=cn)
        box(f'{kind}_web', (0.04, 0.04, 0.03), loc=(sx * 0.035, 0.0, 0), mat=M['anodized_al'], bevel=0.003, parent=cn)
        for zz, sgn in ((0.025, 1), (-0.025, -1)):
            nm = f'{kind}_{"up" if sgn > 0 else "dn"}'
            cyl(nm + '_ring', 0.024, 0.006, loc=(x, 0, zz + sgn * 0.003), mat=M['stainless'], parent=cn)
            if kind == 'cmp3':
                sphere(nm + '_dome', 0.0125, loc=(x, 0, zz + sgn * 0.006), mat=M['dome'], hemi=True, rot=(0 if sgn > 0 else 180, 0, 0), parent=cn)
                cyl(nm + '_sensor', 0.007, 0.001, loc=(x, 0, zz + sgn * 0.0065), mat=M['black_body'], parent=cn)
            else:
                cyl(nm + '_window', 0.016, 0.004, loc=(x, 0, zz + sgn * 0.0075), mat=M['lens_dark'], parent=cn)
    for sx in (-1, 1):
        tube(f'cnr4_shield_ring_{sx}', 0.06, 0.026, 0.003, loc=(sx * SX, 0, 0.0285), mat=kz_white, verts=48, parent=cn)
    box('cnr4_shield_bridge', (0.02, 0.10, 0.003), loc=(0, 0, 0.0285), mat=kz_white, bevel=0.0008, parent=cn)
    for sx in (-1, 1):
        for sy in (-1, 1):
            cyl(f'cnr4_shield_post_{sx}{sy}', 0.003, 0.012, loc=(sx * 0.03, sy * 0.025, 0.022), mat=M['stainless'], verts=8, parent=cn)
    cyl('cnr4_level', 0.009, 0.006, loc=(0, 0.045, 0.028), mat=M['glass'], parent=cn)
    # ------------------------------------------------ Vaisala DRD11A rain detector on top of the boom
    dy = -1.60
    cyl('drd_post', 0.009, 0.10, loc=(0, dy, Z + BR + 0.05), mat=M['stainless'], verts=12)
    box('drd_clamp', (0.045, 0.04, 0.02), loc=(0, dy, Z + BR + 0.008), mat=M['stainless'], bevel=0.002)
    drd = group('drd11a', loc=(0, dy, Z + BR + 0.115), rot=(-30, 0, 0))
    box('drd_body', (0.06, 0.10, 0.018), loc=(0, 0, 0), mat=M['grey_plastic'], bevel=0.003, parent=drd)
    box('drd_plate', (0.052, 0.085, 0.003), loc=(0, 0, 0.0095), mat=drd_plate_m, bevel=0.0005, parent=drd)
    for k in range(6):
        box(f'drd_grid_{k}', (0.046, 0.002, 0.0006), loc=(0, -0.035 + 0.014 * k, 0.011), mat=M['brass'], bevel=0, parent=drd)
    cyl('drd_conn', 0.008, 0.02, loc=(0, 0.06, -0.004), rot=(90, 0, 0), mat=M['black_plastic'], verts=12, parent=drd)
    # ------------------------------------------------ cables: along the crossarm and boom underside, down the tower
    down = Vector((0.03, BOOM_Y0 - 0.05, Z - 0.30))
    cable('cnr4_cable', [Vector((RX + 0.03, TIPY + 0.15, AZ - 0.035)), Vector((RX + 0.02, CY - 0.05, AZ - 0.03)),
                         Vector((0.5, CY - 0.02, AZ - 0.022)), Vector((0.05, CY, Z - BR - 0.006)), Vector((0.03, -0.6, Z - BR - 0.006)),
                         Vector((0.03, -0.25, Z - BR - 0.008)), down], r=0.0035, mat=M['cable'])
    cable('drd_cable', [Vector((0, dy + 0.03, Z + BR + 0.06)), Vector((0.02, dy + 0.06, Z)), Vector((0.035, -0.45, Z - BR - 0.006)),
                        Vector((0.035, -0.2, Z - BR - 0.01)), down + Vector((0.01, 0, 0))], r=0.003, mat=M['cable'])
    return Vector((RX, TIPY, 0))


def enclosure_and_soil(rad_xy):
    # ------------------------------------------------ SEBS logger enclosure, tower north side below the ECOR box
    EB = (0.36, 0.20, 0.46)
    EZ = 0.62
    ey = RR + 0.06 + EB[1] / 2
    for dz in (-0.16, 0.16):
        tube(f'enc_ubolt_{dz}', 0.024, 0.018, 0.014, loc=(0, RR, EZ + dz), mat=M['stainless'], verts=24)
        box(f'enc_rail_{dz}', (0.30, 0.04, 0.03), loc=(0, RR + 0.04, EZ + dz), mat=M['galvanized'], bevel=0.002)
    box('enclosure', EB, loc=(0, ey, EZ), mat=fglass, bevel=0.012)
    box('enc_door', (EB[0] - 0.02, 0.012, EB[2] - 0.02), loc=(0, ey + EB[1] / 2 + 0.004, EZ), mat=fglass, bevel=0.005)
    for dz in (-0.16, 0.16):
        cyl(f'enc_hinge_{dz}', 0.007, 0.045, loc=(-EB[0] / 2 + 0.006, ey + EB[1] / 2 + 0.012, EZ + dz), mat=M['stainless'], verts=10)
        box(f'enc_latch_{dz}', (0.02, 0.016, 0.05), loc=(EB[0] / 2 - 0.02, ey + EB[1] / 2 + 0.014, EZ + dz), mat=M['stainless'])
    box('enc_label', (0.14, 0.002, 0.045), loc=(0, ey + EB[1] / 2 + 0.011, EZ + 0.13), mat=M['label'], bevel=0)
    text('enc_text', 'SEBS', 0.03, loc=(0, ey + EB[1] / 2 + 0.0125, EZ + 0.13), rot=(90, 0, 180), mat=M['label_ink'])
    box('enc_arm', (0.08, 0.002, 0.08), loc=(0, ey + EB[1] / 2 + 0.011, EZ - 0.02), mat=M['arm_blue'], bevel=0)
    text('enc_arm_txt', 'ARM', 0.026, loc=(0, ey + EB[1] / 2 + 0.0125, EZ - 0.02), rot=(90, 0, 180), mat=M['white_plastic'])
    for i, x in enumerate((-0.12, -0.06, 0.0, 0.06, 0.12)):
        cyl(f'enc_gland_{i}', 0.011, 0.022, loc=(x, ey, EZ - EB[2] / 2 - 0.011), mat=M['grey_plastic'], verts=14)
    # ------------------------------------------------ soil sets under the radiometer footprint
    PY = rad_xy.y - 0.12
    sets = [Vector((rad_xy.x - 0.40, PY, 0)), Vector((rad_xy.x, PY - 0.05, 0)), Vector((rad_xy.x + 0.40, PY, 0))]
    J = Vector((0.10, -0.16, 0))                 # conduit foot at the tower's south face
    tines = [Vector((0, 0, 0))] + [Vector((0.0145 * math.cos(a), 0, 0.0145 * math.sin(a))) for a in (math.pi / 2, math.pi / 2 + math.tau / 3, math.pi / 2 + 2 * math.tau / 3)]
    for i, s in enumerate(sets):
        pit = cyl(f'soil_pit_{i}', 0.17, 0.012, loc=(s.x, s.y, 0.002), mat=soil, verts=24, bevel=0.004)
        pit.scale = (1.0, 0.75, 1.0)
        # Hukseflux HFP01: 80 mm x 5 mm plate, flat at 5 cm, lead out of the side
        hp = Vector((s.x + 0.06, s.y - 0.02, -0.05))
        cyl(f'hfp01_plate_{i}', 0.040, 0.005, loc=hp, mat=hfp_m, verts=40, bevel=0.0012)
        cyl(f'hfp01_guard_{i}', 0.0195, 0.0052, loc=hp, mat=M['black_plastic'], verts=24, bevel=0.0008)
        cable(f'hfp01_lead_{i}', [hp + Vector((0, 0.04, 0)), hp + Vector((0, 0.10, 0.01)), Vector((s.x + 0.04, s.y + 0.16, -0.03)),
                                  Vector((s.x + 0.02, s.y + 0.22, -0.02))], r=0.0022, mat=M['cable'])
        # Stevens HydraProbe: body 42 x 124 mm horizontal, tines (4 x 58 mm) at 2.5 cm pointing south
        hy = Vector((s.x - 0.07, s.y + 0.03, -0.025))
        body = cyl(f'hydraprobe_body_{i}', 0.021, 0.124, loc=hy + Vector((0, 0.062, 0)), rot=(90, 0, 0), mat=hydra_m, verts=32, bevel=0.002)
        cyl(f'hydraprobe_base_{i}', 0.021, 0.006, loc=hy + Vector((0, 0.003, 0)), rot=(90, 0, 0), mat=M['black_plastic'], verts=32)
        for k, t in enumerate(tines):
            rod(f'hydraprobe_tine_{i}_{k}', hy + t, hy + t + Vector((0, -0.058, 0)), 0.0015, M['stainless'], verts=8)
        cable(f'hydraprobe_lead_{i}', [hy + Vector((0, 0.124, 0)), hy + Vector((0, 0.17, 0.005)), Vector((s.x - 0.02, s.y + 0.22, -0.02))],
              r=0.0025, mat=M['cable'])
        # survey flag marking the set
        rod(f'flag_wire_{i}', (s.x + 0.14, s.y - 0.10, 0.0), (s.x + 0.14, s.y - 0.10, 0.38), 0.0015, M['stainless'], verts=6)
        box(f'flag_{i}', (0.002, 0.09, 0.065), loc=(s.x + 0.14, s.y - 0.10 + 0.045, 0.345), mat=M['yellow_paint'], bevel=0)
        # leads bundle in a shallow back-filled trench to the conduit at the tower
        a = Vector((s.x, s.y + 0.22, 0))
        cable(f'soil_lead_{i}', [Vector((s.x, s.y + 0.22, -0.02)), (a + J) / 2 + Vector((0, 0, -0.02)), J + Vector((0, -0.03, -0.015))],
              r=0.0035, mat=M['cable'])
        d = J - a
        t = box(f'soil_trench_{i}', (0.07, d.length, 0.006), loc=(a + d / 2) + Vector((0, 0, 0.0005 + 0.0007 * i)), mat=soil, bevel=0.002)
        t.rotation_euler = (0, 0, math.atan2(-d.x, d.y))
    cyl('soil_conduit_elbow', 0.022, 0.06, loc=(J.x, J.y, 0.02), mat=conduit, verts=20)
    cable('soil_conduit', [(J.x, J.y, 0.03), (J.x, J.y + 0.02, 0.2), (0.10, 0.0, 0.32), (0.06, ey - 0.05, EZ - EB[2] / 2 - 0.12),
                           (0.06, ey, EZ - EB[2] / 2 - 0.022)], r=0.014, mat=conduit)
    # radiometer + DRD cables come down the tower's south face into the enclosure
    cable('arm_to_enc', [(0.035, BOOM_Y0 - 0.05, BOOM_Z - 0.30), (0.08, -0.09, 1.6), (0.08, -0.09, 1.0), (-0.06, 0.05, 0.75),
                         (-0.06, ey, EZ - EB[2] / 2 - 0.022)], r=0.0045, mat=M['cable'])
    return ey


# ---------------- INST_SEBS (fits INST_ECOR)
rad = build(0.0)
ey = enclosure_and_soil(rad)
meta(instrument='SEBS', full_name='Surface Energy Balance System', sites=['M1', 'S1'],
     sources=['ARM SEBS handbook DOE/SC-ARM-TR-092', 'DERECHOS SEBS mentor configuration (2026-11-16): shared ECOR tower, CNR4/CNF4, DRD11A, HFP01, HydraProbe',
              'Kipp & Zonen CNR4/CNF4 manual', 'Vaisala DRD11A datasheet', 'Hukseflux HFP01 manual (80 x 5 mm)',
              'Stevens HydraProbe manual (4.2 x 12.4 cm body, 5.8 cm tines)'],
     notes='No mast of its own: overlay on INST_ECOR at the same transform (origin = ECOR tower centre). '
           'CNR4+CNF4 at the end of a 0.9 m crossarm on the ECOR boom (~0.85 m E, 1.65 m S of the tower, 2.8 m AGL); '
           'DRD11A on the boom 1.6 m out; 3 soil sets (HFP01 at 5 cm, HydraProbe at 2.5 cm) under the radiometer; '
           'logger enclosure on the tower north side at 0.6 m.',
     height_m=round(BOOM_Z + 0.25, 2))

# context for previews: the ECOR tower (linked, presentation only)
ctx = bpy.data.collections.new('_Context_SEBS'); bpy.context.scene.collection.children.link(ctx)
EC = '/Users/scollis/Documents/Blender/farm_amf2/assets/instruments/ECOR/ECOR.blend'
with bpy.data.libraries.load(EC, link=True) as (src, dst):
    dst.collections = ['INST_ECOR']
inst = bpy.data.objects.new('ECOR_context', None); inst.instance_type = 'COLLECTION'
inst.instance_collection = dst.collections[0]; ctx.objects.link(inst)

finish(stage_kw=dict(pad_r=2.0), cam_kw=dict(elev_deg=16, lens=40, margin=1.15, target_frac=0.45),
       preview_kw=[dict(azimuths=(-35, 55, 145, 235)),
                   dict(azimuths=(-60, 150), zoom=0.35, target=(rad.x, rad.y, BOOM_Z), elev=15, tag='head'),
                   dict(azimuths=(-20, 160), zoom=0.45, target=(rad.x, rad.y, 0.1), elev=35, tag='soil')])
# buried-sensor check view: hide the ground and the back-fill so the HFP01s and HydraProbes show
hid = [o for o in bpy.data.objects if o.name == 'StageGround' or o.name.startswith(('soil_pit_', 'soil_trench_'))]
for o in hid:
    o.hide_render = True
preview(azimuths=(200, 340), zoom=0.12, target=(rad.x, rad.y - 0.1, -0.03), elev=8, tag='buried')
for o in hid:
    o.hide_render = False
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath, compress=True)

# ---------------- INST_SEBS_4m (fits INST_ECOR_4m: boom 0.60 m higher), built after the previews
main_coll, main_root = _STATE['coll'], _STATE['root']
c4 = bpy.data.collections.new('INST_SEBS_4m')
bpy.context.scene.collection.children.link(c4)
r4 = bpy.data.objects.new('SEBS_root_4m', None); r4.empty_display_type = 'ARROWS'; r4.empty_display_size = 0.5
c4.objects.link(r4)
_STATE.update(coll=c4, root=r4)
rad4 = build(0.60)
enclosure_and_soil(rad4)
for key in main_root.keys():
    r4[key] = main_root[key]
r4['notes'] = main_root['notes'].replace('INST_ECOR', 'INST_ECOR_4m') + ' 4 m tower variant: above-ground parts +0.60 m.'
r4['height_m'] = round(BOOM_Z + 0.85, 2)
c4.use_fake_user = True
_STATE.update(coll=main_coll, root=main_root)
bpy.context.scene.collection.children.unlink(c4)
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath, compress=True)
print('SAVED_4M')
