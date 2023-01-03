import zipfile
import codecs
from shutil import copyfile
from .template import *
from .tools import *
from .makedir import set_epub_cache_file


class EpubFile:

    def __init__(
            self,
            config_dir: str,
            epub_dir: str,
            book_id: str,
            book_name: str,
            author_name: str
    ):

        self.config_dir = config_dir
        self.epub_dir = epub_dir

        self._content_opf = format_content_opf(book_id, book_name, author_name)
        self._toc_ncx = format_toc_ncx(book_id, book_name, author_name)

        self._content_opf_manifest = ""
        self._content_opf_spine = ""
        self._toc_ncx_navMap = ""

    def set_epub_cache_file(self):
        set_epub_cache_file(self.config_dir)

    def set_cover(self, cover_url: str):
        image_path = self.config_dir + '/OEBPS/Images/' + cover_url[cover_url.rfind('/') + 1:]
        if not os.path.exists(image_path) or os.path.getsize(image_path) == 0:
            try:
                urllib.request.urlretrieve(cover_url, image_path)
                copyfile(image_path, self.config_dir + '/OEBPS/Images/cover.jpg')
            except Exception as e:
                print("Error set_cover: ", e)

    def _add_manifest_chapter(self, chapter_id: str):
        if self._content_opf_manifest.find('id="' + chapter_id + '.xhtml"') == -1:
            self._content_opf_manifest += format_manifest(chapter_id)

    def _add_spine(self, chapter_id: str):
        if self._content_opf_spine.find(f'idref="{chapter_id}.xhtml"') == -1:
            self._content_opf_spine += format_spine(chapter_id)

    def add_nav_map(self, chapter_index: str, chapter_id: str, chapter_title: str):
        if self._toc_ncx_navMap.find('id="' + chapter_id) == -1:
            self._toc_ncx_navMap += format_nav_map(chapter_id, chapter_index, chapter_title)

    def add_chapter(self, chapter_index, chapter_title, text_content_path, content_text: str):
        try:
            chapter_data = format_chapter(chapter_index, chapter_title, content_text)
            write(text_content_path, 'w', get_chapter_image(self.config_dir, chapter_data))
        except Exception as e:
            print("Error add_chapter: ", e)

    def download_book_write_chapter(self):
        file_name_list = os.listdir(os.path.join(self.config_dir, 'OEBPS', 'Text'))
        for order_count, filename in enumerate(sorted(file_name_list), start=2):
            if filename.find('$') > -1 or filename == 'cover.xhtml':
                continue
            if re.findall('^(\\d+).xhtml', filename):
                continue
            f_name = os.path.splitext(filename)[0]
            self._add_manifest_chapter(f_name)
            self._add_spine(f_name)
            _data_chapter = re.sub(r'<h3>.*?</h3>', '', write(self.config_dir + '/OEBPS/Text/' + filename, 'r').read())
            division_and_chapter_file = str_mid(_data_chapter, "<title>", "</title>")
            self.add_nav_map(str(order_count), f_name, division_and_chapter_file)

            _data_chapter = re.sub(r'</?[\S\s]*?>', '', _data_chapter)
            write(os.path.splitext(self.epub_dir)[0] + ".txt", 'a', re.sub(r'[\r\n]+', '\r\n', _data_chapter))
            order_count += 1

        for filename in sorted(os.listdir(self.config_dir + '/OEBPS/Images/')):
            if self._content_opf_manifest.find('id="' + filename + '"') == -1:
                _media_type = 'image/png' if filename.endswith('.png') else 'image/jpeg'
                self._content_opf_manifest += format_image_format_manifest(filename, _media_type)
        self.epub_file_export()

    def epub_file_export(self):
        self._content_opf = update_content_opf_spine(self._content_opf, self._content_opf_spine)
        self._content_opf = update_content_opf_manifest(self._content_opf, self._content_opf_manifest)
        self._toc_ncx = update_nav_map(self._toc_ncx, self._toc_ncx_navMap)

        write(os.path.join(self.config_dir, 'OEBPS', 'content.opf'), 'w', self._content_opf)
        with codecs.open(self.config_dir + '/OEBPS/toc.ncx', 'w', 'utf-8') as _file:
            _file.write(self._toc_ncx)
        with zipfile.ZipFile(self.epub_dir, 'w', zipfile.ZIP_DEFLATED) as _file:
            _result = get_all_files(self.config_dir)
            for _name in _result:
                _file.write(_name, _name.replace(self.config_dir + '/', ''))
