# Git Repository Finder And Analyzer For Pisi Linux Packages

Repo finder makes easy to find packages for the developers,it also uses for the git terminal searching
It works on the python3. Repo finder doesnt use git api,it parse html code of git

###### Usage

```sh


usage: search.py [-h] [--repo-user REPO_USER] [--query QUERY]
                 [--only-has-name ONLY_HAS_NAME_BOOLEAN] [--log LOG_FILE]

Repo Finder

optional arguments:
  -h, --help            show this help message and exit
  --repo-user REPO_USER
                        Set Repo User
  --query QUERY         Search Query
  --only-has-name ONLY_HAS_NAME_BOOLEAN
                        While searching package,shows only urls that has query
                        without contents query
  --log LOG_FILE        Write all events to log file



```


###### Dependecies 

- urllib
- BeatifulSoup
- argparse
- time
- colorama




###### Examples


```sh


python3 src/search.py --repo-user pisilinux --query kde


```
this process shows us all that  contains 'kde' queries on urls


```sh

python3 src/search.py --repo-user pisilinux --query kde --only-has-name 1


```
this process shows us urls that contains 'kde' queries and not relational urls
--only-has-name is a boolean and it takes only 1 , if you want to use


```sh

python3 src/search.py --repo-user pisilinux --query kde --logs log_file
```

exract log_file in actions while processing query




###### Conclusion

If you have any issue , please share with us
this script will improved

