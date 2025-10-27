# 🔄 Simulador Token Ring - FDDI

<h3 align="center">
Disciplina: Projetos Infraestrutura de Comunicação
Tema: FDDI (Conceito de Token Ring e Falha)
</h3>

---

## 👥 Integrantes do Grupo

- Felipe Cisneiros

- Julio Bezerra

- Rafael Farias

- Ramom Aguiar

- Victor Simas

---

## 📋 Sobre o Projeto

- Simulador em Python que modela o conceito de Token Ring utilizado no padrão FDDI (Fiber Distributed Data Interface), demonstrando a passagem de token entre nós e o mecanismo de transmissão de dados em uma rede em anel..  

---

## 🚀 Funcionalidades

- ✅ Simulação de rede Token Ring com 4-5 nós
- ✅ Mecanismo de passagem de token entre nós
- ✅ Transmissão de mensagens apenas pelo nó detentor do token 
- ✅ Interface de linha de comando para monitoramento
- ✅ Simulação de latência entre nós
- ✅ Sistema de filas de mensagens

---

## 💾 Banco de Dados

O projeto utiliza **PostgreSQL** como banco de dados principal, devido à sua robustez, integridade relacional e compatibilidade com ferramentas modernas.

> 💡 O acesso e manipulação dos dados é feito utilizando **Prisma ORM**, facilitando a comunicação entre o banco e a aplicação Node.js.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:**
  Python 
- **Bibliotecas Utilizadas:**
   import time -> Controle de tempo e latência
   import threading -> Simulação concorrente dos nós
   import Queue -> Gerenciamento de filas de mensagens
   import List, Optional -> Tipagem estática
  
---

## 🏗 Estrutura do Código

**Classes Principais**
🎯 Node
Representa cada nó na rede Token Ring

**Atributos:**

node_id: Identificador único do nó
name: Nome descritivo do nó
has_token: Estado do token (True/False)
message_queue: Fila de mensagens do nó
next_node: Próximo nó no anel
is_active: Status de atividade do nó

**Métodos Principais:**

receive_token(token_data): Processa recebimento do token
process_messages(): Processa mensagens na fila
pass_token(token_data): Passa token para próximo nó
send_message(message): Adiciona mensagem à fila

🌐 TokenRingNetwork
Classe principal que gerencia toda a rede.

**Atributos:**

nodes: Lista de nós na rede
token: Dicionário com informações do token
is_running: Estado da simulação
thread: Thread de execução da simulação

**Métodos Principais:**

initialize_network(): Configura nós e conexões
start_network(): Inicia simulação
stop_network(): Para simulação
display_network_status(): Mostra status da rede
send_message_to_node(node_id, message): Envia mensagem para nó específico

---

## 📥 Instalação e Execução

### 🧩 Pré-requisitos

- **Python 3.8 ou superior instalado** 

### Como executar:

1. **Clone o repositório:** 
   git clone [url-do-repositorio]

   
2. **Execute o simulador:**
python token_ring_simulator.py

---

## 📄 Documentação

**📎 Anexos Disponíveis:**
 1. [📄 Documentação Completa - Entrega 01](https://drive.google.com/drive/folders/0AKCl1NEUBTalUk9PVA)
 
---

## 📜 Licença
Este projeto é desenvolvido para fins educacionais na disciplina de Projetos Infraestrutura de Comunicação.

