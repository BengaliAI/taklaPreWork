# taklaPreWork
"Takla" dataset Generation and Collection

# DataSet
**A combined dataset of  1008165 _articles_,_single words_,_phrases_ and _sentences_ is created from the following sources**
* [WikiDump Bangla Data](https://dumps.wikimedia.org/bnwiki/latest/)
* [Bangla Newspaper Dataset:400k+ bangla news samples](https://www.kaggle.com/furcifer/bangla-newspaper-dataset)
* [40k Bangla Newspaper Article](https://www.kaggle.com/zshujon/40k-bangla-newspaper-article)

* The [DataSet](https://www.kaggle.com/nazmuddhohaansary/taklagraphemes) contains: 101 csv files with a text column and 10000 text data per csv
* A sample **sentence based division and dataEDA kernel** where a single file of 10000 rows of data creates **124003** rows of sentences/ phrases is available [here](https://www.kaggle.com/nazmuddhohaansary/datasetedasinglefile)


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
# Related resources
For a collection of related resources in takla research [click here](https://docs.google.com/spreadsheets/d/1ntJRkiRoVro24c1Hp3Zpejx9LRum9EQ94qlJYA-ipy4/edit?usp=sharing) 
