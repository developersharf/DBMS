from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from .forms import FoundItemForm
from datetime import datetime
from .models import FoundItem
from django.contrib.auth.decorators import login_required
from django.contrib import messages



@login_required
def user_found_items_view(request):
    items = FoundItem.objects.filter(user=request.user)
    return render(request, 'found/user_found_items.html', {'items': items})


@login_required
def submit_found_item(request):
    if request.method == 'POST':
        post_data = request.POST.copy()
        post_data['finder_email'] = request.user.email

        form = FoundItemForm(post_data)  # optional, if using forms
        if form.is_valid():
            data = form.cleaned_data
            user_id = request.user.id

            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO found_founditem (finder_email, title, description, date_found, location, submitted_at, user_id)
                    VALUES (%s, %s, %s, %s, %s, NOW(), %s)
                """, [
                    request.user.email,
                    data['title'],
                    data['description'],
                    data['date_found'],
                    data['location'],
                    user_id
                ])
            return redirect('/')
    else:
        form = FoundItemForm(initial={'finder_email': request.user.email})

    return render(request, 'found/submit.html', {'form': form})


# def list_found_items(request):
#     with connection.cursor() as cursor:
#         cursor.execute("""
#                SELECT id, finder_email, title, date_found, location, description
#             FROM found_founditem
#             ORDER BY submitted_at DESC
#         """)
#         items = cursor.fetchall()
#     return render(request, 'found/list.html', {'items': items})

# # 

def list_found_items(request):
    try:
        page = max(1, int(request.GET.get('page', 1)))
    except ValueError:
        page = 1

    per_page = 5
    offset = (page - 1) * per_page

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, finder_email, title, date_found, location, description
            FROM found_founditem
            ORDER BY submitted_at DESC
            LIMIT %s OFFSET %s
        """, [per_page, offset])
        items = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) FROM found_founditem")
        total_found = cursor.fetchone()[0]

        # cursor.execute("SELECT COUNT(*) FROM lost_lostitem")
        # total_lost = cursor.fetchone()[0]

    total_pages = (total_found + per_page - 1) // per_page
    page_range = list(range(1, total_pages + 1))

    return render(request, 'found/list.html', {
        'items': items,
        'page': page,
        'total_pages': total_pages,
        'page_range': page_range,
        # 'total_lost': total_lost,
        'total_found': total_found,
    })



def found_detail(request, id):
    found_item = get_object_or_404(FoundItem, id=id)
    return render(request, 'found/found_detail.html', {'item': found_item})


@login_required
def edit_found_item(request, id):
    item = get_object_or_404(FoundItem, id=id, user=request.user)

    if request.method == 'POST':
        form = FoundItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Item updated successfully.")
            return redirect('user_found_items')
    else:
        form = FoundItemForm(instance=item)

    return render(request, 'found/edit_found_item.html', {'form': form})


@login_required
def delete_found_item(request, id):
    item = get_object_or_404(FoundItem, id=id, user=request.user)

    if request.method == 'POST':
        item.delete()
        messages.success(request, "Item deleted successfully.")
        return redirect('user_found_items')

    return render(request, 'found/confirm_delete.html', {'item': item})