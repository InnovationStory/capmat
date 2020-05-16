from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image
from django.utils.html import escape, mark_safe
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.forms import ModelForm
from django.utils.text import slugify
from django.template.defaultfilters import slugify
from django.dispatch import receiver
import re
from django.utils import timezone

from django.conf import settings 
from django.http import HttpResponseRedirect
from django.utils.text import slugify



grandeur_mesure = (

    ('pression','Pression'),
    ('deplacement','Déplacement'),
    ('son','Son', ),
    ('humidite','Humidité', ),


)

grandeur_domaines = (

    ('aéronautique','Aéronautique'),
    ('automobile','Automobile'),
    ('son','Son', ),
    ('industrie_agroalimentaire','Industrie Agroalimentaire', ),
    ('industrie_alimentaire','Industrie Alimentaire', ),
    ('metallurgie','Métallurgie', ),
    ('production','Production énergie' , ),
    ('medical','Médical', ),

)

type_capteur = (

    ('filaire','Filaire'),
    ('sans_fil','Sans fil'),
    ('indétermine','indéterminé', ),
  
)



competances = (

    ('aéronautique','Aéronautique'),
    ('automobile','Automobile'),
    ('son','Son', ),
    ('industrie_agroalimentaire','Industrie Agroalimentaire', ),
    ('industrie_alimentaire','Industrie Alimentaire', ),
    ('metallurgie','Métallurgie', ),
    ('production','Production énergie' , ),
    ('medical','Médical', ),

)





class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)


class Subject(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name




class Domaine(models.Model):
    name = models.CharField(max_length=30)


    def __str__(self):
        return self.name



class TypeCapteur(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name













class Profile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    interests = models.ManyToManyField(Subject, related_name='interested_profile')
    image = models.ImageField(upload_to='media/', default='default.jpg', verbose_name=u"Figure associated with the product ", null=True)
    nom = models.CharField(max_length=270,verbose_name= u"Nom : ",  null=True, blank=True)
    prenom = models.CharField(max_length=270,verbose_name= u"Prénom : ",  null=True, blank=True)
    institution = models.CharField(max_length=100,verbose_name=u"Institution : ",   null=True, blank=True)
    composante = models.CharField(max_length=100,verbose_name=u"Composante : ",   null=True, blank=True)
    adresse_email = models.EmailField(max_length=100,verbose_name=u"Adresse email : ",   null=True, blank=True)
    discipline =  models.CharField(max_length=100, choices = grandeur_domaines, verbose_name=u"Domaine d'activité  :", default='Sélectionner', null=True, blank=True)
    fonction = models.CharField(max_length=270,verbose_name= u"Fonction : ",  null=True, blank=True)
    competances = models.CharField(max_length=100, choices = competances, verbose_name=u" Compétences :" , default='Sélectionner', null=True, blank=True)
    description = models.CharField(max_length=100000,null=True,verbose_name=u"Présentation  ", blank=True)
    adresse = models.CharField(max_length=100000,null=True,verbose_name=u"Adresse ", blank=True)
    numero_telephone = models.CharField(max_length=100000,null=True,verbose_name=u"Adresse ", blank=True)
    mots_cles = models.CharField(max_length=270,verbose_name= u"Mots clés : ",  null=True, blank=True)
    file_2 = models.FileField(upload_to='media/',verbose_name=u"Télecharger un de vos travaux ", null=True, blank=True )
    file_3 = models.FileField(upload_to='media/',verbose_name=u"Télecharger un de vos travaux ", null=True, blank=True )
    file_4 = models.FileField(upload_to='media/',verbose_name=u"Télecharger un de vos travaux ", null=True, blank=True )
    location = models.CharField(max_length=30, blank=True)
    birthdate = models.DateField(null=True,verbose_name=u"Votre date de naissance ", blank=True)
  


    def __str__(self):
        return f'{self.user.username} Profile'
    


        
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


class Quiz(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
    name = models.CharField(max_length=255,null=True, blank=True )
    titre_projet = models.CharField(max_length=100000,verbose_name=u"Intitulé du projet ")
    description_projet = models.TextField(max_length=100000,null=True,verbose_name=u"Description du projet  ", )
    type_evt = models.ForeignKey(TypeCapteur, on_delete=models.CASCADE, verbose_name=u"Type de l'événement à détecter  ", related_name='type_projets')
    domaine = models.ForeignKey(Domaine, on_delete=models.CASCADE,verbose_name= u"Domaine d'application du projet  ", related_name='domaines_projet')
    subject = models.ManyToManyField(Subject, verbose_name= u"Disciplines scientifiques nécessaires au projet ", related_name='projets')
    sensibilite = models.CharField(max_length=270,verbose_name= u"Sensibilité ",  null=True, blank=True)
    stabilite = models.CharField(max_length=270,verbose_name= u"Stabilité  ",  null=True, blank=True)
    selectivite = models.CharField(max_length=270,verbose_name= u"Sélectivité ",  null=True, blank=True)
    precision = models.CharField(max_length=270,verbose_name= u"Precision",  null=True, blank=True)
    gamme = models.CharField(max_length=270,verbose_name= u"Gamme  ",  null=True, blank=True)
    format_sortie = models.CharField(max_length=100,verbose_name=u"Format de sortie ",   null=True, blank=True)
    temps_reponse = models.CharField(max_length=270,verbose_name= u"Temps de réponse ",  null=True, blank=True)
    condition_ambiante = models.CharField(max_length=270,verbose_name= u"Conditions ambiantes ",  null=True, blank=True)
    cout = models.CharField(max_length=270,verbose_name= u"Coût ",  null=True, blank=True)
    poids = models.CharField(max_length=270,verbose_name= u"Dimensions ",  null=True, blank=True)
    taille= models.CharField(max_length=270,verbose_name= u"taille ",  null=True, blank=True)
    file_1 = models.FileField(upload_to='images/',verbose_name=u"Télécharger votre fichier 1 ", null=True, blank=True)
    file_2 = models.FileField(upload_to='images/',verbose_name=u"Télécharger votre fichier 2 ", null=True, blank=True)
    file_3 = models.ImageField(upload_to='images/',verbose_name=u"Figure associée au produit ", null=True, blank=True)
    confidentalite= models.BooleanField( verbose_name=u"Je souhaite que mon projet reste confidentiel ", default=False)
    finance = models.CharField(max_length=270,verbose_name= u"Finanacement : ",  null=True, blank=True)
    nom_1 = models.CharField(max_length=270,verbose_name= u"Nom : ",  null=True, blank=True)
    prenom_1 = models.CharField(max_length=270,verbose_name= u"Prénom : ",  null=True, blank=True)
    adresse_email_1 = models.EmailField(max_length=100,verbose_name=u"Adresse email : ",   null=True, blank=True)
    nom_2 = models.CharField(max_length=270,verbose_name= u"Nom : ",  null=True, blank=True)
    prenom_2 = models.CharField(max_length=270,verbose_name= u"Prénom : ",  null=True, blank=True)
    adresse_email_2 = models.EmailField(max_length=100,verbose_name=u"Adresse email : ",   null=True, blank=True)
    nom_3 = models.CharField(max_length=270,verbose_name= u"Nom : ",  null=True, blank=True)
    prenom_3= models.CharField(max_length=270,verbose_name= u"Prénom : ",  null=True, blank=True)
    adresse_email_3 = models.EmailField(max_length=100,verbose_name=u"Adresse email : ",   null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null= True)
    slug = models.SlugField(max_length=140, unique=True)
    

    def _get_unique_slug(self):
        slug = slugify(self.titre_projet)
        unique_slug = slug
        num = 1
        while Quiz.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug
 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titre_projet









class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    image = models.ImageField(upload_to='images/', default='default.jpg', verbose_name=u"Figure associée à votre profil", null=True)
    nom = models.CharField(max_length=270,verbose_name= u"Nom : ",  null=True, blank=True)
    prenom = models.CharField(max_length=270,verbose_name= u"Prénom : ",  null=True, blank=True)
    adresse_email = models.EmailField(max_length=100,verbose_name=u"Adresse email de contact : ",   null=True, blank=True)
    composante = models.CharField(max_length=100,verbose_name=u"Composante : ",   null=True, blank=True)
    fonction = models.CharField(max_length=270,verbose_name= u"Fonction : ",  null=True, blank=True)
    domaine = models.ManyToManyField(Domaine, verbose_name= u"Domaines d'applications  ", help_text=u"Relativement à vos activités professionnelles.", related_name='domaines_expert')
    interests = models.ManyToManyField(Subject, verbose_name= u"Disciplines scientifiques ", related_name='interested_student')
    expert= models.BooleanField( verbose_name=u"Je souhaite participer à des projet ", default=False)
   
    def get_unanswered_questions(self, quiz):
        answered_questions = self.quiz_answers \
            .filter(answer__question__quiz=quiz) \
            .values_list('answer__question__pk', flat=True)
        questions = quiz.questions.exclude(pk__in=answered_questions).order_by('text')
        return questions

    def __str__(self):
        return self.user.username































class Equipe(models.Model):
    name = models.CharField(max_length=270,verbose_name= u"Nom : ", default='gourpe1')
    quiz = models.OneToOneField(Quiz, on_delete=models.CASCADE,  related_name='equipes')
    nom_1 = models.CharField(max_length=270,verbose_name= u"Nom : ",  null=True, blank=True)
    prenom_1 = models.CharField(max_length=270,verbose_name= u"Prénom : ",  null=True, blank=True)
    adresse_email_1 = models.EmailField(max_length=100,verbose_name=u"Adresse email : ",   null=True, blank=True)
    nom_2 = models.CharField(max_length=270,verbose_name= u"Nom : ",  null=True, blank=True)
    prenom_2 = models.CharField(max_length=270,verbose_name= u"Prénom : ",  null=True, blank=True)
    adresse_email_2 = models.EmailField(max_length=100,verbose_name=u"Adresse email : ",   null=True, blank=True)
    nom_3 = models.CharField(max_length=270,verbose_name= u"Nom : ",  null=True, blank=True)
    prenom_3= models.CharField(max_length=270,verbose_name= u"Prénom : ",  null=True, blank=True)
    adresse_email_3 = models.EmailField(max_length=100,verbose_name=u"Adresse email : ",   null=True, blank=True)
    

    def __str__(self):
        if self.name==None:
           return "ERROR-CUSTOMER NAME IS NULL"
        return self.name








class Liste_Expert_Quiz(models.Model):
    name = models.CharField(max_length=270,verbose_name= u"Nom : ", default='gourpe1')
    quiz = models.OneToOneField(Quiz, on_delete=models.CASCADE,  related_name='projet')
    expert = models.OneToOneField(Student, on_delete=models.CASCADE,  related_name='student')
    created_at = models.DateTimeField(auto_now_add=True, null= True)

    def __str__(self):
        if self.name==None:
           return "ERROR-CUSTOMER NAME IS NULL"
        return self.name













    

class Capteur(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='capteurs')
    nom_capteur = models.CharField(max_length=270,verbose_name= u"Nom du capteur ",  null=True, blank=True)
    type_capteur = models.CharField(max_length=270,verbose_name= u"Type du capteur  ",  null=True, blank=True)
    description_projet = models.TextField(max_length=100000,verbose_name=u"Description du capteur ",null=True, blank=True)
    type_evt = models.ForeignKey(TypeCapteur, on_delete=models.CASCADE, related_name='type_capteurs')
    domaine = models.ManyToManyField(Domaine, verbose_name= u"Domaines d'application  ", related_name='domaines_capteur')
    subject = models.ManyToManyField(Subject, verbose_name= u"Mots Clés  ", related_name='capteurs')
    technologie_utilisee = models.CharField(max_length=270,verbose_name= u"Technologie utilisée",  null=True, blank=True)
    etendue = models.CharField(max_length=270,verbose_name= u"Etendue de mesure  ",  null=True, blank=True)
    sensibilite = models.CharField(max_length=270,verbose_name= u"Sensibilité ",  null=True, blank=True)
    resolution = models.CharField(max_length=270,verbose_name= u"Résolution ",  null=True, blank=True)
    precision = models.CharField(max_length=270,verbose_name= u"Précision  ",  null=True, blank=True)
    rapidite = models.CharField(max_length=270,verbose_name= u"Rapidité ",  null=True, blank=True)
    justesse = models.CharField(max_length=270,verbose_name= u"Justesse  ",  null=True, blank=True)
    reproductibilite = models.CharField(max_length=270,verbose_name= u"Reproductibilité ",  null=True, blank=True)
    temps_de_reponse = models.CharField(max_length=270,verbose_name= u"Temps de réponse   ",  null=True, blank=True)
    bande_passante = models.CharField(max_length=270,verbose_name= u"Bande passante   ",  null=True, blank=True)
    hysteresis = models.CharField(max_length=270,verbose_name= u"Hystérésis ",  null=True, blank=True)
    gamme_temperature = models.CharField(max_length=270,verbose_name= u"Gamme de température d'utilisation ",  null=True, blank=True)
    file_1 = models.ImageField(upload_to='images/',verbose_name=u"Figure associée au produit ", null=True, blank=True)
    file_2 = models.FileField(upload_to='images/',verbose_name=u"Télécharger votre fichier  ", null=True, blank=True)
    file_3 = models.FileField(upload_to='images/',verbose_name=u"Télécharger votre fichier  ", null=True, blank=True)
    confidentalite= models.BooleanField( verbose_name=u"Je souhaite que mon projet reste confidentiel ", default=False)
    created_at = models.DateTimeField(auto_now_add=True, null= True)
    slug = models.SlugField(max_length=140, unique=True)
    

    def _get_unique_slug(self):
        slug = slugify(self.nom_capteur)
        unique_slug = slug
        num = 1
        while Capteur.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug
 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom_capteur





class favoris_expert(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favoris')
    expert = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='expert_favoris')
    projet = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='projet_favoris')
    date = models.DateTimeField(auto_now_add=True)









class TakenExpert(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='taken_expert')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='taken_expert')
    date = models.DateTimeField(auto_now_add=True)





class ExpertListe(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experts')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_list')
    date = models.DateTimeField(auto_now_add=True)















class TakenQuiz(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='taken_quizzes')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='taken_quizzes')
    score = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)








class Comment(models.Model):
    post = models.ForeignKey(Quiz,on_delete=models.CASCADE,related_name='comments')
    user= models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    reply=  models.ForeignKey('Comment', blank=True, null=True, related_name="replies",on_delete=models.CASCADE)
    content = models.TextField(max_length=250, verbose_name="commentaire")
    timestamp = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return 'Comment {} by {}'.format(self.post.titre_projet, str(self.user.username))



class Comment_display(models.Model):
    post = models.ForeignKey(Capteur,on_delete=models.CASCADE,related_name='comments_capteur')
    user= models.ForeignKey(User,on_delete=models.CASCADE,related_name='User_comments_capteurs')
    reply=  models.ForeignKey('Comment_display', blank=True, null=True, related_name="replies_capteur",on_delete=models.CASCADE)
    content = models.TextField(max_length=250, verbose_name="commentaire")
    timestamp = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return 'Comment {} by {}'.format(self.post.nom_capteur, str(self.user.username))
















def unique_slugify(instance, value, slug_field_name='slug', queryset=None,
                   slug_separator='-'):
    """
    Calculates and stores a unique slug of ``value`` for an instance.

    ``slug_field_name`` should be a string matching the name of the field to
    store the slug in (and the field to check against for uniqueness).

    ``queryset`` usually doesn't need to be explicitly provided - it'll default
    to using the ``.all()`` queryset from the model's default manager.
    """
    slug_field = instance._meta.get_field(slug_field_name)

    slug = getattr(instance, slug_field.attname)
    slug_len = slug_field.max_length

    # Sort out the initial slug, limiting its length if necessary.
    slug = slugify(value)
    if slug_len:
        slug = slug[:slug_len]
    slug = _slug_strip(slug, slug_separator)
    original_slug = slug

    # Create the queryset if one wasn't explicitly provided and exclude the
    # current instance from the queryset.
    if queryset is None:
        queryset = instance.__class__._default_manager.all()
    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    # Find a unique slug. If one matches, at '-2' to the end and try again
    # (then '-3', etc).
    next = 2
    while not slug or queryset.filter(**{slug_field_name: slug}):
        slug = original_slug
        end = '%s%s' % (slug_separator, next)
        if slug_len and len(slug) + len(end) > slug_len:
            slug = slug[:slug_len-len(end)]
            slug = _slug_strip(slug, slug_separator)
        slug = '%s%s' % (slug, end)
        next += 1

    setattr(instance, slug_field.attname, slug)


def _slug_strip(value, separator='-'):
    """
    Cleans up a slug by removing slug separator characters that occur at the
    beginning or end of a slug.

    If an alternate separator is used, it will also replace any instances of
    the default '-' separator with the new separator.
    """
    separator = separator or ''
    if separator == '-' or not separator:
        re_sep = '-'
    else:
        re_sep = '(?:-|%s)' % re.escape(separator)
    # Remove multiple instances and if an alternate separator is provided,
    # replace the default '-' separator.
    if separator != re_sep:
        value = re.sub('%s+' % re_sep, separator, value)
    # Remove separator from the beginning and end of the slug.
    if separator:
        if separator != '-':
            re_sep = re.escape(separator)
        value = re.sub(r'^%s+|%s+$' % (re_sep, re_sep), '', value)
    return value


class Forum(models.Model):
    post = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='cases_public', null = True)
    created_at = models.DateTimeField(default=timezone.now,verbose_name=u"The publication date")


class Collaboration_actuelle(models.Model):
    LOW = 0
    NORMAL = 1
    HIGH = 2
    STATUS_CHOICES = (
    (LOW, 'En cours'),
    (NORMAL, 'Confirmée'),
    (HIGH, 'Refusée'), )
    porteur = models.ForeignKey(User, on_delete=models.CASCADE,  related_name='collaboration_porteur')
    expert = models.ForeignKey(User, on_delete=models.CASCADE,  related_name='collaboration_expert')
    projet = models.ForeignKey(Quiz, on_delete=models.CASCADE,  related_name='collaboration_projet')
    description_collaboration = models.TextField(max_length=250,null=True,verbose_name=u"Motivation  ", )
    statut = models.IntegerField(default=NORMAL, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True, null= True)




class Question(models.Model):
    qid = models.AutoField(primary_key=True)
    question_title = models.CharField(max_length=100)
    question_text = models.TextField(max_length=50000)
    date_posted = models.DateTimeField(auto_now_add=True)
    posted_by = models.TextField(max_length=20)
    slug = models.SlugField(max_length=40)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.question_title)
        super(Question, self).save(*args, **kwargs)





class Answer(models.Model):
    aid = models.AutoField(primary_key=True)
    qid = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField(max_length=50000)
    date_posted = models.DateTimeField(auto_now_add=True)
    posted_by = models.TextField(max_length=20)   