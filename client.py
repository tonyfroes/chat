from config import *

root = Tk()
root.withdraw()

#Inicia o socket do cliente
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)

#Função que aguarda o recebimento de novas mensagens
def Receive(canvas, chatBox):
    global CONNECT
    while CONNECT:
        mensagem = client.recv(1024).decode(FORMAT)
        if mensagem:
            print(mensagem)
            frame = Frame(chatBox)
            frame.pack(side="top", fill=X)
            label = Label(frame, text=mensagem, justify='left', wraplength=490)
            label.pack(side='left')
            canvas.update_idletasks()
            canvas.config(scrollregion=(0,0,0,chatBox.winfo_height()))

#Função que envia mensagens para o servidor
def Send(msg):
    message = msg.encode(FORMAT)
    msgLength = len(message)
    sendLength = str(msgLength).encode(FORMAT)
    sendLength += b' ' * (HEADER - len(sendLength))
    client.send(sendLength)
    client.send(message)

#Função que realiza o login do usuário, e abre a tela do chat
def Login():
    global NAME, chatBox, box, scroll
    NAME = username.get()
    if NAME:
        Send(username.get())
    else:
        NAME = 'usuario' + str(randint(0, 10000))
        Send(NAME)
    loginScreen.destroy()
    box = Toplevel()
    box.title("Chat")
    canvas = Canvas(box, width=600, height=600)
    box.configure(width=600, height = 600)
    chatBox = Frame(canvas, bg='blue')
    scroll = Scrollbar(canvas, orient='vertical', command=canvas.yview)
    canvas.config(yscrollcommand=scroll.set)

    canvas.pack(expand=TRUE)
    canvas.pack_propagate(0)
    canvas.create_window(0, 0, window=chatBox, anchor=NW)

    scroll.pack(side=RIGHT, fill=Y, expand=FALSE)

    userArea = Frame(box, width=300, height=30)
    userArea.pack()

    textMessage = Entry(userArea, width=80)
    textMessage.grid(row=0, column=0)
    textMessage.grid_columnconfigure(0, weight=3)

    sendButton = Button(userArea, command= lambda: Send(textMessage.get()), width=10, text='Enviar')
    sendButton.grid(row=0, column=1)
    sendButton.grid_columnconfigure(1, weight=1)

    thread = threading.Thread(target=Receive, args=(canvas,chatBox))   #Inicia a thread que aguarda o recebimento de mensagens
    thread.start()
    box.protocol('WM_DELETE_WINDOW', Close)

#função que desconecta o usuário do servidor quando ele fechar a janela
def Close():
    global CONNECT, NAME
    if messagebox.askokcancel('Sair', 'Você deseja sair do chat?'):
        CONNECT = False
        if NAME:
            Send(DISCONNECT_MESSAGE)
        #box.destroy()
        root.destroy()

def sair(loginScreen):
    global NAME, CONNECT
    CONNECT = False
    Send(DISCONNECT_MESSAGE)
    loginScreen.destroy()
    root.destroy()

def github():
    webbrowser.open_new(r"https://github.com/tonyfroes")

#login
loginScreen = Toplevel()
loginScreen.title('Login')
loginScreen.resizable(False, False)
loginScreen.configure(width=400, height=300, background='#00bfff')

nome = Label(loginScreen, text='Chat', font=('Arial', '20'), bg='#f2f2f2')
nome.place(relheight=0.1, relwidth=0.5, relx=0.25, rely=0.1)

ladodonome = Label(loginScreen, text='Nome: ', font=('Arial', '20'), bg='#f2f2f2')
ladodonome.place(relheight=0.1, relwidth=0.2, relx=0.1, rely=0.3)

username = Entry(loginScreen, font=('Arial', '15'), bg='#f2f2f2')
username.place(relheight=0.1, relwidth=0.6, relx=0.3, rely=0.3)

copyright = Button(loginScreen, text='Desenvolvido por Tony Froes', font=('Arial', '10'), command = github, bg='#f2f2f2')
copyright.place(relheight=0.1, relwidth=0.5, relx=0.25, rely=0.9)

loginButton = Button(loginScreen, text='Fazer Login',font=("Arial", 15), command=Login, bg='#f2f2f2')
loginButton.place(relheight=0.1, relwidth=0.3, relx=0.35, rely=0.5)

#exit button loginscreen
exitButton = Button(loginScreen, text='Sair', command=lambda: sair(loginScreen), font=('Arial', '15'), bg='#f2f2f2')
exitButton.place(relheight=0.1, relwidth=0.3, relx=0.35, rely=0.6)

loginScreen.protocol('WM_DELETE_WINDOW', Close)
root.mainloop()