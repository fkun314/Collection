import MeCab

text = "私は美しいバナナが好きです。"

mecabTagger = MeCab.Tagger()
node = mecabTagger.parseToNode(text)
while node:
    word = node.surface
    hinshi = node.feature.split(",")[0]
    print(word+": "+hinshi)
    node = node.next