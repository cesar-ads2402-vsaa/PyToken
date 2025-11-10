import time
import threading
import tkinter as tk
from tkinter import messagebox, ttk

class TokenRingNode:
    def __init__(self, node_id, next_node=None):
        self.node_id = node_id
        self.has_token = False
        self.next_node = next_node
        self.message_queue = []

    def receive_token(self, gui_callback, log_callback, simulator):
        if not simulator.is_running:
            return

        self.has_token = True
        gui_callback()
        log_callback(f"Node {self.node_id} recebeu o token.")

        if self.message_queue:
            self.transmit(log_callback)

        time.sleep(1)

        self.has_token = False
        gui_callback()
        log_callback(f"Node {self.node_id} passou o token para Node {self.next_node.node_id}.")

        threading.Thread(
            target=self.next_node.receive_token,
            args=(gui_callback, log_callback, simulator),
            daemon=True
        ).start()

    def transmit(self, log_callback):
        if self.has_token and self.message_queue:
            message = self.message_queue.pop(0)
            log_callback(f"Node {self.node_id} transmitindo mensagem: '{message}'")
        else:
            log_callback(f"Node {self.node_id} não pode transmitir sem token.")

    def add_message(self, message):
        self.message_queue.append(message)

class TokenRingSimulator:
    def __init__(self, num_nodes, gui_callback, log_callback):
        self.nodes = []
        self.is_running = False
        self.gui_callback = gui_callback
        self.log_callback = log_callback
        self.create_ring(num_nodes)

    def create_ring(self, num_nodes):
        self.nodes = [TokenRingNode(i) for i in range(num_nodes)]
        for i in range(num_nodes):
            self.nodes[i].next_node = self.nodes[(i + 1) % num_nodes]

    def start_simulation(self):
        if self.is_running:
            self.log_callback("A simulação já está em andamento.")
            return

        if not self.nodes:
            self.log_callback("Nenhum nó disponível para iniciar.")
            return

        self.is_running = True
        self.log_callback("Simulação iniciada.")
        threading.Thread(
            target=self.nodes[0].receive_token,
            args=(self.gui_callback, self.log_callback, self),
            daemon=True
        ).start()

    def stop_simulation(self):
        self.is_running = False
        self.log_callback("Simulação parada.")

    def add_message_to_node(self, node_id, message):
        if not message.strip():
            self.log_callback("Mensagem vazia não adicionada.")
            return

        if 0 <= node_id < len(self.nodes):
            self.nodes[node_id].add_message(message)
            self.log_callback(f"Mensagem adicionada ao Node {node_id}: '{message}'")
        else:
            self.log_callback(f"Erro: Node {node_id} não existe.")

class TokenRingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Token Ring")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        self.simulator = TokenRingSimulator(4, self.update_gui, self.log_event)

        ttk.Label(root, text="Simulador Token Ring", font=("Arial", 16, "bold")).pack(pady=10)

        self.tree = ttk.Treeview(root, columns=("status", "fila"), show="headings", height=5)
        self.tree.heading("status", text="Status do Nó")
        self.tree.heading("fila", text="Mensagens na Fila")
        self.tree.column("status", width=150)
        self.tree.column("fila", width=350)
        self.tree.pack(pady=10)

        for node in self.simulator.nodes:
            self.tree.insert("", "end", iid=node.node_id, values=(f"Nó {node.node_id}", "-"))

        msg_frame = ttk.Frame(root)
        msg_frame.pack(pady=10)

        ttk.Label(msg_frame, text="Nó destino:").grid(row=0, column=0, padx=5)
        self.node_entry = ttk.Entry(msg_frame, width=5)
        self.node_entry.grid(row=0, column=1, padx=5)

        ttk.Label(msg_frame, text="Mensagem:").grid(row=0, column=2, padx=5)
        self.msg_entry = ttk.Entry(msg_frame, width=30)
        self.msg_entry.grid(row=0, column=3, padx=5)

        ttk.Button(msg_frame, text="Adicionar Mensagem", command=self.add_message).grid(row=0, column=4, padx=5)

        control_frame = ttk.Frame(root)
        control_frame.pack(pady=10)
        ttk.Button(control_frame, text="Iniciar", command=self.start_simulation).grid(row=0, column=0, padx=10)
        ttk.Button(control_frame, text="Parar", command=self.stop_simulation).grid(row=0, column=1, padx=10)

        ttk.Label(root, text="Log de Eventos:").pack(pady=(15, 0))
        self.log_text = tk.Text(root, height=10, state="disabled", bg="#f7f7f7")
        self.log_text.pack(fill="both", padx=10, pady=5)

        self.update_gui()

    def update_gui(self):
        for node in self.simulator.nodes:
            status = "🟢 Com Token" if node.has_token else "⚪ Aguardando"
            fila = ", ".join(node.message_queue) if node.message_queue else "-"
            self.tree.item(node.node_id, values=(status, fila))

    def log_event(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert("end", f"{message}\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")
        print(message)

    def start_simulation(self):
        self.simulator.start_simulation()
        self.update_gui()

    def stop_simulation(self):
        self.simulator.stop_simulation()
        self.update_gui()

    def add_message(self):
        try:
            node_id = int(self.node_entry.get())
        except ValueError:
            messagebox.showerror("Erro", "O ID do nó deve ser um número inteiro.")
            return

        message = self.msg_entry.get().strip()
        if message:
            self.simulator.add_message_to_node(node_id, message)
            self.msg_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Aviso", "Digite uma mensagem antes de enviar.")

        self.update_gui()

if __name__ == "__main__":
    root = tk.Tk()
    app = TokenRingGUI(root)
    root.mainloop()