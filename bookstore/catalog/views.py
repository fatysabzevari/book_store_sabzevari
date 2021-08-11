# from django.shortcuts import get_object_or_404, render_to_response
# from .models import Category, Books
# from django.template import RequestContext
#
# def index(request, template_name="catalog/index.html"):
#  page_title = 'کتاب فروشی آنلاین'
#     return render_to_response(template_name, locals(),
#     context_instance=RequestContext(request))
# def show_category(request, category_slug, template_name="catalog/category.html"):
#     c = get_object_or_404(Category, slug=category_slug)
#     books = c.books_set.all()
#     page_title = c.name
#     meta_keywords = c.meta_keywords
#     meta_description = c.meta_description
#
#  return render_to_response(template_name, locals(),
#      context_instance = RequestContext(request))
#
#  def show_product(request, books_slug, template_name="catalog/books.html"):
#      b = get_object_or_404(Books, slug=books_slug)
#      categories = p.categories.filter(is_active=True)
#      page_title = p.name
#      meta_keywords = p.meta_keywords
#      meta_description = p.meta_description
#      return render_to_response(template_name, locals(),
#      context_instance = RequestContext(request))