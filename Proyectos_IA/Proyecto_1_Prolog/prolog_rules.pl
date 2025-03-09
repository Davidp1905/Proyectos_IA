% # Recomendar un libro con la categoría
recommend_book(user,recommended_book) :-
    sale(user,bought_book),
    book_category(bought_book,category),
    book_category(recommended_book,category),
    bought_book \= recommended_book. % # Esto hace que no recomiende el mismo libro
    \+ sale(user,bought_book). %# Esto hace que no recomiende un libro que ya compró el usuario

% # Recomendar una lista de libros
recommend_list(user,book_list) :-
    findall(recommended_book,recommend_book(user,recommended_book),book_list). %# Usa la regla anterior para hacer una lista de todos los libros recomendados

%# Después sigo XD