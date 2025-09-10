import base64

def decrypt(encoded):
    encoded_string = f"{encoded}"

    decoded_bytes = base64.b64decode(encoded_string)

    decoded_string = decoded_bytes.decode('utf-8')
    return decoded_string


