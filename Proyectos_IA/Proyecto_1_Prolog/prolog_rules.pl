% Recomendar un libro con la categoría
recommend_book(User, RecommendedBook) :-
    sale(User, BoughtBook),
    book_category(BoughtBook, Category),
    book_category(RecommendedBook, Category),
    BoughtBook \= RecommendedBook, % Esto hace que no recomiende el mismo libro
    \+ sale(User, RecommendedBook). % Esto hace que no recomiende un libro que ya compró el usuario
 
% Recomendar una lista de libros
recommend_list(User, BookList) :-
    findall(RecommendedBook, recommend_book(User, RecommendedBook), BookList). %  Usa la regla anterior para hacer una lista de todos los libros recomendados
    
% Encontrar usuarios con gustos similares
similar_users(User, SimilarUser) :-
    sale(User, Book),
    sale(SimilarUser, Book),
    User \= SimilarUser. % Esto hace que no se recomiende el mismo usuario
    
%top_10_favoritos([andres, luis, karen], TopLibros).
top_10_favoritos(Users, Resultados) :-
    findall(User-TopBooks, (
        member(User, Users),
        findall(Book-Rating, (
            rating(User, Book, Rating),
            Rating > 3
        ), BooksWithRatings),
        sort(2, @>=, BooksWithRatings, SortedBooks),  % Ordena por rating de mayor a menor
        extract_books(SortedBooks, 10, TopBooks)      % Extrae solo los primeros 10 libros
    ), Resultados).

% Extrae solo los primeros N libros de la lista
extract_books(_, 0, []).
extract_books([], _, []).
extract_books([Book-_|T], N, [Book|R]) :-
    N > 0,
    N1 is N - 1,
    extract_books(T, N1, R).

% Encontrar libros con rating mayor a 3
top_books(BookList) :-
    findall(Book, rating(_, Book, Rating), Books),
    findall(Book-Rating, (member(Book, Books), Rating > 3), BookList).