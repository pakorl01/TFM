# Toma como parametros el número de neuronas en las capas de entrada y salida  
# Toma los valores del fichero "datosFiltrados.txt" y los usa para entrenar una red neuronal
# La red entrenada se guarda en el fichero "modelo_semaforo.keras" para su posterior uso.
# Genera también un par de gráficas con la precisión y la pérdida durante el entrenamiento

import sys
import numpy as np
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense
import matplotlib.pyplot as plt


# Leer y preparar los datos
def leer_datos(fichero_entrada, dim_capa_entrada, dim_capa_salida):
    with open(fichero_entrada, 'r') as f:
        lineas = f.readlines()
    
    datos = [eval(line.strip()) for line in lineas]
    datos = np.array(datos)
    
    indice_80 = int(len(datos) * 0.8)

    X = datos[:, :dim_capa_entrada]
    y = datos[:, dim_capa_entrada:dim_capa_entrada+dim_capa_salida]
    
    X_train = X[:indice_80]
    X_test =  X[indice_80:]

    y_train = y[:indice_80]
    y_test =  y[indice_80:]

    return X_train, y_train, X_test, y_test

# Definir y entrenar el modelo
def entrenar_modelo( X_train, y_train, X_test, y_test, dim_capa_entrada, dim_capa_salida):
    num_capas_ocultas = 3
    num_epoch = 100 

    model = Sequential()
    model.add(Dense(64, input_dim=dim_capa_entrada, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(dim_capa_salida))
    
    model.compile(optimizer='adam', loss='mean_squared_error', metrics =["accuracy"])
    history = model.fit(X_train, y_train, epochs=num_epoch, batch_size=10, validation_split=0.2)

    print("Evaluación del modelo")
    #Evalua el modelo
    test_loss, test_accuracy = model.evaluate(X_test,  y_test, verbose=2)
    print('Precisión del modelo:', test_accuracy, " loss: ", test_loss)
    
    model.save('modelo_semaforo.keras')

    figure=plt.figure(figsize=(10,6))
    axes = figure.add_subplot()
    axes.set_title('Precisión del Entrenamiento y Validación', fontsize=18, color="#003B80")
    axes.plot(history.history['accuracy'],label="Entrenamiento "+str(history.history['accuracy'][-1]))
    axes.plot(history.history['val_accuracy'],label="Validación "+str(history.history['val_accuracy'][-1]))
 
    axes.legend()
    axes.set_xlabel('Época', fontsize=12,labelpad=10,color="#003B80")  
    axes.set_ylabel('Valor métrica', fontsize=12,labelpad=20,color="#003B80")
    axes.set_facecolor("#F0F7FF")
    axes.grid(which='major', axis='both',color="#FFFFFF",linewidth=1)

    # Genera un par de ficheros con las gráficas de pérdida y precisión de la red entrenada
    figure_2=plt.figure(figsize=(10,6))
    axes = figure_2.add_subplot()
    axes.set_title('Pérdida del Entrenamiento y Validación', fontsize=18, color="#003B80")
    axes.plot(history.history['loss'],label="Entrenamiento "+str(history.history['loss'][-1]))
    axes.plot(history.history['val_loss'],label="Validación "+str(history.history['val_loss'][-1]))
 
    axes.legend()
    axes.set_xlabel('Época', fontsize=15,labelpad=10,color="#003B80")  
    axes.set_ylabel('Valor métrica', fontsize=15,labelpad=20,color="#003B80")
    axes.set_facecolor("#F0F7FF")
    axes.grid(which='major', axis='both',color="#FFFFFF",linewidth=1)
 
    nombre_archivo_validacion = f"Figura_{num_capas_ocultas}_Capas_Validacion_Epoch_{num_epoch}.png"
    nombre_archivo_perdida = f"Figura_{num_capas_ocultas}_Capas_Perdida_Epoch_{num_epoch}.png"
    figure.savefig( nombre_archivo_validacion, dpi=300, bbox_inches='tight')
    figure_2.savefig(nombre_archivo_perdida, dpi=300, bbox_inches='tight')


# Usar el modelo para predecir
def predecir(modelo_path, nuevos_datos):
    model = load_model(modelo_path)
    predicciones = model.predict(nuevos_datos)
    return predicciones



########################################
# MAIN
########################################

if __name__ == '__main__':
    if len(sys.argv) == 3:
        dim_capa_entrada = int(sys.argv[1]) 
        dim_capa_salida = int(sys.argv[2])

        fichero_entrada = 'datosFiltrados.txt'
        X_train, y_train, X_test, y_test = leer_datos(fichero_entrada, dim_capa_entrada, dim_capa_salida)
    
        entrenar_modelo( X_train, y_train, X_test, y_test, dim_capa_entrada, dim_capa_salida)
    else:
        print(f"Uso : {sys.argv[0]} num_neuronas_capa_entrada num_neurona_capa_salida")
  
