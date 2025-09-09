import base64

encoded_string = "R2Vub2NpZGUsV2FyIENyaW1lcyxBcGFydGhlaWQsTWFzc2FjcmUsTmFrYmEsRGlzcGxhY2VtZW50LEh1bWFuaXRhcmlhbiBDcmlzaXMsQmxvY2thZGUsT2NjdXBhdGlvbixSZWZ1Z2VlcyxJQ0MsQkRT"
# Encode the Base64 string to bytes
encoded_bytes = encoded_string.encode('utf-8')

# Decode the Base64 bytes
decoded_bytes = base64.b64decode(encoded_bytes)

# Convert the decoded bytes back to a string
decoded_string = decoded_bytes.decode('utf-8')

print(f"Encoded string: {encoded_string}")
print(f"Decoded string: {decoded_string}")