# DarkAlert

## 1. Descrição do Problema

A falta de energia elétrica é um desafio recorrente em diversas regiões do Brasil, resultante de eventos climáticos extremos (tempestades, alagamentos) ou falhas de rede. Em apagões, a ausência de iluminação e a instabilidade das redes de comunicação (internet e telefonia) impedem que pessoas em situação de emergência sinalizem pedidos de socorro, agravando riscos de acidentes, problemas de saúde e atrasos no atendimento.

## 2. Visão Geral da Solução

O **DarkAlert** é uma aplicação em Python que utiliza **MediaPipe** e **OpenCV** para permitir a emissão de alertas visuais em ambientes sem luz, por meio de gestos manuais. Sem necessidade de hardware extra, funciona em câmeras convencionais.

### 2.1 Fluxo de Trabalho

1. **Início do Monitoramento**

   * Interface gráfica em **Tkinter** inicia a captura de vídeo.
2. **Detecção de Baixa Luminosidade**

   * Cálculo do brilho médio do frame; ativa o modo de reconhecimento ao ficar abaixo de um limiar.
3. **Zona Ativa**

   * Desenha um retângulo central para orientar o posicionamento da mão.
     ![Figura 1: Zona ativa de captura](assets/zone_active.png)
4. **Reconhecimento de Gestos** (exige manter o gesto em 3 quadros consecutivos):

   * **Mão Aberta** → "Socorro (mao aberta)"
   * **Punho Fechado** → "Emergencia medica (punho fechado)"
   * **Sinal V** (polegar estendido) → "Ajuda leve (sinal V)"
     ![Figura 2: Exemplos de gestos reconhecidos](assets/gestures.png)
5. **Exibição de Alerta**

   * Sobreposição de texto colorido no vídeo indicando o tipo de emergência.
     ![Figura 3: Alerta visual na tela](assets/alert_display.png)
6. **Registro em Log**

   * Grava timestamp e nome do alerta em `logs_darkalert.txt`.

## 3. Instruções de Instalação e Uso

### 3.1 Pré-requisitos

* Python 3.7 ou superior
* Dependências:

  ```bash
  pip install mediapipe opencv-python
  ```
* Pasta `assets/` contendo as imagens ilustrativas (opcional)

### 3.2 Passos

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/DarkAlert.git
   cd DarkAlert
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Execute a aplicação:

   ```bash
   python darkalert.py
   ```

4. Na janela de controle, selecione o tema e clique em **Iniciar Monitoramento**.

5. Posicione a mão dentro da zona ativa em ambiente escuro e faça os gestos definidos.

6. Para parar, use o botão **Parar Monitoramento** ou pressione `ESC` na janela de vídeo.

7. Para visualizar histórico de alertas, clique em **Exibir Logs**.

#4. Link do video

 ```bash
   https://youtu.be/n4r5vxyanfo
   ```

#5 Integrantes do grupo

* Márcio Gastaldi - RM98811
* Arthur Bessa Pian - RM99215
* Davi Desenzi - RM550849
