import numpy as np
import hashlib
import os
import tkinter as tk
from tkinter import ttk
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# ---------------- BB84 FUNCTIONS ----------------

def generate_bits(n):
    return np.random.randint(2, size=n)

def generate_bases(n):
    return np.random.randint(2, size=n)

def measure(bits, sender_basis, receiver_basis):
    result = []
    for i in range(len(bits)):
        if sender_basis[i] == receiver_basis[i]:
            result.append(bits[i])
        else:
            result.append(np.random.randint(2))
    return np.array(result)

def sift_key(sender_bits, sender_basis, receiver_bits, receiver_basis):
    key_sender = []
    key_receiver = []
    for i in range(len(sender_bits)):
        if sender_basis[i] == receiver_basis[i]:
            key_sender.append(sender_bits[i])
            key_receiver.append(receiver_bits[i])
    return np.array(key_sender), np.array(key_receiver)

def calculate_qber(k1, k2):
    if len(k1) == 0:
        return 1
    errors = np.sum(k1 != k2)
    return errors / len(k1)

# ---------------- AES FUNCTIONS ----------------

def generate_aes_key(qkey):
    key_string = ''.join(map(str, qkey))
    return hashlib.sha256(key_string.encode()).digest()

def encrypt_message(key, message):
    aes = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aes.encrypt(nonce, message.encode(), None)
    return nonce, ciphertext

def decrypt_message(key, nonce, ciphertext):
    aes = AESGCM(key)
    plaintext = aes.decrypt(nonce, ciphertext, None)
    return plaintext.decode()

# ---------------- MAIN APP ----------------

class QuantumApp(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Quantum Secure Communication Simulator (BB84)")
        self.geometry("900x650")

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}

        for F in (InputPage, BB84Page, QBERPage, EncryptionPage, ResultPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show(InputPage)

    def show(self, page):
        frame = self.frames[page]
        frame.tkraise()

# ---------------- INPUT PAGE ----------------

class InputPage(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="INPUT PARAMETERS", font=("Arial",20)).pack(pady=20)

        form = ttk.Frame(self)
        form.pack()

        ttk.Label(form, text="Number of Qubits").grid(row=0,column=0)
        self.qubits = ttk.Entry(form)
        self.qubits.insert(0,"50")
        self.qubits.grid(row=0,column=1)

        ttk.Label(form, text="QBER Threshold").grid(row=1,column=0)
        self.qber = ttk.Entry(form)
        self.qber.insert(0,"0.11")
        self.qber.grid(row=1,column=1)

        ttk.Label(form, text="Message").grid(row=2,column=0)
        self.msg = ttk.Entry(form,width=40)
        self.msg.insert(0,"Hello Quantum World")
        self.msg.grid(row=2,column=1)

        self.eve = tk.BooleanVar()
        ttk.Checkbutton(form,text="Simulate Eve Attack",variable=self.eve).grid(row=3,columnspan=2)

        ttk.Button(self,text="Start BB84 Process",
                   command=self.start).pack(pady=20)

    def start(self):

        n = int(self.qubits.get())
        threshold = float(self.qber.get())
        message = self.msg.get()
        eve = self.eve.get()

        app_data = self.controller.frames

        bb84 = app_data[BB84Page]

        bb84.run_bb84(n,threshold,message,eve)

        self.controller.show(BB84Page)

# ---------------- BB84 PROCESS PAGE ----------------

class BB84Page(tk.Frame):

    def __init__(self,parent,controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self,text="BB84 PROCESS",font=("Arial",20)).pack()

        self.text = tk.Text(self,height=25)
        self.text.pack()

        ttk.Button(self,text="Next → QBER Analysis",
                   command=lambda: controller.show(QBERPage)).pack(pady=10)

    def run_bb84(self,n,threshold,message,eve):

        self.n = n
        self.threshold = threshold
        self.message = message
        self.eve = eve

        self.text.delete("1.0",tk.END)

        self.alice_bits = generate_bits(n)
        self.alice_basis = generate_bases(n)
        self.bob_basis = generate_bases(n)

        self.text.insert(tk.END,"Alice Bits:\n"+str(self.alice_bits)+"\n\n")
        self.text.insert(tk.END,"Alice Bases:\n"+str(self.alice_basis)+"\n\n")
        self.text.insert(tk.END,"Bob Bases:\n"+str(self.bob_basis)+"\n\n")

        if eve:

            eve_basis = generate_bases(n)
            eve_bits = measure(self.alice_bits,self.alice_basis,eve_basis)

            self.bob_bits = measure(eve_bits,eve_basis,self.bob_basis)

            self.text.insert(tk.END,"Eve intercepted photons\n\n")

        else:

            self.bob_bits = measure(self.alice_bits,self.alice_basis,self.bob_basis)

        self.text.insert(tk.END,"Bob Measurement Results:\n"+str(self.bob_bits)+"\n")

        qber_page = self.controller.frames[QBERPage]
        qber_page.set_data(self)

# ---------------- QBER PAGE ----------------

class QBERPage(tk.Frame):

    def __init__(self,parent,controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self,text="KEY SIFTING & QBER ANALYSIS",font=("Arial",20)).pack()

        self.text = tk.Text(self,height=25)
        self.text.pack()

        ttk.Button(self,text="Next → Encryption",
                   command=lambda: controller.show(EncryptionPage)).pack(pady=10)

    def set_data(self,bb84):

        self.text.delete("1.0",tk.END)

        alice_key, bob_key = sift_key(
            bb84.alice_bits,
            bb84.alice_basis,
            bb84.bob_bits,
            bb84.bob_basis
        )

        self.alice_key = alice_key
        self.bob_key = bob_key
        self.threshold = bb84.threshold
        self.message = bb84.message

        qber = calculate_qber(alice_key,bob_key)

        self.qber = qber

        self.text.insert(tk.END,"Alice Final Key:\n"+str(alice_key)+"\n\n")
        self.text.insert(tk.END,"Bob Final Key:\n"+str(bob_key)+"\n\n")

        self.text.insert(tk.END,"QBER = "+str(round(qber,4))+"\n\n")

        if qber > bb84.threshold:
            self.text.insert(tk.END,"⚠ Eavesdropping Detected\n")

        enc_page = self.controller.frames[EncryptionPage]
        enc_page.set_data(self)

# ---------------- ENCRYPTION PAGE ----------------

class EncryptionPage(tk.Frame):

    def __init__(self,parent,controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self,text="AES ENCRYPTION PROCESS",font=("Arial",20)).pack()

        self.text = tk.Text(self,height=25)
        self.text.pack()

        ttk.Button(self,text="Show Final Results",
                   command=lambda: controller.show(ResultPage)).pack(pady=10)

    def set_data(self,data):

        self.text.delete("1.0",tk.END)

        if data.qber > data.threshold:
            self.text.insert(tk.END,"Encryption stopped due to attack")
            return

        aes_key = generate_aes_key(data.alice_key)

        nonce, ciphertext = encrypt_message(aes_key,data.message)

        decrypted = decrypt_message(aes_key,nonce,ciphertext)

        self.cipher = ciphertext
        self.decrypted = decrypted

        self.text.insert(tk.END,"Derived AES Key:\n"+str(aes_key)+"\n\n")
        self.text.insert(tk.END,"Encrypted Message:\n"+str(ciphertext)+"\n\n")
        self.text.insert(tk.END,"Decrypted Message:\n"+decrypted+"\n")

        res = self.controller.frames[ResultPage]
        res.set_data(data,self)

# ---------------- RESULT PAGE ----------------

class ResultPage(tk.Frame):

    def __init__(self,parent,controller):
        super().__init__(parent)

        ttk.Label(self,text="FINAL RESULT",font=("Arial",20)).pack()

        self.text = tk.Text(self,height=25)
        self.text.pack()

    def set_data(self,data,enc):

        self.text.delete("1.0",tk.END)

        self.text.insert(tk.END,"Final Alice Key:\n"+str(data.alice_key)+"\n\n")
        self.text.insert(tk.END,"Final Bob Key:\n"+str(data.bob_key)+"\n\n")
        self.text.insert(tk.END,"QBER: "+str(round(data.qber,4))+"\n\n")

        if data.qber > data.threshold:
            self.text.insert(tk.END,"Communication Aborted\n")
            return

        self.text.insert(tk.END,"Encrypted Message:\n"+str(enc.cipher)+"\n\n")
        self.text.insert(tk.END,"Decrypted Message:\n"+enc.decrypted)

# ---------------- RUN APP ----------------

app = QuantumApp()
app.mainloop()