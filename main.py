import os

if os.path.exists(r"Agenda.txt"):
    archivo_original = open("Agenda.txt",'r')
    with open("Respaldo.txt", 'w') as archivo_respaldo:
        cadena = archivo_original.read()
        archivo_respaldo.write(cadena)
else:
    archivo_original = open("Agenda.txt",'w')
    archivo_respaldo = open("Respaldo.txt",'w')
    print("Se creo la Agenda")
archivo_original.close()
archivo_respaldo.close()

while True:

    archivo_original = open("Agenda.txt", 'a')
    archivo_respaldo = open("Respaldo.txt", 'r')

    print("AGENDA V2")
    print("1)Ingresar alumno")
    print("2)Buscar alumno")
    print("0)Salir")
    opcion = int(input("Ingresar opcion < "))

    if opcion == 1:
        nombre = input("Ingresa el nombre: ")
        codigo = input("Ingrese el codigo: ")
        carrera = input("Ingresa la carrera: ")
        cadena = archivo_respaldo.read()
        archivo_original.write("Nombre: " + nombre + " |" + 
                               "Codigo: " + codigo + " |" + 
                               "Carrera: " + carrera + "\n")

    elif opcion == 2:
        alumno = input("Ingresa el nombre o codigo del alumno a buscar: ")
        encontrado = False
        for linea in archivo_respaldo:
            if alumno in linea:
                print("Alumno encontrado:")
                nombre, codigo, carrera = [elemento.strip().split(': ')[1] 
                                           for elemento in linea.split('|')]
                if alumno == nombre:
                    print("Codigo: " + codigo + " |" + "Carrera: " + carrera)
                elif alumno == codigo:
                    print("Nombre: " + nombre + " |" + "Carrera: " + carrera)
                encontrado = True

        if not encontrado:
            print(f"No se encontró al alumno con el nombre o codigo {alumno}")
            print("Desea añadirlo?")
            opcion = int(input('1)Si 2)No : '))

            if opcion == 1:
                nombre = input("Ingresa el nombre: ")
                codigo = input("Ingrese el codigo: ")
                carrera = input("Ingresa la carrera: ")
                cadena = archivo_respaldo.read()
                archivo_original.write("Nombre: " + nombre + " |" + "Codigo: " + codigo 
                                       + " |" + "Carrera: " + carrera + "\n") 
        
        else:
            print("Que desea hacer")
            print("1)Editar 2)Eliminar 3)Nada")
            opcion = int(input("Ingrese la opcion : "))
            
            if opcion == 1:
                print("Que desea editar")
                print("1)Nombre 2)Codigo 3)Carrera")
                opcion = int(input("Ingrese la opcion : "))
                
                if opcion == 1:
                    nuevo_nombre = input("Ingresa el nuevo nombre: ")
                    cadena = ("Nombre: " + nuevo_nombre + " |" + "Codigo: " 
                              + codigo + " |" + "Carrera: " + carrera + "\n")
                
                elif opcion == 2:
                    nuevo_codigo = input("Ingresa el nuevo codigo: ")
                    cadena = ("Nombre: " + nombre + " |" + "Codigo: " 
                              + nuevo_codigo + " |" + "Carrera: " + carrera + "\n")
                
                elif opcion == 3:
                    nueva_carrera = input("Ingrese la nueva carrera: ")
                    cadena = ("Nombre: " + nombre + " |" + "Codigo: " + 
                               codigo + " |" + "Carrera: " + nueva_carrera + "\n")

                with open("Agenda.txt", 'r') as archivo_temp:
                    lineas = archivo_temp.readlines()
                
                with open("Agenda.txt", 'w') as archivo_temp:
                    for linea in lineas:
                        if alumno not in linea:
                            archivo_temp.write(linea)
                        else:
                            archivo_temp.write(cadena)

            elif opcion == 2:
                with open("Agenda.txt", 'r') as archivo_temp:
                    lineas = archivo_temp.readlines()

                with open("Agenda.txt", 'w') as archivo_temp:
                    for linea in lineas:
                        if alumno not in linea:
                            archivo_temp.write(linea)
            elif opcion == 3:
                print("Regresando al menu")
    elif opcion == 0:
        break

    archivo_original.close()
    archivo_respaldo.close()