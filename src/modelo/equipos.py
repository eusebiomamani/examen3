from modelo.Coneccion import conexion2023
from flask import jsonify, request

def buscar_estu(codigo):
    try:
        conn = conexion2023()
        cur = conn.cursor()
        cur.execute("""select * FROM equipos WHERE EquipoID = %s""", (codigo,))
        datos = cur.fetchone()
        conn.close()

        if datos != None:
            estu = { 'EquipoID': datos[0],
                       'NombreEquipo': datos[1], 'Ciudad': datos[2],
                       'Estadio': datos[3]}
            return estu
        else:
            return None
    except Exception as ex:
            raise ex
    

class ModeloEstudiante():
    @classmethod
    def listar_Estudiante(self):
        try:
            conn = conexion2023()
            cursor=conn.cursor()
            cursor.execute("SELECT * FROM equipos")
            datos = cursor.fetchall()
            estudiantes = []

            for fila in datos:
                estu = {' EquipoID': fila[0],
                       'NombreEquipo': fila[1],
                       'Ciudad': fila[2],
                       'Estadio': fila[3]}
                estudiantes.append(estu)

            conn.close()

            return jsonify({'equipos': estudiantes, 'mensaje': "equipos listados.", 'exito': True})
        except Exception as ex:
            return jsonify({'mensaje': "Errorr", 'exito': False})
    
    @classmethod
    def lista_Estudiante(self,codigo):
        try:
            usuario = buscar_estu(codigo)
            if usuario != None:
                return jsonify({'equipos': usuario, 'mensaje': "partidos encontrado.", 'exito': True})
            else:
                return jsonify({'mensaje': "Usuario no encontrado.", 'exito': False})
        except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False})

    @classmethod
    def registrar_estudiante(self):
        try:
            usuario = buscar_estu(request.json['ci_e'])
            if usuario != None:
                return jsonify({'mensaje': "Cedula de identidad  ya existe, no se puede duplicar.", 'exito': False})
            else:
                conn = conexion2023()
                cur = conn.cursor()
                cur.execute('INSERT INTO equipos values(%s,%s,%s,%s)', (request.json['ci_e'], request.json['nombre_e'], request.json['apell_pat_e'],
                                                                            request.json['apell_mat_e']))
                conn.commit()
                conn.close()
                return jsonify({'mensaje': "equipos registrado.", 'exito': True})
        except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False})
    
    @classmethod
    def actualizar_estudiante(self,codigo):
        try:
            usuario = buscar_estu(codigo)
            if usuario != None:
                conn = conexion2023()
                cur = conn.cursor()
                cur.execute("""UPDATE equipos SET nombreEquuipo=%s, Ciudad=%s, Estadio=%s WHERE EquipoID=%s""",
                        (request.json['nombre_e'], request.json['apell_pat_e'], request.json['apell_mat_e'], codigo))
                conn.commit()
                conn.close()
                return jsonify({'mensaje': "equipos actualizado.", 'exito': True})
            else:
                return jsonify({'mensaje': "equipos  no encontrado.", 'exito': False})
        except Exception as ex:
                return jsonify({'mensaje': "Error", 'exito': False})
        
    @classmethod
    def eliminar_estuy(self,codigo):
        try:
            usuario = buscar_estu(codigo)
            if usuario != None:
                conn = conexion2023()
                cur = conn.cursor()
                cur.execute("DELETE FROM equipos WHERE EquipoID = %s", (codigo,))
                conn.commit()
                conn.close()
                return jsonify({'mensaje': "equipos eliminado.", 'exito': True})
            else:
                return jsonify({'mensaje': "equipos no encontrado.", 'exito': False})
        except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False})