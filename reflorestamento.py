import tkinter as tk
import time

# JOGO: REFLORESTAMENTO
# Controles:
# Jogador 1: WASD para andar, E para plantar, Q para cuidar.
# Jogador 2: Setas para andar, Enter para plantar, Shift direito para cuidar.

LARGURA = 900
ALTURA = 620
COLUNAS = 10
LINHAS = 6
TAMANHO = 72
TEMPO_TOTAL = 120

class JogoFloresta:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Reflorestamento")
        self.raiz.resizable(False, False)
        self.canvas = tk.Canvas(raiz, width=LARGURA, height=ALTURA,
                                bg="#e8f5e9", highlightthickness=0)
        self.canvas.pack()
        self.raiz.bind("<KeyPress>", self.tecla)
        self.iniciar()

    def iniciar(self):
        self.tempo_inicio = time.time()
        self.terminou = False
        self.jogadores = [
            {"nome": "JOGADOR 1", "x": 1, "y": 2, "sementes": 5,
             "plantadas": 0, "cor": "#1976d2", "lado": (0, 4)},
            {"nome": "JOGADOR 2", "x": 8, "y": 2, "sementes": 5,
             "plantadas": 0, "cor": "#e65100", "lado": (5, 9)}
        ]
        self.plantas = {}
        self.desenhar()
        self.atualizar_tempo()

    def dentro_do_lado(self, jogador, x):
        inicio, fim = jogador["lado"]
        return inicio <= x <= fim

    def tecla(self, evento):
        if self.terminou:
            if evento.keysym.lower() == "r":
                self.iniciar()
            return

        k = evento.keysym.lower()
        a, b = self.jogadores

        movimentos = {
            "w": (a, 0, -1), "s": (a, 0, 1),
            "a": (a, -1, 0), "d": (a, 1, 0),
            "up": (b, 0, -1), "down": (b, 0, 1),
            "left": (b, -1, 0), "right": (b, 1, 0)
        }

        if k in movimentos:
            jogador, dx, dy = movimentos[k]
            nx, ny = jogador["x"] + dx, jogador["y"] + dy
            if 0 <= ny < LINHAS and self.dentro_do_lado(jogador, nx):
                jogador["x"], jogador["y"] = nx, ny
        elif k == "e":
            self.plantar(a)
        elif k == "q":
            self.cuidar(a)
        elif k in ("return", "kp_enter"):
            self.plantar(b)
        elif k in ("shift_r", "shift_l"):
            self.cuidar(b)

        self.desenhar()

    def plantar(self, jogador):
        pos = (jogador["x"], jogador["y"])
        if jogador["sementes"] > 0 and pos not in self.plantas:
            self.plantas[pos] = 0
            jogador["sementes"] -= 1
            jogador["plantadas"] += 1

    def cuidar(self, jogador):
        pos = (jogador["x"], jogador["y"])
        if pos not in self.plantas:
            return
        nivel = self.plantas[pos] + 1
        if nivel >= 3:
            jogador["sementes"] += 2
            self.plantas[pos] = 0
        else:
            self.plantas[pos] = nivel

    def desenhar(self):
        self.canvas.delete("all")
        self.canvas.create_text(225, 28, text="JOGADOR 1  |  WASD • E plantar • Q cuidar",
                                fill="#174a7e", font=("Arial", 12, "bold"))
        self.canvas.create_text(675, 28, text="JOGADOR 2  |  SETAS • ENTER plantar • SHIFT cuidar",
                                fill="#a33b00", font=("Arial", 12, "bold"))
        self.canvas.create_line(450, 55, 450, 500, fill="#78909c", width=3, dash=(7, 5))

        for y in range(LINHAS):
            for x in range(COLUNAS):
                px, py = 90 + x * TAMANHO, 75 + y * TAMANHO
                cor = "#dcedc8" if x < 5 else "#fff3e0"
                self.canvas.create_rectangle(px, py, px + TAMANHO - 3,
                                             py + TAMANHO - 3,
                                             fill=cor, outline="#a5b99a", width=1)
                if (x, y) in self.plantas:
                    nivel = self.plantas[(x, y)]
                    tamanhos = [12, 17, 23]
                    r = tamanhos[nivel]
                    cx, cy = px + 34, py + 34
                    self.canvas.create_rectangle(cx - 3, cy + 7, cx + 3, cy + 23,
                                                 fill="#795548", outline="")
                    self.canvas.create_oval(cx-r, cy-r, cx+r, cy+r,
                                            fill=["#81c784", "#43a047", "#1b5e20"][nivel],
                                            outline="#2e7d32", width=2)
                    self.canvas.create_text(cx, py + 62, text="+" if nivel == 2 else "•",
                                            fill="#1b5e20", font=("Arial", 10, "bold"))

        for j in self.jogadores:
            cx = 90 + j["x"] * TAMANHO + 34
            cy = 75 + j["y"] * TAMANHO + 34
            self.canvas.create_oval(cx-13, cy-13, cx+13, cy+13,
                                    fill=j["cor"], outline="white", width=3)
            self.canvas.create_text(cx, cy, text="1" if j is self.jogadores[0] else "2",
                                    fill="white", font=("Arial", 11, "bold"))

        restante = max(0, TEMPO_TOTAL - int(time.time() - self.tempo_inicio))
        self.canvas.create_text(450, 535, text=f"⏱  TEMPO: {restante // 60:02d}:{restante % 60:02d}",
                                fill="#263238", font=("Arial", 20, "bold"))
        for i, j in enumerate(self.jogadores):
            x = 225 if i == 0 else 675
            self.canvas.create_text(x, 575,
                text=f"🌱 Sementes: {j['sementes']}     🌳 Árvores plantadas: {j['plantadas']}",
                fill=j["cor"], font=("Arial", 13, "bold"))

        if restante <= 0:
            self.finalizar()

    def atualizar_tempo(self):
        if not self.terminou:
            self.desenhar()
            self.raiz.after(250, self.atualizar_tempo)

    def finalizar(self):
        self.terminou = True
        p1, p2 = self.jogadores
        if p1["plantadas"] > p2["plantadas"]:
            resultado = "JOGADOR 1 VENCEU!"
        elif p2["plantadas"] > p1["plantadas"]:
            resultado = "JOGADOR 2 VENCEU!"
        else:
            resultado = "EMPATE!"
        self.canvas.create_rectangle(170, 205, 730, 405,
                                     fill="#ffffff", outline="#2e7d32", width=4)
        self.canvas.create_text(450, 250, text="FIM DE JOGO",
                                font=("Arial", 25, "bold"), fill="#1b5e20")
        self.canvas.create_text(450, 300, text=resultado,
                                font=("Arial", 23, "bold"), fill="#263238")
        self.canvas.create_text(450, 345,
            text=f"Jogador 1: {p1['plantadas']} plantas   |   Jogador 2: {p2['plantadas']} plantas",
            font=("Arial", 13), fill="#37474f")
        self.canvas.create_text(450, 380, text="Pressione R para jogar novamente",
                                font=("Arial", 12, "bold"), fill="#2e7d32")

if __name__ == "__main__":
    janela = tk.Tk()
    jogo = JogoFloresta(janela)
    janela.mainloop()
