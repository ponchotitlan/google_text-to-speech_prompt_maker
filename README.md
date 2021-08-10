# Google Text-To-Speech Batch Prompt File Maker

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)

Are you in the need of IVR prompts, but you have no voice actors? Let Google talk your prompts like a pro! This repository contains a tool for generating Google Text-To-Speech audio files in batch. It is ideal for offline prompts creation with Google voices for application in offline IVRs

In order to use this repository, clone the contents in your local environment with the following console command:
```
git clone https://github.com/ponchotitlan/google_text-to-speech_prompt_generator.git
```

Once cloned, follow the next steps for environment setup: 

## 1) GCP account setup

Before adjusting up the contents of this project, it is neccesary to setup the Cloud Text-to-Speech API in your Google Cloud project:

1. [Follow the official documentation](https://cloud.google.com/text-to-speech/docs/quickstart-protocol) for activating this API and creating a Service Account
2. Generate a JSON key associated to this Service Account
3. Save this JSON key file in the same location as the contents of this repository

## 2) CSV and YAML files

Prepare a CSV document with the texts that you want to convert into prompt audio files. The CSV must have the following structure:
```
    <FILE NAME WITHOUT THE EXTENSION> , <PROMPT TEXT OR COMPLIANT SSML GRAMMAR>
```

An example would look like the following:
```
    sample_prompt_01,<speak>Welcome to ACME. How can I help you today?</speak>
    sample_prompt_02,<speak>Press 1 for sales. <break time=200ms/>Press 2 for Tech Support. <break time=200ms/>Or stay in the line for agent support</speak>
    ...
```

Additionally, prepare a YAML document with the structure mentioned in the *setup.yaml* file included in this repository. The fields are the following:
```
# CSV format is: FILE_NAME , PROMPT_CONTENT
csv_prompts_file: <my_csv_file.csv>

google_settings:
    # ROUTE TO THE JSON KEY ASSOCIATED TO GCP. 
    IF THE ROUTE HAS SPACES, ADD QUOTES TO THE VALUE
    JSON_key: <my_service_account.json>

    # PROMPT TYPE. ALLOWED VALUES ARE:
    # NORMAL (DEFAULT) | SSML
    prompt_type: NORMAL

    # FILE FORMAT. ALLOWED VALUES ARE:
    # WAV (DEFAULT) | MP3
    output_audio_format: WAV

    # COMPLIANT LANGUAGE CODE. 
    SEE https://cloud.google.com/text-to-speech/docs/voices FOR COMPATIBLE CODES
    language_code: es-US

    # COMPLIANT VOICE NAME. 
    SEE https://cloud.google.com/text-to-speech/docs/voices FOR COMPATIBLE NAMES
    voice_name: es-US-Wavenet-C

    # COMPLIANT VOICE GENDER. 
    SEE https://cloud.google.com/text-to-speech/docs/voices FOR COMPATIBLE GENDERS WITH THE SELECTED VOICE ABOVE
    voice_gender: MALE

    # COMPLIANT AUDIO ENCODING
    audio_encoding: LINEAR16
```

## 3) Dependencies installation
Install the requirements in a virtual environment with the following command:
```
pip install -r requirements.txt
```

## 4) Inline calling
The usage of the script requires the following inline elements:
```
usage: init.py [-h] [-c CONFIG] [-b BATCH]

Batch prompt generation with Google TTS services

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        YAML file with operation settings
  -b BATCH, --batch BATCH
                        Amount of rows in the CSV file to process at the same
                        time. Suggested max value is 100. Default is 10
```

An example is:
```
py init.py -c setup.yaml
```

The command prompt will show logs based on the status of each row:
```
✅ Prompt sample_prompt_04.WAV created successfully!
✅ Prompt sample_prompt_01.WAV created successfully!
✅ Prompt sample_prompt_03.WAV created successfully!
✅ Prompt sample_prompt_02.WAV created successfully!
```

The corresponding audio files will be saved in the same location where this script is executed.

## 5) Encoding for Cisco CVP Audio Elements
Unfortunately, Google Text-To-Speech service does not support the compulsory 8-bit μ-law encoding. However, there are many online services [such as this one](https://g711.org/) for achieving the aforementioned.

The resulting files can later be uploaded into the Tomcat server for usage within a design in Cisco CallStudio. The route within the CVP Windows Server VM is the following:
```
    C:\Cisco\CVP\VXMLServer\Tomcat\webapps\CVP\audio
```

Please [refer to the Official Cisco Documentation](https://www.cisco.com/c/en/us/support/docs/customer-collaboration/unified-customer-voice-portal/213253-understand-cvp-vxml-audio-path-with-tomc.html) for more information.

Crafted with :heart: by [Alfonso Sandoval - Cisco](https://linkedin.com/in/asandovalros)
