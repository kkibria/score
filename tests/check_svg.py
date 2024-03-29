from score.fontsvg import FontSvg

v = None
with open("Leland.otf", "rb") as f:
    v = FontSvg(f)

k = v.keys()
