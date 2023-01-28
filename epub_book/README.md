# txt 转 epub电子书

## command

```bash
go run main.go -h
  -author string
        author name
  -cover string
        cover image
  -file string
        Input file name (required)
  -intro string
        description information
  -o string
        output dir
  -r string
        rule (default "^第[0-9一二三四五六七八九十零〇百千两 ]+[章回节集卷]|^[Ss]ection.{1,20}$|^[Cc]hapter.{1,20}$|^[Pp]age.{1,20}$|^\\d{1,4}$|^引子$|^楔子$|^ 章节目录|^章节|^序章")
  -tw
        Transform to traditional Chinese
  -zh
        Transform to simplified Chinese
  
```
