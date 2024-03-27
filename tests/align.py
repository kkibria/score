import subprocess
import re
from check_svg import v, k

g='''
<g fill="none" stroke="black" stroke-width="3" >
<line x1="{0}" y1="1.5" x2="300" y2="1.5" />
<line x1="1.5" y1="0" x2="1.5" y2="100" />
</g>
<g fill="red" stroke="none" >
<rect x="0" y="0" width="3" height="3" />
<rect x="297" y="0" width="3" height="3" />
<rect x="0" y="97" width="3" height="3" />
</g>
<g font-size="14" font-family="Verdana" >
<text x="10" y="20">(0,0)</text>
<text x="240" y="20">(300,0)</text>
<text x="10" y="90">(0,100)</text>
</g>
'''

def coord_g(x1, y1, x2, y2, w):
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
    ls= "stroke:#000000;stroke-width:0.5px;stroke-dasharray:10, 10;stroke-opacity:1"
    l.append(f'<g style="{ls}" >')
    xd = 10
    yd = 5
    pt = lambda i,l,h,d: (i+0.5)*(h-l)/d+l
    for xm in range(xd+1):
        x = pt(xm,x1,x2,xd) 
        l.append(f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" />')
    for ym in range(yd+1):
        y = pt(ym,y1,y2,yd) 
        l.append(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" />')
    l.append(f'</g>')

    l.append(v.get_svg('uniE0D3', '000000'))
    l.append(f'<use href="#uniE0D3" x="{pt(0,x1,x2,xd)}" y="{pt(0,y1,y2,yd)}" style="opacity:1.0" />')

    return "\n".join(l)            

def form(g):
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
  <desc>Example InitialCoords - SVG's initial coordinate system</desc>
    {}
</svg>
"""
    return svg.format(w,h,g)

def str2file(fn, s):
    with open(fn, "w") as f:
        print(s, file=f)
    cmd = f'explorer {fn}'.split()
    sts = subprocess.run(cmd)

str2file('x15.svg', svgwrap(1003, 503, coord_g(0, 0, 1000, 500, 3)))
# str2file('x12.svg', svgwrap(g))



