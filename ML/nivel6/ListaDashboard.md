###  checklists: Criterios para Visualización e Informes Interactivos

El objetivo no es solo *mostrar* datos, sino *comunicar* información de forma clara y permitir la *exploración* de manera intuitiva.

#### 1. Claridad y Simplicidad (El Mensaje) 🎯

Un dashboard debe ser entendido en segundos.

* [ ] **Definir la "Pregunta Principal":** ¿Cuál es la única pregunta que este dashboard debe responder? (Ej. "¿Estamos en riesgo de desabastecimiento?"). Todo el diseño debe girar en torno a esa respuesta.
* [ ] **Jerarquía Visual Clara:** Lo más importante (KPIs, alertas) debe ser lo más grande y estar ubicado en la esquina superior izquierda (donde la gente mira primero).
* [ ] **Evitar la Saturación (Chartjunk):** Menos es más. Elimina cualquier elemento que no aporte información:
    * Evita gráficos 3D.
    * Elimina sombras, fondos con imágenes o gradientes innecesarios.
    * Usa un máximo de 3-4 colores principales.
* [ ] **Usar el Gráfico Adecuado:** No uses un gráfico de pie para ver tendencias en el tiempo.
    * **Líneas:** Para tendencias en el tiempo (Ej. Nivel del embalse).
    * **Barras:** Para comparaciones (Ej. Nivel actual vs. Nivel máximo por central).
    * **Mapas:** Para datos geográficos (Ej. Ubicación de centrales).
    * **KPIs / "Tarjetas":** Para un solo número importante (Ej. Generación total MW).
* [ ] **Uso del Color con Intención:** El color no es decoración, es información.
    * **Categoría:** Usa colores distintos para cada central (Ej. Guatape siempre es azul).
    * **Magnitud:** Usa un gradiente de color (Ej. Rojo a Verde) para mostrar el `nivel_pct`.
    * **Alerta:** Usa un color brillante (Rojo) solo para resaltar problemas (Ej. Nivel Crítico).
* [ ] **Etiquetado Claro:** Los ejes, títulos y leyendas deben ser legibles y estar en lenguaje de negocio (Ej. "Nivel (msnm)" en lugar de `db_col_nivel_123`).

#### 2. Audiencia y Contexto (El Usuario) 🧑‍💻

El diseño debe cambiar dependiendo de quién lo va a usar.

* [ ] **Diseño Centrado en la Audiencia:** ¿Es para un **Gerente** (vista macro, KPIs, alertas) o para un **Ingeniero** (vista micro, filtros detallados, datos granulares)?
* [ ] **La Prueba de los 5 Segundos:** Muéstrale el dashboard a un usuario nuevo. Si en 5 segundos no puede decirte de qué se trata, el diseño ha fallado.
* [ ] **Indicar el Contexto de los Datos:** El usuario debe confiar en el informe.
    * ¿Se muestra la fecha de la **"Última Actualización"**? (Ej. "Datos actualizados: 28-oct-2025 08:00 AM").
    * ¿Se definen los cálculos? (Ej. Un ícono `(i)` que explique qué es el "Nivel Crítico").
* [ ] **Manejo de Datos Faltantes:** ¿Qué pasa si un sensor falla? El dashboard no debe romperse. Debe mostrar "N/A" o "Dato no disponible", no un "0" (que es un valor numérico) o un error.

#### 3. Interactividad con Propósito (La Exploración) 🖱️

La interactividad no es un truco; es una herramienta para responder preguntas secundarias.

* [ ] **Filtros Clave Visibles:** Los filtros más importantes (Rango de Fechas, Central) deben estar siempre a la vista, no escondidos en un menú.
* [ ] **Interacción Cruzada (Cross-filtering):** Esta es la clave de un informe interactivo.
    * *Ejemplo:* Al hacer clic en "Guatape" en el mapa (como hicimos), el gráfico de líneas debe filtrarse automáticamente para mostrar solo Guatape.
* [ ] **Tooltips (Información al pasar el mouse):** Al pasar el mouse sobre un punto del gráfico, se deben mostrar los detalles exactos (Ej. "Fecha: 20-oct-2025, Nivel: 1402.5 msnm").
* [ ] **Drill-Down (Profundizar):** El informe debe permitir ir de lo general a lo específico.
    * *Nivel 1:* Mapa de todas las centrales.
    * *Nivel 2 (Clic):* Gráfico de líneas de una central.
    * *(Opcional) Nivel 3 (Doble-Clic):* Tabla con los datos crudos de ese día.
* [ ] **"Botón de Reset":** Debe haber una forma fácil de deshacer todos los filtros y volver a la vista original.

#### 4. Rendimiento y Entrega (La Realidad) ⚡️

Un dashboard hermoso que tarda 1 minuto en cargar es un dashboard inútil.

* [ ] **Tiempo de Carga Rápido:** El objetivo debe ser **menos de 10 segundos** para la carga inicial.
    * **Optimización:** No cargar 10 años de datos en el dashboard. Cargar solo los últimos 90 días (como hicimos) y dejar que la base de datos maneje las consultas más pesadas.
* [ ] **Formato de Reporte Estático (PDF/HTML):**
    * **Legibilidad:** El PDF debe estar formateado para una página (A4/Carta). Los gráficos no deben cortarse entre páginas (como corregimos en el HTML).
    * **Autosuficiencia:** El PDF debe entenderse por sí solo, sin interactividad. Debe incluir la fecha y los filtros que se aplicaron (Ej. "Reporte para: Guatape, Fecha: 28-oct-2025").
* [ ] **Adaptabilidad (Responsive Design):** Si se va a consultar en el celular, el diseño debe reacomodarse. (Los mapas de Leaflet y los gráficos de Plotly hacen esto bastante bien).
