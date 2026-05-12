import logging
import os
from abc import ABC, abstractmethod

# 1. CONFIGURACIÓN DE LOGS (Garantiza que el archivo se cree)
try:
    logging.basicConfig(
        filename='sistema_gestion.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logging.info("Sistema iniciado.")
except Exception as e:
    print(f"Error al crear el archivo de log: {e}")

# 2. EXCEPCIONES PERSONALIZADAS 
class SoftwareFJError(Exception): pass
class ClienteInvalidoError(SoftwareFJError): pass
class ReservaError(SoftwareFJError): pass

# 3. CLASES (POO) [cite: 20]
class Entidad(ABC):
    @abstractmethod
    def mostrar_identidad(self): pass

class Cliente(Entidad):
    def __init__(self, id_c, nombre, correo):
        if not nombre or "@" not in correo:
            raise ClienteInvalidoError(f"Datos inválidos en cliente: {nombre}")
        self.__nombre = nombre # Encapsulación [cite: 22]
        self.__correo = correo

    def mostrar_identidad(self):
        return f"Cliente: {self.__nombre}"

class Servicio(ABC): # Clase abstracta [cite: 23]
    def __init__(self, nombre, costo_base):
        self.nombre = nombre
        self.costo_base = costo_base
    @abstractmethod
    def calcular_costo(self, cantidad): pass

class ReservaSala(Servicio):
    def calcular_costo(self, horas):
        return self.costo_base * horas

class AlquilerEquipos(Servicio):
    def calcular_costo(self, unidades):
        return self.costo_base * unidades

class Asesoria(Servicio):
    def calcular_costo(self, sesiones):
        return self.costo_base * sesiones

class Reserva:
    def __init__(self, cliente, servicio, duracion):
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion

    def gestionar(self):
        try:
            if self.duracion <= 0:
                raise ReservaError("La duración debe ser positiva.")
            total = self.servicio.calcular_costo(self.duracion)
            print(f"ÉXITO: {self.cliente.mostrar_identidad()} - Total: ${total}")
            logging.info(f"Reserva exitosa: {total}")
        except ReservaError as e:
            print(f"ERROR DE RESERVA: {e}")
            logging.error(f"Fallo en reserva: {e}")
        except Exception as e:
            print(f"ERROR INESPERADO: {e}")

# 4. SIMULACIÓN DE 10 OPERACIONES 
def iniciar():
    print("=== SOFTWARE FJ - GESTIÓN INTEGRAL ===\n")
    s1 = ReservaSala("Sala A", 50000)
    s2 = AlquilerEquipos("PC", 20000)
    s3 = Asesoria("Tutoría", 80000)

    casos = [
        ("01", "Yessid", "m@mail.com", s1, 3),   # Válido
        ("02", "", "error@mail.com", s2, 5),      # Inválido
        ("03", "Juan", "j@mail.com", s3, -2),     # Inválido
        ("04", "Ana", "ana@mail.com", s1, 2),     # Válido
        ("05", "Luis", "luis@mail.com", s2, 4),   # Válido
        ("06", "Invalido", "no-mail", s3, 1),     # Inválido
        ("07", "Marta", "m@mail.com", s1, 1),     # Válido
        ("08", "Pedro", "p@mail.com", s2, 0),     # Inválido
        ("09", "Sofia", "s@mail.com", s3, 3),     # Válido
        ("10", "Carlos", "c@mail.com", s1, 5),    # Válido
    ]

    for id_c, nom, mail, serv, dur in casos:
        try:
            cli = Cliente(id_c, nom, mail)
            res = Reserva(cli, serv, dur)
            res.gestionar()
        except ClienteInvalidoError as e:
            print(f"ALERTA: {e}")
            logging.warning(f"Fallo de cliente: {e}")

if __name__ == "__main__":
    iniciar()
    input("\nPresiona Enter para cerrar...")
