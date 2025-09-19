try:
    from PySide2 import QtCore, QtWidgets, QtGui
    import shiboken2
except:
    from PySide6 import QtCore, QtWidgets, QtGui
    import shiboken6

from maya import OpenMayaUI, cmds

def get_maya_main_window():
    pointer = OpenMayaUI.MQtUtil.mainWindow()
    return shiboken6.wrapInstance(int(pointer), QtWidgets.QMainWindow)

class Chunk(object):

    def __init__(self, name='untitled'):
        self.name = str(name)

    def __enter__(self):
        cmds.undoInfo(openChunk=True, chunkName=self.name)

    def __exit__(self, exc_type, exc_val, exc_tb):
        cmds.undoInfo(closeChunk=True)

def chunk(func):
    def wrapper(*args, **kwargs):
        with Chunk(name=func.__name__):
            return func(*args, **kwargs)

    return wrapper