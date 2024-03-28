import sys

from fontTools import ttLib
from fontTools.pens.transformPen import TransformPen
from opentypesvg.fonts2svg import SVGPen

class FontSvg():
    def __init__(self, fontPath:str) -> None:
        self.fontPath = fontPath
        self.svg_dict = {}
        self.loadFont()

    def loadFont(self):
        self.svg_dict = {}
        # Load the fonts and collect their glyph sets
        try:
            font = ttLib.TTFont(self.fontPath)
            self.set_extent(font)
            gSet = font.getGlyphSet()
            font.close()

        except ttLib.TTLibError:
            print(f"ERROR: {self.fontPath} cannot be processed.",
                    file=sys.stderr)
            return 1

        names = sorted(set(gSet.keys()))
        # Remove '.notdef'
        if '.notdef' in names:
            names.remove('.notdef')

        # Confirm that there's something to process
        if not names:
            print("The font can't produce any SVG.",
                file=sys.stdout)
            return 1

        # Generate the SVGs
        for gName in names:
            pen = SVGPen(gSet)
            tpen = TransformPen(pen, (1.0, 0.0, 0.0, -1.0, 0.0, 0.0))
            glyph = gSet[gName]
            glyph.draw(tpen)
            d = pen.d
            # Skip glyphs with no contours
            if not len(d):
                continue
            self.svg_dict[gName] = d

        return 0

    def keys(self):
        return self.svg_dict.keys()

    def extent(self):
        return self.extent

    def upm(self):
        return self.upm

    def set_extent(self, font):
        try:
            head = font["head"]
            # svg y axis increases downwards
            x = head.xMin
            y = -head.yMax
            width = head.xMax - head.xMin
            height = head.yMax - head.yMin
            self.extent = x, y, width, height
            self.upm = head.unitsPerEm

        except KeyError:
            upm = 1000
            self.upm = upm
            self.extent = -upm, -upm, upm+upm, upm+upm

    def get(self, name):
        d = f'<path d="{self.svg_dict[name]}" />'
        return f'<g id="{name}">\n {d}\n</g>'
