import time
import struct
import numpy as np

# ----------------------------------
# Receive
# ----------------------------------

def recv_timeout(socket, escape_seq, timeout=5):
    """
    Receive data until either an escape sequence
    is found or a timeout is exceeded

    Args:
        socket: The socket used for communication
        escape_seq: String containing the escape sequence. Ex. 'EOF'.
        timeout: Reception timeout in seconds
    """

    # total data partwise in an array
    total_data = [];
    data = '';

    begin = time.time()

    while 1:
        if time.time()-begin > timeout:
            print("Error in recv_timeout Timeout exceeded")
            return "RECV_ERR_TIMEOUT"

        try:
            data = socket.recv(2048).decode('utf-8')

            if data:
                total_data.append(data)
                begin = time.time()

                if data.find(escape_seq) > 0:
                    break
        except:
            pass

        # To avoid the program to freeze at connection sometimes
        time.sleep(0.005)

    return ''.join(total_data)


