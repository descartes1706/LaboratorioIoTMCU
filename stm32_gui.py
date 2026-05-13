import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import serial.tools.list_ports

DEFAULT_PORT = "/dev/serial0"

class STM32FlashGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("STM32Flash GUI")
        self.root.geometry("420x300")
        
        # Variables
        self.filepath = tk.StringVar()
        self.port = tk.StringVar(value=DEFAULT_PORT)
        self.available_ports = [DEFAULT_PORT]  # lista inicial
        
        # Widgets
        tk.Label(root, text="Archivo BIN/HEX:").pack(pady=5)
        self.entry_file = tk.Entry(root, textvariable=self.filepath, width=45)
        self.entry_file.pack()
        tk.Button(root, text="Buscar Archivo", command=self.browse_file).pack(pady=5)
        
        # Selector de puertos
        tk.Label(root, text="Puerto serial:").pack(pady=5)
        self.port_menu = tk.OptionMenu(root, self.port, *self.available_ports)
        self.port_menu.pack()
        
        tk.Button(root, text="Buscar Puertos", command=self.search_ports).pack(pady=5)
        
        tk.Button(root, text="Programar STM32", command=self.flash_firmware, bg="green", fg="white").pack(pady=15)
        tk.Button(root, text="Salir", command=root.quit).pack()
    
    def browse_file(self):
        filetypes = [("Binarios", "*.bin"), ("Hexadecimal", "*.hex"), ("Todos", "*.*")]
        filename = filedialog.askopenfilename(title="Selecciona firmware", filetypes=filetypes)
        if filename:
            self.filepath.set(filename)
    
    def search_ports(self):
        """Busca puertos seriales disponibles (incluyendo USB)"""
        ports = [port.device for port in serial.tools.list_ports.comports()]
        if not ports:
            ports = [DEFAULT_PORT]  # fallback
            messagebox.showwarning("Puertos", "No se detectaron puertos USB.\nVerifica la conexión.")
        
        # Actualizar lista en el OptionMenu
        self.available_ports = ports
        menu = self.port_menu["menu"]
        menu.delete(0, "end")
        for p in ports:
            menu.add_command(label=p, command=lambda value=p: self.port.set(value))
        
        # Seleccionar el primero por defecto
        self.port.set(ports[0])
    
    def flash_firmware(self):
        firmware = self.filepath.get()
        port = self.port.get()
        
        if not firmware or not os.path.exists(firmware):
            messagebox.showerror("Error", "Selecciona un archivo válido")
            return
        
        try:
            cmd = ["stm32flash", "-w", firmware, "-v", "-g", "0x0", port]
            print("Ejecutando:", " ".join(cmd))
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                messagebox.showinfo("Éxito", f"Programación completada:\n\n{result.stdout}")
            else:
                messagebox.showerror("Error", f"Falló la programación:\n\n{result.stderr}")
        
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = STM32FlashGUI(root)
    root.mainloop()
