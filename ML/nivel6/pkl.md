## PKL

Un archivo `.pkl` (o a veces `.pickle`) es un archivo utilizado en el lenguaje de programación **Python**.

En resumen, es un archivo que **guarda un objeto de Python "serializado"**.

---

## ¿Qué es "Serializar"?

La serialización (que en Python se hace con el módulo `pickle`) es el proceso de convertir un objeto complejo de Python—como una lista, un diccionario, o incluso un modelo de *machine learning*—en un **flujo de bytes** (una secuencia de 1s y 0s).

Piénsalo como "congelar" un objeto de Python en un estado exacto para guardarlo en un archivo.

El proceso inverso se llama **deserialización** ("unpickling"), que toma ese flujo de bytes del archivo `.pkl` y lo reconstruye en memoria, devolviéndote el objeto original tal como estaba.

---

## ¿Para qué se usa un archivo .pkl?

El propósito principal es **guardar el progreso o el estado** de un programa para no tener que volver a calcularlo todo desde cero.

Los usos más comunes son:

### 1. Guardar Modelos de Machine Learning (IA)
Este es el uso más popular hoy en día. Entrenar un modelo de inteligencia artificial (por ejemplo, con bibliotecas como `scikit-learn`) puede tardar horas o días.

En lugar de re-entrenar el modelo cada vez que ejecutas tu aplicación, simplemente lo entrenas una vez y luego lo "guardas" en un archivo `.pkl`. Cuando tu aplicación necesita hacer una predicción, simplemente "carga" (deserializa) el archivo `.pkl` y tiene el modelo entrenado listo para usar en segundos.

### 2. Guardar el estado de una aplicación
Si tienes un script que procesa muchos datos y quieres poder pausarlo y reanudarlo, puedes guardar las variables importantes en un archivo `.pkl`.

### 3. Caching (Almacenamiento en caché)
Si tienes una función que realiza un cálculo muy pesado (por ejemplo, consultar una base de datos enorme y procesar los resultados), puedes guardar el resultado final en un archivo `.pkl`. La próxima vez que necesites ese resultado, simplemente cargas el archivo en lugar de volver a calcularlo.

### 4. Transferencia de datos entre procesos
Permite enviar objetos complejos de Python entre diferentes scripts o programas que se estén ejecutando al mismo tiempo.

---

## ⚠️ Advertencia de Seguridad Importante

Un archivo `.pkl` **no es seguro**.

**Nunca debes abrir (deserializar) un archivo `.pkl` que hayas descargado de internet o recibido de alguien en quien no confíes al 100%.**

La razón es que el formato `pickle` fue diseñado para ser flexible, no seguro. Al deserializar un archivo `.pkl` manipulado, es posible que este **ejecute código malicioso** en tu computadora. Para compartir datos de forma segura, es mejor usar formatos como JSON o XML.
