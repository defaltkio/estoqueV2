class Estoque:
    def __init__(self):
        self.produtos = {}

    def adicionar_produto(self, nome, quantidade, preco):
        if nome in self.produtos:
            return False, "Produto já existe no estoque."
        else:
            self.produtos[nome] = {'quantidade': quantidade, 'preco': preco}
            return True, "Produto adicionado com sucesso."

    def atualizar_produto(self, nome, quantidade=None, preco=None):
        if nome in self.produtos:
            if quantidade is not None:
                self.produtos[nome]['quantidade'] = quantidade
            if preco is not None:
                self.produtos[nome]['preco'] = preco
            return True, "Produto atualizado com sucesso."
        else:
            return False, "Produto não encontrado no estoque."

    def remover_produto(self, nome):
        if nome in self.produtos:
            del self.produtos[nome]
            return True, "Produto removido com sucesso."
        else:
            return False, "Produto não encontrado no estoque."

    def verificar_estoque(self, nome):
        if nome in self.produtos:
            return True, self.produtos[nome]
        else:
            return False, "Produto não encontrado no estoque."

    def listar_produtos(self):
        if self.produtos:
            return True, self.produtos
        else:
            return False, "O estoque está vazio."
