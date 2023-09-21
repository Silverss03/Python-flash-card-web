<<<<<<< HEAD
from django import template

from cards.models import BOXES, Card

register = template.Library()

@register.inclusion_tag("cards/box_links.html")
def boxes_as_links():
    boxes = []
    for box_num in BOXES:
        card_count = Card.objects.filter(box=box_num).count()
        boxes.append({
            "number": box_num,
            "card_count": card_count,
        })

=======
from django import template

from cards.models import BOXES, Card

register = template.Library()

@register.inclusion_tag("cards/box_links.html")
def boxes_as_links():
    boxes = []
    for box_num in BOXES:
        card_count = Card.objects.filter(box=box_num).count()
        boxes.append({
            "number": box_num,
            "card_count": card_count,
        })

>>>>>>> ea6e64420570d12c6036e759196c37fe4b20cb06
    return {"boxes": boxes}