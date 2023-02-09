from django.views.generic import TemplateView


class DoublePlayerView(TemplateView):
    template_name = "sea_battle/double_player.html"
