"""S1: mount the SEBS on the corn-field ECOR tower (DERECHOS shared ECOR/SEBS tower).

    blender -b --factory-startup --python tools/patch_s1_sebs.py

Replaces the stand-alone SEBS instance (SEBS_FRUI4) with an INST_SEBS_4m instance at the
transform of ECOR_Corn (an INST_ECOR_4m tower), linked from instruments/SEBS/SEBS.blend.
"""
import bpy, os
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(REPO, 'scenes/S1/S1.blend')
bpy.ops.wm.open_mainfile(filepath=F)
D = bpy.data
ecor = D.objects['ECOR_Corn']
assert ecor.instance_collection.name.startswith('INST_ECOR_4m'), ecor.instance_collection.name
old = D.objects.get('SEBS_FRUI4')
c4 = next((c for c in D.collections if c.name == 'INST_SEBS_4m'), None)
if c4 is None:
    with D.libraries.load('//../../instruments/SEBS/SEBS.blend', link=True, relative=True) as (src, dst):
        dst.collections = ['INST_SEBS_4m']
    c4 = dst.collections[0]
sebs = D.objects.get('SEBS_Corn') or D.objects.new('SEBS_Corn', None)
sebs.instance_type = 'COLLECTION'; sebs.instance_collection = c4
sebs.empty_display_size = 0.5
for c in (old.users_collection if old else ecor.users_collection):
    if sebs.name not in c.objects:
        c.objects.link(sebs)
sebs.parent = ecor.parent
sebs.matrix_parent_inverse = ecor.matrix_parent_inverse.copy()
sebs.matrix_basis = ecor.matrix_basis.copy()
if old:
    D.objects.remove(old, do_unlink=True)
bpy.data.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
bpy.context.view_layer.update()
print('SEBS_Corn at', [round(v, 2) for v in sebs.matrix_world.translation], 'ECOR_Corn at', [round(v, 2) for v in ecor.matrix_world.translation])
bpy.ops.wm.save_as_mainfile(filepath=F, compress=True)
print('SAVED', F)
