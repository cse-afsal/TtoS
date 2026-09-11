from gtts import gTTS

text= "Hello my name is afsal . and you are a bitch"

tts = gTTS(text=text, lang='en')

tts.save("voice.mp3")

print("Audio saved sucessfully")