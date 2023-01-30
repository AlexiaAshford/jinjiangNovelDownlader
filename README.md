# 晋江小说下载器

## 介绍

- 本项目是一个用于下载晋江小说的命令行工具，支持下载epub和txt格式的电子书。
~~- 项目基于晋江 android api 开发，使用时需要登入晋江账号```--login username password```~~
- 晋江接入了数美的图文验证码，和设备码校验，目前无法通过接口登入，你可以通过```--token <token>```参数手动添加token实现下载VIP章节。
- 登入后会在当前目录下生成一个```config.json```文件，下次使用时会自动读取该文件，无需再次登入。
- 本项目基于Python3开发，使用了requests库，使用前请确保已安装requests库，安装方法：`pip install requests`。
- 本项目仅供学习交流使用，不得用于商业用途，否则后果自负，作者不承担任何责任。

## 命令行参数

```
usage: run.py [-h] [-d DOWNLOAD] [-s SEARCH] [--token TOKEN] [--max MAX] [--update] [--login LOGIN [LOGIN ...]] [--epub] [--output [OUTPUT]] [--cache [CACHE]]  
              [--update_database]

optional arguments:
  -h, --help            show this help message and exit
  -d DOWNLOAD, --download DOWNLOAD
                        please input book_id
  -s SEARCH, --search SEARCH
                        search book by book name
  --token TOKEN         add token
  --max MAX             please input max threading
  --update              update books
  --login LOGIN [LOGIN ...]
                        login account
  --epub                output epub file
  --output [OUTPUT]     output epub file
  --cache [CACHE]       output epub file
  --update_database     update database

```
