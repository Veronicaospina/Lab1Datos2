import pygraphviz as pgv
from scour import scour
import webbrowser


class Node:
    def __init__(self, title, type, size, image_path, color):
        self.title = title
        self.type = type
        self.size = size
        self.image_path = image_path
        self.metric = title #métrica con la que se construye el árbol AVL
        self.left = None
        self.right = None
        self.height = 1
        self.color = color #Para identificar los nodos con los que se está trabajando


class AVLTree:
    def __init__(self):
        self.root = None

    def height(self, node):
        if node is None:
            return 0
        return node.height

    def balance_factor(self, node):
        if node is None:
            return 0
        return self.height(node.left) - self.height(node.right)

    def update_height(self, node):
        if node is not None:
            node.height = 1 + max(self.height(node.left), self.height(node.right))

    def rotate_left(self, z):
        if z is None or z.right is None:
            return z
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        self.update_height(z)
        self.update_height(y)

        return y

    def rotate_right(self, y):
        if y is None or y.left is None:
            return y
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        self.update_height(y)
        self.update_height(x)

        return x

    def insert(self, root, title, type, size, image_path, color):
        if root is None:
            return Node(title, type, size, image_path, color)

        if title < root.metric:
            root.left = self.insert(root.left, title, type, size, image_path, color)
        else:
            root.right = self.insert(root.right, title, type, size, image_path, color)

        self.update_height(root)

        balance = self.balance_factor(root)

        if balance > 1:
            if title < root.left.metric:
                return self.rotate_right(root)
            else:
                root.left = self.rotate_left(root.left)
                return self.rotate_right(root)

        if balance < -1:
            if title > root.right.metric:
                return self.rotate_left(root)
            else:
                root.right = self.rotate_right(root.right)
                return self.rotate_left(root)

        return root

    def insert_node(self, title, type, size, image_path, color='lightblue'):
        self.root = self.insert(self.root, title, type, size, image_path, color)

    def delete(self, root, title):
        if root is None:
            return root

        if title < root.metric:
            root.left = self.delete(root.left, title)
        elif title > root.metric:
            root.right = self.delete(root.right, title)
        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp
            temp = self.get_min_value_node(root.right)
            root.title, root.metric = temp.title, temp.metric
            root.right = self.delete(root.right, temp.title)

        self.update_height(root)

        balance = self.balance_factor(root)

        if balance > 1:
            if self.balance_factor(root.left) >= 0:
                return self.rotate_right(root)
            else:
                root.left = self.rotate_left(root.left)
                return self.rotate_right(root)

        if balance < -1:
            if self.balance_factor(root.right) <= 0:
                return self.rotate_left(root)
            else:
                root.right = self.rotate_right(root.right)
                return self.rotate_left(root)
        return root

    def delete_node(self, title):
        self.root = self.delete(self.root, title)

    def get_min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def search_node(self, title):
        current = self.root

        while current is not None:
            current_metric = current.title

            if title == current_metric:
                return current
            elif title < current_metric:
                current = current.left
            else:
                current = current.right

        return None

    def search_nodes_by_criteria(self, type, rango_inf, rango_sup):
        result = []
        resultados_por_niveles = self.recorrido_por_niveles()
        if resultados_por_niveles:
            for nivel, nodos in enumerate(resultados_por_niveles, start=1):
                for nodo in nodos:
                    if nodo.type.lower() == type.lower() and nodo.size >= rango_inf and nodo.size < rango_sup:
                        result.append(nodo)
        return result

    def recorrido_por_niveles(self):
        if self.root is None:
            return []

        resultados_por_niveles = []  # Lista para almacenar los resultados por nivel

        # Función auxiliar para realizar el recorrido por niveles de manera recursiva
        def recorrer_nivel(nodos):
            if not nodos:
                return

            nuevos_nodos = []  # Lista para almacenar los nodos del siguiente nivel
            nivel_actual = []  # Lista para almacenar los nodos del nivel actual

            for nodo in nodos:
                nivel_actual.append(nodo[0])  # Agregar el nodo actual al nivel actual
                # Agregar los hijos al nivel siguiente junto con su nivel incrementado en 1
                if nodo[0].left:
                    nuevos_nodos.append((nodo[0].left, nodo[1] + 1))
                if nodo[0].right:
                    nuevos_nodos.append((nodo[0].right, nodo[1] + 1))

            resultados_por_niveles.append(nivel_actual)  # Agregar el nivel actual a los resultados
            recorrer_nivel(nuevos_nodos)  # Llamada recursiva con los nodos del nivel siguiente

        # Comenzar el recorrido por niveles desde la raíz (nivel 0)
        recorrer_nivel([(self.root, 1)])

        return resultados_por_niveles

    def abrir_imagen(self):
        optimize_svg("temp_tree.svg", "temp_tree_optimized.svg")
        webbrowser.open("index.html")

    def generar_imagen(self):
        if self.root:
            dot = pgv.AGraph(directed=True)

            def add_nodes_edges(node):
                if node is not None:
                    label = node.title
                    dot.add_node(node.title, label=label, fillcolor=node.color, style="filled")
                    if node.left:
                        dot.add_edge(node.title, node.left.title)
                        add_nodes_edges(node.left)
                    if node.right:
                        dot.add_edge(node.title, node.right.title)
                        add_nodes_edges(node.right)

            add_nodes_edges(self.root)
            dot.layout(prog='dot')
            dot.draw("temp_tree.svg", format="svg")

    def get_node_level(self, node):
        return self._get_node_level_recursive(self.root, node.metric, 0)

    def _get_node_level_recursive(self, node, metric_value, current_level):
        if metric_value == node.metric:
            return current_level
        elif metric_value < node.metric:
            return self._get_node_level_recursive(node.left, metric_value, current_level + 1)
        else:
            return self._get_node_level_recursive(node.right, metric_value, current_level + 1)

    def find_parent(self, node):
        if self.root is node:
            return None

        return self._find_parent_recursive(None, self.root, node.metric)

    def _find_parent_recursive(self, parent, current_node, metric_value):
        if metric_value == current_node.metric:
            return parent

        if metric_value < current_node.metric:
            return self._find_parent_recursive(current_node, current_node.left, metric_value)
        else:
            return self._find_parent_recursive(current_node, current_node.right, metric_value)

    def find_grandparent(self, node):
        if self.root is None:
            return None

        parent = self.find_parent(node)

        if parent is None:
            return None

        grandparent = self.find_parent(parent)

        return grandparent

    def find_uncle(self, node):
        if self.root is None:
            return None

        # Encuentra el nodo padre del nodo dado usando el método anterior.
        parent = self.find_parent(node)

        if parent is None:
            return None  # No se encontró el nodo padre.

        # Verifica si el nodo padre es el hijo izquierdo o derecho del abuelo.
        grandparent = self.find_parent(parent)
        if grandparent is None:
            return None  # No se encontró el nodo abuelo.

        if grandparent.left is not None and grandparent.left.metric == parent.metric:
            uncle = grandparent.right
        else:
            uncle = grandparent.left

        return uncle


def optimize_svg(input_file, output_file):
    options = scour.parse_args(['--enable-id-stripping', '--enable-comment-stripping', '--enable-viewboxing',
                                '--shorten-ids', '--indent=none', '--quiet',
                                '--remove-metadata', '--strip-xml-prolog', '-i', input_file, '-o', output_file])
    (input, output) = scour.getInOut(options)
    scour.start(options, input, output)
