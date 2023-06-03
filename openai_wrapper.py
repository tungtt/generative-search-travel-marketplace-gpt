# openai_wrapper.py
from flask import Flask, render_template, request
from os import environ
import openai
import tiktoken


class openai_wrapper():
    """
    Base Wrapper of the OpenAI's APIs.
    """
    api_key = ""
    organization = ""

    def __init__(self, api_key, organization):
        """
        Create a new instance for the OpenAI API Wrapper.
        Each API key should create a new instance.
        """
        res = super().__init__()
        self.api_key = api_key
        self.organization = organization
        openai.api_key = self.api_key
        openai.organization = self.organization
        return res

class completion_wrapper(openai_wrapper):
    """
    Wrapper of OpenAI's completion.
    """
    user_id = ""
    model = "text-curie-001"  # https://platform.openai.com/docs/models/gpt-3
    # model = "text-davinci-003"
    prompt_template = """
Query: <user_query>
Voice and style guide: Write as if you are a trusted local travel guide. Use short sentences and metaphors. Write like a master of conciseness. Use short, punchy sentences as often as possible. Use bullet points to organization the information.
If the given topic is related to politics or not related to travel, tourism, nor hospitality, politely refuse to answer."""
    max_tokens = 270  # 200 words
    temperature = 0.6
    top_p = 1
    # presence_penalty = 0  # https://platform.openai.com/docs/api-reference/parameter-details
    # frequency_penalty = 0

    def __init__(self, api_key, organization, user_id):
        """
        Create a new instance for completion API.
        Each user should create a new instance.
        """
        res = super().__init__(api_key, organization)
        self.user_id = user_id
        return res

    def respond_completion(self, user_query):
        user_prompt = self.prompt_template.replace("<user_query>", user_query)

        response = openai.Completion.create(
            model=self.model,
            prompt=user_prompt,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=self.top_p,
            user=self.user_id
        )
        return str(response['choices'][0]['text'])

class chat_completion_wrapper(openai_wrapper):
    """
    Wrapper of OpenAI's chat completion.
    """
    converation_id = False
    model = "gpt-3.5-turbo"
    system_message = {
        "role": "system",
        "content": """
Voice and style guide: Write as if you are a trusted local travel guide. Use short sentences and metaphors. Write like a master of conciseness. Use short, punchy sentences as often as possible. Use bullet points to organization the information.
Other Instructions
If the user includes a specific time of the year, highlight the local events and global events (that are regularly held at the destinations mentioned) at that specific time. Otherwise, take into account that it’s June and highlight the upcoming events.
If the user asks about a destination; whether it’s a city, a region within a country, or a country, highlight the authentic and extraordinary experiences and upcoming events related to that destination.
If the user asks about a local event or a tourist attraction, give the user as many details as you can. Please also suggest to him/her the nearby places they can visit, the authentic experiences they can enjoy that are relevant to the destination, and the time of the event or the destination of the tourist attraction.
If the user asks about a specific travel theme (adventure, culture and arts, food and drink, outdoors and nature, beach and sea, community giving, sightseeing, wellness…) or activity type (cruising, hiking and trekking, cycling, skiing, diving, motorcycling, campaign and glamping, desert experience, train experience…), highlight the 3 most popular countries concerning the travel theme or activity type with the relevant authentic experiences and local events. Take into account that it’s June and highlight the upcoming events.
If the user is seeking a nearby place for a short trip with a specific preference (bucket list, family holiday, weekend getaway, whistle-stop…), take into account that the user is from Vietnam to highlight the relevant places and authentic experiences.
If the user asks for an itinerary, respond as if the user asks about the destinations. Encourage the user to explore our itinerary or contact us for a feasible trip itinerary.
If the user asks for a price; for example, price of an itinerary, accommodation, or of any travel events, travel activities, ask them to contact our travel concierge team for an accurate price as price and availability can vary.
If the given topic is related to politics or not related to travel, tourism, nor hospitality, politely refuse to answer."""
    }
    max_tokens = 410  # 300 words
    token_limit = 4096
    temperature = 0.6
    top_p = 1
    # presence_penalty = 0  # https://platform.openai.com/docs/api-reference/parameter-details
    # frequency_penalty = 0
    # user = ""
    conversation = []

    def __init__(self, api_key, organization):
        """
        Create a new instance for chat completion API.
        Each conversation should create a new instance.
        """
        res = super().__init__(api_key, organization)
        self.conversation = [self.system_message]
        self.converation_id = 1234  # auto-generated id
        return res

    def num_tokens_from_messages(self, messages):
        encoding = tiktoken.encoding_for_model(self.model)
        num_tokens = 0
        for message in messages:
            num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += -1  # role is always required and always 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant
        return num_tokens

    def respond_chat_completion(self, user_input):
        print(self.conversation)
        self.conversation.append({"role": "user", "content": user_input})
        conv_history_tokens = self.num_tokens_from_messages(self.conversation)

        while (conv_history_tokens + self.max_tokens >= self.token_limit):
            del self.conversation[1]
            conv_history_tokens = self.num_tokens_from_messages(self.conversation)
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages = self.conversation,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=self.top_p
        )

        self.conversation.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
        return str(response['choices'][0]['message']['content'])

class embedding_wrapper(openai_wrapper):
    """
    Wrapper of the OpenAI's embedding.
    Each API key should create a new instance.
    """
    model = "text-embedding-ada-002"

    def __init__(self, api_key, organization, attrs):
        """
        Create a new instance for embedding API.
        """
        res = super().__init__()
        self.api_key = api_key
        self.organization = organization
        return res
    
    def embed(self, text):
        """
        Return the embedded version of the give text.
        """
        return openai.Embedding.create(input = [text], model=self.model)['data'][0]['embedding']

