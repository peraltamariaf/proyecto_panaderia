import tkinter as tk
import json
from datetime import datetime
import os


class Producto:

    def __init__(self, nombre, comprado, producido):
        self.nombre = nombre
        self.comprado = int(comprado)
        self.producido = int(producido)
        self.final = None
        self.vendido = None
        self.fecha = datetime.now().strftime("%d-%m-%y")

    def calcular_vendido(self, cantidad_final):
        self.final = int(cantidad_final)
        total = self.comprado + self.producido
        self.vendido = total - self.final

    def mostrar(self):
        return {
            "nombre": self.nombre,
            "comprado": self.comprado,
            "producido": self.producido,
            "final": self.final,
            "vendido": self.vendido,
            "fecha": self.fecha
        }



class InventarioApp:

    def __init__(self, root):
        self.root = root
        self.root.iconbitmap(r"C:\Users\Marife\Documents\maria\programación\proyecto_panaderia\cala-sola.ico")
        self.root.title("Panadería - Control Diario")
        self.root.geometry("500x550")
        self.root.config(bg="#f5f5dc")

        self.crear_interfaz()

    
    def crear_interfaz(self):

     self.frame_izquierdo = tk.Frame(self.root, bg="#f5f5dc")
     self.frame_izquierdo.pack(side="left", padx=15, pady=10)

     self.frame_derecho = tk.Frame(self.root, bg="#f5f5dc")
     self.frame_derecho.pack(side="right", padx=15, pady=10)

     titulo = tk.Label(
         self.root,
         text="Control Diario Panadería",
         bg="#f5f5dc",
         fg="#5c4033",
         font=("Arial", 14, "bold")
        )
     titulo.pack(pady=10)

    
     tk.Label(self.frame_izquierdo, text="--- Registrar Inicio ---",
             bg="#f5f5dc", fg="#8b5a2b",
             font=("Arial", 12, "bold")).pack(pady=5)

     tk.Label(self.frame_izquierdo, text="Nombre:", bg="#f5f5dc", fg="#5c4033").pack()
     self.entry_nombre_inicio = tk.Entry(self.frame_izquierdo)
     self.entry_nombre_inicio.pack(pady=5)

     tk.Label(self.frame_izquierdo, text="Cantidad comprada:", bg="#f5f5dc", fg="#5c4033").pack()
     self.entry_comprado = tk.Entry(self.frame_izquierdo)
     self.entry_comprado.pack(pady=5)

     tk.Label(self.frame_izquierdo, text="Cantidad producida:", bg="#f5f5dc", fg="#5c4033").pack()
     self.entry_producido = tk.Entry(self.frame_izquierdo)
     self.entry_producido.pack(pady=5)

     btn_inicio = tk.Button(
         self.frame_izquierdo,
         text="Guardar Inicio",
         bg="#8b5a2b",
         fg="white",
         command=self.guardar_inicio
     )
     btn_inicio.pack(pady=10)

     tk.Label(self.frame_izquierdo, text="--- Registrar Final ---",
             bg="#f5f5dc", fg="#a0522d",
             font=("Arial", 12, "bold")).pack(pady=10)

     tk.Label(self.frame_izquierdo, text="Nombre del producto:", bg="#f5f5dc", fg="#5c4033").pack()
     self.entry_nombre_final = tk.Entry(self.frame_izquierdo)
     self.entry_nombre_final.pack(pady=5)

     tk.Label(self.frame_izquierdo, text="Cantidad final (sobrante):", bg="#f5f5dc", fg="#5c4033").pack()
     self.entry_final = tk.Entry(self.frame_izquierdo)
     self.entry_final.pack(pady=5)

     btn_final = tk.Button(
        self.frame_izquierdo,
        text="Guardar Final",
        bg="#a0522d",
        fg="white",
        command=self.guardar_final
     )
     btn_final.pack(pady=10)

     self.label_mensaje = tk.Label(self.frame_izquierdo,
                                  text="",
                                  bg="#f5f5dc",
                                  fg="#5c4033")
     self.label_mensaje.pack(pady=15)

     tk.Label(self.frame_derecho,
             text="Resumen del día:",
             bg="#f5f5dc",
             fg="#5c4033",
             font=("Arial", 11, "bold")).pack()

     self.text_resumen = tk.Text(self.frame_derecho, height=20, width=40)
     self.text_resumen.pack()


    def guardar_inicio(self):

        nombre = self.entry_nombre_inicio.get()
        comprado = self.entry_comprado.get()
        producido = self.entry_producido.get()

        if nombre == "" or comprado == "" or producido == "":
            self.label_mensaje.config(text="Complete todos los campos", fg="red")
            return

        producto = Producto(nombre, comprado, producido)

        try:
            with open("inventario_panaderia.json", "r") as archivo:
                datos = json.load(archivo)
        except:
            datos = []

        datos.append(producto.to_dict())

        with open("inventario_panaderia.json", "w") as archivo:
            json.dump(datos, archivo, indent=4)

        self.label_mensaje.config(text="Inicio guardado correctamente", fg="green")

        self.entry_nombre_inicio.delete(0, tk.END)
        self.entry_comprado.delete(0, tk.END)
        self.entry_producido.delete(0, tk.END)

   
    def guardar_final(self):

        nombre = self.entry_nombre_final.get()
        cantidad_final = self.entry_final.get()

        if nombre == "" or cantidad_final == "":
            self.label_mensaje.config(text="Complete los datos del final", fg="red")
            return

        try:
            with open("inventario_panaderia.json", "r") as archivo:
                datos = json.load(archivo)
        except:
            self.label_mensaje.config(text="No hay registros", fg="red")
            return

        producto_encontrado = False

        for producto in datos:
            if producto["nombre"] == nombre and producto["final"] is None:
                total = producto["comprado"] + producto["producido"]
                producto["final"] = int(cantidad_final)
                producto["vendido"] = total - int(cantidad_final)
                producto_encontrado = True

                self.text_resumen.delete("1.0", tk.END)
                resumen = (
                    f"Producto: {producto['nombre']}\n"
                    f"Comprado: {producto['comprado']}\n"
                    f"Producido: {producto['producido']}\n"
                    f"Total inicial: {total}\n"
                    f"Final (sobró): {producto['final']}\n"
                    f"Vendido: {producto['vendido']}\n"
                    f"Fecha: {producto['fecha']}\n"
                )
                self.text_resumen.insert(tk.END, resumen)

                break

        if not producto_encontrado:
            self.label_mensaje.config(text="Producto no encontrado", fg="red")
            return

        with open("inventario_panaderia.json", "w") as archivo:
            json.dump(datos, archivo, indent=4)

        self.label_mensaje.config(text="Final guardado y ventas calculadas", fg="brown")

        self.entry_nombre_final.delete(0, tk.END)
        self.entry_final.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = InventarioApp(root)
    root.mainloop()
