from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow CORS for all origins

openai.api_key = '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'  
messages = [{"role": "system", "content": "You are an intelligent assistant."}]


@app.route('/chat', methods=['POST'])
def receive_data():
    try:
        data = request.form.to_dict()
        print(data)
        user_input = data.get('type')
        print(user_input)
        ingredients = data.get('ingredients')
        print(ingredients)

        if user_input:
            messages.append({"role": "user", "content": "make a recipe which is " + user_input})
            if ingredients:
                messages.append({"role": "user", "content": "using these ingredients " + ingredients + " and their nutritional values"})
                print(messages)
            
            chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=messages
            )

            reply = chat.choices[0].message.content
            messages.append({"role": "assistant", "content": reply})

            return jsonify({'reply': reply})
        else:
            return jsonify({'error': 'No input provided'})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'Internal Server Error'})

@app.route('/')  # Add a route for the root URL
def root():
    return "Welcome to the ChatGPT API!"

if __name__ == '__main__':
    app.run(debug=True)
