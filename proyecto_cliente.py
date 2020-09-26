from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import psycopg2
from tkcalendar import Calendar
from datetime import datetime, timedelta


class ConexionBaseDeDatos():

    def __init__(self,ruta):
        self.ruta = ruta

    def __enter__(self):
        self.conexion = psycopg2.connect(self.ruta)
        return self.conexion.cursor()

    def __exit__(self,exc_class,exc,traceback):
        self.conexion.commit()
        self.conexion.close()

#--------------------- funcion decoradora  -----------------------------------------------------------------------
def ejecutarSentenciaSQL(consulta,*valores):
    def decoradorConsulta(funcion):
        def funcionDecorada(*valores):
            ruta = "user=bdi2019p password=bdi2019p host=plop.inf.udec.cl dbname=bdi2019p port=5432"
            with ConexionBaseDeDatos(ruta) as sentencia:
                sentencia.execute(consulta,*valores)
                listaDatos = sentencia.fetchall()
            return listaDatos
        return funcionDecorada
    return decoradorConsulta


class Ventana_principal(object):

    def __init__(self, parent):
        self.principal = parent
        self.principal.title("CINEDB")
        self.principal.resizable(0, 0)
        self.principal.geometry("800x500")
        self.principal.config(bg = "dimgray")

        self.frame = Frame(self.principal, width = "600", height = "300", bg = 'Black')
        self.frame.place(x = 100, y = 100)
        self.label = Label(self.frame, text = "Bienvenido a CINEDB", justify = 'center', bg = 'Black', fg = "goldenrod", font = ("Bookman Old Style", 20)).place(x = 150, y = 100, width = "300", height = "150")
        self.boton = Button(self.principal, text = "Star", command = self.openFrame).place(x = 390, y = 450, width = "50", height = "30")

    def hide(self):
        self.principal.withdraw()

    def openFrame(self):
        self.hide()
        subFrame = Ventana_dos(self)

    def show(self):
        self.principal.update()
        self.principal.deiconify()


class Ventana_dos(Toplevel):

    def __init__(self, wind):
        self.wind = wind
        Toplevel.__init__(self)
        self.title("Opciones")
        self.resizable(0, 0)
        self.geometry("800x500")
        self.config(bg = 'dimgray')

        self.frame = Frame(self, width = "600", height = "400", bg = 'Black')
        self.frame.pack()
        self.frame.place(x = 100, y = 50)

        self.boton1 = Button(self.frame, text = 'PELICULA', command = self.boton_pelicula)
        self.boton1.place(x = 250, y = 130, width = 100, height = 50)
        self.boton2 = Button(self.frame, text = 'CINE', command = self.boton_cine)
        self.boton2.place(x = 250, y = 200, width = 100, height = 50)

        self.botonVolver = Button(self, text = 'atrás', command = self.volverAtras)
        self.botonVolver.place(x = 10, y = 10, width = 40, height = 20)

    def hide(self):
        self.withdraw()

    def boton_pelicula(self):
        self.hide()
        subFrame = Peliculas(self)

    def boton_cine(self):
        self.hide()
        subFrame = Cines(self)

    def volverAtras(self):
        self.destroy()
        self.wind.show()

    def show(self):
        self.update()
        self.deiconify()


class Peliculas(Toplevel):
    def __init__(self, wind):
        self.wind = wind
        Toplevel.__init__(self)
        self.title("CONFIGURACION PELICULAS")
        self.resizable(0, 0)
        self.geometry("800x500")
        self.config(bg='dimgray')

        self.var = IntVar()
        self.ingresar = Label(self, text = 'INGRESAR', bg = 'darkmagenta').place(x = 130, y = 50, width = 300, height = 30)
        self.ingresar_pelicula = Radiobutton(self, text = 'Ingresar película', variable = self.var, value = 1)
        self.ingresar_pelicula.place(x = 200, y = 100, width = 180)
        self.ingresar_funcion = Radiobutton(self, text = 'Ingresar función', variable = self.var, value = 2)
        self.ingresar_funcion.place(x = 200, y = 130, width = 180)

        self.actualizar = Label(self, text = 'ACTUALIZAR', bg = 'darkmagenta').place(x = 130, y = 200, width = 300, height = 30)
        self.actualizar_pelicula = Radiobutton(self, text = 'Actualizar película', variable = self.var, value = 3)
        self.actualizar_pelicula.place(x = 200, y = 250, width = 180)
        self.actualizar_funcion = Radiobutton(self, text = 'Actualizar función', variable = self.var, value = 4)
        self.actualizar_funcion.place(x = 200, y = 280, width = 180)

        self.eliminar = Label(self, text = 'ELIMINAR', bg = 'darkmagenta').place(x = 130, y = 350, width = 300, height = 30)
        self.eliminar_pelicula = Radiobutton(self, text = 'Eliminar película', variable = self.var, value = 5)
        self.eliminar_pelicula.place(x = 200, y = 400, width = 180)
        self.eliminar_funcion = Radiobutton(self, text = 'Eliminar función', variable = self.var, value = 6)
        self.eliminar_funcion.place(x = 200, y = 430, width = 180)

        self.ok_1 = Button(self, text = 'OK', command = self.openFrame).place(x = 410, y = 100, width = 100, height = 50)
        self.ok_2 = Button(self, text = 'OK', command = self.openFrame).place(x = 410, y = 250, width = 100, height = 50)
        self.ok_3 = Button(self, text = 'OK', command = self.openFrame).place(x = 410, y = 400, width = 100, height = 50)

        self.botonVolver = Button(self, text = 'atrás', command = self.volverAtras)
        self.botonVolver.place(x = 10, y = 10, width = 40, height = 20)

    def show(self):
        self.update()
        self.deiconify()

    def volverAtras(self):
        self.destroy()
        self.wind.show()

    def hide(self):
        self.withdraw()

    def openFrame(self):
        self.hide()
        self.num = self.var.get()
        if self.num == 1:
            subFrame = Ingresar_pel(self)
        elif self.num == 2:
            subFrame = Ingresar_fun(self)
        elif self.num == 3:
            subFrame = Actualizar_pel(self)
        elif self.num == 4:
            subFrame = Actualizar_fun(self)
        elif self.num == 5:
            subFrame = Eliminar_pel(self)
        elif self.num == 6:
            subFrame = Eliminar_fun(self)


class Cines(Toplevel):
    def __init__(self, wind):
        self.wind = wind
        Toplevel.__init__(self)
        self.title("CONFIGURACION CINES")
        self.resizable(0, 0)
        self.geometry("800x500")
        self.config(bg = 'dimgray')

        self.boton_ingresar = Button(self, text = "Ingresar cine", command = self.ingresar_cine)
        self.boton_ingresar.place(x = 350, y = 100, width = 150, height = 50)

        self.boton_actualizar = Button(self, text = "Actualizar cine", command = self.actualizar_cine)
        self.boton_actualizar.place(x = 350, y = 200, width = 150, height = 50)

        self.boton_eliminar = Button(self, text = "Eliminar cine", command = self.eliminar_cine)
        self.boton_eliminar.place(x = 350, y = 300, width = 150, height = 50)

        self.botonVolver = Button(self, text = 'atrás', command = self.volverAtras)
        self.botonVolver.place(x = 10, y = 10, width = 40, height = 20)

    def hide(self):
        self.withdraw()

    def ingresar_cine(self):
        self.hide()
        subFrame = Ingresar_cine(self)

    def actualizar_cine(self):
        self.hide()
        subFrame = Actualizar_cine(self)

    def eliminar_cine(self):
        self.hide()
        subFrame = Eliminar_cine(self)

    def show(self):
        self.update()
        self.deiconify()

    def volverAtras(self):
        self.destroy()
        self.wind.show()


class Ingresar_cine(Toplevel):
    def __init__(self, wind):
        self.wind = wind
        Toplevel.__init__(self)
        self.dsnBaseDatos = "user=bdi2019p password=bdi2019p host=plop.inf.udec.cl dbname=bdi2019p port=5432"

        self.title("Ingresar cine")
        self.resizable(0, 0)
        self.geometry("800x500")
        self.config(bg = 'dimgray')

        self.nombre_region = StringVar()
        self.nombre_ciudad = StringVar()
        self.codigo_postal = IntVar()
        self.sector_direccion = StringVar()
        self.calle_direccion = StringVar()
        self.numero_direccion = IntVar()
        self.nombre_cine = StringVar()
        self.cadena_cine = "CineDB"

        self.region = Label(self, text = "Region: ", bg = "pink").place(x = 20, y = 60, width = 130)
        self.entry_reg = Entry(self)
        self.entry_reg.place(x = 160, y = 60, width = 530)

        self.boton_ok = Button(self, text = "Ok", state = 'normal', command = self.mostrar_ciudad)
        self.boton_ok.place(x = 700, y = 60)

        self.boton_ingresar = Button(self, text = "Ingresar", state = 'disabled', command = self.ingresar_BD_cines)
        self.boton_ingresar.place(x = 300, y = 450)

        self.botonVolver = Button(self, text = 'atrás', command = self.volverAtras)
        self.botonVolver.place(x = 10, y = 10, width = 40, height = 20)

    def mostrar_mensaje_error(self):
        #CAMBIAR NOMBRE
        messagebox.showwarning(message = "Por favor, ingrese texto faltante.", title = "Texto vacío")

    def error_cine(self):
        messagebox.showwarning(message = "Esta ciudad ya tiene un cine.", title = "Ciudad ya existe")

    def mostrar_ciudad(self):
        self.nombre_region = self.entry_reg.get()
        if self.nombre_region == "":
            self.mostrar_mensaje_error()
        else:
            self.ciudad = Label(self, text = "Ciudad: ", bg = "pink").place(x = 20, y = 100, width = 130)
            self.entry_ciu = Entry(self)
            self.entry_ciu.place(x = 160, y = 100, width = 160)

            self.boton_ok = Button(self, text = "Ok", state = 'normal', command = self.mostrar_codigo)
            self.boton_ok.place(x = 330, y = 100)

    def mostrar_codigo(self):
        self.nombre_ciudad = self.entry_ciu.get()
        if self.nombre_ciudad == "":
            self.mostrar_mensaje_error()
        else:
            with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
                SQL = "SELECT nombre_ciudad FROM ps.ciudadyregion WHERE nombre_ciudad = (%s)"
                data = (self.nombre_ciudad,)
                sentencia.execute(SQL, data)
                self.nom_ciu = sentencia.fetchone()
            if self.nom_ciu:
                if self.nombre_ciudad == self.nom_ciu[0]:
                    self.error_cine()
            else:
                self.codigo = Label(self, text = "Codigo postal: ", bg = "pink", wraplength = 70).place(x = 390, y = 100, width = 130)
                self.entry_cod = Entry(self)
                self.entry_cod.place(x = 530, y = 100, width = 160)

                self.boton_ok = Button(self, text = "Ok", state = 'normal', command = self.mostrar_direccion)
                self.boton_ok.place(x = 700, y = 100)

    def mostrar_direccion(self):
        self.codigo_postal = self.entry_cod.get()
        if self.codigo_postal == "":
            self.mostrar_mensaje_error()
        else:  
            self.direccion = Label(self, text = "Direccion", bg = "skyblue").place(x = 20, y = 160, width = 130, height = 50)

            self.sector = Label(self, text = "Sector: ", bg = "pink").place(x = 20, y = 240, width = 130)
            self.entry_sec = Entry(self)
            self.entry_sec.place(x = 160, y = 240, width = 530)

            self.calle = Label(self, text = "Calle: ", bg = "pink").place(x = 20, y = 300, width = 130)
            self.entry_calle = Entry(self)
            self.entry_calle.place(x = 160, y = 300, width = 220)

            self.numero = Label(self, text = "Numero: ", bg = "pink").place(x = 390, y = 300, width = 130)
            self.entry_num = Entry(self)
            self.entry_num.place(x = 530, y = 300, width = 160)

            self.boton_ok = Button(self, text = "Ok", state = 'normal', command = self.comprobar_datos)
            self.boton_ok.place(x = 700, y = 270)

    def comprobar_datos(self):
        self.sector_direccion = self.entry_sec.get()
        self.calle_direccion = self.entry_calle.get()
        self.numero_direccion = self.entry_num.get()

        if self.sector_direccion == "" or self.calle_direccion == "" or self.numero_direccion == "":
            self.mostrar_error_direccion()
        if self.sector_direccion != "" and self.calle_direccion != "" and self.numero_direccion != "":
            self.boton_ingresar.config(state = 'normal')

        self.nombre_cine = self.cadena_cine + "_" + self.nombre_ciudad

    def mostrar_error_direccion(self):
        self.mens = messagebox.askyesno(message="Ha dejado espacios vacíos en dirección. ¿Desea continuar?", title="Dirección")
        if self.mens:
            self.boton_ingresar.config(state = 'normal')
        else:
            self.boton_ingresar.config(state = 'disabled')

    def volverAtras(self):
        self.destroy()
        self.wind.show()

    def ingresar_salas(self):
        with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
            for i in range(1, 5):
                SQL = "INSERT INTO ps.sala (numero_sala, tipo_sala, cantidad_asientos, nombre_cine) VALUES (%s, %s, %s, %s)"
                data = (i, '2D', 208, self.nombre_cine,)
                sentencia.execute(SQL, data)
            for i in range(5, 7):
                SQL = "INSERT INTO ps.sala (numero_sala, tipo_sala, cantidad_asientos, nombre_cine) VALUES (%s, %s, %s, %s)"
                data = (i, '3D', 150, self.nombre_cine,)
                sentencia.execute(SQL, data)
            for i in range(7, 9):
                SQL = "INSERT INTO ps.sala (numero_sala, tipo_sala, cantidad_asientos, nombre_cine) VALUES (%s, %s, %s, %s)"
                data = (i, '4D', 96, self.nombre_cine,)
                sentencia.execute(SQL, data)
            for i in range(9, 11):
                SQL = "INSERT INTO ps.sala (numero_sala, tipo_sala, cantidad_asientos, nombre_cine) VALUES (%s, %s, %s, %s)"
                data = (i, 'XD', 288, self.nombre_cine,)
                sentencia.execute(SQL, data)

    def ingresar_asientos(self):
        with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
            letras_2D = ['A','B','C','D','E','F','G','H','I','J','K','L','M']
            letras_3D = ['A','B','C','D','E','F','G','H','I','J']
            letras_4D = ['A','B','C','D','E','F','G','H']
            letras_XD = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P']
            
            for i in range(1, 5):
                for j in letras_2D:
                    for k in range(1, 17):
                        num_asiento_2D = j + '-' + str(k)
                        SQL = "INSERT INTO ps.asiento (numero_asiento, numero_sala, nombre_cine) VALUES (%s, %s, %s)"
                        data = (num_asiento_2D, i, self.nombre_cine,)
                        sentencia.execute(SQL, data)
                    
            for i in range(5, 7):
                for j in letras_3D:
                    for k in range(1, 16):
                        num_asiento_3D = j + '-' + str(k)
                        SQL = "INSERT INTO ps.asiento (numero_asiento, numero_sala, nombre_cine) VALUES (%s, %s, %s)"
                        data = (num_asiento_3D, i, self.nombre_cine,)
                        sentencia.execute(SQL, data)
        
            for i in range(7, 9):
                for j in letras_4D:
                    for k in range(1, 13):
                        num_asiento_4D = j + '-' + str(k)
                        SQL = "INSERT INTO ps.asiento (numero_asiento, numero_sala, nombre_cine) VALUES (%s, %s, %s)"
                        data = (num_asiento_4D, i, self.nombre_cine,)
                        sentencia.execute(SQL, data)
        
            for i in range(9, 11):
                for j in letras_XD:
                    for k in range(1, 19):
                        num_asiento_XD = j + '-' + str(k)
                        SQL = "INSERT INTO ps.asiento (numero_asiento, numero_sala, nombre_cine) VALUES (%s, %s, %s)"
                        data = (num_asiento_XD, i, self.nombre_cine,)
                        sentencia.execute(SQL, data)
        


    def ingresar_BD_cines(self):

        with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
            SQL1 = "INSERT INTO ps.ciudadyregion (nombre_ciudad, region) VALUES (%s, %s)"
            data1 = (self.nombre_ciudad, self.nombre_region,)
            sentencia.execute(SQL1, data1)

            SQL2 = "INSERT INTO ps.ciudad (codigo_postal, nombre_ciudad) VALUES (%s, %s)"
            data2 = (self.codigo_postal, self.nombre_ciudad,)
            sentencia.execute(SQL2, data2)

            SQL3 = "INSERT INTO ps.cine (nombre_cine, sector, calle, numero, cadena_cine, codigo_postal) VALUES (%s, %s, %s, %s, %s, %s)"
            data3 = (self.nombre_cine, self.sector_direccion, self.calle_direccion, self.numero_direccion, self.cadena_cine, self.codigo_postal,)
            sentencia.execute(SQL3, data3)

        self.ingresar_salas()
        self.ingresar_asientos()
        self.volverAtras()


class Actualizar_cine(Toplevel):
    def __init__(self, wind):
        self.wind = wind
        Toplevel.__init__(self)
        self.dsnBaseDatos = "user=bdi2019p password=bdi2019p host=plop.inf.udec.cl dbname=bdi2019p port=5432"

        self.title("Actualizar cine")
        self.resizable(0, 0)
        self.geometry("800x500")
        self.config(bg='dimgray')

        self.nombre_region = StringVar()
        self.nombre_ciudad = StringVar()
        self.codigo_postal = IntVar()
        self.sector_direccion = StringVar()
        self.calle_direccion = StringVar()
        self.numero_direccion = IntVar()

        self.region = Label(self, text = "Region: ", bg = "pink").place(x = 20, y = 60, width = 130)
        self.lista_reg = ttk.Combobox(self, state = 'readonly')

        with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
            SQL1 = "SELECT region FROM ps.ciudadyregion"
            sentencia.execute(SQL1)
            self.regiones = sentencia.fetchall()

        self.lista_reg["values"] = self.regiones
        self.lista_reg.place(x = 160, y = 60, width = 530)

        self.boton_actualizar = Button(self, text = "Actualizar", state = 'disabled', command = self.actualizar_BD_cines)
        self.boton_actualizar.place(x = 300, y = 450)

        self.botonVolver = Button(self, text = 'atrás', command = self.volverAtras)
        self.botonVolver.place(x = 10, y = 10, width = 40, height = 20)

        self.boton_ok = Button(self, text = "Ok", state = 'normal', command = self.mostrar_ciudad)
        self.boton_ok.place(x = 700, y = 60)

    def mostrar_mensaje_error(self):
        #CAMBIAR NOMBRE
        messagebox.showwarning(message = "Por favor, ingrese texto faltante.", title="Texto vacío")

    def mostrar_ciudad(self):
        self.nombre_region = self.lista_reg.get()
        if self.nombre_region == "":
            self.mostrar_mensaje_error()
        else:
            self.ciudad = Label(self, text = "Ciudad: ", bg = "pink").place(x = 20, y = 100, width = 130)
            self.lista_ciu = ttk.Combobox(self, state = 'readonly')

            with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
                SQL2 = "SELECT nombre_ciudad FROM ps.ciudadyregion WHERE region = (%s)"
                data2 = (self.nombre_region,)
                sentencia.execute(SQL2, data2)
                self.ciudades = sentencia.fetchall()

            self.lista_ciu["values"] = self.ciudades
            self.lista_ciu.place(x = 160, y = 100, width = 160)

            self.boton_ok = Button(self, text = "Ok", state = 'normal', command = self.mostrar_direccion)
            self.boton_ok.place(x = 330, y = 100)

    def mostrar_direccion(self):
        self.nombre_ciudad = self.lista_ciu.get()
        if self.nombre_ciudad == "":
            self.mostrar_mensaje_error()
        else:
            with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
                SQL3 = "SELECT codigo_postal FROM ps.ciudad WHERE nombre_ciudad = (%s)"
                data3 = (self.nombre_ciudad,)
                sentencia.execute(SQL3, data3)
                self.codigo = sentencia.fetchone()

            self.codigo_postal = self.codigo[0]    
            self.direccion = Label(self, text = "Direccion", bg = "skyblue").place(x = 20, y = 160, width = 130, height = 50)
            self.sector = Label(self, text = "Sector: ", bg = "pink").place(x = 20, y = 240, width = 130)
            self.lista_sec = ttk.Combobox(self)

            with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
                SQL4 = "SELECT sector FROM ps.cine WHERE codigo_postal = (%s)"
                data4 = (self.codigo_postal,)
                sentencia.execute(SQL4, data4)
                self.sector1 = sentencia.fetchall()

            self.lista_sec["values"] = self.sector1
            self.lista_sec.place(x = 160, y = 240, width = 530)

            self.calle = Label(self, text = "Calle: ", bg = "pink").place(x = 20, y = 300, width = 130)
            self.lista_calle = ttk.Combobox(self)

            with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
                SQL5 = "SELECT calle FROM ps.cine WHERE codigo_postal = (%s)"
                data5 = (self.codigo_postal,)
                sentencia.execute(SQL5, data5)
                self.calle1 = sentencia.fetchall()

            self.lista_calle["values"] = self.calle1
            self.lista_calle.place(x = 160, y = 300, width = 220)

            self.numero = Label(self, text = "Numero: ", bg = "pink").place(x = 390, y = 300, width = 130)
            self.lista_num = ttk.Combobox(self)

            with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
                SQL6 = "SELECT numero_calle FROM ps.cine WHERE codigo_postal = (%s)"
                data6 = (self.codigo_postal,)
                sentencia.execute(SQL6, data6)
                self.numero1 = sentencia.fetchall()

            self.lista_num["values"] = self.numero1
            self.lista_num.place(x = 530, y = 300, width = 160)

            self.boton_ok = Button(self, text = "Ok", state = 'normal', command = self.comprobar_datos)
            self.boton_ok.place(x = 700, y = 270)

    def volverAtras(self):
        self.destroy()
        self.wind.show()

    def comprobar_datos(self):
        self.sector_direccion = self.lista_sec.get()
        self.calle_direccion = self.lista_calle.get()
        self.numero_direccion = self.lista_num.get()

        if self.sector_direccion == "" or self.calle_direccion == "" or self.numero_direccion == "":
            self.mostrar_mensaje_error()
        if self.sector_direccion != "" and self.calle_direccion != "" and self.numero_direccion != "":
            self.boton_actualizar.config(state = 'normal')

    def actualizar_BD_cines(self):
        with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
            SQL7 = "UPDATE ps.cine SET sector = (%s), calle = (%s), numero_calle = (%s) WHERE codigo_postal = (%s)"
            data7 = (self.sector_direccion, self.calle_direccion, self.numero_direccion, self.codigo_postal,)
            sentencia.execute(SQL7, data7)
        self.volverAtras()


class Eliminar_cine(Toplevel):
    def __init__(self, wind):
        self.wind = wind
        Toplevel.__init__(self)
        self.dsnBaseDatos = "user=bdi2019p password=bdi2019p host=plop.inf.udec.cl dbname=bdi2019p port=5432"

        self.title("Eliminar cine")
        self.resizable(0, 0)
        self.geometry("800x500")
        self.config(bg = 'dimgray')

        self.nombre_region = StringVar()
        self.nombre_ciudad = StringVar()
        self.nombre_cine = IntVar()

        self.region = Label(self, text = "Region: ", bg = "pink").place(x = 20, y = 150, width = 130)
        self.lista_reg = ttk.Combobox(self, state = "readonly")

        with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
            SQL1 = "SELECT region FROM ps.ciudadyregion"
            sentencia.execute(SQL1)
            self.regiones = sentencia.fetchall()

        self.lista_reg["values"] = self.regiones
        self.lista_reg.place(x = 160, y = 150, width = 530)
        self.lista_reg.bind("<<ComboboxSelected>>", self.enableWidgets1)

        self.boton_ok = Button(self, text = "Ok", state = 'disabled', command = self.mostrar_ciudad)
        self.boton_ok.place(x = 700, y = 150)

        self.boton_eliminar = Button(self, text = "Eliminar", state = 'disabled', command = self.eliminar_BD_cine)
        self.boton_eliminar.place(x = 300, y = 450)

        self.botonVolver = Button(self, text = 'atrás', command = self.volverAtras)
        self.botonVolver.place(x = 10, y = 10, width = 40, height = 20)

    def enableWidgets1(self, event):
        self.boton_ok.config(state = 'normal')
        self.nombre_region = self.lista_reg.get()

    def mostrar_ciudad(self):
        self.ciudad = Label(self, text = "Ciudad: ", bg = "pink").place(x = 20, y = 200, width = 130)
        self.lista_ciu = ttk.Combobox(self, state = "readonly")

        with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
            SQL2 = "SELECT nombre_ciudad FROM ps.ciudadyregion WHERE region = (%s)"
            data2 = (self.nombre_region,)
            sentencia.execute(SQL2, data2)
            self.ciudades = sentencia.fetchall()

        self.lista_ciu["values"] = self.ciudades
        self.lista_ciu.place(x = 160, y = 200, width = 530)
        self.lista_ciu.bind("<<ComboboxSelected>>",self.enableWidgets2)

        self.boton_ok = Button(self, text = "Ok", state = 'disabled', command = self.mostrar_cine)
        self.boton_ok.place(x = 700, y = 200)

    def enableWidgets2(self, event):
        self.boton_ok.config(state = 'normal')
        self.nombre_ciudad = self.lista_ciu.get()

    def mostrar_cine(self):
        self.cine = Label(self, text = "Cine: ", bg = "pink").place(x = 20, y = 250, width = 130)
        self.lista_cine = ttk.Combobox(self, state = "readonly")

        with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
            SQL3 = "SELECT codigo_postal FROM ps.ciudad WHERE nombre_ciudad = (%s)"
            data3 = (self.nombre_ciudad,)
            sentencia.execute(SQL3, data3)
            self.codigo_postal = sentencia.fetchone()

            SQL4 = "SELECT nombre_cine FROM ps.cine WHERE codigo_postal = (%s)"
            data4 = (self.codigo_postal[0],)
            sentencia.execute(SQL4, data4)
            self.ciudades = sentencia.fetchall()

        self.lista_cine["values"] = self.ciudades
        self.lista_cine.place(x = 160, y = 250, width = 530)
        self.lista_cine.bind("<<ComboboxSelected>>",self.enableWidgets3)

        self.boton_ok = Button(self, text = "Ok", state = 'disabled', command = self.comprobar_datos)
        self.boton_ok.place(x = 700, y = 250)

    def enableWidgets3(self, event):
        self.boton_ok.config(state = 'normal')
        self.nombre_cine = self.lista_cine.get()

    def comprobar_datos(self):
        self.boton_eliminar.config(state = 'normal')

    def volverAtras(self):
        self.destroy()
        self.wind.show()

    def eliminar_BD_cine(self):
        with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
            SQL5 = "DELETE FROM ps.cine WHERE nombre_cine = (%s)"
            data5 = (self.nombre_cine,)
            sentencia.execute(SQL5, data5)

        with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
            SQL6 = "DELETE FROM ps.ciudadyregion WHERE nombre_ciudad = (%s)"
            data6 = (self.nombre_ciudad,)
            sentencia.execute(SQL6, data6)

        with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
            SQL7 = "DELETE FROM ps.ciudad WHERE codigo_postal = (%s)"
            data7 = (self.codigo_postal[0],)
            sentencia.execute(SQL7, data7)
        self.volverAtras()


class Ingresar_pel(Toplevel):
    def __init__(self, wind):
        self.wind = wind
        Toplevel.__init__(self)
        self.dsnBaseDatos = "user=bdi2019p password=bdi2019p host=plop.inf.udec.cl dbname=bdi2019p port=5432"

        self.title("Ingresar peliculas")
        self.resizable(0, 0)
        self.geometry("800x500")
        self.config(bg='dimgray')

        self.nombre_pelicula = StringVar()
        self.duracion_pelicula = StringVar()
        self.clasificacion_pelicula = StringVar()
        self.estreno_pelicula = StringVar()
        self.productora_pelicula = StringVar()
        self.genero_pelicula1 = StringVar()
        self.genero_pelicula2 = StringVar()
        self.genero_pelicula3 = StringVar()
        self.genero_pelicula4 = StringVar()
        self.genero_pelicula5 = StringVar()
        self.genero_pelicula6 = StringVar()

        self.nombre_pel = Label(self, text = "Nombre: ", bg = "pink").place(x = 20, y = 60, width = 130)
        self.entry_pel = Entry(self)
        self.entry_pel.place(x = 160, y = 60, width = 530)

        self.boton_ok = Button(self, text = "Ok", state = 'normal', command = self.mostrar_duracion)
        self.boton_ok.place(x = 700, y = 60)

        self.boton_ingresar = Button(self, text = "Ingresar", state = 'disabled', command = self.ingresar_BD_peliculas)
        self.boton_ingresar.place(x = 300, y = 450)

        self.botonVolver = Button(self, text = 'atrás', command = self.volverAtras)
        self.botonVolver.place(x = 10, y = 10, width = 40, height=20)

    def mostrar_mensaje_error(self):
        #CAMBIAR NOMBRE
        messagebox.showwarning(message = "Por favor, ingrese texto faltante.", title="Texto vacío")

    def mostrar_duracion(self):
        self.nombre_pelicula = self.entry_pel.get()
        if self.nombre_pelicula == "":
            self.mostrar_mensaje_error()
        else:
            self.duracion = Label(self, text = "Duración (minutos): ", bg = "pink", wraplength = 70).place(x = 20, y = 100, width = 130)
            self.entry_dur = Entry(self)
            self.entry_dur.place(x = 160, y = 100, width = 160)

            self.boton_ok = Button(self, text = "Ok", state = 'normal', command = self.mostrar_clasificacion)
            self.boton_ok.place(x = 330, y = 100)

    def mostrar_clasificacion(self):
        self.duracion_pelicula = self.entry_dur.get()
        if self.duracion_pelicula == "":
            self.mostrar_mensaje_error()
        else:
            self.hora = int(self.duracion_pelicula) // 60
            self.minutos = int(self.duracion_pelicula) - (60 * self.hora) 
            self.clasificacion = Label(self, text = "Clasificación: ", bg = "pink", wraplength = 90).place(x = 390, y = 100, width = 130)
            self.lista_clas = ttk.Combobox(self, state = "readonly")
            self.lista_clas["values"] = ["TE", "TE+7", "14", "18"]
            self.lista_clas.place(x = 530, y = 100, width = 160)
            self.lista_clas.bind("<<ComboboxSelected>>",self.enableWidgets1)

            self.boton_ok = Button(self, text = "Ok", state = 'disabled', command = self.mostrar_fecha)
            self.boton_ok.place(x = 700, y = 100)

    def enableWidgets1(self, event):
        self.boton_ok.config(state = 'normal')
        self.clasificacion_pelicula = self.lista_clas.get()

    def mostrar_fecha(self):
        self.estreno = Label(self, text = "Fecha estreno: ", bg = "pink", wraplength = 90).place(x = 20, y = 160, width = 130)
        self.boton_selec = Button(self, text = 'Ver', command = self.ver_fecha)
        self.boton_selec.place(x = 170, y = 160)

    def ver_fecha(self):
        self.now = datetime.now()
        self.top = Toplevel(self)
        self.fecha = Calendar(self.top, font = "Arial 14", selectmode = 'day', cursor = "hand1", year = self.now.year, month = self.now.month, day = self.now.day)
        self.fecha.pack(fill = "both", expand = True)
        self.ok = Button(self.top, text = "Ok", command = self.salir).pack()

    def salir(self):
        self.top.destroy()
        self.estreno_pelicula = self.fecha.selection_get()
        self.imprimir_fecha = Label(self, text = self.estreno_pelicula, bg = 'steelblue').place(x = 240, y = 160)
        self.mostrar_productora()

    def mostrar_productora(self):
        self.productora = Label(self, text = "Productora: ", bg = "pink").place(x = 20, y = 210, width = 130)
        self.entry_pro = Entry(self)
        self.entry_pro.place(x = 160, y = 210, width = 530)

        self.boton_ok = Button(self, text = "Ok", state = 'normal', command = self.mostrar_generos)
        self.boton_ok.place(x = 700, y = 210)


    def mostrar_generos(self):
        self.productora_pelicula = self.entry_pro.get()
        if self.productora_pelicula == "":
            self.mostrar_mensaje_error()
        else:
            self.genero = Label(self, text = "Géneros: (hasta 6)", bg = "pink", wraplength = 90).place(x = 20, y = 280, width = 130)
            self.entry_gen1 = Entry(self)
            self.entry_gen1.place(x = 160, y = 280, width = 170)
            self.entry_gen2 = Entry(self)
            self.entry_gen2.place(x = 345, y = 280, width = 170)
            self.entry_gen3 = Entry(self)
            self.entry_gen3.place(x = 530, y = 280, width = 170)
            self.entry_gen4 = Entry(self)
            self.entry_gen4.place(x = 160, y = 320, width = 170)
            self.entry_gen5 = Entry(self)
            self.entry_gen5.place(x = 345, y = 320, width = 170)
            self.entry_gen6 = Entry(self)
            self.entry_gen6.place(x = 530, y = 320, width = 170)

            self.boton_ok = Button(self, text = "Ok", state = 'normal', command = self.comprobar_datos)
            self.boton_ok.place(x = 720, y = 300)

    def comprobar_datos(self):
        self.genero_pelicula1 = self.entry_gen1.get()
        self.genero_pelicula2 = self.entry_gen2.get()
        self.genero_pelicula3 = self.entry_gen3.get()
        self.genero_pelicula4 = self.entry_gen4.get()
        self.genero_pelicula5 = self.entry_gen5.get()
        self.genero_pelicula6 = self.entry_gen6.get()

        self.boton_ingresar.config(state = 'normal')

        self.duracion_pelicula = str(self.hora) + ":" + str(self.minutos) + ":00"
        print(self.duracion_pelicula)



    def show(self):
        self.update()
        self.deiconify()

    def volverAtras(self):
        self.destroy()
        self.wind.show()

    def ingresar_BD_peliculas(self):
        with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
            SQL1 = "INSERT INTO ps.pelicula (nombre_pelicula, duracion, clasificacion, estreno, productora) VALUES (%s, %s, %s, %s, %s)"
            data1 = (self.nombre_pelicula, self.duracion_pelicula, self.clasificacion_pelicula, self.estreno_pelicula, self.productora_pelicula,)
            sentencia.execute(SQL1, data1)

            self.id_pel = IntVar()
            SQL2 = "SELECT id_pelicula FROM ps.pelicula WHERE nombre_pelicula = (%s)"
            data2 = (self.nombre_pelicula,)
            sentencia.execute(SQL2, data2)
            self.id_pel = sentencia.fetchone()


            if self.genero_pelicula1 != "":
                SQL3 = "INSERT INTO ps.generopelicula (id_pelicula, genero) VALUES (%s, %s)"
                data3 = (self.id_pel, self.genero_pelicula1)
                sentencia.execute(SQL3, data3)
            if self.genero_pelicula2 != "":
                SQL4 = "INSERT INTO ps.generopelicula (id_pelicula, genero) VALUES (%s, %s)"
                data4 = (self.id_pel, self.genero_pelicula2)
                sentencia.execute(SQL4, data4)
            if self.genero_pelicula3 != "":
                SQL5 = "INSERT INTO ps.generopelicula (id_pelicula, genero) VALUES (%s, %s)"
                data5 = (self.id_pel, self.genero_pelicula3)
                sentencia.execute(SQL5, data5)
            if self.genero_pelicula4 != "":
                SQL6 = "INSERT INTO ps.generopelicula (id_pelicula, genero) VALUES (%s, %s)"
                data6 = (self.id_pel, self.genero_pelicula4)
                sentencia.execute(SQL6, data6)
            if self.genero_pelicula5 != "":
                SQL7 = "INSERT INTO ps.generopelicula (id_pelicula, genero) VALUES (%s, %s)"
                data7 = (self.id_pel, self.genero_pelicula5)
                sentencia.execute(SQL7, data7)
            if self.genero_pelicula6 != "":
                SQL8 = "INSERT INTO ps.generopelicula (id_pelicula, genero) VALUES (%s, %s)"
                data8 = (self.id_pel, self.genero_pelicula6)
                sentencia.execute(SQL8, data8)

        self.volverAtras()


class Ingresar_fun(Toplevel):
    def __init__(self, wind):
        self.wind = wind
        Toplevel.__init__(self)
        self.dsnBaseDatos = "user=bdi2019p password=bdi2019p host=plop.inf.udec.cl dbname=bdi2019p port=5432"
        self.title("Ingresar funciones")
        self.resizable(0, 0)
        self.geometry("800x500")
        self.config(bg = 'dimgray')

        #formato, idioma, fecha, salas, hora_inicio, hora_final

        self.nombre_region = StringVar()
        self.nombre_ciudad = StringVar()
        self.nombre_cine = StringVar()
        self.codigo_postal = IntVar()
        self.nombre_pelicula = StringVar()
        self.fecha_funcion = StringVar()
        self.formato_funcion = StringVar()
        self.idioma_funcion = StringVar()
        self.hora_funcion = StringVar()
        self.hora_final_funcion = StringVar()
        self.salas_disponibles = StringVar()

        self.region = Label(self, text = "Región: ", bg = "pink").place(x = 20, y = 60, width = 130)
        self.lista_reg = ttk.Combobox(self, state = "readonly")

        with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
            SQL = "SELECT region FROM ps.ciudadyregion"
            sentencia.execute(SQL)
            self.regiones = sentencia.fetchall()

        self.lista_reg["values"] = self.regiones
        self.lista_reg.place(x = 160, y = 60, width = 150)
        self.lista_reg.bind("<<ComboboxSelected>>", self.enableWidgets1)

        self.boton_ok = Button(self, text = "Ok", state = 'disabled', command = self.mostrar_ciudad)
        self.boton_ok.place(x = 320, y = 60)

        self.boton_ingresar = Button(self, text = "Ingresar", state = 'disabled', command = self.ingresar_BD_funciones)
        self.boton_ingresar.place(x = 300, y = 450)

        self.botonVolver = Button(self, text = 'atrás', command = self.volverAtras)
        self.botonVolver.place(x = 10, y = 10, width = 40, height = 20)

    def enableWidgets1(self, event):
        self.boton_ok.config(state = 'normal')
        self.nombre_region = self.lista_reg.get()

    def mostrar_ciudad(self):
        self.ciudad = Label(self, text = "Ciudad: ", bg = "pink").place(x = 400, y = 60, width = 130)
        self.lista_ciu = ttk.Combobox(self, state = "readonly")

        with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
            SQL1 = "SELECT nombre_ciudad FROM ps.ciudadyregion WHERE region = (%s)"
            data1 = (self.nombre_region,)
            sentencia.execute(SQL1, data1)
            self.ciudades = sentencia.fetchall()

        self.lista_ciu["values"] = self.ciudades
        self.lista_ciu.place(x = 540, y = 60, width = 150)
        self.lista_ciu.bind("<<ComboboxSelected>>", self.enableWidgets2)

        self.boton_ok = Button(self, text = "Ok", state = 'disabled', command = self.mostrar_cine)
        self.boton_ok.place(x = 700, y = 60)

    def enableWidgets2(self, event):
        self.boton_ok.config(state = 'normal')
        self.nombre_ciudad = self.lista_ciu.get()

    def mostrar_cine(self):
        self.cine = Label(self, text = "Escoja cine: ", bg = "pink").place(x = 20, y = 100, width = 130)
        self.lista_cine = ttk.Combobox(self, state = "readonly")

        with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
            SQL3 = "SELECT codigo_postal FROM ps.ciudad WHERE nombre_ciudad = (%s)"
            data3 = (self.nombre_ciudad,)
            sentencia.execute(SQL3, data3)
            self.codigo_postal = sentencia.fetchone()

            SQL4 = "SELECT nombre_cine FROM ps.cine WHERE codigo_postal = (%s)"
            data4 = (self.codigo_postal[0],)
            sentencia.execute(SQL4, data4)
            self.cines = sentencia.fetchall()

        self.lista_cine["values"] = self.cines
        self.lista_cine.place(x = 160, y = 100, width = 530)
        self.lista_cine.bind("<<ComboboxSelected>>", self.enableWidgets3)

        self.boton_ok = Button(self, text = "Ok", state = 'disabled', command = self.mostrar_pelicula)
        self.boton_ok.place(x = 700, y = 100)

    def enableWidgets3(self, event):
        self.boton_ok.config(state = 'normal')
        self.nombre_cine = self.lista_cine.get()

    def mostrar_pelicula(self):
        self.pelicula = Label(self, text = "Escoja pelicula: ", bg = "pink").place(x = 20, y = 140, width = 130)
        self.lista_pel = ttk.Combobox(self, state = "readonly")

        with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
            SQL5 = "SELECT nombre_pelicula FROM ps.pelicula"
            sentencia.execute(SQL5)
            self.peliculas = sentencia.fetchall()
        
        self.lista_pel["values"] = self.peliculas
        self.lista_pel.place(x = 160, y = 140, width = 530)
        self.lista_pel.bind("<<ComboboxSelected>>", self.enableWidgets4)

        self.boton_ok = Button(self, text = "Ok", state = 'disabled', command = self.mostrar_fechayformato)
        self.boton_ok.place(x = 700, y = 140)

    def enableWidgets4(self, event):
        self.boton_ok.config(state = 'normal')
        self.nombre_pelicula = self.lista_pel.get()

    def mostrar_fechayformato(self):
        self.fecha_fun = Label(self, text = "Fecha: ", bg = "pink").place(x = 20, y = 180, width = 130)
        self.boton_selec = Button(self, text = 'Ver', command = self.ver_fecha)
        self.boton_selec.place(x = 180, y = 180)

        self.formato = Label(self, text = "Formato: ", bg = "pink").place(x = 400, y = 180, width = 130)
        self.lista_form = ttk.Combobox(self, state = "readonly")
        self.lista_form["values"] = ["2D", "3D", "4D", "XD"]
        self.lista_form.place(x = 540, y = 180, width = 150)
        self.lista_form.bind("<<ComboboxSelected>>", self.enableWidgets5)

        self.boton_ok = Button(self, text = "Ok", state = 'disabled', command = self.mostrar_idioma)
        self.boton_ok.place(x = 700, y = 180)

    def ver_fecha(self):
        self.now = datetime.now()
        self.top = Toplevel(self)
        self.fecha = Calendar(self.top, font = "Arial 14", selectmode = 'day', cursor = "hand1", year = self.now.year, month = self.now.month, day = self.now.day)
        self.fecha.pack(fill = "both", expand = True)
        self.ok = Button(self.top, text = "Ok", command = self.salir).pack()

    def error_fecha(self, num):
        if num == 1:
            messagebox.showwarning(message = "Esta fecha ya pasó.", title="Fecha incorrecta")
        if num == 2:
            messagebox.showwarning(message = "Fecha seleccionada no coincide con estreno.", title="Fecha incorrecta")

    def salir(self):
        self.top.destroy()
        self.fecha_funcion = self.fecha.selection_get()

        with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
            SQL7 = "SELECT id_pelicula FROM ps.pelicula WHERE nombre_pelicula = (%s)"
            data7 = (self.nombre_pelicula,)
            sentencia.execute(SQL7, data7)
            self.id_pel = sentencia.fetchone()

        with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
            SQL5 = "SELECT estreno FROM ps.pelicula WHERE id_pelicula = (%s)"
            data5 = (self.id_pel[0],)
            sentencia.execute(SQL5, data5)
            self.fecha_estreno = sentencia.fetchone()
        
        if str(self.fecha_funcion) < str(datetime.now().date()):
            self.error_fecha(1)
        elif str(self.fecha_estreno[0]) > str(self.fecha_funcion):
            self.error_fecha(2)
        else:
            self.imprimir_fecha = Label(self, text = self.fecha_funcion, bg = 'steelblue').place(x = 240, y = 180)

    def enableWidgets5(self, event):
        self.boton_ok.config(state = 'normal')
        self.formato_funcion = self.lista_form.get()

    def mostrar_idioma(self):
        self.idioma = Label(self, text = "Idioma: ", bg = "pink").place(x = 400, y = 220, width = 130)
        self.entry_idioma = Entry(self)
        self.entry_idioma.place(x = 540, y = 220, width = 150)

        self.boton_ok = Button(self, text = "Ok", state = 'normal', command = self.mostrar_salas)
        self.boton_ok.place(x = 700, y = 220)

    def mostrar_salas(self):
        self.idioma_funcion = self.entry_idioma.get()
        self.sala = Label(self, text = "Salas disponibles: ",bg = "pink", wraplength = 70).place(x = 20, y = 230, width = 130)
        self.lista_salas = ttk.Combobox(self, state = "readonly")

        with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
            SQL6 = "SELECT numero_sala FROM ps.sala WHERE tipo_sala = (%s) AND nombre_cine = (%s)"
            data6 = (self.formato_funcion, self.nombre_cine,)
            sentencia.execute(SQL6, data6)
            self.salas = sentencia.fetchall()

        self.lista_salas["values"] = self.salas
        self.lista_salas.place(x = 160, y = 230, width = 130)
        self.lista_salas.bind("<<ComboboxSelected>>", self.enableWidgets6)

        self.boton_ok = Button(self, text = "Ok", state = 'disabled', command = self.mostrar_horarios_ocupados)
        self.boton_ok.place(x = 320, y = 230)

    def enableWidgets6(self, event):
        self.boton_ok.config(state = 'normal')
        self.salas_disponibles = self.lista_salas.get()

        with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
            SQL9 = "SELECT duracion FROM ps.pelicula WHERE id_pelicula = (%s)"
            data9 = (self.id_pel[0],)
            sentencia.execute(SQL9, data9)
            self.duracion_pel = sentencia.fetchone()

        with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
            self.horas_ocupadas = StringVar()
            SQL8 = "SELECT hora_inicio, hora_final FROM ps.funcion WHERE id_pelicula = (%s) AND fecha = (%s) AND numero_sala = (%s) AND nombre_cine = (%s)"
            data8 = (self.id_pel[0], self.fecha_funcion, self.salas_disponibles, self.nombre_cine,)
            sentencia.execute(SQL8, data8)
            self.horas_ocupadas = sentencia.fetchall()

    def formato_incorrecto(self):
        messagebox.showwarning(message = "Formato incorrecto.", title="Error")


    def mostrar_horarios_ocupados(self):
        if self.horas_ocupadas:
            self.hora_fun = Label(self, text = "Horarios ocupados: ", bg = "orange red").place(x = 20, y = 320, width = 130)
            self.lista_horas = ttk.Combobox(self, state = "readonly")
            self.lista_horas["values"] = self.horas_ocupadas 
            self.lista_horas.place(x = 190, y = 320, width = 560)
        else:
            self.hora_fun = Label(self, text = "Todos los horarios están disponibles.", bg = "steelblue").place(x = 20, y = 320, width = 300) 

        self.ingresar_hora()

    def ingresar_hora(self):
        self.horario = Label(self, text = "Ingrese hora inicio (00:00:00): ", bg = "pink", wraplength = 90).place(x = 20, y = 370, width = 130)
        self.entry_hora = Entry(self)
        self.entry_hora.place(x = 160, y = 370, width = 150)

        self.boton_ok = Button(self, text = "Ok", state = 'normal', command = self.comprobar_horarios)
        self.boton_ok.place(x = 320, y = 370)


    def comprobar_horarios(self):
        self.hora_funcion = self.entry_hora.get()
        self.fecha_hora = str(self.fecha_funcion) + " " + str(self.hora_funcion)
        try:
            self.h_ini = datetime.strptime(self.fecha_hora, "%Y-%m-%d %H:%M:%S")
            self.duracion_peli = str(self.duracion_pel[0])
            self.dur_pel = self.duracion_peli.split(":")
            self.hora = int(self.dur_pel[0])
            self.minuto = int(self.dur_pel[1])
            self.f_fin = self.h_ini + timedelta(hours = self.hora, minutes = self.minuto)
            self.tiempo_de_limpieza = 10 
            self.h_fin_fun = self.f_fin + timedelta(minutes = self.tiempo_de_limpieza)
            self.tam = len(self.horas_ocupadas)

            if self.horas_ocupadas:
                self.horas_ocup = []

                for i in range(0, self.tam):
                    for j in range(0, 2):
                        hora_fecha = str(self.fecha_funcion) + " " + str(self.horas_ocupadas[i][j])
                        self.horas_ocup.append(datetime.strptime(hora_fecha, "%Y-%m-%d %H:%M:%S"))

                self.c1 = 0
                self.c2 = 1
                for i in range(0, self.tam):
                    if self.h_ini < self.horas_ocup[self.c1]:
                        if self.h_fin_fun <= self.horas_ocup[self.c1]:
                            self.boton_ingresar.config(state = 'normal')
                        else:
                            self.error_horarios()
                    elif self.h_ini >= self.horas_ocup[self.c2]:
                        self.boton_ingresar.config(state = 'normal')
                    else:
                        self.error_horarios()
                    self.c1 += 2
                    self.c2 += 2
            else:
                self.boton_ingresar.config(state = 'normal')

        except:
            self.formato_incorrecto()

    def error_horarios(self):
        messagebox.showwarning(message = "Horario no disponible.", title = "Error")

    def show(self):
        self.update()
        self.deiconify()

    def volverAtras(self):
        self.destroy()
        self.wind.show()

    def ingresar_BD_funciones(self):
        with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
            SQL1 = "INSERT INTO ps.funcion (formato, idioma, hora_inicio, hora_final, id_pelicula, fecha, numero_sala, nombre_cine) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            data1 = (self.formato_funcion, self.idioma_funcion, self.h_ini, self.h_fin_fun, self.id_pel[0], self.fecha_funcion, self.salas_disponibles, self.nombre_cine,)
            sentencia.execute(SQL1, data1)
        self.volverAtras()


class Actualizar_pel(Toplevel):
    def __init__(self, wind):
        self.wind = wind
        Toplevel.__init__(self)
        self.dsnBaseDatos = "user=bdi2019p password=bdi2019p host=plop.inf.udec.cl dbname=bdi2019p port=5432"

        self.title("Actualizar películas")
        self.resizable(0, 0)
        self.geometry("800x500")
        self.config(bg='dimgray')

        self.nombre_pelicula = StringVar()
        self.clasificacion_pelicula = StringVar()
        self.productora_pelicula = StringVar()
        self.genero_pelicula1 = StringVar()
        self.genero_pelicula2 = StringVar()
        self.genero_pelicula3 = StringVar()
        self.genero_pelicula4 = StringVar()
        self.genero_pelicula5 = StringVar()
        self.genero_pelicula6 = StringVar()

        self.nombre_pel = Label(self, text = "Nombre: ", bg = "pink").place(x = 20, y = 60, width = 130)
        self.entry_pel = ttk.Combobox(self, state = 'readonly')

        with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
                SQL1 = "SELECT nombre_pelicula FROM ps.pelicula"
                sentencia.execute(SQL1)
                self.peliculas = sentencia.fetchall()

        self.entry_pel["values"] = self.peliculas
        self.entry_pel.place(x = 160, y = 60, width = 530)

        self.boton_ok = Button(self, text = "Ok", state = 'normal', command = self.mostrar_clasificacion)
        self.boton_ok.place(x = 700, y = 60)

        self.boton_actualizar = Button(self, text = "Actualizar", state = 'disabled', command = self.actualizar_BD_peliculas)
        self.boton_actualizar.place(x = 300, y = 450)

        self.botonVolver = Button(self, text = 'atrás', command = self.volverAtras)
        self.botonVolver.place(x = 10, y = 10, width = 40, height = 20)

    def mostrar_mensaje_error(self):
        #CAMBIAR NOMBRE
        messagebox.showwarning(message = "Por favor, ingrese texto faltante.", title="Texto vacío")

    def mostrar_clasificacion(self):
        self.nombre_pelicula = self.entry_pel.get()
        if self.nombre_pelicula == "":
            self.mostrar_mensaje_error()
        else:
            with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
                SQL2 = "SELECT id_pelicula FROM ps.pelicula WHERE nombre_pelicula = (%s)"
                data2 = (self.nombre_pelicula,)
                sentencia.execute(SQL2, data2)
                self.id_pel = sentencia.fetchone()

            self.clasificacion = Label(self, text = "Clasificación: ", bg = "pink", wraplength = 90).place(x = 20, y = 100, width = 130)
            self.lista_clas = ttk.Combobox(self, state = 'readonly')
            self.lista_clas["values"] = ["TE", "TE+7", "14", "18"]
            self.lista_clas.place(x = 160, y = 100, width = 160)
            self.lista_clas.bind("<<ComboboxSelected>>",self.enableWidgets1)

            self.boton_ok = Button(self, text = "Ok", state = 'normal', command = self.mostrar_productora)
            self.boton_ok.place(x = 330, y = 100)

    def enableWidgets1(self, event):
        self.boton_ok.config(state = 'normal')
        self.clasificacion_pelicula = self.lista_clas.get()


    def mostrar_productora(self):
        self.productora = Label(self, text="Productora: ", bg = "pink").place(x = 20, y = 210, width = 130)
        self.entry_pro = ttk.Combobox(self)

        with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
                SQL5 = "SELECT productora FROM ps.pelicula WHERE id_pelicula = (%s)"
                data5 = (self.id_pel[0],)
                sentencia.execute(SQL5, data5)
                self.prod1 = sentencia.fetchone()

        self.entry_pro["values"] = self.prod1
        self.entry_pro.place(x = 160, y = 210, width = 530)

        self.boton_ok = Button(self, text = "Ok", state = 'normal', command = self.mostrar_generos)
        self.boton_ok.place(x = 700, y = 210)

    def mostrar_generos(self):
        self.productora_pelicula = self.entry_pro.get()
        if self.productora_pelicula == "":
            self.mostrar_mensaje_error()
        else:
            with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
                SQL6 = "SELECT genero FROM ps.generopelicula WHERE id_pelicula = (%s)"
                data6 = (self.id_pel[0],)
                sentencia.execute(SQL6, data6)
                self.generos = sentencia.fetchall()

            self.genero = Label(self, text = "Géneros: (hasta 6)", bg = "pink", wraplength = 90).place(x = 20, y = 280, width = 130)
            self.entry_gen1 = ttk.Combobox(self)
            self.entry_gen1["values"] = self.generos
            self.entry_gen1.place(x = 160, y = 280, width = 170)
            self.entry_gen2 = ttk.Combobox(self)
            self.entry_gen2["values"] = self.generos
            self.entry_gen2.place(x = 345, y = 280, width = 170)
            self.entry_gen3 = ttk.Combobox(self)
            self.entry_gen3["values"] = self.generos
            self.entry_gen3.place(x = 530, y = 280, width = 170)
            self.entry_gen4 = ttk.Combobox(self)
            self.entry_gen4["values"] = self.generos
            self.entry_gen4.place(x = 160, y = 320, width = 170)
            self.entry_gen5 = ttk.Combobox(self)
            self.entry_gen5["values"] = self.generos
            self.entry_gen5.place(x = 345, y = 320, width = 170)
            self.entry_gen6 = ttk.Combobox(self)
            self.entry_gen6["values"] = self.generos
            self.entry_gen6.place(x = 530, y = 320, width = 170)

            self.boton_ok = Button(self, text = "Ok", state = 'normal', command = self.comprobar_datos)
            self.boton_ok.place(x = 720, y = 300)

    def comprobar_datos(self):
        self.genero_pelicula1 = self.entry_gen1.get()
        self.genero_pelicula2 = self.entry_gen2.get()
        self.genero_pelicula3 = self.entry_gen3.get()
        self.genero_pelicula4 = self.entry_gen4.get()
        self.genero_pelicula5 = self.entry_gen5.get()
        self.genero_pelicula6 = self.entry_gen6.get()

        self.boton_actualizar.config(state = 'normal')

    def show(self):
        self.update()
        self.deiconify()

    def volverAtras(self):
        self.destroy()
        self.wind.show()

    def actualizar_BD_peliculas(self):
        with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
            SQL7 = "UPDATE ps.pelicula SET clasificacion = (%s), productora = (%s) WHERE id_pelicula = (%s)"
            data7 = (self.clasificacion_pelicula, self.productora_pelicula, self.id_pel,)
            sentencia.execute(SQL7, data7)

            SQL8 = "DELETE FROM ps.generopelicula WHERE id_pelicula = (%s)"
            data8 = (self.id_pel[0],)
            sentencia.execute(SQL8, data8)

            if self.genero_pelicula1 != "":
                SQL1 = "INSERT INTO ps.generopelicula (id_pelicula, genero) VALUES (%s, %s)"
                data1 = (self.id_pel[0], self.genero_pelicula1)
                sentencia.execute(SQL1, data1)
            if self.genero_pelicula2 != "":
                SQL2 = "INSERT INTO ps.generopelicula (id_pelicula, genero) VALUES (%s, %s)"
                data2 = (self.id_pel[0], self.genero_pelicula2)
                sentencia.execute(SQL2, data2)
            if self.genero_pelicula3 != "":
                SQL3 = "INSERT INTO ps.generopelicula (id_pelicula, genero) VALUES (%s, %s)"
                data3 = (self.id_pel[0], self.genero_pelicula3)
                sentencia.execute(SQL3, data3)
            if self.genero_pelicula4 != "":
                SQL4 = "INSERT INTO ps.generopelicula (id_pelicula, genero) VALUES (%s, %s)"
                data4 = (self.id_pel[0], self.genero_pelicula4)
                sentencia.execute(SQL4, data4)
            if self.genero_pelicula5 != "":
                SQL5 = "INSERT INTO ps.generopelicula (id_pelicula, genero) VALUES (%s, %s)"
                data5 = (self.id_pel[0], self.genero_pelicula5)
                sentencia.execute(SQL5, data5)
            if self.genero_pelicula6 != "":
                SQL6 = "INSERT INTO ps.generopelicula (id_pelicula, genero) VALUES (%s, %s)"
                data6 = (self.id_pel[0], self.genero_pelicula6)
                sentencia.execute(SQL6, data6)

        self.volverAtras()


class Actualizar_fun(Toplevel):
    def __init__(self, wind):
        self.wind = wind
        Toplevel.__init__(self)
        self.dsnBaseDatos = "user=bdi2019p password=bdi2019p host=plop.inf.udec.cl dbname=bdi2019p port=5432"

        self.title("Actualizar funciones")
        self.resizable(0, 0)
        self.geometry("800x500")
        self.config(bg='dimgray')

        self.nombre_region = StringVar()
        self.nombre_ciudad = StringVar()
        self.nombre_cine = StringVar()
        self.nombre_pelicula = StringVar()
        self.funcion = StringVar()
        self.formato_funcion = StringVar()
        self.fecha_funcion = StringVar()
        self.salas_disponibles = StringVar()
        self.hora_funcion = StringVar()

        self.region = Label(self, text = "Región: ", bg = "pink").place(x = 20, y = 60, width = 130)
        self.lista_reg = ttk.Combobox(self, state = "readonly")
        with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
            SQL = "SELECT region FROM ps.ciudadyregion"
            sentencia.execute(SQL)
            self.regiones = sentencia.fetchall()

        self.lista_reg["values"] = self.regiones
        self.lista_reg.place(x = 160, y = 60, width = 150)
        self.lista_reg.bind("<<ComboboxSelected>>", self.enableWidgets1)

        self.boton_ok = Button(self, text = "Ok", state = 'disabled', command = self.mostrar_ciudad)
        self.boton_ok.place(x = 320, y = 60)

        self.boton_actualizar = Button(self, text = "Actualizar", command = self.actualizar_BD_funciones)
        self.boton_actualizar.place(x = 300, y = 450)

        self.botonVolver = Button(self, text = 'atrás', command = self.volverAtras)
        self.botonVolver.place(x = 10, y = 10, width = 40, height = 20)

    def enableWidgets1(self, event):
        self.boton_ok.config(state = 'normal')
        self.nombre_region = self.lista_reg.get()

    def mostrar_ciudad(self):
        self.ciudad = Label(self, text="Ciudad: ", bg = "pink").place(x = 400, y = 60, width = 130)
        self.lista_ciu = ttk.Combobox(self, state = "readonly")

        with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
            SQL1 = "SELECT nombre_ciudad FROM ps.ciudadyregion WHERE region = (%s)"
            data1 = (self.nombre_region,)
            sentencia.execute(SQL1, data1)
            self.ciudades = sentencia.fetchall()

        self.lista_ciu["values"] = self.ciudades
        self.lista_ciu.place(x = 540, y = 60, width = 150)
        self.lista_ciu.bind("<<ComboboxSelected>>", self.enableWidgets2)

        self.boton_ok = Button(self, text = "Ok", state = 'disabled', command = self.mostrar_cine)
        self.boton_ok.place(x = 700, y = 60)

    def enableWidgets2(self, event):
        self.boton_ok.config(state = 'normal')
        self.nombre_ciudad = self.lista_ciu.get()

    def mostrar_cine(self):
        self.cine = Label(self, text = "Escoja cine: ",bg = "pink").place(x = 20, y = 100, width = 130)
        self.lista_cine = ttk.Combobox(self, state = "readonly")

        with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
            SQL3 = "SELECT codigo_postal FROM ps.ciudad WHERE nombre_ciudad = (%s)"
            data3 = (self.nombre_ciudad,)
            sentencia.execute(SQL3, data3)
            self.codigo_postal = sentencia.fetchone()

            SQL4 = "SELECT nombre_cine FROM ps.cine WHERE codigo_postal = (%s)"
            data4 = (self.codigo_postal[0],)
            sentencia.execute(SQL4, data4)
            self.cines = sentencia.fetchall()

        self.lista_cine["values"] = self.cines
        self.lista_cine.place(x = 160, y = 100, width = 530)
        self.lista_cine.bind("<<ComboboxSelected>>", self.enableWidgets3)

        self.boton_ok = Button(self, text = "Ok", state = 'disabled', command = self.mostrar_pelicula)
        self.boton_ok.place(x = 700, y = 100)

    def enableWidgets3(self, event):
        self.boton_ok.config(state = 'normal')
        self.nombre_cine = self.lista_cine.get()

    def mostrar_pelicula(self):
        self.pelicula = Label(self, text = "Escoja pelicula: ", bg = "pink").place(x = 20, y = 140, width = 130)
        self.lista_pel = ttk.Combobox(self, state = "readonly")

        with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
            SQL5 = "SELECT nombre_pelicula FROM ps.pelicula"
            sentencia.execute(SQL5)
            self.peliculas = sentencia.fetchall()

        self.lista_pel["values"] = self.peliculas
        self.lista_pel.place(x = 160, y = 140, width = 530)
        self.lista_pel.bind("<<ComboboxSelected>>", self.enableWidgets4)

        self.boton_ok = Button(self, text = "Ok", state = 'disabled', command = self.mostrar_funcion)
        self.boton_ok.place(x = 700, y = 140)

    def enableWidgets4(self, event):
        self.boton_ok.config(state = 'normal')
        self.nombre_pelicula = self.lista_pel.get()
        with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
            SQL6 = "SELECT id_pelicula FROM ps.pelicula WHERE nombre_pelicula = (%s)"
            data6 = (self.nombre_pelicula,)
            sentencia.execute(SQL6, data6)
            self.id_pel = sentencia.fetchone()

    def mostrar_funcion(self):
        self.funciones = Label(self, text = "Función: ",bg = "pink").place(x = 20, y = 180, width = 130)
        self.lista_fun = ttk.Combobox(self, state = "readonly")

        with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
            SQL7 = "SELECT id_funcion, fecha FROM ps.funcion WHERE nombre_cine = (%s) AND id_pelicula = (%s)"
            data7 = (self.nombre_cine, self.id_pel[0],)
            sentencia.execute(SQL7, data7)
            self.funciones = sentencia.fetchall()

        self.lista_fun["values"] = self.funciones
        self.lista_fun.place(x = 160, y = 180, width = 150)
        self.lista_fun.bind("<<ComboboxSelected>>", self.enableWidgets5)

        self.boton_ok = Button(self, text = "Ok", state = 'disabled', command = self.datos_actuales)
        self.boton_ok.place(x = 320, y = 180)

    def enableWidgets5(self, event):
        self.boton_ok.config(state = 'normal')
        self.funcion = self.lista_fun.get()
        self.fun = self.funcion.split(" ")

        with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
            SQL7 = "SELECT formato FROM ps.funcion WHERE id_funcion = (%s)"
            data7 = (self.fun[0],)
            sentencia.execute(SQL7, data7)
            self.actual_formato = sentencia.fetchone()

            SQL7 = "SELECT fecha FROM ps.funcion WHERE id_funcion = (%s)"
            data7 = (self.fun[0],)
            sentencia.execute(SQL7, data7)
            self.actual_fecha = sentencia.fetchone()

            SQL7 = "SELECT numero_sala FROM ps.funcion WHERE id_funcion = (%s)"
            data7 = (self.fun[0],)
            sentencia.execute(SQL7, data7)
            self.actual_sala = sentencia.fetchone()

            SQL7 = "SELECT hora_inicio FROM ps.funcion WHERE id_funcion = (%s)"
            data7 = (self.fun[0],)
            sentencia.execute(SQL7, data7)
            self.actual_hora = sentencia.fetchone()

    def datos_actuales(self):
        self.cambiar()
        self.datos = Label(self, text = "Datos actuales", bg = "pink").place(x = 140, y = 230, width = 150, height = 40)
        self.formato_actual = Label(self, text = "Formato: ", bg = "lavender").place(x = 100, y = 290, width = 100)
        self.formato_actual1 = Label(self, text = self.actual_formato, bg = "sky blue").place(x = 210, y = 290, width = 150)
        self.fecha_actual = Label(self, text = "Fecha: ", bg = "lavender").place(x = 100, y = 320, width = 100)
        self.fecha_actual1 = Label(self, text = self.actual_fecha, bg = "sky blue").place(x = 210, y = 320, width = 150) 
        self.sala_actual = Label(self, text = "Sala: ", bg = "lavender").place(x = 100, y = 350, width = 100)
        self.sala_actual1 = Label(self, text = self.actual_sala, bg = "sky blue").place(x = 210, y = 350, width = 150)
        self.horario_actual = Label(self, text = "Hora: ", bg = "lavender").place(x = 100, y = 380, width = 100)
        self.horario_actual1 = Label(self, text = self.actual_hora, bg = "sky blue").place(x = 210, y = 380, width = 150)

    def cambiar(self):
        self.cambio = Label(self, text = '¿Qué desea modificar?', bg = 'steelblue').place(x = 430, y = 230, width = 200, height = 50)
        self.boton1 = Button(self, text = 'Formato', command = self.mostrar_formato)
        self.boton1.place(x = 430, y = 300, width = 100, height = 40)
        self.boton2 = Button(self, text = 'Fecha', command = self.mostrar_fecha)
        self.boton2.place(x = 550, y = 300, width = 100, height = 40)
        self.boton3 = Button(self, text = 'Sala', command = self.mostrar_salas)
        self.boton3.place(x = 430, y = 350, width = 100, height = 40)
        self.boton4 = Button(self, text = 'Horario', command = self.mostrar_hora)
        self.boton4.place(x = 550, y = 350, width = 100, height = 40)

    def mostrar_formato(self):
        self.top = Toplevel(self)
        self.top.geometry("350x200")
        self.formato = Label(self.top, text="Formato: ", bg = "coral").place(x = 20, y = 20, width = 200, height = 50)
        self.lista_form = ttk.Combobox(self.top, state = "readonly")
        self.lista_form["values"] = ["2D", "3D", "4D", "XD"]
        self.lista_form.place(x = 40, y = 100,  width = 150)
        self.lista_form.bind("<<ComboboxSelected>>", self.enableWidgets6)

        self.boton_ok = Button(self.top, text = "Ok", state = 'disabled', command = self.salir_formato)
        self.boton_ok.place(x = 210, y = 100)

    def salir_formato(self):
        self.top.destroy()
        self.formato_nuevo = Label(self, text = self.formato_funcion, bg = "wheat1").place(x = 210, y = 290, width = 150)

    def enableWidgets6(self, event):
        self.boton_ok.config(state = 'normal')
        self.formato_funcion = self.lista_form.get()

    def mostrar_fecha(self):
        self.now = datetime.now()
        self.top = Toplevel(self)
        self.fecha = Calendar(self.top, font = "Arial 14", selectmode = 'day', cursor = "hand1", year = self.now.year, month = self.now.month, day = self.now.day)
        self.fecha.pack(fill = "both", expand = True)
        self.ok = Button(self.top, text = "Ok", command = self.salir_fecha).pack()

    def salir_fecha(self):
        self.top.destroy()
        self.fecha_funcion = self.fecha.selection_get()
        self.fecha_nueva = Label(self, text = self.fecha_funcion, bg = 'wheat1').place(x = 210, y = 320, width = 150)

    def mostrar_salas(self):
        self.top = Toplevel(self)
        self.top.geometry("350x200")
        self.salas = Label(self.top, text = "Salas disponibles: ",bg = "coral", wraplength = 90).place(x = 20, y = 20, width = 200, height = 50)
        self.lista_salas = ttk.Combobox(self.top, state = "readonly")
        
        if self.formato_funcion != ["2D", "3D", "4D", "XD"]:
            with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
                SQL1 = "SELECT numero_sala FROM ps.sala WHERE tipo_sala = (%s) AND nombre_cine = (%s)"
                data1 = (self.actual_formato[0], self.nombre_cine,)
                sentencia.execute(SQL1, data1)
                self.salas = sentencia.fetchall()
        elif self.formato_funcion == ["2D", "3D", "4D", "XD"]:
            with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
                SQL8 = "SELECT numero_sala FROM ps.sala WHERE tipo_sala = (%s) AND nombre_cine = (%s)"
                data8 = (self.actual_formato[0], self.nombre_cine,)
                sentencia.execute(SQL8, data8)
                self.salas = sentencia.fetchall()

        self.lista_salas["values"] = self.salas
        self.lista_salas.place(x = 40, y = 100, width = 150)
        self.lista_salas.bind("<<ComboboxSelected>>", self.enableWidgets7)

        self.boton_ok = Button(self.top, text = "Ok", state = 'disabled', command = self.salir_sala)
        self.boton_ok.place(x = 210, y = 100)

    def salir_sala(self):
        self.top.destroy()
        self.sala_nueva = Label(self, text = self.salas_disponibles, bg = "wheat1").place(x = 210, y = 350, width = 150)

    def enableWidgets7(self, event):
        self.boton_ok.config(state = 'normal')
        self.salas_disponibles = self.lista_salas.get()

    def mostrar_hora(self):
        self.top = Toplevel(self)
        self.top.geometry("350x200")
        self.hora_fun = Label(self.top, text = "Hora: ",bg = "orange red", wraplength = 90).place(x = 20, y = 20, width = 200, height = 50)
        self.lista_hora = Entry(self.top)
        self.lista_hora.place(x = 40, y = 100, width = 150)
        
        self.boton_ok = Button(self.top, text = "Ok", state = 'normal', command = self.salir_hora)
        self.boton_ok.place(x = 210, y = 100)

    def salir_hora(self):
        self.top.destroy()
        self.hora_funcion = self.lista_hora.get()
        self.hora_nueva = Label(self, text = self.hora_funcion, bg = "wheat1").place(x = 210, y = 380, width = 150)

    def show(self):
        self.update()
        self.deiconify()

    def volverAtras(self):
        self.destroy()
        self.wind.show()

    def actualizar_BD_funciones(self):
        if self.formato_funcion:
            pass


class Eliminar_pel(Toplevel):
    def __init__(self, wind):
        self.wind = wind
        Toplevel.__init__(self)
        self.dsnBaseDatos = "user=bdi2019p password=bdi2019p host=plop.inf.udec.cl dbname=bdi2019p port=5432"

        self.title("Eliminar películas")
        self.resizable(0, 0)
        self.geometry("800x500")
        self.config(bg = 'dimgray')

        self.nombre_pelicula = StringVar()
        self.pelicula = Label(self, text = "Escoja película: ", bg = "pink").place(x = 100, y = 100, width = 130)
        self.lista_pel = ttk.Combobox(self, state = "readonly")

        with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
            SQL5 = "SELECT nombre_pelicula FROM ps.pelicula"
            sentencia.execute(SQL5)
            self.peliculas = sentencia.fetchall()

        self.lista_pel["values"] = self.peliculas
        self.lista_pel.place(x = 240, y = 100, width = 400)

        self.boton_ok = Button(self, text = "Ok", state = 'normal', command = self.comprobar_datos)
        self.boton_ok.place(x = 660, y = 100)

        self.boton_eliminar = Button(self, text = "Eliminar", state = 'disable', command = self.eliminar_BD_peliculas)
        self.boton_eliminar.place(x = 300, y = 450)

        self.botonVolver = Button(self, text = 'atrás', command = self.volverAtras)
        self.botonVolver.place(x = 10, y = 10, width = 40, height = 20)

    def show(self):
        self.update()
        self.deiconify()

    def volverAtras(self):
        self.destroy()
        self.wind.show()

    def comprobar_datos(self):
        self.nombre_pelicula = self.lista_pel.get()
        self.boton_eliminar.config(state = 'normal')
        with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
            SQL6 = "SELECT id_pelicula FROM ps.pelicula WHERE nombre_pelicula = (%s)"
            data6 = (self.nombre_pelicula,)
            sentencia.execute(SQL6, data6)
            self.peliculas = sentencia.fetchall()

    def eliminar_BD_peliculas(self):
        with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
            SQL7 = "DELETE FROM ps.pelicula WHERE id_pelicula = (%s)"
            data7 = (self.peliculas[0])
            sentencia.execute(SQL7, data7)

            SQL8 = "DELETE FROM ps.generopelicula WHERE id_pelicula = (%s)"
            data8 = (self.peliculas[0])
            sentencia.execute(SQL8, data8)
            #eliminar tambien funciones que dependan

        self.volverAtras()


class Eliminar_fun(Toplevel):
    def __init__(self, wind):
        self.wind = wind
        Toplevel.__init__(self)
        self.dsnBaseDatos = "user=bdi2019p password=bdi2019p host=plop.inf.udec.cl dbname=bdi2019p port=5432"

        self.title("Eliminar funciones")
        self.resizable(0, 0)
        self.geometry("800x500")
        self.config(bg = 'dimgray')

        self.nombre_region = StringVar()
        self.nombre_ciudad = StringVar()
        self.nombre_cine = StringVar()
        self.nombre_pelicula = StringVar()
        self.funciones = StringVar()

        self.region = Label(self, text = "Región: ", bg = "pink").place(x = 100, y = 100, width = 130)
        self.lista_reg = ttk.Combobox(self, state = "readonly")

        with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
            SQL = "SELECT region FROM ps.ciudadyregion"
            sentencia.execute(SQL)
            self.regiones = sentencia.fetchall()

        self.lista_reg["values"] = self.regiones
        self.lista_reg.place(x = 240, y = 100, width = 150)
        self.lista_reg.bind("<<ComboboxSelected>>", self.enableWidgets1)

        self.boton_ok = Button(self, text = "Ok", state = 'disabled', command = self.mostrar_ciudad)
        self.boton_ok.place(x = 400, y = 100)

        self.boton_eliminar = Button(self, text = "Eliminar", state = 'disabled', command = self.eliminar_BD_funciones)
        self.boton_eliminar.place(x = 300, y = 450)

        self.botonVolver = Button(self, text = 'atrás', command = self.volverAtras)
        self.botonVolver.place(x = 10, y = 10, width = 40, height = 20)

    def enableWidgets1(self, event):
        self.boton_ok.config(state = 'normal')
        self.nombre_region = self.lista_reg.get()

    def mostrar_ciudad(self):
        self.ciudad = Label(self, text = "Ciudad: ", bg = "pink").place(x = 100, y = 150, width = 130)
        self.lista_ciu = ttk.Combobox(self, state = "readonly")

        with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
            SQL1 = "SELECT nombre_ciudad FROM ps.ciudadyregion WHERE region = (%s)"
            data1 = (self.nombre_region,)
            sentencia.execute(SQL1, data1)
            self.ciudades = sentencia.fetchall()

        self.lista_ciu["values"] = self.ciudades
        self.lista_ciu.place(x = 240, y = 150, width = 150)
        self.lista_ciu.bind("<<ComboboxSelected>>", self.enableWidgets2)

        self.boton_ok = Button(self, text = "Ok", state = 'disabled', command = self.mostrar_cine)
        self.boton_ok.place(x = 400, y = 150)

    def enableWidgets2(self, event):
        self.boton_ok.config(state = 'normal')
        self.nombre_ciudad = self.lista_ciu.get()

    def mostrar_cine(self):
        self.cine = Label(self, text = "Cine: ", bg = "pink").place(x = 100, y = 200, width = 130)
        self.lista_cine = ttk.Combobox(self, state = "readonly")

        with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
            SQL3 = "SELECT codigo_postal FROM ps.ciudad WHERE nombre_ciudad = (%s)"
            data3 = (self.nombre_ciudad,)
            sentencia.execute(SQL3, data3)
            self.codigo_postal = sentencia.fetchone()

            SQL4 = "SELECT nombre_cine FROM ps.cine WHERE codigo_postal = (%s)"
            data4 = (self.codigo_postal[0],)
            sentencia.execute(SQL4, data4)
            self.cines = sentencia.fetchall()

        self.lista_cine["values"] = self.cines
        self.lista_cine.place(x = 240, y = 200, width = 150)
        self.lista_cine.bind("<<ComboboxSelected>>", self.enableWidgets3)

        self.boton_ok = Button(self, text = "Ok", state = 'disabled', command = self.mostrar_pelicula)
        self.boton_ok.place(x = 400, y = 200)

    def enableWidgets3(self, event):
        self.boton_ok.config(state = 'normal')
        self.nombre_cine = self.lista_cine.get()

    def mostrar_pelicula(self):
        self.pelicula = Label(self, text = "Pelicula: ", bg = "pink").place(x = 100, y = 250, width = 130)
        self.lista_pel = ttk.Combobox(self, state = "readonly")

        with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
            SQL5 = "SELECT nombre_pelicula FROM ps.pelicula"
            sentencia.execute(SQL5)
            self.peliculas = sentencia.fetchall()

        self.lista_pel["values"] = self.peliculas
        self.lista_pel.place(x = 240, y = 250, width = 400)
        self.lista_pel.bind("<<ComboboxSelected>>", self.enableWidgets4)

        self.boton_ok = Button(self, text = "Ok", state = 'disabled', command = self.mostrar_funcion)
        self.boton_ok.place(x = 650, y = 250)

    def enableWidgets4(self, event):
        self.boton_ok.config(state = 'normal')
        self.nombre_pelicula = self.lista_pel.get()

    def mostrar_funcion(self):
        self.funcion = Label(self, text = "Función: ", bg = "pink").place(x = 100, y = 300, width = 130)
        self.lista_fun = ttk.Combobox(self, state = "readonly")

        with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
            SQL6 = "SELECT id_pelicula FROM ps.pelicula WHERE nombre_pelicula = (%s)"
            data6 = (self.nombre_pelicula,)
            sentencia.execute(SQL6, data6)
            self.id_pel = sentencia.fetchone()

            SQL7 = "SELECT id_funcion, fecha FROM ps.funcion WHERE id_pelicula = (%s)"
            data7 = (self.id_pel[0],)
            sentencia.execute(SQL7, data7)
            self.funciones = sentencia.fetchall()

        self.lista_fun["values"] = self.funciones
        self.lista_fun.place(x = 240, y = 300, width = 400)
        self.lista_fun.bind("<<ComboboxSelected>>", self.enableWidgets5)

        self.boton_ok = Button(self, text = "Ok", state = 'disabled', command = self.comprobar_datos)
        self.boton_ok.place(x = 650, y = 300)

    def enableWidgets5(self, event):
        self.boton_ok.config(state = 'normal')
        self.funcion = self.lista_fun.get()
        self.fun = self.funcion.split(" ")

    def show(self):
        self.update()
        self.deiconify()

    def volverAtras(self):
        self.destroy()
        self.wind.show()

    def comprobar_datos(self):
        self.boton_eliminar.config(state = 'normal')

    def eliminar_BD_funciones(self):
        with ConexionBaseDeDatos(self.dsnBaseDatos) as sentencia:
            SQL9 = "DELETE FROM ps.funcion WHERE id_funcion = (%s)"
            data9 = (self.fun[0],)           
            sentencia.execute(SQL9, data9)
        self.volverAtras()


if __name__ == '__main__':


    parent = Tk()
    app = Ventana_principal(parent)
    parent.mainloop()
