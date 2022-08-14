#!/usr/bin/env python
# coding: utf-8

# # საქართველოს დასაქმების რუკა რეგიონების მიხედვით
# 
# სტატისტიკური რუკა რომელიც გვიჩვენებს დასაქმებულთა რაოდენობას რეგიონების მიხედვით (რაც ასევე მიგვითითებს თუ სად არის სამუშაო ადგილები).

# In[1]:


from IPython.display import display, HTML

display(HTML("""<img alt="დასაქმების რუკა" src="map.png"></img>"""))


# # დასაქმება საქართველოში რეგიონების მიხედვით
# 
# ფერების ზუსტი მნიშვნელობები მითითებულია რუკის გამოსახულების ზედა მარჯვენა კუთხეში (რაოდენობა ათასებშია) და თითოეული ფერის გასწვრივ მითითებული რიცხვები გვეუბნება შუალედებს, თუ რომელი ფერი რამდენ ათას დასაქმებულს გამოხატავს. სტატისტიკური მონაცემებისათვის ფერების შეხამება შესრულებულია `coolwarm` colormap-ის გამოყენებით, რაც იმას ნიშნავს, რომ უფრო თბილი ფერები შეესაბამება რეგიონებს სადაც სტატისტიკურად უფრო მაღალი დასაქმებაა (რაც უფრო თბილი ფერია, დასაქმებულების/სამუშაო ადგილების რაოდენობაც უფრო მაღალია), ხოლო ცივი ფერები კი პირიქით, შეესაბამება სტატისტიკურად დაბალ დასაქმებას (შესაბამისად ნაკლები რაოდენობის დასაქმებულს და ნაკლებ სამუშაო ადგილებს). მოცემული რუკის გამოსახულების შექმნისათვის გამოყენებული Python-კოდი სრულიად ღია სახით შეგიძლიათ იხილოთ ამავე დოკუმენტის [ინგლისურენოვან ვერსიაში](../).
# 
# 
# 
# გამოყენებული მონაცემები:
# - სტატისტიკური მონაცემები რეგიონების მიხედვით სამუშაო ძალის მაჩვენებლების შესახებ მოპოვებულია 2022 წლის 1 ივნისს საქართველოს სტატისტიკის ეროვნული სამსახურის (საქსტატის) ვებსაიტიდან: [geostat.ge](https://www.geostat.ge/ka/)
# 
# - რუკის მონაცემები საქართველოს რეგიონების ადმინისტრაციული საზღვრების შესახებ (GADM data v4.0 for Georgia in `Shapefile` format) მოპოვებულია 2022 წლის 1 ივნისს GADM-ის ვებსაიტიდან: [gadm.org](https://gadm.org)
# 

# In[2]:


get_ipython().run_cell_magic('HTML', '', "<style>\n@media (max-width: 540px) {\n  .output .output_subarea {\n    max-width: 100%;\n  }\n}\n</style>\n<script>\n  $( document ).ready(function(){\n    $('div.input').hide();\n  });\n</script>\n")


# In[3]:


get_ipython().run_cell_magic('capture', '', '%mkdir OGP_classic_ka\n')


# In[4]:


get_ipython().run_cell_magic('capture', '', '%%file "OGP_classic_ka/conf.json"\n{\n  "base_template": "classic",\n  "preprocessors": {\n    "500-metadata": {\n      "type": "nbconvert.preprocessors.ClearMetadataPreprocessor",\n      "enabled": true,\n      "clear_notebook_metadata": true,\n      "clear_cell_metadata": true\n    },\n    "900-files": {\n      "type": "nbconvert.preprocessors.ExtractOutputPreprocessor",\n      "enabled": true\n    }\n  }\n}\n')


# In[5]:


get_ipython().run_cell_magic('capture', '', '%%file "OGP_classic_ka/index.html.j2"\n{%- extends \'classic/index.html.j2\' -%}\n{%- block html_head -%}\n\n{#  OGP attributes for shareability #}\n<meta property="og:url"          content="https://sentinel-1.github.io/employment_map_Georgia/ka/" />\n<meta property="og:type"         content="article" />\n<meta property="og:title"        content="საქართველოს დასაქმების რუკა რეგიონების მიხედვით" />\n<meta property="og:description"  content="სად არის სამუშაო ადგილები საქართველოში?" />\n<meta property="og:image"        content="https://raw.githubusercontent.com/sentinel-1/employment_map_Georgia/master/map.png" />\n<meta property="og:image:alt"    content="დასაქმების რუკა" />\n<meta property="og:image:type"   content="image/png" />\n<meta property="og:image:width"  content="1296" />\n<meta property="og:image:height" content="648" />\n\n<meta property="article:published_time" content="2022-08-14T06:18:45+00:00" />\n<meta property="article:modified_time"  content="{{ resources.iso8610_datetime_utcnow }}" />\n<meta property="article:publisher"      content="https://sentinel-1.github.io" />\n<meta property="article:author"         content="https://github.com/sentinel-1" />\n<meta property="article:section"        content="datascience" />\n<meta property="article:tag"            content="datascience" />\n<meta property="article:tag"            content="geospatialdata" />\n<meta property="article:tag"            content="Python" />\n<meta property="article:tag"            content="data" />\n<meta property="article:tag"            content="analytics" />\n<meta property="article:tag"            content="datavisualization" />\n<meta property="article:tag"            content="bigdataunit" />\n<meta property="article:tag"            content="visualization" />\n<meta property="article:tag"            content="employment" />\n<meta property="article:tag"            content="Georgia" />\n\n\n{{ super() }}\n\n{%- endblock html_head -%}\n\n\n{% block body_header %}\n<body>\n\n<div class="container">\n  <nav class="navbar navbar-default">\n    <div class="container-fluid">\n      <ul class="nav nav-pills  navbar-left">\n        <li role="presentation">\n          <a href="/ka/">\n            <svg xmlns="http://www.w3.org/2000/svg"\n                 viewBox="0 0 576 512" width="1em">\n              <path \n                fill="#999999"\nd="M 288,0 574,288 511,288 511,511 352,511 352,352 223,352 223,511 62,511 64,288 0,288 Z"\n              />\n            </svg> მთავარი\n          </a>\n        </li>\n      </ul>\n      <ul class="nav nav-pills  navbar-right">\n        <li role="presentation">\n          <a href="/employment_map_Georgia/">🇬🇧 English </a>\n        </li>\n        <li role="presentation" class="active">\n          <a href="/employment_map_Georgia/ka/">🇬🇪 ქართული</a>\n        </li>\n      </ul>\n    </div>\n  </nav>\n</div>\n\n\n\n  <div tabindex="-1" id="notebook" class="border-box-sizing">\n    <div class="container" id="notebook-container">    \n{% endblock body_header %}\n\n{% block body_footer %}\n    </div>\n  </div>\n  <footer>\n    <div class="container"\n         style="display:flex; flex-direction: row; justify-content: center; align-items: center;">\n      <p style="margin: 3.7em auto;"> © 2022\n        <a href="https://github.com/sentinel-1" target="_blank">Sentinel-1</a>\n      </p>\n      <!-- TOP.GE ASYNC COUNTER CODE -->\n      <div id="top-ge-counter-container" data-site-id="116052"\n           style="margin-right: 3.7em;float: right;"></div>\n      <script async src="//counter.top.ge/counter.js"></script>\n      <!-- / END OF TOP.GE COUNTER CODE -->\n      <!-- ANALYTICS.LAGOGAL.COM -->\n      <div id="analytics-lagogal-com-access" data-site-id="20221"\n           style="margin: 0;padding: 0;"></div>\n      <script async src="//analytics.lagogal.com/access.js"></script>\n      <!-- / END OF ANALYTICS.LAGOGAL.COM -->\n     </div>\n  </footer>\n</body>\n{% endblock body_footer %}\n')


# 
# *მოცემული დოკუმენტი თავდაპირველად გამოქვეყნებულ იქნა Apache License (Version 2.0) ლიცენზიით შემდეგ GitHub რეპოზიტორზე: [sentinel-1/employment_map_Georgia](https://github.com/sentinel-1/employment_map_Georgia)*
# 
# მოცემულ დოკუმენტის ორიგინალ ვერსიასთან დაკავშირებულ საკითხებზე შესაბამისი უკუკავშირისათვის, რჩევებისათვის ან შენიშვნებისთვის (თუ რამეა) შეგიძლიათ ახალი Issue-ს შექმნის გზით დააყენოთ საკითხი მისივე GitHub რეპოზიტორის შესაბამის გვერდზე: [Issues page of the repository](https://github.com/sentinel-1/employment_map_Georgia/issues)
# 
