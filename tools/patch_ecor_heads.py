"""Replace the ECOR sensor heads in instruments/ECOR/ECOR.blend (INST_ECOR and INST_ECOR_4m)
with the Gill WindMaster Pro 3 and a white LI-COR LI-7500DS (geometry in tools/ecor_heads.py).

    blender -b --factory-startup --python tools/patch_ecor_heads.py

Old objects named sonic_* and irga_* are removed from each ECOR collection and rebuilt in place,
positioned from the old parts (sonic base = old sonic mount, IRGA post foot = old irga_post),
using the materials already in the file so texture paths stay relative.
"""
import bpy, bmesh, math, os, re, sys
from mathutils import Vector, Matrix, Euler
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ecor_heads import windmaster, li7500ds

REPO = os.path.dirname(HERE)
BLEND = os.path.join(REPO, 'instruments', 'ECOR', 'ECOR.blend')
bpy.ops.wm.open_mainfile(filepath=BLEND)
COMPRESSED = open(BLEND, 'rb').read(7) != b'BLENDER'
base = lambda n: re.sub(r'\.\d{3}$', '', n)
MATS = {}
for m in bpy.data.materials:
    MATS.setdefault(base(m.name), m)
M = {k: MATS[k] for k in ('stainless', 'aluminum', 'black_plastic', 'white_plastic', 'grey_plastic', 'black_anod', 'lens_dark')}
CUR = {}


def _finish(ob, mat, smooth=True):
    if mat is not None:
        ob.data.materials.append(mat)
    CUR['coll'].objects.link(ob)
    ob.parent = CUR['root']; ob.matrix_parent_inverse = Matrix.Identity(4)
    if smooth and ob.type == 'MESH':
        for p in ob.data.polygons:
            p.use_smooth = True
        md = ob.modifiers.new('WN', 'WEIGHTED_NORMAL'); md.keep_sharp = True
    return ob


def _mesh(name, bm):
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    return bpy.data.objects.new(name, me)


def box(name, size, loc=(0, 0, 0), rot=(0, 0, 0), mat=None, bevel=0, parent=None):
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0); bmesh.ops.scale(bm, vec=Vector(size), verts=bm.verts)
    ob = _mesh(name, bm); ob.location = loc; ob.rotation_euler = Euler([math.radians(a) for a in rot])
    return _finish(ob, mat, smooth=False)


def cyl(name, r, depth, loc=(0, 0, 0), rot=(0, 0, 0), mat=None, verts=48, bevel=0, r2=None, parent=None):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=verts, radius1=r, radius2=r if r2 is None else r2, depth=depth)
    ob = _mesh(name, bm); ob.location = loc; ob.rotation_euler = Euler([math.radians(a) for a in rot])
    return _finish(ob, mat)


def rod(name, p0, p1, r, mat=None, verts=16, parent=None, bevel=0):
    p0, p1 = Vector(p0), Vector(p1); d = p1 - p0
    ob = cyl(name, r, d.length, loc=(p0 + p1) / 2, mat=mat, verts=verts)
    ob.rotation_mode = 'QUATERNION'; ob.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d.normalized())
    return ob


def lathe(name, profile, loc=(0, 0, 0), rot=(0, 0, 0), mat=None, steps=64, parent=None, bevel=0):
    bm = bmesh.new()
    vs = [bm.verts.new((r, 0, z)) for r, z in profile]
    es = [bm.edges.new((vs[i], vs[i + 1])) for i in range(len(vs) - 1)]
    bmesh.ops.spin(bm, geom=vs + es, cent=(0, 0, 0), axis=(0, 0, 1), angle=math.tau, steps=steps, use_merge=True)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6); bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    ob = _mesh(name, bm); ob.location = loc; ob.rotation_euler = Euler([math.radians(a) for a in rot])
    return _finish(ob, mat)


def cable(name, pts, r=0.006, mat=None, parent=None):
    cu = bpy.data.curves.new(name, 'CURVE'); cu.dimensions = '3D'
    cu.bevel_depth = r; cu.bevel_resolution = 3; cu.use_fill_caps = True
    sp = cu.splines.new('BEZIER'); sp.bezier_points.add(len(pts) - 1)
    for bp, p in zip(sp.bezier_points, pts):
        bp.co = p; bp.handle_left_type = bp.handle_right_type = 'AUTO'
    ob = bpy.data.objects.new(name, cu)
    if mat: cu.materials.append(mat)
    CUR['coll'].objects.link(ob); ob.parent = CUR['root']; ob.matrix_parent_inverse = Matrix.Identity(4)
    return ob


def text(name, body, size, loc=(0, 0, 0), rot=(90, 0, 0), mat=None, parent=None):
    cu = bpy.data.curves.new(name, 'FONT'); cu.body = body; cu.size = size; cu.extrude = 0.0005
    cu.align_x = 'CENTER'; cu.align_y = 'CENTER'
    ob = bpy.data.objects.new(name, cu); ob.location = loc; ob.rotation_euler = Euler([math.radians(a) for a in rot])
    if mat: cu.materials.append(mat)
    CUR['coll'].objects.link(ob); ob.parent = CUR['root']; ob.matrix_parent_inverse = Matrix.Identity(4)
    return ob


H = dict(cyl=cyl, lathe=lathe, cable=cable, rod=rod, box=box, text=text)
for coll in [c for c in bpy.data.collections if re.fullmatch(r'INST_ECOR(_4m)?', c.name)]:
    root = next(o for o in coll.objects if base(o.name) == 'ECOR_root')
    obs = {base(o.name): o for o in coll.objects}
    mt = obs['sonic_mount_tube'] if 'sonic_mount_tube' in obs else None
    if mt is not None:
        sb = mt.location - Vector((0, 0, 0.07))
    else:                                   # already patched: flange sits 4 mm above the base
        sb = obs['sonic_flange'].location - Vector((0, 0, 0.004))
    ip = obs['irga_post']
    ib = ip.location - Vector((0, 0, ip.dimensions.z / 2)) if ip.rotation_mode != 'QUATERNION' else \
        ip.location - (ip.rotation_quaternion @ Vector((0, 0, 0.18)))
    gone = [o for o in coll.objects if re.match(r'(sonic|irga)_', base(o.name))]
    for o in gone:
        bpy.data.objects.remove(o, do_unlink=True)
    CUR.update(coll=coll, root=root)
    windmaster(H, M, sb, pro=True)
    li7500ds(H, M, ib)
    print(f'PATCHED {coll.name}: removed {len(gone)}, sonic base {tuple(round(v, 3) for v in sb)}, irga foot {tuple(round(v, 3) for v in ib)}')
    if isinstance(root.get('sources'), str):
        root['sources'] = root['sources'].replace('Gill WindMaster Pro datasheet (750 x 240 mm)',
                                                  'Gill WindMaster Pro datasheet 1561-0012 iss 8 (750 x 240 mm, 254/233 mm hub spacing)')
for blk in (bpy.data.meshes, bpy.data.curves):
    for b in list(blk):
        if b.users == 0:
            blk.remove(b)
bpy.ops.wm.save_as_mainfile(filepath=BLEND, compress=COMPRESSED)
print('SAVED', BLEND)
