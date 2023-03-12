import os

import openai
import re
from flask import Flask, redirect, render_template, request, url_for
import sys

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        subject = request.form["course"]
        number = request.form["id"]

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(subject, number),
            max_tokens=256,
            temperature=0.6,
        )

        response_text = response.choices[0].text

        return redirect(url_for("index", result=response_text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(subject, id):
    # Read text from local file
    if subject == "EECS":
        filename = 'EECS-Courses.txt'
        regex = f"((?<=EECS\s({id}):)([\s\S]*?)(?=EECS\s\d{{3}}:|\Z))"


    elif subject == "SI":
        filename = 'SI-Courses.txt'
        regex = f"((?<=SI\s({id}):)([\s\S]*?)(?=SI\s\d{{3}}:|\Z))"


    else: 
        filename = 'General-Courses.txt'
        regex = f"((?<={subject}\s({id}):)([\s\S]*?)(?=:|\Z))"


    with open(filename, 'r') as file:
        data = file.read()
        match = re.search(regex, data)
        reviews = match.group(1)[:2500]
        print(reviews)
        # for match in matches:
        #     number = match[0]
        #     content = match[1].strip()
        #     print("MATCH", match[0])
        # print(f'Review {number}: {content}\n', file=sys.stderr)

    # for m in matches:
        
    #     reviews = m[0]
    #     print(reviews)

        prompt = """Here are some reviews of the course {subject} {id}:

        {reviews}

        In summary, what are the pros and cons of taking {subject} {id}? Answer in paragraph form.
""".format(reviews=reviews, subject=subject, id=id)
            
        print("Prompt starting...")
        print(prompt)
        print("End of prompt\n")

        return prompt
