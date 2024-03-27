import sys

from fontTools import ttLib
from fontTools.pens.transformPen import TransformPen
from opentypesvg.fonts2svg import SVGPen, viewbox_settings

class FontSvg():
    def __init__(self, fontPath:str, adjust_view_box_to_glyph:bool) -> None:
        self.fontPath = fontPath
        self.svg_dict = {}
        self.adjust_view_box_to_glyph = adjust_view_box_to_glyph
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

            self.svg_dict[gName] = d
        return 0

    def keys(self):
        return self.svg_dict.keys()

    def get_svg(self, name, hex_color):
        viewbox = viewbox_settings(
            self.fontPath,
            self.adjust_view_box_to_glyph
        )

        svgStr = (u"""<symbol id="{}" """
                u"""viewBox="{}">\n""".format(name, viewbox))

        d = self.svg_dict[name]

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
