import requests
from translate import Translator
from flask import Flask,render_template,url_for
from flask import request as req


app = Flask(__name__)
@app.route("/",methods=["GET","POST"])
def Index():
    return render_template("index.html")

@app.route("/Summarize",methods=["GET","POST"])
def Summarize():
    if req.method== "POST":
        API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
        API_TOKEN="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"
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        data=req.form["data"]

 
        maxL=int(req.form["maxL"])
        minL=maxL//4
        def my_function(sentence): 
            say_lang='en'
            convert_lang='pa-IN'
            translator=Translator(from_lang =say_lang,to_lang=convert_lang)
            translation=translator.translate(sentence)
            return translation
        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()

        output = query({
            "inputs":data,
            "parameters":{"min_length":minL,"max_length":maxL},
        })[0]
        #result=my_function(output["summary_text"])
        return render_template("index.html",result=my_function(output["summary_text"]))
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.debug=True
    app.run()