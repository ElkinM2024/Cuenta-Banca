import hashlib
import tkinter as tk
from tkinter import messagebox, simpledialog


class CuentaBancaria:
    def __init__(self, numero_cuenta, titular, tipo_cuenta, saldo_inicial=0, usuario="", contrasena=""):
        self.numero_cuenta = numero_cuenta
        self.titular = titular
        self.tipo_cuenta = tipo_cuenta
        self.saldo = saldo_inicial
        self.transacciones = []
        self.usuario = usuario
        self.contrasena = contrasena  # Contraseña en formato hash

    def consultar_saldo(self):
        return f"Saldo disponible: {self.saldo}€"
    
    def depositar(self, monto):
        if monto > 0:
            self.saldo += monto
            self.transacciones.append(f"Depósito: {monto}€")
            return f"Depósito realizado. Saldo actual: {self.saldo}€"
        return "Error: El monto debe ser positivo."
    
    def retirar(self, monto):
        if monto <= 0:
            return "Error: El monto debe ser positivo."
        elif monto > self.saldo:
            return "Error: Fondos insuficientes."
        else:
            self.saldo -= monto
            self.transacciones.append(f"Retiro: {monto}€")
            return f"Retiro realizado. Saldo actual: {self.saldo}€"
    
    def transferir(self, cuenta_destino, monto):
        if monto <= 0:
            return "Error: El monto debe ser positivo."
        elif monto > self.saldo:
            return "Error: Fondos insuficientes."
        else:
            self.saldo -= monto
            cuenta_destino.saldo += monto
            self.transacciones.append(f"Transferencia a cuenta {cuenta_destino.numero_cuenta}: {monto}€")
            cuenta_destino.transacciones.append(f"Transferencia desde cuenta {self.numero_cuenta}: {monto}€")
            return f"Transferencia realizada. Saldo actual: {self.saldo}€"

    def mostrar_transacciones(self):
        return "\n".join(self.transacciones) if self.transacciones else "No hay transacciones registradas."

    def verificar_contrasena(self, contrasena_ingresada):
        return self.contrasena == hashlib.md5(contrasena_ingresada.encode()).hexdigest()


class BancoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación de Cuenta Bancaria")
        self.root.geometry("600x600")
        self.root.config(bg="#f4f4f9")
        
        # Cuentas predefinidas
        self.cuentas = {
            "123456789": CuentaBancaria(
                numero_cuenta="123456789", 
                titular="Elkin Martillo",  # Nombre actualizado
                tipo_cuenta="Ahorro", 
                saldo_inicial=1000, 
                usuario="elkin",  # Usuario actualizado
                contrasena=hashlib.md5("1234".encode()).hexdigest()  # Contraseña "1234" en hash
            ),
            "987654321": CuentaBancaria(
                numero_cuenta="987654321", 
                titular="Manuel Martillo", 
                tipo_cuenta="Corriente", 
                saldo_inicial=500, 
                usuario="manuel", 
                contrasena=hashlib.md5("1234".encode()).hexdigest()
            )
        }
        
        self.cuenta_autenticada = None
        self.iniciar_login()

    def iniciar_login(self):
        self.login_frame = tk.Frame(self.root, bg="#f4f4f9")
        self.login_frame.pack(pady=100)
        
        tk.Label(self.login_frame, text="Usuario", bg="#f4f4f9", font=("Helvetica", 14)).pack()
        self.usuario_entry = tk.Entry(self.login_frame, font=("Helvetica", 12))
        self.usuario_entry.pack(pady=5)
        
        tk.Label(self.login_frame, text="Contraseña", bg="#f4f4f9", font=("Helvetica", 14)).pack()
        self.contrasena_entry = tk.Entry(self.login_frame, show="*", font=("Helvetica", 12))
        self.contrasena_entry.pack(pady=5)
        
        self.login_button = tk.Button(self.login_frame, text="Iniciar Sesión", font=("Helvetica", 14), command=self.autenticar_usuario, bg="#4CAF50", fg="white", width=20)
        self.login_button.pack(pady=20)

    def autenticar_usuario(self):
        usuario = self.usuario_entry.get()
        contrasena = self.contrasena_entry.get()
        
        for cuenta in self.cuentas.values():
            if cuenta.usuario == usuario and cuenta.verificar_contrasena(contrasena):
                self.cuenta_autenticada = cuenta
                self.login_frame.destroy()
                self.mostrar_dashboard()
                return
        messagebox.showerror("Error", "Credenciales incorrectas.")

    def mostrar_dashboard(self):
        self.dashboard_frame = tk.Frame(self.root, bg="#f4f4f9")
        self.dashboard_frame.pack(pady=50)
        
        tk.Label(self.dashboard_frame, text=f"Bienvenido, {self.cuenta_autenticada.titular}", font=("Helvetica", 16), bg="#f4f4f9").pack(pady=10)
        self.saldo_label = tk.Label(self.dashboard_frame, text=self.cuenta_autenticada.consultar_saldo(), font=("Helvetica", 14), bg="#f4f4f9")
        self.saldo_label.pack(pady=10)
        
        self.deposito_button = tk.Button(self.dashboard_frame, text="Depositar", font=("Helvetica", 14), command=self.depositar, bg="#2196F3", fg="white", width=20)
        self.deposito_button.pack(pady=5)
        
        self.retirar_button = tk.Button(self.dashboard_frame, text="Retirar", font=("Helvetica", 14), command=self.retirar, bg="#FF5722", fg="white", width=20)
        self.retirar_button.pack(pady=5)
        
        self.transferir_button = tk.Button(self.dashboard_frame, text="Transferir", font=("Helvetica", 14), command=self.transferir, bg="#9C27B0", fg="white", width=20)
        self.transferir_button.pack(pady=5)
        
        self.transacciones_button = tk.Button(self.dashboard_frame, text="Ver Transacciones", font=("Helvetica", 14), command=self.mostrar_transacciones, bg="#607D8B", fg="white", width=20)
        self.transacciones_button.pack(pady=5)
        
        self.logout_button = tk.Button(self.dashboard_frame, text="Cerrar Sesión", font=("Helvetica", 14), command=self.cerrar_sesion, bg="#F44336", fg="white", width=20)
        self.logout_button.pack(pady=20)
    
    def depositar(self):
        monto = simpledialog.askfloat("Monto", "Ingrese el monto a depositar:")
        if monto and monto > 0:
            resultado = self.cuenta_autenticada.depositar(monto)
            messagebox.showinfo("Depósito", resultado)
            self.saldo_label.config(text=self.cuenta_autenticada.consultar_saldo())
        else:
            messagebox.showerror("Error", "Monto no válido.")
    
    def retirar(self):
        monto = simpledialog.askfloat("Monto", "Ingrese el monto a retirar:")
        if monto and monto > 0:
            resultado = self.cuenta_autenticada.retirar(monto)
            messagebox.showinfo("Retiro", resultado)
            self.saldo_label.config(text=self.cuenta_autenticada.consultar_saldo())
        else:
            messagebox.showerror("Error", "Monto no válido.")
    
    def transferir(self):
        monto = simpledialog.askfloat("Monto", "Ingrese el monto a transferir:")
        if monto and monto > 0:
            cuenta_destino = simpledialog.askstring("Cuenta Destino", "Ingrese el número de cuenta destino:")
            cuenta_destino_obj = self.cuentas.get(cuenta_destino)
            if cuenta_destino_obj:
                resultado = self.cuenta_autenticada.transferir(cuenta_destino_obj, monto)
                messagebox.showinfo("Transferencia", resultado)
                self.saldo_label.config(text=self.cuenta_autenticada.consultar_saldo())
            else:
                messagebox.showerror("Error", "Cuenta destino no válida.")
    
    def mostrar_transacciones(self):
        transacciones = self.cuenta_autenticada.mostrar_transacciones()
        messagebox.showinfo("Transacciones", transacciones)

    def cerrar_sesion(self):
        self.dashboard_frame.destroy()
        self.iniciar_login()


if __name__ == "__main__":
    root = tk.Tk()
    app = BancoApp(root)
    root.mainloop()
