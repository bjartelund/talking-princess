import json
import os
import sys
import pygame
import sounddevice as sd
import soundfile as sf
from ChatGPTMinimalAPI import ChatGPTAPIClient
from TTSClient import TTSApiClient
from WhisperClient import WhisperAPIClient
pygame.init()

# Define the size of the window
WINDOW_SIZE = (1024, 1024)

# Define the colors to use
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Define the font to use
FONT = pygame.font.Font(None, 36)

# Define the recording state
SMILING = "smilingmouth.png"
OPEN = "openmouth.png"
THINKING = "thinking.png"
# Define the filename to use
FILENAME = "recording.wav"
file = None
# Define the callback function to use


class SoundRecorder:
    def __init__(self):
        self.file = sf.SoundFile(FILENAME, mode='x', samplerate=44100, channels=1)
        self.stream = sd.InputStream(channels=1,samplerate=44100, callback=self.callback)
    def Start(self):
        if self.stream.closed:
            self.file = sf.SoundFile(FILENAME, mode='x', samplerate=44100, channels=1)
            self.stream = sd.InputStream(channels=1,samplerate=44100, callback=self.callback)
        self.stream.start()
    def Stop(self):
        self.stream.stop()
        self.stream.close()
        self.file.close()
    def callback(self,indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        self.file.write(indata.copy())

class SoundPlayer:
    filename = "output.wav"
    def Play(self):
        data, fs = sf.read(self.filename)
        sd.play(data, fs)

class Secrets:
    TokenOpenAI =""
    KeyGoogleAPI = ""
    def __init__(self):
        with open('secrets.json', 'r') as secretFile:
            secrets = json.load(secretFile)
            self.TokenOpenAI = secrets["OpenAI-token"]
            self.KeyGoogleAPI = secrets["GoogleAPIKey"]

# Define the main function
def main():
    # Create the Pygame window
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Sound Recorder")

    # Create the text surfaces for the buttons
    button_text = FONT.render("Start Recording", True, BLACK)

    # Create the buttons
    button = button_text.get_rect()
    button.center = (WINDOW_SIZE[0] // 4, WINDOW_SIZE[1] // 2)

    soundRecorder = SoundRecorder()
    soundPlayer = SoundPlayer()
    secrets = Secrets()
    transcriber = WhisperAPIClient(secrets.TokenOpenAI)
    synthesizer = TTSApiClient(secrets.KeyGoogleAPI)
    chatbot = ChatGPTAPIClient(secrets.TokenOpenAI)
    RECORDING = False
    BACKGROUND = pygame.image.load(SMILING)

    # Main loop
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button.collidepoint(event.pos):
                    if RECORDING is False:
                        RECORDING = True
                        soundRecorder.Start()
                        button_text = FONT.render("Stop Recording", True, BLACK)

                        BACKGROUND = pygame.image.load(THINKING)
                        print("Recording started")
                    else:
                        RECORDING = False
                        soundRecorder.Stop()
                        BACKGROUND = pygame.image.load(OPEN)
                        print("Recording stopped")
                        transcribedText = transcriber.Transcribe(FILENAME)
                        print(transcribedText)
                        chatbotResponse = chatbot.chat(transcribedText)
                        print(chatbotResponse)
                        synthesizer.Synthesize(chatbotResponse)
                        soundPlayer.Play()
                        os.remove("recording.wav")
                        button_text = FONT.render("Start Recording", True, BLACK)


        # Draw the buttons
        screen.blit(BACKGROUND,(0,0))
        pygame.draw.rect(screen, GRAY, button)
        screen.blit(button_text, button)

        # Update the display
        pygame.display.update()

if __name__ == '__main__':
    main()