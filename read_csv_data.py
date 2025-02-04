import pandas as pd
import chardet
import tensorflow as tf # 導入 tensorflow
import numpy as np # 導入 numpy

def detect_encoding(file_path):
    """
    使用 chardet 偵測檔案編碼。
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
    """
    detected_encoding = detect_encoding(file_path)
    if not detected_encoding:
        print("警告：無法偵測檔案編碼，將嘗試使用預設編碼 utf-8")
        detected_encoding = 'utf-8'

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

def create_lstm_model(): # 新增 create_lstm_model 函式
    """
    建立 LSTM 模型 (初步版本，模型結構可調整)。
    """
    model = tf.keras.models.Sequential([
        tf.keras.layers.LSTM(50, input_shape=(None, 2)), # LSTM 層，input_shape 假設輸入序列的特徵數為 2 (例如車速和車流量)
        tf.keras.layers.Dense(3, activation='linear') # Dense 層，輸出 3 個預測值 (車速、車流量、壅塞程度)
    ])
    model.compile(optimizer='adam', loss='mse') # 使用 Adam 優化器和均方誤差損失函數
    return model

def analyze_traffic_flow(chunk_dataframe, lstm_model): # 修改 analyze_traffic_flow 函式，加入 lstm_model 參數
    """
    使用 LSTM 模型分析交通流量數據，預測車速、車流量和壅塞程度，並提出應變措施建議。
    """
    if chunk_dataframe.empty:
        return "數據塊為空，無法分析。"

    try:
        print("DataCollectTime 欄位前 5 個值:")
        print(chunk_dataframe['DataCollectTime'].head())

        chunk_dataframe['DataCollectTime'] = pd.to_datetime(chunk_dataframe['DataCollectTime'], errors='coerce') 
        # 為了簡化，我們只使用 LinkID、Speed 和 Volume 作為 LSTM 模型的輸入特徵
        # **資料準備 (簡化版)**: 假設每個 LinkID 的數據都是一個時間序列，只取前幾行資料示範
        sample_link_id = chunk_dataframe['LinkID'].iloc[0] # 取第一個 LinkID 作為示範
        link_data = chunk_dataframe[chunk_dataframe['LinkID'] == sample_link_id][['Speed', 'Volume']].head(10).values # 取前 10 行 Speed 和 Volume 資料
        if len(link_data) < 10: # 如果資料少於 10 行，則跳過
            return f"LinkID {sample_link_id} 數據不足，跳過分析。"

        # **模型預測 (簡化版)**: 使用未訓練的模型進行預測，僅為示範流程
        link_data_reshaped = np.reshape(link_data, (1, 10, 2)) # reshape 成 LSTM 模型輸入要求的 shape (batch_size, timesteps, features)
        predicted_traffic = lstm_model.predict(link_data_reshaped) # 進行預測，predicted_traffic 包含預測的 [車速, 車流量, 壅塞程度]

        predicted_speed, predicted_volume, congestion_level = predicted_traffic[0] # 解包預測結果

        congestion_threshold_level = 0.7 # 壅塞程度閾值，暫定 0.7，可調整
        if congestion_level > congestion_threshold_level:
            suggestion = "預測重點路段可能發生嚴重壅塞，建議立即啟動交通應變措施，例如加強號誌控制、發布交通資訊等。"
        elif congestion_level > 0.4: # 中度壅塞
            suggestion = "預測重點路段可能發生中度壅塞，建議加強監控，並準備啟動交通疏導措施。"
        else:
            suggestion = "預測目前交通狀況正常。"

        return f"LinkID {sample_link_id} 交通流量預測分析結果:\n預測車速: {predicted_speed:.2f} km/h, 預測車流量: {predicted_volume:.2f} 輛/分鐘, 預測壅塞程度: {congestion_level:.2f}\n應變措施建議: {suggestion}"

    except Exception as e:
        return f"分析交通流量時發生錯誤：{e}"


if __name__ == '__main__':
    file_path = r"D:\Old.D_\大學\專題\競賽資料\Data\traffic_data.csv"
    csv_reader = read_large_csv(file_path)
    lstm_model = create_lstm_model() # 建立 LSTM 模型

    if csv_reader:
        try:
            for chunk_dataframe in csv_reader:
                print("讀取到一個數據塊，形狀:", chunk_dataframe.shape)
                print(chunk_dataframe.head())
                analysis_result = analyze_traffic_flow(chunk_dataframe, lstm_model) # 進行交通流量分析，並傳入 lstm_model
                print("\n交通流量分析結果:")
                print(analysis_result)
                print("-" * 50)
        except StopIteration:
            print("CSV 檔案讀取完成")
        except Exception as e:
            print(f"處理 CSV 數據塊時發生錯誤：{e}")
