import time

nos = [0, 1, 2, 3, 4]

token = 0

while True:
    print(f"Nó {token} tem o token e está transmitindo...")
    time.sleep(1)
    token = (token + 1) % len(nos)