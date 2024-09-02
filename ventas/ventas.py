from crud import JsonFile
from company import Company
from customer import RegularClient, VipClient
from product import Product
from datetime import date
import os, uuid

# Colores en formato ANSI escape code
reset_color = "\033[0m"
green_color = "\033[92m"
blue_color = "\033[94m"
cyan_color = "\033[96m"

# Colores en formato ANSI escape code
reset_color = "\033[0m"
green_color = "\033[92m"
blue_color = "\033[94m"
cyan_color = "\033[96m"
purple_color = "\033[35m"

class SaleDetail:
    _line = 0

    def __init__(self, product, quantity):
        SaleDetail._line += 1
        self.__id = SaleDetail._line
        self.product = product
        self.preci = product.preci
        self.quantity = quantity

    @property
    def id(self):
        return self.__id

    def __repr__(self):
        return f'{self.id} {self.product.descrip} {self.preci} {self.quantity}'

class Icalculo:
    def cal_iva(self, iva=0.12, valor=0):
        return round(valor * iva, 2)

    def cal_discount(self, valor=0, discount=0):
        return round(valor * discount, 2)

class Sale(Icalculo):
    next = 0
    FACTOR_IVA = 0.12

    def __init__(self, client):
        Sale.next += 1
        self.__invoice = "F0" + str(Sale.next)
        self.date = date.today()
        self.client = client
        self.subtotal = 0
        self.percentage_discount = client.discount if isinstance(self.client, RegularClient) else 0
        self.discount = 0
        self.iva = 0
        self.total = 0
        self.sale_detail = []

    @property
    def invoice(self):
        return self.__invoice

    def __repr__(self):
        return f'Factura# {self.invoice} {self.date} {self.client.fullName()} {self.total} {self.sale_detail}'

    def add_detail(self, product, quantity):
        detail = SaleDetail(product, quantity)
        self.subtotal += round(detail.preci * detail.quantity, 2)
        self.discount = self.cal_discount(self.subtotal, self.percentage_discount)
        self.iva = self.cal_iva(Sale.FACTOR_IVA, self.subtotal - self.discount)
        self.total = round(self.subtotal + self.iva - self.discount, 2)
        self.sale_detail.append(detail)

    def print_invoice(self, company):
        os.system('cls')
        print('\033c', end='')
        print(green_color + "*"*70 + reset_color)
        print(blue_color + f"Empresa: {company.business_name} Ruc: {company.ruc}", end='')
        print(f" Factura#:{self.invoice:7} Fecha:{self.date}")
        self.client.show()
        print(green_color + "*"*70 + reset_color)
        print(purple_color + "Linea Articulo Precio Cantidad Subtotal")
        for det in self.sale_detail:
            print(blue_color + f"{det.id:5} {det.product.descrip:6} {det.preci:7} {det.quantity:2} {det.preci*det.quantity:14}")
        print(green_color + "*"*70 + reset_color)
        print(purple_color + " "*23 + "Subtotal:  " + str(self.subtotal))
        print(" "*23 + "Descuento: " + str(self.discount))
        print(" "*23 + "Iva:       " + str(self.iva))
        print(" "*23 + "Total:     " + str(self.total) + reset_color)

class Menu:
    def __init__(self):
        self.company_file = JsonFile('companies.json')
        self.clients_file = JsonFile('clients.json')
        self.products_file = JsonFile('products.json')
        self.sales_file = JsonFile('sales.json')

    def menu(self):
        while True:
            os.system('cls')
            print(green_color + "MENU PRINCIPAL" + reset_color)
            print(blue_color + "1. Gestionar Empresa")
            print("2. Gestionar Clientes")
            print("3. Gestionar Productos")
            print("4. Gestionar Ventas")
            print("5. Salir" + reset_color)

            choice = input("Seleccione una opción: ")
            os.system('cls')

            if choice == '1':
                self.manage_companies()
            elif choice == '2':
                self.manage_clients()
            elif choice == '3':
                self.manage_products()
            elif choice == '4':
                self.manage_sales()
            elif choice == '5':
                break

    def manage_companies(self):
        while True:
            os.system('cls')
            print(cyan_color + "GESTION DE EMPRESAS" + reset_color)
            print("1. Ingresar Nueva Empresa")
            print("2. Listar Empresas")
            print("3. Eliminar Empresa")
            print("4. Regresar")
            sub_choice = input("Seleccione una opción: ")
            os.system('cls')

            if sub_choice == '1':
                business_name = input("Ingrese el nombre de la empresa: ")
                ruc = input("Ingrese el RUC de la empresa: ")
                companies = self.company_file.read()

                # Validación de RUC duplicado
                if any(company['ruc'] == ruc for company in companies):
                    input("El RUC ya está registrado. Presione Enter para continuar...")
                    continue

                company = Company(business_name, ruc)
                companies.append(company.__dict__)
                self.company_file.save(companies)
                input("Empresa registrada exitosamente. Presione Enter para continuar...")

            elif sub_choice == '2':
                companies = self.company_file.read()
                if companies:
                    for i, company in enumerate(companies):
                        print(f"{i+1}. Nombre: {company['business_name']}, RUC: {company['ruc']}")
                else:
                    print("No hay empresas registradas.")
                input("Presione Enter para continuar...")
            elif sub_choice == '3':
                companies = self.company_file.read()
                if companies:
                    for i, company in enumerate(companies):
                        print(f"{i+1}. Nombre: {company['business_name']}, RUC: {company['ruc']}")
                    del_choice = int(input("Seleccione el número de la empresa a eliminar: ")) - 1
                    if 0 <= del_choice < len(companies):
                        del companies[del_choice]
                        self.company_file.save(companies)
                        input("Empresa eliminada exitosamente. Presione Enter para continuar...")
                    else:
                        input("Opción inválida. Presione Enter para continuar...")
                else:
                    print("No hay empresas registradas.")
                    input("Presione Enter para continuar...")
            elif sub_choice == '4':
                return  # Regresa al menú principal

    def manage_clients(self):
        while True:
            os.system('cls')
            print("GESTION DE CLIENTES")
            print("1. Crear Cliente Regular")
            print("2. Crear Cliente VIP")
            print("3. Listar Clientes")
            print("4. Eliminar Cliente")
            print("5. Regresar")
            sub_choice = input("Seleccione una opción: ")
            os.system('cls')

            if sub_choice == '1' or sub_choice == '2':
                name = input("Nombre: ").strip()
                last_name = input("Apellido: ").strip()
                dni = input("DNI: ").strip()

                if not dni:
                    input("DNI no puede estar vacío. Presione Enter para continuar...")
                    continue

                clients = self.clients_file.read()

                # Asegurarse de que todos los clientes tienen un DNI válido antes de la validación
                if any(client.get('dni') == dni for client in clients):
                    input("El DNI ya está registrado. Presione Enter para continuar...")
                    continue

                if sub_choice == '1':
                    client = RegularClient(name, last_name, dni, card=True)
                else:
                    client = VipClient(name, last_name, dni)

                clients.append(client.__dict__)
                self.clients_file.save(clients)
                input("Cliente registrado exitosamente. Presione Enter para continuar...")

            elif sub_choice == '3':
                clients = self.clients_file.read()
                if clients:
                    for i, client in enumerate(clients):
                        client_id = client.get('client_id')
                        name = client.get('first_name')
                        last_name = client.get('last_name')
                        dni = client.get('dni')
                        print('Lista de Clientes:')
                        print(f"{i+1}. ID: {client_id}, Nombre: {name} {last_name}, DNI: {dni}")
                else:
                    print("No hay clientes registrados.")
                input("Presione Enter para continuar...")
            elif sub_choice == '4':
                clients = self.clients_file.read()
                if clients:
                    for i, client in enumerate(clients):
                        client_id = client.get('client_id')
                        name = client.get('first_name')
                        last_name = client.get('last_name')
                        dni = client.get('dni')
                        print(f"{i+1}. ID: {client_id}, Nombre: {name} {last_name}, DNI: {dni}")
                    del_choice = int(input("Seleccione el número del cliente a eliminar: ")) - 1
                    if 0 <= del_choice < len(clients):
                        del clients[del_choice]
                        self.clients_file.save(clients)
                        input("Cliente eliminado exitosamente. Presione Enter para continuar...")
                    else:
                        input("Opción inválida. Presione Enter para continuar...")
                else:
                    print("No hay clientes registrados.")
                    input("Presione Enter para continuar...")
            elif sub_choice == '5':
                return  # Regresa al menú principal

    def manage_products(self):
        while True:
            os.system('cls')
            print(cyan_color + "GESTION DE PRODUCTOS" + reset_color)
            print("1. Crear Producto")
            print("2. Listar Productos")
            print("3. Eliminar Producto")
            print("4. Regresar")
            sub_choice = input("Seleccione una opción: ")

            if sub_choice == '1':
                descrip = input("Descripción: ")
                products = self.products_file.read()

                # Validación de descripción de producto duplicado (insensible a mayúsculas)
                if any(product['descrip'].lower() == descrip.lower() for product in products):
                    input(f'Este producto ya se encuentra registrado. Presione "Enter" para continuar...')
                    continue

                preci = float(input("Precio: "))
                stock = int(input("Stock: "))
                product = Product(descrip, preci, stock)
                products.append(product.__dict__)
                self.products_file.save(products)
                input(f'Producto registrado exitosamente. Presione "Enter" para continuar...')

            elif sub_choice == '2':
                products = self.products_file.read()
                if products:
                    for i, product in enumerate(products):
                        descrip = product.get('descrip')
                        preci = product.get('preci')
                        stock = product.get('stock')
                        print(f"{i+1}. Descripción: {descrip}, Precio: {preci}, Stock: {stock}")
                else:
                    print("No hay productos registrados.")
                input("Presione Enter para continuar...")
            elif sub_choice == '3':
                products = self.products_file.read()
                if products:
                    for i, product in enumerate(products):
                        descrip = product.get('descrip')
                        preci = product.get('preci')
                        stock = product.get('stock')
                        print(f"{i+1}. Descripción: {descrip}, Precio: {preci}, Stock: {stock}")
                    del_choice = int(input("Seleccione el número del producto a eliminar: ")) - 1
                    if 0 <= del_choice < len(products):
                        del products[del_choice]
                        self.products_file.save(products)
                        input("Producto eliminado exitosamente. Presione Enter para continuar...")
                    else:
                        input("Opción inválida. Presione Enter para continuar...")
                else:
                    print("No hay productos registrados.")
                    input("Presione Enter para continuar...")
            elif sub_choice == '4':
                return  # Regresa al menú principal

    def manage_sales(self):
        while True:
            os.system('cls')
            print("GESTION DE VENTAS")
            print("1. Registrar Venta")
            print("2. Listar Ventas")
            print("3. Regresar")
            sub_choice = input("Seleccione una opción: ")

            if sub_choice == '1':
                clients = self.clients_file.read()
                if not clients:
                    input("No hay clientes registrados. Presione Enter para continuar...")
                    continue

                products = self.products_file.read()
                if not products:
                    input("No hay productos registrados. Presione Enter para continuar...")
                    continue

                print("Clientes registrados:")
                for client in clients:
                    print(f"ID: {client.get('client_id')}, Nombre: {client.get('first_name')} {client.get('last_name')}")

                client_id_input = input("Ingrese el ID del cliente: ")
                try:
                    client_id = int(client_id_input)
                except ValueError:
                    input("ID del cliente inválido. Presione Enter para continuar...")
                    continue

                client = next((c for c in clients if c.get('client_id') == client_id), None)
                
                print(f"Buscando cliente con ID: {client_id}")
                print(f"Clientes cargados: {[c.get('client_id') for c in clients]}")

                if not client:
                    input("Cliente no encontrado. Presione Enter para continuar...")
                    continue

                sale = Sale(client)
                print("Ingrese los productos para la venta:")
                while True:
                    product_id_input = input("Ingrese el ID del producto (o 'fin' para terminar): ")
                    if product_id_input.lower() == 'fin':
                        break

                    try:
                        product_id = int(product_id_input)
                    except ValueError:
                        input("ID del producto inválido. Presione Enter para continuar...")
                        continue

                    product = next((p for p in products if p.get('product_id') == product_id), None)

                    print(f"Buscando producto con ID: {product_id}")
                    print(f"Productos cargados: {[p.get('product_id') for p in products]}")

                    if not product:
                        input("Producto no encontrado. Presione Enter para continuar...")
                        continue

                    quantity = int(input("Ingrese la cantidad: "))
                    if quantity <= 0:
                        input("La cantidad debe ser mayor a cero. Presione Enter para continuar...")
                        continue

                    sale.add_detail(product, quantity)

                sales = self.sales_file.read()
                sales.append({
                    'invoice': sale.invoice,
                    'date': str(sale.date),
                    'client': sale.client.fullName(),
                    'subtotal': sale.subtotal,
                    'discount': sale.discount,
                    'iva': sale.iva,
                    'total': sale.total,
                    'details': [{'product': det.product.descrip, 'quantity': det.quantity, 'price': det.preci} for det in sale.sale_detail]
                })
                self.sales_file.save(sales)
                input("Venta registrada exitosamente. Presione Enter para continuar...")

            elif sub_choice == '2':
                sales = self.sales_file.read()
                if sales:
                    for i, sale in enumerate(sales):
                        print(f"{i+1}. Factura#: {sale['invoice']} Fecha: {sale['date']} Cliente: {sale['client']} Total: {sale['total']}")
                else:
                    print("No hay ventas registradas.")
                input("Presione Enter para continuar...")
            elif sub_choice == '3':
                return  # Regresa al menú principal

            
if __name__ == "__main__":
    menu = Menu()
    menu.menu()
