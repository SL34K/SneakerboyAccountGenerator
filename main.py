#.------..------..------..------..------.
#|S.--. ||L.--. ||3.--. ||4.--. ||K.--. |
#| :/\: || :/\: || :(): || :/\: || :/\: |
#| :\/: || (__) || ()() || :\/: || :\/: |
#| '--'S|| '--'L|| '--'3|| '--'4|| '--'K|
#`------'`------'`------'`------'`------'
#https://twitter.com/SL34K
#https://github.com/SL34K
#00110001 00110011
#00110000 00110011
#00110001 00111000 
#########################################
import requests, bs4, time, names, random, string, configparser
from bs4 import BeautifulSoup
from random import *
localstore = ['Sneakerboy Melbourne','Sneakerboy Chadstone','Sneakerboy Sydney','Sneakerboy Pacific Fair','Sneakerboy DSX','Sneakerboy X','Website']
x=0
def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)
def solution(apikey,sitekey,form):
    print("Getting captcha solution")
    url="http://2captcha.com/in.php?key={}&method=userrecaptcha&googlekey={}&pageurl={}".format(apikey,sitekey,form)
    resp = requests.get(url) 
    if resp.text[0:2] != 'OK':
        quit('Error. Captcha is not received')
    captcha_id = resp.text[3:]
    fetch_url = "http://2captcha.com/res.php?key={}&action=get&id={}".format(apikey,captcha_id)
    for i in range(1, 20):	
        time.sleep(5) # wait 5 sec.
        resp = requests.get(fetch_url)
        if resp.text[0:2] == 'OK':
                break
    captchasolution = resp.text[3:]
    return captchasolution
def account(form,apikey,sitekey,catchalldomain):
    numbers = getrandbits(10)
    first = names.get_first_name()
    last = names.get_last_name()
    randomletters = "".join(choice(string.ascii_letters) for x in range(randint(1, 4)))
    username = randomletters+first+randomletters+(str(numbers))
    email = username+'@'+catchalldomain
    phone = '+61'+(str(random_with_N_digits(8)))
    capsolution = solution(apikey,sitekey,form)
    data = {
        'cid':'',
        'a': 'joinsubmit',
        'name': first,
        'surname': last,
        'email': email,
        'mobilephonecountrycode': 'AU',
        'mobilephone': phone,
        'password': username,
        'confirmpassword': username,
        'postcode': str(random_with_N_digits(4)),
        'country': 'Australia',
        'emailupdates': 'No',
        'smsupdates': 'No',
        'currency': 'AUD',
        'gender': 'male',
        'localstore': choice(localstore),
        'g-recaptcha-response':capsolution,}
    sesh = requests.session()
    sesh.headers = {
        'Origin':'https://sneakerboy.com',
        'Referer':'https://sneakerboy.com',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
    }
    sesh.headers.update()
    signup = sesh.post(form,data=data)
    if signup.status_code == 200:
        return email,username
    else:
        return 'Error'
def main():
    global x
    print("Sneakerboy Account Generator 1.0")
    print("Coded by @SL34K")
    con = configparser.ConfigParser()
    con.read('config.ini')
    form = con.get('Config', 'form')
    apikey = con.get('Config', '2capkey')
    sitekey = con.get('Config', 'sitekey')
    catchalldomain = con.get('Config', 'catchalldomain')
    try:
        signups = int(input ("How many accounts do you want to make?"))
    except:
        print("Enter a whole number")
    while signups > x:
        try:
            email,username = account(form,apikey,sitekey,catchalldomain)
            file = open('accounts.txt', 'a')
            file.write(email+':'+username+'\n')
            file.close()
            print("Signed up successfully")
            x=+1
        except:
            print("Error signing up")
            time.sleep(5)
    else:
        print("{} Accounts signed up".format(x))
main()
