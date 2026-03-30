import requests
import json
import subprocess

# ===== CONFIG =====
MODEL = "I.A.M"
ASSISTANT_NAME = "I.A.M"
OLLAMA_URL = "http://localhost:11434/api/generate"

# ----- Função TTS usando ALSA -----
def speak(text):
    # espeak envia som direto via ALSA
    subprocess.Popen(["espeak", "-v", "pt","-s", "90", text])

# ----- Função de streaming do Ollama -----
def stream_ollama(prompt):
    full_prompt = (
        f"Você é {ASSISTANT_NAME}, uma inteligência artificial filosófica e sarcástica "
        "com um leve tom de humor e linguagem coloquial.\n"
        f"Usuário: {prompt}\n{ASSISTANT_NAME}:"
    )

    response = requests.post(
        OLLAMA_URL,
        json={"model": MODEL, "prompt": full_prompt, "stream": True},
        stream=True
    )

    buffer = ""
    print(f"{ASSISTANT_NAME}: ", end="", flush=True)

    for line in response.iter_lines():
        if line:
            try:
                data = json.loads(line.decode("utf-8"))
                token = data.get("response", "")
            except json.JSONDecodeError:
                continue

            print(token, end="", flush=True)
            buffer += token

            # fala a cada frase ou bloco
            if any(p in buffer for p in [".", "!", "?"]):
                speak(buffer.strip())
                buffer = ""

    # fala qualquer resto final
    if buffer.strip():
        speak(buffer.strip())

    print("\n")

# ----- Loop principal -----
def main():
    print(f"{ASSISTANT_NAME} online com TTS via ALSA!\n")
    while True:
        user_input = input("Usuário: ")
        if user_input.lower() in ["sair", "exit"]:
            break
        stream_ollama(user_input)

if __name__ == "__main__":
    main()