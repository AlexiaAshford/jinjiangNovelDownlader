def format_manifest(chapter_id):
    return f'<item href="Text/{chapter_id}.xhtml" id="{chapter_id}.xhtml" media-type="application/xhtml+xml" />\r\n'


def format_image_format_manifest(filename: str, media_type: str):
    return f'<item href="Images/{filename}" id="{filename}" media-type="{media_type}" />\r\n'


def format_chapter(chapter_index, chapter_title, chapter_content):
    return chapter_xhtml.replace('<title>${chapter_title}</title>',
                                 f'<title>第{chapter_index}章: {chapter_title} </title>') \
        .replace('${chapter_content}', f'<h3>{chapter_title}</h3>\r\n' + chapter_content)


def format_spine(chapter_id):
    return f'<itemref idref="{chapter_id}.xhtml" />\r\n'


def format_nav_map(chapter_id, chapter_index, chapter_title):
    return f'<navPoint id="{chapter_id}" playOrder="{chapter_index}"><navLabel><text>{chapter_title}</text>' \
           f'</navLabel><content src="Text/{chapter_id}.xhtml" /></navPoint>\r\n'


def format_content_opf(book_id, book_name, book_author):
    return content_opf.replace('${book_id}', book_id). \
        replace('${book_title}', book_name).replace('${book_author}', book_author)


def format_toc_ncx(book_id, book_name, book_author):
    return toc_ncx.replace('${book_id}', book_id). \
        replace('${book_title}', book_name).replace('${book_author}', book_author)


def update_content_opf_manifest(update_content_opf, content_opf_manifest):
    default_content_opf_manifest = """<item href="toc.ncx" id="ncx" media-type="application/x-dtbncx+xml" />
    <item href="Images/cover.jpg" id="cover.jpg" media-type="image/jpeg" />
    <item href="Text/cover.xhtml" id="cover.xhtml" media-type="application/xhtml+xml" />\n"""
    return update_content_opf.replace(
        '<manifest></manifest>', f'<manifest>{default_content_opf_manifest + content_opf_manifest}</manifest>'
    )


def update_content_opf_spine(update_content_opf, content_opf_spine):
    default_content_opf_spine = '<itemref idref="cover.xhtml" />\n'
    return update_content_opf.replace('<spine toc="ncx"></spine>',
                                      f'<spine toc="ncx">{default_content_opf_spine + content_opf_spine}</spine>')


def update_nav_map(update_toc_ncx, nav_map):
    default_nav_map = '<navPoint id="cover" playOrder="1"><navLabel><text>書籍封面</text></navLabel>' \
                      '<content src="Text/cover.xhtml" /></navPoint>'
    return update_toc_ncx.replace('<navMap></navMap>', f'<navMap>{default_nav_map + nav_map}</navMap>')

container = """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
    <rootfiles>
        <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
   </rootfiles>
</container>
"""

mimetype = "application/epub+zip"

content_opf = """<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="BookId" version="2.0">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
<dc:identifier id="BookId">hbooker:${book_id}</dc:identifier>
<dc:title>${book_title}</dc:title>
<dc:creator opf:role="aut">${book_author}</dc:creator>
<dc:language>zh-CN</dc:language>
<dc:publisher>hbooker.com</dc:publisher>
<meta name="cover" content="cover.jpg"/>
</metadata>
<manifest></manifest>
<spine toc="ncx"></spine>
<guide>
<reference href="Text/cover.xhtml" title="书籍封面" type="cover" />
</guide>
</package> 
"""

toc_ncx = """<?xml version="1.0" encoding="utf-8" standalone="no" ?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN"
 "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
<head>
<meta content="hbooker:${book_id}" name="dtb:uid"/>
<meta content="2" name="dtb:depth"/>
<meta content="0" name="dtb:totalPageCount"/>
<meta content="0" name="dtb:maxPageNumber"/>
</head>
<docTitle>
<text>${book_title}</text>
</docTitle>
<docAuthor>
<text>${book_author}</text>
</docAuthor>
<navMap></navMap>
</ncx>  
"""

cover_xhtml = """<?xml version="1.0" encoding="utf-8" standalone="no"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ch">
<head>
<title>书籍封面</title>
</head>
<body>
<div style="text-align: center; padding: 0; margin: 0;">
<svg xmlns="http://www.w3.org/2000/svg" height="100%" preserveAspectRatio="xMidYMid meet" version="1.1" viewBox="0 0 179 248" width="100%" xmlns:xlink="http://www.w3.org/1999/xlink">
<image height="248" width="179" xlink:href="../Images/cover.jpg"> </image>
</svg>
</div>
</body>
</html> 
"""

chapter_xhtml = """<?xml version="1.0" encoding="utf-8" standalone="no"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>${chapter_title}</title>
</head>
<body>
${chapter_content}
</body>
</html>
"""
