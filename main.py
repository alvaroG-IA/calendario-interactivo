import json
import os
import tkinter as tk
import tkinter.messagebox as tkm
import calendar
from datetime import datetime
from date_tools import date_format

class CalendarApp:
    def __init__(self, root, data_path):
        self.root = root
        self.root.title("Calendario de horas - Prácticas")

        # Carga de JSON
        with open(data_path, "r") as f:
            self.datos = json.load(f)
        
        self.total_hours = sum(self.datos.values())
        self.string_hours = f'Total acumulado {self.total_hours}h'

        # Fecha inicial
        self.current_year = datetime.now().year
        self.current_month = datetime.now().month

        # Encabezado (mes y año)
        self.header = tk.Label(self.root, text="", font=("Helvetica", 16))
        self.header.pack(pady=10)

        # Botones de navegación
        nav_frame = tk.Frame(self.root)
        nav_frame.pack()

        prev_btn = tk.Button(nav_frame, text="←", command=self.prev_month)
        prev_btn.grid(row=0, column=0)

        next_btn = tk.Button(nav_frame, text="→", command=self.next_month)
        next_btn.grid(row=0, column=1)

        # Marco para el calendario
        self.calendar_frame = tk.Frame(self.root)
        self.calendar_frame.pack(pady=10)

        # Resumen de horas (placeholder)
        self.total_label = tk.Label(self.root, text=self.string_hours, font=("Helvetica", 16))
        self.total_label.pack(pady=10)

        self.draw_calendar()

    def draw_calendar(self):
        # Limpiar calendario previo
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        # Encabezado del mes
        month_name = calendar.month_name[self.current_month]
        self.header.config(text=f"{month_name} {self.current_year}")

        # Nombres de los días
        days = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
        for col, day in enumerate(days):
            tk.Label(self.calendar_frame, text=day, font=("Helvetica", 10, "bold"), padx=10, pady=5).grid(row=0, column=col)

        # Días del mes
        month_days = calendar.monthcalendar(self.current_year, self.current_month)
        for row, week in enumerate(month_days, start=1):
            for col, day in enumerate(week):
                if day == 0:
                    # Día vacío
                    label = tk.Label(self.calendar_frame, text="", width=5, height=2)
                else:
                    date = date_format(str(day), self.current_month, self.current_year)
                    
                    if date in self.datos:
                        # Día trabajado → Label verde con check
                        label = tk.Label(
                            self.calendar_frame,
                            text=str(day) + " ✔",
                            width=10,
                            height=2,
                            bg="lightgreen",
                            fg="black",
                            font=("Helvetica", 12, "bold")
                        )
                        # Para hacer clic en un día trabajado, podemos usar bind
                        label.bind("<Button-1>", lambda e, d=str(date): self.consultar_horas(d))
                    else:
                        # Día sin horas → botón normal
                        label = tk.Button(
                            self.calendar_frame,
                            text=str(day),
                            width=5,
                            height=2,
                            command=lambda d=str(day): self.increment_hours(d)
                        )

                label.grid(row=row, column=col, padx=2, pady=2)


    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.draw_calendar()

    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.draw_calendar()

    def increment_hours(self, day):
        popup = tk.Toplevel(self.root)
        popup.title("Registrar horas")
        
        date = date_format(day=day, month=self.current_month, year=self.current_year)

        label = tk.Label(popup, text = f'Horas trabajadas el dia {date}')
        label.pack(padx=20, pady=20)

        entry = tk.Entry(popup)
        entry.pack(pady=5)

        def save_hours():
            horas = entry.get()
            if not horas.isdigit():
                tkm.showerror("Error", "Formato incorrecto, se esperaba un número como entrada")
                return
            
            horas = int(horas)

            self.datos[date] = horas
            with open(data_path, "w") as f:
                json.dump(self.datos, f, indent=4)

            self.total_hours=sum(self.datos.values())
            self.string_hours=f'Total acumulado {self.total_hours}h'
            self.total_label.config(text=self.string_hours)
            self.draw_calendar()

            popup.destroy()

        save_button = tk.Button(popup, text='Guardar', command=save_hours)
        save_button.pack(pady=5)
    
    def consultar_horas(self, date):
        hours = self.datos[date]

        popup = tk.Toplevel(self.root) 
        popup.title(f'Horas trabajadas el {date}')

        # Mostrar las horas en un label o text
        label = tk.Label(popup, text=f'Las horas trabajadas el día {date} fueron: {hours}')
        label.pack(pady=20, padx=20)

if __name__ == "__main__":
    data_path = 'hours.json'
    if not os.path.exists(data_path):  
        with open(data_path, "w") as f:
            json.dump({}, f)
    root = tk.Tk()
    app = CalendarApp(root, data_path=data_path)
    root.mainloop()
