用 python 做一個可以將PDF文件逐頁轉成圖片的工具。

要使用這個工具可以透過CLI介面或是使用 docker 搭建server，再透過 client端的函式庫進行交互。

使用 CLI 介面時建議先建立虛擬環境(python venv 或是 uv ...等都可以)，使用 `pip install -e .` 安裝。

使用docker 部署 server 時可以透過 docker-compose 快速啟動。