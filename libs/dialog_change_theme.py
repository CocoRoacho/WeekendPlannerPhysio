import os

from kivy.properties import StringProperty, ListProperty
from kivy.uix.modalview import ModalView
from kivy.utils import get_color_from_hex, get_hex_from_color

from kivymd.color_definitions import colors, palette
from kivymd.theming import ThemableBehavior

from kivymd.uix.list import TwoLineListItem, ThreeLineListItem, ILeftBody, OneLineAvatarListItem
from kivy.uix.widget import Widget




class DPBaseDialog(ThemableBehavior, ModalView):
    pass


class DPOneLineLeftWidgetItem(OneLineAvatarListItem):
    color = ListProperty()


class LeftWidget(ILeftBody, Widget):
    pass


class DPDialogChangeTheme(DPBaseDialog):
    """ fills the dialog with data about color themes """

    def set_list_colors_themes(self):
        for name_theme in palette:
            self.ids.rv.data.append(
                {
                    "viewclass": "DPOneLineLeftWidgetItem",
                    "color": get_color_from_hex(colors[name_theme]["500"]),
                    "text": name_theme,
                }
            )


class DPUsageCode(DPBaseDialog):
    code = StringProperty()
    title = StringProperty()
    website = StringProperty()