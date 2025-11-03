import time
import threading

class TokenRingNode:
    def __init__(self, node_id, next_node=None):
        self.node_id = node_id
        self.has_token = False
        self.next_node = next_node
        self.message_queue = []

    def receive_token(self):
        self.has_token = True
        print(f"Node {self.node_id} recebeu o token.")

        if self.message_queue:
            self.transmit()

        time.sleep(1)
        self.pass_token()

    def pass_token(self):
        self.has_token = False
        print(f"Node {self.node_id} passou o token para Node {self.next_node.node_id}.")
        self.next_node.receive_token()

    def transmit(self):
        if self.has_token and self.message_queue:
            message = self.message_queue.pop(0)
            print(f"Node {self.node_id} transmitindo: '{message}'")
        else:
            print(f"Node {self.node_id} não pode transmitir sem token.")

    def add_message(self, message):
        self.message_queue.append(message)
        print(f"Mensagem '{message}' adicionada à fila do Node {self.node_id}.")

class TokenRingSimulator:
    def __init__(self, num_nodes):
        self.nodes = []
        self.create_ring(num_nodes)

    def create_ring(self, num_nodes):
        for i in range(num_nodes):
            self.nodes.append(TokenRingNode(i))

        for i in range(num_nodes):
            self.nodes[i].next_node = self.nodes[(i + 1) % num_nodes]

    def start_simulation(self):
        if not self.nodes:
            print("Nenhum nó no anel.")
            return

        print("Iniciando simulação do Token Ring...")
        self.nodes[0].receive_token()

    def add_message_to_node(self, node_id, message):
        if 0 <= node_id < len(self.nodes):
            self.nodes[node_id].add_message(message)
        else:
            print(f"Node {node_id} não existe.")

if __name__ == "__main__":
    simulator = TokenRingSimulator(4)
    
    simulator.add_message_to_node(0, "Hello from Node 0!")
    simulator.add_message_to_node(2, "Mensagem do Node 2!")
    simulator.add_message_to_node(1, "Node 1 transmitindo!")
    
    sim_thread = threading.Thread(target=simulator.start_simulation)
    sim_thread.daemon = True
    sim_thread.start()
    
    try:
        time.sleep(15)
    except KeyboardInterrupt:
        print("\nSimulação interrompida pelo usuário.")