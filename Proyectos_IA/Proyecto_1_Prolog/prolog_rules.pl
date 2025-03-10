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
    findall(User-TopBooks, (  % Encuentra la lista de favoritos para cada usuario
        member(User, Users),   % Itera sobre cada usuario en la lista "Users"
        
        % Obtiene todos los libros calificados por el usuario con rating > 3
        findall(Book-Rating, (
            rating(User, Book, Rating),
            Rating > 3  % Filtra solo libros con calificación mayor a 3
        ), BooksWithRatings),

        % Ordena los libros por calificación de mayor a menor
        sort(2, @>=, BooksWithRatings, SortedBooks),

        % Extrae solo los primeros 10 libros de la lista ordenada
        extract_books(SortedBooks, 10, TopBooks)
    ), Resultados).

% Regla auxiliar: Extrae los primeros N libros de la lista.
% Cuando N llega a 0, se devuelve una lista vacía.
extract_books(_, 0, []). 

% Si la lista de libros está vacía antes de llegar a N, se devuelve una lista vacía.
extract_books([], _, []). 

% Caso recursivo: Se toma el primer libro de la lista y se reduce N en 1.
extract_books([Book-_|T], N, [Book|R]) :-
    N > 0,
    N1 is N - 1,
    extract_books(T, N1, R).