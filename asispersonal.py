import pyttsx3
import datetime
import tkinter as tk
from tkinter import ttk
from twilio.rest import Client
import threading
import requests
import json
import os
import gpt_2_simple as gpt2
import requests
import smtplib


# Inicializar el motor Text-to-Speech
engine = pyttsx3.init()

# Función para que el asistente hable
def speak(text):
    engine.say(text)
    engine.runAndWait()
# Configuración de Twilio (reemplaza con tus credenciales)
account_sid = 'AC5961c8aab7539a8252665cbdc3592352'
auth_token = '5f3b223ba917c80f31989e335c68c9a5'
client = Client(account_sid, auth_token)

# Función para enviar un mensaje de notificación por SMS a través de Twilio
 #def send_twilio_message(body):
    #client = Client(account_sid, auth_token)
    #message = client.messages.create(
       # body=body,
        #from_='+14786067866',
       # to='+18299701690'
    #)
    # print(f"Mensaje Twilio enviado. SID: {message.sid}")#   

# Función para agregar tareas
def add_task(tasks, task):
    tasks.append((task, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Pendiente"))
    save_tasks(tasks)  # Guardar las tareas en el archivo
    speak(f"Tarea agregada: {task}")
    show_tasks()

# Enviar mensaje de notificación por SMS
    #message_body = f"Nueva tarea agregada: {task}"
   # send_twilio_message(message_body)
    
# Configurar tu número de teléfono para recibir el mensaje (reemplaza con tu número)
#twilio_to_number = '+18299701690'  # Tu número de teléfono

#configuracion de las alerta 
#def check_pending_tasks():
    #while True:
        
        #pending_tasks = [task for task, _, status in tasks if status == "Pendiente"]
        
        #if pending_tasks:
          
          #  message_body = f"Tareas pendientes: {', '.join(pending_tasks)}"
           
           # send_twilio_message(message_body)
        # Esperar 150 segundos antes de volver a verificar
        #threading.Timer(150, check_pending_tasks).start()

# Agrega esta línea al final del código para iniciar el temporizador
#threading.Timer(150, check_pending_tasks).start()
    
# Función para mostrar las tareas pendientes en la tabla
def show_tasks():
    for item in treeview.get_children():
        treeview.delete(item)

    for task, date, status in tasks:
        color = "red" if status == "Pendiente" else "green"
        treeview.insert("", tk.END, values=(task, date, status), tags=(status, ))
    
# Función para cambiar el estado de una tarea
def toggle_status():
    selected_item = treeview.selection()
    if selected_item:
        task, date, status = treeview.item(selected_item)['values']
        new_status = "Completada" if status == "Pendiente" else "Pendiente"
        tasks[treeview.index(selected_item)] = (task, date, new_status)
        save_tasks(tasks)
        show_tasks()
        
# Función para enviar el correo con las tareas pendientes y completadas
def send_email(subject, body):
    # Configurar el servidor SMTP (para Gmail)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "personalvirtualasistente@gmail.com"  # Reemplaza con tu dirección de correo
    receiver_email = "robertico959@gmail.com"  # Reemplaza con la dirección de correo del destinatario
    sender_password = "10Monin10."  # Reemplaza con tu contraseña de correo

    # Crear conexión segura con el servidor SMTP
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)

    # Crear el mensaje del correo
    message = f"Subject: {subject}\n\n{body}"

    # Enviar el correo
    server.sendmail(sender_email, receiver_email, message)

    # Cerrar la conexión con el servidor SMTP
    server.quit()

# Función para eliminar una tarea seleccionada
def delete_task():
    selected_item = treeview.selection()
    if selected_item:
        tasks.pop(treeview.index(selected_item))
        save_tasks(tasks)
        show_tasks()

# Función para guardar las tareas en el archivo
def save_tasks(tasks):
    with open("tasks.txt", "w") as file:
        for task, date, status in tasks:
            file.write(f"{task}|{date}|{status}\n")

# Función para cargar las tareas desde el archivo
def load_tasks():
    tasks = []
    try:
        with open("tasks.txt", "r") as file:
            for line in file:
                parts = line.strip().split("|")
                if len(parts) == 3:
                    task, date, status = parts
                elif len(parts) == 2:
                    task, date = parts
                    status = "Pendiente"
                tasks.append((task, date, status))
    except FileNotFoundError:
        pass
    return tasks

# Función para manejar el botón "Agregar tarea"
def add_task_button_handler():
    task = entry_task.get()
    if task:
        add_task(tasks, task)
        entry_task.delete(0, tk.END)

# Función para manejar el botón "Mostrar tareas"
def show_tasks_button_handler():
    frame_table.pack()
    show_tasks()

# Función para manejar el botón "Ocultar tareas"
def hide_tasks_button_handler():
    frame_table.pack_forget()

# Crear la ventana principal
root = tk.Tk()
root.title("Asistente Personal")

# Cargar las tareas desde el archivo
tasks = load_tasks()

# Frame para los botones "Agregar tarea", "Mostrar tareas" y "Salir"
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

label = tk.Label(frame_buttons, text="Asistente Personal", font=("Arial", 16))
label.pack(pady=10)

entry_task = tk.Entry(frame_buttons, font=("Arial", 12))
entry_task.pack(pady=5)

btn_add_task = tk.Button(frame_buttons, text="Agregar tarea", font=("Arial", 12), command=add_task_button_handler)
btn_add_task.pack(side=tk.LEFT, padx=5)

btn_show_tasks = tk.Button(frame_buttons, text="Mostrar tareas", font=("Arial", 12), command=show_tasks_button_handler)
btn_show_tasks.pack(side=tk.LEFT, padx=5)

btn_exit = tk.Button(frame_buttons, text="Salir", font=("Arial", 12), command=root.quit)
btn_exit.pack(side=tk.LEFT, padx=5)

# Frame para la tabla y botones de "Eliminar Tarea", "Cambiar Estado" y "Ocultar Tareas"
frame_table = tk.Frame(root)

columns = ("Tarea", "Fecha de Creación", "Estado de Progreso")
treeview = ttk.Treeview(frame_table, columns=columns, show="headings", selectmode="browse")

treeview.heading("Tarea", text="Tarea")
treeview.heading("Fecha de Creación", text="Fecha de Creación")
treeview.heading("Estado de Progreso", text="Estado de Progreso")

treeview.tag_configure("Pendiente", foreground="red")
treeview.tag_configure("Completada", foreground="green")

treeview.pack(pady=10)

# Botón para cambiar el estado de una tarea
btn_toggle_status = tk.Button(frame_table, text="Cambiar Estado", font=("Arial", 12), command=toggle_status)
btn_toggle_status.pack(pady=5)

# Botón para eliminar una tarea
btn_delete_task = tk.Button(frame_table, text="Eliminar Tarea", font=("Arial", 12), command=delete_task)
btn_delete_task.pack(pady=5)

# Botón para ocultar la tabla de tareas
btn_hide_tasks = tk.Button(frame_table, text="Ocultar Tareas", font=("Arial", 12), command=hide_tasks_button_handler)
btn_hide_tasks.pack(pady=5)

# Iniciar mostrando solo el frame con los botones "Agregar tarea", "Mostrar tareas" y "Salir"
frame_buttons.pack()


#segunda interfaz

# Función para enviar la pregunta al asistente y recibir la respuesta

assistant_window = None  # Variable global para la ventana del asistente

def open_assistant_interface():
    global assistant_window
    root.withdraw()  # Ocultar la ventana principal
    assistant_window = tk.Toplevel(root)
    assistant_window.title("Asistente")

    # Variables globales para que las funciones puedan acceder a ellas
    global entry_question, text_response
    entry_question = None
    text_response = None
    

    label_question = tk.Label(assistant_window, text="Escribe tu pregunta:")
    label_question.pack(pady=10)

    entry_question = tk.Entry(assistant_window, font=("Arial", 12))
    entry_question.pack(pady=5)

    btn_ask = tk.Button(assistant_window, text="Preguntar", font=("Arial", 12), command=ask_assistant)
    btn_ask.pack(pady=5)

    text_response = tk.Text(assistant_window, font=("Arial", 12), wrap=tk.WORD, state=tk.DISABLED, height=10)
    text_response.pack(pady=10)

    btn_close = tk.Button(assistant_window, text="Volver al Inicio", font=("Arial", 12), command=back_to_home)
    btn_close.pack(pady=5)
    
def back_to_home():
    global assistant_window
    root.deiconify()  # Volver a mostrar la ventana principal
    assistant_window.destroy()

#funcion de api chagpt 
def respond_with_gpt2(question):
    sess = gpt2.start_tf_sess()
    gpt2.load_gpt2(sess)
    response = gpt2.generate(sess, run_name='run1', prefix=question, length=100, temperature=0.7, return_as_list=True)
    return response[0]

# Función para interactuar con el asistente
def ask_assistant():
    question = entry_question.get()  # Obtener la pregunta del usuario
    if question:
        # Responder usando GPT-2
        answer = respond_with_gpt2(question)
        # Mostrar la respuesta del asistente en el cuadro de texto
        text_response.config(state=tk.NORMAL)
        text_response.delete(1.0, tk.END)
        text_response.insert(tk.END, answer)
        text_response.config(state=tk.DISABLED)



# Botón "Asistente" para abrir la interfaz del asistente
btn_open_assistant = tk.Button(frame_buttons, text="Asistente", font=("Arial", 12), command=open_assistant_interface)
btn_open_assistant.pack(side=tk.LEFT, padx=5)

# Iniciar el bucle de eventos de la interfaz gráfica
root.mainloop()
