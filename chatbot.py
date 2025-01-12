# 1. detect wake word,
# 2. prompt for question, 
# 3. pass query to OpenAi and 
# 4. speak response


import waitForWakeWord

#import callOpenai
#import openai
#from gtts import gTTS
#import playsound
import subprocess, os
from config import gemini_key
#from speech_to_text import recognize_speech
from stt_gg_cloud_v2 import stt_process
from text_to_speech import text_to_speech
from pixels import Pixels
import google.generativeai as genai

"""
def speak(text, filename):
  tts = gTTS(text=text, lang="en")
  tts.save(filename)
"""
# Cấu hình Generative AI
genai.configure(api_key=gemini_key)
model = genai.GenerativeModel("gemini-1.5-flash")
# Hàm sinh phản hồi từ Generative AI
def generate_ai_response(data):
    response = model.generate_content(data)
    return response.text
    
def play(filename):
  #playsound.playsound(filename)
  subprocess.call(["ffplay", "-nodisp", "-autoexit", filename])
  os.remove(filename)

def main():
    #openai.api_key =  keys.key['OPEN_AI_KEY']
    filename = "respond.mp3"
    loi=0
    """
    def Gspeak(speech, filename):
        speak(speech, filename)
        play(filename)
        return
    """
    pixels = Pixels()
    pixels.speak()
    speech = "Xin chào, mời bạn đánh thức và ra khẩu lệnh cho tôi"
    text_to_speech(speech, filename)
    play(filename)
    pixels.off()
    #Gspeak(speech, filename)

    

    while True:
        success = waitForWakeWord.wait()
        if not success:
            break  # Nếu không kích hoạt, thoát chương trình
        while success:
            #Gspeak("Ask me a question or say quit", filename)
            pixels.wakeup()
            subprocess.call(["ffplay", "-nodisp", "-autoexit", 'ding.mp3'])
            #text_to_speech("Xin chào", filename)
            #play(filename)
            #query = recognize_speech()
            query = stt_process()
            pixels.think()
            try:
                if query != 'Chào bạn':
                    #Gspeak("I think you said " + str(query) + ". Asking chat g p t", filename)
                    #response = callOpenai.openai_create(query)
                    gemini_result = generate_ai_response(query)
                    print("GPT:", gemini_result)
                    pixels.speak()
                    text_to_speech(gemini_result, filename)
                    play(filename)
                else:
                    success = False
                    pixels.speak()
                    text_to_speech("chào bạn", filename)
                    play(filename)
            except Exception as e:
                print(f"Lỗi xử lý: {e}")
                answer_text = 'Không nhận dạng được câu lệnh'
                pixels.speak()
                text_to_speech(answer_text, filename)
                play(filename)
                loi=loi+1
                if(loi==2): 
                    loi=0
                    success = False
            pixels.off()
            subprocess.call(["ffplay", "-nodisp", "-autoexit", "/home/pi/Personal-AI-Assistant/sounds/dong.mp3"])
            pixels.off()
            print("End trò chuyện")

    subprocess.call(["ffplay", "-nodisp", "-autoexit", 'dong.mp3'])
if __name__ == "__main__":
    main()