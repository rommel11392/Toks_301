import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont
import conexion
import menu

def abrir_ventas():
    ventas = tk.Tk()
    ventas.title("Ventas")
    ventas.geometry("1100x750")
    ventas.config(bg="#26A69A")
    ventas.resizable(True, True)

    titulo_font = tkFont.Font(family="Helvetica", size=16, weight="bold")
    label_font = tkFont.Font(family="Helvetica", size=10)
    boton_font = tkFont.Font(family="Helvetica", size=10, weight="bold")

    frame_principal = tk.Frame(ventas, bg="#FFFFFF", padx=25, pady=25, bd=3, relief="groove")
    frame_principal.pack(padx=30, pady=30, fill="both", expand=True)

    tk.Label(frame_principal, text="Ventas", font=titulo_font, bg="#FFFFFF", fg="#333333") \
        .grid(row=0, column=0, columnspan=10, pady=(10, 20))

    campos = [
        ("id_ventas", 1, 0),
        ("fecha_venta (YYYY-MM-DD)", 2, 0),
        ("id_productos", 3, 0),
        ("id_sucursal", 4, 0),
        ("id_empleado", 5, 0),
        ("cantidad_productos", 1, 3),
        ("precio_unitario", 2, 3),
        ("subtotal", 3, 3),
        ("iva", 4, 3),
        ("total", 5, 3)
    ]

    entradas = {}
    for texto, fila, col in campos:
        tk.Label(frame_principal, text=texto.replace("_", " ").capitalize() + ":", font=label_font,
                 bg="#FFFFFF", anchor="w").grid(row=fila, column=col, padx=10, pady=5, sticky="w")

        entrada = tk.Entry(frame_principal, bd=2, relief="solid", font=label_font, width=30)
        entrada.grid(row=fila, column=col + 1, padx=10, pady=5)
        entradas[texto] = entrada

    def ejecutar_sql(sql, params=(), fetch=False):
        con = conexion.conectar_bd()
        cursor = con.cursor()
        cursor.execute(sql, params)
        if fetch:
            datos = cursor.fetchall()
            con.close()
            return datos
        else:
            con.commit()
            con.close()

    def calcular_totales(event=None):
        try:
            cantidad = float(entradas["cantidad_productos"].get())
            precio = float(entradas["precio_unitario"].get())
            subtotal = cantidad * precio
            iva = subtotal * 0.16
            total = subtotal + iva
            for campo, valor in [("subtotal", subtotal), ("iva", iva), ("total", total)]:
                entradas[campo].delete(0, tk.END)
                entradas[campo].insert(0, f"{valor:.2f}")
        except ValueError:
            for campo in ("subtotal", "iva", "total"):
                entradas[campo].delete(0, tk.END)

    entradas["cantidad_productos"].bind("<KeyRelease>", calcular_totales)
    entradas["precio_unitario"].bind("<KeyRelease>", calcular_totales)

    def insertar():
        if not entradas["id_ventas"].get() or not entradas["fecha_venta (YYYY-MM-DD)"].get() or not entradas["id_productos"].get():
            messagebox.showwarning("Campos vacíos", "El ID, la fecha y el producto son obligatorios")
            return
        sql = """INSERT INTO ventas
                (id_ventas, fecha_venta, id_productos, id_sucursal, id_empleado, cantidad_productos,
                 precio_unitario, subtotal, iva, total)
                 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        params = tuple(entradas[c].get() for c in [
            "id_ventas", "fecha_venta (YYYY-MM-DD)", "id_productos", "id_sucursal",
            "id_empleado", "cantidad_productos", "precio_unitario", "subtotal", "iva", "total"])
        ejecutar_sql(sql, params)
        mostrar_datos()
        limpiar()
        messagebox.showinfo("Éxito", "Venta registrada correctamente")

    def actualizar():
        if not entradas["id_ventas"].get():
            messagebox.showwarning("Atención", "Seleccione una venta para actualizar")
            return
        sql = """UPDATE ventas SET 
                 fecha_venta=%s, id_productos=%s, id_sucursal=%s, id_empleado=%s, 
                 cantidad_productos=%s, precio_unitario=%s, subtotal=%s, iva=%s, total=%s 
                 WHERE id_ventas=%s"""
        params = (
            entradas["fecha_venta (YYYY-MM-DD)"].get(),
            entradas["id_productos"].get(),
            entradas["id_sucursal"].get(),
            entradas["id_empleado"].get(),
            entradas["cantidad_productos"].get(),
            entradas["precio_unitario"].get(),
            entradas["subtotal"].get(),
            entradas["iva"].get(),
            entradas["total"].get(),
            entradas["id_ventas"].get()
        )
        ejecutar_sql(sql, params)
        mostrar_datos()
        limpiar()
        messagebox.showinfo("Éxito", "Venta actualizada correctamente")

    def eliminar():
        if not entradas["id_ventas"].get():
            messagebox.showwarning("Atención", "Seleccione una venta para eliminar")
            return
        ejecutar_sql("DELETE FROM ventas WHERE id_ventas=%s", (entradas["id_ventas"].get(),))
        mostrar_datos()
        limpiar()
        messagebox.showinfo("Éxito", "Venta eliminada correctamente")

    def limpiar():
        for e in entradas.values():
            e.delete(0, tk.END)

    columnas = ("id_ventas", "fecha_venta", "id_productos", "id_sucursal", "id_empleado",
                "cantidad_productos", "precio_unitario", "subtotal", "iva", "total")
    tabla = ttk.Treeview(frame_principal, columns=columnas, show="headings", height=12)
    for col in columnas:
        tabla.heading(col, text=col.replace("_", " ").capitalize())
        tabla.column(col, width=170)
    tabla.grid(row=7, column=0, columnspan=5, padx=10, pady=20, sticky="nsew")

    def mostrar_datos():
        for row in tabla.get_children():
            tabla.delete(row)
        datos = ejecutar_sql("SELECT * FROM ventas", fetch=True)
        for fila in datos:
            tabla.insert("", tk.END, values=fila)

    def seleccionar(event):
        seleccionado = tabla.selection()
        if seleccionado:
            valores = tabla.item(seleccionado[0], "values")
            for i, campo in enumerate([
                "id_ventas", "fecha_venta (YYYY-MM-DD)", "id_productos", "id_sucursal",
                "id_empleado", "cantidad_productos", "precio_unitario", "subtotal", "iva", "total"
            ]):
                entradas[campo].delete(0, tk.END)
                entradas[campo].insert(0, valores[i])

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
        crear_boton(texto, cmd, color).grid(row=6, column=i, padx=5, pady=10)

    crear_boton("Regresar al Menú", lambda: [ventas.destroy(), menu.abrir_menu()], "#E0F2F1") \
        .grid(row=8, column=0, columnspan=10, pady=15)

    mostrar_datos()
    ventas.mainloop()


if __name__ == "__main__":
    abrir_ventas()