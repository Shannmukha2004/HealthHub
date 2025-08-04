from django.shortcuts import render, redirect,get_object_or_404
from .models import Tip
from .forms import TipForm
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    tips = Tip.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'tips/dashboard.html', {'tips': tips})

@login_required
def create_tip(request):
    if request.method == 'POST':
        form = TipForm(request.POST)
        if form.is_valid():
            tip = form.save(commit=False)
            tip.user = request.user
            tip.save()
            return redirect('dashboard')
    else:
        form = TipForm()
    return render(request, 'tips/create_tip.html', {'form': form})
def edit_tip(request, pk):
    tip = get_object_or_404(Tip, pk=pk)
    if request.method == 'POST':
        form = TipForm(request.POST, instance=tip)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect to home or list page
    else:
        form = TipForm(instance=tip)
    return render(request, 'tips/edit_tip.html', {'form': form})
def delete_tip(request, pk):
    tip = get_object_or_404(Tip, pk=pk)
    if request.method == 'POST':
        tip.delete()
        return redirect('dashboard')
    return render(request, 'tips/confirm_delete.html', {'tip': tip})
