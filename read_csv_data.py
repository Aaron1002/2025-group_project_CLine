import pandas as pd
import chardet

def detect_encoding(file_path):
    """
    使用 chardet 偵測檔案編碼。

    Args:
        file_path (str): 檔案路徑。

    Returns:
        str: 偵測到的編碼方式，如果偵測失敗則返回 None。
    """
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            return result['encoding']
    except Exception as e:
        print(f"偵測檔案編碼時發生錯誤：{e}")
        return None

def read_large_csv(file_path, chunk_size=10000):
    """
    高效讀取大型 CSV 檔案並返回一個可迭代的 DataFrame 塊，自動偵測編碼。

    Args:
        file_path (str): CSV 檔案的路徑。
        chunk_size (int): 每次讀取的行數，用於分塊讀取。

    Returns:
        pandas.io.parsers.TextFileReader: 可迭代的 DataFrame 塊。
    """
    detected_encoding = detect_encoding(file_path)
    if not detected_encoding:
        print("警告：無法偵測檔案編碼，將嘗試使用預設編碼 utf-8")
        detected_encoding = 'utf-8'  # 預設編碼

    print(f"偵測到的檔案編碼：{detected_encoding}")

    try:
        csv_reader = pd.read_csv(file_path, chunksize=chunk_size, iterator=True, encoding=detected_encoding)
        return csv_reader
    except FileNotFoundError:
        print(f"錯誤：找不到檔案於 {file_path}")
        return None
    except Exception as e:
        print(f"讀取 CSV 檔案時發生錯誤：{e}")
        return None

if __name__ == '__main__':
    file_path = r"D:\Old.D_\大學\專題\競賽資料\Data\traffic_data.csv"  # 替換成你的 CSV 檔案路徑
    csv_reader = read_large_csv(file_path)

    if csv_reader:
        try:
            for chunk_dataframe in csv_reader:
                # 在這裡處理每個 DataFrame 塊，例如進行初步分析或預處理
                print("讀取到一個數據塊，形狀:", chunk_dataframe.shape)
                print(chunk_dataframe.head()) # 印出每個數據塊的前幾行
                # 為了演示，我們在這裡只打印數據塊的形狀，你可以根據需要修改
        except StopIteration:
            print("CSV 檔案讀取完成")
        except Exception as e:
            print(f"處理 CSV 數據塊時發生錯誤：{e}")