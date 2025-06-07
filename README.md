# DarkAlert

## 1. Descrição do Problema 🔍

Em muitas regiões do Brasil, apagões e falhas de energia causados por tempestades, enchentes ou problemas na rede elétrica deixam pessoas totalmente sem luz e sem acesso a canais de comunicação convencionais (internet, telefone). Nesses cenários:

* 🚨 **Risco de acidentes:** ambientes escuros aumentam colisões, quedas e até incêndios.
* 🆘 **Dificuldade de socorro:** hospitais, asilos ou pessoas isoladas não conseguem sinalizar emergências.
* ⏳ **Atraso na resposta:** equipes de resgate podem demorar para chegar por falta de sinalização clara.

Sem um sistema de alerta alternativo, a falta de visibilidade e comunicação agrava ainda mais as consequências de uma queda de energia.

## 2. Visão Geral da Solução 💡

O **DarkAlert** é uma aplicação leve em **Python** que combina **OpenCV** e **MediaPipe** para reconhecer gestos manuais em ambientes escuros, sem depender de hardware adicional. Basta uma câmera comum ou webcam.

### 2.1 Fluxo de Trabalho 🔄

1. 🖥️ **Início do Monitoramento**

   * A interface em **Tkinter** abre um painel de controle e inicia a captura de vídeo.

2. 🌙 **Detecção de Baixa Luminosidade**

   * Calcula o brilho médio de cada frame; quando abaixo de um limiar configurado, entra no modo de reconhecimento.

3. 📏 **Zona Ativa**

   * Desenha um retângulo guia na tela, indicando onde posicionar a mão para melhor precisão.

4. 🤚 **Reconhecimento de Gestos** (confirmação em 3 frames consecutivos):

   * ✋ **Mão Aberta** → alerta: **“Socorro”**
   * ✊ **Punho Fechado** → alerta: **“Emergência médica”**
   * 👍 **Sinal V** (polegar estendido) → alerta: **“Ajuda leve”**

5. ⚠️ **Exibição de Alerta**

   * Exibe mensagem colorida sobre o vídeo indicando o tipo de emergência.

6. 📝 **Registro em Log**

   * Grava data, hora e descrição do alerta em `logs_darkalert.txt` para análise posterior.

## 3. Instruções de Instalação e Uso 🚀

### 3.1 Pré-requisitos

* **Python 3.7+**
* Pacotes Python:

  ```bash
  pip install mediapipe opencv-python
  ```

### 3.2 Passos de Instalação

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/seu-usuario/DarkAlert.git
   cd DarkAlert
   ```

2. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Execute a aplicação:**

   ```bash
   python darkalert.py
   ```

4. **Uso:**

   * Selecione o tema e clique em **Iniciar Monitoramento** no painel.
   * Posicione a mão dentro da zona ativa em ambiente escuro e realize o gesto desejado.
   * Para parar, clique em **Parar Monitoramento** ou pressione `ESC` na janela de vídeo.
   * Para visualizar o histórico de alertas, clique em **Exibir Logs**.

## 4. Link do Vídeo 🎥

Assista à demonstração completa:

```bash
https://youtu.be/n4r5vxyanfo
```

## 5. Integrantes do Grupo 👥

* Márcio Gastaldi - RM98811
* Arthur Bessa Pian - RM99215
* Davi Desenzi - RM550849
