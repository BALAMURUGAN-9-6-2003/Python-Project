import pprint
import google.generativeai as palm
import speech_recognition as sr
import pyttsx3

def voice():
    listener = sr.Recognizer()
    command = ""
    
    try:
        with sr.Microphone() as source:
            print("Listening...")
            listener.adjust_for_ambient_noise(source,1)
            audio = listener.listen(source)
            command = listener.recognize_google(audio)
            print(command)
            print("End")

    except sr.UnknownValueError:
        print("Could not understand audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

    return command

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    palm.configure(api_key='AIzaSyBtFg0uv0_CAzjXDXNdQs987wqo5z11RK4')

    models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
    model = models[0].name
    print(model)
    
    speak("Hello! I am your voice assistant. How can I assist you today?")

    while True:
        command = voice()
        command = command.lower()

        if "stop" in command or "exit" in command:
            speak("Goodbye!")
            break
        elif "hello" in command:
            speak("Hi there!")
        elif "how are you" in command:
            speak("I'm doing well, thank you!")
        else:
            # Extract the relevant part for generating text
            
            prompt=command
            if prompt == "exit":
                quit()
            try:
                completion = palm.generate_text(
                    model=model,
                    prompt=prompt,
                    max_output_tokens=800,
                )
                speak(completion.result)
            except:
                speak("I cant understand pleas tell again")
                
