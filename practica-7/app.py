import gradio as gr
import torch
from transformers import pipeline

device = 0 if torch.cuda.is_available() else -1

classifier = pipeline(
    task="image-classification",
    model="google/mobilenet_v2_1.0_224",
    device=device,
)


def clasificar(imagen):
    if imagen is None:
        return {}

    resultados = classifier(imagen, top_k=3)
    return {item["label"]: round(float(item["score"]) * 100, 2) for item in resultados}


demo = gr.Interface(
    fn=clasificar,
    inputs=gr.Image(type="pil", label="Sube o arrastra una imagen"),
    outputs=gr.Label(num_top_classes=3, label="Top 3 predicciones (%)"),
    title="¿Qué hay en la foto?",
    description="Clasifica imágenes usando el modelo google/mobilenet_v2_1.0_224.",
)

if __name__ == "__main__":
    demo.launch()