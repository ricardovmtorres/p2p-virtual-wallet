class Wallet:
     def __init__(self, saldo):
         if not (isinstance(saldo, (int, float)) and saldo > 0):
             raise ValueError(f"positive saldo expected, got {saldo}")
         self.saldo = saldo

     def depositar(self, valor):
        if valor>0 and valor<self.saldo:
            self.saldo+=valor 
            print(f"Valor Depositado: {valor}")
        else:
            print(f"Valor deve ser positivo e não, {valor}!")