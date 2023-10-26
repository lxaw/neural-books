# For making audiobooks from text.

多少のわかりにくいところがあるかもしれません。もしあれば、GitIssueを使って指摘してください。

## NOTE: Only for Japanese.
Unfortunately, I have only tested this for Japanese. As there are a plethora of language voice models out there, I am sure you can find what you are looking for. As such, this is mainly for a Japanese audience, or those who are learning Japanese.

Voice from (write this later)

## Accepted File Types:
- PDF
- MOBI
- EPUB
- TXT

## 概要
本を長時間読むと、目が疲れますよね。朗読とかもありますが、大抵の場合は有料で、しかも限られたタイトルにしかありません。
合成音声を使ってオーディオブックを作れば、お金を払わずに高音質のオーディオブックが手に入ります。

このリポジトリの中にあるコードを使えば、声優並みの声であなたの読みたい本が朗読されます。いい時代になりました！

### リポジトリの構成:
。。。（後で記述します）


### 参照文献：
- https://r9y9.github.io/ttslearn/latest/index.html
- https://github.com/r9y9/ttslearn

### 使用例：
`python gen_mp3s.py -g book.txt`
`python gen_mp3s.py -c combined.mp3`
