from enums import enum
from fc_list import FontList

__all_fonts__ = FontList.all()

class FontFamily(object):
    def __init__(self, font_name):
        self.all = __all_fonts__.by_partial_name(font_name)

        try:
            self.regular = [
                font for font in self.all.regular()
                if font not in self.all.by_style("Condensed")
            ][0]
            
        except IndexError:
            self.regular = None

        
        try:
            self.bold = [
                font for font in self.all.by_style("Bold")
                if (font not in self.all.by_style("Italic") and
                    font not in self.all.by_style("Condensed"))
            ][0]
            
        except IndexError:
            self.bold = None

        try:
            self.italic = [
                font for font in self.all.by_style("Italic")
                if (font not in self.all.by_style("Bold") and
                    font not in self.all.by_style("Condensed"))
            ][0]
            
        except IndexError:
            self.italic = None

font_roles = enum(title=0,
                  body=1,
                  mono=2,
                  cursive=3)

class FontSet(object):
    def __init__(self, body, title, mono, cursive):
        self.body = body
        self.title = title
        self.mono = mono
        self.cursive = cursive
    def by_role(self, role):
        if role == font_roles.title:
            return self.title
        elif role == font_roles.body:
            return self.body
        elif role == font_roles.mono:
            return self.mono
        elif role == font_roles.cursive:
            return self.cursive
            

class Span(str):
    def __new__(self, text, styles=list()):
        return str.__new__(self, text)
    def __init__(self, text, styles=list()):
        self.styles = styles

class Block(list):
    def __init__(self, *args, styles=list()):
        list.__init__(self, args)
        self.styles = styles

class Style(object):
    def __init__(self, name):
        self.name = name

class InlineStyle(Style):
    def __init__(self, name, is_bold, is_italic, font_role):
        Style.__init__(self, name)
        self.is_bold = is_bold
        self.is_italic = is_italic
        self.font_role = font_role

class BlockStyle(Style):
    def __init__(self, name, is_bold, is_italic, font_role, point_size, indent_left, indent_right, space_before, space_after):
        Style.__init__(self, name)
        self.is_bold = is_bold
        self.is_italic = is_italic
        self.font_role = font_role
        self.point_size = point_size
        self.indent_left = indent_left
        self.indent_right = indent_right
        self.space_before = space_before
        self.space_after = space_after

if __name__ == "__main__":
    import pickle
    
    italic = Style("italic")
    bold = Style("bold")
    paragraph = Style("paragraph")
    quotation = Style("quotation")

    span = Span("This is a test.", styles=[bold, italic])
    
    doc = Block(Block(Span("This is a test.", styles=[bold, italic]),
                      Block(Span("C'est la vie."),
                            styles=[quotation]),
                      Span("That was what some Frenchman said."),
                      styles=[paragraph]),
                Block(Span("Here is some "),
                      Span("italic text", styles=[italic]),
                      Span(" for your delectation."),
                      styles=[paragraph]))

    with open("docs.pic", "wb") as f:
        saver = pickle.Pickler(f)
        saver.dump(doc)

    fset = FontSet(FontFamily("Times New"),
                   FontFamily("URW Palladio L"),
                   FontFamily("Courier New"),
                   FontFamily("Chancery"))

    for role in [font_roles.body, font_roles.title, font_roles.mono, font_roles.cursive]:
        fam = fset.by_role(role)
        if role == font_roles.cursive:
            print(fam.italic["path"])
        else:
            print([fam.regular["path"],
                   fam.bold["path"],
                   fam.italic["path"]])

    
