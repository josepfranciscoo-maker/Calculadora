# Joseph Almachi 3RO B 
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField


# Clase Principal que hereda de Screen - es la pantalla principal de la calculadora
class Principal(Screen):
    # Constructor de la clase - se ejecuta al crear la pantalla
    def __init__(self, **kwargs):
        # Llamar al constructor de la clase padre (Screen)
        super().__init__(**kwargs)

        # Crear layout principal con orientación vertical (widgets uno debajo del otro)
        layout_principal = BoxLayout(
            orientation='vertical',  # Orientación vertical
            padding=20,              # Márgenes de 20 píxeles
            spacing=15               # Espacio de 15 píxeles entre widgets
        )

        # Crear campo de texto para mostrar los números y resultados
        self.display = MDTextField(
            hint_text="000",         # Texto de sugerencia que muestra "0"
            readonly=True,          # Solo lectura - el usuario no puede escribir directamente
            font_size=100,           # Tamaño de fuente grande (40)
            halign="right",        # Alineación del texto a la derecha
            size_hint_y=None,       # No usar tamaño automático en altura
            height=80,              # Altura fija de 80 píxeles
            mode="rectangle"       # Estilo rectangular del campo
        )

        # Crear layout de cuadrícula para organizar los botones
        layout_botones = GridLayout(
            cols=4,                 # 4 columnas en la cuadrícula
            spacing=10,             # Espacio de 10 píxeles entre botones
            size_hint_y=1           # Ocupar todo el espacio vertical disponible
        )

        # Lista de tuplas con (texto del botón, color) para cada botón
        botones = [
            ('C', 'red'), ('/', 'orange'), ('*', 'orange'), ('-', 'orange'),  # Fila 1: Limpiar, division, multiplicacion, resta
            ('7', 'blue'), ('8', 'blue'), ('9', 'blue'), ('+', 'orange'),    # Fila 2: 7, 8, 9, suma
            ('4', 'blue'), ('5', 'blue'), ('6', 'blue'), ('%', 'purple'),    # Fila 3: 4, 5, 6, porcentaje
            ('1', 'blue'), ('2', 'blue'), ('3', 'blue'), ('=', 'green'),    # Fila 4: 1, 2, 3, igual
            ('0', 'blue'), ('.', 'blue'), ('', 'gray'), ('', 'gray')         # Fila 5: 0, punto, vacios para espaciado
        ]

        # Recorrer cada tupla de la lista de botones
        for texto, color in botones:
            if texto:  # Solo crear botones si tienen texto (ignorar los vacíos)
                # Crear botón con estilo Material Design
                btn = MDRaisedButton(
                    text=texto,                                    # Texto del botón
                    font_size=30,                                  # Tamaño de fuente
                    md_bg_color=self.get_color(color),            # Color de fondo usando función auxiliar
                    on_press=lambda x, t=texto: self.boton_presionado(t)  # Al presionar, llamar a boton_presionado
                )
                # Añadir el botón al layout de cuadrícula
                layout_botones.add_widget(btn)

        # Añadir el display (campo de texto) al layout principal
        layout_principal.add_widget(self.display)
        # Añadir el layout de botones al layout principal
        layout_principal.add_widget(layout_botones)

        # Añadir el layout principal a la pantalla
        self.add_widget(layout_principal)

        # Inicializar variables para el estado de la calculadora
        self.numero_actual = ""      # Número que se está escribiendo actualmente
        self.operacion = None         # Operación pendiente (+, -, *, /)
        self.numero_anterior = ""    # Primer número antes de la operación
        self.nuevo_numero = True      # Bandera: True si se debe empezar un nuevo número

    # Función auxiliar para obtener el color RGB de un nombre de color
    def get_color(self, color_nombre):
        # Diccionario con nombres de colores y sus valores RGBA (Rojo, Verde, Azul, Alpha)
        colores = {
            'red': (1, 0, 0, 1),          # Rojo puro
            'orange': (1, 0.5, 0, 1),     # Naranja
            'blue': (0, 0.5, 1, 1),       # Azul
            'green': (0, 1, 0, 1),        # Verde
            'purple': (0.5, 0, 0.5, 1),   # Púrpura
            'gray': (0.5, 0.5, 0.5, 1)    # Gris
        }
        # Retornar el color si existe, sino retornar gris por defecto
        return colores.get(color_nombre, (0.5, 0.5, 0.5, 1))

    # Función que se ejecuta cuando se presiona cualquier botón
    def boton_presionado(self, texto):
        # Si el texto es un dígito (0-9)
        if texto.isdigit():
            if self.nuevo_numero:  # Si se debe empezar un nuevo número
                self.numero_actual = texto      # El número actual es solo el dígito presionado
                self.nuevo_numero = False       # Ya no es un nuevo número
            else:  # Si se continúa escribiendo el número actual
                self.numero_actual += texto     # Concatenar el dígito al número actual
            self.display.text = self.numero_actual  # Mostrar en el display

        # Si se presiona el punto decimal
        elif texto == '.':
            # Solo permitir un punto decimal por número
            if '.' not in self.numero_actual:
                if self.nuevo_numero:  # Si se debe empezar un nuevo número
                    self.numero_actual = "0."    # Empezar con "0."
                    self.nuevo_numero = False     # Ya no es un nuevo número
                else:  # Si se continúa escribiendo el número actual
                    self.numero_actual += "."    # Agregar punto al número actual
                self.display.text = self.numero_actual  # Mostrar en el display

        # Si se presiona el porcentaje
        elif texto == '%':
            if self.numero_actual:  # Si hay un número actual
                try:  # Intentar calcular el porcentaje
                    num = float(self.numero_actual)  # Convertir a número decimal
                    resultado = num / 100              # Dividir entre 100 para obtener porcentaje
                    # Si el resultado es entero, mostrar sin decimales
                    if resultado == int(resultado):
                        self.display.text = str(int(resultado))
                    else:  # Si tiene decimales, redondear a 6 decimales
                        self.display.text = str(round(resultado, 6))
                    self.numero_actual = self.display.text  # Guardar el resultado
                    self.nuevo_numero = True              # Indicar que es un nuevo número
                except:  # Si hay error en el cálculo
                    self.display.text = "Error"           # Mostrar error
                    self.numero_actual = ""               # Limpiar número actual
                    self.nuevo_numero = True               # Indicar que es un nuevo número

        # Si se presiona C (Clear - Limpiar)
        elif texto == 'C':
            self.numero_actual = ""      # Limpiar número actual
            self.numero_anterior = ""    # Limpiar número anterior
            self.operacion = None         # Limpiar operación
            self.nuevo_numero = True      # Indicar que es un nuevo número
            self.display.text = "0"       # Mostrar 0 en el display

        # Si se presiona una operación (+, -, *, /)
        elif texto in ['+', '-', '*', '/']:
            if self.numero_actual:  # Si hay un número actual
                self.numero_anterior = self.numero_actual  # Guardar como número anterior
                self.numero_actual = ""                   # Limpiar número actual
                self.operacion = texto                      # Guardar la operación
                self.nuevo_numero = True                   # Indicar que es un nuevo número

        # Si se presiona igual (=) para calcular el resultado
        elif texto == '=':
            # Verificar que haya operación, número anterior y número actual
            if self.operacion and self.numero_anterior and self.numero_actual:
                try:  # Intentar realizar el cálculo
                    num1 = float(self.numero_anterior)  # Convertir primer número a decimal
                    num2 = float(self.numero_actual)    # Convertir segundo número a decimal
                    
                    # Realizar la operación correspondiente
                    if self.operacion == '+':
                        resultado = num1 + num2           # Suma
                    elif self.operacion == '-':
                        resultado = num1 - num2           # Resta
                    elif self.operacion == '*':
                        resultado = num1 * num2           # Multiplicación
                    elif self.operacion == '/':
                        if num2 != 0:                    # Verificar que no sea división por cero
                            resultado = num1 / num2       # División
                        else:
                            resultado = "Error"           # Error si divide entre cero
                    
                    # Mostrar el resultado en el display
                    if isinstance(resultado, str):  # Si el resultado es un string (Error)
                        self.display.text = resultado
                    else:  # Si el resultado es un número
                        # Si el resultado es entero, mostrar sin decimales
                        if resultado == int(resultado):
                            self.display.text = str(int(resultado))
                        else:  # Si tiene decimales, redondear a 6 decimales
                            self.display.text = str(round(resultado, 6))
                    
                    # Actualizar variables después del cálculo
                    self.numero_actual = self.display.text  # Guardar resultado como número actual
                    self.numero_anterior = ""               # Limpiar número anterior
                    self.operacion = None                    # Limpiar operación
                    self.nuevo_numero = True                 # Indicar que es un nuevo número
                    
                except Exception as e:  # Si hay algún error en el cálculo
                    self.display.text = "Error"              # Mostrar error
                    self.numero_actual = ""                  # Limpiar número actual
                    self.numero_anterior = ""                # Limpiar número anterior
                    self.operacion = None                     # Limpiar operación
                    self.nuevo_numero = True                  # Indicar que es un nuevo número


# Clase MiApp que hereda de MDApp - es la aplicación principal
class MiApp(MDApp):
    # Método build - construye la interfaz de la aplicación
    def build(self):
        SC = ScreenManager()                        # Crear gestor de pantallas
        SC.add_widget(Principal(name='principal'))  # Añadir pantalla Principal con nombre 'principal'
        self.theme_cls.theme_style = 'Dark'         # Establecer tema oscuro
        self.theme_cls.primary_palette = 'Blue'      # Establecer paleta de colores azul
        return SC                                    # Retornar el ScreenManager


# Si este archivo se ejecuta directamente (no importado)
if __name__ == '__main__':
    MiApp().run()  # Crear instancia de MiApp y ejecutarla
