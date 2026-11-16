"""Copy an instrument asset built in the farm_amf2 workspace into this library.

    blender -b --factory-startup --python tools/port_farm_instrument.py -- <farm .blend> <NAME>

Keeps the INST_<NAME>* collections (asset-marked, fake user, not linked to a scene), drops the
presentation stage/context collections and any linked libraries, and rewrites texture paths from
the workspace's _tex folder to textures/pbr/ (relative). Fails if a texture is missing here.
Writes instruments/<NAME>/<NAME>.blend and refreshes each root's bbox_min/bbox_max.
"""
import bpy, os, sys, json, re
from mathutils import Vector

a = sys.argv[sys.argv.index('--') + 1:]
SRC, NAME = a[0], a[1]
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, 'instruments', NAME, NAME + '.blend')
bpy.ops.wm.open_mainfile(filepath=SRC)

for lib in list(bpy.data.libraries):
    bpy.data.libraries.remove(lib)
keep = [c for c in bpy.data.collections if re.fullmatch(rf'INST_{NAME}(_\w+)?', c.name)]
assert keep, 'no INST_%s collections' % NAME
for c in list(bpy.data.collections):
    if c not in keep:
        for o in list(c.objects):
            if not any(o.name in k.objects for k in keep):
                bpy.data.objects.remove(o, do_unlink=True)
        bpy.data.collections.remove(c)
sc = bpy.context.scene
for c in keep:
    if c.name in sc.collection.children:
        sc.collection.children.unlink(c)
    c.use_fake_user = True
    if not c.asset_data:
        c.asset_mark()
for o in list(sc.collection.objects):
    bpy.data.objects.remove(o, do_unlink=True)
sc.world = None
bpy.data.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)

missing = []
for im in bpy.data.images:
    if not im.filepath:
        continue
    p = im.filepath.replace('\\', '/')
    m = re.search(r'_tex/(.+)$', p)
    if m:
        rel = 'textures/pbr/' + m.group(1)
        if not os.path.exists(os.path.join(REPO, rel)):
            missing.append(rel)
        im.filepath = '//../../' + rel
assert not missing, 'textures missing from the library: %s' % sorted(set(missing))

for c in keep:
    sc.collection.children.link(c)
bpy.context.view_layer.update()
dg = bpy.context.evaluated_depsgraph_get()
for c in keep:
    root = next(o for o in c.objects if o.name.startswith(NAME + '_root'))
    mn = Vector((1e9,) * 3); mx = Vector((-1e9,) * 3)
    for o in c.all_objects:
        if o.type not in ('MESH', 'FONT'):          # bezier cables' bounds include handles
            continue
        oe = o.evaluated_get(dg)
        for b in oe.bound_box:
            w = oe.matrix_world @ Vector(b)
            mn = Vector(map(min, mn, w)); mx = Vector(map(max, mx, w))
    root['bbox_min'] = json.dumps([round(v, 3) for v in mn])
    root['bbox_max'] = json.dumps([round(v, 3) for v in mx])
    print('PORTED', c.name, len(c.all_objects), 'objects; bbox', root['bbox_min'], root['bbox_max'])
for c in keep:
    sc.collection.children.unlink(c)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=OUT, compress=True, relative_remap=False)
print('SAVED', OUT)
