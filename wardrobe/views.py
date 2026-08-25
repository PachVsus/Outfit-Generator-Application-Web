from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .constants import CLOTHING_TYPES, STYLES
from .forms import GarmentForm, GeneratorForm, OutfitSaveForm
from .models import Garment, Outfit
from .services import generate_outfit


def home(request):
    if request.user.is_authenticated:
        return redirect("wardrobe:dashboard")
    return render(request, "home.html")


@login_required
def dashboard(request):
    garments = request.user.garments.all()
    context = {
        "garment_count": garments.count(),
        "outfit_count": request.user.outfits.count(),
        "category_count": garments.values("clothing_type").distinct().count(),
        "recent_garments": garments[:4],
        "recent_outfits": request.user.outfits.prefetch_related("garments")[:3],
    }
    return render(request, "wardrobe/dashboard.html", context)


@login_required
def garment_list(request):
    garments = request.user.garments.all()
    search = request.GET.get("q", "").strip()
    clothing_type = request.GET.get("type", "")
    style = request.GET.get("style", "")
    if search:
        garments = garments.filter(Q(name__icontains=search) | Q(main_color__icontains=search) | Q(secondary_color__icontains=search))
    if clothing_type:
        garments = garments.filter(clothing_type=clothing_type)
    if style:
        garments = garments.filter(style=style)
    return render(request, "wardrobe/garment_list.html", {
        "garments": garments,
        "clothing_types": CLOTHING_TYPES,
        "styles": STYLES,
        "filters": {"q": search, "type": clothing_type, "style": style},
    })


@login_required
def garment_create(request):
    form = GarmentForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        garment = form.save(commit=False)
        garment.owner = request.user
        garment.save()
        messages.success(request, f"{garment.name} was added to your wardrobe.")
        return redirect("wardrobe:garment_list")
    return render(request, "wardrobe/garment_form.html", {"form": form, "title": "Add a garment", "submit_label": "Add to wardrobe"})


@login_required
def garment_update(request, pk):
    garment = get_object_or_404(Garment, pk=pk, owner=request.user)
    form = GarmentForm(request.POST or None, request.FILES or None, instance=garment)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"{garment.name} was updated.")
        return redirect("wardrobe:garment_list")
    return render(request, "wardrobe/garment_form.html", {"form": form, "garment": garment, "title": "Edit garment", "submit_label": "Save changes"})


@login_required
def garment_delete(request, pk):
    garment = get_object_or_404(Garment, pk=pk, owner=request.user)
    if request.method == "POST":
        name = garment.name
        garment.delete()
        if request.headers.get("HX-Request") == "true":
            return HttpResponse(status=204)
        messages.success(request, f"{name} was removed from your wardrobe.")
        return redirect("wardrobe:garment_list")
    return render(request, "wardrobe/garment_confirm_delete.html", {"garment": garment})


@login_required
def generator(request):
    form = GeneratorForm(request.POST or None)
    selected = []
    if request.method == "POST" and form.is_valid():
        selected = generate_outfit(request.user.garments.all(), **form.cleaned_data)
        request.session["generated_outfit"] = [garment.pk for garment in selected]
        request.session["generated_filters"] = form.cleaned_data
        context = {"selected": selected, "save_form": OutfitSaveForm(), "filters": form.cleaned_data}
        if request.headers.get("HX-Request") == "true":
            return render(request, "wardrobe/partials/generated_outfit.html", context)
    return render(request, "wardrobe/generator.html", {"form": form, "selected": selected, "save_form": OutfitSaveForm()})


@login_required
def save_generated_outfit(request):
    if request.method != "POST":
        return redirect("wardrobe:generator")
    garment_ids = request.session.get("generated_outfit", [])
    filters = request.session.get("generated_filters", {"style": "Any", "weather": "Any"})
    garments = request.user.garments.filter(pk__in=garment_ids)
    if not garment_ids or garments.count() != len(set(garment_ids)):
        messages.error(request, "Generate an outfit before saving it.")
        return redirect("wardrobe:generator")
    form = OutfitSaveForm(request.POST)
    if form.is_valid():
        outfit = Outfit.objects.create(
            owner=request.user,
            name=form.cleaned_data["name"],
            style=filters.get("style", "Any"),
            weather=filters.get("weather", "Any"),
        )
        outfit.garments.set(garments)
        request.session.pop("generated_outfit", None)
        request.session.pop("generated_filters", None)
        messages.success(request, "Your outfit was saved.")
        return redirect("wardrobe:outfit_detail", pk=outfit.pk)
    messages.error(request, "Please check the outfit name.")
    return redirect("wardrobe:generator")


@login_required
def outfit_list(request):
    outfits = request.user.outfits.prefetch_related("garments")
    return render(request, "wardrobe/outfit_list.html", {"outfits": outfits})


@login_required
def outfit_detail(request, pk):
    outfit = get_object_or_404(Outfit.objects.prefetch_related("garments"), pk=pk, owner=request.user)
    return render(request, "wardrobe/outfit_detail.html", {"outfit": outfit})


@login_required
def outfit_delete(request, pk):
    outfit = get_object_or_404(Outfit, pk=pk, owner=request.user)
    if request.method == "POST":
        outfit.delete()
        messages.success(request, "The saved outfit was deleted.")
        return redirect("wardrobe:outfit_list")
    return render(request, "wardrobe/outfit_confirm_delete.html", {"outfit": outfit})
