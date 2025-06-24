import json
from transformers import pipeline

# === CONFIG ===
model_path = "src/models/v02"        # Path to your fine-tuned model directory
squad_path = "src/data/squad_data.json"            # Your SQuAD-format dataset file

# === LOAD PIPELINE ===
qa_pipeline = pipeline("question-answering", model=model_path, tokenizer=model_path)
print("✅ Loaded model and tokenizer.")

# === LOAD DATA ===
with open(squad_path, "r", encoding="utf-8") as f:
    squad_json = json.load(f)

examples = []
for paragraph in squad_json["data"][0]["paragraphs"]:
    context = paragraph["context"]
    for qa in paragraph["qas"]:
        examples.append({
            "id": qa["id"],
            "question": qa["question"],
            "context": context,
            "true_answer": qa["answers"][0]["text"]
        })

# === EVALUATE ===
print(f"🔍 Evaluating {len(examples)} questions...\n")
correct = 0
total = len(examples)

for ex in examples:
    result = qa_pipeline({
        "question": ex["question"],
        "context": ex["context"]
    })

    predicted = result["answer"].strip()
    expected = ex["true_answer"].strip()
    confidence = result["score"]

    is_correct = predicted.lower() == expected.lower()

    print(f"Q: {ex['question']}")
    print(f"Expected: {expected}")
    print(f"Predicted: {predicted}")
    print(f"Score: {confidence:.4f} | {'✅' if is_correct else '❌'}\n")

    if is_correct:
        correct += 1

# === SUMMARY ===
accuracy = correct / total * 100
print(f"\n✅ Evaluation complete. Accuracy: {correct}/{total} = {accuracy:.2f}%")
