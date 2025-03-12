import os
from groq import Groq
from portkey_ai import Portkey

# Retrieve API keys from environment variables
groq_api_key = os.environ.get("GROQ_API_KEY")
portkey_api_key = os.environ.get("PORTKEY_API_KEY")
virtual_key = os.environ.get("VIRTUAL_KEY")

# Ensure the keys are available
if not groq_api_key or not portkey_api_key or not virtual_key:
    raise ValueError("API keys and virtual key must be set in environment variables")

client = Groq(api_key=groq_api_key)
portkey = Portkey(api_key=portkey_api_key, virtual_key=virtual_key)

# Specify the path to the audio file
filename = os.path.join(os.path.dirname(__file__), "3.mp3")  # Replace with your audio file!

def create_transcription(client, filename, audio_content):
    return client.audio.transcriptions.create(
        file=(filename, audio_content),
        model="whisper-large-v3",
        prompt="This is a conversation between peoples: Peoples discussing work issues.",
        response_format="json",
        language="tr",
        temperature=0.0
    )

def create_chat_completion(portkey, transcription_text):
    return portkey.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": ("Sen büyük bir taşımacılık şirketinde stratejik hesap çözüm direktörü olarak çalışan bir profesyonelsin. "
                            "Türkçeyi akıcı şekilde kullanıyorsun ve iş toplantıları, raporlar ve sunumlar hazırlama konusunda deneyimlisin. "
                            "Şimdi verilen toplantı notlarına dayanarak farklı formatlarda profesyonel özetler oluşturacaksın. "
                            "Yapı şu şekilde olacak: Kısa özet, Detaylı özet, Atıf içeren detaylı özet, Eylem maddeleri ve Madde madde öne çıkan noktalar. "
                            "Cevaplarını sadece Türkçe yaz, her başlığı ve alt başlığı net şekilde ayır ve maddeleme yaparken profesyonel bir dil kullan."),
            },
            {
                "role": "user",
                "content": f"İşte toplantıdan alınan notlar:\n{transcription_text} \n "
                           "Şimdi bu içerik temelinde şu yapıyı oluştur: \n "
                           "1. Kısa Özet\n "
                           "2. Detaylı Özet\n "
                           "3. Atıf İçeren Detaylı Özet\n "
                           "4. Eylem Maddeleri\n "
                           "5. Madde Madde Öne Çıkan Noktalar"
            },
        ],
        model="llama3-8b-8192",
        temperature=0.5,
        stream=True,
    )

# Main logic
try:
    with open(filename, "rb") as file:
        audio_content = file.read()
    transcription = create_transcription(client, filename, audio_content)
    stream = create_chat_completion(portkey, transcription.text)
    
    # Print the transcription text and chat completion
    print(transcription.text)
    for chunk in stream:
        print(chunk.choices[0].delta.content, end="")
except FileNotFoundError:
    raise FileNotFoundError(f"Audio file '{filename}' not found")
except IOError as e:
    raise IOError(f"Error reading file '{filename}': {e}")
