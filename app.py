from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__, static_folder='.', template_folder='.')
openai.api_key = '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'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/story', methods=['POST'])
def story():
    name = request.form['name']
    hobbies = request.form['hobbies']
    friends = request.form['friends']
    storyAbout = request.form['storyAbout']
    ageRange = request.form['ageRange']

    story_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a children's story teller. You write in standard English. You use perfect grammar. You must use capital letters at the beginning of each sentence."},
            {"role": "user", "content": f"Write a story about {name} who is in the age range of {ageRange}. {name} likes to {hobbies}. {name}'s best friends are {friends}. The story should be about {storyAbout}."},
        ]
    )

    story_text = story_response['choices'][0]['message']['content']

    prompt_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You read stories and then generate a prompt for DALL·E about the stories. Must be kid-friendly. Clearly specify no text. Use a cartoon style."},
            {"role": "user", "content": f"Make a DALL·E prompt for this story: {story_text}"},
        ]
    )

    iprompt = prompt_response['choices'][0]['message']['content']

    image_response = openai.Image.create(
        prompt=iprompt,
        n=1,
        size="1024x1024"
    )

    image_url = image_response['data'][0]['url']

    return jsonify({
        'story': story_text,
        'iprompt': iprompt,
        'image_url': image_url
    })

if __name__ == "__main__":
    app.run(debug=True)

