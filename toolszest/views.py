from django.shortcuts import render

# Create your views here.

def image_resizer_stage(request):
	context={}
	return render(request, "tools/imager_resizer.html", context)