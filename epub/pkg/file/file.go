package file

import (
	"fmt"
	"os"
)

func CreateFile(filename string) {
	if _, err := os.Stat(filename); os.IsNotExist(err) {
		if err = os.Mkdir(filename, os.ModePerm); err != nil {
			fmt.Println("Mkdir error", err)
		}
	}
}
