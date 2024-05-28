import os
import requests

# Read temperature from file
with open('temperature.txt', 'r') as file:
    temperature = file.read().strip()

# Write temperature to file to be read by C++ program
with open('input_for_cpp.txt', 'w') as file:
    file.write(temperature)

# Run the C++ program
os.system('./process_temperature')

# Read the result from file
with open('output_from_python.txt', 'r') as file:
    result = file.read().strip()

# Send data to the website
url = 'http://example.com/submit'
data = {'result': result}

response = requests.post(url, data=data)

print(response.status_code)
print(response.text)
