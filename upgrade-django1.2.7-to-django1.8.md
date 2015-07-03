We are upgrading the project from django1.2.7 to django1.8
<br>
this file will record what we are making to migrations

1.setting.py
  check the document

2.json, image
  import simplejson -> import json
  pil -> image

3.url retrives:
  {% url view_name args %} -> {% url 'view_name' args %}
  TODO
  * find . -type f -print0 | xargs -0 sed -i -r -e "s#\{% url ([a-zA-Z0-9_.:-]+)#\{% url '\1'#g"

4.urls.py:
  from django.conf.urls.defaults * -> from django.conf.urls import patterns, include, url
  

5.localflavor
  from django.localflavor... import ... -> from localflavor.... import ...
  
  TODO 
  * pip install localflavor
  * INSTALLED_APPS = (
    # ...
    'localflavor',
    )

6.crfs_token
  add {% crfs_token%} for forms.submit and view function  

  can decorates all the urls in url.py

7.messages
  user.message_set.add() -> messages.add_message(request, messages.INFO, messages)  

  TODO
  * from django.contrib import messages

8.adminmedia
  django1.5 had deprecated adminmedia 

9.auto_now & default
  in django1.3, we used auto_now and default in model together(sometimes)  

  in django1.8, just use auto_now

10.PROFANITIES_LIST  

 deprecated 
