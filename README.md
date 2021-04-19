# taklaPreWork
"Takla" dataset Generation and Collection

# related resources
For a collection of related resources in takla research [click here](https://docs.google.com/spreadsheets/d/1ntJRkiRoVro24c1Hp3Zpejx9LRum9EQ94qlJYA-ipy4/edit?usp=sharing) 


# Murad Takla
* **“Pure Banglish”**= phonetically correct romanization

* **“Murad Takla”**  =  phonetically in-correct romanization. Or “Mis-spelled Romanized Bangla”.
* Detected ops for conversion (till date):
    * Replacement of Pseudo Similar Sounding letters (RPSS)
    * Trailing H reduction (THR)
    * Vowel change (VC)
    * Vowel Addition (VA)
    * Vowel Reduction (VR)

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

# Utils-Unittest
* change directory to utils:```cd utils```
* run the two tests:``` python3 -m unittest test_wordCleaner```