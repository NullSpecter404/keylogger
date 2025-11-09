import socket
import keyboard


class GamePlay:

    def __init__(self,HOST,PORT):
        self.HOST = HOST
        self.PORT = PORT
        self.Client = None
    def StartConnection(self):
        try:
            self.Client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.Client.connect((self.HOST,self.PORT))
            while True:
                event = keyboard.read_event()
                if event.event_type == "down":
                    self.Client.sendall((event.name.encode()))
        except ConnectionAbortedError:
            pass
        except ConnectionRefusedError:
            pass
        except Exception as e:
            pass
        finally:
            if self.Client:
                self.Client.close()
            pass

if __name__ == "__main__":
    game = GamePlay("127.0.0.1",1234)
    game.StartConnection()
