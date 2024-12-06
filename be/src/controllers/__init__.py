from flask import jsonify

class ControllerObject:
    def __init__(self, title=None, message=None, payload=None, status=200):
        self.title = title
        self.message = message
        self.payload = payload
        self.status = status
    
    def jsonify(self):
        try: 
            status = int(self.status)
        except:
            print("Error in ControllerObject. Invalid status:", self.status)
            status = 500
        
        obj = dict(status=status)
        title = self.title

        if not title:
            if 200 <= status < 300:
                title = "Success"
            else:
                title = "Error"

        obj["title"] = title
        if self.message: 
            obj["message"] = self.message

        if self.payload:
            if "message" in obj: 
                obj["payload"] = self.payload
            else: 
                obj = self.payload
        
        return jsonify(obj), status
