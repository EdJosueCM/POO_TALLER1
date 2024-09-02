import json

class Client:
    _id_counter = 0  # Contador de IDs

    def __init__(self, first_name="Consumidor", last_name="Final", dni="9999999999"):
        Client._id_counter += 1
        self.client_id = Client._id_counter % 10  # ID único de 1 dígito
        self.__dni = dni
        self.first_name = first_name
        self.last_name = last_name
                    
    @property
    def dni(self):
        return self.__dni
    
    @dni.setter
    def dni(self, value):
        if len(value) in (10, 13):
            self.__dni = value
        else:
            self.__dni = "9999999999"
  
    def to_dict(self):
        # Convierte el objeto a un diccionario para serializarlo en JSON
        return {
            "client_id": self.client_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "dni": self.dni
        }
    
    def __str__(self):
        return f'Cliente: {self.first_name} {self.last_name}'

    def show(self):
        print(f"ID: {self.client_id}, Name: {self.first_name} {self.last_name}")
        
class RegularClient(Client):
    def __init__(self, first_name="Cliente", last_name="Final", dni="9999999999", card=False):
        super().__init__(first_name, last_name, dni)
        self.__discount = 0.10 if card else 0.05
            
    @property
    def discount(self):
        return self.__discount
    
    @staticmethod
    def from_dict(data):
        return RegularClient(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            dni=data.get("dni"),
            card=data.get("discount") > 0
        )
    
    def __str__(self):
        return f'Cliente Regular: {self.first_name} {self.last_name}, Descuento: {self.discount*100}%'
    
    def to_dict(self):
        # Convierte el objeto a un diccionario e incluye el descuento
        data = super().to_dict()
        data["discount"] = self.discount
        return data

class VipClient(Client):
    def __init__(self, first_name="Consumidor", last_name="Final", dni="9999999999"):
        super().__init__(first_name, last_name, dni)
        self.__limit = 10000  # Límite de crédito del cliente VIP
    
    @property
    def limit(self):
        return self.__limit
    
    @limit.setter
    def limit(self, value):
        self.__limit = 10000 if (value < 10000 or value > 20000) else value

    @staticmethod
    def from_dict(data):
        return VipClient(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            dni=data.get("dni")
        )
    
    def __str__(self):
        return f'Cliente VIP: {self.first_name} {self.last_name}, Cupo: {self.limit}'
    
    def to_dict(self):
        # Convierte el objeto a un diccionario e incluye el límite de crédito
        data = super().to_dict()
        data["limit"] = self.limit
        return data

    def show(self):
        # Muestra la información de VipClient
        super().show()  # Llama al método `show` de la clase base `Client`
        print(f"Limit: {self.limit}")
