from langchain_openai import ChatOpenAI
from browser_use import Agent
from dotenv import load_dotenv
import speech_recognition as sr
import asyncio
from pathlib import Path
from openai import OpenAI
import os
from playsound import playsound 

load_dotenv(".env")
llm = ChatOpenAI(model="gpt-4o")
client = OpenAI()

async def speak(text, voice="fable", model="tts-1"):
    """Convert text to speech using OpenAI's TTS"""
    try:
        # Generate speech
        response = client.audio.speech.create(
            model=model,
            voice=voice,
            input=text,
            response_format="mp3"
        )
        
        # Create temp file
        temp_file = Path(__file__).parent / "temp_speech.mp3"
        response.stream_to_file(temp_file)
        
        # Async play and cleanup
        def play_cleanup():
            playsound(str(temp_file))
            os.remove(temp_file)
            
        await asyncio.get_event_loop().run_in_executor(None, play_cleanup)
        
    except Exception as e:
        print(f"\033[91mSpeech error: {str(e)}\033[0m")

async def get_voice_input(attempt):
    """Get voice input with conversational prompts"""
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            if attempt == 1:
                await speak("I'm listening...", voice="fable")
                print("\n[Listening...]  \U0001F3A4")
            else:
                await speak("Let me try that again...", voice="fable")
                print("\n[Retrying...]  \U0001F50A")
                
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, timeout=15, phrase_time_limit=30)
            
        text = r.recognize_google(audio, language="en-US")
        await speak(f"I heard: {text}", voice="fable")
        print(f"\n\033[94mJarvis heard:\033[0m \"{text}\"")
        return text
        
    except sr.WaitTimeoutError:
        await speak("I didn't hear anything, please try again", voice="fable")
        print("\n\033[91mTime out - No audio detected\033[0m")
    except sr.UnknownValueError:
        await speak("Sorry, I couldn't understand that", voice="fable")
        print("\n\033[91mAudio recognition failed\033[0m")
    except Exception as e:
        await speak("Oops, something went wrong", voice="fable")
        print(f"\n\033[91mError: {str(e)}\033[0m")
    return None

async def main():
    # Initial greeting
    await speak("Hi Guanming!, It's Jarvis! How can I assist you today?", voice="fable")
    print("\033[96mHi Guanming, It's Jarvis! \U0001F44B\033[0m")
    print("\033[96mHow can I assist you today?\033[0m\n")

    max_retries = 3
    for attempt in range(1, max_retries + 1):
        if task := await get_voice_input(attempt):
            agent = Agent(task=task, llm=llm)
            await speak("Processing your request...", voice="fable")
            print("\n\033[92mProcessing... \U0001F680\033[0m")
            result = await agent.run()
            
            await speak("Here's what I accomplished:", voice="fable")
            print("\n\033[95mResults:\033[0m")
            print(result)
            return
            
    await speak("Let's try again later. Goodbye!", voice="fable")
    print("\n\033[91mGoodbye! \U0001F44B\033[0m")

if __name__ == "__main__":
    asyncio.run(main())