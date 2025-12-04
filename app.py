import customtkinter as ctk
import json
import os

# Configurações Visuais
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

ARQUIVO_DADOS = "dados_lixo.json"

# --- JANELA DO RANKING (---
class JanelaRanking(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Classificação - VISUALIZAÇÃO")
        self.geometry("400x600")
        self.resizable(True, True)

        self.lbl_titulo = ctk.CTkLabel(self, text="🏆 RANKING GERAL 🏆", font=("Arial", 28, "bold"), text_color="#FFD700")
        self.lbl_titulo.pack(pady=20)

        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.pack(pady=10, padx=20, expand=True, fill="both")

    def atualizar_tela(self, dados):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        ranking_ordenado = sorted(dados.items(), key=lambda item: item[1], reverse=True)

        for i, (nome, pontos) in enumerate(ranking_ordenado):
            emoji = f"{i+1}º"
            cor_texto = "white"
            tamanho_fonte = 20
            
            if i == 0: 
                emoji = "1º"
                cor_texto = "#FFD700" # Dourado
                tamanho_fonte = 26
            elif i == 1: 
                emoji = "2º"
                cor_texto = "#C0C0C0" # Prata
                tamanho_fonte = 24
            elif i == 2: 
                emoji = "3º"
                cor_texto = "#CD7F32" # Bronze
                tamanho_fonte = 22

            # Card visual
            card = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
            card.pack(pady=5, padx=5, fill="x")

            # Texto: Rank + Nome
            lbl_nome = ctk.CTkLabel(card, text=f"{emoji}  {nome}", font=("Arial", tamanho_fonte, "bold"), text_color=cor_texto)
            lbl_nome.pack(side="left", padx=10)

            # Texto: Pontos
            lbl_pontos = ctk.CTkLabel(card, text=f"{pontos} XP", font=("Arial", tamanho_fonte), text_color="#00FF00")
            lbl_pontos.pack(side="right", padx=10)


# --- JANELA DE ADMIN (O Controle Remoto) ---
class AppAdmin(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Painel ADMIN ⚙️")
        self.geometry("500x500")
        self.resizable(False, False)

        self.dados = self.carregar_dados()
        self.janela_ranking = None

        # --- Layout do Admin ---
        ctk.CTkLabel(self, text="⚙️ Painel de Controle", font=("Arial", 20, "bold")).pack(pady=15)

        self.btn_abrir_ranking = ctk.CTkButton(self, text="📺 Abrir Tela de Ranking", command=self.abrir_janela_ranking)
        self.btn_abrir_ranking.pack(pady=5)

        frame_add = ctk.CTkFrame(self)
        frame_add.pack(pady=15, padx=20, fill="x")
        
        self.entry_nome = ctk.CTkEntry(frame_add, placeholder_text="Novo participante...")
        self.entry_nome.pack(side="left", padx=10, pady=10, expand=True, fill="x")
        
        btn_add = ctk.CTkButton(frame_add, text="Cadastrar", width=80, command=self.adicionar_participante)
        btn_add.pack(side="right", padx=10)

        self.scroll_admin = ctk.CTkScrollableFrame(self, label_text="Gerenciar Pontos")
        self.scroll_admin.pack(pady=10, padx=20, expand=True, fill="both")

        self.atualizar_lista_admin()
        self.abrir_janela_ranking()

    def carregar_dados(self):
        if os.path.exists(ARQUIVO_DADOS):
            try:
                with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def salvar_dados(self):
        with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
            json.dump(self.dados, f, indent=4, ensure_ascii=False)
        if self.janela_ranking is not None and self.janela_ranking.winfo_exists():
            self.janela_ranking.atualizar_tela(self.dados)

    def abrir_janela_ranking(self):
        if self.janela_ranking is None or not self.janela_ranking.winfo_exists():
            self.janela_ranking = JanelaRanking(self)
            self.janela_ranking.atualizar_tela(self.dados)
            self.janela_ranking.focus()
        else:
            self.janela_ranking.focus()

    def adicionar_participante(self):
        nome = self.entry_nome.get().strip()
        if nome and nome not in self.dados:
            self.dados[nome] = 0
            self.salvar_dados()
            self.entry_nome.delete(0, "end")
            self.atualizar_lista_admin()

    def dar_pontos(self, nome, qtd):
        self.dados[nome] += qtd
        self.salvar_dados()
        self.atualizar_lista_admin()

    def resetar(self, nome):
        self.dados[nome] = 0
        self.salvar_dados()
        self.atualizar_lista_admin()

    def atualizar_lista_admin(self):
        # Atualiza a lista
        for widget in self.scroll_admin.winfo_children():
            widget.destroy()
        for nome in sorted(self.dados.keys()):
            pontos = self.dados[nome]
            
            row = ctk.CTkFrame(self.scroll_admin)
            row.pack(pady=2, padx=2, fill="x")

            ctk.CTkLabel(row, text=f"{nome} ({pontos})", anchor="w", width=150).pack(side="left", padx=5)
            
            ctk.CTkButton(row, text="+1", width=40, fg_color="green", command=lambda n=nome: self.dar_pontos(n, 1)).pack(side="right", padx=2)
            ctk.CTkButton(row, text="Zerar", width=40, fg_color="red", command=lambda n=nome: self.resetar(n)).pack(side="right", padx=2)

if __name__ == "__main__":
    app = AppAdmin()
    app.mainloop()