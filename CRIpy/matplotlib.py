from matplotlib.colors import ListedColormap
from CRIpy.core import Colors


class ColorMaps:

    @classmethod
    def get_cmap(cls, name):
        return getattr(cls, name)

    @staticmethod
    def tab_colors():
        c = Colors
        return [c.blue, c.orange, c.green, c.red, c.purple, c.yellow, c.magenta, c.gray, c.forest_green, c.cyan]

    @classmethod
    def get_tab10(cls):
        tab10 = [x.hex for x in cls.tab_colors()]
        return ListedColormap(tab10, 'CRI_tab10')

    @classmethod
    def get_tab20(cls):
        tab20 = [i for t in [(x.hex, x.tint(.5).hex) for x in cls.tab_colors()] for i in t]
        return ListedColormap(tab20, 'CRI_tab20')

    tab10 = property(get_tab10)
    tab20 = property(get_tab20)
