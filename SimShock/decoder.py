def number_to_letter(number):
    decoded_message = ''
    print("Decoding explanation:")
    for i in range(0, len(number), 2):
        num = int(number[i:i+2])
        letter = chr((num - 1) % 26 + ord('a'))
        decoded_message += letter
        print(f"Digits {number[i:i+2]} converted to '{letter}'")
    return decoded_message

def shift_letters(message, shift):
    shifted_message = ''
    for char in message:
        if char.isalpha():
            shifted_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            shifted_message += shifted_char
        else:
            shifted_message += char
    return shifted_message

user_input = input("Enter a number of any length: ")

# Adjust the input if it does not have an even number of digits
if len(user_input) % 2 != 0:
    user_input = user_input[:-1]

# Proceed only if the input is numeric
if user_input.isdigit():
    decoded_message = number_to_letter(user_input)
    print("The decoded message is:", decoded_message)
    print("Shifted versions:")
    for i in range(1, 27):
        shifted_message = shift_letters(decoded_message, i)
        print(f"Shift {i}: {shifted_message}")
else:
    print("Please enter a valid numeric value.")
