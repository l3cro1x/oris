import socket
import random

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

address = ('127.0.0.1', 8000)
sock.bind(address)
sock.listen()
print(f"started listening on {address}")

print(f"waiting for client to connect...")
client_sock, client_addr = sock.accept()

print(f"connected from: {client_addr}")

number: int = random.randint(0, 99)
words = ["man", "woman", "boy", "girl", "child", "friend", "family", "mother", "father", "brother", "sister", "name",
         "people", "house", "room", "door", "window", "table", "chair", "bed", "key", "book", "pen", "paper", "phone",
         "clock", "food", "water", "bread", "milk", "tea", "coffee", "apple", "banana", "meat", "fish", "cheese", "egg",
         "sugar", "time", "day", "week", "month", "year", "morning", "afternoon", "evening", "night", "hour", "minute",
         "weekend", "city", "town", "street", "shop", "school", "hospital", "car", "bus", "train", "plane", "ticket",
         "world", "sun", "moon", "sky", "tree", "flower", "animal", "dog", "cat", "bird", "weather", "sea", "money",
         "work", "job", "life", "thing", "word", "question", "answer", "problem", "student", "teacher", "doctor",
         "body", "head", "hand", "eye", "face", "foot", "class", "lesson", "homework", "game", "box", "bag", "coat",
         "shoe"]
word = list(words[number])

word_length = len(word)
send_message = ['_' for i in range(word_length)]
while True:
    data_bytes: bytes = client_sock.recv(5120)
    if not data_bytes:
        print("connection closed")
        break
    try:
        client_message =data_bytes.decode("utf-8")
    except UnicodeDecodeError:
        print("invalid data")
        break
    # business logic
    if not client_message: continue
    if list(client_message) == word:
        response = f"you won, word was {''.join(word)}. try again"
        client_sock.sendall(response.encode('utf-8'))
        number: int = random.randint(0, 99)
        word = list(words[number])
        word_length = len(word)
        send_message = ['_' for i in range(word_length)]
        continue
    for i in range(min(word_length,len(client_message))):
        if word[i] == client_message[i]:
            send_message[i] = word[i]
    if not ('_' in send_message):
        response = f"you won, word was {''.join(word)}. try again"
        client_sock.sendall(response.encode('utf-8'))
        number: int = random.randint(0, 99)
        word = list(words[number])
        word_length = len(word)
        send_message = ['_' for i in range(word_length)]
        continue

    status = f"{''.join(send_message)}\n"
    client_sock.sendall(status.encode("utf-8"))

client_sock.close()
sock.close()
