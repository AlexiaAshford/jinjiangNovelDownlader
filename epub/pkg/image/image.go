package image

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"path"
	"strings"
)

func DownloaderCover(CoverUrl string) string {
	var imageFile []byte
	if resp, err := http.Get(CoverUrl); err != nil {
		fmt.Println("Download error", err)
		imageFile = nil
	} else {
		defer func(Body io.ReadCloser) {
			if err = Body.Close(); err != nil {
				fmt.Println("Close error", err)
			}
		}(resp.Body)
		if imageFile, err = io.ReadAll(resp.Body); err != nil {
			fmt.Printf("Read http response failed! %v", err)
			imageFile = nil
		}
	}

	if imageFile != nil {
		var coverName string
		if strings.Contains(path.Base(CoverUrl), ".jpg") {
			coverName = path.Join("cover", path.Base(CoverUrl))
		} else {
			coverName = path.Join("cover", path.Base(CoverUrl)+".jpg")
		}
		if err := os.WriteFile(coverName, imageFile, 0666); err != nil {
			fmt.Println("WriteFile error", err)
		}
		return coverName
	} else {
		fmt.Println("download cover failed: ", CoverUrl)
	}
	return ""
}
