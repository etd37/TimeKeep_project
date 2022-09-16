from datetime import datetime, timezone
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from project.models import Project, Entry
from team.models import Team


def start_timer(request):
    print(request.user)
    print(datetime.now())
    entry = Entry.objects.create(
        team_id=request.user.userprofile.active_team_id,
        minutes=0,
        created_by=request.user,
        is_tracked=False,
        created_at=datetime.now()
    )

    print(entry)

    return JsonResponse({'success': True})


def stop_timer(request):
    entry = Entry.objects.get(
        team_id=request.user.userprofile.active_team_id,
        created_by=request.user,
        minutes=0,
        is_tracked=False
    )

    tracked_minutes = int(
        (
                datetime.now(timezone.utc) - entry.created_at
        ).total_seconds() / 60
    )

    if tracked_minutes < 1:
        tracked_minutes = 1

    entry.minutes = tracked_minutes
    entry.is_tracked = False
    entry.save()

    return JsonResponse({'success': True, 'entryID': entry.id})


def discard_timer(request):
    entries = Entry.objects.filter(
        team_id=request.user.userprofile.active_team_id,
        created_by=request.user,
        is_tracked=False
    ).order_by('-created_at')

    if entries:
        entry = entries.first()
        entry.delete()

    return JsonResponse({'success': True})
