import os
import sys
import ntpath
import json
import pandas as pd
import pprint
pd.set_option('display.max_colwidth', -1)


#def form_html_tag(item_type, path, video_type='mp4'):
def form_html_tag(item_type, path, media_id=0, video_type='mp4'): #### MoDIFY

    tag = None
    if item_type =='image':
        tag = '<img id=img%d class=img usemap=#m4 src=\"%s\" alt=\"\" border=3 class=\"img-icon\"></img>' % (media_id, path)
    elif item_type == 'video':
        tag = '<video controls><source src=\"%s\" type=\"video/%s\"></video>' % (path, video_type)
    return tag
        
def result_dataframe(data):

    result_dict = dict()
    result_dict['measure_uid'] = []
    media_id = 0 ####ADD
    for rid, result_collections in data.items():
        #print(result_collections)
        if not isinstance(result_collections, dict): continue
        for iid, result in result_collections.items():
            # Going into the dict describing each result containing description of fixed, moving, transformed images with measures
            if not isinstance(result, dict): 
                result_dict['measure_uid'].append(result)
                continue
                
            header, item_type, path = None, None, None
            for key, item in result.items():
                # Going into the innermost dict describing each item such as fixed image
                if key == 'header':
                    header = item
                    if item not in result_dict: # add additional table-column headers
                        result_dict[item] = []
                elif key == 'type':
                    item_type = item
                elif key == 'path':
                    path = item
            result_dict[header].append(form_html_tag(item_type, path, media_id)) ####ADD
            media_id +=1 ####ADD
            print(media_id)
            
    return pd.DataFrame(result_dict)
  
def generate_html(experiment_title, html_file, dataframe, css_style='staticpages.css'):
    table = dataframe.to_html(notebook=False, escape=False, justify='left', col_space=20,
          max_rows=1000, max_cols=1000).replace('<table border="1" class="dataframe">','<table class="sortable">')
    
 
    html_string = '''
<html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="../styles/'''+css_style+'''" type="text/css">
        <style></style>
        <script src="../js_lib/sorttable.js"></script>

    </head>
    <body>
        <div class="banner-image"></div>


        <h1>'''+experiment_title+'''</h1>
        <br><br>
        <div>
        ''' + table + '''
        </div>

    </body>
</html>'''     

    f = open(html_file,'w')
    f.write(html_string)
    f.close()
    
    return html_string
        
  
if __name__ == "__main__":    

    json_file, html_file, css_style = None, None, None
    experiment_title, measurements = None, None
    if len(sys.argv) < 3:
        print('Please provide\n1) a json file describing the experimet results to be reported and\n2) html output filename')
    else:
        json_file = sys.argv[1]
        html_file = sys.argv[2]
    if len(sys.argv) >= 4:
        css_style = ntpath.basename(sys.argv[3])
    
    with open(json_file) as f:
        data = json.load(f)
    
    if 'experiment_title' not in data:
        print('Please describe the experiment name in json')
    else:
        experiment_title = data['experiment_title']
      
    if 'measurements' not in data:
        print('Please provide path/to/quantitive_measurements in json')
    else:
        measurements = pd.read_csv(data['measurements'], header =0)

    media_results = result_dataframe(data)
    results = pd.merge(media_results, measurements, left_on='measure_uid', right_on='measure_uid', how='outer')
    results.drop(['measure_uid'], axis=1, inplace=True)    
    
    if css_style: generate_html(experiment_title, html_file, results, css_style)
    else: generate_html(experiment_title, html_file, results)
    
    