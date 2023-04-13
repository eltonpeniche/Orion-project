from apps.orion.models import Chamado, Empresa, Endereco, Equipamento


class OrionMixin:
    def make_endereco(self, cep=66093-908, rua = "Avenida Almirante Barroso", bairro = "Marco", uf = 'PA', cidade = "Belém", numero="1454" ):
        return Endereco.objects.create(cep=-cep, rua = rua, bairro = bairro, uf = uf, cidade = cidade, numero=numero)
    
    def make_empresa(self, nome ="HOSPITAL PORTO DIAS LTDA", cnpj="84154608000160", telefone="9130843000"):
        endereco = self.make_endereco()

        empresa = Empresa.objects.create(nome = nome, cnpj=cnpj, telefone=telefone, endereco = endereco)

        return empresa

    def make_empresa_in_batch(self):
        empresas = [ { "nome":"HOSPITAL PORTO DIAS LTDA", "cnpj":"84154608000160","telefone":"9130843000" }, { "nome":"HOSPITAL ADVENTISTA DE BELEM", "cnpj":"83367342000252", "telefone":"9131941100" ,"email":"controladoria@hab.org.br" }, { "nome":"HOSPITAL UNIVERSITARIO DO MARANHAO", "cnpj":"06279103000208", "telefone":"9821091289" }, { "nome":"Hospital Sao Luis", "cnpj":"09192098000109", "email":"contabilidade2@hospitalsaoluiz.net", "telefone":"9827391289"}]
        
        lista_empresas = []
        for dados in empresas:
            empresa = self.make_empresa(nome=dados['nome'] , cnpj=dados['cnpj'], telefone=dados['telefone'])
            lista_empresas.append(empresa)
        return lista_empresas
    
    def make_equipamento(self, empresa = None, numero_serie = "17593", equipamento="Magnetom Concerto", tipo_equipamento  = "MR", descricao  = "uma descrição qualquer" ):
        if empresa is None:
            empresa = self.make_empresa()
        return Equipamento.objects.create(empresa=empresa, numero_serie=numero_serie, equipamento=equipamento, tipo_equipamento=tipo_equipamento, descricao=descricao)
    
    def make_equipamento_in_batch(self):
        equipamentos = [{ "empresa_id":1, "numero_serie":"17593", "equipamento":"Magnetom Concerto", "tipo_equipamento":"MR","descricao":"None" }, { "empresa_id":2, "numero_serie":"CT411187HM8","equipamento":"GE Brivo", "tipo_equipamento":"CT", "descricao":"None" }, { "empresa_id":2, "numero_serie":"B0522101","equipamento":"Toschiba Asteion", "tipo_equipamento":"CT", "descricao":"Equipamento em Porto Franco-MA" }, { "empresa_id":3, "numero_serie":"84217", "equipamento":"Somatom Spirit", "tipo_equipamento":"CT", "descricao":"None" }, {"empresa_id":4, "numero_serie":"441541", "equipamento":"wqd", "tipo_equipamento":"dad", "descricao":"None" } ]
        
        lista_equipamentos = []
        for dados in equipamentos:
            equipamento = self.make_equipamento(empresa_id=dados['empresa_id'] , numero_serie=dados['numero_serie'], equipamento=dados['equipamento'], tipo_equipamento=dados['tipo_equipamento'],descricao=dados['descricao'] )
            lista_equipamentos.append(equipamento)
        return lista_equipamentos
    

    def make_chamado(self, empresa=None, equipamento=None, descricao_chamado= "Chamado de Teste", status='P', tipo_chamado='C', status_chamado='A', numero_chamado='000000001111'):
        if empresa is None:
            empresa = self.make_empresa()
        if equipamento is None:
            equipamento = self.make_equipamento()
        Chamado.objects.create( descricao_chamado = descricao_chamado,
                   status = status, tipo_chamado=tipo_chamado ,status_chamado = status_chamado, numero_chamado = numero_chamado, empresa = empresa, equipamento = equipamento
        )