import tkinter as tk
import tkinter.font as tkFont
import login
import empleados
import proveedores
import sucursales
import productos
import ventas

def abrir_menu():
    menu = tk.Tk()
    menu.title("Menú Principal")
    menu.geometry("500x500")
    menu.config(bg="#26A69A")  
    menu.resizable(True, True)

    titulo_font = tkFont.Font(family="Helvetica", size=16, weight="bold")
    boton_font = tkFont.Font(family="Helvetica", size=11, weight="bold")

    def regresar_a_login():
        menu.destroy()
        login.mostrar_login()
        
    def abrir_empleados():
        menu.withdraw()
        empleados.abrir_empleados()
        menu.deiconify()
    
    def abrir_sucursales():
        menu.withdraw()
        sucursales.abrir_sucursales()
        menu.deiconify()
        
    def abrir_productos():
        menu.withdraw()
        productos.abrir_productos()
        menu.deiconify()
        
    def abrir_ventas():
        menu.withdraw()
        ventas.abrir_ventas()
        menu.deiconify()
        
    def abrir_proveedores():
        menu.withdraw()
        proveedores.abrir_proveedores()
        menu.deiconify()

    main_frame = tk.Frame(menu, bg="#ffffff", padx=20, pady=20, bd=3, relief="groove")
    main_frame.pack(padx=30, pady=30, fill="both", expand=True)

    tk.Label(
        main_frame,
        text="Bienvenido al Menú Principal",
        font=titulo_font,
        bg="#ffffff",
        fg="#333333"
    ).pack(pady=(10, 20))

    def crear_boton(texto, comando, color):
        return tk.Button(
            main_frame,
            text=texto,
            command=comando,
            bg=color,
            fg="black",
            font=boton_font,
            relief="raised",
            bd=2,
            width=25,
            padx=5,
            pady=5,
            cursor="hand2",
            activebackground="#333333",
            activeforeground="black"
        )

    crear_boton("Empleados", abrir_empleados, "#26A69A").pack(pady=5)
    crear_boton("Sucursales", abrir_sucursales, "#4DB6AC").pack(pady=5)
    crear_boton("Productos", abrir_productos, "#80CBC4").pack(pady=5)
    crear_boton("Ventas", abrir_ventas, "#B2DFDB").pack(pady=5)
    crear_boton("Proveedores", abrir_proveedores, "#E0F2F1").pack(pady=5)

    crear_boton("Cerrar sesión", regresar_a_login, "#B2EBF2").pack(pady=(20, 10))

    menu.mainloop()

if __name__ == "__main__":
    abrir_menu()