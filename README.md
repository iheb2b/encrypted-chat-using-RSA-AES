# encrypted-chat-using-RSA-AES
based on rsa/aes encryption , a chat app in pyhton with gui that support socket communication to share encrypted messages between multipule clients 
-----
SUMMERY

A secure chat application that uses RSA encryption for message encryption, communicates via sockets and authenticates users through an LDAP server with certificate based authentication that combines the security of RSA encryption and certificate-based authentication with the convenience of a chat application that uses sockets for fast and efficient communication.

In this application, each user generates a pair of RSA keys, a public key and a private key, using a key generation algorithm. The public key is then made available to other users, while the private key is kept secret.

When a user wants to send an encrypted message to another user, they use the recipient's public key to encrypt the message. The recipient can then use their private key to decrypt the message. This ensures that the message remains confidential, as only the intended recipient will be able to decrypt and read the message.

The application uses sockets to transmit the messages between users. Sockets are a low-level network programming interface that allows applications to send and receive data over a network. By using sockets, the application can transmit the encrypted messages over the network in a fast and efficient manner.

For authentication, the application verifies the user's identity by checking the certificate issued by a trusted certificate authority. The certificate contains information about the user's identity and is verified by the LDAP server. This ensures that only authorized users can access the chat application.
---------
encrytion preccess :
![Diagramme sans nom drawio](https://user-images.githubusercontent.com/61081690/212868983-4e447d83-5a79-4938-a592-776844d28822.png)
•	Using the login/regestration page the client can sign in or register by entreing his
details, a password complexty cheker is imlemented alonge side with an email
verrificatin method.
•	If the client is able to authentificate, the chat server send a request for a nickname
and a public key is generated .
•	The client send back his nickname to the server that store it and promt a message to
all active user that « client-name » have joined the chat.
•	The server then send the symetric session encryption key after it has been encrypted
by the client’s public key.
•	The client recieves the message and decrypt it using his private key.
•	From this point, both the client and the server share the same session key, which
they use to communicate.

•	Using wireshark to capture and analyse the trafic bettween the two clients and the server :
We run this simulation locally in the same machine that's why the source and the destination ipv4 address is 127.0.0.1(loopback address) :

we send a message « is this safe ? » from one client to another :


 
![encrytion](https://user-images.githubusercontent.com/61081690/212870277-9d77a9aa-83d4-4a83-95ca-19a1b09653a4.png)


