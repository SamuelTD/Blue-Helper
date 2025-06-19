import json
import uuid

# Load your flat corpus
with open("src/qa.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

# Convert to SQuAD format
squad_data = {
    "data": [
        {
            "title": "Azure Portal",
            "paragraphs": []
        }
    ]
}

index = 0
for item in raw_data:
    context = item["answer"]
    question = item["question"]
    qid = str(uuid.uuid4())  # fallback to auto-generated ID
    category = item.get("category", "")
    tags = item.get("tags", [])

    answer_start = context.find(item["answer"])
    if answer_start == -1:
        print(f"Warning: Answer not found in context for {qid}")
        continue

    squad_data["data"][0]["paragraphs"].append({
        "context": context,
        "qas": [
            {
                "id": qid,
                "question": question,
                "answers": [
                    {
                        "text": item["answer"],
                        "answer_start": answer_start
                    }
                ],
                "is_impossible": False,
                "metadata": {
                    "category": category,
                    "tags": tags
                }
            }
        ]
    })
    
    index += 1

# Save as SQuAD-style JSON
with open("squad_data.json", "w", encoding="utf-8") as f:
    json.dump(squad_data, f, indent=2, ensure_ascii=False)

print("✅ SQuAD-style dataset saved to squad_data.json")
