from typing import Dict, Any, Union
import numpy as np
from flashrag.dataset import Dataset


def convert_numpy(obj: Union[Dict, list, np.ndarray, np.generic]) -> Any:
    """Recursively convert numpy objects in nested dictionaries or lists to native Python types."""
    if isinstance(obj, dict):
        return {k: convert_numpy(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy(i) for i in obj]
    elif isinstance(obj, np.ndarray):
        return obj.tolist()  # Convert numpy arrays to lists
    elif isinstance(obj, (np.integer, np.floating)):
        return obj.item()  # Convert numpy scalars to native Python scalars
    elif isinstance(obj, np.float32):
        return float(obj)
    else:
        return obj  # Return the object as-is if it's neither a dict, list, nor numpy type


def filter_dataset(dataset: Dataset, filter_func=None):
    if filter_func is None:
        return dataset
    data = dataset.data
    for item in data:
        if not filter_func(item):
            data.remove(item)
    return Dataset(config=dataset.config, data=data)


def split_dataset(dataset: Dataset, split_symbol: list):
    assert len(split_symbol) == len(dataset)

    data = dataset.data
    data_split = {symbol: [] for symbol in set(split_symbol)}
    for symbol in set(split_symbol):
        symbol_data = [x for x, x_symbol in zip(data, split_symbol) if x_symbol == symbol]
        data_split[symbol] = Dataset(config=dataset.config, data=symbol_data)

    return data_split


def merge_dataset(dataset_split: dict, split_symbol: list):
    assert len(split_symbol) == sum([len(data) for data in dataset_split.values()])
    dataset_split_iter = {symbol: iter(dataset.data) for symbol, dataset in dataset_split.items()}

    final_data = []
    for item_symbol in split_symbol:
        final_data.append(next(dataset_split_iter[item_symbol]))
    final_dataset = Dataset(config=list(dataset_split.values())[0].config, data=final_data)

    return final_dataset


def get_batch_dataset(dataset: Dataset, batch_size=16):
    data = dataset.data
    for idx in range(0, len(data), batch_size):
        batched_data = data[idx : idx + batch_size]
        batch_dataset = Dataset(config=dataset.config, data=batched_data)
        yield batch_dataset


def merge_batch_dataset(dataset_list: Dataset):
    dataset = dataset_list[0]
    total_data = []
    for batch_dataset in dataset_list:
        total_data.extend(batch_dataset.data)
    dataset = Dataset(config=dataset.config, data=total_data)
    return dataset
