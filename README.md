# 晋江小说下载器


## 介绍
- 本项目是一个用于下载晋江小说的命令行工具，支持下载单本小说，也支持下载多本小说。
- 项目基于晋江 android api 开发，使用时需要登入晋江账号```--login username password```
- 登入后会在当前目录下生成一个```config.json```文件，下次使用时会自动读取该文件，无需再次登入。
- 本项目基于Python3开发，使用了requests库，使用前请确保已安装requests库，安装方法：`pip install requests`。
- 本项目仅供学习交流使用，不得用于商业用途，否则后果自负，作者不承担任何责任。


## 命令行参数
```
optional arguments:
  -h, --help            show this help message and exit
  -d DOWNLOADBOOK, --id DOWNLOADBOOK
                        please input book_id
  -s SEARCH, --search SEARCH
                        search book by book name
  -m THREADING_MAX, --max THREADING_MAX
                        please input max threading
  -up, --update         update books
  -clear, --clear_cache
  -l LOGIN [LOGIN ...], --login LOGIN [LOGIN ...]  login account and password
```
