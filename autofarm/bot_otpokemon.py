import pyautogui
import cv2
import numpy as np
import time
import random
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

# Variáveis globais
POKEMON_ALVO = "imagens/pokemon.png"
POKEMON_MORTO = "imagens/pokemon_morto.png"
ITEM_DROPADO = "imagens/item.png"
SKILLS = ["f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8"]
bot_rodando = False

# Função para encontrar imagem na tela
def encontrar_imagem(imagem_alvo, confianca=0.75):
    tela = pyautogui.screenshot()
    tela_np = np.array(tela)
    tela_cv = cv2.cvtColor(tela_np, cv2.COLOR_RGB2BGR)
    imagem = cv2.imread(imagem_alvo)

    if imagem is None:
        log(f"[ERRO] Não encontrei a imagem: {imagem_alvo}")
        return None

    resultado = cv2.matchTemplate(tela_cv, imagem, cv2.TM_CCOEFF_NORMED)
    _, max_valor, _, max_local = cv2.minMaxLoc(resultado)

    if max_valor >= confianca:
        return max_local
    return None

# Função para atacar usando as skills
def atacar_pokemon():
    for skill in SKILLS:
        pyautogui.press(skill)
        time.sleep(0.2)

# Função para clicar com o botão direito em uma imagem
def clicar_imagem(imagem_alvo, descricao, confianca=0.75, offset=(20, 20)):
    pos = encontrar_imagem(imagem_alvo, confianca)
    if pos:
        x, y = pos
        pyautogui.rightClick(x + offset[0], y + offset[1])
        log(f"🖱 {descricao} encontrado e clicado!")
        return True
    return False

# Função principal do bot
def bot_loop():
    global bot_rodando
    log("🤖 Bot iniciado! Procurando Pokémon alvo...")
    time.sleep(3)

    while bot_rodando:
        # Procurar o Pokémon alvo
        pos = encontrar_imagem(POKEMON_ALVO, confianca=0.75)

        if pos:
            x, y = pos
            pyautogui.rightClick(x + 20, y + 20)
            log("🎯 Pokémon encontrado! Atacando...")
            atacar_pokemon()

            # Aguardar 2 segundos antes de verificar o loot
            time.sleep(1)

            # Tentar encontrar o Pokémon morto até 4 vezes
            encontrado = False
            for tentativa in range(8):
                if clicar_imagem(POKEMON_MORTO, "Pokémon derrotado"):
                    encontrado = True
                    time.sleep(1)
                    # Tentar pegar o item dropado
                    if clicar_imagem(ITEM_DROPADO, "Item dropado"):
                        log("💎 Item coletado!")
                    else:
                        log("⚠ Nenhum item dropado encontrado.")
                    break
                else:
                    log(f"⚠ Tentativa {tentativa + 1}/8: Não encontrei o Pokémon derrotado na tela.")
                    time.sleep(1)

            if not encontrado:
                log("❌ Não foi possível encontrar o Pokémon derrotado após 8 tentativas.")

            time.sleep(random.uniform(1.5, 2.5))
            time.sleep(random.uniform(2, 4))
        else:
            log("🔍 Nenhum Pokémon alvo na tela... procurando...")
            time.sleep(1)

    log("⛔ Bot parado!")

# Iniciar o bot em uma thread separada
def iniciar_bot():
    global bot_rodando
    if bot_rodando:
        messagebox.showwarning("Aviso", "O bot já está rodando!")
        return
    bot_rodando = True
    threading.Thread(target=bot_loop, daemon=True).start()

# Parar o bot
def parar_bot():
    global bot_rodando
    bot_rodando = False

# Alterar o Pokémon alvo
def escolher_pokemon():
    global POKEMON_ALVO
    caminho = filedialog.askopenfilename(filetypes=[("Imagens", "*.png *.jpg *.jpeg")])
    if caminho:
        POKEMON_ALVO = caminho
        log(f"✅ Pokémon alvo atualizado: {POKEMON_ALVO}")

# Alterar a imagem do Pokémon morto
def escolher_pokemon_morto():
    global POKEMON_MORTO
    caminho = filedialog.askopenfilename(filetypes=[("Imagens", "*.png *.jpg *.jpeg")])
    if caminho:
        POKEMON_MORTO = caminho
        log(f"💀 Pokémon derrotado atualizado: {POKEMON_MORTO}")

# Alterar a imagem do item dropado
def escolher_item():
    global ITEM_DROPADO
    caminho = filedialog.askopenfilename(filetypes=[("Imagens", "*.png *.jpg *.jpeg")])
    if caminho:
        ITEM_DROPADO = caminho
        log(f"💎 Item dropado atualizado: {ITEM_DROPADO}")

# Alterar as skills
def salvar_skills():
    global SKILLS
    texto = entry_skills.get()
    SKILLS = [s.strip() for s in texto.split(",") if s.strip()]
    log(f"⚡ Skills atualizadas: {', '.join(SKILLS)}")

# Função para exibir logs na interface
def log(msg):
    txt_log.insert(tk.END, msg + "\n")
    txt_log.see(tk.END)

# Criando a interface gráfica
root = tk.Tk()
root.title("Bot OTPokémon")
root.geometry("550x550")
root.resizable(False, False)

# Botões para selecionar imagens
frame_imagens = tk.Frame(root)
frame_imagens.pack(pady=5)
tk.Button(frame_imagens, text="Selecionar Pokémon Alvo", command=escolher_pokemon).grid(row=0, column=0, padx=5)
tk.Button(frame_imagens, text="Selecionar Pokémon Morto", command=escolher_pokemon_morto).grid(row=0, column=1, padx=5)
tk.Button(frame_imagens, text="Selecionar Item Dropado", command=escolher_item).grid(row=0, column=2, padx=5)

# Entrada para configurar as skills
frame_skills = tk.Frame(root)
frame_skills.pack(pady=5)
tk.Label(frame_skills, text="Skills (separadas por vírgula):").pack()
entry_skills = tk.Entry(frame_skills, width=60)
entry_skills.insert(0, ",".join(SKILLS))
entry_skills.pack()
btn_skills = tk.Button(frame_skills, text="Salvar Skills", command=salvar_skills)
btn_skills.pack(pady=5)

# Botões de controle
frame_controle = tk.Frame(root)
frame_controle.pack(pady=10)
btn_iniciar = tk.Button(frame_controle, text="▶ Iniciar Bot", bg="green", fg="white", width=18, command=iniciar_bot)
btn_iniciar.grid(row=0, column=0, padx=5)
btn_parar = tk.Button(frame_controle, text="⏹ Parar Bot", bg="red", fg="white", width=18, command=parar_bot)
btn_parar.grid(row=0, column=1, padx=5)

# Caixa de logs
txt_log = scrolledtext.ScrolledText(root, width=65, height=18)
txt_log.pack(pady=10)

# Inicia a interface
root.mainloop()
