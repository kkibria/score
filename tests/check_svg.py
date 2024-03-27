from score.fontsvg import FontSvg

v = None
with open("C:/Users/Khan/Documents/python/verovio/fonts/Leland/Leland.otf", "rb") as f:
    v = FontSvg(f)
    v.loadFont()

k = v.keys()

    # uniE0D3

print(v.get_svg('uniE0D3', '000000'))