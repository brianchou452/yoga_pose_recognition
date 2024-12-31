# 瑜伽姿勢辨識

這是一個使用 MediaPipe 的人體姿態辨識技術來輔助瑜伽練習。透過即時的姿勢偵測與分析，改善瑜伽姿勢的準確性，進練習效果。

## Usage

### Backend

這個專案使用 poetry。它是一個現代的依賴管理工具。

要在本機運行專案，請使用以下命令：  
（你需要先在電腦上裝好 poetry）

```bash
poetry config virtualenvs.path .venv
poetry config virtualenvs.in-project true  
poetry install
```

> [!TIP]
> 如果你想要啟動 Python server，請使用以下命令：
> `poetry run python -m yoga_pose_recognition`

### UI

```bash
npm install
```

### Start

Electron 會自動啟動 Python server，所以只需要啟動UI即可。

```bash
npm run start
```

> [!NOTE]
> electron builder config 沒有設定好，所以目前只能在開發模式下運行。
