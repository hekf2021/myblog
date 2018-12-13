from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from ckeditor.widgets import CKEditorWidget

class CommentForm(forms.Form):
    content_type =forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    text = forms.CharField(widget=CKEditorWidget(config_name='comment_ckeditor'),error_messages={'required':'评论内容不能为空'})

    def __init__(self,*args, **kwargs):
        if 'user' in kwargs:     #此user是在views的update_comment方法中，CommentForm(request.POST,user=request.user)传过来的
            #如kwargs参数中有user才能取
            self.user = kwargs.pop('user')  #这儿user必须从kwargs中弹出，不然下面的方法super会出错
        super(CommentForm,self).__init__(*args, **kwargs)

    def clean(self):
        #判断用户是否登陆
        if self.user.is_authenticated:
            self.cleaned_data['user']=self.user
        else:
            raise forms.ValidationError('用户尚未登陆')
        # 评论对象验证
        content_type = self.cleaned_data['content_type']
        object_id = self.cleaned_data['object_id']
        try:
            model_class = ContentType.objects.get(model=content_type).model_class()
            model_obj = model_class.objects.get(pk=object_id)
            self.cleaned_data['content_object']= model_obj
        except ObjectDoesNotExist:
            raise forms.ValidationError('评论对象不存在')

        return  self.cleaned_data