from flask import jsonify

class ControllerObject:
    def __init__(self, title=None, mensaje=None, payload=None, status=200):
        self.title = title
        self.mensaje = mensaje
        self.payload = payload
        self.status = status
    
    def jsonify(self):
        try: status = int(self.status)
        except:
            print("Error en ControllerObject. Status inválido:", self.status)
            status = 500
        
        obj = dict(status=status)
        title = self.title

        if not title:
            if 200 <= status < 300:
                title = "Éxito"
            else:
                title = "Error"

        obj["title"] = title
        if self.mensaje: obj["mensaje"] = self.mensaje

        if self.payload:
            if "mensaje" in obj: obj["payload"] = self.payload
            else: obj = self.payload
        
        return jsonify(obj), status