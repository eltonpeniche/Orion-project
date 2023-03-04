from faker import Faker

from orion.models import Empresa

fake = Faker()

cnpj = '07.987.925/0001-17'
linha  = []
for _ in range(100):
    nome = fake.company()
    telefone = fake.phone_number()
    email = fake.email()
    linha.append([f'{nome},{cnpj},{telefone},{email}'])
    empresa = Empresa.objects.create(nome = nome,       
                        cnpj = cnpj,      
                        telefone = telefone,  
                        email = email  )
    empresa.save()


#exec(open('/home/elton/Documentos/Orion-project/popula_banco.py').read())