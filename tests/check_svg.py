from score.fontsvg import FontSvg

with open("C:/Users/Khan/Documents/python/verovio/fonts/Leland/Leland.otf", "rb") as f:
    v = FontSvg(f, True)
    v.loadFont()
    # uniE0D3
    # print(v.svg_dict.keys())

    print(v.get_svg('uniE0D3', '000000'))