# checklist/context_processors.py

def check_user_groups(request):
    context = {
        'is_adm': False,
        'is_cuidador': False,
        'is_tutor': False,
    }
    
    if request.user.is_authenticated:
        context['is_adm'] = request.user.groups.filter(name='ADM').exists()
        context['is_cuidador'] = request.user.groups.filter(name='CUIDADOR').exists()
        context['is_tutor'] = request.user.groups.filter(name='TUTOR').exists()
        
    
    return context

