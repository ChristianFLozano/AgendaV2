from prefect import flow, task
import os

# Tarea para inicializar archivos
@task
def inicializar_archivos():
    if os.path.exists("Agenda.txt"):
        with open("Agenda.txt", 'r') as archivo_original, open("Respaldo.txt", 'w') as archivo_respaldo:
            cadena = archivo_original.read()
            archivo_respaldo.write(cadena)
    else:
        with open("Agenda.txt", 'w') as archivo_original, open("Respaldo.txt", 'w') as archivo_respaldo:
            print("Se creó la Agenda")

# Función para hacer un respaldo antes de realizar cambios
@task
def respaldar():
    if os.path.exists("Agenda.txt"):
        with open("Agenda.txt", 'r') as archivo_original, open("Respaldo.txt", 'w') as archivo_respaldo:
            archivo_respaldo.write(archivo_original.read())
    else:
        print("No hay nada que respaldar, el archivo de agenda no existe aún.")

# Tarea para ingresar un alumno
@task
def ingresar_alumno(nombre, codigo, carrera):
    respaldar()  
    with open("Agenda.txt", 'a') as archivo_original:
        archivo_original.write(f"Nombre: {nombre} | Codigo: {codigo} | Carrera: {carrera}\n")

# Tarea para buscar un alumno
@task
def buscar_alumno(alumno):
    encontrado = False
    with open("Agenda.txt", 'r') as archivo_original: 
        for linea in archivo_original:
            if alumno in linea:
                print("Alumno encontrado:")
                nombre, codigo, carrera = [elemento.strip().split(': ')[1] for elemento in linea.split('|')]
                if alumno == nombre or alumno == codigo:
                    print(f"Nombre: {nombre} | Codigo: {codigo} | Carrera: {carrera}")
                    encontrado = True
                    return (nombre, codigo, carrera)
    return None

# Tarea para editar o eliminar un alumno
@task
def modificar_alumno(alumno, nombre=None, codigo=None, carrera=None, eliminar=False):
    respaldar() 
    with open("Agenda.txt", 'r') as archivo_temp:
        lineas = archivo_temp.readlines()
    
    with open("Agenda.txt", 'w') as archivo_temp:
        for linea in lineas:
            if alumno not in linea:
                archivo_temp.write(linea)
            elif eliminar:
                continue  
            else:
                partes = linea.split('|')
                nuevo_nombre = nombre or partes[0].split(': ')[1].strip()
                nuevo_codigo = codigo or partes[1].split(': ')[1].strip()
                nueva_carrera = carrera or partes[2].split(': ')[1].strip()
                cadena = f"Nombre: {nuevo_nombre} | Codigo: {nuevo_codigo} | Carrera: {nueva_carrera}\n"
                archivo_temp.write(cadena)

# Flujo principal
@flow
def agenda_flow():
    inicializar_archivos()

    while True:
        print("AGENDA V2")
        print("1) Ingresar alumno")
        print("2) Buscar alumno")
        print("0) Salir")
        opcion = int(input("Ingresar opción < "))

        if opcion == 1:
            nombre = input("Ingresa el nombre: ")
            codigo = input("Ingresa el codigo: ")
            carrera = input("Ingresa la carrera: ")
            ingresar_alumno(nombre, codigo, carrera)

        elif opcion == 2:
            alumno = input("Ingresa el nombre o código del alumno a buscar: ")
            alumno_encontrado = buscar_alumno(alumno)

            if alumno_encontrado:
                print("¿Qué desea hacer?")
                print("1) Editar 2) Eliminar 3) Nada")
                opcion = int(input("Ingrese la opción: "))
                
                if opcion == 1:
                    print("¿Qué desea editar?")
                    print("1) Nombre 2) Código 3) Carrera")
                    editar_opcion = int(input("Ingrese la opción: "))
                    
                    if editar_opcion == 1:
                        nuevo_nombre = input("Ingresa el nuevo nombre: ")
                        modificar_alumno(alumno, nombre=nuevo_nombre)
                    
                    elif editar_opcion == 2:
                        nuevo_codigo = input("Ingresa el nuevo código: ")
                        modificar_alumno(alumno, codigo=nuevo_codigo)
                    
                    elif editar_opcion == 3:
                        nueva_carrera = input("Ingresa la nueva carrera: ")
                        modificar_alumno(alumno, carrera=nueva_carrera)

                elif opcion == 2:
                    modificar_alumno(alumno, eliminar=True)
                    print(f"Alumno {alumno} eliminado correctamente.")

            else:
                print(f"No se encontró al alumno con el nombre o código {alumno}")
                print("¿Desea añadirlo?")
                opcion = int(input('1) Sí 2) No: '))

                if opcion == 1:
                    nombre = input("Ingresa el nombre: ")
                    codigo = input("Ingresa el código: ")
                    carrera = input("Ingresa la carrera: ")
                    ingresar_alumno(nombre, codigo, carrera)
        
        elif opcion == 0:
            break

# Ejecutar el flujo
if __name__ == "__main__":
    agenda_flow()
