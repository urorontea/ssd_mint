from django import forms

class NameForm(forms.Form):
    your_name = forms.CharField(label="Your name", max_length=100)

class URLForm_1(forms.Form):
    url_1 = forms.URLField(label = "URL_1")
    start_1 = forms.IntegerField(label = "start_1")
    end_1 = forms.IntegerField(label = "end_1")
    type = forms.CharField(label = "type")#車両タイプの指定をする

class URLForm_2(forms.Form):
    url_1 = forms.URLField(label = "URL_1")
    start_1 = forms.IntegerField(label = "start_1")
    end_1 = forms.IntegerField(label = "end_1")
    url_2 = forms.URLField(label = "URL_2")
    start_2 = forms.IntegerField(label = "start_2")
    end_2 = forms.IntegerField(label = "end_2")
    name = forms.CharField(label = "name")#動画連結後の名前をここで指定する
    type = forms.CharField(label = "type")#車両タイプの指定をする

class URLForm_3(forms.Form):
    url_1 = forms.URLField(label = "URL_1")
    start_1 = forms.IntegerField(label = "start_1")
    end_1 = forms.IntegerField(label = "end_1")
    url_2 = forms.URLField(label = "URL_2")
    start_2 = forms.IntegerField(label = "start_2")
    end_2 = forms.IntegerField(label = "end_2")
    url_3 = forms.URLField(label = "URL_3")
    start_3 = forms.IntegerField(label = "start_3")
    end_3 = forms.IntegerField(label = "end_3")
    
    name = forms.CharField(label = "name")#動画連結後の名前をここで指定する
    type = forms.CharField(label = "type")#車両タイプの指定をする
   
