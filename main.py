import cv2
import mediapipe as mp
import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread
from datetime import datetime

# --- Variáveis globais e temas ---
running = False
log_file = "logs_darkalert.txt"
themes = {
    'Light': {
        'alert_bg': (0, 0, 255),
        'zone_color': (0, 255, 0),
        'env_dark_bg': (0, 255, 255),
        'env_dark_fg': (0, 0, 0),
        'env_light_bg': (0, 200, 80),
        'env_light_fg': (255, 255, 255)
    },
    'Dark': {
        'alert_bg': (0, 0, 200),
        'zone_color': (255, 255, 255),
        'env_dark_bg': (0, 255, 255),
        'env_dark_fg': (0, 0, 0),
        'env_light_bg': (0, 128, 0),
        'env_light_fg': (255, 255, 255)
    },
    'HighContrast': {
        'alert_bg': (255, 255, 0),
        'zone_color': (255, 0, 255),
        'env_dark_bg': (255, 0, 0),
        'env_dark_fg': (0, 0, 0),
        'env_light_bg': (0, 0, 255),
        'env_light_fg': (255, 255, 255)
    }
}
current_theme = 'Dark'

# --- MediaPipe setup ---
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

# --- Funções de detecção e utilitários ---
def log_event(event):
    with open(log_file, "a") as f:
        f.write(f"{datetime.now()}: {event}\n")

def verificar_iluminacao(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return gray.mean() < 50

def detectar_mao_aberta(lm):
    dedos = [(8,6), (12,10), (16,14), (20,18)]
    return all(lm[tip].y < lm[pip].y for tip,pip in dedos)

def detectar_punho_fechado(lm):
    dedos = [(8,6), (12,10), (16,14), (20,18)]
    return all(lm[tip].y > lm[pip].y for tip,pip in dedos)

def detectar_sinal_v(lm):
    # Reaproveita lógica de polegar para cima como sinal V
    return (lm[4].y < lm[3].y) and (lm[4].y < lm[2].y)

def center_of_hand(lm, width, height):
    x_mean = sum(p.x for p in lm) / len(lm)
    y_mean = sum(p.y for p in lm) / len(lm)
    return int(x_mean * width), int(y_mean * height)

def draw_text(frame, text, pos, font_scale=1.0, thickness=2, padding=8, text_color=(255,255,255), bg_color=(0,0,255)):
    font = cv2.FONT_HERSHEY_DUPLEX
    (w,h), baseline = cv2.getTextSize(text, font, font_scale, thickness)
    x,y = pos
    cv2.rectangle(frame, (x, y), (x + w + 2*padding, y + h + 2*padding), bg_color, -1)
    cv2.putText(frame, text, (x + padding, y + h + padding - baseline//2), font, font_scale, text_color, thickness)

def detectar():
    global running, current_theme
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Erro", "Nao foi possivel acessar a camera.")
        running = False
        return

    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    x1, y1 = int(width*0.2), int(height*0.2)
    x2, y2 = int(width*0.8), int(height*0.8)
    cont = {'open':0, 'closed':0, 'v_sign':0}
    limiar = 3

    while running:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)
        rgb   = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        escuro = verificar_iluminacao(frame)

        cv2.rectangle(frame, (x1,y1), (x2,y2), themes[current_theme]['zone_color'], 2)
        results = hands.process(rgb)
        alerta = ""

        if escuro and results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                lm = hand_landmarks.landmark
                cx, cy = center_of_hand(lm, width, height)
                if x1<cx<x2 and y1<cy<y2:
                    cont['open']   = cont['open']+1   if detectar_mao_aberta(lm) else 0
                    cont['closed'] = cont['closed']+1 if detectar_punho_fechado(lm) else 0
                    cont['v_sign'] = cont['v_sign']+1 if detectar_sinal_v(lm) else 0
                    if cont['open']   >= limiar:
                        alerta = "Socorro (mao aberta)"
                    elif cont['closed']>= limiar:
                        alerta = "Emergencia medica (punho fechado)"
                    elif cont['v_sign']>= limiar:
                        alerta = "Ajuda leve (sinal V)"

        if alerta:
            draw_text(frame, f"ALERTA: {alerta}", (30,30), font_scale=0.9,
                      thickness=2, padding=8, text_color=(255,255,255),
                      bg_color=themes[current_theme]['alert_bg'])
            log_event(alerta)

        if escuro:
            draw_text(frame, "AMBIENTE SEM LUZ", (30, height-60), font_scale=0.7,
                      thickness=1, padding=6, text_color=themes[current_theme]['env_dark_fg'],
                      bg_color=themes[current_theme]['env_dark_bg'])
        else:
            draw_text(frame, "AMBIENTE COM LUZ", (30, height-60), font_scale=0.7,
                      thickness=1, padding=6, text_color=themes[current_theme]['env_light_fg'],
                      bg_color=themes[current_theme]['env_light_bg'])

        cv2.imshow("DarkAlert - Monitoramento", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            running = False
            break

    cap.release()
    cv2.destroyAllWindows()

# --- Funções ligando UI e detecção ---
def iniciar_monitoramento():
    global running
    if not running:
        running = True
        Thread(target=detectar, daemon=True).start()


def parar_monitoramento():
    global running
    running = False


def exibir_logs():
    log_win = tk.Toplevel(root)
    log_win.title("Logs de Alerta")
    log_win.configure(bg="#2E2E2E")
    log_win.geometry("600x400")
    txt = tk.Text(log_win, wrap='none', bg='#1E1E1E', fg='#FFFFFF', font=('Consolas',10))
    yscroll = ttk.Scrollbar(log_win, orient='vertical', command=txt.yview)
    xscroll = ttk.Scrollbar(log_win, orient='horizontal', command=txt.xview)
    txt.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)
    log_win.grid_rowconfigure(0, weight=1)
    log_win.grid_columnconfigure(0, weight=1)
    txt.grid(row=0, column=0, sticky='nsew')
    yscroll.grid(row=0, column=1, sticky='ns')
    xscroll.grid(row=1, column=0, sticky='ew')
    try:
        with open(log_file, "r") as f:
            for line in f:
                txt.insert('end', line)
    except FileNotFoundError:
        txt.insert('end', "Arquivo de log nao encontrado.")
    txt.config(state='disabled')
    log_win.transient(root)
    log_win.lift()
    log_win.focus_force()


def set_theme(event):
    global current_theme
    current_theme = theme_var.get()

# --- Interface integrada ---
root = tk.Tk()
root.title("DarkAlert - Painel de Controle")
root.geometry("400x350")
root.configure(bg="#2E2E2E")

style = ttk.Style(root)
style.theme_use('clam')
style.configure('TFrame', background='#2E2E2E')
style.configure('Header.TLabel', font=('Helvetica',16,'bold'), foreground='#FFFFFF', background='#2E2E2E')
style.configure('TButton', font=('Helvetica',12), padding=6)
style.map('TButton',
          foreground=[('active','#FFFFFF')],
          background=[('active','#0052CC'),('!disabled','#007ACC')])
style.configure('TLabel', font=('Helvetica',12), foreground='#DDDDDD', background='#2E2E2E')
style.configure('TCombobox', font=('Helvetica',12), fieldbackground='#FFFFFF', background='#FFFFFF')

frame = ttk.Frame(root, padding=(20,20))
frame.pack(fill='both', expand=True)

ttk.Label(frame, text="DarkAlert", style='Header.TLabel').pack(pady=(0,20))
ttk.Label(frame, text="Selecione o tema:").pack(anchor='w')
theme_var = tk.StringVar(value=current_theme)
theme_combo = ttk.Combobox(frame, values=list(themes.keys()), textvariable=theme_var, state='readonly')
theme_combo.pack(fill='x', pady=(0,15))
theme_combo.bind('<<ComboboxSelected>>', set_theme)

ttk.Button(frame, text="Iniciar Monitoramento", command=iniciar_monitoramento).pack(fill='x', pady=5)
ttk.Button(frame, text="Parar Monitoramento",   command=parar_monitoramento).pack(fill='x', pady=5)
ttk.Button(frame, text="Exibir Logs",           command=exibir_logs).pack(fill='x', pady=5)
ttk.Button(frame, text="Fechar",                command=root.destroy).pack(fill='x', pady=(20,0))

root.mainloop()