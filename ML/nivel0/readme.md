# Gestión de Datos en Python: Guía Práctica

## Contenido
1. [Estructuras de Datos Básicas](#1-estructuras-de-datos-básicas)
2. [Almacenamiento en Archivos Planos](#2-almacenamiento-en-archivos-planos)
3. [Bases de Datos Relacionales (SQLite)](#3-bases-de-datos-relacionales-sqlite)
4. [Análisis de Datos con Pandas](#4-análisis-de-datos-con-pandas)
5. [Gestión Avanzada de Archivos](#5-gestión-avanzada-de-archivos)
6. [Ejemplo Integrado: Sistema de Tareas](#6-ejemplo-integrado-sistema-de-tareas)
7. [Resumen Comparativo](#7-resumen-comparativo)

---

## 1. Estructuras de Datos Básicas
Las estructuras nativas de Python permiten manejar datos eficientemente en memoria.

```python
# Listas (ordenadas y mutables)
frutas = ["manzana", "banana", "cereza"]
frutas.append("naranja")  # Añadir elemento
print(frutas[0])  # Acceso por índice

# Diccionarios (clave-valor)
persona = {"nombre": "Ana", "edad": 30}
persona["profesion"] = "Ingeniera"  # Añadir clave

# Conjuntos (elementos únicos)
colores = {"rojo", "verde", "azul"}
colores.add("amarillo")

# Tuplas (inmutables)
coordenadas = (40.7128, -74.0060)  # Latitud, Longitud
