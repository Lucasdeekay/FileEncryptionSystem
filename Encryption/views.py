from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from django.views import View


class EncryptView(View):
    template_name = "home.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        input_file = request.FILES.get("file")
        key = b'ThisIsASecretKey'

        filename = str(input_file).split(".")[0]

        chunk_size = 64 * 1024  # 64KB

        # Generate a random initialization vector (IV)
        iv = get_random_bytes(16)

        # Create the AES cipher object with the provided key and mode
        cipher = AES.new(key, AES.MODE_CBC, iv)

        # Read the input file in chunks and encrypt each chunk
        encrypted_chunks = []
        while True:
            chunk = input_file.read(chunk_size)
            if len(chunk) == 0:
                break
            elif len(chunk) % 16 != 0:
                # Pad the last chunk if its length is not a multiple of 16
                chunk = pad(chunk, 16)

            # Encrypt the chunk and store it in a list
            encrypted_chunk = cipher.encrypt(chunk)
            encrypted_chunks.append(encrypted_chunk)

        # Create a downloadable file containing the encrypted data
        response = HttpResponse(content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{filename}.bin"'

        # Write the IV to the response
        response.write(iv)

        # Write the encrypted chunks to the response
        for chunk in encrypted_chunks:
            response.write(chunk)

        return response


def decrypt_file(request):
    input_file = request.FILES.get("file")
    key = b'ThisIsASecretKey'

    filename = str(input_file).split(".")[0]

    chunk_size = 64 * 1024  # 64KB

    # Read the initialization vector (IV) from the first 16 bytes
    iv = input_file.read(16)

    # Create the AES cipher object with the provided key, mode, and IV
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Read the encrypted data and decrypt it in chunks
    decrypted_chunks = []
    while True:
        chunk = input_file.read(chunk_size)
        if len(chunk) == 0:
            break

        # Decrypt the chunk and store it in a list
        decrypted_chunk = cipher.decrypt(chunk)
        decrypted_chunks.append(decrypted_chunk)

    # Unpad the last decrypted chunk
    plaintext = unpad(b''.join(decrypted_chunks), 16)

    # Create a downloadable file containing the decrypted data
    response = HttpResponse(plaintext, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="{filename}.txt"'
    return response
