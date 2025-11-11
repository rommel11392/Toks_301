import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont
import conexion
import menu

def abrir_sucursales():
    sucursales = tk.Tk()
    sucursales.title("Sucursales")
    sucursales.geometry("1500x1200")
    sucursales.config(bg="#26A69A")
    sucursales.resizable(True, True)

    titulo_font = tkFont.Font(family="Helvetica", size=16, weight="bold")
    label_font = tkFont.Font(family="Helvetica", size=10)
    boton_font = tkFont.Font(family="Helvetica", size=10, weight="bold")

    frame_principal = tk.Frame(sucursales, bg="#FFFFFF", padx=20, pady=20, bd=3, relief="groove")
    frame_principal.pack(padx=30, pady=30, fill="both", expand=True)

    tk.Label(
        frame_principal,
        text="Sucursales",
        font=titulo_font,
        bg="#FFFFFF",
        fg="#333333"
    ).grid(row=0, column=0, columnspan=3, pady=(10, 20))

    campos = ["id_sucursal", "nombre_sucursal", "direccion"]
    entradas = {}

    for i, texto in enumerate(campos):
        tk.Label(
            frame_principal,
            text=f"{texto.replace('_', ' ').capitalize()}:",
            font=label_font,
            bg="#FFFFFF",
            anchor="w"
        ).grid(row=i + 1, column=0, padx=10, pady=5, sticky="w")

        entradas[texto] = tk.Entry(frame_principal, bd=2, relief="solid", font=label_font, width=40)
        entradas[texto].grid(row=i + 1, column=1, padx=10, pady=5, sticky="we")

    def ejecutar_sql(sql, params=(), fetch=False):
        con = conexion.conectar_bd()
        cursor = con.cursor()
        cursor.execute(sql, params)
        if fetch:
            resultado = cursor.fetchall()
            con.close()
            return resultado
        else:
            con.commit()
            con.close()

    def insertar():
        if any(not entradas[c].get() for c in campos):
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios")
            return
        sql = "INSERT INTO sucursales (id_sucursal, nombre_sucursal, direccion) VALUES (%s, %s, %s)"
        params = tuple(entradas[c].get() for c in campos)
        ejecutar_sql(sql, params)
        mostrar_datos()
        limpiar()
        messagebox.showinfo("Éxito", "Sucursal agregada correctamente")

    def actualizar():
        if not entradas["id_sucursal"].get():
            messagebox.showwarning("Atención", "Seleccione una sucursal para actualizar")
            return
        sql = "UPDATE sucursales SET nombre_sucursal=%s, direccion=%s WHERE id_sucursal=%s"
        params = (
            entradas["nombre_sucursal"].get(),
            entradas["direccion"].get(),
            entradas["id_sucursal"].get()
        )
        ejecutar_sql(sql, params)
        mostrar_datos()
        limpiar()
        messagebox.showinfo("Éxito", "Sucursal actualizada correctamente")

    def eliminar():
        if not entradas["id_sucursal"].get():
            messagebox.showwarning("Atención", "Seleccione una sucursal para eliminar")
            return
        sql = "DELETE FROM sucursales WHERE id_sucursal=%s"
        ejecutar_sql(sql, (entradas["id_sucursal"].get(),))
        mostrar_datos()
        limpiar()
        messagebox.showinfo("Éxito", "Sucursal eliminada correctamente")

    def limpiar():
        for e in entradas.values():
            e.delete(0, tk.END)

    columnas = ("id_sucursal", "nombre_sucursal", "direccion")
    tabla = ttk.Treeview(frame_principal, columns=columnas, show="headings", height=12)
    for col in columnas:
        tabla.heading(col, text=col.replace("_", " ").capitalize())
        tabla.column(col, width=540)
    tabla.grid(row=6, column=0, columnspan=5, padx=10, pady=20, sticky="nsew")

    def mostrar_datos():
        for row in tabla.get_children():
            tabla.delete(row)
        datos = ejecutar_sql("SELECT * FROM sucursales", fetch=True)
        for fila in datos:
            tabla.insert("", tk.END, values=fila)

    def seleccionar(event):
        seleccionado = tabla.selection()
        if seleccionado:
            valores = tabla.item(seleccionado[0], "values")
            for i, c in enumerate(campos):
                entradas[c].delete(0, tk.END)
                entradas[c].insert(0, valores[i])

    tabla.bind("<<TreeviewSelect>>", seleccionar)

    def crear_boton(texto, comando, color):
        return tk.Button(
            frame_principal,
            text=texto,
            command=comando,
            bg=color,
            fg="black",
            font=boton_font,
            relief="raised",
            bd=2,
            width=14,
            padx=5,
            pady=5,
            cursor="hand2",
            activebackground="#333333",
            activeforeground="white"
        )

    botones = [
        ("Agregar", insertar, "#26A69A"),
        ("Actualizar", actualizar, "#4DB6AC"),
        ("Eliminar", eliminar, "#80CBC4"),
        ("Limpiar", limpiar, "#B2DFDB"),
    ]
    for i, (texto, cmd, color) in enumerate(botones):
        crear_boton(texto, cmd, color).grid(row=4, column=i, padx=5, pady=10)

    crear_boton("Regresar al Menú", lambda: [sucursales.destroy(), menu.abrir_menu()], "#E0F2F1") \
        .grid(row=8, column=0, columnspan=3, pady=10)

    mostrar_datos()
    sucursales.mainloop()


if __name__ == "__main__":
    abrir_sucursales()