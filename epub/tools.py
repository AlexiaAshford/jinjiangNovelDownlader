from instance import *
import urllib.request
from .template import cover_xhtml


def str_mid(string: str, left: str, right: str, start=None, end=None):
    pos1 = string.find(left, start, end)
    if pos1 > -1:
        pos2 = string.find(right, pos1 + len(left), end)
        if pos2 > -1:
            return string[pos1 + len(left): pos2]
    return ''


def get_all_files(dir_path: str):
    result = list()
    for _name in os.listdir(dir_path):
        if os.path.isdir(dir_path + '/' + _name):
            result.extend(get_all_files(dir_path + '/' + _name))
        else:
            result.append(dir_path + '/' + _name)
    return result


def add_image(config_dir, filename: str, url: str):
    image_path = os.path.join(config_dir, 'OEBPS', 'Images', filename)
    if os.path.exists(image_path):
        if os.path.getsize(image_path) != 0:
            return
    try:
        urllib.request.urlretrieve(url, image_path)
    except OSError as e:
        print("Error add_image: ", e)


def get_chapter_image(config_dir, chapter_data: str):
    for _img in re.findall(r'<img .*src="http.*?>', chapter_data):
        _src = str_mid(_img.replace('>', ' />'), 'src="', '"')
        if _src.rfind('/') == -1:
            continue
        filename = _src[_src.rfind('/') + 1:]
        add_image(config_dir, filename, _src)
        chapter_data = chapter_data.replace(_src, '../Images/' + filename)
        chapter_data = re.sub(
            f"(<img *src=[\"\']\\.\\./Images/{filename}[\"\'] *alt=[\"\'][^\"^\']+[\"\'] *)(?!( ))(?!(/>))[/>]?",
            "\\1/>", chapter_data)
        chapter_data = re.sub(
            f"(<img *alt=[\"\'][^\"^\']+[\"\'] *src=[\"\']\\.\\./Images/{filename}[\"\'] *)(?!( ))(?!(/>))[/>]?",
            "\\1/>", chapter_data)
    return chapter_data


def text_to_html_element_escape(text: str):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def html_element_to_text_unescape(element: str):
    return element.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')


def make_in_cover_template(config_dir: str, epub_dir: str, display_information: str):
    write(os.path.join(config_dir, 'OEBPS', 'Text', 'cover.xhtml'), 'w',
          re.sub('</body></html>', f'{display_information}\r\n</body>\r\n</html>',
                 cover_xhtml.replace("\r", "").replace("\n", "")))
    cover = str(write(config_dir + '/OEBPS/Text/cover.xhtml', 'r').read())
    write(epub_dir.replace(".epub", ".txt"), 'w', replace_cover(str_mid(cover, '<h1>', '</body>')))


def write(path: str, mode: str, info=None):
    if info is None:
        try:
            return open(path, f'{mode}', encoding='UTF-8')
        except (UnicodeEncodeError, UnicodeDecodeError) as error:
            print("error: ", error)
            return open(path, f'{mode}', encoding='gbk')
    with open(path, f'{mode}', encoding='UTF-8', newline='') as file:
        file.writelines(info)
