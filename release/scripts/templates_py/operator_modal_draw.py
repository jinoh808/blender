#################################################################################################
# How to test?                                                                                  #
#  1. Run this script in text editor                                                            #
#  2. Locate mouse pointer on text editor and Press F3 key                                      #
#  3. Search operator with "bl_name"                                                            #
#    (In this case it's "Simple Modal Draw Operator")                                           #
#  4. Click "Simple Modal Draw Operator" and move mouse pointer!                                #
#    (First item is last added operator)                                                        #
#  5. Right click to finish test                                                                #
#                                                                                               #
# If you want to draw on other space.                                                           #
#  0. If you follow this instruction, you can draw on VIEW3D area                               #
#    (if you draw on other area which is not VIEW3D, check instrouction number 5 first)         #
#  1. Change 'TEXT_EDITOR' into 'VIEW_3D'                                                       # 
#  2. Change all "SpaceTextEditor" in script into "SpaceView3D"                                 #
#  3. Run script and move mouse pointer to VIEW3D                                               #
#  4. Follow the how to test instructions from number 2                                         #
#  5. you can check other possible options in this page                                         #
#     https://docs.blender.org/api/current/bpy.types.Space.html?highlight=space#bpy.types.Space #
#################################################################################################

import bpy
import bgl
import blf
import gpu
from gpu_extras.batch import batch_for_shader


def draw_callback_px(self, context):
    print("mouse points", len(self.mouse_path))

    font_id = 0  # XXX, need to find out how best to get this.

    # draw some text
    blf.position(font_id, 15, 30, 0)
    blf.size(font_id, 20, 72)
    blf.draw(font_id, "Hello Word " + str(len(self.mouse_path)))

    # 50% alpha, 2 pixel width line
    shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    bgl.glEnable(bgl.GL_BLEND)
    bgl.glLineWidth(2)
    batch = batch_for_shader(shader, 'LINE_STRIP', {"pos": self.mouse_path})
    shader.bind()
    shader.uniform_float("color", (1.0, 1.0, 1.0, 0.5))
    batch.draw(shader)

    # restore opengl defaults
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)


class ModalDrawOperator(bpy.types.Operator):
    """Draw a line with the mouse"""
    bl_idname = "template.modal_operator"
    bl_label = "Simple Modal Draw Operator"

    def modal(self, context, event):
        context.area.tag_redraw()

        if event.type == 'MOUSEMOVE':
            self.mouse_path.append((event.mouse_region_x, event.mouse_region_y))

        elif event.type == 'LEFTMOUSE':
            bpy.types.SpaceTextEditor.draw_handler_remove(self._handle, 'WINDOW')
            return {'FINISHED'}

        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            bpy.types.SpaceTextEditor.draw_handler_remove(self._handle, 'WINDOW')
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if context.area.type == 'TEXT_EDITOR':
            # the arguments we pass the the callback
            args = (self, context)
            # Add the region OpenGL drawing callback
            # draw in TEXT_EIDTOR space with 'POST_VIEW' and 'PRE_VIEW'
            self._handle = bpy.types.SpaceTextEditor.draw_handler_add(draw_callback_px, args, 'WINDOW', 'POST_PIXEL')

            self.mouse_path = []

            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "Area found, cannot run operator")
            return {'CANCELLED'}


def register():
    bpy.utils.register_class(ModalDrawOperator)


def unregister():
    bpy.utils.unregister_class(ModalDrawOperator)

def menu_func(self, context):
    self.layout.operator(ModalDrawOperator.bl_idname)

if __name__ == "__main__":
    register()
    bpy.types.TOPBAR_MT_app_system.append(menu_func)
