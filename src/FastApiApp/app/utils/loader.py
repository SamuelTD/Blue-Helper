from huggingface_hub import hf_hub_download
import faiss
import pickle

def load_index_and_data():
    index_path = hf_hub_download(repo_id="LudivineRB/azure-qa-index", filename="faiss_index.idx", repo_type="dataset")
    data_path = hf_hub_download(repo_id="LudivineRB/azure-qa-index", filename="qa_data.pkl", repo_type="dataset")

    index = faiss.read_index(index_path)

    with open(data_path, "rb") as f:
        data = pickle.load(f)

    return index, data["questions"], data["answers"]
