from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError

from classroom.models import (Collaboration_actuelle,Comment_display, Equipe, Quiz, Capteur,  Student, TypeCapteur , Domaine, Subject, User, Profile, Comment)











# Email Adress

class Subscribe(forms.Form):
    Email = forms.EmailField()
    
    def __str__(self):
        return self.Email









# Subject
class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'



#Type_Capteur
class TypeCapteurForm(forms.ModelForm):
    class Meta:
        model = TypeCapteur
        fields = '__all__'


#Domaine

class DomaineForm(forms.ModelForm):
    class Meta:
        model = Domaine
        fields = '__all__'



#StudentSignUpForm

class StudentSignUpForm(UserCreationForm):
    email= forms.EmailField()


    interests = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label='Vos disciplines scientifiques ',
    )

    domaine = forms.ModelMultipleChoiceField(
        queryset=Domaine.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label='Vos domaines d"applications ',
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']
       
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        student.interests.add(*self.cleaned_data.get('interests'))
        student.domaine.add(*self.cleaned_data.get('domaine'))
        student.domaine.add(*self.cleaned_data.get('domaine'))
        return user









class EventForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.get('user',None)
        #self.user = kwargs.pop('user',None)
        super(EventForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        #self.helper.form_action = reverse_lazy('simpleuser')
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn-success'))     

    class Meta:
        model = Quiz
        fields = ['subject', 'domaine', 'titre_projet', 'description_projet', 'type_evt']
        widgets ={
        'subject': forms.CheckboxSelectMultiple,
        }













class ProjetForm(forms.ModelForm):

    subject = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Mots Clés ',
    

    )
    

    class Meta:
          model = Quiz
          fields = ['titre_projet', 'description_projet','type_evt', 'domaine', 'subject','sensibilite', 'stabilite',  'selectivite', 'precision','gamme','format_sortie','temps_reponse','condition_ambiante', 'cout','poids', 'taille','nom_1', 'prenom_1', 'adresse_email_1', 'nom_2','prenom_2','adresse_email_2','adresse_email_3','nom_3',  'file_1', 'file_2', 'file_3','confidentalite']
         

   





class ProjetForm(forms.ModelForm):

    subject = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label = 'Disciplines scientifiques necessaires au projet ',
    )

    class Meta:
          model = Quiz
          fields = ['titre_projet', 'description_projet','type_evt', 'domaine', 'subject','sensibilite', 'stabilite',  'selectivite', 'precision','gamme','format_sortie','temps_reponse','condition_ambiante', 'cout','poids', 'taille','nom_1', 'prenom_1', 'adresse_email_1', 'nom_2','prenom_2','adresse_email_2','adresse_email_3','nom_3',  'file_1', 'file_2', 'confidentalite']
         



class CapteurForm(forms.ModelForm):

    subject = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
          model = Capteur
          fields = ['nom_capteur', 'description_projet','subject', 'type_evt', 'domaine', 'technologie_utilisee', 'etendue','sensibilite','resolution','precision', 'rapidite','justesse','reproductibilite', 'temps_de_reponse','bande_passante','hysteresis', 'gamme_temperature','file_1', 'file_2', 'file_3','confidentalite',]
         
      
       












class EquipeForm(forms.ModelForm):

    class Meta:
        model = Equipe
        fields = ['nom_1', 'prenom_1', 'adresse_email_1', 'nom_2','prenom_2']






class actuelle(forms.ModelForm):

    class Meta:
        model = Collaboration_actuelle
        fields = ['description_collaboration',]



































class TeacherSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user



 






class DateInput(forms.DateInput):
    input_type = 'date'







        





class StudentInterestsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('interests', )
        widgets = {
            'interests': forms.CheckboxSelectMultiple
        }

class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username']



class ProfileUpdateForm(forms.ModelForm):


    class Meta:
          model = Student
          fields = ['image','nom', 'prenom',  'composante', 'fonction',  'expert']
         
  
class ProfileCUpdateForm(forms.ModelForm):


    class Meta:
          model = Student
          fields = ['image','nom', 'prenom','adresse_email','interests', 'composante', 'fonction', 'domaine', 'expert']        

class CommentForm(forms.ModelForm):
    class Meta:
        content = forms.CharField(label="", widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Text goes here!!', 'rows':'4', 'cols':'50'}))
        model = Comment
        fields = ('content',)

class CommentForm_capteurs(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Text goes here!!', 'rows':'4', 'cols':'50'}))
    class Meta:
        model = Comment_display
        fields = ('content',)