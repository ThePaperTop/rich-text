import rich_text

class Htmlinator(object):
    """Allows agents to convert PaperTop rich text to styled HTML."""
    def __init__(self, font_set):
        self._doc_tmpl = """
<html>
<head>
<title>%(title)s</title>
</head>
<body style="%(style)s">
%(content)s
</body>
</html>"""

        self._block_tmpl = """
<div style="%(style)s">
%(content)s
</div>"""

        self._span_tmpl = '<span style="%(style)s">%(content)s</span>'

        self._font_set = font_set

    def _cssinate(self, style):
        """Returns CSS to portray the specified style"""
        out = []

        if style.is_bold:
            out.append("font-weight: bold;")
            
        if style.is_italic:
            out.append("font-style: italic;")

        font = self._font_set.by_role(style.font_role)
        
        if font and font.regular:
            out.append("font-family: %s;" % font.regular["name"])

        if style.block:
            if style.is_bulleted:
                out.append("display: list-item;")
                out.append("list-style-type: disc;")
                out.append("list-style-position: inside;")

            out.append("font-size: %spt;" % style.point_size)
            out.append("text-indent: %spx;" % style.first_line_indent)
            out.append("padding-left: %spx;" % style.indent_left)
            out.append("padding-right: %spx;" % style.indent_right)
            out.append("padding-top: %spx;" % style.space_before)
            out.append("padding-bottom: %spx;" % style.space_after)

        return "\n".join(out)
    
    def _format_block(self, block):
        content = "\n".join(
            [self._format_element(element)
             for element in block])

        return self._block_tmpl % {"content": content,
                                   "style": self._cssinate(block.style)}

    def _format_span(self, span):
        return self._span_tmpl % {"style": self._cssinate(span.style),
                                  "content": span}

    def _format_element(self, element):
        try:
            return self._format_block(element)
        except:
            return self._format_span(element)
        
    def htmlinate(self, doc):
        """Convert the specified document to styled HTML"""
        content = "\n".join(
            [self._format_block(block)
             for block in doc])
        return self._doc_tmpl % {"content": content,
                                 "style": "",
                                 "title": doc.title}
