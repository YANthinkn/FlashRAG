import re

# 提取文件中每一行的 id
def extract_ids_from_file(file_path):
    ids = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # 匹配形如 'id': '123456' 的字段
            id_pattern = re.compile(r"'id':\s*'(\d+)'")  # 匹配 id 字段
            for line in file:
                match = id_pattern.search(line)
                if match:
                    ids.append(match.group(1))  # 提取到的 id
        return ids
    except Exception as e:
        print(f"读取文件时发生错误: {e}")
        return []

# 对比两个文件中的 id
def compare_ids(ids1, ids2):
    # 找出位置发生变化的记录
    changed_positions = []
    for i, (id1, id2) in enumerate(zip(ids1, ids2)):
        if id1 != id2:
            changed_positions.append(i)
    
    # 计算变化比例
    total_records = len(ids1)
    changed_percentage = (len(changed_positions) / total_records) * 100 if total_records > 0 else 0
    
    # 输出结果
    print(f"发生位置变化的记录数量：{len(changed_positions)}")
    print(f"占总记录的比例：{changed_percentage:.2f}%")

# 示例文件路径
file1 = 'Reranker_20241127_165357.txt'
file2 = 'RerankerAfter_20241127_165357.txt'
# 提取id
ids1 = extract_ids_from_file(file1)
ids2 = extract_ids_from_file(file2)

# 对比id并输出变化情况
compare_ids(ids1, ids2)

