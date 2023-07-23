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

#### nix (not supported by this fork) ####

```
nix run github:auino/cookidump -- <outputdir> [--separate-json]
```

Nix provisions `google-chrome` together with `chromedriver`. Only 
`<outputdir>` and `[--separate-json]` arguments are expected.

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

### Usage ###

Simply run the following command to start the program interactively, to simplify it's usage:

```
python cookidump.py webdriverfile outputdir
```

where the options are:
* `webdriverfile` identifies the path to the downloaded [Chrome WebDriver](https://sites.google.com/chromium.org/driver/) (for instance, `chromedriver.exe` for Windows hosts, `./chromedriver` for Linux and macOS hosts)
* `outputdir` identifies the path of the output directory (will be created, if not already existent)
* `-s` or `--separate-json` creates a separate JSON file for each recipe; otherwise, a single data file will be generated
* `-l LOCALE` or `--locale LOCALE` preselects the locale for cookidoo website (end of domain, ex. de, it, etc.))
* `-k` or `--keep-data` persists chrome data and cookies between runs, creates a local chrome-data directory and avoid logging in for each separate run
* `--searchquery SEARCHQUERY` specifies the search query to use, copied from the site after setting filter(e.g. something like "/search/?context=recipes&categories=VrkNavCategory-RPF-013")
* `-p` or `--pdf` saves recipe in pdf format, together with json and html
* `--save-cookies` store cookies in local cookies.json file then exits; to be used with --headless or to avoid login on subsequent runs
* `--headless` runs Chrome in headless mode, needs both a cookies.json saved with --save-cookies previously and --searchquery specified
* `-h` prints the complete set of options:

```
usage: cookidump.py [-h] [-s] [-l LOCALE] [-k] [--searchquery SEARCHQUERY] [-p] [--save-cookies | --headless] webdriverfile outputdir

Dump Cookidoo recipes from a valid account

positional arguments:
  webdriverfile         the path to the Chrome WebDriver file
  outputdir             the output directory. If a search query is specified it will be used directly to save the recipes

options:
  -h, --help            show this help message and exit
  -s, --separate-json   creates a separate JSON file for each recipe; otherwise, a single data file will be generated
  -l LOCALE, --locale LOCALE
                        sets locale of cookidoo website (end of domain, ex. de, it, etc.))
  -k, --keep-data       persists chrome data and cookies between runs, creates a local chrome-data directory
  --searchquery SEARCHQUERY
                        the search query to use copied from the site after setting filter, without the domain (e.g. something like
                        "/search/?context=recipes&categories=VrkNavCategory-RPF-013")
  -p, --pdf             saves recipe in pdf format too
  --save-cookies        store cookies in local cookies.json file then exits; to be used with --headless or to avoid login on subsequent runs
  --headless            runs Chrome in headless mode, needs both a cookies.json saved with --save-cookies previously and --searchquery
                        specified
  ```

The program will open a [Google Chrome](https://chrome.google.com) window - or headless - and wait until you are logged in into your [Cookidoo](https://cookidoo.co.uk) account if needed, (different countries are supported, either interactively or using the --locale/-l option).

After that, follow intructions provided by the script itself to proceed with the dump.

### Advanced usage ###

By using the various options you can automate everything. Using a shell script to iterate to queries of interest you can dump whatever you want without interacting besides the first login:

```

$ python ./cookidump.py -l it -p ./chromedriver.i386 ./recipes/test --save-cookies
[CD] Welcome to cookidump, starting things off...
[CD] Locale argument set, going to https://cookidoo.it
[CD] Not authenticated, please login to your account and then enter y to continue: y
[CD] Cookies saved to cookies.json, please re-run cookidump without --save-cookies

$ python ./cookidump.py -l it --pdf --headless --searchquery '/search/it-IT?context=recipes&countries=it&accessories=includingFriend,includingBladeCover,includingBladeCoverWithPeeler,includingCutter&query=bun&categories=VrkNavCategory-RPF-013' -s ./chromedriver.i386 ./recipes/mysearch
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

$ ls -lR recipes/mysearch
total 136
drwxr-xr-x  3 user  staff     96 Jul 23 19:55 images
-rw-r--r--  1 user  staff  67083 Jul 23 19:55 index.html
drwxr-xr-x  5 user  staff    160 Jul 23 19:55 recipes

recipes/mysearch/images:
total 96
-rw-r--r--  1 user  staff  45152 Jul 23 19:55 r660642.jpg

recipes/mysearch/recipes:
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
* Set up a dedicated container for the program -> needs to handle user and password via CLI if the end user is not smart enough to manually dump cookies

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
