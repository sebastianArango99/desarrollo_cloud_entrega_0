import flet as ft
from flet import TextField, ElevatedButton, Page, Column, Text, TextButton, Page
import requests
API_URL = "http://backend:4000/"  
import json
import flet as ft
from flet import TextField, ElevatedButton, Page, Column, Row, TextButton, UserControl
import pandas as pd
#import flet_fastapi



def navigate_to_sign_up(page: Page, event):
    # Clear the current view
    page.controls.clear()
    # Add the sign-up form
    add_sign_up_form(page)
    page.update()

def navigate_to_sign_in(page: Page, event):
    # Clear the current view
    page.controls.clear()
    # Add the sign-in form
    add_sign_in_form(page)
    page.update()

def navigate_to_menu_principal(page: Page, event):
    # Clear the current view
    page.controls.clear()
    # Add the sign-in form
    add_sign_in_form(page)
    page.update()

def add_sign_in_form(page: Page):
    username_tf = TextField(label="Usuario", autofocus=True)
    password_tf = TextField(label="Contraseña", password=True)
    sign_in_btn = sign_in_btn = ElevatedButton("Sign in", on_click=lambda e: sign_in( username_tf, password_tf, page))
    sign_up_link = TextButton("Sign up", on_click=lambda e: navigate_to_sign_up(page, e))
    
    page.add(Column([username_tf, password_tf, sign_in_btn, sign_up_link], alignment="center"))
def pick_files(e):
    file_picker = ft.FilePicker()  # Create an instance of FilePicker
    file_picker.pick_files(allow_multiple=False)  # Call the method on the instance


def add_sign_up_form(page: Page):
    username_tf = TextField(label="Usuario")
    password_tf = TextField(label="Contraseña", password=True)

    file_picker = ft.FilePicker()
 

    # Add the file picker to the page
    page.add(file_picker)

    foto_perfil=ft.ElevatedButton("Selecciona Foto Perfil (opcional)",
    on_click=lambda _: file_picker.pick_files(allow_multiple=False))
    
    upload_list=[]
    if file_picker.result != None and file_picker.result.files != None:
        for f in file_picker.result.files:
            upload_list.append(
                ft.FilePickerUploadFile(
                    f.name,
                    upload_url=page.get_upload_url(f.name, 600),
                )
            )
        file_picker.upload(upload_list)

    sign_up_btn = ElevatedButton("Sign up", on_click=lambda e: sign_up(username_tf, password_tf, foto_perfil, page))
    sign_in_link = TextButton("Sign in", on_click=lambda e: navigate_to_sign_in(page, e))
    
    page.add(Column([username_tf, password_tf, foto_perfil, sign_up_btn, sign_in_link], alignment="center"))

def create_post_login_view(page: Page, token: str, usuario_id: int):
    page.controls.clear()  # Clear the current view
    
    welcome_message = Text(f"Bienvenido!")
    categorias= ElevatedButton("Categorías")#,on_click=lambda e: navigate_to_sign_in(page, e))
    tareas= ElevatedButton("Tareas", on_click=lambda e: pagina_tareas(page,token, usuario_id))
    logout_button = ElevatedButton("Logout", on_click=lambda e: navigate_to_sign_in(page, e))
    #fetch_categories_btn = TextButton("Fetch Categories")
    #fetch_categories_btn.on_click = lambda e: page.add(ft.Text(get_categories(usuario_id, token)))  # Replace ListView with the appropriate component for displaying categories
    
    page.add(Column([welcome_message, categorias,tareas, logout_button], alignment="center"))
    page.update()

def pagina_tareas(page: Page, token: str, usuario_id: int):
    page.controls.clear()  # Clear the current view
    
    welcome_message = Text(f"Bienvenido a tus tareas!")
    ver_tareas= ElevatedButton("Ver tareas", on_click=lambda e: pagina_ver_tareas(page,token, usuario_id))
    pagina_nueva_tarea
    agregar_tareas=ElevatedButton("Agregar tareas", on_click=lambda e: pagina_nueva_tarea(page, token, usuario_id))
    modificar_tareas= ElevatedButton("Modificar tareas")#, on_click=lambda e: navigate_to_sign_in(page, e))
    eliminar_tareas= ElevatedButton("Eliminar tareas")#, on_click=lambda e: navigate_to_sign_in(page, e))
    menu_principal = ElevatedButton("Menu Principal", on_click=lambda e: create_post_login_view(page,token,usuario_id))
    #fetch_categories_btn = TextButton("Fetch Categories")
    #fetch_categories_btn.on_click = lambda e: page.add(ft.Text(get_categories(usuario_id, token)))  # Replace ListView with the appropriate component for displaying categories
    
    # First column
    first_column = Column(
        controls=[welcome_message, ver_tareas, agregar_tareas, modificar_tareas, eliminar_tareas, menu_principal],
        alignment="start"
    )

    # Add the row to the page
    page.add(first_column)

    page.update()
def main(page: Page):
    page.title = "Gestion de Tareas"
    page.vertical_alignment = "center"
    # Initially load the sign-in form
    add_sign_in_form(page)

import requests  # Assuming synchronous operation is acceptable in your scenario

def sign_in(username_tf: TextField, password_tf: TextField, page: Page):
    API_URL = "http://backend:8080/sign-in"  # Adjust to your actual endpoint
    try:
        response = requests.post(API_URL, json={"username": username_tf.value, "password": password_tf.value})
        if response.status_code == 200:
            data = response.content.decode('utf-8')
            parsed_data=json.loads(data)
            token= parsed_data['token']  # Adjust based on how the token is returned
            usuario_id= parsed_data['usuario_id']
            print(response)
            create_post_login_view(page, token,usuario_id)  # Redirect to the post-login view
        else:
            dlg=ft.AlertDialog(
                title=ft.Text("Usuario y/o contraseña incorrecto"), on_dismiss=lambda e: print(username_tf.value, password_tf.value, response)
            )
            page.dialog = dlg
            dlg.open = True
            page.update()


            

    except Exception as e:
        # Handle errors
        print(f"An error occurred: {str(e)}")
        print(response.content)


def sign_up( username: str, password: str, profile_image:str, page: Page):
    API_URL = "http://127.0.0.1:8000/sign-up"  # Update to your actual endpoint
    try:
        response = requests.post(API_URL, json={"username": username.value, "password": password.value, "profile_image": profile_image.value})
        if response.status_code == 200:
            # Handle successful login, such as storing the token for future requests
            #ft.MessageBox.show(page, "Login successful!", title="Success")
            dlg=ft.AlertDialog(
                title=ft.Text("Usuario creado correctamente"), on_dismiss=lambda e: print(username.value, password.value)
            )
            page.dialog = dlg
            dlg.open = True
            page.update()

            navigate_to_sign_in(page, None)
        else:
            print('not ok')
            #ft.MessageBox.show(page, "Login failed!", title="Error")
    except Exception as e:
        print(username.value)
        print(password.value)
        #ft.MessageBox.show(page, f"An error occurred: {str(e)}", title="Error")

def tareas_usuario(usuario_id: int, token: str):
    # Replace with your actual API call to /get_categories
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(f'http://127.0.0.1:8000/tareas/usuario/{usuario_id}', headers=headers)

    return response.json()

def nueva_tarea(usuario_id: int, token:str, titulo: str, due_date: str, category_id: int):
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response= requests.post("http://127.0.0.1:8000/tareas", json={
            "text": titulo,
            "due_date": due_date,
            "category_id": category_id,
            "status": 'NOT_STARTED'
        }, headers=headers)

    return response.json()


def pagina_ver_tareas(page:Page, token: str,usuario_id:int):
    page.controls.clear()
    welcome_message = Text(f"Visualizador de Tareas")
    resp=tareas_usuario(usuario_id,token)
    resp_text=ft.Text(resp)
    menu_principal = ElevatedButton("Atrás", on_click=lambda e: pagina_tareas(page,token,usuario_id))
    json_data=resp
    columns = [
        ft.DataColumn(label=ft.Text("ID")),
        ft.DataColumn(label=ft.Text("Descripción")),
        ft.DataColumn(label=ft.Text("Fecha fin")),
        ft.DataColumn(label=ft.Text("Categoría")),
        ft.DataColumn(label=ft.Text("Fecha Creación")),
        ft.DataColumn(label=ft.Text("Status")),
    ]

    
    rows = []
    for item in json_data:
        cells = [
            ft.DataCell(ft.Text(str(item["id"]))),
            ft.DataCell(ft.Text(item["text"])),
            ft.DataCell(ft.Text(item["due_date"])),
            ft.DataCell(ft.Text(item["category_id"])),
            ft.DataCell(ft.Text(item["creation_date"])),
            ft.DataCell(ft.Text(item.get("status", "N/A")))
        ]
        rows.append(ft.DataRow(cells=cells))

    # Create the DataTable widget with the columns and rows
    data_table = ft.DataTable(columns=columns, rows=rows)

    # First column
    first_column = Column(
        controls=[welcome_message, data_table, menu_principal],
        alignment="start"
    )

    # Add the row to the page
    page.add(first_column)

    page.update()

def pagina_nueva_tarea(page: Page, token, usuario_id):
        # Call FastAPI backend to add the task
    page.controls.clear()
    welcome_message = Text(f"Nueva Tarea:")
    nombre=TextField(label="Descripción", width=200)
    fecha_entrega=ft.DatePicker()
    category_id=TextField(label="Categoría", width=200)
    agregar = ElevatedButton("Agregar Tarea", on_click=lambda e: nueva_tarea(usuario_id, token, nombre.value, fecha_entrega.value, category_id.value))
    menu_principal = ElevatedButton("Atrás", on_click=lambda e: pagina_tareas(page,token,usuario_id))

    page.add(Column([welcome_message, nombre,fecha_entrega, category_id, agregar, menu_principal], alignment="center"))
    page.update()


    
ft.app(target=main,view=ft.AppView.WEB_BROWSER)
