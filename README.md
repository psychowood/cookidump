# cookidump

Easily dump cookidoo recipes from the official website

### Description ###

This program allows you to dump all recipes on [Cookidoo](https://cookidoo.co.uk) websites (available for different countries) for offline and posticipate reading.
Those recipes are valid in particular for [Thermomix/Bimby](https://en.wikipedia.org/wiki/Thermomix) devices.
In order to dump the recipes, a valid subscription (or a trial one) is needed.

The initial concept of this program was based on [jakubszalaty/cookidoo-parser](https://github.com/jakubszalaty/cookidoo-parser).

### Mentioning ###

If you intend to scientifically investigate or extend cookidump, please consider citing the following paper.

```
@article{cambiaso2022cookidump,
title = {Web security and data dumping: The Cookidump case},
journal = {Software Impacts},
volume = {14},
pages = {100426},
year = {2022},
issn = {2665-9638},
doi = {https://doi.org/10.1016/j.simpa.2022.100426},
url = {https://www.sciencedirect.com/science/article/pii/S2665963822001105},
author = {Enrico Cambiaso and Maurizio Aiello},
keywords = {Cyber-security, Data dump, Database security, Browser automation},
abstract = {In the web security field, data dumping activities are often related to a malicious exploitation. In this paper, we focus on data dumping activities executed legitimately by scraping/storing data shown on the browser. We evaluate such operation by proposing Cookidump, a tool able to dump all recipes available on the Cookidoo© website portal. While such scenario is not relevant, in terms of security and privacy, we discuss the impact of such kind of activity for other scenarios including web applications hosting sensitive information.}
}
```

Further information can be found at [https://www.sciencedirect.com/science/article/pii/S2665963822001105](https://www.sciencedirect.com/science/article/pii/S2665963822001105).

### Features ###

* Easy to run
* Easy to open HTML output
* Output including a surfable list of dumped recipes
* Customizable searches
* Additional json and pdf output

### Installation ###

#### manual ####

1. Clone the repository:

```
git clone https://github.com/auino/cookidump.git
```

2. `cd` into the download folder

3. Install [Python](https://www.python.org) requirements:

```
pip install -r requirements.txt
```

4. Install the [Google Chrome](https://chrome.google.com) browser, if not already installed. In MacOs you can also just copy the Chrome app in the cookidump folder

5. Download the [Chrome WebDriver](https://sites.google.com/chromium.org/driver/) and save it on the `cookidump` folder

6. You are ready to dump your recipes

#### nix (not supported by this fork) ####

```
nix run github:auino/cookidump -- <outputdir> [--separate-json]
```

Nix provisions `google-chrome` together with `chromedriver`. Only 
`<outputdir>` and `[--separate-json]` arguments are expected.

### Usage ###

Simply run the following command to start the program interactively, to simplify it's usage:

```
python cookidump.py webdriverfile outputdir
```

where the options are:
* `webdriverfile` identifies the path to the downloaded [Chrome WebDriver](https://sites.google.com/chromium.org/driver/) (for instance, `chromedriver.exe` for Windows hosts, `./chromedriver` for Linux and macOS hosts). Defaults to `chromedriver`, can be set via `CD_WEBDRIVER` env variable
* `outputdir` identifies the path of the output directory (will be created, if not already existent). Defaults to `recipes`, can be set via `CD_OUTPUTDIR` env variable
* `-o` or `--subdir` saves recipes inside outputdir in a specified subdirectory, useful for categoryzing. No default value, can be set via `CD_SUBDIR` env variable
* `-s` or `--separate-json` creates a separate JSON file for each recipe; otherwise, a single data file will be generated. Defaults to `false`, can be set via `CD_SEPARATE_JSON` env variable
* `-l LOCALE` or `--locale LOCALE` preselects the locale for cookidoo website (end of domain, ex. de, it, etc.)). No default value, can be set via `CD_LOCALE` env variable 
* `-p` or `--pdf` saves recipe in pdf format, together with json and html. Defaults to `false`, can be set via `CD_PDF` env variable
* `-q` or `--searchquery SEARCHQUERY` specifies the search query to use, copied from the site after setting filter(e.g. something like "/search/?context=recipes&categories=VrkNavCategory-RPF-013")
* `--headless` runs Chrome in headless mode, needs --searchquery specified and either --login or a cookies.json saved with --save-cookies previously. Defaults to `false`, can be set via `CD_HEADLESS` env variable
* `--login` interactive login, mostly for headless mode
* `--save-cookies` store cookies in local cookies.json file then exits; to be used with --headless or to avoid login on subsequent runs

* `-h` prints the complete set of options:

```
usage: cookidump.py [-h] [-s] [-l LOCALE] [-p] [--searchquery SEARCHQUERY] [--headless] [--login] [--save-cookies] [webdriverfile] [outputdir]

Dump Cookidoo recipes from a valid account

positional arguments:
  webdriverfile         the path to the Chrome WebDriver file. Default: 'chromedriver', Env var: CD_WEBDRIVER
  outputdir             the output directory, if a search query is specified it will be used directly to save the recipes. Default:
                        'recipes', Env var: CD_OUTPUTDIR

options:
  -h, --help            show this help message and exit
  -o SUBDIR, --subdir SUBDIR
                        saves recipes inside outputdir in a specified subdirectory, useful for categoryzing. No default - it will be asked -,
                        Env var: CD_SUBDIR
  -s, --separate-json   creates a separate JSON file for each recipe; otherwise, a single data file will be generated. Default: 'False', Env
                        var: CD_SEPARATE_JSON
  -l LOCALE, --locale LOCALE
                        sets locale of cookidoo website (end of domain, ex. de, it, etc.)). No default, Env var: CD_LOCALE
  -p, --pdf             saves recipe in pdf format too. Default: 'False', Env var: CD_PDF
  -q SEARCHQUERY, --searchquery SEARCHQUERY
                        the search query to use copied from the site after setting filter, without the domain (e.g. something like
                        "/search/?context=recipes&categories=VrkNavCategory-RPF-013")
  --headless            runs Chrome in headless mode, needs --searchquery specified and either --login or a cookies.json saved with --save-
                        cookies previously. Default: 'False', Env var: CD_HEADLESS
  --login               interactive terminal login
  --save-cookies        store cookies in local cookies.json file then exits; to be used with --headless or to avoid login on subsequent runs
```

The program will open a [Google Chrome](https://chrome.google.com) window - or headless - and wait until you are logged in into your [Cookidoo](https://cookidoo.co.uk) account if needed, (different countries are supported, either interactively or using the --locale/-l option).

After that, follow intructions provided by the script itself to proceed with the dump.

### Advanced usage ###

By using the various options you can automate everything. Using a shell script to iterate to queries of interest you can dump whatever you want without interacting besides the first login:

```
export CD_LOCALE='it'
$ python ./cookidump.py -p --save-cookies --login --headless
[CD] Starting cookidump with arguments:
[CD]    webdriverfile = chromedriver
[CD]    outputdir = recipes
[CD]    subdir = None
[CD]    separate_json = False
[CD]    locale = it
[CD]    pdf = True
[CD]    searchquery = None
[CD]    headless = True
[CD]    login = True
[CD]    save_cookies = True
[CD] Welcome to cookidump, starting things off...
[CD] Locale argument set, going to https://cookidoo.it
[CD] Logging in
[CD] Enter your email: xxxx
[CD] Enter your password: 
[CD] Cookies saved to cookies.json, please re-run cookidump without --save-cookies


export CD_SEPARATE_JSON=True
$ python ./cookidump.py --pdf --headless --searchquery '/search/it-IT?context=recipes&countries=it&accessories=includingFriend,includingBladeCover,includingBladeCoverWithPeeler,includingCutter&query=bun&categories=VrkNavCategory-RPF-013' -o test
[CD] Starting cookidump with arguments:
[CD]    webdriverfile = chromedriver
[CD]    outputdir = recipes
[CD]    subdir = test
[CD]    separate_json = True
[CD]    locale = it
[CD]    pdf = True
[CD]    searchquery = /search/it-IT?context=recipes&countries=it&accessories=includingFriend,includingBladeCover,includingBladeCoverWithPeeler,includingCutter&query=bun&categories=VrkNavCategory-RPF-013
[CD]    headless = True
[CD]    login = False
[CD]    save_cookies = False
[CD] Welcome to cookidump, starting things off...
[CD] Locale argument set, going to https://cookidoo.it
[CD] cookies.json file found and parsed
[CD] Injecting cookies
[CD] Proceeding with scraping page https://cookidoo.it/search/it-IT?context=recipes&countries=it&accessories=includingFriend,includingBladeCover,includingBladeCoverWithPeeler,includingCutter&query=bun&categories=VrkNavCategory-RPF-013
Scrolling [8/1]
Getting all recipes...
[CD] Exporting recipe in PDF file
[CD] Writing recipe to JSON file
[CD] Closing session
[CD] Goodbye!

$ ls -lR recipes/test
total 136
drwxr-xr-x  3 user  staff     96 Jul 23 19:55 images
-rw-r--r--  1 user  staff  67083 Jul 23 19:55 index.html
drwxr-xr-x  5 user  staff    160 Jul 23 19:55 recipes

recipes/test/images:
total 96
-rw-r--r--  1 user  staff  45152 Jul 23 19:55 r660642.jpg

recipes/test/recipes:
total 528
-rw-r--r--  1 user  staff   68960 Jul 23 19:55 r660642.html
-rw-r--r--  1 user  staff    2865 Jul 23 19:55 r660642.json
-rw-r--r--  1 user  staff  192693 Jul 23 19:55 r660642.pdf
```


#### Considerations ####

By following script instructions, it is also possible to apply custom filters to export selected recipes (for instance, in base of the dish, title and ingredients, Thermomix/Bimby version, etc.).

Output is represented by an `index.html` file, included in `outputdir`, plus a set of recipes inside of structured folders.
By opening the generated `index.html` file on your browser, it is possible to have a list of recipes downloaded and surf to the desired recipe.

The number of exported recipes is limited to around `1000` for each execution.
Hence, use of filters may help in this case to reduce the number of recipes exported.

### Other approaches ###

A different approach, previously adopted, is based on the retrieval of structured data on recipes.
More information can be found on the [datastructure branch](https://github.com/auino/cookidump/tree/datastructure).
Output is represented in this case in a different (structured) format, hence, it has to be interpreted. Such interpretation is not implemented in the linked previous commit.

### TODO ###

* Bypass the limited number of exported recipes -> not really feasible automatically, the remote API limits to 1000 records. Can be bypassed by running multiple times with different search queries but needs quite a bit of smartness on the algorithm and would need merge of lists in the main html file to be browseable
* Parse downloaded recipes to store them on a database, or to generate a unique linked PDF
* Set up a dedicated container for the program

### Supporters ###

* [@vikramsoni2](https://github.com/vikramsoni2), regarding JSON saves plus minor enhancements
* [@mrwogu](https://github.com/mrwogu), regarding additional information to be extracted on the generated JSON file, plus suggestions on the possibility to save recipes on dedicated JSON files
* [@nilskrause](https://github.com/NilsKrause), regarding argument parsing and updates on the link to download the Chrome WebDriver
* [@NightProgramming](https://github.com/NightProgramming), regarding the use of selenium version 3
* [@morela](https://github.com/morela), regarding the update of the tool to support a newer version of Selenium
* [@ndjc](https://github.com/ndjc), fixing some deprecation warnings

### Disclaimer ###

The authors of this program are not responsible of the usage of it.
This program is released only for research and dissemination purposes.
Also, the program provides users the ability to locally and temporarily store recipes accessible through a legit subscription.
Before using this program, check Cookidoo subscription terms of service, according to the country related to the exploited subscription. 
Sharing of the obtained recipes is not a legit activity and the authors of this program are not responsible of any illecit and sharing activity accomplished by the users.

### Contacts ###

You can find me on Twitter as [@auino](https://twitter.com/auino).
