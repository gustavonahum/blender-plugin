import bpy

# Comprimentos (x, y e z) do degrau superior
length1 = 3
length2 = 2
length3 = 1

# Quantidade de degraus
steps = 5

def criaDegrau(length1, length2, length3, times):
    if times == 0:
        return times
    
    # Replica o andar imediatamente superior e faz as translações necessárias para o degrau seguinte
    bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":"TRANSLATION"}, TRANSFORM_OT_translate={"value":(0,0,-length3)})
    bpy.ops.transform.translate(value=(length1/2,0,0))
    bpy.ops.transform.translate(value=(0,length2/2,0))
    bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":"TRANSLATION"}, TRANSFORM_OT_translate={"value":(-length1,0,0)})
    bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":"TRANSLATION"}, TRANSFORM_OT_translate={"value":(0,-length2,0)})
    bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":"TRANSLATION"}, TRANSFORM_OT_translate={"value":(length1,0,0)})

    # Une os elementos em um MESH
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.join()
    
    # Elimina eventuais repetições de elementos, para evitar sobrecarregar o peso do programa
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='TOGGLE')
    bpy.ops.mesh.remove_doubles()
    bpy.ops.mesh.select_all(action='TOGGLE')
    bpy.ops.object.editmode_toggle()
    
    # Repete o processo para o degrau seguinte
    times = times - 1
    criaDegrau(length1, length2, length3, times)


 
# Define os vértices e faces
verts = [(0,0,0),(0,length2,0),(length1,length2,0),(length1,0,0),(0,0,length3),(0,length2,length3),(length1,length2,length3),(length1,0,length3)]
faces = [(0,1,2,3), (4,5,6,7), (0,4,5,1), (1,5,6,2), (2,6,7,3), (3,7,4,0)]
 
# Define o mesh e o objeto
mesh = bpy.data.meshes.new("Paralelepipedo")
object = bpy.data.objects.new("Paralelepipedo", mesh)
 
#Set location and scene of object
object.location = bpy.context.scene.cursor_location
bpy.context.scene.objects.link(object)
 
# Cria o mesh
mesh.from_pydata(verts,[],faces)
mesh.update(calc_edges=True)

# Ativa o objeto, para ser usado nas seguintes recursões
bpy.context.scene.objects.active = object

criaDegrau(length1, length2, length3, steps)
 
 
