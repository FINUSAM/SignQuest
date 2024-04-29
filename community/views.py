from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import GroupModel, MessageModel

# Create your views here.

@login_required
def default_community(request):
    return redirect('community', 'universe')

@login_required
def community(request, group='main'):
    if request.method == 'POST':
        if group=='create_group':
            new_group_name = request.POST.get('new_group_name')
            if new_group_name:
                GroupModel.objects.create(group_name=new_group_name)
            else:
                print('xxxxxxxxxxxxxxxxxxxxxxx')
        elif group != 'main':
            message = request.POST.get('message')
            group_id = GroupModel.objects.get(group_name=group)
            MessageModel.objects.create(message=message, author=request.user, group=group_id)
        return redirect('community', group=group)
    else:
        groups = GroupModel.objects.all()
        if group == 'main' or group=='create_group':
            community_messages = None
        else:
            group_id = GroupModel.objects.get(group_name=group).id
            community_messages = MessageModel.objects.filter(group=group_id)
        return render(request, 'community/community.html', {'groups': groups, 'current_group': group, 'messages': community_messages}) 