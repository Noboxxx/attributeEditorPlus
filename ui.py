from .core import create_attribute_on_selected

try:
    from PySide2 import QtWidgets, QtCore, QtGui
except ModuleNotFoundError:
    from PySide6 import QtWidgets, QtCore, QtGui

from .utils import get_maya_main_window
from maya import cmds


ATTRIBUTE_TYPES = [
    {
        'name': 'float',
        'flag': 'attributeType',
    },
    {
        'name': 'bool',
        'nice_name': 'boolean',
        'flag': 'attributeType',
    },
    {
        'name': 'enum',
        'flag': 'attributeType',
    },
    {
        'name': 'long',
        'nice_name': 'integer',
        'flag': 'attributeType',
    },
    {
        'name': 'string',
        'flag': 'dataType',
    },
    {
        'name': 'matrix',
        'flag': 'attributeType',
    },
    {
        'name': 'message',
        'flag': 'attributeType',
    },
]


class AttributeEditor(QtWidgets.QDialog):

    def __init__(self, parent=None):
        if parent is None:
            parent = get_maya_main_window()
        super().__init__(parent)

        self.setWindowTitle('Attribute Editor')
        self.resize(750, 500)

        self.long_name_line = QtWidgets.QLineEdit()
        self.nice_name_line = QtWidgets.QLineEdit()

        self.keyable_check = QtWidgets.QCheckBox()
        self.keyable_check.setChecked(True)

        self.attribute_type_combo = QtWidgets.QComboBox()
        for attribute_info in ATTRIBUTE_TYPES:
            label = attribute_info.get('nice_name', attribute_info['name'])
            self.attribute_type_combo.addItem(label, userData=attribute_info)

        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow('long name', self.long_name_line)
        form_layout.addRow('nice name', self.nice_name_line)
        form_layout.addRow('type', self.attribute_type_combo)
        form_layout.addRow('keyable', self.keyable_check)

        create_btn = QtWidgets.QPushButton('Create')
        create_btn.clicked.connect(self.create_attribute)

        create_seperator_action = QtGui.QAction('Seperator Attr', self)
        create_seperator_action.triggered.connect(self.create_seperator_attribute)

        create_menu = QtWidgets.QMenu('Create')
        create_menu.addAction(create_seperator_action)

        menu_bar = QtWidgets.QMenuBar()
        menu_bar.addMenu(create_menu)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setMenuBar(menu_bar)
        main_layout.addLayout(form_layout)
        main_layout.addWidget(create_btn, alignment=QtCore.Qt.AlignmentFlag.AlignRight)

    def create_attribute(self):
        long_name = self.long_name_line.text()
        keyable = self.keyable_check.isChecked()

        attribute_info = self.attribute_type_combo.currentData(QtCore.Qt.ItemDataRole.UserRole)
        create_attribute_on_selected(
            long_name,
            keyable=keyable,
            shown=True,
            attribute_flag=attribute_info['flag'],
            attribute_type=attribute_info['name']
        )

    def create_seperator_attribute(self):
        label = 'default'

        long_name = f'{label}_seperator'
        nice_name = '_' * 10

        value = [label]

        create_attribute_on_selected(
            long_name,
            nice_name=nice_name,
            keyable=False,
            locked=True,
            attribute_flag='attributeType',
            attribute_type='enum',
            value=value
        )

def open_attribute_editor():
    ui = AttributeEditor()
    ui.show()
    return ui