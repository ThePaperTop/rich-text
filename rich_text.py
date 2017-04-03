from enums import enum
from fontlist import FontList
from datetime import datetime

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

        try:
            self.bold_italic = self.all.italic().bold()[0]
        except IndexError:
            self.bold_italic = None

font_roles = enum(title=0,
                  body=1,
                  mono=2,
                  cursive=3,
                  inherit=-1)

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
    def __new__(self, text, style):
        return str.__new__(self, text)
    def __init__(self, text, style):
        self.style = style

class Block(list):
    def __init__(self, *args, style):
        list.__init__(self, args)
        self.style = style

class Document(list):
    def __init__(self,
                 *args,
                 title="",
                 author="",
                 date=datetime.now()):
        
        list.__init__(self, args)
        
        self.title = title
        self.author = author
        self.date = date

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
    def __init__(self,
                 name,
                 is_bold,
                 is_italic,
                 is_bulleted,
                 font_role,
                 point_size,
                 first_line_indent,
                 indent_left,
                 indent_right,
                 space_before,
                 space_after,
                 next_style=None):
        
        Style.__init__(self, name)
        
        self.is_bold = is_bold
        self.is_italic = is_italic
        self.is_bulleted = is_bulleted
        self.font_role = font_role
        self.point_size = point_size
        self.first_line_indent = first_line_indent
        self.indent_left = indent_left
        self.indent_right = indent_right
        self.space_before = space_before
        self.space_after = space_after
        
        if next_style == None:
            self.next_style = self
        else:
            self.next_style = next_style

if __name__ == "__main__":

    import math

    paragraph_style = BlockStyle("Paragraph",
                                 False,
                                 False,
                                 False,
                                 font_roles.body,
                                 12,
                                 15,
                                 0,
                                 0,
                                 10,
                                 3)
    
    quotation_style = BlockStyle("Quotation",
                                 False,
                                 False,
                                 False,
                                 font_roles.body,
                                 11,
                                 15,
                                 30,
                                 15,
                                 10,
                                 10)
    
    bulleted_style = BlockStyle("Bulleted",
                                False,
                                False,
                                True,
                                font_roles.body,
                                12,
                                15,
                                0,
                                0,
                                10,
                                10)
    
    header_styles = [BlockStyle("H%s" % depth,
                                True,
                                False,
                                False,
                                font_roles.title,
                                math.floor(12 + 3 * (5 - depth)),
                                0, 0, 0, 10, 3,
                                paragraph_style)
                     for depth in range(1, 6)]

    block_styles = header_styles + [paragraph_style,
                                    quotation_style,
                                    bulleted_style]
    
    inline_styles = [InlineStyle("Significant",
                                 False,
                                 True,
                                 font_roles.inherit),
                     InlineStyle("Emphatic",
                                 True,
                                 False,
                                 font_roles.inherit),
                     InlineStyle("Doubly Emphatic",
                                 True,
                                 True,
                                 font_roles.inherit),
                     InlineStyle("Code",
                                 False,
                                 False,
                                 font_roles.mono),
                     InlineStyle("Fancy",
                                 False,
                                 True,
                                 font_roles.cursive)]

    
