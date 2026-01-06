from flask import Flask, render_template, request
import re

app = Flask(__name__)

def check_url(url):
    score = 0

    if " " in url or not (url.startswith("http://") or url.startswith("https://")) or "." not in url:
        return "Invalid URL format ❌", 0

    if len(url) > 75:
        score += 1

    if re.search(r"\d+\.\d+\.\d+\.\d+", url):
        score += 1

    if "@" in url:
        score += 1

    if not url.startswith("https://"):
        score += 1

    suspicious_words = ["login", "verify", "update", "secure", "bank", "account"]
    for word in suspicious_words:
        if word in url.lower():
            score += 1

    if score >= 3:
        return "Phishing URL ❌", score
    else:
        return "Legitimate URL ✅", score


@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    score = None

    if request.method == "POST":
        url = request.form["url"]
        result, score = check_url(url)

    return render_template("index.html", result=result, score=score)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
