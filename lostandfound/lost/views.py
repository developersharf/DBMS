from django.shortcuts import render, redirect, get_object_or_404
from .models import LostItem
from django.db import connection
from .forms import LostItemForm
from datetime import datetime
from django.core.paginator import Paginator
from django.utils.dateparse import parse_date
from lost.models import LostItem
from .utils import calculate_match_score
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def user_lost_items(request):
    items = LostItem.objects.filter(user=request.user)
    return render(request, 'lost/user_lost_items.html', {'items': items})


def lost_detail(request, id):
    lost_item = get_object_or_404(LostItem, id=id)
    return render(request, 'lost/lost_detail.html', {'item': lost_item})

@login_required
def submit_lost_item(request):
    if request.method == 'POST':
        # Inject the logged-in user's email into the POST data (safeguard)
        post_data = request.POST.copy()
        post_data['user_email'] = request.user.email

        form = LostItemForm(post_data)
        if form.is_valid():
            data = form.cleaned_data
            user_id = request.user.id

            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO lost_lostitem (user_email, title, description, date_lost, location, submitted_at, user_id)
                    VALUES (%s, %s, %s, %s, %s, NOW(), %s)
                """, [
                    request.user.email,
                    data['title'],
                    data['description'],
                    data['date_lost'],
                    data['location'],
                    user_id
                ])
            return redirect('/')
    else:
        form = LostItemForm(initial={'user_email': request.user.email})

    return render(request, 'lost/submit.html', {'form': form})


def list_lost_items(request):
    page = int(request.GET.get('page', 1))
    per_page = 5
    offset = (page - 1) * per_page

    search_query = request.GET.get('q', '')
    location_filter = request.GET.get('location', '')
    date_filter = request.GET.get('date', '')

    filters = []
    params = []

    if search_query:
        filters.append("(title ILIKE %s OR description ILIKE %s)")
        params += [f"%{search_query}%", f"%{search_query}%"]
    if location_filter:
        filters.append("location ILIKE %s")
        params.append(f"%{location_filter}%")
    if date_filter:
        filters.append("date_lost = %s")
        params.append(parse_date(date_filter))

    where_clause = "WHERE " + " AND ".join(filters) if filters else ""

    with connection.cursor() as cursor:
        cursor.execute(f"""
            SELECT id, user_email, title, date_lost, location, description
            FROM lost_lostitem
            {where_clause}
            ORDER BY submitted_at DESC
            LIMIT %s OFFSET %s
        """, params + [per_page, offset])
        items = cursor.fetchall()

        cursor.execute(f"SELECT COUNT(*) FROM lost_lostitem {where_clause}", params)
        total_items = cursor.fetchone()[0]

    total_pages = (total_items + per_page - 1) // per_page
    page_range = list(range(1, total_pages + 1))

    return render(request, 'lost/list.html', {
    'items': items,
    'page': page,
    'total_pages': total_pages,
    'page_range': page_range,
    'search_query': search_query,
    'location_filter': location_filter,
    'date_filter': date_filter,
    'total_lost': total_items,
    'location_choices': LostItem.LOCATION_CHOICES,
})




def match_found_items(request, lost_id):
    with connection.cursor() as cursor:
        # Get the lost item
        cursor.execute("SELECT id, title, description, location, date_lost FROM lost_lostitem WHERE id = %s", [lost_id])
        lost_item_row = cursor.fetchone()
        if not lost_item_row:
            return render(request, '404.html', status=404)

        lost_item = {
            'id': lost_item_row[0],
            'title': lost_item_row[1],
            'description': lost_item_row[2],
            'location': lost_item_row[3],
            'date_lost': lost_item_row[4]
        }

        # Get all found items
        cursor.execute("SELECT id, title, description, location, date_found FROM found_founditem")
        found_rows = cursor.fetchall()

        matches = []
        for row in found_rows:
            found_item = {
                'id': row[0],
                'title': row[1],
                'description': row[2],
                'location': row[3],
                'date_found': row[4]
            }
            score = calculate_match_score(lost_item, found_item)
            matches.append((found_item, score))

        # Sort matches by score descending
        matches.sort(key=lambda x: x[1], reverse=True)

    return render(request, 'lost/match_results.html', {
        'lost_item': lost_item,
        'matches': matches,
    })
    
    
    
    
    
    
@login_required
def edit_lost_item(request, id):
    item = get_object_or_404(LostItem, id=id, user=request.user)

    if request.method == 'POST':
        form = LostItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Item updated successfully.")
            return redirect('user_lost_items')
    else:
        form = LostItemForm(instance=item)

    return render(request, 'lost/edit_lost_item.html', {'form': form})


@login_required
def delete_lost_item(request, id):
    item = get_object_or_404(LostItem, id=id, user=request.user)

    if request.method == 'POST':
        item.delete()
        messages.success(request, "Item deleted successfully.")
        return redirect('user_lost_items')

    return render(request, 'lost/confirm_delete.html', {'item': item})