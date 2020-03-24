from django.shortcuts import render, redirect


from .models import *
from .forms import *
# .FORMS REFERS TO THE FORMS.PY IN CURRENT DIRECTORY AND * USED FOR IMPORTING EVERYTHING

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
import datetime

# HOME PAGE
def indice(request):
    return render(
        request,
        'indice.html',
    )


# VIEW THAT WILL RETURN LIST OF ALL BOOKS IN LIBRARY
@login_required
def BookListView(request):
    book_list = Book.objects.all()
    # MODELNAME.objects.all() is used to get all objects i.e. tuples from database
    return render(request, 'catalogo/book_list.html', locals())

@login_required
def Usuario_BookListView(request):
    usu=Usuario.objects.get(roll_no=request.user)
    bor=Borrower.objects.filter(usuario=usu)
    book_list=[]
    for b in bor:
        book_list.append(b.book)
    # MODELNAME.objects.all() is used to get all objects i.e. tuples from database
    return render(request, 'catalogo/book_list.html', locals())

#This view return detail of a particular book
#it also accepts a parameter pk that is the id  i.e. primary_key of book to identify it
#get_object_404 if object is not found then return 404 server error
#locals return a dictionary of loacl varibles
def BookDetailView(request, pk):
    book = get_object_or_404(Book, id=pk)
    reviews=Reviews.objects.filter(book=book).exclude(review="none")
    try:
        usu= Usuario.objects.get(roll_no=request.user)
        rr=Reviews.objects.get(review="none")
    except:
        pass
    return render(request, 'catalogo/book_detail.html', locals())



@login_required
def BookCreate(request):
    if not request.user.is_superuser:
        return redirect('indice')
    form = BookForm()
    if request.method == 'POST':
        form = BookForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect(index)
    return render(request, 'catalogo/form.html', locals())


@login_required
def BookUpdate(request, pk):
    if not request.user.is_superuser:
        return redirect('indice')
    obj = Book.objects.get(id=pk)
    form = BookForm(instance=obj)
    if request.method == 'POST':
        form = BookForm(data=request.POST, files=request.FILES, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return redirect(indice)
    return render(request, 'catalogo/form.html', locals())


@login_required
def BookDelete(request, pk):
    if not request.user.is_superuser:
        return redirect('indice')
    obj = get_object_or_404(Book, pk=pk)
    obj.delete()
    return redirect('indice')



@login_required
def usuario_request_issue(request, pk):
    obj = Book.objects.get(id=pk)
    stu = Usuario.objects.get(roll_no=request.user)
    s = get_object_or_404(Usuario, roll_no=str(request.user))
    if s.total_books_due < 10:
        message = "Has reservado el libro, Puedes ir a recogerlo"
        a = Borrower()
        a.usuario = s
        a.book = obj
        a.issue_date = datetime.datetime.now()
        obj.available_copies = obj.available_copies - 1
        obj.save()
        stu.total_books_due=stu.total_books_due+1
        stu.save()
        a.save()
    else:
        message = "Has excedido el límite de libros"
    return render(request, 'catalogo/result.html', locals())


@login_required
def UsuarioCreate(request):
    if not request.user.is_superuser:
        return redirect('indice')
    form = userForm()
    if request.method == 'POST':
        form = usertForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            s=form.cleaned_data['roll_no']
            form.save()
            u=User.objects.get(username=s)
            s=user.objects.get(roll_no=s)
            u.save()
            return redirect(indice)
    return render(request, 'catalogo/form.html', locals())


@login_required
def UsuarioUpdate(request, pk):
    if not request.user.is_superuser:
        return redirect('indice')
    obj = Usuario.objects.get(id=pk)
    form = UsuarioForm(instance=obj)
    if request.method == 'POST':
        form = UsuarioForm(data=request.POST, files=request.FILES, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return redirect(indice)
    return render(request, 'catalogo/form.html', locals())


@login_required
def UsuarioDelete(request, pk):
    obj = get_object_or_404(user, pk=pk)
    obj.delete()
    return redirect('indice')

@login_required
def UsuarioList(request):
    usuario = Usuario.objects.all()
    return render(request, 'catalogo/Usuario_list.html', locals())

@login_required
def UsuarioDetail(request, pk):
    usuario = get_object_or_404(Usuario, id=pk)
    books=Borrower.objects.filter(usuario=usuario)
    return render(request, 'catalogo/Usuario_detail.html', locals())




@login_required
def ret(request, pk):
    if not request.user.is_superuser:
        return redirect('indice')
    obj = Borrower.objects.get(id=pk)
    book_pk=obj.book.id
    usuario_pk=obj.usuario.id
    usuario = Usuario.objects.get(id=usuario_pk)
    usuario.total_books_due=usuario.total_books_due-1
    usuario.save()

    book=Book.objects.get(id=book_pk)
    rating = Reviews(review="none", book=book,usuario=usuario,rating='2.5')
    rating.save()
    book.available_copies=book.available_copies+1
    book.save()
    obj.delete()
    return redirect('indice')


import re

from django.db.models import Q

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
    '''
    query = None # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query
def search_book(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        entry_query = get_query(query_string, ['title', 'summary','author'])

        book_list= Book.objects.filter(entry_query)

    return render(request,'catalogo/book_list.html',locals() )
def search_user(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        entry_query = get_query(query_string, ['roll_no','name'])

        usuario = Usuario.objects.filter(entry_query)

    return render(request,'catalogo/Usuario_list.html',locals())




@login_required
def RatingUpdate(request, pk):
    obj =Reviews.objects.get(id=pk)
    form = RatingForm(instance=obj)
    if request.method == 'POST':
        form = RatingForm(data=request.POST, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return redirect('book-detail',pk=obj.book.id)
    return render(request, 'catalogo/form.html', locals())


@login_required
def RatingDelete(request, pk):
    obj = get_object_or_404(Reviews, pk=pk)
    st=user.objects.get(roll_no=request.user)
    if not st==obj.user:
        return redirect('indice')
    pk = obj.book.id
    obj.delete()
    return redirect('book_detail',pk)
# Create your views here.
