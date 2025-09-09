import json
class RetrievingFiles:
    def __init__(self):
        pass

    def content_in_binary_form(self, path):
        path = path
        try:
            with open(path, 'rb') as f:
                binary_data = f.read()

            # with open(rf'C:\Users\User\ניסיון\name.wav', 'wb') as f_out:
            #     f_out.write(binary_data)


        except FileNotFoundError:
            return f"Error: Source binary file '{path}' not found."
        except Exception as e:
            return e

        return binary_data


