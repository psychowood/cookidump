#!/usr/bin/python3

# cookidump
# Original GitHub project:
# https://github.com/auino/cookidump

import os
import io
import re
import time
import json
import pathlib
import argparse
import base64
from getpass import getpass
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.parse import urlparse
from urllib.request import urlretrieve
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains

PAGELOAD_TO = 3
SCROLL_TO = 1
MAX_SCROLL_RETRIES = 5
COOKIES_FILE = 'cookies.json'

def startBrowser(chrome_driver_path, headless = False):
    """Starts browser with predefined parameters"""
    chrome_options = Options()
    if "GOOGLE_CHROME_PATH" in os.environ:
        chrome_options.binary_location = os.getenv('GOOGLE_CHROME_PATH')
    if headless:
        chrome_options.add_argument('--headless')
    chrome_service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return driver

def listToFile(browser, baseDir):
    """Gets html from search list and saves in html file"""
    filename = '{}index.html'.format(baseDir)
    # creating directories, if needed
    path = pathlib.Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    # getting web page source
    #html = browser.page_source
    html = browser.execute_script("return document.documentElement.outerHTML")
    # saving the page
    with io.open(filename, 'w', encoding='utf-8') as f: f.write(html)

def imgToFile(outputdir, recipeID, img_url):
    img_path = '{}images/{}.jpg'.format(outputdir, recipeID)
    path = pathlib.Path(img_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    urlretrieve(img_url, img_path)
    return '../images/{}.jpg'.format(recipeID)

def recipeToFile(browser, filename):
    """Gets html of the recipe and saves in html file"""
    # creating directories, if needed
    path = pathlib.Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    # getting web page source
    html = browser.page_source
    # saving the page
    with io.open(filename, 'w', encoding='utf-8') as f: f.write(html)

def recipeToJSON(browser, recipeID):
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

    recipe = {}
    recipe['id'] = recipeID
    recipe['language'] = soup.select_one('html').attrs['lang']
    recipe['title'] = soup.select_one(".recipe-card__title").text
    recipe['rating_count'] = re.sub(r'\D', '', soup.select_one(".core-rating__label").text, flags=re.IGNORECASE)
    recipe['rating_score'] = soup.select_one(".core-rating__counter").text
    recipe['tm-versions'] = [v.text.replace('\n','').strip().lower() for v in soup.select(".recipe-card__tm-version core-badge")]
    recipe.update({ l.text : l.next_sibling.strip() for l in soup.select("core-feature-icons label span") })
    recipe['ingredients'] = [re.sub(' +', ' ', li.text).replace('\n','').strip() for li in soup.select("#ingredients li")]
    recipe['nutritions'] = {}
    for item in list(zip(soup.select(".nutritions dl")[0].find_all("dt"), soup.select(".nutritions dl")[0].find_all("dd"))):
        dt, dl = item
        recipe['nutritions'].update({ dt.string.replace('\n','').strip().lower(): re.sub(r'\s{2,}', ' ', dl.string.replace('\n','').strip().lower()) })
    recipe['steps'] = [re.sub(' +', ' ', li.text).replace('\n','').strip() for li in soup.select("#preparation-steps li")]
    recipe['tags'] = [a.text.replace('#','').replace('\n','').strip().lower() for a in soup.select(".core-tags-wrapper__tags-container a")]

    return recipe

def recipeToPdf(browser, filename):
    """Gets html of the recipe and saves in pdf file"""
    send_devtools(browser, "Emulation.setEmulatedMedia", {'media': 'screen'})
    printOutput = send_devtools(browser, "Page.printToPDF", {
        "paperWidth": 210 / 25.4,
        "paperHeight": 297 / 25.4,
        "scale": 0.45,
        "displayHeaderFooter": False,
        "printBackground": False,
        "marginTop": 0.1,
        "marginRight": 0.1,
        "marginBottom": 0.1,
        "marginLeft": 0.1
    })
    with open(filename, 'wb') as outfile: 
        outfile.write( base64.b64decode(printOutput['data']))

def send_devtools(driver, cmd, params={}):
  """Send devtools command with params to browser, used to export in pdf"""
  resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
  url = driver.command_executor._url + resource
  body = json.dumps({'cmd': cmd, 'params': params})
  response = driver.command_executor._request('POST', url, body)
  if 'status' in response:
    raise Exception(response.get('value'))
  return response.get('value')

def cleanHtml(browser):

    #remove header and residual margin
    try: removeElements(browser, By.TAG_NAME, 'header')
    except: pass
    try: runActionOnElements(browser, By.CLASS_NAME, 'l-header-offset-small', 'setAttribute("style","margin-top: 0 !important")')
    except: pass
    
    #remove footer
    try: removeElements(browser, By.TAG_NAME, 'core-footer')
    except: pass
    
    #remove alternative recipes
    try: removeElements(browser, By.ID, 'alternative-recipes')
    except: pass
    
    #remove sharing banner
    try: removeElements(browser, By.ID, 'core-share')
    except: pass
    
    #remove common collections
    try: removeElements(browser, By.ID, 'in-collections')
    except: pass
    
    #remove recipe actions (e.g. add to my recipes/my week)
    try: removeElements(browser, By.CLASS_NAME, 'recipe-card__btn-line')
    except: pass
    
    #disable serving size modal
    try: removeClassFromElements(browser, By.ID, 'serving-size-modal-trigger','core-feature-icons__item--large-rectangle')
    except: pass

    #disable serving size modal
    try: removeClassFromElements(browser, By.ID, 'serving-size-modal-trigger','core-feature-icons__item--large-rectangle')
    except: pass
    try: removeClassFromElements(browser, By.CSS_SELECTOR, 'core-feature-icons .core-feature-icons__icon','core-feature-icons__icon')
    except: pass

    #expand tags, remove expand/collapse links and override hrefs
    try: runActionOnElements(browser, By.CSS_SELECTOR, 'core-tags-wrapper .core-tags-wrapper__wrapper', 'setAttribute("style","max-height: 100% !important")')
    except: pass
    try: removeElements(browser,By.CSS_SELECTOR, 'core-tags-wrapper .link--subsequent')
    except: pass
    try: removeElements(browser,By.CSS_SELECTOR, 'core-tags-wrapper .link--subsequent')
    except: pass
    try: runActionOnElements(browser, By.CSS_SELECTOR, 'core-tags-wrapper a', 'href="#";')
    except: pass

    #remove cookie banner and scripts
    try: removeElements(browser, By.ID, '#onetrust-consent-sdk')
    except: pass
    try: removeElements(browser, By.CSS_SELECTOR, 'script[src*="otSDKStub"]')
    except: pass

def removeElements(browser, byQuery, query):
    runActionOnElements(browser, byQuery, query, 'parentNode.removeChild(item);')

def removeClassFromElements(browser, byQuery, query, classToRemove):
    runActionOnElements(browser, byQuery, query, 'classList.remove("'+classToRemove+'")')

def runActionOnElements(browser, byQuery, query, action):
    browser.execute_script("arguments[0].forEach(function(item) {item."+ action + "})", browser.find_elements(byQuery, query))

def isAuthenticated(browser):
    return browser.get_cookie("v-authenticated") is not None

def run(webdriverfile, outputdir, separate_json, searchquery, locale, pdf = False, save_cookies = False, headless = False, login = False):
    """Scraps all recipes and stores them in html"""
    print('[CD] Welcome to cookidump, starting things off...')
    # fixing the outputdir parameter, if needed
    if outputdir[-1:][0] != '/': outputdir += '/'
    
    if locale is None:
        locale = str(input('[CD] Complete the website domain: https://cookidoo.'))
    else:
        print('[CD] Locale argument set, going to https://cookidoo.{}'.format(locale))

    baseURL = 'https://cookidoo.{}/'.format(locale)

    if not save_cookies:
        try: 
            with open(COOKIES_FILE, 'r') as infile: 
                cookies = json.load(infile)
                print('[CD] {} file found and parsed'.format(COOKIES_FILE))
        except FileNotFoundError: 
            if headless and not login:
                print('[CD] Error: {} file not found, please run cookidump with --save-cookies or --login.'.format(COOKIES_FILE))
                exit(-1)
            cookies = None
        except:
            print('[CD] Error: {} file not valid, please check - or delete - it, and run cookidump with --save-cookies again'.format(COOKIES_FILE))
            exit(-1)
    else:
        cookies = None
    
    brw = startBrowser(webdriverfile, headless)

    # try opening the profile url and check if authenticated
    brw.get(baseURL)
    time.sleep(PAGELOAD_TO)

    if (cookies is not None):
        try:
            # inject cookies
            print('[CD] Injecting cookies')
            for cookie in cookies:
                brw.add_cookie(cookie)
        except:
            print('[CD] Error: {} file not valid, please check - or delete - it, and run cookidump with --save-cookies again'.format(COOKIES_FILE))
            exit(-1)

    while (not isAuthenticated(brw)):
        if login:
            # login
            print('[CD] Logging in')
            brw.get(baseURL + 'profile/login')
            time.sleep(PAGELOAD_TO)
            brw.find_element(By.ID, 'email').send_keys(input('[CD] Enter your email: '))
            brw.find_element(By.ID, 'password').send_keys(getpass('[CD] Enter your password: '))
            brw.find_element(By.CSS_SELECTOR, '#login_form_id button').click()
            time.sleep(PAGELOAD_TO)
        else:
           reply = input('[CD] Not authenticated, please login to your account and then enter y to continue: ')

    if save_cookies:
        with open(COOKIES_FILE, 'w') as outfile: json.dump(brw.get_cookies(), outfile)
        print('[CD] Cookies saved to {}, please re-run cookidump without --save-cookies'.format(COOKIES_FILE))
        return

    # clicking on cookie reject
    try: brw.find_element(By.ID, 'onetrust-reject-all-handler').click()
    except: pass

    # recipes base url
    rbURL = 'https://cookidoo.{}'.format(locale)

    if searchquery is None:
        rbURL += '/search'
        brw.get(rbURL)
        time.sleep(PAGELOAD_TO)
        
        # possible filters done here
        reply = input('[CD] Set your filters, if any, and then enter y to continue: ')
        custom_output_dir = input("[CD] enter the directory name to store the results (ex. vegetarian): ")
        if custom_output_dir : outputdir += '{}/'.format(custom_output_dir)
    else:
        rbURL += searchquery
        brw.get(rbURL)
        time.sleep(PAGELOAD_TO)

    print('[CD] Proceeding with scraping page {}'.format(brw.current_url))

    # removing the base href header
    removeElements(brw,By.TAG_NAME, 'base')

    # removing the name
    removeElements(brw, By.TAG_NAME, 'core-transclude')

    # showing all recipes
    elementsToBeFound = int(brw.find_element(By.CLASS_NAME, 'search-results-count__hits').get_attribute('innerHTML'))
    previousElements = 0
    while True:
        # checking if ended or not
        currentElements = len(brw.find_elements(By.CLASS_NAME, 'link--alt'))
        if currentElements >= elementsToBeFound: break
        # scrolling to the end
        brw.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_TO)
        # clicking on the "load more recipes" button
        try:
            brw.find_element(By.ID, 'load-more-page').click()
            time.sleep(PAGELOAD_TO)
        except: pass
        print('Scrolling [{}/{}]'.format(currentElements, elementsToBeFound))
        # checking if I can't load more elements
        count = count + 1 if previousElements == currentElements else 0
        if count >= MAX_SCROLL_RETRIES: break
        previousElements = currentElements

    print('Scrolling [{}/{}]'.format(currentElements, elementsToBeFound))

    # saving all recipes urls
    els = brw.find_elements(By.CLASS_NAME, 'link--alt')
    recipesURLs = []
    for el in els:
        recipeURL = el.get_attribute('href')
        recipesURLs.append(recipeURL)
        recipeID = recipeURL.split('/')[-1:][0]
        brw.execute_script("arguments[0].setAttribute(arguments[1], arguments[2]);", el, 'href', './recipes/{}.html'.format(recipeID))

    # removing search bar
    removeElements(brw, By.TAG_NAME, 'search-bar')

    # removing scripts
    removeElements(brw, By.TAG_NAME, 'script')

    #cleaning html for local saving and printing
    cleanHtml(brw)

    # saving the list to file
    listToFile(brw, outputdir)

    # filter recipe Url list because it contains terms-of-use, privacy, disclaimer links too
    recipesURLs = [l for l in recipesURLs if 'recipe' in l]

    # getting all recipes
    print("Getting all recipes...")
    c = 0
    recipeData = []
    for recipeURL in recipesURLs:
        try:
            # building urls
            u = str(urlparse(recipeURL).path)
            if u[0] == '/': u = '.'+u
            recipeID = u.split('/')[-1:][0]
            # opening recipe url
            brw.get(recipeURL)
            time.sleep(PAGELOAD_TO)
            # removing the base href header
            removeElements(brw,By.TAG_NAME, 'base')
            
            # removing the name
            removeElements(brw,By.TAG_NAME, 'core-transclude')
            
            # changing the top url
            brw.execute_script("arguments[0].setAttribute(arguments[1], arguments[2]);", brw.find_element(By.CLASS_NAME, 'page-header__home'), 'href', '../../index.html')

            # saving recipe image
            img_url = brw.find_element(By.ID, 'recipe-card__image-loader').find_element(By.TAG_NAME, 'img').get_attribute('src')
            local_img_path = imgToFile(outputdir, recipeID, img_url)

            # change the image url to local
            brw.execute_script("arguments[0].setAttribute(arguments[1], arguments[2]);", brw.find_element(By.CLASS_NAME, 'core-tile__image'), 'srcset', '')
            brw.execute_script("arguments[0].setAttribute(arguments[1], arguments[2]);", brw.find_element(By.CLASS_NAME, 'core-tile__image'), 'src', local_img_path)

            #cleaning html for local saving and printing
            cleanHtml(brw)

            # saving the file
            recipeToFile(brw, '{}recipes/{}.html'.format(outputdir, recipeID))

            if pdf:
                # exporting in pdf
                print('[CD] Exporting recipe in PDF file')
                recipeToPdf(brw, '{}recipes/{}.pdf'.format(outputdir, recipeID))

            # extracting JSON info
            recipe = recipeToJSON(brw, recipeID)

            # saving JSON file, if needed
            if separate_json:
                print('[CD] Writing recipe to JSON file')
                with open('{}recipes/{}.json'.format(outputdir, recipeID), 'w') as outfile: json.dump(recipe, outfile)
            else:
                recipeData.append(recipe)
                        
            # printing information
            c += 1
            if c % 10 == 0: print('Dumped recipes: {}/{}'.format(c, len(recipesURLs)))
        except: pass

    # save JSON file, if needed
    if not separate_json:
        print('[CD] Writing recipes to JSON file')
        with open('{}data.json'.format(outputdir), 'w') as outfile: json.dump(recipeData, outfile)

    if cookies is None:
        # logging out
        logoutURL = 'https://cookidoo.{}/profile/logout'.format(locale)
        brw.get(logoutURL)
        time.sleep(PAGELOAD_TO)

    # closing session
    print('[CD] Closing session\n[CD] Goodbye!')
    brw.close()

if  __name__ =='__main__':
    parser = argparse.ArgumentParser(description='Dump Cookidoo recipes from a valid account')
    parser.add_argument('webdriverfile', type=str, help='the path to the Chrome WebDriver file')
    parser.add_argument('outputdir', type=str, help='the output directory. If a search query is specified it will be used directly to save the recipes')
    parser.add_argument('-s', '--separate-json', action='store_true', help='creates a separate JSON file for each recipe; otherwise, a single data file will be generated')
    parser.add_argument('-l', '--locale', type=str, help='sets locale of cookidoo website (end of domain, ex. de, it, etc.))')
    parser.add_argument('--searchquery', type=str, help='the search query to use copied from the site after setting filter, without the domain (e.g. something like "/search/?context=recipes&categories=VrkNavCategory-RPF-013")')
    parser.add_argument('-p', '--pdf', action='store_true', help='saves recipe in pdf format too')
    parser.add_argument('--login', action='store_true', help='interactive login, mostly for headless mode')
    parser.add_argument('--save-cookies', action='store_true', help='store cookies in local {} file then exits; to be used with --headless or to avoid login on subsequent runs'.format(COOKIES_FILE))
    parser.add_argument('--headless', action='store_true', help='runs Chrome in headless mode, needs both a {} saved with --save-cookies previously and --searchquery specified'.format(COOKIES_FILE))
    args = parser.parse_args()

    if (not args.login and args.headless and args.searchquery is None):
        parser.error('--headless requires --searchquery to be specified when run without --login')
        exit(-1)



    run(args.webdriverfile, args.outputdir, args.separate_json, args.searchquery, args.locale, args.pdf, args.save_cookies, args.headless, args.login)
