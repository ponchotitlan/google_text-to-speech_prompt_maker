# -*- coding: utf-8 -*-
__author__ = "Alfonso Sandoval"
__version__ = "1.0.1"
__maintainer__ = "Alfonso Sandoval"
__status__ = "Production"

""" Google TTS Recording maker -> Execution Handler
Class for running the operations required for Google TTS prompt generation   
"""
from google.cloud import texttospeech
import os

class ExecHandler:
    '''
        Class constructor
    '''
    def __init__(self) -> None:
        self._VOICEPARAMS = self._AUDIOCONFIG = ''

    def set_service(self, _JSON_key, _language_code, _voice_name, _voice_gender, _audio_encoding, _prompt_type = "NORMAL", _output_audio_format= "WAV") -> None:
        '''
            Setup of Google Text-To-Speech services

            Output:
                True -> (bool) if the setup was successful
                False -> (bool) if the if the setup was not successful
        '''
        #GCP prompting parameters
        self._prompt_type = _prompt_type
        self._output_audio_format = _output_audio_format
        #OS variable for JSON keys
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = _JSON_key
        #Google TextToSpeech instance
        try:
            self._CLIENT = texttospeech.TextToSpeechClient()
            #Assembly of voice request
            self._VOICEPARAMS = texttospeech.VoiceSelectionParams(
                language_code = _language_code,
                name = _voice_name,
                ssml_gender = texttospeech.SsmlVoiceGender[_voice_gender]
            )
            self._AUDIOCONFIG = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding[_audio_encoding]
            )
            return True
        except Exception as ex:
            print(f'🔥 ERROR authenticating with gTTS API ({str(ex)})')
            return False
    
    def create_prompt(self,FILE_NAME,PROMPT_CONTENT):
        '''
            Creation of the prompt using Google Text-To-Speech service. If the creation is successful, the resulting audio file will be created in the local directory where the script is executed

            Input:
            FILE_NAME -> (string): Name of the output file
            PROMPT_CONTENT -> (string): Text to convert to speech, Can be normal text or SSML syntax

            Output:
            True -> (bool) if the creation of the audio file was successful
            False -> (bool) if the creation of the audio file was not successful
        '''
        #Prompt builder based on prompt type
        if self._prompt_type == "SSML":
            input_text = texttospeech.SynthesisInput(ssml = PROMPT_CONTENT)
        else:
            input_text = texttospeech.SynthesisInput(text = PROMPT_CONTENT)
        #Request issuing
        try:
            response = self._CLIENT.synthesize_speech(
                request = 
                    {
                        "input": input_text, 
                        "voice": self._VOICEPARAMS, 
                        "audio_config": self._AUDIOCONFIG
                    }
            )
            #Audio file dumping
            with open(f'{FILE_NAME}.{self._output_audio_format}', "wb") as AUDIO_FILE:
                AUDIO_FILE.write(response.audio_content)
                return [True,'']
        except Exception as ex:
            return [False,str(ex)]