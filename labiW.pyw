import tkinter as tk
import tempfile
import os
import threading
import base64
import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wav
from openai import OpenAI
import pygame

# CAPTURA
from PIL import Image, ImageTk
import mss
import mss.tools

# ================= CONFIG =================
API_KEY = ""
FS = 44100

client = OpenAI(api_key=API_KEY)

# ===== MEMORIA CONTEXTUAL =====
memoria_preguntas = []

def agregar_a_memoria(texto, tipo="texto"):
    if tipo == "vision":
        memoria_preguntas.append(f"[Contexto visual]: {texto}")
    else:
        memoria_preguntas.append(texto)

pygame.mixer.init()

# ===== CONTROL DE VOZ =====
voz_activada = True
def borrar_chat():

    global memoria_preguntas, historial

    memoria_preguntas.clear()

    historial.delete("1.0", tk.END)

    if hasattr(historial, "imagenes"):
        historial.imagenes.clear()

    pygame.mixer.music.stop()

    historial.insert(
        tk.END,
        "🧹 Chat y memoria borrados.\n\n"
    )
def alternar_voz():

    global voz_activada

    voz_activada = not voz_activada

    if not voz_activada:
        pygame.mixer.music.stop()
        boton_voz.config(text="🔇")
    else:
        boton_voz.config(text="🔊")

# ================= AUDIO =================
def grabar_audio(duracion=8):

    audio = sd.rec(
        int(duracion * FS),
        samplerate=FS,
        channels=1,
        device=MIC_ID,
        dtype="float32"
    )
    sd.wait()

    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val

    archivo = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    wav.write(archivo.name, FS, audio)

    return archivo.name


def voz_a_texto():

    audio_path = grabar_audio()

    with open(audio_path, "rb") as f:
        transcripcion = client.audio.transcriptions.create(
            file=f,
            model="gpt-4o-transcribe",
            language="es"
        )

    os.remove(audio_path)
    return transcripcion.text.strip()


def texto_a_voz(texto):

    if not voz_activada:
        return

    audio = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=texto
    )

    path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name

    with open(path, "wb") as f:
        f.write(audio.read())

    pygame.mixer.music.load(path)
    pygame.mixer.music.play()

# ================= IA TEXTO =================
def preguntar_ia(texto):

    agregar_a_memoria(texto, "texto")

    contexto = "\n".join([f"- {p}" for p in memoria_preguntas])

    respuesta = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content":
                "Eres Labi, asistente experto en electrónica y microcontroladores.\n"
                "Puedes usar contexto conversacional y descripciones visuales previas.\n\n"
                "Historial:\n" + contexto
            },
            {"role": "user", "content": texto}
        ],
        temperature=0.3,
        max_tokens=300
    )

    return respuesta.choices[0].message.content.strip()

# ================= IA VISIÓN =================
def enviar_imagen_a_ia(path, prompt):

    with open(path, "rb") as img_file:
        b64_image = base64.b64encode(img_file.read()).decode("utf-8")

    respuesta = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content":
                "Eres Labi, asistente experto en electrónica y microcontroladores."
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{b64_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=300
    )

    return respuesta.choices[0].message.content.strip()

# ================= CAPTURA =================
modo_captura_activo = False

def capturar_pantalla():

    with mss.mss() as sct:

        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)

        path = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".png"
        ).name

        mss.tools.to_png(
            screenshot.rgb,
            screenshot.size,
            output=path
        )

    return path

# ================= MOSTRAR + ANALIZAR =================
def mostrar_captura_en_chat(path):

    global chat_window, historial

    if chat_window.state() == "withdrawn":
        chat_window.deiconify()

    historial.insert(tk.END, "📷 Captura enviada:\n")

    img = Image.open(path)
    img.thumbnail((300, 300))
    photo = ImageTk.PhotoImage(img)

    historial.image_create(tk.END, image=photo)
    historial.insert(tk.END, "\n\n")

    if not hasattr(historial, "imagenes"):
        historial.imagenes = []

    historial.imagenes.append(photo)

    historial.insert(tk.END, "💬 Analizando imagen con Labi...\n")
    chat_window.update()

    try:

        respuesta = enviar_imagen_a_ia(
            path,
            "Analiza esta captura y dame información técnica relevante."
        )

        agregar_a_memoria(respuesta, "vision")

        # ❌ NO voz aquí (capturas no hablan)

    except Exception as e:
        historial.insert(tk.END, f"Error: {e}\n")

# ================= ROOT =================
root = tk.Tk()
root.overrideredirect(True)
root.attributes("-topmost", True)
root.config(bg="black")
root.wm_attributes("-transparentcolor", "black")
root.geometry("80x80+100+300")

chat_window = None
historial = None
entrada = None
boton_voz = None

# ================= BOLA =================
canvas = tk.Canvas(
    root,
    width=80,
    height=80,
    bg="black",
    highlightthickness=0
)
canvas.pack()

canvas.create_oval(12, 12, 78, 78, fill="#1e3a8a", outline="")
canvas.create_oval(4, 4, 72, 72, fill="#2563eb", outline="")
canvas.create_oval(16, 10, 38, 30, fill="#60a5fa", outline="")

texto_bola = canvas.create_text(
    40, 42,
    text="Labi",
    fill="white",
    font=("Segoe UI", 14, "bold")
)

# ================= CHAT =================
def toggle_chat(event=None):

    global chat_window, historial, entrada, boton_voz

    if chat_window and chat_window.winfo_exists():

        if chat_window.state() == "withdrawn":
            chat_window.deiconify()
        else:
            chat_window.withdraw()

        return

    chat_window = tk.Toplevel()
    chat_window.title("Labi")
    chat_window.geometry("460x560")
    chat_window.attributes("-topmost", True)
    chat_window.configure(bg="#0f172a")

    historial = tk.Text(
        chat_window,
        wrap=tk.WORD,
        bg="#020617",
        fg="white",
        font=("Segoe UI", 11),
        bd=0
    )
    historial.pack(expand=True, fill="both", padx=10, pady=10)

    entrada = tk.Entry(
        chat_window,
        bg="#020617",
        fg="white",
        font=("Segoe UI", 11),
        bd=0
    )
    entrada.pack(fill="x", padx=10, pady=5)

    # ===== FUNCIONES =====
    def enviar_texto():

        texto = entrada.get()
        if not texto:
            return

        entrada.delete(0, tk.END)

        historial.insert(tk.END, f"Tú: {texto}\n")

        respuesta = preguntar_ia(texto)

        historial.insert(tk.END, f"Labi: {respuesta}\n\n")

        threading.Thread(
            target=texto_a_voz,
            args=(respuesta,)
        ).start()

    def activar_captura():

        global modo_captura_activo

        chat_window.withdraw()
        modo_captura_activo = True

        canvas.itemconfig(texto_bola, text="📷")

    # ===== BOTONES =====
    frame = tk.Frame(chat_window, bg="#0f172a")
    frame.pack(fill="x")

    tk.Button(frame, text="Enviar", command=enviar_texto).pack(side="left")
    tk.Button(frame, text="📷", command=activar_captura).pack(side="left")

    boton_voz = tk.Button(
        frame,
        text="🔊",
        command=alternar_voz
    )
    boton_voz.pack(side="right")
    tk.Button(
        frame,
        text="🗑️",
        command=borrar_chat
    ).pack(side="right")

    entrada.bind("<Return>", lambda e: enviar_texto())

# ================= ACCIÓN BOLA =================
def accion_bola(event=None):

    global modo_captura_activo

    if modo_captura_activo:

        path = capturar_pantalla()

        modo_captura_activo = False
        canvas.itemconfig(texto_bola, text="Labi")

        mostrar_captura_en_chat(path)
        return

    toggle_chat()

canvas.bind("<Button-1>", accion_bola)

# ================= DRAG =================
def mover(event):
    root.geometry(f"+{event.x_root-40}+{event.y_root-40}")

canvas.bind("<B1-Motion>", mover)

# ================= RUN =================
root.mainloop()
