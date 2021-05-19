from tkinter import ttk
from tkinter import *
import cassandra


from cassandra.cluster import Cluster

cluster = Cluster(['127.0.0.1'])




class Product:

    def __init__(self, window):
        self.wind = window
        self.wind.title('Aplicacion Productos')

        #Crear un contenedor

        frame = LabelFrame(self.wind, text='Busca el producto que desee')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)#GRID -> Lugar en el que se pone el recuadro anterior

        #Nombre de entrada
        Label(frame, text = 'Nombre: ').grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row = 1, column = 1)

        #Precio de entrada

        #Label(frame, text = 'Precio: ').grid(row = 2, column = 0)
        #self.price = Entry(frame)
        #self.price.grid(row = 2, column = 1)

        #Boton para añadir productos

        ttk.Button(frame, text = 'Buscar', command = self.search_product).grid(row = 3, columnspan = 2, sticky = W + E)


        #Tabla
        self.tree = ttk.Treeview(height = 10, columns = 2)
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'Productos', anchor = CENTER)
        self.tree.heading('#1', text = 'Precio', anchor = CENTER)

        self.get_producto()
        #if self.search_product():
        #    self.search_product()
        #self.search_product()

    #def run_query(self, query, parameters = ()):
    #    session = cluster.connect()
    #    session.set_keyspace("db")
    #    result = session.execute(query, parameters)
    #    print(result)
    #    return result


    def get_producto(self):
        records = self.tree.get_children()
        for element in records: #Obtenemos la tabla actual y eliminamos todos los datos que ya contiene para poder obtenerlos de nuevo en la consulta que realizemos
            self.tree.delete(element)
        #Consultamos los datos de la tabla
        session = cluster.connect()
        session.set_keyspace("db")
        #session.execute
        #query = 'SELECT * from productos'
        db_rows = session.execute('SELECT * from productos')
        for row in db_rows:
            self.tree.insert('', 0, text = row[1], values = row[2])


    def validation(self):
        #Comparamos la longitud del nombre con 0 , si es cero no queremos insertar
        return len(self.name.get()) != 0 #nd len(self.price.get()) != 0  



    def search_product(self):
        records = self.tree.get_children()
        for element in records: #Obtenemos la tabla actual y eliminamos todos los datos que ya contiene para poder obtenerlos de nuevo en la consulta que realizemos
            self.tree.delete(element)
        if self.validation:
            data = self.name.get() + '%'
            session = cluster.connect()
            session.set_keyspace("db")
            print(data)
            rows_busca = session.execute("SELECT * from productos where name LIKE %(data)s", {"data":(data)})
            print (rows_busca)
            for row in rows_busca:
                print(row)
                self.tree.insert('', 0, text = row[1], values = row[2])
            #query = 'SELECT * from productos where name = "?"'
            #parameters = (self.name.get())#, self.price.get())
            #self.run_query(query, parameters)
            #print(query)
        else:
            print('Nombre y el precio son necesarios')

if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()
