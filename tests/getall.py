from score.fontsvg import FontSvg

font_path = "Leland.otf"
v = None

with open(font_path, "rb") as f:
    v = FontSvg(f)
k = v.keys()

def getall(fn):
    with open(fn, "w") as f:
        print(f'<!-- upm={v.upm} -->', file=f)
        print(f'<!-- extent={v.extent} -->', file=f)
        print('<dev>', file=f)
        for i in k:
            print(f'<!-- {i} -->', file=f)
            print(v.get(i), file=f)
        print('</dev>', file=f)

getall("getall.svg")


