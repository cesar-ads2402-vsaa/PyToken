import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
from datetime import datetime

class TokenRingNode:
    def __init__(self, node_id, next_node=None):
        self.node_id = node_id
        self.has_token = False
        self.next_node = next_node
        self.message_queue = []
        self.is_failed = False
        self.transmission_count = 0
        self.last_transmission = None
        self.received_messages = []

    def receive_token(self, simulator):
        if not simulator.is_running:
            return
            
        if self.is_failed:
            simulator.log_event(f"Node {self.node_id} está falho. Pulando para o próximo.")
            if self.next_node:
                self.next_node.receive_token(simulator)
            return

        self.has_token = True
        simulator.log_event(f"Node {self.node_id} recebeu o token")
        simulator.update_gui()

        if self.message_queue and simulator.is_running:
            self.transmit(simulator)

        if simulator.is_running:
            time.sleep(simulator.transmission_delay)
            self.pass_token(simulator)

    def pass_token(self, simulator):
        if not simulator.is_running:
            return
            
        self.has_token = False
        if not self.is_failed and self.next_node and simulator.is_running:
            simulator.log_event(f"Node {self.node_id} passou o token para Node {self.next_node.node_id}")
            self.next_node.receive_token(simulator)

    def transmit(self, simulator):
        if self.has_token and self.message_queue and not self.is_failed and simulator.is_running:
            message = self.message_queue.pop(0)
            simulator.log_event(f"Node {self.node_id} transmitindo: '{message}'")
            
            self.transmission_count += 1
            self.last_transmission = datetime.now().strftime("%H:%M:%S")
            self.received_messages.append(f"Transmitido: {message}")
            simulator.update_gui()

    def add_message(self, message, simulator):
        if not self.is_failed:
            self.message_queue.append(message)
            simulator.log_event(f"Mensagem '{message}' adicionada à fila do Node {self.node_id}")
            return True
        else:
            simulator.log_event(f"Falha: Node {self.node_id} está inoperante")
            return False

    def toggle_failure(self, simulator):
        self.is_failed = not self.is_failed
        status = "FALHOU" if self.is_failed else "RECUPERADO"
        simulator.log_event(f"Node {self.node_id} {status}")
        simulator.update_gui()

class TokenRingSimulator:
    def __init__(self, num_nodes=4):
        self.nodes = []
        self.is_running = False
        self.simulation_thread = None
        self.transmission_delay = 1.0
        self.log_messages = []
        self._stop_event = threading.Event()
        self.create_ring(num_nodes)

    def create_ring(self, num_nodes):
        self.nodes = []
        for i in range(num_nodes):
            self.nodes.append(TokenRingNode(i))

        for i in range(num_nodes):
            self.nodes[i].next_node = self.nodes[(i + 1) % num_nodes]

    def start_simulation(self):
        if not self.nodes:
            self.log_event("Erro: Nenhum nó no anel")
            return

        if self.is_running:
            self.log_event("Simulação já está em execução")
            return

        self.is_running = True
        self._stop_event.clear()
        self.log_event("=== INICIANDO SIMULAÇÃO TOKEN RING ===")
        
        def run_simulation():
            current_node_index = 0
            while self.is_running and not self._stop_event.is_set():
                try:
                    start_index = current_node_index
                    while True:
                        node = self.nodes[current_node_index]
                        if not node.is_failed and self.is_running:
                            break
                        current_node_index = (current_node_index + 1) % len(self.nodes)
                        if current_node_index == start_index:
                            time.sleep(0.5)
                            continue
                    
                    for n in self.nodes:
                        n.has_token = False
                    
                    node.has_token = True
                    self.update_gui()
                    node.receive_token(self)
                    
                    current_node_index = (current_node_index + 1) % len(self.nodes)
                    
                    time.sleep(0.1)
                    
                except Exception as e:
                    self.log_event(f"Erro na simulação: {str(e)}")
                    break
                    
            self.is_running = False
            self.log_event("=== SIMULAÇÃO FINALIZADA ===")

        self.simulation_thread = threading.Thread(target=run_simulation)
        self.simulation_thread.daemon = True
        self.simulation_thread.start()

    def stop_simulation(self):
        self.log_event("=== SOLICITANDO PARADA DA SIMULAÇÃO ===")
        self.is_running = False
        self._stop_event.set()
        
        for node in self.nodes:
            node.has_token = False
            
        self.update_gui()

    def add_message_to_node(self, node_id, message):
        if 0 <= node_id < len(self.nodes):
            return self.nodes[node_id].add_message(message, self)
        else:
            self.log_event(f"Erro: Node {node_id} não existe")
            return False

    def toggle_node_failure(self, node_id):
        if 0 <= node_id < len(self.nodes):
            self.nodes[node_id].toggle_failure(self)

    def log_event(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.log_messages.append(log_entry)
        if hasattr(self, 'log_text'):
            try:
                self.log_text.insert(tk.END, log_entry + "\n")
                self.log_text.see(tk.END)
            except tk.TclError:
                pass

    def update_gui(self):
        if hasattr(self, 'update_display'):
            try:
                self.update_display()
            except:
                pass

    def get_node_status(self, node_id):
        if 0 <= node_id < len(self.nodes):
            node = self.nodes[node_id]
            status = "FALHO" if node.is_failed else "OPERACIONAL"
            token = "COM TOKEN" if node.has_token else "SEM TOKEN"
            queue_size = len(node.message_queue)
            return status, token, queue_size, node.transmission_count, node.last_transmission
        return "INEXISTENTE", "", 0, 0, ""

class TokenRingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador FDDI Token Ring - Entrega 3")
        self.root.geometry("1200x800")
        
        self.simulator = TokenRingSimulator(4)
        self.simulator.update_display = self.update_display
        
        self.setup_gui()
        self.update_display()

    def setup_gui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))

        self.start_btn = ttk.Button(control_frame, text="Iniciar Simulação", 
                                   command=self.start_simulation)
        self.start_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.stop_btn = ttk.Button(control_frame, text="Parar Simulação", 
                                  command=self.stop_simulation, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame, text="Reiniciar Anel", 
                  command=self.reset_ring).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Limpar Log", 
                  command=self.clear_log).pack(side=tk.LEFT, padx=5)

        ttk.Label(control_frame, text="Atraso (s):").pack(side=tk.LEFT, padx=(20, 5))
        self.delay_var = tk.DoubleVar(value=1.0)
        delay_spin = ttk.Spinbox(control_frame, from_=0.1, to=5.0, increment=0.1,
                               textvariable=self.delay_var, width=5,
                               command=self.update_delay)
        delay_spin.pack(side=tk.LEFT, padx=5)

        self.status_indicator = tk.Canvas(control_frame, width=20, height=20, bg='red')
        self.status_indicator.pack(side=tk.LEFT, padx=(20, 5))
        ttk.Label(control_frame, text="Parada").pack(side=tk.LEFT)

        paned_window = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True)

        left_frame = ttk.Frame(paned_window)
        paned_window.add(left_frame, weight=1)

        status_frame = ttk.LabelFrame(left_frame, text="Status dos Nós", padding="10")
        status_frame.pack(fill=tk.BOTH, expand=True)

        self.node_frames = []
        for i in range(4):
            node_frame = ttk.LabelFrame(status_frame, text=f"Node {i}", padding="8")
            node_frame.pack(fill=tk.X, pady=5)
            
            status_row = ttk.Frame(node_frame)
            status_row.pack(fill=tk.X)
            
            status_canvas = tk.Canvas(status_row, width=20, height=20, bg='red')
            status_canvas.pack(side=tk.LEFT, padx=(0, 10))
            
            status_text_frame = ttk.Frame(status_row)
            status_text_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            status_label = ttk.Label(status_text_frame, text="Status: FALHO")
            status_label.pack(anchor=tk.W)
            
            token_label = ttk.Label(status_text_frame, text="Token: SEM TOKEN")
            token_label.pack(anchor=tk.W)
            
            queue_label = ttk.Label(status_text_frame, text="Fila de Mensagens: 0")
            queue_label.pack(anchor=tk.W)
            
            stats_label = ttk.Label(status_text_frame, text="Transmissões: 0 | Última: N/A")
            stats_label.pack(anchor=tk.W)
            
            btn_frame = ttk.Frame(node_frame)
            btn_frame.pack(fill=tk.X, pady=(5, 0))
            
            ttk.Button(btn_frame, text="Falhar/Recuperar", 
                      command=lambda n=i: self.toggle_node_failure(n)).pack(side=tk.LEFT, padx=(0, 5))
            ttk.Button(btn_frame, text="Enviar Mensagem", 
                      command=lambda n=i: self.send_message_dialog(n)).pack(side=tk.LEFT, padx=(0, 5))
            ttk.Button(btn_frame, text="Ver Mensagens", 
                      command=lambda n=i: self.show_messages(n)).pack(side=tk.LEFT)
            
            self.node_frames.append({
                'canvas': status_canvas,
                'status': status_label,
                'token': token_label,
                'queue': queue_label,
                'stats': stats_label
            })

        message_control_frame = ttk.LabelFrame(left_frame, text="Controles Rápidos", padding="10")
        message_control_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(message_control_frame, text="Mensagem Aleatória para Nó Aleatório", 
                  command=self.send_random_message).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(message_control_frame, text="Broadcast para Todos", 
                  command=self.broadcast_message).pack(side=tk.LEFT, padx=5)
        ttk.Button(message_control_frame, text="Teste de Estresse", 
                  command=self.stress_test).pack(side=tk.LEFT, padx=5)

        right_frame = ttk.Frame(paned_window)
        paned_window.add(right_frame, weight=1)

        log_frame = ttk.LabelFrame(right_frame, text="Log de Eventos em Tempo Real", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True)

        self.log_text = scrolledtext.ScrolledText(log_frame, width=60, height=25)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.simulator.log_text = self.log_text

        stats_frame = ttk.LabelFrame(right_frame, text="Estatísticas do Sistema", padding="10")
        stats_frame.pack(fill=tk.X, pady=(10, 0))

        self.stats_label = ttk.Label(stats_frame, text="Total de Transmissões: 0 | Nós Ativos: 4/4 | Status: Parado")
        self.stats_label.pack(anchor=tk.W)

    def update_display(self):
        total_transmissions = 0
        active_nodes = 0
        
        for i in range(4):
            status, token, queue_size, transmissions, last_trans = self.simulator.get_node_status(i)
            
            color = 'red' if status == "FALHO" else 'green'
            if token == "COM TOKEN":
                color = 'yellow'
            
            self.node_frames[i]['canvas'].config(bg=color)
            self.node_frames[i]['status'].config(text=f"Status: {status}")
            self.node_frames[i]['token'].config(text=f"Token: {token}")
            self.node_frames[i]['queue'].config(text=f"Fila: {queue_size} mensagens")
            last_display = last_trans if last_trans else "N/A"
            self.node_frames[i]['stats'].config(text=f"Transmissões: {transmissions} | Última: {last_display}")
            
            total_transmissions += transmissions
            if status == "OPERACIONAL":
                active_nodes += 1
        
        status_text = "Executando" if self.simulator.is_running else "Parado"
        self.stats_label.config(text=f"Total de Transmissões: {total_transmissions} | Nós Ativos: {active_nodes}/4 | Status: {status_text}")
        
        self.status_indicator.config(bg='green' if self.simulator.is_running else 'red')

    def start_simulation(self):
        self.simulator.start_simulation()
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)

    def stop_simulation(self):
        self.simulator.stop_simulation()
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.update_display()

    def reset_ring(self):
        self.simulator.stop_simulation()
        time.sleep(0.5)
        self.simulator = TokenRingSimulator(4)
        self.simulator.update_display = self.update_display
        self.simulator.log_text = self.log_text
        self.update_display()
        self.simulator.log_event("=== ANEL REINICIADO ===")
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)

    def clear_log(self):
        self.log_text.delete(1.0, tk.END)

    def update_delay(self):
        self.simulator.transmission_delay = self.delay_var.get()

    def toggle_node_failure(self, node_id):
        self.simulator.toggle_node_failure(node_id)

    def send_message_dialog(self, node_id):
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Enviar Mensagem para Node {node_id}")
        dialog.geometry("300x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text=f"Mensagem para Node {node_id}:").pack(pady=10)
        
        message_var = tk.StringVar()
        message_entry = ttk.Entry(dialog, textvariable=message_var, width=30)
        message_entry.pack(pady=5)
        message_entry.focus()
        
        def send_and_close():
            message = message_var.get().strip()
            if message:
                self.simulator.add_message_to_node(node_id, message)
            dialog.destroy()
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Enviar", command=send_and_close).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        message_entry.bind('<Return>', lambda e: send_and_close())

    def send_random_message(self):
        node_id = random.randint(0, 3)
        messages = [
            "Mensagem de teste",
            "Hello World!",
            "Transmissão de dados",
            "Token Ring funcionando",
            "Simulação FDDI",
            "Mensagem aleatória",
            "Teste de rede",
            "Comunicação em anel"
        ]
        message = f"{random.choice(messages)} #{random.randint(100, 999)}"
        self.simulator.add_message_to_node(node_id, message)

    def broadcast_message(self):
        message = f"BROADCAST {datetime.now().strftime('%H:%M:%S')}"
        for i in range(4):
            self.simulator.add_message_to_node(i, message)

    def stress_test(self):
        for i in range(10):
            node_id = random.randint(0, 3)
            message = f"Teste estresse #{i+1}"
            self.simulator.add_message_to_node(node_id, message)

    def show_messages(self, node_id):
        node = self.simulator.nodes[node_id]
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Mensagens do Node {node_id}")
        dialog.geometry("400x300")
        
        ttk.Label(dialog, text=f"Mensagens recebidas/transmitidas pelo Node {node_id}:").pack(pady=10)
        
        text_widget = scrolledtext.ScrolledText(dialog, width=50, height=15)
        text_widget.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        for msg in node.received_messages[-20:]:
            text_widget.insert(tk.END, f"{msg}\n")
        
        text_widget.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    app = TokenRingGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()