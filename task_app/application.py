##prospect_app
import uvicorn


def app(scope, receive, send):
    ...

if __name__ == "__main__":
    uvicorn.run("main:app", host="172.16.10.149", port=4006,reload=True, log_level="info",env_file=".env")