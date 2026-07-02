#!/bin/bash
# Snort Sentinel - scriptd'installation automatique
# Auteur : Olivia Josie Kompane | Github: Olivia-Josie

echo "=== Installation de Snort Sentinel ==="

# je verifie si le script est lance en root,necessaire pour installer des paquets
if ["$EUID" -ne 0 ]; then
echo "[!] Merci de lancer ce script avec sudo."
exit 1
fi

echo "[+] Mise a jour des paquets..."
apt update -y

echo "[+] Installation de Snort..."
apt install -y snort

echo "[+] Installation de MariaDB..."
apt install -y mariadb-server

echo "[+] Installation de Grafana..."
apt install -y grafana

echo "=== Installation terminee ! ==="
echo "Prochaine etape : configure tes regles dans rules / et lance Snort."
