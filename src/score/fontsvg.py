import sys

from fontTools import ttLib
from fontTools.pens.transformPen import TransformPen
from opentypesvg.fonts2svg import SVGPen, viewbox_settings

class FontSvg():
    def __init__(self, fontPath:str) -> None:
        self.fontPath = fontPath
        self.svg_dict = {}
        pass

    def loadFont(self):
        self.svg_dict = {}
        # Load the fonts and collect their glyph sets
        try:
            font = ttLib.TTFont(self.fontPath)
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

            viewbox = self.viewbox_settings(gName)
            svgStr = (u"""<symbol id="{}" """
                    u"""viewBox="{}">\n""".format(gName, viewbox))
            self.svg_dict[gName] = svgStr, d
            

        return 0

    def keys(self):
        return self.svg_dict.keys()

    def viewbox_settings(self, name):
        try:
            head = ttLib.TTFont(self.fontPath, res_name_or_index=name)["head"]
            # it looks like compared to viewbox in the head table
            # the yMin and yMax are inverted
            x = head.xMin
            y = -head.yMax
            width = head.xMax - head.xMin
            height = head.yMax - head.yMin
            return """{} {} {} {}""".format(x, y, width, height)
        except KeyError:
            upm = 1000
            return """0 -{} {} {}""".format(upm, upm, upm)

    def get_svg(self, name, hex_color):

        svgStr, d = self.svg_dict[name]

        hex_str = hex_color
        opc = ''
        if len(hex_str) != 6:
            opcHex = hex_str[6:]
            hex_str = hex_str[:6]
            if opcHex.lower() != 'ff':
                opc = ' opacity="{:.2f}"'.format(int(opcHex, 16) / 255)

        svgStr += u'\t<path{} fill="#{}" d="{}"/>\n'.format(
            opc, hex_str, d)
        svgStr += u'</symbol>'

        # Skip svg that have no paths
        if '<path' in svgStr:
            return svgStr
