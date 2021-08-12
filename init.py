# -*- coding: utf-8 -*-
__author__ = "Alfonso Sandoval"
__version__ = "1.0.1"
__maintainer__ = "Alfonso Sandoval"
__status__ = "Production"

import argparse,threading,yaml,csv
from ExecHandler import *

#Threads list for concurrent processing
threads = []
#Global ExecHandler for multiple threads
exec_handler = ExecHandler()

""" Google TTS Recording maker
Simple script for batch WAV prompts generation using Google Text-to-Speech services
"""

def GetArgs():
   """
   Supports the command-line arguments listed below.
   """
   parser = argparse.ArgumentParser(description= 'Batch prompt generation with Google TTS services')
   parser.add_argument('-b', '--batch', required=False, help='Amount of rows in the CSV file to process at the same time. Suggested max value is 100. Default is 10', type=int, default=10)
   parser.add_argument('configurationYAML', help='YAML file with operation settings')
   args = parser.parse_args()
   return args

def row_generator(ROWS: list, AMOUNT: int):
    """
        Yielded dispatch of rows within the CSV users file

        Input:
            ROWS -> (list): CSV file rows list
            AMOUNT -> (int): Amount of rows to yield in a single batch

        Output:
            ROWS -> (list): List with specific amount of rows from the file
    """
    for i in range(0, len(ROWS), AMOUNT):
        yield ROWS[i:i + AMOUNT]

def generate_prompt(FILE_NAME: str, PROMPT_CONTENT: str, OUTPUT_AUDIO_FORMAT:str) -> None:
    '''
        Invoke the Google Text-To-Speech service using the ExecHandler instance. If the execution is successful, an audio file will be generated in the same location where this script is executed

        Input:
            FILE_NAME -> (string): Name of the output file
            PROMPT_CONTENT -> (string): Text to convert to speech, Can be normal text or SSML syntax
            OUTPUT_AUDIO_FORMAT -> (string): Format of the output audio file
    '''
    PROMPT_RESULT = exec_handler.create_prompt(FILE_NAME,PROMPT_CONTENT)
    if PROMPT_RESULT[0]:
        print(f'✅ Prompt {FILE_NAME}.{OUTPUT_AUDIO_FORMAT} created successfully!')
    else:
        print(f'🔥 ERROR creating the prompt ({FILE_NAME}.{OUTPUT_AUDIO_FORMAT}) : ({PROMPT_RESULT[1]})')    

def main():
    ARGS = GetArgs()
    #YAML settings parsing
    with open(ARGS.configurationYAML) as f:
        CONFIG = yaml.load(f, Loader = yaml.FullLoader)
        CONFIG_GOOGLE = CONFIG['google_settings']
    #Create instance of handler for gTTS service
    VALID_HANDLER = exec_handler.set_service(
            CONFIG_GOOGLE['JSON_key'],
            CONFIG_GOOGLE['language_code'],
            CONFIG_GOOGLE['voice_name'],
            CONFIG_GOOGLE['voice_gender'],
            CONFIG_GOOGLE['audio_encoding'],
            CONFIG_GOOGLE['prompt_type'],
            CONFIG_GOOGLE['output_audio_format']
        )
    #Validate handler
    if VALID_HANDLER:
        #Open CSV file
        CSV_FILE = open(CONFIG['csv_prompts_file'])
        user_rows = list(csv.reader(CSV_FILE))
        #Yield CSV file's rows
        current_rows = row_generator(user_rows,ARGS.batch)
        #Processing of current rows in a single threaded batch
        for record in current_rows:
            for my_record in record:
                process = threading.Thread(target = generate_prompt, args=[my_record[0],my_record[1],CONFIG_GOOGLE['output_audio_format']])
                threads.append(process)
                process.start()
            for x in threads:
                x.join()
        
if __name__ == "__main__":
    main()