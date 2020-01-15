This repository contains the code for **Influence Dispersion Tree: Modeling the Impact of Scientific Papers**
authored by Annu Joshi, Sumit Bhatia & Tanmoy Chakraborty. 

## Instruction
The NID of an paper can be calculated using this repository. 
* The script will parse the citing_cited.csv and create the citation graph, using which the Influence Dispersion Tree and Influence Disperion Index will be calculated.  


## Directories 
### src
This has 2 has scripts named 
* ```init.py```
This script parses the dataset. It first parses for the year, and then creates a ```global_citation_graph```. In this, the invalid edges are removed, the Influence Dispersion Graph (IDG) for each paper is isolated and converted to Influence Dispersion Tree (IDT) and serialised in the form of a dictionary. 
The agruments it takes are (All are mandatory):
    * ```--dataset```: path of the meta data file dataset. 
    * ```--dumps```: path to dump the serialised pickled files. 
    * ```--graph_path```: path to citation-cited.csv. 
    
    
* ```utils.py```
This script houses all the functions used in the other two scripts. all the documentation can be accessed by ```function_name.__doc__```. 
 

### data 
We have used two datasets in this paper:

* _APS Datatset_: We are unable to make this dataset publicly available due to privacy agreement. Interested parties may request the data from the [official website](http://journals.aps.org/datasets) or data-requests@aps.org.

The dataset comes in two parts:
* citing_cited.csv - Data set containing pairs of APS articles that cite each other for the corpus of Physical Review Letters, Physical Review, and Reviews of Modern Physics from 1893 through 2009. If article A cites article B, there will be an entry in the data set consisting of the pair of identifiers for A and B.
* metadata - contains information regarding the paper.

* ```<article>```
* ```<journal>```
* ```<volume>```
* ```<issue>```
* ```<title>```
* ```<authgrp>```
* ```<author>```
* ```<givenname>```
* ```<middlename>```
* ```<surname>```
* ```<aff>```
* ```<cpyrt>```
* ```<cpyrtdate date>```

An example from the dataset :
```
<article doi="10.1103/PhysRevA.1.106">
<journal jcode="PRA" short="Phys. Rev. A">Physical Review A</journal>
<volume>1</volume>
<issue printdate="1970-01-00">1</issue>
<fpage>106</fpage>
<lpage>121</lpage>
<seqno>1</seqno>
<price></price><tocsec>Articles</tocsec>
<arttype type="article"></arttype><doi>10.1103/PhysRevA.1.106</doi>
<title>Long-Term Solutions in Semiclassical Radiation Theory</title>
<authgrp>
<author><givenname>C.</givenname><middlename>R.</middlename><surname>Stroud</surname><suffix>Jr.</suffix></author>
<aff>The Institute of Optics, The University of Rochester, Rochester, New York 14627</aff>
</authgrp>
<authgrp>
<author><givenname>E.</givenname><middlename>T.</middlename><surname>Jaynes</surname></author>
<aff>Arthur H. Compton Laboratory of Physics, Washington University, St. Louis, Missouri 63130</aff>
</authgrp>
<history>
<received date="1969-05-22"/>
</history>
<cpyrt>
<cpyrtdate date="1970" /><cpyrtholder>The American Physical Society</cpyrtholder>
</cpyrt>
</article>
```

* _MAS Datatset_: The data which we have used is the Microsoft Academic Search Dataset (MAS), this dataset was created by crawling the [Microsoft Academic](https://academic.microsoft.com/home) web portal. 

For computer science dataset related information, please refer [here](https://github.com/LCS2-IIITD/influence-dispersion)

The dataset description are as follows:

|            Number of Papers            |    PRJ |    MAS    |
|:--------------------------------------:|:------:|:---------:|
|         Number of Papers               | 384,289| 3,908,805 |
|         Number of Unique Venues        |   412  |   5,149   |
|        Number of unique authors        | 235,533| 1,186,412 |
|    Avg. number of papers per author    | 10.47  | 5.21      |
|    Avg. number of authors per paper    | 5.33   | 2.57      |
| Min/Max number of references per paper | 1/581  | 1/2,432   |
|  Min/Max number of citations per paper | 1/4757 | 1/13,102  |
 
 
Incase of any queries you can reach annuj@iiitd.ac.in
