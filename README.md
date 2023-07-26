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
git clone https://github.com/psychowood/cookidump/
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

#### Docker ####

You can use docker to run cookidump, if you prefer to segregate the dependencies. Being a command line tool and not a running service (not talking here - yet - about setting up an API to expose it, sorry :) ), manual interaction over the CLI is expected anyway.

Docker work is largely inspired by [Zenika's alpine-chrome project](https://github.com/Zenika/alpine-chrome/) and uses [@jessfraz's seccomp chrome template](https://github.com/jessfraz/dotfiles/blob/master/etc/docker/seccomp/chrome.json) which was copied inside the repo, and will be probably customized/reduce for the minimum needs in future.

Since I'm lazy and forgetful, I prefer to set up everything in compose, so the instructions here are docker-compose based.


1. Clone the repo and enter the directory:
   `git clone https://github.com/psychowood/cookidump/ && cd cookidump/`
2. Build the cookidump image passing current user UID and GID:
   `docker-compose build --build-arg DOCKER_UID="$(id -u)" --build-arg DOCKER_GID="$(id -g)"`
   that will result in 
   `Successfully tagged cookidump_build:latest`
3. You can now edit the `docker-compose.yml` if you want to customize the settings, using the environment variables:
```yaml
    environment:
      - CD_WEBDRIVER=chromedriver
      - CD_OUTPUTDIR=recipes
    # - CD_SUBDIR=subdir
      - CD_LOCALE=it
      - CD_SEPARATE_JSON=True
      - CD_PDF=True
      - CD_HEADLESS=True # Don't remove this variable or cookidump won't run inside docker
```
4. Setup cookies and login:
   `docker-compose run --rm cookidump ./run.sh --save-cookies --login`
   then enter email and password, and you should get 
   `[CD] Cookies saved to cookies.json, please re-run cookidump without --save-cookies`
5. Try your first scrape command:
   `docker-compose run --rm cookidump ./run.sh  -o test --searchquery '/search/it-IT?context=recipes&countries=it&accessories=includingFriend,includingBladeCover,includingBladeCoverWithPeeler,includingCutter&query=bun&categories=VrkNavCategory-RPF-013'`
   and wait for...
   `[CD] Goodbye!`
6. You'll have your dumped recipes inside `./recipes/test`
7. Enjoy your meal! :)

<details>
  <summary><code>Expand to see a full sample execution log</code></summary>
  
```shell
$ git clone https://github.com/psychowood/cookidump/ && cd cookidump/
Cloning into 'cookidump'...
remote: Enumerating objects: 254, done.
remote: Counting objects: 100% (254/254), done.
remote: Compressing objects: 100% (153/153), done.
remote: Total 254 (delta 117), reused 220 (delta 95), pack-reused 0
Receiving objects: 100% (254/254), 1.86 MiB | 9.85 MiB/s, done.
Resolving deltas: 100% (117/117), done.

$ docker-compose build --build-arg DOCKER_UID="$(id -u)" --build-arg DOCKER_GID="$(id -g)"
cookidump uses an image, skipping
Building build
Sending build context to Docker daemon  2.084MB
Step 1/13 : FROM python:alpine
 ---> 9a2ccd0e4ef5
Step 2/13 : RUN apk upgrade --no-cache --available    && apk add --no-cache chromium-chromedriver git
 ---> Using cache
 ---> d5695b861a37
Step 3/13 : RUN mkdir -p /home/cookidump     && adduser -D cookidump     && chown -R cookidump:cookidump /home/cookidump
 ---> Using cache
 ---> 7740ef313158
Step 4/13 : ARG DOCKER_UID
 ---> Using cache
 ---> 7d7da7393e0a
Step 5/13 : ARG DOCKER_GID
 ---> Using cache
 ---> 9f0606ea28ae
Step 6/13 : RUN deluser --remove-home cookidump     && addgroup -S cookidump -g ${DOCKER_GID}     && adduser -S -G cookidump -u ${DOCKER_UID} cookidump
 ---> Using cache
 ---> 372f8b377939
Step 7/13 : WORKDIR /home/cookidump
 ---> Using cache
 ---> c21efa64326b
Step 8/13 : RUN  chown -R cookidump:cookidump /home/cookidump
 ---> Using cache
 ---> 4eca170a86de
Step 9/13 : USER cookidump
 ---> Using cache
 ---> 9bc3c29eb210
Step 10/13 : COPY --chown=cookidump:cookidump ./ ./repo
 ---> 0e90316fb313
Step 11/13 : WORKDIR /home/cookidump/repo
 ---> Running in 12b1207c84ff
Removing intermediate container 12b1207c84ff
 ---> 3b58b3612a2c
Step 12/13 : RUN pip install -r requirements.txt
 ---> Running in 872c62cf1e29
Defaulting to user installation because normal site-packages is not writeable
Collecting beautifulsoup4 (from -r requirements.txt (line 1))
  Downloading beautifulsoup4-4.12.2-py3-none-any.whl (142 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 143.0/143.0 kB 9.2 MB/s eta 0:00:00
Collecting selenium>=4.8.0 (from -r requirements.txt (line 2))
  Downloading selenium-4.10.0-py3-none-any.whl (6.7 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 6.7/6.7 MB 32.4 MB/s eta 0:00:00
Collecting soupsieve>1.2 (from beautifulsoup4->-r requirements.txt (line 1))
  Downloading soupsieve-2.4.1-py3-none-any.whl (36 kB)
Collecting urllib3[socks]<3,>=1.26 (from selenium>=4.8.0->-r requirements.txt (line 2))
  Downloading urllib3-2.0.4-py3-none-any.whl (123 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 123.9/123.9 kB 31.6 MB/s eta 0:00:00
Collecting trio~=0.17 (from selenium>=4.8.0->-r requirements.txt (line 2))
  Downloading trio-0.22.2-py3-none-any.whl (400 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 400.2/400.2 kB 41.4 MB/s eta 0:00:00
Collecting trio-websocket~=0.9 (from selenium>=4.8.0->-r requirements.txt (line 2))
  Downloading trio_websocket-0.10.3-py3-none-any.whl (17 kB)
Collecting certifi>=2021.10.8 (from selenium>=4.8.0->-r requirements.txt (line 2))
  Downloading certifi-2023.7.22-py3-none-any.whl (158 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 158.3/158.3 kB 42.9 MB/s eta 0:00:00
Collecting attrs>=20.1.0 (from trio~=0.17->selenium>=4.8.0->-r requirements.txt (line 2))
  Downloading attrs-23.1.0-py3-none-any.whl (61 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 61.2/61.2 kB 17.8 MB/s eta 0:00:00
Collecting sortedcontainers (from trio~=0.17->selenium>=4.8.0->-r requirements.txt (line 2))
  Downloading sortedcontainers-2.4.0-py2.py3-none-any.whl (29 kB)
Collecting idna (from trio~=0.17->selenium>=4.8.0->-r requirements.txt (line 2))
  Downloading idna-3.4-py3-none-any.whl (61 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 61.5/61.5 kB 20.6 MB/s eta 0:00:00
Collecting outcome (from trio~=0.17->selenium>=4.8.0->-r requirements.txt (line 2))
  Downloading outcome-1.2.0-py2.py3-none-any.whl (9.7 kB)
Collecting sniffio (from trio~=0.17->selenium>=4.8.0->-r requirements.txt (line 2))
  Downloading sniffio-1.3.0-py3-none-any.whl (10 kB)
Collecting exceptiongroup (from trio-websocket~=0.9->selenium>=4.8.0->-r requirements.txt (line 2))
  Downloading exceptiongroup-1.1.2-py3-none-any.whl (14 kB)
Collecting wsproto>=0.14 (from trio-websocket~=0.9->selenium>=4.8.0->-r requirements.txt (line 2))
  Downloading wsproto-1.2.0-py3-none-any.whl (24 kB)
Collecting pysocks!=1.5.7,<2.0,>=1.5.6 (from urllib3[socks]<3,>=1.26->selenium>=4.8.0->-r requirements.txt (line 2))
  Downloading PySocks-1.7.1-py3-none-any.whl (16 kB)
Collecting h11<1,>=0.9.0 (from wsproto>=0.14->trio-websocket~=0.9->selenium>=4.8.0->-r requirements.txt (line 2))
  Downloading h11-0.14.0-py3-none-any.whl (58 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 58.3/58.3 kB 16.9 MB/s eta 0:00:00
Installing collected packages: sortedcontainers, urllib3, soupsieve, sniffio, pysocks, idna, h11, exceptiongroup, certifi, attrs, wsproto, outcome, beautifulsoup4, trio, trio-websocket, selenium
Successfully installed attrs-23.1.0 beautifulsoup4-4.12.2 certifi-2023.7.22 exceptiongroup-1.1.2 h11-0.14.0 idna-3.4 outcome-1.2.0 pysocks-1.7.1 selenium-4.10.0 sniffio-1.3.0 sortedcontainers-2.4.0 soupsieve-2.4.1 trio-0.22.2 trio-websocket-0.10.3 urllib3-2.0.4 wsproto-1.2.0

[notice] A new release of pip is available: 23.1.2 -> 23.2.1
[notice] To update, run: pip install --upgrade pip
Removing intermediate container 872c62cf1e29
 ---> e30e79606f2e
Step 13/13 : VOLUME /home/cookidump/repo
 ---> Running in 8e8f050ba50b
Removing intermediate container 8e8f050ba50b
 ---> e7a8f8a11b39
Successfully built e7a8f8a11b39
Successfully tagged cookidump_build:latest

$ docker-compose run --rm cookidump ./run.sh --save-cookies --login
Creating cookidump_cookidump_run ... done
[CD] Starting cookidump with arguments:
[CD]    webdriverfile = chromedriver
[CD]    outputdir = recipes
[CD]    subdir = None
[CD]    separate_json = True
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

$ docker-compose run --rm cookidump ./run.sh --searchquery '/search/it-IT?context=recipes&countries=it&accessories=includingFriend,includingBladeCover,includingBladeCoverWithPeeler,includingCutter&query=bun&categories=VrkNavCategory-RPF-013' -o test
Creating cookidump_cookidump_run ... done
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

$ ls -laR ./recipes/
./recipes/:
total 0
drwxr-xr-x 1 rancher rancher   8 Jul 25 11:35 .
drwxr-xr-x 1 rancher rancher 278 Jul 25 11:35 ..
drwxr-xr-x 1 rancher rancher  46 Jul 25 11:35 test

./recipes/test:
total 68
drwxr-xr-x 1 rancher rancher    46 Jul 25 11:35 .
drwxr-xr-x 1 rancher rancher     8 Jul 25 11:35 ..
drwxr-xr-x 1 rancher rancher    22 Jul 25 11:35 images
-rw-r--r-- 1 rancher rancher 67083 Jul 25 11:35 index.html
drwxr-xr-x 1 rancher rancher    70 Jul 25 11:35 recipes

./recipes/test/images:
total 48
drwxr-xr-x 1 rancher rancher    22 Jul 25 11:35 .
drwxr-xr-x 1 rancher rancher    46 Jul 25 11:35 ..
-rw-r--r-- 1 rancher rancher 45152 Jul 25 11:35 r660642.jpg

./recipes/test/recipes:
total 252
drwxr-xr-x 1 rancher rancher     70 Jul 25 11:35 .
drwxr-xr-x 1 rancher rancher     46 Jul 25 11:35 ..
-rw-r--r-- 1 rancher rancher  68960 Jul 25 11:35 r660642.html
-rw-r--r-- 1 rancher rancher   2865 Jul 25 11:35 r660642.json
-rw-r--r-- 1 rancher rancher 183757 Jul 25 11:35 r660642.pdf
```
</details>

#### Considerations ####

By following script instructions, it is also possible to apply custom filters to export selected recipes (for instance, in base of the dish, title and ingredients, Thermomix/Bimby version, etc.).

Output is represented by an `index.html` file, included in `outputdir`, plus a set of recipes inside of structured folders.
By opening the generated `index.html` file on your browser, it is possible to have a list of recipes downloaded and surf to the desired recipe.

The number of exported recipes is limited to around `1000` for each execution.
Hence, use of filters may help in this case to reduce the number of recipes exported.

If you play a little too much with authentication, you may incur in a CAPTCHA error in headless mode. You can then solve the captcha using the browser, or wait some hours for it to reset.

### Other approaches ###

A different approach, previously adopted, is based on the retrieval of structured data on recipes.
More information can be found on the [datastructure branch](https://github.com/auino/cookidump/tree/datastructure).
Output is represented in this case in a different (structured) format, hence, it has to be interpreted. Such interpretation is not implemented in the linked previous commit.

### TODO ###

* Bypass the limited number of exported recipes -> not really feasible automatically, the remote API limits to 1000 records. Can be bypassed by running multiple times with different search queries but needs quite a bit of smartness on the algorithm and would need merge of lists in the main html file to be browseable
* Parse downloaded recipes to store them on a database, or to generate a unique linked PDF
* Expose a rest service in the container to allow proxying requests, perhaps paired with an access token
* Publish a docker hub image

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
