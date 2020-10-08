from CRIpy.depends import Color


class Colors:
    black = Color('#000000')
    white = Color('#FFFFFF')
    gray = Color('#A0A0A0')

    red = Color('#CD5F4B')
    green = Color('#5AA06E')
    blue = Color('#6496B9')
    cyan = Color('#64B4C8')
    magenta = Color('#F9557B')
    yellow = Color('#F5D20F')
    orange = Color('#DC8714')
    purple = Color('#914B96')

    dark_green = Color('#41825A')
    forest_green = Color('#82A050')
    light_green = Color('#AAC85F')
    logo_green = Color('#82B45F')
    pale_green = Color('#8CBE87')

    basic = [red, green, blue, cyan, magenta, yellow, orange, purple]
    secondary = [red, blue, cyan, magenta, yellow, orange, purple]
    greens = [green, dark_green, light_green, pale_green, forest_green]
    logo = [logo_green, black, white]
