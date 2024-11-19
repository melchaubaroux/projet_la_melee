#!/bin/bash

# Racine des différents modules à activer
MAIN_ROOT="/mnt/c/Users/Utilisateur/Desktop/git_stage/stage/"



# Noms des services back à activer
API_DB="ApiDb/ApiDb.py"
API_WHISPER="ApiWhisper/ApiWhisper.py"
API_CHATBOT="ApiChatbot/ApiChatbot.py"


# Activation
python "$MAIN_ROOT$API_DB" & 
python "$MAIN_ROOT$API_WHISPER" & 
python "$MAIN_ROOT$API_CHATBOT"
