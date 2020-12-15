import uvicorn

uvicorn.run("app:app", host="192.168.2.17", port=80, workers=1)
