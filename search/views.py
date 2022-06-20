
import requests

from django.utils import dateparse
from django.conf import settings
from django.shortcuts import render

from .models import Videos
from .serializers import VideosSerializer

from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination


from youtube_search.settings import YOUTUBE_DATA_API_KEY

#function to search and store youtube videos
def index(request):

    #list to store the first 9 videos which will be displayed on each search
    videos = []

    if request.method == 'POST': 
      search_url = 'https://www.googleapis.com/youtube/v3/search'
      video_url = 'https://www.googleapis.com/youtube/v3/videos'

      #defining the parameters for the search results
      search_params={
          'part' : 'snippet',
          'q' : request.POST['search'],
          'key' : settings.YOUTUBE_DATA_API_KEY,
          'maxResults' : 9,
          'type': 'video',
          'order' : 'date',
          'publishedAfter' : '2018-01-01T00:00:00Z'
       }

      r= requests.get(search_url, params=search_params)

      results = r.json()['items']


      # storing video ids of the first 9 results
      video_ids = []
      for result in results:
          video_ids.append(result['id']['videoId'])
      
      video_params = {
          'key' : YOUTUBE_DATA_API_KEY,
          'part' : 'snippet, contentDetails',
          'id' : ','.join(video_ids),
          'maxResults' : 9,
       }

      r = requests.get(video_url, params=video_params)

      results = r.json()['items']

      # extracting the required details from the 9 videos
      for result in results:
            
            title = result['snippet']['title']
            duration = round(dateparse.parse_duration(result['contentDetails']['duration']).total_seconds()/60,2)
            date = result['snippet']['publishedAt']
            description = result['snippet']['description']
            thumbnail = result['snippet']['thumbnails']['high']['url']
            video_data = {
             'title' : title,
             'id' : result['id'],
             'duration' : duration,
             'date' : date,
             'description' : description,
             'thumbnail': thumbnail,
             'url' : f'https://www.youtube.com/watch?v={result["id"]}',
            }

            #storing each result in the database
            Videos.objects.create(title=title,duration=duration,date=date,thumbnail=thumbnail,description=description)

            videos.append(video_data)
    
    # storing the search results of the videos to be displayed
    context = {
        'videos' : videos
    }

    return render(request,'search/index.html',context)



# class to create a paginated list of the database
class VideoList(generics.ListAPIView):
    queryset = Videos.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    search_fields = ['title']
    filter_fields = ['description']

    ordering = ['-date']
    serializer_class = VideosSerializer
    pagination_class = PageNumberPagination