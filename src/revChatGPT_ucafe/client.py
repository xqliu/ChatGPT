# Ref: https://www.cnblogs.com/jason-huawen/p/16212668.html

import socket
import json
import sys
import optparse

class UDPClient:
    def __init__(self, target, port):
        self.target = target
        self.port = port
        self.client_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Connecting to TCP server: %s %d" % (self.target, self.port))
        self.client_s.connect((self.target, self.port))

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.client_s.send(json_data.encode('utf-8'))
    
    def reliable_recv(self):
        received_data = ""
        while True:
            try:
                received_data = received_data + self.client_s.recv(1024).decode('utf-8')
                return json.loads(received_data)
            except ValueError:
                continue
            

    def run(self):
        while True:
            command = input("$~ ")
            self.reliable_send(command)
            if command == 'q':
                break
            print(self.reliable_recv())
        self.client_s.close()


def get_params():
    parser = optparse.OptionParser('Usage: <Program> -t target -p port')
    parser.add_option('-t', '--target', dest='target', type="string", help="Specify IP address of target")
    parser.add_option('-p','--port', dest='port', type='int', help='Specify port')
    options, args = parser.parse_args()
    if options.target is None or options.port is None:
        print(parser.usage)
        sys.exit(0)
    return options.target, options.port

if __name__ == "__main__":
    target, port  = get_params()
    udpclient = UDPClient(target, port)
    udpclient.run()