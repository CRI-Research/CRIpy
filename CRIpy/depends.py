import colour
import functools
from colour import Color as OriginalColor


# This class was copied from https://github.com/astropy/astropy/blob/master/astropy/utils/decorators.py
# Copyright (c) 2011-2020, Astropy Developers
# License: https://github.com/astropy/astropy/blob/master/LICENSE.rst
class classproperty(property):
    """
    Similar to `property`, but allows class-level properties.  That is,
    a property whose getter is like a `classmethod`.
    The wrapped method may explicitly use the `classmethod` decorator (which
    must become before this decorator), or the `classmethod` may be omitted
    (it is implicit through use of this decorator).
    .. note::
        classproperty only works for *read-only* properties.  It does not
        currently allow writeable/deletable properties, due to subtleties of how
        Python descriptors work.  In order to implement such properties on a class
        a metaclass for that class must be implemented.
    Parameters
    ----------
    fget : callable
        The function that computes the value of this property (in particular,
        the function when this is used as a decorator) a la `property`.
    doc : str, optional
        The docstring for the property--by default inherited from the getter
        function.
    lazy : bool, optional
        If True, caches the value returned by the first call to the getter
        function, so that it is only called once (used for lazy evaluation
        of an attribute).  This is analogous to `lazyproperty`.  The ``lazy``
        argument can also be used when `classproperty` is used as a decorator
        (see the third example below).  When used in the decorator syntax this
        *must* be passed in as a keyword argument.
    Examples
    --------
    ::
        >>> class Foo:
        ...     _bar_internal = 1
        ...     @classproperty
        ...     def bar(cls):
        ...         return cls._bar_internal + 1
        ...
        >>> Foo.bar
        2
        >>> foo_instance = Foo()
        >>> foo_instance.bar
        2
        >>> foo_instance._bar_internal = 2
        >>> foo_instance.bar  # Ignores instance attributes
        2
    As previously noted, a `classproperty` is limited to implementing
    read-only attributes::
        >>> class Foo:
        ...     _bar_internal = 1
        ...     @classproperty
        ...     def bar(cls):
        ...         return cls._bar_internal
        ...     @bar.setter
        ...     def bar(cls, value):
        ...         cls._bar_internal = value
        ...
        Traceback (most recent call last):
        ...
        NotImplementedError: classproperty can only be read-only; use a
        metaclass to implement modifiable class-level properties
    When the ``lazy`` option is used, the getter is only called once::
        >>> class Foo:
        ...     @classproperty(lazy=True)
        ...     def bar(cls):
        ...         print("Performing complicated calculation")
        ...         return 1
        ...
        >>> Foo.bar
        Performing complicated calculation
        1
        >>> Foo.bar
        1
    If a subclass inherits a lazy `classproperty` the property is still
    re-evaluated for the subclass::
        >>> class FooSub(Foo):
        ...     pass
        ...
        >>> FooSub.bar
        Performing complicated calculation
        1
        >>> FooSub.bar
        1
    """

    def __new__(cls, fget=None, doc=None, lazy=False):
        if fget is None:
            # Being used as a decorator--return a wrapper that implements
            # decorator syntax
            def wrapper(func):
                return cls(func, lazy=lazy)

            return wrapper

        return super().__new__(cls)

    def __init__(self, fget, doc=None, lazy=False):
        self._lazy = lazy
        if lazy:
            self._cache = {}
        fget = self._wrap_fget(fget)

        super().__init__(fget=fget, doc=doc)

        # There is a buglet in Python where self.__doc__ doesn't
        # get set properly on instances of property subclasses if
        # the doc argument was used rather than taking the docstring
        # from fget
        # Related Python issue: https://bugs.python.org/issue24766
        if doc is not None:
            self.__doc__ = doc

    def __get__(self, obj, objtype):
        if self._lazy and objtype in self._cache:
            return self._cache[objtype]

        # The base property.__get__ will just return self here;
        # instead we pass objtype through to the original wrapped
        # function (which takes the class as its sole argument)
        val = self.fget.__wrapped__(objtype)

        if self._lazy:
            self._cache[objtype] = val

        return val

    def getter(self, fget):
        return super().getter(self._wrap_fget(fget))

    def setter(self, fset):
        raise NotImplementedError(
            "classproperty can only be read-only; use a metaclass to "
            "implement modifiable class-level properties")

    def deleter(self, fdel):
        raise NotImplementedError(
            "classproperty can only be read-only; use a metaclass to "
            "implement modifiable class-level properties")

    @staticmethod
    def _wrap_fget(orig_fget):
        if isinstance(orig_fget, classmethod):
            orig_fget = orig_fget.__func__

        # Using stock functools.wraps instead of the fancier version
        # found later in this module, which is overkill for this purpose

        @functools.wraps(orig_fget)
        def fget(obj):
            return orig_fget(obj.__class__)

        return fget


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
        return (*self.get_rgb()), self._alpha

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
