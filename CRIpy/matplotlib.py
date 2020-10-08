from matplotlib.colors import ListedColormap
from CRIpy.core import Colors
from CRIpy.depends import classproperty


class ColorMaps:

    @classmethod
    def get_cmap(cls, name):
        return getattr(cls, name)

    @staticmethod
    def tab_colors():
        c = Colors
        return [c.blue, c.orange, c.green, c.red, c.purple, c.yellow, c.magenta, c.gray, c.forest_green, c.cyan]

    @classproperty
    def tab10(cls):
        tab10 = [x.hex for x in cls.tab_colors()]
        return ListedColormap(tab10, 'CRI_tab10')

    @classproperty
    def tab20(cls):
        tab20 = [i for t in [(x.hex, x.tint(.5).hex) for x in cls.tab_colors()] for i in t]
        return ListedColormap(tab20, 'CRI_tab20')
