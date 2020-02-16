import socket
from flask import Flask
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def client():
    return render_template('client.html')

#background process happening without any refreshing
@app.route('/background_process_test')
def background_process_test():
    TCP_IP = 'localhost'
    TCP_PORT = 9001
    BUFFER_SIZE = 1024
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    with open('received_file', 'wb') as f:
        print ('file opened')
        while True:
            #print('receiving data...')
            data = s.recv(BUFFER_SIZE)
            print('data=%s', (data))
            if not data:
                f.close()
                print ('file close()')
                break
            # write data to a file
            f.write(data)

    print('Successfully get the file')
    s.close()
    print('connection closed')
    return {"status":200}

if __name__ == '__main__':
    app.run(host="127.0.0.1",port="8081")