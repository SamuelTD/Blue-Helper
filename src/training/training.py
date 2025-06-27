from datasets import load_dataset, Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForQuestionAnswering,
    TrainingArguments,
    Trainer,
)

# Flatten the nested SQuAD-style dataset
def flatten_squad(example):
    new_examples = []
    for paragraph in example["paragraphs"]:
        context = paragraph["context"]
        for qa in paragraph["qas"]:
            new_examples.append({
                "context": context,
                "question": qa["question"],
                "answers": {
                    "text": [ans["text"] for ans in qa["answers"]],
                    "answer_start": [ans["answer_start"] for ans in qa["answers"]]
                }
            })
    return new_examples

# ---------- STEP 2: Preprocessing ----------
def preprocess_function(example, tokenizer):
    inputs = tokenizer(
        example["question"],
        example["context"],
        max_length=384,
        truncation="only_second",
        stride=128,
        return_overflowing_tokens=True,
        return_offsets_mapping=True,
        padding="max_length"
    )

    sample_mapping = inputs.pop("overflow_to_sample_mapping")
    offset_mapping = inputs.pop("offset_mapping")

    start_positions = []
    end_positions = []

    for i, offsets in enumerate(offset_mapping):
        input_ids = inputs["input_ids"][i]
        cls_index = input_ids.index(tokenizer.cls_token_id)
        sequence_ids = inputs.sequence_ids(i)
        sample_index = sample_mapping[i]
        answer = example["answers"][sample_index]
        start_char = answer["answer_start"][0]
        end_char = start_char + len(answer["text"][0])

        token_start_index = 0
        while sequence_ids[token_start_index] != 1:
            token_start_index += 1

        token_end_index = len(input_ids) - 1
        while sequence_ids[token_end_index] != 1:
            token_end_index -= 1

        if not (offsets[token_start_index][0] <= start_char and offsets[token_end_index][1] >= end_char):
            start_positions.append(cls_index)
            end_positions.append(cls_index)
        else:
            for idx in range(token_start_index, token_end_index + 1):
                if offsets[idx][0] <= start_char < offsets[idx][1]:
                    start_pos = idx
                if offsets[idx][0] < end_char <= offsets[idx][1]:
                    end_pos = idx
            start_positions.append(start_pos)
            end_positions.append(end_pos)

    inputs["start_positions"] = start_positions
    inputs["end_positions"] = end_positions
    return inputs


# ---------- MAIN TRAINING PIPELINE ----------
def main():
    squad_file = "src/data/squad_data.json"           # Converted file
    output_model_dir = "bert-azurebot"       # Output model directory
    model_name = "deepset/bert-base-cased-squad2"

    # Load the dataset
    raw_datasets = load_dataset("json", data_files={"train": squad_file}, field="data")

    train_data = []
    for item in raw_datasets["train"]:
        train_data.extend(flatten_squad(item))
    train_dataset = Dataset.from_list(train_data)


    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForQuestionAnswering.from_pretrained(model_name)

    tokenized_data = train_dataset.map(
        lambda x: preprocess_function(x, tokenizer),
        batched=True,
        remove_columns=train_dataset.column_names
    )

    training_args = TrainingArguments(
        output_dir=output_model_dir,
        per_device_train_batch_size=2,
        num_train_epochs=1,
        learning_rate=3e-5,
        weight_decay=0.01,
        logging_steps=50,
        save_steps=500,
        save_total_limit=1,
        remove_unused_columns=False,
        gradient_accumulation_steps=4
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_data,
        tokenizer=tokenizer,
    )

    print("🚀 Training begins...")
    trainer.train()
    print("✅ Training complete!")

    trainer.save_model(output_model_dir)
    tokenizer.save_pretrained(output_model_dir)
    print(f"📦 Model saved to: {output_model_dir}")

if __name__ == "__main__":
    main()
