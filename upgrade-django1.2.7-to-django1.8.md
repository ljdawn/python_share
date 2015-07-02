We are upgrading the project from django1.2.7 to django1.8
<br>
this file will record what we are making to migrations

1.json, image
  import simplejson -> import json
  pil -> image

2.url retrives:
  {% url view_name args %} -> {% url 'view_name' args %}
  TODO
  * find . -type f -print0 | xargs -0 sed -i -r -e "s#\{% url ([a-zA-Z0-9_.:-]+)#\{% url '\1'#g"

3.urls.py:
  from django.conf.urls.defaults * -> from django.conf.urls import patterns, include, url
  

4.localflavor
  from django.localflavor... import ... -> from localflavor.... import ...
  
  TODO 
  * pip install localflavor
  * INSTALLED_APPS = (
    # ...
    'localflavor',
    )

5.crfs_token
  add {% crfs_token%} for forms.submit and view function
  BUT!!!!!!! there should be a better way

6.messages
  user.message_set.add() -> messages.add_message(request, messages.INFO, messages)
  TODO
  * from django.contrib import messages

7.adminmedia
  django1.5 had deprecated adminmedia 

8.auto_now & default
  in django1.3, we used auto_now and default in model together(sometimes)
  in django1.8, just use auto_now


