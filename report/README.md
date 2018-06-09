
# HTML Report Generator

A simple generator developed for reporting results from (large-scale) experimental studies in a form of a sortable table. The generator receives a json file describing experimental results to be displayed; thus column headers and contents can be designed and tailored to individual experiments. It supports 2D images, videos, and quantitative measurements. The format of json file compatible with the generator is described below. 

## Section 1. Getting Started


### Prerequisites

The generator was developed using [python 3.6.5](https://www.python.org/downloads/) and [pandas 0.23.0](https://pandas.pydata.org/) to generate an html table. For conda users, you can install the packages using a
command
```
conda install python=3.6.5 pandas=0.23.0
```
or create a new conda environment using .yml files provided in `./enviroments/` using a command
```
conda env create -f environment.yml
```
Currently only a yml file for **Windows** is provided and that for Linux will be added soon.

### HTML Style
A generated HTML report uses a style defined in `./styles/staticpages.css`. You can, of course, change the style and appearance of your report by copying this `.css` and modifying it according to your liking, perhaps to change the size of images and/or video, the background color, font styles and colors, etc. To use your `.css`, place your `.css` in `./styles/` and pass it as input the generator as described in Section 2.

### JSON format

A json file is used as an input to describe the format of your desired HTML table and paths to experimental results to be displayed. The generator supports quantitative measurements and media (i.e., 2D images and videos). Here we assume that your quantitative measurements are stored in one .csv file on which each column represents each metric measure separated by a comma (,). **An extra column with the pre-defined, fixed header `measure_uid` need to be present**; each element in this column is an **ID of each experiment**, implying that all related images and/or videos resulted from the experiment shared the same ID. `measure_uid` is used internally as a key to link each measurement to each relevant media to be displayed in the same row of the HTML table. An example of a csv file reporting target registration error, normalized cross correlation, and Jacobian determinants of displacement fields is

```
measure_uid,TRE, NCC, JD
1223323,0.223,0.845,4.678
1223326,0.593,0.707,3.086
1223327,0.432,0.789,3.976
...
```
The json file contains two `name/value` pairs: <br/>
```
"experiment_title":"your experiment name"
"measurements":"path/to/csv-file"
```
The latter is the csv file described above. Aside from these two pairs, the json file contains **any number** of `name/object` pairs. An `object` in each `name/object` pair describe media involving with each experiment and the `name` is just an arbitrary ID for the result. An example result from a rigid registration could be <br/>

```
"AnyID":{
      "fixed":{}
      "moving":{}
      "measure_uid":"alphanumeric_characters"
      "result_img":{}
      "video":{}
    }
```
This is one json object. The value of `"measure_id"` is some alphanumeric characters matching that of a quanititative measure recorded in the corresponding .csv file. Values of other members of an object are **not** `{}` and will be described below. (We ignore it for now for clarity and simplicity.) These members of a json object, **except `"measure_id"`**, (named `"fixed"`, `"moving"`, `"result_img"`, `"video"`) are not required and can be changed according to your requirement. Hence, your object could be
```
"BARBAR":{
      "true_label":{}
      "measure_uid":"alphanumeric_characters"
      "estimated_label1":{}
      "estimated_label2":{}
      "estimated_label3":{}
    }
```
where `"estimated_label1"`, `"estimated_label2"`, `"estimated_label3"` the three most likely labels for an object in a given test image. 

Now we define values of members of an object, which is presented as `{}` above. Each member is by itself a json object and required to contain the following three `name/value` pairs: <br/>

```
"header":"....",
"type":"....",
"path":"...."
```
The value of `"header"` is the name of the column or the column header. The value of `"type"` is either `"image"` or `"video"`, but not both, and the value of `"path"` is path\to\image or path\to\video. We recommend using absolute paths if you want to separate the report generator code from your experimental results. Hence, the `AnyID` object above should look like <br/>
```
"AnyID":{
      "fixed":{ 
        "header":"....",
        "type":"....",
        "path":"...."
      }
      "moving":{
        "header":"....",
        "type":"....",
        "path":"...."
      }
      "measure_uid":"alphanumeric_characters"
      "result_img":{
        "header":"....",
        "type":"....",
        "path":"...."      
      }
      "video":{
         "header":"....",
        "type":"....",
        "path":"...."     
      }
    }
```
In a nutshell, a json file should follow the following format <br/>
```
{
    "experiment_title":"your experiment name"
    "measurements":"path/to/csv-file"
    "BARBAR1":{
          "true_label":{
                "header":"....",
                "type":"....",
                "path":"...."   
          }
          "measure_uid":"alphanumeric_characters"
          "estimated_label1":{
                "header":"....",
                "type":"....",
                "path":"...."   
          }
          "estimated_label2":{
                "header":"....",
                "type":"....",
                "path":"...."   
          }
          "estimated_label3":{
                "header":"....",
                "type":"....",
                "path":"...."   
          }
    }
    "BARBAR2":{
          "true_label":{
                "header":"....",
                "type":"....",
                "path":"...."   
          }
          "measure_uid":"alphanumeric_characters"
          "estimated_label1":{
                "header":"....",
                "type":"....",
                "path":"...."   
          }
          "estimated_label2":{
                "header":"....",
                "type":"....",
                "path":"...."   
          }
          "estimated_label3":{
                "header":"....",
                "type":"....",
                "path":"...."   
          }
    }    
    ......
}
```
An example json file can be found in `./examples/`.


## Section 2. Generating a Report


### Run an Example

The package includes example 'results' to be displayed in `./examples/`. The associated json file is `./examples/results.json` and the generated HTML report is `./examples/report.html`. Assuming that you are at the package folder, to reproduce the report, use the following command 

```
> python html_report.py ./examples/results.json ./examples/report_blue.html 
```

### Generate a Report

The script requires two input and one optional input in the following format

```
> python html_report.py /path/to/input.json /path/to/report.html [css_file]
```
In cases that you have your own css style file in `./styles/` and want to use it, use the following command <br/>
```
> python html_report.py /path/to/input.json /path/to/report.html css_filename
```

## Versioning

Let's say its version is v0.0. 

## Authors

* **Sureerat Reaungamornrat** - *Initial work* <br/>
To be added


## Acknowledgments

We acknowledge Sebustien Piat for his html report genertor which inspires this development... To be continue....

