from datetime import datetime

def hello_world(host: str) -> dict[str, str]:
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {
        "message": "Hello, world!",
        "current_time": current_time,
        "host": host
    }
