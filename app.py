from app import socketio, app


if __name__ == '__main__':
    socketio.run(app, debug=True)
#, certfile='./ssl/server.crt', keyfile='./ssl/server.key'