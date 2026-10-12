import requests
import base64

# 这里我为你挑选了几个目前 GitHub 上更新比较稳定的免费节点源
SOURCES = [
    "https://raw.githubusercontent.com/freefq/free/master/v2",
    "https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub",
    "https://raw.githubusercontent.com/aiboboxx/v2rayfree/main/v2"
]

def decode_base64(data):
    """尝试解密 base64，如果是明文则直接返回"""
    try:
        # 补齐 '=' 防止解密报错
        missing_padding = len(data) % 4
        if missing_padding:
            data += '=' * (4 - missing_padding)
        return base64.b64decode(data).decode('utf-8')
    except Exception:
        return data

def fetch_nodes():
    all_nodes = []
    for url in SOURCES:
        print(f"正在抓取: {url}")
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                text = resp.text.strip()
                # 如果内容中没有链接协议头，说明它大概率被整体 base64 加密了
                if '://' not in text:
                    text = decode_base64(text)
                
                # 按行分割，提取有效节点
                for line in text.splitlines():
                    line = line.strip()
                    if line and '://' in line:
                        all_nodes.append(line)
        except Exception as e:
            print(f"抓取失败 {url}: {e}")
            
    # 去重处理，避免大量重复节点导致软件卡顿
    unique_nodes = list(set(all_nodes))
    
    # 重新进行 Base64 编码（这是各大代理软件和转换工具最标准的订阅读取格式）
    raw_text = '\n'.join(unique_nodes)
    encoded_text = base64.b64encode(raw_text.encode('utf-8')).decode('utf-8')
    
    # 将结果写入 txt 文件
    with open("my_nodes.txt", "w", encoding="utf-8") as f:
        f.write(encoded_text)
        
    print(f"成功合并并更新了 {len(unique_nodes)} 个去重节点！")

if __name__ == "__main__":
    fetch_nodes()