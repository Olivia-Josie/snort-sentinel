#!/usr/bin/env python3
# Snort Sentinel - surveillance des alertes en temps reel avec regroupement
# Auteur : Olivia Josie Kompane | Github : Olivia-Josie

import subprocess
import time
import threading
from notifier import envoyer_alerte

FICHIER_LOG = "/var/log/snort/alert_fast.txt"
INTERVALLE_ENVOI = 30  # secondes entre chaque email groupe

# buffer partage entre les threads
buffer_alertes = []
verrou = threading.Lock()

def envoyer_resume():
    """Envoie un email groupe toutes les INTERVALLE_ENVOI secondes si des alertes sont en attente."""
    while True:
        time.sleep(INTERVALLE_ENVOI)
        with verrou:
            if buffer_alertes:
                nombre = len(buffer_alertes)
                # on limite l'affichage a 20 lignes dans l'email pour rester lisible
                extrait = "\n".join(buffer_alertes[:20])
                if nombre > 20:
                    extrait += f"\n... et {nombre - 20} autres alertes."
                message = f"{nombre} alerte(s) detectee(s) au cours des {INTERVALLE_ENVOI} dernieres secondes :\n\n{extrait}"
                envoyer_alerte(message)
                buffer_alertes.clear()

def surveiller():
    print(f"[*] Surveillance de {FICHIER_LOG} demarree (regroupement toutes les {INTERVALLE_ENVOI}s)...")

    # on demarre le thread d'envoi groupe en arriere-plan
    thread_envoi = threading.Thread(target=envoyer_resume, daemon=True)
    thread_envoi.start()

    process = subprocess.Popen(
        ["sudo", "tail", "-F", "-n", "0", FICHIER_LOG],
        stdout=subprocess.PIPE,
        text=True
    )
    for ligne in process.stdout:
        ligne = ligne.strip()
        if ligne:
            print(f"[!] Nouvelle alerte detectee : {ligne}")
            with verrou:
                buffer_alertes.append(ligne)

if __name__ == "__main__":
    surveiller()
