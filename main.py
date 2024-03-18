import Tree as util
import os
from PIL import Image

resA = None
resB = []

dataset_path = "dataset"
tree = util.AVLTree()

"""for root, dirs, files in os.walk(dataset_path):
    for file in files:
        ruta_archivo = os.path.join(root, file)
        nombre, extension = os.path.splitext(file)
        size = os.path.getsize(ruta_archivo)
        if "carsgraz_" in nombre:
            type = "Cars"
        elif "bike_" in nombre:
            type = "Bike"
        elif "cat." in nombre:
            type = "Cats"
        elif "dog." in nombre:
            type = "Dogs"
        elif "horse-" in nombre:
            type = "Horses"
        elif "rider-" in nombre:
            type = "Human"
        else:
            type = "Flowers"
        tree.insert_node(nombre, type, size, ruta_archivo, "white")"""

def insertar_nodo_1():
    title = input("Ingrese el título del archivo: ")
    found_node = tree.search_node(title)
    if found_node:
        print("Ya existe un nodo con esta metrica!")
    else:
        type = input("Ingrese la categoría a la que corresponde esta imagen: ")
        image_path = input("Ingrese la dirección del archivo: ")
        size = os.path.getsize(image_path)
        tree.insert_node(title, type, size, image_path,"green")
        print("El nodo fue insertado exitosamente!")
        tree.generar_imagen()
        tree.abrir_imagen()
        found_node = tree.search_node(title)
        found_node.color = "white"

def eliminar_nodo_2():
    title_to_delete = str(input("Ingrese el titulo del nodo a eliminar: "))
    print(f"buscando nodo....")
    found_node = tree.search_node(title_to_delete)
    if found_node:
        tree.delete_node(title_to_delete)
        print("El nodo fue eliminado exitosamente!")
        tree.generar_imagen()
        tree.abrir_imagen()
    else:
        print("No fue encontrado ningún nodo con este titulo")

def buscar_nodo_3():
    titulo = input("Ingrese el título del nodo a buscar ")
    found_node = tree.search_node(titulo)
    if found_node:
        print("El nodo fue encontrado exitosamente!")
        found_node.color = "yellow"
        tree.generar_imagen()
        tree.abrir_imagen()
        found_node.color = "white"
        return found_node
    else:
        print("No fue encontrado ningún nodo con esta metrica!")

def buscar_nodos_4():
    type = input("¿A qué categoría deben pertenecer los nodos? ")
    rango_inf = int(input("¿Cuál es el tamaño minimo de bytes que deben tener los nodos? "))
    rango_sup = float(input("¿Cuál es el tamaño máximo de bytes que deben tener los nodos? "))
    print(f"Buscando nodos pertenecientes a {type}, con un tamaño de bytes entre {rango_inf} y {rango_sup}:")
    result = tree.search_nodes_by_criteria(type, rango_inf, rango_sup)
    if result:
        resB.clear()
        for nodo in result:
            resB.append(nodo)
            nodo.color = "yellow"
        tree.generar_imagen()
        tree.abrir_imagen()
        for nodo in result:
            nodo.color = "white"
    else:
        print("No se encontraron nodos con el criterio elegido!")

def recorrer_por_niveles_5():
    resultados_por_niveles = tree.recorrido_por_niveles()
    if resultados_por_niveles:
        print("Recorrido por niveles del árbol:")
        for nivel, nodos in enumerate(resultados_por_niveles, start=1):
            print(f"Nivel {nivel-1}:")
            for nodo in nodos:
                print(f"    Título: {nodo.title}")

def mostrar_informacion_6(nodos):
    if nodos:
        while True:
            print("Nodos disponibles:")
            for nodo in nodos:
                print(f"- {nodo.title}")
            titulo = input("Por favor elige un nodo de la lista: ")
            for nodo in nodos:
                if nodo.title == titulo:
                    target = nodo
            if target is None:
                print("Elegiste un nodo invalido!")
            else:
                print("El nodo fue seleccionado correctamente!")
                acceder_menu_2(target)
                break
    else:
        print("Primero use las opciones 3 o 4")

def acceder_menu_2(nodo):
    while True:
        mostrar_menu_2()
        opcion2 = input("Selecciona una opción: ")
        if opcion2 == "1":
            print(f"El nivel del nodo es: {tree.get_node_level(nodo)}")
        elif opcion2 == "2":
            print(f"El factor de balanceo del nodo es: {tree.balance_factor(nodo)}")
        elif opcion2 == "3":
            padre = tree.find_parent(nodo)
            if padre is not None:
                nodo.color = "gray"
                padre.color = "yellow"
                tree.generar_imagen()
                tree.abrir_imagen()
                nodo.color = "white"
                padre.color = "white"
            else:
                print("El nodo seleccionado no tiene nodo padre")
        elif opcion2 == "4":
            abuelo = tree.find_grandparent(nodo)
            if abuelo is not None:
                nodo.color = "gray"
                abuelo.color = "yellow"
                tree.generar_imagen()
                tree.abrir_imagen()
                nodo.color = "white"
                abuelo.color = "white"
            else:
                print("El nodo seleccionado no tiene nodo abuelo")
        elif opcion2 == "5":
            tio = tree.find_uncle(nodo)
            if tio is not None:
                nodo.color = "gray"
                tio.color = "yellow"
                tree.generar_imagen()
                tree.abrir_imagen()
                nodo.color = "white"
                tio.color = "white"
            else:
                print("El nodo seleccionado no tiene nodo tio")
        elif opcion2 == "6":
            img = Image.open(nodo.image_path)
            img.show()
            break
        elif opcion2 == "7":
            break
        else:
            print("Opción no válida. Por favor, elige una opción válida.")


def mostrar_menu():
    print("===========[ARBOL AVL]===========")
    print("1. Insertar nodo")
    print("2. Eliminar nodo utilizando métrica")
    print("3. Buscar nodo utilizando métrica")
    print("4. Buscar nodos siguiendo criterio")
    print("5. Mostrar recorrido por niveles")
    print("6. Mostrar información de un nodo")
    print("7. Mostrar árbol")
    print("8. Salir")
    print("=================================")

def mostrar_menu_2():
    print("===========[INFORMACIÓN NODO]===========")
    print("1. Obtener nivel del nodo")
    print("2. Obtener factor de balanceo del nodo")
    print("3. Encontrar padre del nodo")
    print("4. Encontrar el abuelo del nodo")
    print("5. Encontrar el tío del nodo")
    print("6. Mostrar imagen del nodo")
    print("7. Atrás")
    print("=================================")

# Bucle principal del programa
while True:
    mostrar_menu()
    opcion = input("Selecciona una opción: ")
    if opcion == "1":
        insertar_nodo_1()
    elif opcion == "2":
        eliminar_nodo_2()
    elif opcion == "3":
        resA = buscar_nodo_3()
    elif opcion == "4":
        buscar_nodos_4()
    elif opcion == "5":
        recorrer_por_niveles_5()
    elif opcion == "6":
        nodos = []
        if resA is not None:
            nodos.append(resA)
        if resB:
            for no in resB:
                nodos.append(no)
        mostrar_informacion_6(nodos)
    elif opcion == '7':
        if tree.root is not None:
            tree.generar_imagen()
            tree.abrir_imagen()
        else:
            print("Por favor ingrese algun nodo!")
    elif opcion == '8':
        print("Hasta luego!!!!")
        break
    else:
        print("Opción no válida. Por favor, elige una opción válida.")