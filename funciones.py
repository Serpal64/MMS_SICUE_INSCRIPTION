#Biblioteca para utilizar la base de datos
import sqlite3

from tabulate import tabulate

def manejarLogin():
    while True:
        usuario = input('Nombre de Usuario: ')
        password = input('Contraseña: ')
        conexion = sqlite3.connect('BaseDeDatos.db')
        cursorBD = conexion.cursor()
        cursorBD.execute(' SELECT rol, idGrado, curso, idUser FROM login WHERE usuario=? AND contrasena=? ', (usuario, password))
        resultado = cursorBD.fetchone()
        conexion.close()
        if resultado:
            #Devuelve el rol de ese usuario con esa contraseña
            return resultado
        else:
            print('\nNOMBRE DE USUARIO Y/O CONTRASEÑA INCORRECTOS\n')
           
def menu():
    print('\n¡¡¡Bienvenido a SICUE!!!\n')
    datosUser = manejarLogin()
    if datosUser[0] == 'Administrador':
        while True:
            print('\n---------- MENU DEL ADMINISTRADOR ----------\n')
            print('\t1. Crear un Plan de Convalidación')
            print('\t2. Crear un Plan de Intercambio')
            print ('\t3. Salir del Programa')
            select = input ('\nSelecciona una opción del menú: ')
            if select.isdigit():
                select = int(select)
                if select == 1:
                    print ('\nCREANDO PLAN DE CONVALIDACIÓN...')
                    idConvenio = crearPlan()
                    imprimirPlan(idConvenio)
                elif select == 2:
                    print('\nCREANDO PLAN DE INTERCAMBIO')
                    crearPlanIntercambio()
                elif select == 3:
                    print('\nSALIENDO DEL PROGRAMA...\n')
                    break
                else:
                    print('NÚMERO NO VÁLIDO. POR FAVOR, INTRODUCE UN NÚMERO QUE SE ENCUENTRE DENTRO DEL RANGO [1-2]')
            else:
                print('ENTRADA NO VÁLIDA. POR FAVOR, INTRODUCE UN NÚMERO')
    elif datosUser[0] == 'Alumno':
        while True:
            print('\n---------- MENU DEL ALUMNO ----------\n')
            print('\t1. Inscripción en un Plan de Convalidación')
            print('\t2. Consultar mis inscripciones')
            print('\t3. Borrar una inscripción activa')
            print ('\t4. Salir del Programa')
            select = input ('\nSelecciona una opción del menú: ')
            if select.isdigit():
                select = int(select)
                if select == 1:
                    menuPlanes(datosUser[1], datosUser[2], datosUser[3])
                elif select == 2:
                    consultarInscripcionesAlumno(datosUser[3])
                elif select == 3:
                    idConvenio = consultarInscripcionesAlumno(datosUser[3])
                    if idConvenio!=0:
                        while True:
                            opcion = input('\n¿Desea realmente anular la inscripción? (s/n)')
                            if opcion=='s':
                                borrarInscripcion(idConvenio, datosUser[3])
                                break
                            elif opcion=='n':
                                print('\nOPERACIÓN ANULADA')
                                break
                            else:
                                print('\nENTRADA INVÁLIDA. INTRODUCE s(sí) SI CONFIRMA LA ANULACIÓN O n(no) SI NO CONFIRMA')
                elif select == 4:
                    print('\nSALIENDO DEL PROGRAMA...\n')
                    break
                else:
                    print('\nNÚMERO NO VÁLIDO. POR FAVOR, INTRODUCE UN NÚMERO QUE SE ENCUENTRE DENTRO DEL RANGO [1-4]')
            else:
                print('\nENTRADA NO VÁLIDA. POR FAVOR, INTRODUCE UN NÚMERO')

    else:
        while True:
            print('\n---------- MENU DEL PROFESOR ----------\n')
            print('\t1. Inscripción en un Programa de Intercambio')
            print('\t2. Consultar mis inscripciones')
            print('\t3. Borrar una inscripción activa')
            print ('\t4. Salir del Programa')
            select = input ('\nSelecciona una opción del menú: ')
            if select.isdigit():
                select = int(select)
                if select == 1:
                    menuUnis(datosUser[1])
                elif select == 2:
                    consultarInscripcionesProfesor(datosUser[3])
                elif select == 3:
                    print('Anular inscripciones')
                elif select == 4:
                    print('\nSALIENDO DEL PROGRAMA...\n')
                    break
                else:
                    print('\nNÚMERO NO VÁLIDO. POR FAVOR, INTRODUCE UN NÚMERO QUE SE ENCUENTRE DENTRO DEL RANGO [1-4]')
            else:
                print('\nENTRADA NO VÁLIDA. POR FAVOR, INTRODUCE UN NÚMERO')            

def ListaUniversidades(cursorBD):
    cursorBD.execute(' SELECT nombre, ciudad FROM universidades WHERE idUni!=1')
    return cursorBD.fetchall()

def ListaCentros(cursorBD, idUni):
    cursorBD.execute('SELECT nombre FROM centros WHERE idUni=?', (idUni,))
    return cursorBD.fetchall()

def ListaGradosCentro(cursorBD, idCentro):
    cursorBD.execute('SELECT nombre FROM grados WHERE idCentro=?', (idCentro,))
    return cursorBD.fetchall()

def crearUniversidad(cursorBD):
    nombre = input('\nNombre de la Universidad: ')
    ciudad = input('Ciudad donde se ubica: ')
    cursorBD.execute('INSERT INTO universidades(nombre, ciudad) VALUES (?, ?)', (nombre, ciudad))
    return cursorBD.lastrowid

def crearCentro(cursorBD, idUni):
    nombre = input('\nNombre del nuevo centro: ')
    cursorBD.execute(' INSERT INTO centros(nombre, idUni) VALUES(?,?)', (nombre, idUni))
    return cursorBD.lastrowid

def crearGrado(cursorBD, idCentro):
    nombre = input('\nNombre del nuevo grado: ')
    cursorBD.execute(' INSERT INTO grados(nombre, idCentro) VALUES(?, ?)', (nombre, idCentro))
    return cursorBD.lastrowid

def crearConvenio(cursorBD, idGradoOrigen, idGradoDestino, curso, duracion):
    cursorBD.execute(' INSERT INTO convenios(idGradoOrigen, idGradoDestino, curso, duracion) VALUES(?,?,?,?)', (idGradoOrigen, idGradoDestino, curso, duracion))

def buscarUniversidad(cursorBD, nombre, ciudad):
    cursorBD.execute('SELECT idUni FROM universidades WHERE nombre=? AND ciudad=?', (nombre, ciudad))
    resultado = cursorBD.fetchone()
    return resultado[0]

def buscarCentro(cursorBD, nombre, idUni):
    cursorBD.execute('SELECT idCentro FROM centros WHERE nombre=? AND idUni=?', (nombre, idUni))
    resultado = cursorBD.fetchone()
    return resultado[0]

def buscarGrado(cursorBD, nombre, idCentro):
    cursorBD.execute('SELECT idGrado FROM grados WHERE nombre=? AND idCentro=?', (nombre, idCentro))
    resultado = cursorBD.fetchone()
    return resultado[0]

def buscarCursosComunes(cursorBD, idgradoOrigen, idgradoDestino):
    cursorBD.execute(' SELECT DISTINCT curso FROM asignaturas WHERE idGrado=? ', (idgradoOrigen,))
    cursosGradoOrigen = set(row[0] for row in cursorBD.fetchall())

    cursorBD.execute(' SELECT DISTINCT curso FROM asignaturas WHERE idGrado=? ', (idgradoDestino,))
    cursosGradoDestino = set(row[0] for row in cursorBD.fetchall())

    cursosComunes = list(cursosGradoOrigen.intersection(cursosGradoDestino))
    return cursosComunes

def buscarDuracionComun(cursorBD, idgradoOrigen, idgradoDestino, curso):
    cursorBD.execute('SELECT DISTINCT cuatrimestre FROM asignaturas WHERE idGrado=? AND curso=?', (idgradoOrigen, curso))
    cuatrimestresOrigen = set(row[0] for row in cursorBD.fetchall())

    cursorBD.execute('SELECT DISTINCT cuatrimestre FROM asignaturas WHERE idGrado=? AND curso=?', (idgradoDestino, curso))
    cuatrimestresDestino = set(row[0] for row in cursorBD.fetchall())

    cuatrimestresComunes = list(cuatrimestresOrigen.intersection(cuatrimestresDestino))
    return cuatrimestresComunes

def consultarExistenciaConvenio (cursorBD, idGradoOrigen, idGradoDestino, curso, duracion):
    cursorBD.execute ('SELECT idConvenio FROM convenios WHERE idGradoOrigen=? AND idGradoDestino=? AND curso=? AND duracion=?', (idGradoOrigen, idGradoDestino, curso, duracion))
    resultado = cursorBD.fetchone()
    return resultado

def crearPlan():
    conexion = sqlite3.connect('BaseDeDatos.db')
    cursorBD = conexion.cursor()

    #Imprimimos los centros de la Universidad de Origen (UCO) o permitimos crear un nuevo centro de la UCO
    while True:
        centrosUCO = ListaCentros(cursorBD, '1')
        i = 1
        print('\nCENTROS DE LA UCO:')
        for centroUCO in centrosUCO:
            print(f'\t{i}. {centroUCO[0]}')
            i = i + 1
        opcion = input('\nSelecciona un centro: ')
        if opcion.isdigit():
            opcion=int(opcion)
            if 0 < opcion < i:
                idCentroUCO = buscarCentro(cursorBD, centrosUCO[opcion-1][0], '1')
                break
            else:
                print(f'\nNÚMERO INVÁLIDO. POR FAVOR, INTRODUCE UN NÚMERO DENTRO DEL RANGO [1, {i-1}]')
        else:
            print('\nENTRADA INVÁLIDA. POR FAVOR, INTRODUCE UN NÚMERO')

    #Imprimimos los grados de ese centro seleccionado de la UCO o permitimos crear un nuevo grado en ese centro de la UCO
    while True:
        gradosCentroUCO = ListaGradosCentro(cursorBD, idCentroUCO)
        i = 1
        print('\nGRADOS EN ESE CENTRO DE LA UCO:')
        for gradoCentroUCO in gradosCentroUCO:
            print(f'\t{i}. {gradoCentroUCO[0]}')
            i = i + 1
        opcion = input('\nSelecciona un grado: ')
        if opcion.isdigit():
            opcion=int(opcion)
            if 0 < opcion < i:
                idgradoUCO = buscarGrado(cursorBD, gradosCentroUCO[opcion - 1][0], idCentroUCO)
                break
            else:
                print(f'\nNÚMERO INVÁLIDO. POR FAVOR, INTRODUCE UN NÚMERO DENTRO DEL RANGO [1, {i-1}]')
        else:
            print('\nENTRADA INVÁLIDA. POR FAVOR, INTRODUCE UN NÚMERO')


    #Imprimimos las universidades existentes en la base de datos (menos UCO) y permitimos seleccionar una de ellas o crear una universidad nueva
    while True:
        universidades = ListaUniversidades(cursorBD)
        i = 1
        print('\nUNIVERSIDADES DE DESTINO:')
        for universidad in universidades:
            print(f'\t{i}. Universidad: {universidad[0]}, Ciudad: {universidad[1]}')
            i = i + 1
        opcion = input('\nSelecciona una Universidad de Destino: ')
        if opcion.isdigit():
            opcion=int(opcion)
            if 0 < opcion < i:
                idUniDestino = buscarUniversidad(cursorBD, universidades[opcion-1][0], universidades[opcion-1][1])
                break
            else:
                print(f'\nNÚMERO INVÁLIDO. POR FAVOR, INTRODUCE UN NÚMERO DENTRO DEL RANGO [1, {i-1}]')
        else:
            print('\nENTRADA INVÁLIDA. POR FAVOR, INTRODUCE UN NÚMERO')

    
    #Imprimimos los centros de la Universidad de Destino seleccionada o permitimos crear un nuevo centro para esa universidad de destino
    while True:
        centrosUniDestino = ListaCentros(cursorBD, idUniDestino)
        i = 1
        print('\nCENTROS DE LA UNIVERSIDAD DE DESTINO:')
        for centroUniDestino in centrosUniDestino:
            print(f'\t{i}. {centroUniDestino[0]}')
            i = i + 1
        opcion = input('\nSelecciona un centro: ')
        if opcion.isdigit():
            opcion=int(opcion)
            if 0 < opcion < i:
                idCentroUniDestino = buscarCentro(cursorBD, centrosUniDestino[opcion-1][0], idUniDestino)
                break
            else:
                print(f'\nNÚMERO INVÁLIDO. POR FAVOR, INTRODUCE UN NÚMERO DENTRO DEL RANGO [1, {i-1}]')
        else:
            print('\nENTRADA INVÁLIDA. POR FAVOR, INTRODUCE UN NÚMERO')

    #Imprimimos los grados de ese centro seleccionado de la universidad de destino o permitimos crear un nuevo grado en ese centro de esa universidad de destino
    while True:
        gradosCentroUniDestino = ListaGradosCentro(cursorBD, idCentroUniDestino)
        i = 1
        print('\nGRADOS EN ESE CENTRO:')
        for gradoCentroUniDestino in gradosCentroUniDestino:
            print(f'\t{i}. {gradoCentroUniDestino[0]}')
            i = i + 1
        opcion = input('\nSelecciona un grado: ')
        if opcion.isdigit():
            opcion=int(opcion)
            if 0 < opcion < i:
                idgradoUniDestino = buscarGrado(cursorBD, gradosCentroUniDestino[opcion - 1][0], idCentroUniDestino)
                break
            else:
                print(f'\nNÚMERO INVÁLIDO. POR FAVOR, INTRODUCE UN NÚMERO DENTRO DEL RANGO [1, {i-1}]')
        else:
            print('\nENTRADA INVÁLIDA. POR FAVOR, INTRODUCE UN NÚMERO')

    #Selecciona el curso que es a partir de 2º curso y no llega a más del 5º curso
    while True:
        cursos = buscarCursosComunes(cursorBD, idgradoUCO, idgradoUniDestino)
        i = 1
        print('\nCURSOS DISPONIBLES PARA ESOS GRADOS:')
        if not cursos:
            print ('\nNO EXISTE UN CURSO PARA ESOS GRADOS')
            return
        for curse in cursos:
            print(f'\t{i}. Curso {curse}º')
            i = i + 1
        opcion = input('\nSelecciona un curso: ')
        if opcion.isdigit():
            opcion=int(opcion)
            if 0 < opcion < i:
                curso = cursos[opcion-1]
                print(f'\nCURSO SELECCIONADO: {curso}')
                break
            else:
                print(f'\nNÚMERO INVÁLIDO. POR FAVOR, INTRODUCE UN NÚMERO DENTRO DEL RANGO [1, {i-1}]')
        else:
            print('\nENTRADA INVÁLIDA. POR FAVOR, INTRODUCE UN NÚMERO')

    #Selecciona la Duración del Plan de Convalidación
    while True:
        cuatrimestres = buscarDuracionComun(cursorBD, idgradoUCO, idgradoUniDestino, curso)
        print('\nDURACIÓN DEL PLAN DE CONVALIDACIÓN:')
        if cuatrimestres == None:
            print('\nNO EXISTE UNA DURACIÓN PARA ESOS GRADOS Y ESE CURSO')
            break
        aux=0
        for tiempo in cuatrimestres:
            if aux == 0:
                print(f'\t1. {tiempo}º Cuatrimestre')
                aux = tiempo
            else:
                print(f'\t2. {tiempo}º Cuatrimestre')
                print('\t3. Curso Completo')
        opcion = input('\nSelecciona una duración: ')
        if opcion.isdigit():
            opcion=int(opcion)
            if 0 < opcion < 4:
                if opcion == 1 or opcion == 2:
                    aux = cuatrimestres[opcion - 1]
                    nAsignaturas = 5
                    if aux == 1:
                        duracion = '1_cuatri'
                        cuatrimestre1= '1'
                        cuatrimestre2= '0'
                        print(f'\nDURACIÓN SELECCIONADA: {duracion}')
                        break
                    else:
                        duracion = '2_cuatri'
                        cuatrimestre1 = '0'
                        cuatrimestre2 = '2'
                        print(f'\nDURACIÓN SELECCIONADA: {duracion}')
                        break
                else:
                    duracion = 'curso_completo'
                    cuatrimestre1 = '1'
                    cuatrimestre2 = '2'
                    print(f'\nDURACIÓN SELECCIONADA: {duracion}')
                    nAsignaturas = 10
                    break
            else:
                print('\nNÚMERO INVÁLIDO. POR FAVOR, INTRODUCE UN NÚMERO DENTRO DEL RANGO [1, 4]')
        else:
            print('\nENTRADA INVÁLIDA. POR FAVOR, INTRODUCE UN NÚMERO')

    #Vemos si ya está creado el convenio y si no existe, lo creamos
    resultado = consultarExistenciaConvenio(cursorBD, idgradoUCO, idgradoUniDestino, curso, duracion) #Devuelve una tupla
    if resultado == None:
        crearConvenio(cursorBD, idgradoUCO, idgradoUniDestino, curso, duracion)
        idConvenio = consultarExistenciaConvenio(cursorBD, idgradoUCO, idgradoUniDestino, curso, duracion) #Devuelve una tupla
        print('\nCONVENIO CREADO CON ÉXITO')

        asignaturasOrigen = obtenerAsignaturas(cursorBD, idgradoUCO, curso, cuatrimestre1, cuatrimestre2)
        for asignaturaOrigen in asignaturasOrigen:
            print(f'\nEQUIVALENCIA DE LA ASIGNATURA {asignaturaOrigen[0]}:')
            eleccionAsignaturaDestino(cursorBD, idgradoUniDestino, curso, asignaturaOrigen[2], asignaturaOrigen[1], idConvenio[0]) #Ponemos idConvenio[0] para quitar la tupla
        
    else:
        idConvenio = resultado #Es una tupla
        print('\nESTE CONVENIO YA ESTÁ CREADO')
    
    conexion.commit()
    conexion.close()
    return idConvenio[0] #Ponemos idConvenio[0] para quitar la tupla

def imprimirPlan(idConvenio):
    conexion = sqlite3.connect('BaseDeDatos.db')
    cursorBD = conexion.cursor()
    cursorBD.execute(''' SELECT uo.nombre, co.nombre, go.nombre, ao.nombre, ad.nombre, gd.nombre, cd.nombre, ud.nombre, c.curso, c.duracion
                    FROM equivalenciasAsignaturas e
                    JOIN convenios c ON e.idConvenio = c.idConvenio
                    JOIN asignaturas ao ON e.idAsignaturaOrigen = ao.idAsignatura
                    JOIN asignaturas ad ON e.idAsignaturaDestino = ad.idAsignatura
                    JOIN grados go ON ao.idGrado = go.idGrado
                    JOIN grados gd ON ad.idGrado = gd.idGrado
                    JOIN centros co ON co.idCentro = go.idCentro
                    JOIN centros cd ON cd.idCentro = gd. idCentro
                    JOIN universidades uo ON co.idUni = uo.idUni
                    JOIN universidades ud ON cd.idUni = ud.idUni
                    WHERE e.idConvenio=?
                    ORDER BY c.idConvenio, e.idEquivalencia ''', (idConvenio,))
    resultados = cursorBD.fetchall()
    conexion.close()
    if not resultados:
        print('\nNO SE OBTUVO NIGÚN PLAN\n')
        return

    datosOrigen = [
        ['Universidad Origen:', resultados[0][0]],
        ['Centro Origen:', resultados[0][1]],
        ['Grado Origen:', resultados[0][2]]
    ]

    print("\n" + tabulate(datosOrigen) + "\n")

    datosDestino = [
        ['Universidad Destino:', resultados[0][7]],
        ['Centro Destino:', resultados[0][6]],
        ['Grado Destino:', resultados[0][5]]
    ]

    print("\n" + tabulate(datosDestino) + "\n")

    datosGeneral = [
        ['Curso:', resultados[0][8]],
        ['Duración:', resultados[0][9]]
    ]

    print("\n" + tabulate(datosGeneral) + "\n")


    asignaturas = []
    for resultado in resultados:
        asignaturas.append([resultado[3], resultado[4]])
    print("\n" + tabulate(asignaturas, headers=["Asignaturas Origen", "Asignaturas Destino"]) + "\n")

def obtenerAsignaturas(cursorBD, idGrado, curso, cuatrimestre1, cuatrimestre2):
    if cuatrimestre2 == '0':
        cursorBD.execute('SELECT nombre, idAsignatura, cuatrimestre FROM asignaturas WHERE idGrado=? AND curso=? AND cuatrimestre=?', (idGrado, curso, cuatrimestre1))
        return cursorBD.fetchall()
    elif cuatrimestre1 == '0':
        cursorBD.execute('SELECT nombre, idAsignatura, cuatrimestre  FROM asignaturas WHERE idGrado=? AND curso=? AND cuatrimestre=?', (idGrado, curso, cuatrimestre2))
        return cursorBD.fetchall()
    else:
        cursorBD.execute('SELECT nombre, idAsignatura, cuatrimestre  FROM asignaturas WHERE idGrado=? AND curso=? AND (cuatrimestre=? OR cuatrimestre=?)', (idGrado, curso, cuatrimestre1, cuatrimestre2))
        return cursorBD.fetchall()

def eleccionAsignaturaDestino(cursorBD, idGrado, curso, cuatrimestre, idAsignaturaOrigen, idConvenio):
    cursorBD.execute('SELECT nombre, idAsignatura FROM asignaturas WHERE idGrado=? AND curso=? AND cuatrimestre=?', (idGrado, curso, cuatrimestre))
    asignaturasDestino = cursorBD.fetchall()
    i = 1
    while True:
        print('\nASIGNATURAS DE DESTINO:')
        for asignaturaDestino in asignaturasDestino:
            print(f'\t{i}. {asignaturaDestino[0]}')
            i = i + 1
        opcion = input('\nSelecciona la equivalencia: ')
        if opcion.isdigit():
            opcion=int(opcion)
            if 0 < opcion < i:
                cursorBD.execute('INSERT INTO equivalenciasAsignaturas(IdConvenio, idAsignaturaOrigen, idAsignaturaDestino) VALUES(?,?,?)', (idConvenio, idAsignaturaOrigen, asignaturasDestino[opcion-1][1]))
                break
            else:
                print(f'\nNÚMERO INVÁLIDO. POR FAVOR, INTRODUCE UN NÚMERO DENTRO DEL RANGO [1, {i-1}]')
        else:
            print('\nENTRADA INVÁLIDA. POR FAVOR, INTRODUCE UN NÚMERO')

def menuPlanes(idGrado, curso, idUser):
    conexion = sqlite3.connect('BaseDeDatos.db')
    cursorBD = conexion.cursor()
    cursorBD.execute(''' SELECT con.idConvenio, g.nombre, c.nombre, u.nombre, con.duracion
                     FROM convenios con
                     JOIN grados g ON g.idGrado=con.idGradoDestino
                     JOIN centros c ON c.idCentro=g.idCentro
                     JOIN universidades u ON u.idUni=c.idUni
                     WHERE con.idGradoOrigen=? AND con.curso=?
                     ORDER BY con.idConvenio''', (idGrado, curso))
    
    planes = cursorBD.fetchall()

    cursorBD.execute('SELECT nombre FROM grados WHERE idGrado=?', (idGrado, ))
    gradoOrigen = cursorBD.fetchone()


    if not planes:
        print('\nNO HAY PLANES PARA EL GRADO EN EL QUE ESTÁ MATRICULADO')
        return
    while True:
        print(f'\nPLANES DISPONIBLES PARA EL {gradoOrigen[0]} EN EL CURSO {curso}º')
        i=1
        for plan in planes:
            print(f'\t{i}. Universidad:{plan[3]}   Centro:{plan[2]}   Grado:{plan[1]}   duracion:{plan[4]}')
            i = i + 1
        opcion = input('Selecciona un plan: ')
        if opcion.isdigit():
            opcion=int(opcion)
            if 0 < opcion < i:
                imprimirPlan(planes[opcion-1][0])
                while True:
                    respuesta = input('\n¿Desea inscribirse a este plan? (s/n): ')
                    if respuesta=='s':
                        comprobarCrearInscripcion(cursorBD, idUser, planes[opcion-1][0])
                        break
                    elif respuesta=='n':
                        print('\nINSCRIPCIÓN NO REALIZADA')
                        break
                    else:
                        print('\nENTRADA INVÁLIDA. POR FAVOR, INTRODUCE s(sí) si CONFIRMA LA INSCRIPCIÓN O n(no) SI NO CONFIRMA LA INSCRIPCIÓN')
            else:
                print(f'\nNÚMERO INVÁLIDO. POR FAVOR, INTRODUCE UN NÚMERO DENTRO DEL RANGO [1, {i-1}]')
        else: 
            print('\nENTRADA INVÁLIDA. POR FAVOR, INTRODUCE UN NÚMERO')
        break

    conexion.commit()
    conexion.close()

def comprobarCrearInscripcion(cursorBD, idUser, idConvenio):
    cursorBD.execute('SELECT idInscripcion, estado FROM inscripciones WHERE idUser=? AND idConvenio=?', (idUser, idConvenio))
    resultado = cursorBD.fetchone()

    if not resultado:
        cursorBD.execute('INSERT INTO inscripciones(idUser, idConvenio, estado) VALUES(?,?,?)', (idUser, idConvenio, 'Activa'))
        print('\nINSCRIPCIÓN CREADA CORRECTAMENTE')
    elif resultado[1]=='Anulada':
        cursorBD.execute('UPDATE inscripciones SET estado="Activa" WHERE idInscripcion=?', (resultado[0],))
        print('\nINSCRIPCIÓN CREADA CON ANTERIORIDAD PERO CON ESTADO ANULADA PASA A ESTADO ACTIVA')
    else:
        print('\nINSCRIPCIÓN CREADA CON ANTERIORIDAD')

def consultarInscripcionesAlumno(idUser):
    conexion = sqlite3.connect('BaseDeDatos.db')
    cursorBD = conexion.cursor()
    cursorBD.execute(''' SELECT u.nombre, c.nombre, g.nombre, con.duracion, con.idConvenio, i.estado
                     FROM inscripciones i
                     JOIN convenios con ON con.idConvenio=i.idConvenio
                     JOIN grados g ON g.idGrado=con.idGradoDestino
                     JOIN centros c ON c.idCentro=g.idCentro
                     JOIN universidades u ON u.idUni=c.idUni
                     WHERE idUser=?
                     ORDER BY u.nombre''', (idUser,))
    resultados = cursorBD.fetchall()
    i = 1
    print('\nMIS INSCRIPCIONES:')
    for resultado in resultados:
        print(f'\t{i}. Universidad:{resultado[0]}   Centro:{resultado[1]}   Grado:{resultado[2]}   Duración:{resultado[3]}   Estado:{resultado[5]}')
        i = i + 1
    print(f'\t{i}. Volver al menú')
    opcion = input('\nSelecciona una opción: ') 
    if opcion.isdigit():
        opcion=int(opcion)
        if 0 < opcion < i:
            imprimirPlan(resultados[opcion-1][4])
            return resultados[opcion-1][4]
        elif opcion==i:
            return 0
        else:
            print(f'\nNÚMERO NO VÁLIDO. POR FAVOR, INTRODUCE UN NÚMERO QUE SE ENCUENTRE DENTRO DEL RANGO [1-{i-1}]')
    else:
        print('\nENTRADA NO VÁLIDA. POR FAVOR, INTRODUCE UN NÚMERO')
    conexion.close()

def borrarInscripcion(idConvenio, idUser):
    conexion = sqlite3.connect('BaseDeDatos.db')
    cursorBD = conexion.cursor()
    cursorBD.execute('SELECT estado FROM inscripciones WHERE idConvenio=? AND idUser=?', (idConvenio, idUser))
    estado = cursorBD.fetchone()
    if estado[0]=='Anulada':
        print('\nESTA INSCRIPCIÓN YA SE HABÍA ANULADO ANTERIORMENTE')
    else:
        cursorBD.execute('UPDATE inscripciones SET estado="Anulada" WHERE idConvenio=? AND idUser=? ', (idConvenio, idUser))
        print('\nINSCRIPCIÓN ANULADA CORRECTAMENTE')
    conexion.commit()
    conexion.close()

def menuUnis(idGrado):
    print('Menu unis intercambio profesor')

def consultarInscripcionesProfesor(idUser):
    print('Inscripciones profesor')

def crearPlanIntercambio():
    print('Crear plan de intercambio entre profesores')

menu()