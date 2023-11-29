import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes


listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    command = ""
    try:
        with sr.Microphone() as source:
            print("Listening...")
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source, timeout=5, phrase_time_limit=5)
            print("Recognizing...")
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'veda' in command:
                command = command.replace('veda', '')
                print(command)

    except sr.UnknownValueError:
        print("Sorry, I couldn't understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return command

def run_veda():
    listening = True
    while listening:
        command = take_command()
        print(command)

        if 'play' in command:
            song = command.replace('play', '')
            talk('Playing ' + song)
            pywhatkit.playonyt(song)

        elif 'time' in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            talk("The current time is " + current_time)

        elif "who is" in command or "what is" in command:
            query = command.replace("who is", "").replace("what is", "")
            try:
                info = wikipedia.summary(query, sentences=3)
                talk(info)
            except wikipedia.DisambiguationError as e:
                talk(f"There are multiple results for {query}. Please be more specific.")
            except wikipedia.PageError as e:
                talk(f"Sorry, I could not find any information about {query}.")

        elif "joke" in command:
            talk(pyjokes.get_joke())

        elif 'stop' in command or 'exit' in command:
            talk("Exiting voice assistant.")
            listening = False

        elif 'stop work' in command:
            talk("Stopping voice recognition.")
            break

        else:
            talk("Sorry, I didn't understand that. Can you please repeat?")

if __name__ == "__main__":
    run_veda()
