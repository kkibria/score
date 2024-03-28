import subprocess
import re
from check_svg import v, k

pt = lambda i,l,h,d: (i)*(h-l)/d+l

def coord_g(x1, y1, x2, y2, w, xd, yd):
    l = []
    l.extend(draw_coord(x1, y1, x2, y2, w))
    l.extend(draw_grid(x1, y1, x2, y2, xd, yd))
    return l 

def draw_coord(x1, y1, x2, y2, w):
    wh = w/2
    l = []
    l.append(f'<g fill="none" stroke="black" stroke-width="{w}" >')
    l.append(f'<line x1="{x1}" y1="{y1+wh}" x2="{x2}" y2="{y1+wh}" />')
    l.append(f'<line x1="{x1+wh}" y1="{y1}" x2="{x1+wh}" y2="{y2}" />')
    l.append(f'</g>')
    l.append(f'<g fill="red" stroke="none" >')
    l.append(f'<rect x="{x1}" y="{y1}" width="{w}" height="{w}" />')
    l.append(f'<rect x="{x2-w}" y="{y1}" width="{w}" height="{w}" />')
    l.append(f'<rect x="{x1}" y="{y2-w}" width="{w}" height="{w}" />')
    l.append(f'</g>')
    l.append(f'<g font-size="14" font-family="Verdana" >')
    l.append(f'<text x="{x1+10}" y="{y1+20}">({x1},{y1})</text>')
    l.append(f'<text x="{x2-60}" y="{y1+20}">({x2},{y1})</text>')
    l.append(f'<text x="{x1+10}" y="{y2-10}">({x1},{y2})</text>')
    l.append(f'</g>')
    return l

def draw_grid(x1, y1, x2, y2, xd, yd):
    l = []
    ls= 'stroke:#D3D3D3;stroke-width:0.5px;stroke-dasharray:10, 10;stroke-opacity:1'
    l.append(f'<g style="{ls}" >')
    for xm in range(xd+1):
        x = pt(xm,x1,x2,xd) 
        l.append(f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" />')
    for ym in range(yd+1):
        y = pt(ym,y1,y2,yd) 
        l.append(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" />')           
    l.append(f'</g>')
    return l 

# kinda kludgy approach requires hand editing the outcome 
def templetize(g:str):
    ll = []
    for i in g.splitlines():
        l = i
        if not ('<g' in i or '</g' in i):
            l = re.sub(r'"(.+?)"', lambda x: '"{'+x[1]+'}"', i)
        ll.append(f'l.append(f\'{l}\')')
        return "\n".join(ll)

# print(form(g))
def svgwrap(w, h, g):
    svg = """<?xml version="1.0" standalone="no"?>

<svg version="1.1"
    viewBox="0 0 {} {}"
     xmlns="http://www.w3.org/2000/svg">
  <desc>shows all the symbols from font</desc>
    {}
</svg>
"""
    return svg.format(w,h,g)

def str2file(fn, s):
    with open(fn, "w") as f:
        print(s, file=f)
    cmd = f'explorer {fn}'.split()
    # sts = subprocess.run(cmd)

font = """
<def>
{}
</def>
<g transform="translate({}, {}) scale({}) ">
 <use href="#{}" />
</g>
"""

def draw(x, y, w, xd, yd, s):
    return _draw(x, y, w, xd+1, yd, s)

def _draw(x, y, w, xd, yd, s):
    l = coord_g(0, 0, x, y, w, xd, yd)
    px = 100
    py = 100
    ids = list(k)
    pages = {}
    total = (xd-1)*(yd-1)

    for i in range(len(ids)):
        xl = i % (xd-1)
        _r = i // (xd-1)
        yl = _r % (yd-1)
        p = _r // (yd-1)

        px = (x//xd)*(1+xl)
        py = (y//yd)*(1+yl)

        id = ids[i]
        f = v.get(id)
        if p not in pages:
            pages[p] = []
        pages[p].append(font.format(f, px, py, s, id))
        pages[p].append(f'<g font-size="10" font-family="Verdana" >')
        pages[p].append(f'<text x="{px}" y="{py+y//yd//2}">{id}</text>')
        pages[p].append(f'</g>')

    for i in pages:
        _svg = svgwrap(x+w, y+w, "\n".join(l+pages[i]))
        str2file(f'xp{i}.svg', _svg)

    return (len(pages))

pages = draw(1000, 500, 3, 10, 5, 0.02)

# pdf = fpdf.FPDF(unit="pt", format=(1003, 503))
# for i in range(pages):
#     svgobj = fpdf.svg.SVGObject.from_file(f'xp{i}.svg')
#     pdf.add_page()
#     svgobj.draw_to_page(pdf)
# pdf.output("my_file.pdf")


