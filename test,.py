import argparse
import multiprocessing as mp
from datasets import load_dataset
from tokenizers import BertWordPieceTokenizer
import os

def process_dataset(dataset_name, vocab_size, limit_alphabet, token, temp_dir):
    print(f"Processing dataset: {dataset_name}")
    fw = load_dataset("HuggingFaceFW/fineweb", name=dataset_name, split="train", streaming=True, token=token)
    
    # BertWordPieceTokenizer 초기화
    tokenizer = BertWordPieceTokenizer(
        clean_text=True,
        handle_chinese_chars=True,
        strip_accents=False,  # cased 모델의 경우 False
        lowercase=False,
        wordpieces_prefix="##"
    )
    
    texts = []
    for example in fw:
        tokenizer.train_from_iterator(example['text'], limit_alphabet=limit_alphabet, vocab_size=vocab_size)

    # 각 데이터셋의 vocab 파일을 임시 디렉토리에 저장
    output_vocab_file = os.path.join(temp_dir, f"vocab_{dataset_name}.json")
    tokenizer.save_model(temp_dir, f"vocab_{dataset_name}")
    print(f"Vocab file for {dataset_name} saved as {output_vocab_file}")
    return output_vocab_file

def merge_vocab_files(vocab_files, output_file):
    from collections import Counter
    import json

    combined_vocab = Counter()

    for vocab_file in vocab_files:
        with open(vocab_file, 'r', encoding='utf-8') as f:
            vocab = json.load(f)
            combined_vocab.update(vocab)

    # 상위 vocab_size만 남기기
    combined_vocab = dict(combined_vocab.most_common(args.vocab_size))

    # combined_vocab을 파일로 저장
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(combined_vocab, f, ensure_ascii=False, indent=4)
    print(f"Merged vocab file saved as {output_file}")

def main(vocab_size, limit_alphabet, token):
    datasets = [
        "CC-MAIN-2024-18",
        "CC-MAIN-2024-10",
        "CC-MAIN-2023-50",
        "CC-MAIN-2023-40",
        "CC-MAIN-2023-23",
        "CC-MAIN-2023-14",
        "CC-MAIN-2023-06",
        "CC-MAIN-2022-49",
        "CC-MAIN-2022-40",
        "CC-MAIN-2022-33",
        "CC-MAIN-2022-27",
        "CC-MAIN-2022-21",
        "CC-MAIN-2022-05",
        "CC-MAIN-2021-49",
        "CC-MAIN-2021-43",
        "CC-MAIN-2021-39",
        "CC-MAIN-2021-31",
        "CC-MAIN-2021-25",
        "CC-MAIN-2021-21",
        "CC-MAIN-2021-17",
        "CC-MAIN-2021-10",
        "CC-MAIN-2021-04",
        "CC-MAIN-2020-50",
        "CC-MAIN-2020-45",
        "CC-MAIN-2020-40",
        "CC-MAIN-2020-34",
        "CC-MAIN-2020-29",
        "CC-MAIN-2020-24",
        "CC-MAIN-2020-16",
        "CC-MAIN-2020-10",
        "CC-MAIN-2020-05",
        "CC-MAIN-2019-51",
        "CC-MAIN-2019-47",
        "CC-MAIN-2019-43",
        "CC-MAIN-2019-39",
        "CC-MAIN-2019-35",
        "CC-MAIN-2019-30",
        "CC-MAIN-2019-26",
        "CC-MAIN-2019-22",
        "CC-MAIN-2019-18",
        "CC-MAIN-2019-13",
        "CC-MAIN-2019-09",
        "CC-MAIN-2019-04",
        "CC-MAIN-2018-51",
        "CC-MAIN-2018-47",
        "CC-MAIN-2018-43",
        "CC-MAIN-2018-39",
        "CC-MAIN-2018-34",
        "CC-MAIN-2018-30",
        "CC-MAIN-2018-26",
        "CC-MAIN-2018-22",
        "CC-MAIN-2018-17",
        "CC-MAIN-2018-13",
        "CC-MAIN-2018-09",
        "CC-MAIN-2018-05",
        "CC-MAIN-2017-51",
        "CC-MAIN-2017-47",
        "CC-MAIN-2017-43",
        "CC-MAIN-2017-39",
        "CC-MAIN-2017-34",
        "CC-MAIN-2017-30",
        "CC-MAIN-2017-26",
        "CC-MAIN-2017-22",
        "CC-MAIN-2017-17",
        "CC-MAIN-2017-13",
        "CC-MAIN-2017-09",
        "CC-MAIN-2017-04",
        "CC-MAIN-2016-50",
        "CC-MAIN-2016-44",
        "CC-MAIN-2016-40",
        "CC-MAIN-2016-36",
        "CC-MAIN-2016-30",
        "CC-MAIN-2016-26",
        "CC-MAIN-2016-22",
        "CC-MAIN-2016-18",
        "CC-MAIN-2016-07",
        "CC-MAIN-2015-48",
        "CC-MAIN-2015-40",
        "CC-MAIN-2015-35",
        "CC-MAIN-2015-32",
        "CC-MAIN-2015-27",
        "CC-MAIN-2015-22",
        "CC-MAIN-2015-18",
        "CC-MAIN-2015-14",
        "CC-MAIN-2015-11",
        "CC-MAIN-2015-06",
        "CC-MAIN-2014-52",
        "CC-MAIN-2014-49",
        "CC-MAIN-2014-42",
        "CC-MAIN-2014-41",
        "CC-MAIN-2014-35",
        "CC-MAIN-2014-23",
        "CC-MAIN-2014-15",
        "CC-MAIN-2014-10",
        "CC-MAIN-2013-48",
        "CC-MAIN-2013-20"
    ]

    temp_dir = "./temp_vocabs"
    os.makedirs(temp_dir, exist_ok=True)
    
    with mp.Pool(processes=mp.cpu_count()) as pool:
        results = [pool.apply_async(process_dataset, (dataset, vocab_size, limit_alphabet, token, temp_dir)) for dataset in datasets]
        vocab_files = [p.get() for p in results]

    merge_vocab_files(vocab_files, f"merged_vocab_{limit_alphabet}_{vocab_size}.json")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--vocab_size", type=int, default=1000000, help="Number of tokens in the vocabulary")
    parser.add_argument("--limit_alphabet", type=int, default=10000, help="Maximum different characters to include in the vocabulary")
    
    args = parser.parse_args()
    
    main(args.vocab_size, args.limit_alphabet, "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")
