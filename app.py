from flask import Flask,render_template,jsonify, request, redirect
import numpy as np
from urllib.parse import urlparse
import ipaddress
from flask_cors import CORS
from tensorflow.keras.models import load_model



# app = Flask(__name__, static_url_path='/static')

app = Flask(__name__)



CORS(app)



def load_ml_model():
    # load model 
    model = load_model('malicious_ml.h5')
    return model




def hello(url):
     print("hello world " + url)




def separate_url(url):
    # Parse the URL using urlparse
    parsed_url = urlparse(url)

    # Extract protocol, hostname, and path
    protocol = parsed_url.scheme + "://"
    hostname = parsed_url.netloc
    path = parsed_url.path
    directories = path.strip('/').split('/')
    return protocol, hostname, path, directories

def check_hostname(url):
    # Parse the URL using urlparse
    parsed_url = urlparse(url)

    # Extract the hostname from the parsed URL
    hostname = parsed_url.hostname

    # Check if the hostname is an IP address
    try:
        ipaddress.IPv4Address(hostname)
        # If it's a valid IPv4 address, return -1
        return -1
    except ipaddress.AddressValueError:
        pass

    try:
        ipaddress.IPv6Address(hostname)
        # If it's a valid IPv6 address, return -1
        return -1
    except ipaddress.AddressValueError:
        pass

    # If it's not an IP address, return 1
    return 1



def count_special_characters(url):
    # Define the list of special characters to count
    special_characters = ['-', '@', '?', '%', '.', '=']

    # Initialize counts for each special character
    counts = {char: 0 for char in special_characters}

    # Iterate through the URL and count occurrences of each special character
    for char in url:
        if char in counts:
            counts[char] += 1

    return counts

def count_letters_and_digits(input_string):
    # Initialize counts for letters and digits
    num_letters = sum(char.isalpha() for char in input_string)
    num_digits = sum(char.isdigit() for char in input_string)

    return num_digits, num_letters



@app.route('/', methods=['GET', 'POST'])     
def check():
    return render_template("index.html")

# @app.route('/see/<path:url>')
@app.route('/see', methods=['POST'])
def see():
    data = request.get_json(force=True)
    my_url = data.get('url')
    
    url_data={

        "site": my_url,
        "name": "agrahari"
        }
    
    return jsonify(url_data), 200

   

# @app.route('/check/<path:url>')

@app.route('/check', methods=['POST'])

def check_url():
     
   

         data = request.get_json(force=True)
         my_url = data.get('url')

         print(my_url)
         ff = load_ml_model()
         protocol, hostname, path, directories = separate_url(my_url)
         print("protocol = ", protocol, " hostname = ", hostname)
         special_char_counts = count_special_characters(my_url)
         count_http = 0
         count_https = 0
         count_www = 0
         if "http" in protocol:
            count_http += 1
         if "https" in protocol:
            count_https += 1
         if "www" in hostname:
            count_www += 1
         count_digits, count_letters = count_letters_and_digits(my_url)

         
         url_arr = np.array([len(hostname), len(path), len(directories[0]), 
                            special_char_counts['-'],special_char_counts['@'], 
                            special_char_counts['?'],special_char_counts['%'], 
                            special_char_counts['.'], special_char_counts['='], 
                            count_http, count_https, count_www, count_digits, 
                            count_letters, len(directories), check_hostname(my_url)
                            ])
         url_arr = url_arr.reshape(1, -1)
        
     
         y_predict = ff.predict(url_arr)
        
         if y_predict < 0.5 :
             probability = (1-y_predict[0,0])*100
             result = "Not-Mallicious"
            
              
         else:
            probability = y_predict[0,0]*100
            result = "Mallicious"
         
         url_data={

          "result": result,
          "prob": probability
            }
             
         print(result, " ", probability)
         return jsonify(url_data)



if __name__ == "__main__":
    app.run(debug=True, port= 9000)
