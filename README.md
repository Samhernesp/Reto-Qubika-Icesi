# Comparador de Noticias con Narración

Aplicación interactiva diseñada para buscar, comparar y generar narraciones de noticias relacionadas sobre un tema específico, cuenta con una pequeña base de datos de noticias. La aplicación utiliza herramientas avanzadas de procesamiento de lenguaje natural y síntesis de voz para brindar una experiencia informativa y accesible.

---

## **Descripción del Proyecto**

Este proyecto permite a los usuarios:

1. **Buscar noticias relacionadas** sobre un tema ingresado en un cuadro de texto.
2. **Comparar noticias relevantes** y obtener resúmenes generados automáticamente.
3. **Escuchar narraciones** de la comparación generadas por un modelo de síntesis de voz.
4. **Visualizar similitudes** entre noticias mediante una matriz interactiva.

### **Características Técnicas**

- **Búsqueda Semántica**: Utiliza embeddings generados con `SentenceTransformer` para encontrar las noticias más relevantes.
- **Resúmenes Generados**: Emplea un modelo generativo (Gemini AI) para resumir los artículos.
- **Narración de Comparaciones**: Convierte texto en audio utilizando tecnologías como Eleven Labs Text to Speech.
- **Visualización de Similitudes**: Muestra relaciones entre noticias con una matriz de similitud generada por embeddings.

---

## **Tecnologías Utilizadas**

- **Lenguaje de Programación**: Python
- **Framework Web**: [Streamlit](https://streamlit.io/)
- **Modelos de Lenguaje**:
  - [SentenceTransformers](https://www.sbert.net/)
  - [Google Generative AI (Gemini)](https://cloud.google.com/ai/generative-ai)
- **Base de Datos Vectorial**: [Pinecone](https://www.pinecone.io/)
- **Visualización**:
  - Matplotlib
  - Seaborn
- **Síntesis de Voz**:
  - Eleven Labs Text-to-Speech

---

## **Despliegue**

La aplicación está desplegada en **Streamlit Community Cloud** y puedes acceder a ella en el siguiente enlace:

🔗 [https://reto-qubika.streamlit.app](https://reto-qubika.streamlit.app)

En el despliegue anterior no es posible apreciar el audio generado por políticas de Eleven Labs por lo tanto en el siguiente video se puede apreciar como debería ser su funcionamiento normal:

[https://youtu.be/QFC7uTfGbbU](https://youtu.be/QFC7uTfGbbU)

---

## **Cómo Usar la Aplicación**

1. Ingresa un tema de interés en el cuadro de texto (por ejemplo, "Economia en Colombia").
2. Haz clic en el botón "Buscar noticias relacionadas".
3. Explora las noticias relacionadas y sus resúmenes.
4. Escucha la narración de la comparación generada automáticamente.
5. Visualiza la matriz de similitudes para identificar relaciones entre noticias.

---

## **Requisitos para Despliegue Local**

Si deseas ejecutar la aplicación localmente, sigue estos pasos:

### **1. Clonar el Repositorio**
```bash
git clone https://github.com/tu-usuario/tu-repositorio.git
cd tu-repositorio
```

### **2. Instalar Dependencias**
Asegúrate de tener Python 3.9 o superior. Luego, instala las dependencias:
```bash
pip install -r requirements.txt
```

### **3. Configurar Variables de Entorno**
Crea un archivo .env en el directorio principal con las siguientes claves:
```bash
GEMINI_API=tu_clave_gemini
PINECONE_KEY=tu_clave_pinecone
ELLABS_KEY=tu_clave_elevenlabs
```

### **4. Ejecutar la Aplicación**
Ejecuta la aplicación con el siguiente comando:
```bash
streamlit run app.py
```

Accede a la aplicación en [http://localhost:8501](http://localhost:8501).
