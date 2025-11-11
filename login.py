import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont
import menu

usuario_correcto = "borjita"
pass_correcto = "72"

def mostrar_login():
    ventana_login = tk.Tk()
    ventana_login.title("Inicio de Sesión")
    ventana_login.geometry("400x400")
    ventana_login.config(bg="#26A69A")  
    ventana_login.resizable(True, True)

    titulo_font = tkFont.Font(family="Helvetica", size=16, weight="bold")
    label_font = tkFont.Font(family="Helvetica", size=10)
    boton_font = tkFont.Font(family="Helvetica", size=10, weight="bold")

    def verificar_login():
        usuario = entry_usuario.get()
        contraseña = entry_contraseña.get()

        if not usuario or not contraseña:
            messagebox.showwarning("Campos vacíos", "Por favor, ingrese usuario y contraseña.")
            return

        if usuario == usuario_correcto and contraseña == pass_correcto:
            messagebox.showinfo("Acceso concedido", f"¡Bienvenido, {usuario}!")
            ventana_login.destroy()
            menu.abrir_menu()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    frame_login = tk.Frame(ventana_login, bg="#FFFFFF", padx=20, pady=20, bd=3, relief="groove")
    frame_login.pack(padx=30, pady=30, fill="both", expand=True)

    tk.Label(
        frame_login,
        text="Iniciar Sesión",
        font=titulo_font,
        bg="#FFFFFF",
        fg="#333333"
    ).pack(pady=(5, 15))

    tk.Label(frame_login, text="Usuario:", font=label_font, bg="#FFFFFF", anchor="w").pack(fill="x", pady=(5, 0))
    entry_usuario = tk.Entry(frame_login, bd=2, relief="solid", font=label_font)
    entry_usuario.pack(fill="x", pady=5)
    entry_usuario.focus()

    tk.Label(frame_login, text="Contraseña:", font=label_font, bg="#FFFFFF", anchor="w").pack(fill="x", pady=(10, 0))
    entry_contraseña = tk.Entry(frame_login, show="*", bd=2, relief="solid", font=label_font)
    entry_contraseña.pack(fill="x", pady=5)

    button_frame = tk.Frame(frame_login, bg="#FFFFFF")
    button_frame.pack(pady=20)

    def crear_boton(texto, comando, color):
        return tk.Button(
            button_frame,
            text=texto,
            command=comando,
            bg=color,
            fg="white",
            font=boton_font,
            padx=10,
            pady=5,
            width=12,
            relief="raised",
            bd=2,
            cursor="hand2",
            activebackground="#333333",
            activeforeground="white"
        )

    crear_boton("Iniciar sesión", verificar_login, "#4DB6AC").pack(side="left", padx=5)
    crear_boton("Salir", ventana_login.destroy, "#80CBC4").pack(side="left", padx=5)

    ventana_login.mainloop()


if __name__ == "__main__":
    mostrar_login()