import os
from groq import Groq
from portkey_ai import Portkey

api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

portkey = Portkey(
    api_key="2vSuOCLrOosko6Y5azZ8lTLAaLCh",  # Replace with your Portkey API key
    virtual_key="virtualkey-dc5917" # Replace with your virtual key for Groq
)


# Specify the path to the audio file
filename = os.path.dirname(__file__) + "/3.mp3"  # Replace with your audio file!

# Open the audio file
with open(filename, "rb") as file:
    # Create a transcription of the audio file
    transcription = client.audio.transcriptions.create(
        file=(filename, file.read()),  # Required audio file
        model="whisper-large-v3",  # Required model to use for transcription
        prompt="This is a conversation between peoples: Peoples discussing work issues.",  # Updated prompt for context
        response_format="json",  # Optional
        language="tr",  # Optional
        temperature=0.0  # Optional
    )
    # Print the transcription text
    print(transcription.text)


# Create the prompt using the text from the .txt file and the follow-up question
stream  = portkey.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "Sen büyük bir taşımacılık şirketinde stratejik hesap çözüm direktörü olarak çalışan bir profesyonelsin. \
                        Türkçeyi akıcı şekilde kullanıyorsun ve iş toplantıları, raporlar ve sunumlar hazırlama konusunda deneyimlisin. \
                        Şimdi verilen toplantı notlarına dayanarak farklı formatlarda profesyonel özetler oluşturacaksın. \
                        Yapı şu şekilde olacak: Kısa özet, Detaylı özet, Atıf içeren detaylı özet, Eylem maddeleri ve Madde madde öne çıkan noktalar. \
                        Cevaplarını sadece Türkçe yaz, her başlığı ve alt başlığı net şekilde ayır ve maddeleme yaparken profesyonel bir dil kullan.",
        },
        {
            "role": "user",
            "content": f"İşte toplantıdan alınan notlar:\n{transcription.text} \n \
            Şimdi bu içerik temelinde şu yapıyı oluştur: \n \
            1. Kısa Özet\n \
            2. Detaylı Özet\n \
            3. Atıf İçeren Detaylı Özet\n \
            4. Eylem Maddeleri\n \
            5. Madde Madde Öne Çıkan Noktalar"
        },
    ],
    model="llama3-8b-8192",
    temperature=0.5,
    stream=True,
)

# Yanıtı al ve çıktı olarak yazdır
for chunk in stream:
    print(chunk.choices[0].delta.content, end="")
