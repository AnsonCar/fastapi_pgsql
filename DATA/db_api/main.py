# API 主文件
import uvicorn
from setting import API_PORT, API_DEBUG

if __name__ == "__main__":
    uvicorn.run("src.app:app", host="0.0.0.0", port=API_PORT, reload=API_DEBUG)
