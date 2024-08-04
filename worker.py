from gliner import GLiNER

model = GLiNER.from_pretrained("numind/NuZero_token")

labels = ["concept", "abbreviation"]

with open("../data/test.html", "r") as file:
    html = file.read()

text = re.sub("<[^<]+?>", "", html)


def chunk_text(text, length):
    return [text[i : i + length] for i in range(0, len(text), length)]


for chunk in chunk_text(text, 256):
    entities = model.predict_entities(chunk, labels)

    for entity in entities:
        print(entity["text"], "=>", entity["label"])
