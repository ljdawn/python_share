We are upgrading the project from django1.2.7 to django1.8  
this file will record what we are making to migrations

1.setting.py  
  check the document

2.json, image  
  import simplejson -> import json  
  pil -> image/pillow

3.url retrives:  
  {% url view_name args %} -> {% url 'view_name' args %}  
  TODO  
  * find . -type f -print0 | xargs -0 sed -i -r -e "s#\{% url ([a-zA-Z0-9_.:-]+)#\{% url '\1'#g"

4.urls.py:  
  from django.conf.urls.defaults * -> from django.conf.urls import patterns, include, url

5.localflavor  
  from django.localflavor... import ... -> from localflavor.... import ...  
  <br>
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
  in django1.3, we used auto_now and default in model together  
  in django1.8, just use auto_now

10.PROFANITIES_LIST,mimetype  
   deprecated 

11. get_query_set -> get_queryset

12. command - transaction.commit_manually -> transaction.atomic  
    transaction decprete set_dirty

13. AttributeError: class BILLING has no attribute 'SUBSCRIPTION_DONT_RENEW' ?
    /home/Asa/svn/trunk/billing/management/commands/upgrade_biller.py

14. 'FallbackStorage' object does not support indexing  
   {% if messages|is_error_msg %} -> <p class="{% if messages.0.level == DEFAULT_MESSAGE_LEVELS.ERROR %}error{% else %}success{% endif %}"  
   bad way...

15. mod_python -> wsgi
