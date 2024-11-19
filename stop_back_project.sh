# #!/bin/bash

# # Chemin racine des modules
# MAIN_ROOT="/mnt/c/Users/Utilisateur/Desktop/git_stage/stage/"

# # Fonction pour arrêter un processus par nom
# stop_process() {
#     local name="$1"
#     local command="ps aux | grep $name | grep -v grep | awk '{print \$1}'"
#     local pid=$(eval "$command")
#     if [ ! -z "$pid" ]; then
#         kill $pid
#         echo "Arrêt de $name..."
#         sleep 5
#         kill -9 $pid
#         echo "$name arrêté."
#     else
#         echo "$name n'est pas en cours d'exécution."
#     fi
# }

# # Arrêter les API
# stop_process "ApiDb"
# stop_process "ApiWhisper"
# stop_process "ApiChatbot"

# echo "Toutes les API ont été arrêtées."


#!/bin/bash

# Chemin racine des modules
MAIN_ROOT="/mnt/c/Users/Utilisateur/Desktop/git_stage/stage/"

# Fonction pour arrêter un processus par nom
stop_process() {
    local name="$1"
    # Rechercher les PIDs des processus qui correspondent au nom
    local pids=$(pgrep -f "$name")

    if [ -n "$pids" ]; then
        echo "Arrêt de $name..."
        # Envoyer un signal SIGTERM pour chaque PID
        kill $pids
        sleep 5
        # Forcer l'arrêt si le processus n'est pas terminé
        kill -9 $pids 2>/dev/null
        echo "$name arrêté."
    else
        echo "$name n'est pas en cours d'exécution."
    fi
}

# Arrêter les API
stop_process "ApiDb"
stop_process "ApiWhisper"
stop_process "ApiChatbot"

echo "Toutes les API ont été arrêtées."
