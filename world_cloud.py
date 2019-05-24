from wordcloud import WordCloud
from konlpy.tag import Twitter
from collections import Counter
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify

app = Flask(__name__)

font_path = 'NanumGothic.ttf'

def get_tags(text, max_count, min_length):
    t = Twitter()
    nouns = t.nouns(text)
    processed = [n for n in nouns if len(n) >= min_length]
    count = Counter(processed)
    result = {}
    for n,c in count.most_common(max_count):
        result[n] = c
    if len(result) == 0:
        result["non contents"] = 1
    return result

def make_cloud_image(tags, file_name):
    word_cloud = WordCloud(
        font_path = font_path,
        width=800, height=800, background_color="white"
    )
    word_cloud = word_cloud.generate_from_frequencies(tags)
    fig = plt.figure(figsize=(10,10))
    plt.imshow(word_cloud)
    plt.axis("off")
    fig.savefig("outputs/{0}.png".format(file_name))


def process_from_text(text, max_count, min_length, words):
    tags = get_tags(text, max_count, min_length)
    for n, c in words.items():
        if n in tags:
            tags[n] = tags[n] * int(words[n])

    make_cloud_image(tags, "output")

@app.route("/process", methods=['GET','POST'])

def process():
    content = request.json
    words = {}
    if content['words'] is not None:
        for data in content['words'].values():
            words[data['word']] = data['weight']
            process_from_text(content['text'], content['maxCount'], content['minLength'],words)
            result = {'result': True}
    return jsonify(words)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)