from pathlib import Path
import time
import gradio as gr
import torch
from transformers import pipeline

device = 0 if torch.cuda.is_available() else -1

classifier = pipeline(
    task="image-classification",
    model="google/mobilenet_v2_1.0_224",
    device=device,
)


def cargar_ejemplos(carpeta="ejemplos"):
    ruta = Path(carpeta)
    if not ruta.is_dir():
        return []
    extensiones = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
    return [
        [str(archivo)]
        for archivo in sorted(ruta.iterdir())
        if archivo.is_file() and archivo.suffix.lower() in extensiones
    ]


def clasificar(imagen):
    if imagen is None:
        return {}, "0.00 s"

    inicio = time.perf_counter()
    resultados = classifier(imagen, top_k=3)
    if torch.cuda.is_available():
        torch.cuda.synchronize()
    duracion = time.perf_counter() - inicio

    predicciones = {
        item["label"]: round(float(item["score"]) * 100, 2) for item in resultados
    }
    tiempo_texto = f"{duracion:.2f} s"
    return predicciones, tiempo_texto

demo = gr.Interface(
    fn=clasificar,
    inputs=gr.Image(type="pil", label="Sube o arrastra una IMAGEN"),
    outputs=[
        gr.Label(num_top_classes=3, label="Top 3 predicciones (%)"),
        gr.Textbox(label="Tiempo de inferencia"),
    ],
    examples=cargar_ejemplos("ejemplos"),
    title="¿Qué hay en la foto?",
    description="Clasifica imágenes usando el modelo google/mobilenet_v2_1.0_224.",
)

if __name__ == "__main__":
    demo.launch()