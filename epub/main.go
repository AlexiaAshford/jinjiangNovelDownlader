package main

import (
	"epubset/pkg/config"
	"epubset/pkg/epub"
	"epubset/pkg/file"
	"epubset/pkg/image"
	"epubset/transform"
	"fmt"
	"github.com/schollz/progressbar/v3"
	"os"
	"path"
	"regexp"
	"strings"
	"time"
)

var Args *config.Config

func init() {
	Args = config.InitParams()
	if Args.FileName == "" {
		fmt.Println("Please input file name, use -h to get help")
		os.Exit(0)
	}
	Args.BookName = strings.ReplaceAll(Args.FileName, ".txt", "")
}

type EpubConfig struct {
	// Epub is the main struct for the epub package.
	epub     *epub.Epub
	saveDir  string
	savePath string
}

func SetBookInfo(Author, Cover, Description string) *EpubConfig {
	Epub := &EpubConfig{epub: epub.NewEpub(Args.BookName), saveDir: "output"} // Create a new EPUB
	if Args.SaveDir != "" {
		Epub.saveDir = Args.SaveDir
	}
	// Create a new epub file
	file.CreateFile(Epub.saveDir)
	// Create a new image directory
	file.CreateFile("cover")
	// Set the output file path
	Epub.savePath = path.Join(Epub.saveDir, Args.BookName+".epub")
	Epub.epub.SetLang("zh")
	if Author != "" {
		Epub.epub.SetAuthor(Author)
	} else {
		Epub.epub.SetAuthor("侠名")
	}
	if Description != "" {
		Epub.epub.SetDescription(Description)
	} else {
		Epub.epub.SetDescription("简介信息为空")
	}
	if Cover != "" {
		Epub.DownloaderCover(Cover, true)
	} else {
		Epub.epub.AddImage("cover/cover.jpg", "cover.jpg")
		Epub.epub.SetCover("../images/cover.jpg", "")
	}
	return Epub
}

func (ep *EpubConfig) DownloaderCover(CoverUrl string, Cover bool) {
	coverName := image.DownloaderCover(CoverUrl)
	FilePath, ok := ep.epub.AddImage(coverName, path.Base(coverName))
	if ok != nil {
		fmt.Println("AddImage error", ok)
	} else {
		fmt.Println("===>", FilePath, "added")
		if Cover {
			ep.epub.SetCover("../images/"+FilePath, "")
		} else {
			ep.AddChapter("封面", fmt.Sprintf(`<img src="%s" />`, FilePath))
		}
	}
}

func (ep *EpubConfig) AddChapter(title string, content string) {
	_, err := ep.epub.AddSection(content, title, "", "")
	if err != nil {
		fmt.Println("AddSection error", err)
		return
	}
	//println(section) // section0002.xhtml
}
func (ep *EpubConfig) Save(max_retry int) {
	if err := ep.epub.Write(ep.savePath); err != nil {
		fmt.Println("Save error:", err)
		if max_retry > 0 {
			ep.Save(max_retry - 1)
		}
	}
}

func (ep *EpubConfig) SplitChapter(fileByte []byte) {
	var title string
	var content string
	ContentList := strings.Split(string(fileByte), "\n")
	bar := progressbar.Default(int64(len(ContentList)), Args.BookName)
	title = "前言\n"
	for _, line := range ContentList {
		bar.Add(1)
		line = strings.ReplaceAll(line, "\r", "")
		if regexp.MustCompile(Args.Rule).MatchString(line) {
			if Args.TransformTW {
				title = transform.ZhTransformTw(line)
				content = transform.ZhTransformTw(content)
			} else if Args.TransformZh {
				title = transform.TwTransformZh(line)
				content = transform.TwTransformZh(content)
			}
			ep.AddChapter(title, "<h1>"+title+"</h1>"+content) // 添加章节
			title = line                                       // new title
			content = ""                                       // clear content
		} else {
			content += fmt.Sprintf("\n<p>%s</p>", line)
		}
	} //end for
	fmt.Println(Args.BookName, "done") // last chapter
}
func main() {
	// 统计耗时
	defer func(start time.Time) {
		fmt.Println("耗时：", time.Since(start))
	}(time.Now())
	Epub := SetBookInfo(Args.Author, Args.Cover, Args.Description)
	if fileByte, err := os.ReadFile(Args.FileName); err != nil {
		fmt.Println("ReadFile error", err)
	} else {
		Epub.SplitChapter(fileByte)
		Epub.Save(2)
	}
}
