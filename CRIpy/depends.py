import colour
from colour import Color as OriginalColor


class Alpha:
    @staticmethod
    def mix(fg, bg):
        r = Color()
        r.A = 1 - (1 - fg.A) * (1 - bg.A)
        if r.A < colour.FLOAT_ERROR:
            return r
        r.R = fg.R * fg.A / r.A + bg.R * bg.A * (1 - fg.A) / r.A
        r.G = fg.G * fg.A / r.A + bg.G * bg.A * (1 - fg.A) / r.A
        r.B = fg.B * fg.A / r.A + bg.B * bg.A * (1 - fg.A) / r.A
        return r

    @classmethod
    def tint(cls, c, t):
        return cls.mix(c.alpha(t), Color('white'))

    @classmethod
    def shade(cls, c, t):
        return cls.mix(c.alpha(t), Color('black'))


alpha = Alpha


class Color(OriginalColor):
    _alpha = 1.0

    def __init__(self, *args, **kwargs):
        self.shading = alpha
        super().__init__(*args, **kwargs)

    def __setattr__(self, label, value):
        if label not in ["_alpha", "_hsl", "equality", "shading"]:
            fc = getattr(self, 'set_' + label)
            fc(value)
        else:
            self.__dict__[label] = value

    def get_alpha(self):
        return self._alpha

    def get_R(self):
        return self.rgb[0]

    def get_G(self):
        return self.rgb[1]

    def get_B(self):
        return self.rgb[2]

    def get_A(self):
        return self._alpha

    def get_rgba(self):
        return *self.get_rgb(), self._alpha

    def set_alpha(self, value):
        self._alpha = value

    def set_R(self, value):
        _, g, b = self.rgb
        self.set_rgb((value, g, b))

    def set_G(self, value):
        r, _, b = self.rgb
        self.set_rgb((r, value, b))

    def set_B(self, value):
        r, g, _ = self.rgb
        self.set_rgb((r, g, value))

    def set_A(self, value):
        self._alpha = value

    def mix(self, background):
        return self.shading.mix(self, background)

    def tint(self, value):
        return self.shading.tint(self, value)

    def tints(self, count):
        for i in range(count):
            yield self.tint(1.0 - (1.0 / count) * i)

    def shade(self, value):
        return self.shading.shade(self, value)

    def shades(self, count):
        for i in range(count):
            yield self.shade(1.0 - (1.0 / count) * i)

    def alpha(self, value):
        r = Color(self)
        r.A = value
        return r
