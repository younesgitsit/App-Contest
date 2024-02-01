import speech_recognition as sr
import openai

openai.api_key = "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" # Secret API key

recognizer = sr.Recognizer()

# Function for making text requests to an OpenAI text generation model 
def chat(prompt):
    response = openai.ChatCompletion.create(
        model = "gpt-4-0314",
        messages = [{"role": "user", "content": prompt},
                    {"name": "DiceDecide","role": "system", "content": "CONSTRAINTS: If the input is not a prompt for different decisions, respond with a '--' and nothing else. You: are an app called DiceDecide. The user will begin by saying DiceDecide>> followed by some options. Task: Make a decision for the user, choose one of the options they propose. If applicable, base the decision off of logic, otherwise just for fun (a decision must be made). Format: Provide the full chosen decision from the prompt. On a new line, a short cool explanation with an emoji if needed."}]
    )
    return response.choices[0].message.content.strip()



with sr.Microphone() as source:
    print("Speak now...")
    audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)


try:
    text = recognizer.recognize_google(audio)
    # Generating decision based on user's prompt
    response = chat(text)
    print("Decision: ", response)

    if response != "--":
        # Generating image prompt based on the decision DiceDecide made
        imagePrompt = "Create a cool stylized image in connection to the object of this phrase: " + response.split('\n')[0]
        # Feeding image prompt to an OpenAI image generation model
        image = openai.Image.create(
            model="dall-e-3",
            prompt=imagePrompt,
            size="1024x1024",
            quality="standard",
            n=1,)
        image_url = image.data[0].url
        print(image_url)
except sr.UnknownValueError:
    print("error")
except sr.RequestError as e:
    print("error; {0}".format(e))
