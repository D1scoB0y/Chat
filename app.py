from app import socketio, app


if __name__ == '__main__':
    socketio.run(app, debug=True)

'''
    https пока что не работает должным образом
'''
#certfile='./ssl/cert.pem', keyfile='./ssl/key.pem', server_side=True
