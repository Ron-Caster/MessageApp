import socket

# Get the IP address of the smartphone
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address

# Get an available port
def get_available_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 0))
    port = sock.getsockname()[1]
    sock.close()
    return port

# Sender's IP and port
sender_ip = get_ip_address()
sender_port = get_available_port()

# Receiver's IP and port
receiver_ip = 'FRIENDS_IP_ADDRESS'  # Replace with your friend's IP address
receiver_port = 12345

# Create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the sender's IP and port
sock.bind((sender_ip, sender_port))

while True:
    # Get the message from the user
    message = input("Enter your message: ")

    # Send the message to the receiver
    sock.sendto(message.encode(), (receiver_ip, receiver_port))

    # Receive the response from the receiver
    data, addr = sock.recvfrom(1024)
    print("Received response:", data.decode())

# Close the socket
sock.close()
