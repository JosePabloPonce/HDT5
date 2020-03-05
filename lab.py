#Jose Pablo Ponce 19092
#HDT 5

import simpy
import random
import statistics

#tiempo de creacion de intervalos exponencialmente
creacionprocesointervalo = int(input ("Ingrese intervalo a utilizar:\n"))

#cantidad de procesos 
cantidadprocesos = int(input ("Ingrese cantidad de procesos:\n"))

#tiempo total en completar todo
tiempototal = 0

#seed y ambiente
random_seed = int(input ("Ingrese Semilla:\n"))
random.seed(random_seed)
env = simpy.Environment()

#caracteristicas procesador
capacidadprocesadores = int(input ("Ingrese cantidad de procesadores:\n"))
procesador = simpy.Resource(env, capacity=capacidadprocesadores)
capacidadram = simpy.Container(env, init=100, capacity=100)
tiempo = simpy.Resource(env, capacity=1)


#desviacionestandar
desviacion =0
tiemposobtenidos =[]

def correr(capacidadram,intervalo,cantidadprocesos,tiempo,procesador,env):
    #contador
    i=1
    
    #mientras i sea menor a la cantidad de procesos se sige ejecutando
    while i <cantidadprocesos+1:
        global nombre
        actual = env.now
        instrucciones = random.randint(1,10)
        nombre = "proceso" + str(i)
        proceso = procesonuevo(nombre,capacidadram,procesador,instrucciones,actual,tiempo, env)
        env.process(proceso)
        intervalotiempo = random.expovariate(1.0/intervalo)
        i+=1
        
        #intervalo esperado para siguiente proceso
        yield env.timeout(intervalotiempo)
        
 #obtener la ram y asignarsela al proceso   
def procesonuevo (name, capacidadram,procesador,instrucciones,actual,tiempo, env):
    
    ramasignada = random.randint(1,10)
    
    with capacidadram.get(ramasignada) as obtener:
        yield obtener
        
    print( nombre,'-RAM disponible:',capacidadram.level, '-RAM utilizando:',ramasignada, '-Instrucciones faltantes:', instrucciones)
    procesar=procesar1(procesador,instrucciones,ramasignada,actual,tiempo,env)
    env.process(procesar)
        
def procesar1(procesador,instrucciones,ramasignada,actual,tiempo,env):
    
        global tiempototal
        while instrucciones >= 1:
            
            #Numero generado al procesar la operacion
            generado = random.randint(1,2)
            
            
            with procesador.request() as procesamiento:  
                yield procesamiento
                yield env.timeout(1)
                
                #condicion de cantidad de operacaiones a procesar
                if instrucciones >3:
                    instrucciones = instrucciones - 3
            
           
                    #Si se genera uno va a la cola de tiempo
                    if generado == 1:
                         
                        with tiempo.request() as tiempo1:
                            yield tiempo1
                            yield env.timeout(1)
                            
                    #Si se genera un dos se dirige a ready        
                    else:
                        instrucciones = instrucciones -3
                        
                #condicion si hay menos de tres instrucciones        
                else:
                    instrucciones = 0
                    
                                      
                        
        #retorna la ram utilizada            
        with capacidadram.put(ramasignada) as retornar:
            yield retornar
        
            
            esperado = env.now - actual
            tiempototal = tiempototal + esperado
            #lista para generar la desviacion estandar
            tiemposobtenidos.append(esperado)     
            print (nombre, "Tiempo en computadora:",esperado )

        

env.process(correr(capacidadram, creacionprocesointervalo,cantidadprocesos,tiempo,procesador, env))
env.run()
print ("")
print ('Tiempo total en computadora:',tiempototal)
print ('Promedio de tiempo total:',tiempototal / cantidadprocesos)
print ("La desviacion estandar es de: ", statistics.pstdev(tiemposobtenidos))

