# 🔄 Simulador Token Ring - FDDI

### Disciplina: Projetos Infraestrutura de Comunicação  
### Tema: FDDI (Conceito de Token Ring e Falha)

---

## 👥 Integrantes do Grupo

- **Felipe Cisneiros**
- **Julio Bezerra**
- **Rafael Farias**
- **Ramom Aguiar**
- **Victor Simas**

---

## 📋 Sobre o Projeto

Este projeto implementa um **simulador completo do protocolo Token Ring** baseado no padrão **FDDI (Fiber Distributed Data Interface)**.

A aplicação demonstra:

- A circulação contínua do token em um anel lógico  
- Envio e recebimento de mensagens entre nós  
- Detecção, simulação e recuperação de falhas  
- Visualização gráfica em tempo real  
- Filas de mensagens e controle de acesso ao meio  

É uma ferramenta educacional desenvolvida para **facilitar o entendimento de redes em anel** e de como elas se comportam diante de falhas.

---

## 🚀 Funcionalidades

- ✅ Simulação completa de uma rede Token Ring  
- ✅ Interface gráfica desenvolvida com Tkinter  
- ✅ Visualização do estado de cada nó  
- ✅ Passagem do token em ciclo contínuo  
- ✅ Transmissão restrita ao nó portador do token  
- ✅ Filas individuais de mensagens por nó  
- ✅ Sistema de logs atualizado em tempo real  
- ✅ Ajuste de latência entre transmissões  
- ✅ Envio de mensagens para um nó específico  
- ✅ Broadcast para todos os nós do anel  
- ✅ Teste de estresse (múltiplas mensagens automáticas)  
- ✅ Simulação de falha e recuperação de nós  
- ✅ Execução em thread separada para operações em tempo real  

---

## 🧪 Possibilidades Pedagógicas

- Demonstração prática do funcionamento do FDDI  
- Visualização clara de falhas e resiliência da rede  
- Entendimento de gerenciamento de token  
- Análise do impacto de latência na comunicação  
- Modelagem de anéis lógicos e topologia física  

---

## 🛠️ Tecnologias Utilizadas

### **Linguagem**
- Python 3.8+

### **Bibliotecas**
- `tkinter` → Interface gráfica  
- `threading` → Execução paralela da simulação  
- `time` → Controle de latência  
- `datetime` → Marcação temporal  
- `random` → Geração de valores aleatórios  

---

## 🏗 Estrutura do Código

### 🎯 Classe: **Node**
Representa cada nó da rede Token Ring.

#### **Atributos Principais**
- `node_id` — Identificador do nó  
- `has_token` — Indica se o nó possui o token  
- `next_node` — Próximo nó no anel lógico  
- `message_queue` — Fila de mensagens pendentes  
- `received_messages` — Histórico de mensagens recebidas  
- `transmission_count` — Total de mensagens transmitidas  
- `is_failed` — Estado de falha do nó  

#### **Métodos Principais**
- `receive_token(simulator)` — Processa a chegada do token  
- `pass_token(simulator)` — Passa o token ao próximo nó  
- `transmit(simulator)` — Transmite mensagens da fila  
- `add_message(message)` — Adiciona mensagem ao nó  
- `toggle_failure()` — Alterna entre falha e operação  

---

### 🌐 Classe: **TokenRingNetwork**
Gerencia todo o funcionamento da rede.

#### **Atributos Principais**
- `nodes` — Lista de nós da rede  
- `token` — Estrutura com dados do token  
- `is_running` — Estado da simulação  
- `thread` — Thread principal da simulação  

#### **Métodos Principais**
- `initialize_network()` — Configura nós e conexões  
- `start_network()` — Inicia a simulação  
- `stop_network()` — Interrompe a simulação  
- `display_network_status()` — Exibe o estado atual da rede  
- `send_message_to_node(node_id, message)` — Envia mensagem a um nó específico  

---

## 📥 Instalação e Execução

### 🧩 Pré-requisitos
- Python **3.8 ou superior**

### ▶️ Como executar:

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/cesar-ads2402-vsaa/PyToken
   ```
2. **Execute o simulador:**
   ```bash
   python entrega04.py
   ```
### 📄 Documentação
1. [📄 Documentação Completa – Entrega 01](https://docs.google.com/document/d/1OjXsGWlRVC4G7oisoF2WypfzSHeCLp3V9NUsJucnPAM/edit?usp=sharing)

### 📜 Licença
Este projeto foi desenvolvido para fins educacionais na disciplina de Projetos de Infraestrutura de Comunicação e está sujeito à licença anexada neste repositório.