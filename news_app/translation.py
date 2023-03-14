from modeltranslation.translator import register
from modeltranslation.translator import TranslationOptions

from .models import News
from .models import Category


@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'body')


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)
