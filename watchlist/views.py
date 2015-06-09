from django.http import *
from django.shortcuts import *
from django.utils import simplejson
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.messages import add_message
from django.contrib import messages
from django.db.models import *


from kenstream.settings import *
from ua_detector.views  import *
from ua_detector.generic_views import *
from django.views.generic.base import RedirectView
from django.core.urlresolvers import reverse_lazy,resolve
from ua_detector.model_views import *

from .utils import generic_search
from watchlist.models import *
from watchlist.forms import *

def clone(self):
    return copy.copy(self)

sql = Movie.objects.all().order_by('-timestamp')

QUERY="search-query"

MODEL_MAP = {
   Movie :['title','genre'],
   Genre: ['name',]
}

def search(request):
    objects = []

    for model,fields in MODEL_MAP.iteritems():
        objects+=generic_search(request,model,fields,QUERY)
        return render_to_response(
        "search_results.html",
        {"objects":objects,"search_string" : request.GET.get(QUERY,""),
                              }
        )

class WatchListView(ModelListView):
      model = Movie
      template_name = 'movie_list.html'
      mobile_template_name = 'm_movie_list.html'
      
      def get_queryset(self):
          queryset = sql
          return queryset
          
class DiscoverListView(ModelListView):
      model = Movie
      template_name = 'user_list.html'
      mobile_template_name = 'm_user_list.html'
      
      def get_queryset(self):
          queryset = sql.filter(editors_pick=False)
          return queryset
          
      
class WatchDetailView(MobileDetailView):
      template_name = 'movie_detail.html'
      mobile_template_name = 'm_movie_detail.html'
      context_object_name = 'movie'
      model = Movie
      
      def get_context_data(self,**kwargs):
        context= super(WatchDetailView,self).get_context_data(**kwargs)
        return context 
      
class PostReview(ModelCreateView):
      model = Movie
      form_class = SimpleForm
      template_name = 'movie_form.html'
      mobile_template_name = 'm_movie_form.html'
      success_url = reverse_lazy('watchlist')#with edit options
    
      def form_valid(self, form):
          form.instance.user = self.request.user 
          return super(PostReview, self).form_valid(form)
          
          

class EditReview(ModelUpdateView):
      model = Movie
      form_class = SimpleForm
      template_name = 'movie_form.html'
      mobile_template_name = 'm_movie_form.html'
      success_url = reverse_lazy('watchlist')#with edit options
    
      def form_valid(self, form):
          form.instance.user = self.request.user 
          return super(EditReview, self).form_valid(form)
      
      
class DeleteReview(ModelDeleteView):
      model = Movie
      form_class = SimpleForm
      template_name = 'movie_form.html'
      mobile_template_name = 'm_movie_form.html'
      success_url = reverse_lazy('watchlist')#with edit options
    
      def form_valid(self, form):
          form.instance.user = self.request.user 
          return super(DeleteReview, self).form_valid(form)
          
class GenreListView(ModelListView):
      model = Movie
      template_name = 'genre_list.html'
      mobile_template_name = 'm_genre_list.html'
      
      def get_queryset(self):
          #queryset = movies.order_by('genre')
          queryset = Movie.objects.all().order_by('genre')
          return queryset
          
class TvShowsListView(ModelListView):
      model = Movie
      template_name = 'tvshows_list.html'
      mobile_template_name = 'm_tvshows_list.html'
      
      def get_queryset(self):
          #queryset = movies.order_by('genre')
          queryset = Movie.objects.filter(genre__name__icontains='t.v show')
          return queryset
          
class ClassicsListView(ModelListView):
      model = Movie
      template_name = 'classics_list.html'
      mobile_template_name = 'm_classics_list.html'
      
      def get_queryset(self):
          #queryset = movies.filter(genre__name__icontains='classics')
          queryset = Movie.objects.filter(genre__name__icontains='classics')
          return queryset
          
class SeriesListView(ModelListView):
      model = Movie
      template_name = 'series_list.html'
      mobile_template_name = 'm_series_list.html'
      
      def get_queryset(self):
          #queryset = movies.filter(genre__name__icontains='series')
          queryset = Movie.objects.filter(genre__name__icontains='series')
          return queryset
          
class DocumentariesListView(ModelListView):
      model = Movie
      template_name = 'documentaries_list.html'
      mobile_template_name = 'm_documentaries_list.html'
      
      def get_queryset(self):
          #queryset = movies.filter(genre__name__icontains='documentaries')
          queryset = Movie.objects.filter(genre__name__icontains='documentaries')
          return queryset
          
          
def like(request):
    vars = {}
    if request.method == 'POST':
        user = request.user
        slug = request.POST.get('slug', None)
        company = get_object_or_404(Movie, slug=slug)

        liked, created = Like.objects.create(movie=movie)

        try:
            user_liked = Like.objects.get(movie=movie, user=user)
        except:
            user_liked = None

        if user_liked:
            user_liked.total_likes -= 1
            liked.user.remove(request.user)
            user_liked.save()
        else:
            liked.user.add(request.user)
            liked.total_likes += 1
            liked.save()


    return HttpResponse(simplejson.dumps(vars),
           mimetype='application/javascript'
           )
          

"""
class PostReviewWizard(SessionWizardView):
      template_name = 'wizard_form.html'
      mobile_template_name = 'm_wizard_form.html'
      
      def get_form(self, step=None, data=None, files=None):
          form = super(PostReviewWizard, self).get_form(step, data, files)
          form.instance.user = self.request.user
          return form
          
      def get_form_step_files(self, form):
          #trigger task for uploading files 
          return form.files 
             
      def done(self, form_list, **kwargs):
          #form.instance.user = self.request.user
          return HttpResponseRedirect(reverse_lazy('preview'))
          
          
class PreviewPost(ModelListView):
      model = Movie
      template_name = 'preview_list.html'
      mobile_template_name = 'm_preview_list.html'
      
      def get_queryset(self):
          queryset = Movie.objects.filter(user=self.request.user)[:1]
          return queryset
          #then user has the option to edit/proceed

"""                
