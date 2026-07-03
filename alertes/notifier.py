

#!/usr/bin/env python3
# Snort Sentinel - envoi d'alertes par email
# Auteur : Olivia Josie Kompane | Github : Olivia-Josie

# j'importe smtplib pour envoyer des emails
import smtplib
# j'importe email.mime pour construire le message
from email.mime.text import MIMEText
# j'importe sys pour recevoir le message d'alerte en argument
import sys

# parametres du serveur email (a adapter par l'utilisateur)
import os
EMAIL_EXPEDITEUR = os.environ.get("SENTINEL_EMAIL_FROM", "")
MOT_DE_PASSE = os.environ.get("SENTINEL_EMAIL_PASSWORD", "")
EMAIL_DESTINATAIRE = os.environ.get("SENTINEL_EMAIL_TO", "")
SERVEUR_SMTP = "smtp.gmail.com"
PORT_SMTP = 587


def envoyer_alerte(message_alerte):
    # je construis le contenu de l'email
    msg = MIMEText(f"Snort Sentinel a detecte une alerte :\n\n{message_alerte}")
    msg["Subject"] = "[Snort Sentinel] Alerte de securite detectee"
    msg["From"] = EMAIL_EXPEDITEUR
    msg["To"] = EMAIL_DESTINATAIRE

    # je me connecte au serveur SMTP et j'envoie le message
    try:
        with smtplib.SMTP(SERVEUR_SMTP, PORT_SMTP) as serveur:
            serveur.starttls()
            serveur.login(EMAIL_EXPEDITEUR, MOT_DE_PASSE)
            serveur.send_message(msg)
        print("[+] Alerte envoyee par email.")
    except Exception as e:
        print(f"[!] Erreur lors de l'envoi de l'alerte : {e}")


if __name__ == "__main__":
    # le message d'alerte est recu en argument de ligne de commande
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
        envoyer_alerte(message)
    else:
        print("[!] Aucun message d'alerte fourni.")
