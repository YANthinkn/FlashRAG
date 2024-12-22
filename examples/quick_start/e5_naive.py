import argparse
from flashrag.config import Config
from flashrag.utils import get_dataset
from flashrag.pipeline import SequentialPipeline
from flashrag.prompt import PromptTemplate

parser = argparse.ArgumentParser()
parser.add_argument("--model_path", type=str)
parser.add_argument("--retriever_path", type=str)
args = parser.parse_args()

config_dict = {
    "data_dir": "dataset/FlashRAG_datasets/",
    # 2wikimultihopqa/musique
    "dataset_name": "2wikimultihopqa",
    # test / train
    "split": ["train"],
    "index_path": "e5_indexes/e5_Flat.index",
    "corpus_path": "dataset/wiki-18.jsonl",
    "model2path": {"e5": "models/e5-base-v2", "llama3-8B-instruct": "models/llama-3-8b"},
    "generator_model": "llama3-8B-instruct",
    "retrieval_method": "e5",
    "metrics": ['em','f1','acc','precision','recall','input_tokens'] ,
    "retrieval_topk": 10,
    "save_intermediate_data": True,
    # GPU
    "gpu_id": "1",
}

config = Config(config_dict=config_dict)

all_split = get_dataset(config)
# test / train
test_data = all_split["train"]
prompt_templete = PromptTemplate(
    config,
    system_prompt="Answer the question based on the given document. \
                    Only give me the answer and do not output any other words. \
                    \nThe following are given documents.\n\n{reference}",
    user_prompt="Question: {question}\nAnswer:",
)


pipeline = SequentialPipeline(config, prompt_template=prompt_templete)


output_dataset = pipeline.run(test_data, do_eval=True)
print("---generation output by e5---")
print(output_dataset.pred)

