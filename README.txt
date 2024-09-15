INSTRUCCIONES PARA EL ESTABLECIMIENTO DEL ENTORNO:

    Abrir una consola (probado en Windows)
    Ejecutar :                                  %SUMO_HOME%\start-command-line.bat
    Establecer la vble de entorno :	            set SCRIPT_DIR=%HOMEPATH%\tfm\ScriptsPython
	
EJECUCION DE LOS SCRIPTS:

    Copiar los ficheros de configuración en una carpeta y moverse a esa carpeta.
	
    Ejecutar los siguientes comandos:
    1.	python %SUMO_HOME%\tools\randomTrips.py -n fichero_generado.net.xml --weights-output-prefix fichero_probabilidad
    2.	python %SCRIPT_DIR%\GeneraFicheroProbabilidades.py
    3.	python %SCRIPT_DIR%\GeneraEscenariosTrafico.py
    4.	python %SCRIPT_DIR%\ModificaTiempoDePartidaVehiculos.py
    5.	python %SCRIPT_DIR%\EjecutaSimulaciones.py
    6.	python %SCRIPT_DIR%\SeleccionaListas.py
    7.	python %SCRIPT_DIR%\EntrenaIA.py 4 2
    8.	python %SCRIPT_DIR%\GeneraDatosAPredecir.py 2 5 10 10
    9.	python %SCRIPT_DIR%\EjecutaIA_Con_Distancia_Euclidea.py
	
	
	
FICHEROS USADOS CON LOS SCRIPTS:
																				
	
    fichero_generado.net.xml        ==>	    randomTrips.py                              ==>     fichero_probabilidad.src.xml

    fichero_probabilidad.src.xml    ==>     GeneraFicheroProbabilidades.py              ==>     output_probability_files/*

    output_probability_files/*      ==>     GeneraEscenariosTrafico.py                  ==>     output_traffic_file/*          (unos 40 minutos )

    output_traffic_file/*           ==>	    ModificaTiempoDePartidaVehiculos.py	        ==>	    output_traffic_file_depart0/*

    output_traffic_file_depart0/*   ==>     EjecutaSimulaciones.py                      ==>     fichero_datos_simulacion.txt    ( unas 10 horas)

    fichero_datos_simulacion        ==>     SeleccionaListas.py                         ==>     datosFiltrados.txt y datosFiltrados.SIN_NORMALIZAR.txt

    datosFiltrados.txt              ==>     EntrenaIA.py 4 2                            ==>     modelo_semaforo.keras

    2 5 10 10 (desde consola)       ==>     GeneraDatosAPredecir.py 2 5 10 10           ==>	    datosAPredecir.txt

    ficheroRedNeuronal  |
           +            |           ==>     EjecutaIA_Con_Distancia_Euclidea.py	        ==>     SalidaEjecutaIA.txt	 (previsión de tiempos de los semáforos)
    datosAPredecir.txt	|		


CARPETA UTILIDADES:

    Contiene scripts para la recolección de datos y creación de gráficas usados en el documento del TFM