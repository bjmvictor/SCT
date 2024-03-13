import tkinter as tk

root = tk.Tk()
root.overrideredirect(True)  # Remove a moldura da janela

# Define a transparência (0.5 para 50%)
root.attributes('-alpha', 0.5)

# Configura a janela para sempre ficar no topo
root.wm_attributes("-topmost", True)

# Máscara para evitar que a janela apareça na barra de tarefas (só funciona em Windows)
root.wm_attributes("-toolwindow", True)

# Define a cor de fundo como semi-transparente
root.configure(bg='black')  # Pode alterar a cor de fundo aqui

# Configura a geometria da janela
root.geometry("400x300+300+200")  # Largura x Altura + Posição X + Posição Y

root.mainloop()