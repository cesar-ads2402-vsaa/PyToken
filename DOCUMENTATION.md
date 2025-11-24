# Simulador FDDI Token Ring

Este documento descreve a estrutura, funcionamento e componentes principais do **Simulador FDDI Token Ring**, implementado em Python com interface gráfica utilizando **Tkinter**.

---

## 📌 Objetivo do Projeto
O projeto simula o funcionamento de uma rede **Token Ring**, incluindo:
- Circulação do token entre os nós.
- Transmissão de mensagens quando um nó possui o token.
- Falha e recuperação de nós.
- Visualização em tempo real do estado de cada nó.
- Log detalhado dos eventos da simulação.

O simulador também inclui:
- Interface gráfica completa.
- Contadores de transmissões.
- Sistema de filas de mensagens por nó.
- Painel de estatísticas.

---

## 🏛 Arquitetura Geral
O código é dividido em três componentes principais:

### **1. TokenRingNode**
Representa um nó do anel. Suas responsabilidades incluem:
- Armazenar estado (token, fila, falha, contador de transmissões).
- Receber o token.
- Transmitir mensagens.
- Passar o token ao próximo nó.
- Entrar em falha e se recuperar.

### **2. TokenRingSimulator**
Gerencia o anel completo:
- Inicializa o conjunto de nós.
- Controla o loop da simulação em uma thread.
- Registra logs.
- Atualiza a interface.
- Ajusta o atraso entre transmissões.

### **3. TokenRingGUI**
Implementa toda a interface gráfica:
- Botões de controle (iniciar, parar, resetar).
- Status visual dos nós (cores, mensagens, contador, etc.).
- Janela de mensagens por nó.
- Log de eventos.
- Estatísticas gerais.

---

## 🔄 Funcionamento da Simulação
1. O token sempre circula no sentido horário.
2. Apenas um nó pode transmitir por vez (posse do token).
3. Cada nó pode:
   - Adicionar mensagens à sua fila.
   - Falhar e ser ignorado pelo token.
4. A simulação ocorre em *thread* separada.
5. O sistema para imediatamente quando solicitado.

---

## 🎛 Interface Gráfica
A GUI exibe:
- Painel de controle geral.
- Status de cada nó:
  - Cor (falho, operante, com token).
  - Estado do token.
  - Fila de mensagens.
  - Última transmissão.
- Botões individuais por nó:
  - Falhar/Recuperar.
  - Enviar mensagem.
  - Ver mensagens recentes.
- Log em tempo real.
- Estatísticas globais.

---

## 📂 Estrutura do Código
- **TokenRingNode**
  - `receive_token()`
  - `pass_token()`
  - `transmit()`
  - `add_message()`
  - `toggle_failure()`

- **TokenRingSimulator**
  - `create_ring()`
  - `start_simulation()`
  - `stop_simulation()`
  - `add_message_to_node()`
  - `toggle_node_failure()`
  - `log_event()`
  - `update_gui()`

- **TokenRingGUI**
  - `setup_gui()`
  - `update_display()`
  - `send_message_dialog()`
  - `broadcast_message()`
  - `stress_test()`

---

## ▶️ Como Executar
1. Instale Python 3.
2. Execute o arquivo principal:
```
python entrega04.py
```
3. A interface abrirá automaticamente.

---

## 📡 Recursos Adicionais
- Teste de estresse com envio rápido de mensagens.
- Envio de mensagens aleatórias.
- Broadcast para todos os nós.
- Visualização histórica de mensagens por nó.

---

## 📄 Licença
Este projeto pode utilizar qualquer licença desejada (MIT recomendado). Inclua um arquivo `LICENSE` no repositório.

---

## 📝 Autor
Documentação gerada automaticamente para fins de organização no GitHub.

