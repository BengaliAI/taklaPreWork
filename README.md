# taklaPreWork
"Takla" dataset Generation and Collection
```python
Version: 0.0.1     
Authors: Md. Nazmuddoha Ansary
```
**LOCAL ENVIRONMENT**  
```python
OS          : Ubuntu 18.04.3 LTS (64-bit) Bionic Beaver        
Memory      : 7.7 GiB  
Processor   : Intel® Core™ i5-8250U CPU @ 1.60GHz × 8    
Graphics    : Intel® UHD Graphics 620 (Kabylake GT2)  
Gnome       : 3.28.2  
```
# Setup
* ```pip3 install -r requirements.txt``` 
> Its better to use a virtual environment 

**Error Case**: In the case of unwanted errors please kill headless chrome serrions: ```pkill -f "(chrome)?(--headless)"```

# Scrapper Useage (Data Collection from facebook)
**Scrapper Available for**
- [x] page
- [x] post 
- [ ] group 

* change directory to **scrapper** : ```cd scrapper/```
* change config as needed:
```python
    {
        "type"      :   use "post"/"page"
        "ids"       :   [corresponding entity ids as list],
        "save_path" :   "/path/to/save/ScrappedData/"
    }
```
* run : **python3 main.py**
### config notes
**example: page config.json**

```python
    {
        "type"      :   "page",
        "ids"       :   ["MuradTakla","chillox.burgers"],
        "save_path" :   "/media/ansary/DriveData/Work/bengalAI/Takla/ScrappedData/"
    }
```
**For ids field for a page**: for an url   https://m.facebook.com/MuradTakla page_id="MuradTakla"

**example: page config.json**

```python
    {
        "type"      :   "post",
        "ids"       :   ["https://facebook.com/story.php?story_fbid=XXXXXXXXXXXXXX&id=YYYYYYYYYYYYYYYY",
                         "https://facebook.com/story.php?story_fbid=ZZZZZZZZZZZZZZ&id=AAAAAAAAAAAAAAAA"],
        "save_path" :   "/path/to/save/ScrappedData/"
    }
```
**For ids field for posts**: 
* the story_fbid= the id of the story (the last number in www. sites)
* the id= user id in numbers

## Data Format:
**saves:**
* ```posts_%m_%d_%Y_%H_%M.csv```: with the following data columns:
>  ['post_url','time','text','likes', 'comments','shares']
* ```comments_%m_%d_%Y_%H_%M.csv```: with the following data columns:    
> [post_url","author","text"]
* ```%m_%d_%Y_%H_%M.csv```: saves the concatenated **text** data combined from **posts** and **comments**      

## Unstable Disclaimer: Group Scrapping
* use **./main.py** under **scrapper/unstable** to scrape groups
```python
    usage: main.py [-h] [--url URL]

    Group Facebook scraper script

    optional arguments:
    -h, --help  show this help message and exit
    --url URL   link of the Group to scrape (default: None)
```
The execution saves a **.json** file under **temp** folder within the same directory where the following data are saved with the following functions:

> POST CONTENT DATA:

```python 
    container['id']         =   post_index
    # time
    container['time']       =   UTILS.stringTime(get_post_time(post_iden)).strftime("%d/%m/%Y")
    # get author
    container['author']     =   get_post_author(post_iden)
    # get text 
    container['text']       =   get_post_text(post_iden) 
    # additional
    container['type']       =   'post'
```    
> RESPONSE SECTION DATA:
```python
    # fill container
    container['id']         =   post_index
    # time
    container['time']       =   get_comment_time(comment)
    # get author
    container['author']     =   get_comment_author(comment)
    # get text 
    container['text']       =   get_comment_text(comment)
    # additional
    container['type']       =   get_comment_type(comment) # reply / comment
```

## TODO
- [ ] format group scrapper base to : m.facebook.com (_avoid new look implementation for LTS_)
- [ ] same format for data saing



# DataSet
**A combined dataset of  1008165 _articles_,_single words_,_phrases_ and _sentences_ is created from the following sources**
* [WikiDump Bangla Data](https://dumps.wikimedia.org/bnwiki/latest/)
* [Bangla Newspaper Dataset:400k+ bangla news samples](https://www.kaggle.com/furcifer/bangla-newspaper-dataset)
* [40k Bangla Newspaper Article](https://www.kaggle.com/zshujon/40k-bangla-newspaper-article)
