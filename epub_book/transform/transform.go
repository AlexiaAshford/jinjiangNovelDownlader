package transform

import "fmt"

func Transform(str string, original string, transformString string) string {
	var new_str string
	var transform_str string
	for _, v := range str {
		for index, v2 := range []rune(original) {
			if v == v2 {
				transform_str = fmt.Sprintf("%c", []rune(transformString)[index])
				break
			}
		}
		if transform_str == "" {
			new_str += fmt.Sprintf("%c", v)
		} else {
			new_str += transform_str
		}
		transform_str = ""
	}
	return new_str
}

// ZhTransformTw ZhTransform 简体转繁体
func ZhTransformTw(str string) string {
	return Transform(str, ZH_CH_STRING, TW_CH_STRING)
}

// TwTransform 繁体转简体
func TwTransformZh(str string) string {
	return Transform(str, TW_CH_STRING, ZH_CH_STRING)
}
