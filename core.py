from maya import cmds
from .utils import chunk

@chunk
def create_attribute_on_selected(long_name, nice_name=None, keyable=True, shown=True, locked=False, attribute_flag='attributeType', attribute_type='float', value=None):
    # create
    selection = cmds.ls(sl=True)

    for node in selection:
        create_attribute(node, long_name, nice_name, keyable, shown, locked, attribute_flag, attribute_type, value)

@chunk
def create_attribute(node, long_name, nice_name=None, keyable=True, shown=True, locked=False, attribute_flag='attributeType', attribute_type='float', value=None):
    kwargs = dict()

    kwargs['longName'] = long_name

    if nice_name is not None:
        kwargs['niceName'] = nice_name

    kwargs['keyable'] = keyable

    kwargs[attribute_flag] = attribute_type

    if value:
        if attribute_type == 'enum':
            kwargs['enumName'] = ':'.join(value)

    cmds.addAttr(node, **kwargs)

    plug = f'{node}.{long_name}'
    if not keyable:
        cmds.setAttr(plug, channelBox=shown)

    cmds.setAttr(plug, lock=locked)