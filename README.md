Shape Statistics using python
=========
---------
This package allows the application of advanced statistical models to morphological data such as shapes.
A similar package allows statistical models tailored to the data produced by [BrainSuite]
Some features of this package are:

  - a python interface for manipulating morphological data using [R] through [Rpy2]
  - a python interface for using [statsmodels] with [pandas] for a pure python implementation
  - Ability to plot graphs, charts and visualizations on surfaces (coming soon)


Download
----

Currently download from https://bitbucket.org/shjoshi/shapestats/

Requirements (short version)
-----------
* [R] - built as a library with –enable-R-shlib (Default on Windows and Mac OSX)
* [Python] 2.7 
* Base Python packages - virtualenv, pip, numpy, scipy
> ##### **NOTE:** Alternately, install [Canopy] python. Makes life much easier.
* Add on Python packages - [pandas], [statsmodels], [rpy2]

Requirements (long version)
-----------
To stick to a pure python execution, one could skip installing R, and Rpy2. However, in our benchmarks, Rpy2+R currently shows the best performance. 

Thus, to get all the functionality of the toolbox, it is recommended to install the following software on your computer.

* Working [python] installation (We recommend version 2.7) -   
with the following packages:
    * virtualenv, pip, numpy, scipy  

> ##### **NOTE:** Alternately, you could download [Canopy] express, a comprehensive python framework geared towards scientifc computing, available for free.

* [R] - R software for statistical computing (built as a library with –enable-R-shlib)
    
    This is by default on Mac OSX and Windows. 
    
    On Linux, for e.g. in the root directory of the R source, one can do:

    ```sh
sudo ./configure  --enable-R-shlib  
sudo make  
sudo make install  
    ```

* [Rpy2] - python interface to R


* [statsmodels] - pure python module for statistical inference and much more


Installation for Mac OSX/Linux - Approach 1
--------------
To be followed if all the requirements above are satisfied. 

It is recommended to create a virtual python environment for your user.
If the downloaded location for the stats package is at ~/shapestats

For e.g., to create a virtualenv in your user directory, you could open the terminal and type
```sh
virtualenv --system-site-packages ~/statsenv
```
and
```sh
~/statsenv/bin/python ~/shapestats/setup.py install
```

Installation for Mac OSX/Linux  - Approach 2
--------------
>####**To be developed.**

Bootstrap everything. Start with a basic python installation

Create a virtualenv in the user directory

Install all the packages in virtualenv

Install the shapestats package in virtualenv


Example for running ANOVA for model comparison
--------------
The source package includes a test directory with sample data. Assuming the unzipped source directory is located at: ~/shapestats, open the file
```sh
~/shapestats/shapests/test/data/sample1/modelspec.ini
```
and change the respective paths for the variables
```sh
subjectdir, demographics, phenotype_attribute_matrix, atlas_surface
```
to correspond to the paths on your file system. 
Then type,
```sh
~/statsenv/bin/shapestats_model.py -modelspec
~/shapestats/shapestats/test/data/sample1/modelspec.ini -outdir ~/ -statsengine R
```

---
License
----

MIT

[BrainSuite]:http://brainsuite.org
[python]:http://www.python.org 
[Canopy]:https://www.enthought.com/products/canopy/
[statsmodels]:http://statsmodels.sourceforge.net
[pandas]:http://pandas.pydata.org
[R]:http://www.r-project.org
[Rpy2]:http://rpy.sourceforge.net/rpy2.html
