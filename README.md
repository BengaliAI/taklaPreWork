# taklaPreWork
"Takla" dataset Generation and Collection
```python
Version: 0.0.1     
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

### TODO
- [ ] format group scrapper base to : m.facebook.com (_avoid new look implementation for LTS_)
- [ ] same format for data saing



# DataSet
**A combined dataset of  1008165 _articles_,_single words_,_phrases_ and _sentences_ is created from the following sources**
* [WikiDump Bangla Data](https://dumps.wikimedia.org/bnwiki/latest/)
* [Bangla Newspaper Dataset:400k+ bangla news samples](https://www.kaggle.com/furcifer/bangla-newspaper-dataset)
* [40k Bangla Newspaper Article](https://www.kaggle.com/zshujon/40k-bangla-newspaper-article)

* The [DataSet](https://www.kaggle.com/nazmuddhohaansary/taklagraphemes) contains: 101 csv files with a text column and 10000 text data per csv
* A sample **sentence based division and dataEDA kernel** where a single file of 10000 rows of data creates **124003** rows of sentences/ phrases is available [here](https://www.kaggle.com/nazmuddhohaansary/datasetedasinglefile)

### TODO:(depends on the parser)
- [x] word separation 
- [x] grapheme division based on word separation

# Murad Takla
* **“Pure Banglish”**= phonetically correct romanization

* **“Murad Takla”**  =  phonetically in-correct romanization. Or “Mis-spelled Romanized Bangla”.
* Detected ops for conversion (till date):
    * Replacement of Pseudo Similar Sounding letters (RPSS)
    * Trailing H reduction (THR)
    * Vowel change (VC)
    * Vowel Addition (VA)
    * Vowel Reduction (VR)

### Sample Reasoing
```
    “Murad Takla” actually originates from the bangla phrase “মুরোদ থাকলে"

    So how did “Murod Thakle” become “Murad Takla”?


    vowel “o” after the letter “r”  was changed to “a” -- vowel change
    Thakle  -> Takla  

    Th has converted to T or in other words the “h” has been reduced 
    Vowel  “e” after the letter “l” was changed to “a” -- vowel change

    Again, let’s consider something else,

    Khela - > Kala

    Kh has converted to K or in other words the “h” has been reduced 
    Vowel  “e” after the letter “h”  was changed to “a” -- vowel change
    Hobe -> Haba

    Vowel  “o” after the letter “H”  was changed to “a” -- vowel change
    Vowel  “e” after the letter “b”  was changed to “a” -- vowel change

    But does this rule of reducing a trailing “h” and random changing of vowels apply all across the board? Well ,not exactly.

    Let’s consider another common word and some of its variances, "ভাই" Romanized- Bhai may come in the form of :

    Bhae - vowel change (VC)
    Bhaai/Bahai- vowel Addition (VA)
    Bhi - vowel Reduction (VR)
    Bai- Trailing H reduction (THR)
    Bi- A combination of THR and VC and VR
    Will also come in the form of : Vai or Vae or Vy and so on . Now here we are introduced with the letter “V” and although previously only vowels were replacing vowels , we see a semi-vowel (y) replacing a vowel. For simplicity , we will consider the addition/change/reduction of “W” and “Y” i.e- semi-vowels within VA/ VC/ VR.

    A general way to put this ,could be “Replacement of Pseudo Similar Sounding letters”(RPSS)

    Example of RPSS: (<-> means interchangeable )

    “Bh” or “B” <-> “V”  
    “Ph” or “P”<->”F”
    “Ch”or “C”<->”S”
    “G” or ”J”<->”Z”
    ”C”<->”K”
    and so on.
```
* [Published Blog](https://www.markopolo.ai/blog/articles/kala-hoba)

* check **takla_poc.ipynb** for proof of concepts operations
**sample**:
```python
    given: Sokhi bhalo kore binod beni badhiya de

    Increased Operations Test

    --------------------------------
    generated at  Number of Random Ops:1:	Sokhi bhalo kore binod veni badhiya de
    --------------------------------
    --------------------------------
    generated at  Number of Random Ops:2:	Sakhwa vhelau kerww bwnyd benuu budhoyoyo da
    --------------------------------


    Constant Single Operations Test
    --------------------------------
    generated: Skha bhol kora banod bini budheo de
    --------------------------------
    --------------------------------
    generated: Sokhi bhalo kore vinod beni vadhiya de
    --------------------------------
    --------------------------------
    generated: Soki balo kore binod beni badhiya de
    --------------------------------
    --------------------------------
    generated: Skha bhlu kra bnd bun bodh d
    --------------------------------
    --------------------------------
    generated: Soki balo kore binod beni badiya de
    --------------------------------
```
