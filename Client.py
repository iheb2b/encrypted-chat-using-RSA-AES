import pickle
import socket
import threading
import tkinter
from tkinter.constants import RIGHT
import tkinter.scrolledtext
from tkinter import simpledialog
from Crypto.Cipher import AES
import rsa
from datetime import  datetime

host_ip = socket.gethostname()    # My local IP adress
host_port = 5555



class Client:
    def __init__(self,hostIP,port):
        msg=tkinter.Tk()
        msg.withdraw()

        self.nickname= simpledialog.askstring("Nickname", "please choose a nickaname", parent=msg)  # First popup
        (self.public_key,self.private_key)=rsa.newkeys(512) # Will be used for encryption.

        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.connect((hostIP,port))


        self.gui_done = False
        self.running = True

        msg.destroy()

        gui_thread= threading.Thread(target=self.gui_loop)
        receive_thread= threading.Thread(target=self.receive)

        gui_thread.start()
        receive_thread.start()
#gui

    def gui_loop(self):
        self.window=tkinter.Tk()
        self.window.title("Secure Chat ")
        self.window.resizable(width=True, height=False)
        self.window.configure(background = "#202049")
        self.window.wm_iconbitmap("Images/icon.ico")
        self.chat_label = tkinter.Label(self.window,text="Secure chat", font=("Nunito", 30, "bold"),bg="#202049",fg="white")
        self.chat_label.pack(padx=20,pady=5)

        self.text_area=tkinter.scrolledtext.ScrolledText(self.window)
        self.text_area.pack(padx=20,pady=5)
        self.text_area.config(state='disabled') # mynajimch ybadel wlla yfasa5 lmsgtt

        self.input_area = tkinter.Text(self.window,height=3,font=("Nunito", 12, "bold"),background="#16212b",fg="white")
        self.input_area.pack(padx=20,pady=5)

        self.button_img = tkinter.PhotoImage(file="./Images/Button.png")
        self.send_button = tkinter.Button(self.window, text="send", command = self.write, image = self.button_img, highlightthickness = 0, bd = 0,background="#202049",activebackground="#202049")
        self.send_button.pack()



        self.gui_done=True
        self.window.mainloop()

    def write(self):
        if len(self.input_area.get('1.0','end')) > 1 :  # my5alikch tabeeth  empty msg
            message = f"{self.nickname}: {self.input_area.get('1.0','end')}"    # forma mtaa lmsg- "Nickname: text"

            cipher = AES.new(self.symetric_key, AES.MODE_EAX)   # Encrypt the sent message
            nonce = cipher.nonce
            ciphertext, tag = cipher.encrypt_and_digest(message.encode('utf-8'))

            tupled_data = pickle.dumps((ciphertext,nonce,tag))
            self.sock.send(tupled_data)

            self.input_area.delete('1.0','end') # Clears the input field

    def stop(self):
        self.running=False
        self.window.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                message = pickle.loads(self.sock.recv(1024))

                if message == 'NICK':
                    self.sock.send(pickle.dumps(self.nickname))

                elif message == 'PUBLIC KEY':
                    public_key_in_bytes=pickle.dumps(self.public_key) #
                    self.sock.send(public_key_in_bytes)

                    wait_for_symetric_key = True
                    while wait_for_symetric_key:
                        message = self.sock.recv(1024)
                        self.symetric_key = pickle.loads(rsa.decrypt(message,self.private_key)).encode('utf-8')
                        wait_for_symetric_key = False


                elif type(message) is tuple:  # (ciphertext,nonce,tag)

                    cipher = AES.new(self.symetric_key, AES.MODE_EAX, nonce=message[1])
                    plaintext = cipher.decrypt(message[0])
                    try:
                        cipher.verify(message[2])
                    except ValueError:
                        pass
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end',plaintext)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')

            except ConnectionAbortedError:
                break
            except:
                print("Error")
                self.sock.close()
                break

client= Client(host_ip,host_port)