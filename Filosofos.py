import time
import random
import threading

numerosFilosofos = 5

class filosofo(threading.Thread):
    semaforo = threading.Lock() 
    estado = [] 
    tenedores = [] 
    contador=0

    def __init__(self):   
        super().__init__() 
        self.id=filosofo.contador 
        filosofo.contador+=1 
        filosofo.estado.append('Pensar') 
        filosofo.tenedores.append(threading.Semaphore(0))

    def tenedorDerecha(self,i):
        return (i-1)%numerosFilosofos

    def tenedorIzquierda(self,i):
        return(i+1)%numerosFilosofos

    def pensar(self):
        time.sleep(random.randint(0,4))

    def agarrarTenedores(self):
        filosofo.semaforo.acquire() 
        filosofo.estado[self.id] = 'Hambre'
        self.verficarTenedores(self.id)
        filosofo.semaforo.release() 
        filosofo.tenedores[self.id].acquire() 
    
    def comer(self):
        print("\nEl filosofo {} esta comiendo".format(self.id))
        time.sleep(2) 
        print("El filosofo {} termino de comer\n".format(self.id))
    
    def dejarTenedores(self):
        filosofo.semaforo.acquire() 
        filosofo.estado[self.id] = 'Pensar'
        self.verficarTenedores(self.tenedorIzquierda(self.id))
        self.verficarTenedores(self.tenedorDerecha(self.id))
        filosofo.semaforo.release() 
    
    def verficarTenedores(self,i):
        if filosofo.estado[i] == 'Hambre' and filosofo.estado[self.tenedorIzquierda(i)] != 'Comiendo' and filosofo.estado[self.tenedorDerecha(i)] != 'Comiendo':
            filosofo.estado[i]='Comiendo'
            filosofo.tenedores[i].release()  
    
    def run(self):
        self.pensar() 
        self.agarrarTenedores() 
        self.comer() 
        self.dejarTenedores() 
    
    def __del__(self):
        print("El filosofo {0} - Se paro de la mesa".format(self.id)) 

def main():
    lista=[]
    for i in range(numerosFilosofos):
        lista.append(filosofo())

    for f in lista:
        f.start() 

    for f in lista:
        f.join()

if __name__=="__main__":
    main()