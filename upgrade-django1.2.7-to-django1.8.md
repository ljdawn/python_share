We are upgrading the project from django1.2.7 to django1.8
<br\>
this file will record what we are making to migrations

1.url retrives:
  {% url view_name args %} -> {% url 'view_name' args %}
  TODO
  * find . -type f -print0 | xargs -0 sed -i -r -e "s#\{% url ([a-zA-Z0-9_.:-]+)#\{% url '\1'#g"

2.urls.py:
  from django.conf.urls.defaults * -> from django.conf.urls import patterns, include, url
  

3.localflavor
  from django.localflavor... import ... -> from localflavor.... import ...
  
  TODO 
  * pip install localflavor
  * INSTALLED_APPS = (
    # ...
    'localflavor',
    )

4.crfs_token
  add {% crfs_token%} for forms.submit

5.messages
  user.message_set.add() -> messages.add_message(request, messages.INFO, messages)
  TODO
  * from django.contrib import messages

5.json
  import simplejson -> import json
