# main.py
from flask import Flask, render_template, request
from os import environ
import openai
import tiktoken

openai.api_key = environ.get("OPENAI_API_KEY")
openai.organization = environ.get("OPENAI_ORGANIZATION")

system_message = {
    "role": "system",
    "content": "You are a helpful travel assistant. Therefore, only answer questions related to travel and hospitality."\
               " Return the answer in the JSON format with the following elements\n"\
               "- is_valid_question: true if the question is either about travel and hospitality; otherwise, false\n"\
               "- has_intent_to_enquire: true if the user's intention is to make an enquiry; otherwise, false\n"\
               "- is_asking_itinerary: true if the question asks for an itinerary; otherwise, false\n"\
               "- is_asking_price: true if the question asks for a price; otherwise, false\n"\
               "If the user asks for an itinerary, return is_asking_itinerary as true and highlight the authentic experiences"\
               " related to the user's query without creating an itinerary.\n"\
               "If the user asks for a price; either a price of an itinerary, an accommodation, a travel event, a travel activity,"\
               " return is_asking_price as true and ask them to contact our travel concierge team for an accurate price. This is"\
               " because price and availability can vary from time to time."
}
max_response_tokens = 100
token_limit= 4096
conversation=[]
conversation.append(system_message)

def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
    encoding = tiktoken.encoding_for_model(model)
    num_tokens = 0
    for message in messages:
        num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":  # if there's a name, the role is omitted
                num_tokens += -1  # role is always required and always 1 token
    num_tokens += 2  # every reply is primed with <im_start>assistant
    return num_tokens

app = Flask(__name__)

#define app routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get")
def completion_response():
    global conversation
    user_input = request.args.get('msg')   
    conversation.append({"role": "user", "content": user_input})
    conv_history_tokens = num_tokens_from_messages(conversation)

    while (conv_history_tokens+max_response_tokens >= token_limit):
        del conversation[1]
        conv_history_tokens = num_tokens_from_messages(conversation)
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = conversation,
        temperature=1,
        max_tokens=max_response_tokens,
        top_p=0.9
    )

    conversation.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
    return str(response['choices'][0]['message']['content'])


if __name__ == "__main__":
    PORT = int(os.getenv("PORT")) if os.getenv("PORT") else 8080
    app.run(host="0.0.0.0", port=PORT, debug=True)
