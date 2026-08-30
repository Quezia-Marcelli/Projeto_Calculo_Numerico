import customtkinter as ctk
from tkinter import filedialog, messagebox
import numpy as np
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

CFG = {
    "tema_janela": "Dark",          
    "tema_botoes": "blue",          
    
    # Cores do Gráfico
    "grafico_fundo": "#242424",     
    "grafico_miolo": "#2b2b2b",     
    "cor_eixos": "white",           
    
    "cor_pontos": "#FF9800",        
    "cor_linha": "#8E00E6",         
    "cor_previsao": "#FAE315",      
    
    # Cores dos Botões 
    "btn_calcular": "#2E7D32",      
    "btn_limpar": "#C62828"         
}

# Configuração inicial do CustomTkinter
ctk.set_appearance_mode(CFG["tema_janela"])
ctk.set_default_color_theme(CFG["tema_botoes"])

class AppFinal(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MMQ - Visualizador de Ajuste de Curvas")
        self.geometry("1100x650")
        
        self.lx, self.ly, self.coefs = [], [], None

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._criar_interface()

    def _criar_interface(self):
        # PAINEL LATERAL
        painel = ctk.CTkFrame(self, width=280, corner_radius=0)
        painel.grid(row=0, column=0, sticky="nsew")

        ctk.CTkLabel(painel, text="DADOS", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Inputs X e Y
        f_in = ctk.CTkFrame(painel, fg_color="transparent")
        f_in.pack()
        self.en_x = ctk.CTkEntry(f_in, width=60, placeholder_text="X"); self.en_x.pack(side="left", padx=2)
        self.en_y = ctk.CTkEntry(f_in, width=60, placeholder_text="Y"); self.en_y.pack(side="left", padx=2)
        ctk.CTkButton(f_in, text="+", width=30, command=self.add).pack(side="left")

        ctk.CTkButton(painel, text="Importar CSV", command=self.csv).pack(fill="x", padx=20, pady=10)
        
        # Botão Limpar 
        ctk.CTkButton(painel, text="Limpar", fg_color=CFG["btn_limpar"], hover_color="#800000", command=self.limpar).pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(painel, text="GRAU DO POLINÔMIO").pack(pady=(15,0))
        self.grau = ctk.CTkComboBox(painel, values=["1", "2", "3", "4"]); self.grau.pack(pady=5)
        
        # Botão Calcular 
        ctk.CTkButton(painel, text="CALCULAR (MMQ)", fg_color=CFG["btn_calcular"], hover_color="#1B5E20", command=self.calcular_manual).pack(fill="x", padx=20, pady=10)

        # Labels de Resultado
        self.lb_eq = ctk.CTkLabel(painel, text="Eq: ...", text_color="#4FC3F7", wraplength=250, font=("Consolas", 13))
        self.lb_eq.pack(pady=10)
        self.lb_r2 = ctk.CTkLabel(painel, text="R²: --", text_color="#03F48C", font=("Arial", 14))
        self.lb_r2.pack(pady=5)

        # Previsão
        ctk.CTkLabel(painel, text="PREVISÃO", font=("Arial", 12, "bold")).pack(pady=(20,5))
        self.en_prev = ctk.CTkEntry(painel, placeholder_text="Novo X"); self.en_prev.pack()
        ctk.CTkButton(painel, text="Prever", command=self.prever).pack(pady=5)
        self.lb_res = ctk.CTkLabel(painel, text="Result: --"); self.lb_res.pack()

        # ÁREA DO GRÁFICO 
        self.fig = Figure(figsize=(5,5), dpi=100, facecolor=CFG["grafico_fundo"])
        self.ax = self.fig.add_subplot(111, facecolor=CFG["grafico_miolo"])
        
        
        cor_txt = CFG["cor_eixos"]
        self.ax.tick_params(colors=cor_txt, labelcolor=cor_txt)
        for spine in self.ax.spines.values(): spine.set_color(cor_txt)
        self.ax.xaxis.label.set_color(cor_txt)
        self.ax.yaxis.label.set_color(cor_txt)
        self.ax.title.set_color(cor_txt)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    # LÓGICA MATEMÁTICA
    def calcular_manual(self):
        if len(self.lx) < 2: return
        g = int(self.grau.get())
        
        X_vals = np.array(self.lx, dtype=float)
        Y_vals = np.array(self.ly, dtype=float)

        # 1. Matriz Vandermonde
        X = np.vander(X_vals, g + 1, increasing=True)
        
        # 2. Equação Normal (MMQ)
        Xt = X.T
        try:
            XtX = Xt @ X
            XtX_inv = np.linalg.inv(XtX)
            Xty = Xt @ Y_vals
            self.coefs = (XtX_inv @ Xty).flatten()
        except np.linalg.LinAlgError:
            messagebox.showerror("Erro", "Matriz Singular.")
            return

        # 3. R²
        y_pred = np.array([self.f_polinomio(x) for x in X_vals])
        res = np.sum((Y_vals - y_pred)**2)
        tot = np.sum((Y_vals - np.mean(Y_vals))**2)
        r2 = 1 - (res/tot) if tot != 0 else 0.0
        
        self.lb_r2.configure(text=f"R²: {r2:.4f}")
        
        eq_text = "y = " + "".join([f"{c:+.2f}x^{i} " for i, c in enumerate(self.coefs)])
        self.lb_eq.configure(text=eq_text)

        # 4. Plotagem
        x_lin = np.linspace(min(X_vals), max(X_vals), 100)
        y_lin = [self.f_polinomio(v) for v in x_lin]

        self.ax.clear(); self.ax.grid(True, linestyle=':', alpha=0.3)
        self.ax.scatter(self.lx, self.ly, c=CFG["cor_pontos"], s=50, label="Dados")
        self.ax.plot(x_lin, y_lin, c=CFG["cor_linha"], lw=2, label="Ajuste")
        self.ax.legend(facecolor=CFG["grafico_miolo"], labelcolor=CFG["cor_eixos"])
        self.canvas.draw()

    def f_polinomio(self, x_val):
        if self.coefs is None: return 0
        y = 0
        for i, c in enumerate(self.coefs):
            y += c * (x_val ** i)
        return y

    def prever(self):
        try:
            val = float(self.en_prev.get())
            if self.coefs is None: return
            res = self.f_polinomio(val)
            self.lb_res.configure(text=f"Y = {res:.4f}")
            self.ax.scatter(val, res, c=CFG["cor_previsao"], marker='*', s=150, zorder=5)
            self.canvas.draw()
        except: pass

    def add(self):
        try:
            x, y = float(self.en_x.get()), float(self.en_y.get())
            self.lx.append(x); self.ly.append(y)
            self.ax.scatter(x, y, c=CFG["cor_pontos"]); self.canvas.draw()
            self.en_x.delete(0,'end'); self.en_y.delete(0,'end')
        except: pass

    def csv(self):
        f = filedialog.askopenfilename()
        if f:
            try:
                df = pd.read_csv(f, header=None).select_dtypes(include=[np.number])
                self.limpar()
                self.lx, self.ly = df.iloc[:,0].tolist(), df.iloc[:,1].tolist()
                self.ax.scatter(self.lx, self.ly, c=CFG["cor_pontos"]); self.canvas.draw()
            except: pass

    def limpar(self):
        self.lx, self.ly, self.coefs = [], [], None
        self.ax.clear(); self.canvas.draw()
        self.lb_eq.configure(text="Eq: ..."); self.lb_r2.configure(text="R²: --")
        self.lb_res.configure(text="Result: --")

if __name__ == "__main__":
    app = AppFinal()
    app.mainloop()